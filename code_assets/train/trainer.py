"""Training loop with early stopping, checkpointing, and console progress.

Phase 7 compliant: per-epoch output matches the 12-field format specified
in docs/工作流与指南/论文工作流.md § Phase 7 实验训练进度输出规范.
"""
import os
import sys
import time
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch.utils.tensorboard import SummaryWriter
from eval.metrics import compute_metrics, AverageMeter

from utils.progress import (
    log_experiment_start, log_epoch, log_best_ckpt, log_experiment_end,
    EpochLogger, StdoutCapture,
)

try:
    from tqdm import tqdm
    _HAS_TQDM = True
except ImportError:
    _HAS_TQDM = False


def _to_device(data, device):
    if isinstance(data, (list, tuple)):
        return [d.to(device, non_blocking=True) if torch.is_tensor(d) else d
                for d in data]
    return data.to(device, non_blocking=True)


class EarlyStopping:
    """Early stopping with patience and best model restoration."""

    def __init__(self, patience=30, min_delta=0.0, mode='max'):
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.best_score = -float('inf') if mode == 'max' else float('inf')
        self.best_epoch = 0
        self.counter = 0
        self.early_stop = False

    def step(self, score, epoch=None):
        if self.mode == 'max':
            improved = score > self.best_score + self.min_delta
        else:
            improved = score < self.best_score - self.min_delta
        if improved:
            self.best_score = score
            self.best_epoch = epoch if epoch is not None else 0
            self.counter = 0
            return True
        self.counter += 1
        if self.counter >= self.patience:
            self.early_stop = True
        return False


class Trainer:
    """Standard single-task trainer with Phase 7 console progress.

    Args:
        model: nn.Module
        device: torch device
        config: dict with training hyperparams
        log_dir, checkpoint_dir: paths
        class_weights: tensor of per-class weights (optional)
        model_name: used in console progress banners
        phase: '7A' / '7B' / '7C' for progress labels
        progress_callback: optional fn(epoch_info) for custom progress handling
    """

    def __init__(self, model, device, config, log_dir="./logs",
                 checkpoint_dir="./checkpoints", class_weights=None,
                 model_name="Model", phase="7A"):
        self.model = model.to(device)
        self.device = device
        self.config = config
        self.log_dir = log_dir
        self.checkpoint_dir = checkpoint_dir
        self.model_name = model_name
        self.phase = phase

        os.makedirs(log_dir, exist_ok=True)
        os.makedirs(checkpoint_dir, exist_ok=True)

        self.writer = SummaryWriter(log_dir) if config.get('tensorboard', True) else None
        self.early_stopping = EarlyStopping(
            patience=config.get('early_stop_patience', 30), mode='max')

        lr = config.get('lr', 1e-3)
        wd = config.get('weight_decay', 1e-4)
        betas = tuple(config.get('betas', [0.9, 0.999]))
        self.optimizer = torch.optim.AdamW(
            model.parameters(), lr=lr, weight_decay=wd, betas=betas)

        self.scheduler = self._build_scheduler()
        self.class_weights = class_weights.to(device) if class_weights is not None else None
        self.label_smoothing = config.get('label_smoothing', 0.0)
        self.grad_clip = config.get('gradient_clip_norm', 1.0)
        self.use_amp = config.get('use_amp', False)
        self.scaler = torch.amp.GradScaler() if (device.type == 'cuda' and self.use_amp) else None

        self.best_metric = 0.0
        self.best_epoch = 0
        self.best_state = None

        # timing
        self._fit_start_time = 0.0
        self._epoch_times: list[float] = []

    def _build_scheduler(self):
        sched = self.config.get('scheduler', 'cosine_warm_restart')
        if sched == 'cosine_warm_restart':
            return torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
                self.optimizer, T_0=self.config.get('T_0', 20),
                T_mult=self.config.get('T_mult', 2))
        elif sched == 'cosine':
            return torch.optim.lr_scheduler.CosineAnnealingLR(
                self.optimizer, T_max=self.config.get('epochs', 200))
        elif sched == 'step':
            return torch.optim.lr_scheduler.StepLR(
                self.optimizer, step_size=50, gamma=0.5)
        return None

    def fit(self, train_loader, val_loader, epochs):
        """Full training loop with console progress output.

        Prints per-epoch lines matching the Phase 7 workflow spec
        (12 mandatory fields).

        Returns:
            dict with keys: best_metric, best_epoch, total_time, epoch_times,
                            early_stop_triggered, stopped_epoch
        """
        self._fit_start_time = time.time()
        self._epoch_times = []

        # ── experiment start banner ──
        init_lr = self.optimizer.param_groups[0]['lr']
        patience = self.config.get('early_stop_patience', 30)
        log_experiment_start(
            phase=self.phase,
            model_name=self.model_name,
            seed=self.config.get('seed', 0),
            device=str(self.device),
            batch_size=self.config.get('batch_size', 0),
            optimizer='AdamW',
            init_lr=init_lr,
            patience=patience,
            config_path=self.config.get('_config_path', 'configs/default.yaml'),
            commit_sha=self._get_commit_sha(),
            total_epochs=epochs,
        )

        early_stop_triggered = False
        stopped_epoch = epochs

        for epoch in range(epochs):
            ep_start = time.time()

            train_loss, train_acc = self._train_epoch(train_loader, epoch, epochs)
            val_loss, val_acc, val_metrics = self._validate(val_loader)

            if self.scheduler:
                if isinstance(self.scheduler, torch.optim.lr_scheduler.CosineAnnealingWarmRestarts):
                    self.scheduler.step(epoch)
                else:
                    self.scheduler.step()

            lr = self.optimizer.param_groups[0]['lr']
            ep_time = time.time() - ep_start
            self._epoch_times.append(ep_time)
            total_elapsed = time.time() - self._fit_start_time

            if self.writer:
                self.writer.add_scalar('Loss/train', train_loss, epoch)
                self.writer.add_scalar('Loss/val', val_loss, epoch)
                self.writer.add_scalar('Acc/train', train_acc, epoch)
                self.writer.add_scalar('Acc/val', val_acc, epoch)
                self.writer.add_scalar('LR', lr, epoch)

            improved = self.early_stopping.step(val_acc, epoch=epoch + 1)
            old_best = self.best_metric
            if improved:
                self.best_metric = val_acc
                self.best_epoch = epoch + 1
                self.best_state = {k: v.cpu().clone() for k, v in
                                   self.model.state_dict().items()}
                ckpt_path = os.path.join(self.checkpoint_dir, 'best.pth')
                self._save_checkpoint('best.pth', epoch, val_acc)
                log_best_ckpt(epoch + 1, old_best, val_acc, ckpt_path)

            # ── per-epoch console line (12-field format) ──
            remaining_epochs = max(0, epochs - (epoch + 1))
            avg_ep_time = (total_elapsed / (epoch + 1)) if self._epoch_times else ep_time
            eta = avg_ep_time * remaining_epochs

            gpu_alloc = None
            gpu_total = None
            if self.device.type == 'cuda':
                gpu_alloc = torch.cuda.memory_allocated(self.device) / (1024 * 1024)
                gpu_total = torch.cuda.get_device_properties(self.device).total_memory / (1024 * 1024)

            log_epoch(
                current_epoch=epoch + 1,
                total_epochs=epochs,
                train_loss=train_loss,
                val_loss=val_loss,
                val_acc=val_acc,
                val_f1=val_metrics.get('f1', 0.0),
                best_val_acc=self.best_metric,
                best_epoch=self.best_epoch,
                current_lr=lr,
                epoch_time=ep_time,
                total_elapsed=total_elapsed,
                eta=eta,
                train_acc=train_acc,
                gpu_mem_allocated=gpu_alloc,
                gpu_mem_total=gpu_total,
            )

            if self.early_stopping.early_stop:
                print(f'\n  EarlyStopping @ epoch {epoch+1}  patience={patience}  '
                      f'best={self.best_metric:.4f} @ epoch {self.best_epoch}',
                      flush=True)
                early_stop_triggered = True
                stopped_epoch = epoch + 1
                break

        # restore best weights
        if self.best_state is not None:
            self.model.load_state_dict(self.best_state)

        total_time = time.time() - self._fit_start_time
        return {
            'best_metric': self.best_metric,
            'best_epoch': self.best_epoch,
            'total_time': total_time,
            'epoch_times': self._epoch_times,
            'early_stop_triggered': early_stop_triggered,
            'stopped_epoch': stopped_epoch,
        }

    def _train_epoch(self, loader, epoch, total_epochs):
        self.model.train()
        loss_meter = AverageMeter()
        acc_meter = AverageMeter()

        for batch_idx, (x, y) in enumerate(self._iter_loader(loader, 'train', epoch, total_epochs)):
            x, y = x.to(self.device, non_blocking=True), y.to(self.device, non_blocking=True)

            self.optimizer.zero_grad()
            if self.scaler:
                with torch.amp.autocast('cuda'):
                    logits = self.model(x)
                    loss = self._loss_fn(logits, y)
                if not torch.isfinite(loss):
                    print(f"\n[WARN] NaN loss at batch {batch_idx}, skipping", flush=True)
                    continue
                self.scaler.scale(loss).backward()
                self.scaler.unscale_(self.optimizer)
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.grad_clip)
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                logits = self.model(x)
                loss = self._loss_fn(logits, y)
                if not torch.isfinite(loss):
                    print(f"\n[WARN] NaN loss at batch {batch_idx}, skipping", flush=True)
                    continue
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.grad_clip)
                self.optimizer.step()

            preds = logits.argmax(dim=1)
            acc = (preds == y).float().mean()
            loss_meter.update(loss.item(), x.size(0))
            acc_meter.update(acc.item(), x.size(0))

        return loss_meter.avg, acc_meter.avg

    def _iter_loader(self, loader, mode, epoch, total_epochs):
        """Iterate loader. Batch-level tqdm suppressed — use per-epoch progress instead."""
        # The progress module handles per-epoch console output.
        # Set TQDM_DISABLE=0 in env to restore batch-level tqdm.
        return loader

    @torch.no_grad()
    def _validate(self, loader):
        self.model.eval()
        loss_meter = AverageMeter()
        acc_meter = AverageMeter()
        all_preds, all_labels, all_probs = [], [], []

        for x, y in loader:
            x, y = x.to(self.device, non_blocking=True), y.to(self.device, non_blocking=True)
            logits = self.model(x)
            loss = self._loss_fn(logits, y)
            probs = F.softmax(logits, dim=1)
            preds = probs.argmax(dim=1)
            acc = (preds == y).float().mean()

            loss_meter.update(loss.item(), x.size(0))
            acc_meter.update(acc.item(), x.size(0))
            all_preds.append(preds.cpu().numpy())
            all_labels.append(y.cpu().numpy())
            all_probs.append(probs.cpu().numpy())

        y_true = np.concatenate(all_labels)
        y_pred = np.concatenate(all_preds)
        y_prob = np.concatenate(all_probs)
        metrics = compute_metrics(y_true, y_pred, y_prob)

        return loss_meter.avg, acc_meter.avg, metrics

    def _loss_fn(self, logits, targets):
        if self.label_smoothing > 0:
            n_classes = logits.size(-1)
            smooth_targets = torch.full_like(logits, self.label_smoothing / (n_classes - 1))
            smooth_targets.scatter_(1, targets.unsqueeze(1), 1.0 - self.label_smoothing)
            log_probs = F.log_softmax(logits, dim=1)
            return -(smooth_targets * log_probs).sum(dim=1).mean()
        return F.cross_entropy(logits, targets, weight=self.class_weights)

    def _save_checkpoint(self, filename, epoch, metric):
        torch.save({
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'metric': metric,
        }, os.path.join(self.checkpoint_dir, filename))

    def _get_commit_sha(self) -> str:
        try:
            import subprocess
            r = subprocess.run(['git', 'rev-parse', '--short=8', 'HEAD'],
                             capture_output=True, text=True, timeout=5)
            return r.stdout.strip() if r.returncode == 0 else ''
        except Exception:
            return ''

    def evaluate(self, loader):
        """Final evaluation returning metrics dict."""
        _, _, metrics = self._validate(loader)
        return metrics

    def measure_latency(self, input_shape=(1, 1, 10000), n_warmup=10, n_repeat=100):
        """Measure single-sample inference latency in ms."""
        self.model.eval()
        x = torch.randn(*input_shape).to(self.device)
        with torch.no_grad():
            for _ in range(n_warmup):
                self.model(x)
            if self.device.type == 'cuda':
                torch.cuda.synchronize()
            t0 = time.time()
            for _ in range(n_repeat):
                self.model(x)
            if self.device.type == 'cuda':
                torch.cuda.synchronize()
            elapsed = (time.time() - t0) / n_repeat * 1000
        return elapsed


class MultiTaskTrainer(Trainer):
    """Trainer for multi-task RSN (status + mode + type)."""

    def __init__(self, model, device, config, log_dir="./logs",
                 checkpoint_dir="./checkpoints", model_name="RSN_MT", phase="7A"):
        super().__init__(model, device, config, log_dir, checkpoint_dir,
                        model_name=model_name, phase=phase)
        self.loss_weights = {
            'status': config.get('loss_main_weight', 1.0),
            'mode': config.get('loss_mode_weight', 0.3),
            'type': config.get('loss_type_weight', 0.1),
        }

    def _train_epoch(self, loader, epoch, total_epochs):
        self.model.train()
        loss_meter = AverageMeter()
        acc_meter = AverageMeter()

        for batch_idx, (x, y_s, y_m, y_t) in enumerate(
                self._iter_loader(loader, 'train', epoch, total_epochs)):
            x = x.to(self.device, non_blocking=True)
            y_s = y_s.to(self.device, non_blocking=True)
            y_m = y_m.to(self.device, non_blocking=True)
            y_t = y_t.to(self.device, non_blocking=True)

            self.optimizer.zero_grad()
            logits_s, logits_m, logits_t = self.model(x)

            loss_s = self._loss_fn(logits_s, y_s) * self.loss_weights['status']
            loss_m = self._loss_fn(logits_m, y_m) * self.loss_weights['mode']
            loss_t = self._loss_fn(logits_t, y_t) * self.loss_weights['type']
            loss = loss_s + loss_m + loss_t

            if not torch.isfinite(loss):
                print(f"\n[WARN] NaN loss at batch {batch_idx}, skipping", flush=True)
                continue

            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.grad_clip)
            self.optimizer.step()

            preds = logits_s.argmax(dim=1)
            acc = (preds == y_s).float().mean()
            loss_meter.update(loss.item(), x.size(0))
            acc_meter.update(acc.item(), x.size(0))

        return loss_meter.avg, acc_meter.avg

    @torch.no_grad()
    def _validate(self, loader):
        self.model.eval()
        loss_meter = AverageMeter()
        acc_meter = AverageMeter()
        all_preds, all_labels, all_probs = [], [], []

        for x, y_s, y_m, y_t in loader:
            x = x.to(self.device, non_blocking=True)
            y_s = y_s.to(self.device, non_blocking=True)
            y_m = y_m.to(self.device, non_blocking=True)
            y_t = y_t.to(self.device, non_blocking=True)

            logits_s, logits_m, logits_t = self.model(x)
            loss = (self._loss_fn(logits_s, y_s) * self.loss_weights['status'] +
                    self._loss_fn(logits_m, y_m) * self.loss_weights['mode'] +
                    self._loss_fn(logits_t, y_t) * self.loss_weights['type'])

            probs = F.softmax(logits_s, dim=1)
            preds = probs.argmax(dim=1)
            acc = (preds == y_s).float().mean()

            loss_meter.update(loss.item(), x.size(0))
            acc_meter.update(acc.item(), x.size(0))
            all_preds.append(preds.cpu().numpy())
            all_labels.append(y_s.cpu().numpy())
            all_probs.append(probs.cpu().numpy())

        y_true = np.concatenate(all_labels)
        y_pred = np.concatenate(all_preds)
        y_prob = np.concatenate(all_probs)
        metrics = compute_metrics(y_true, y_pred, y_prob)

        return loss_meter.avg, acc_meter.avg, metrics
