"""Phase 7 interactive experiment runner.

Phase 7A: all baselines + RSN (default 30 epochs, LOBO-CV).
Phase 7B: RSN ablation matrix.
Phase 7C: robustness (multi-seed) + efficiency.
Phase 7D: final tables + figure data.

Features:
  - Interactive user checkpoints between sub-phases
  - Real-time per-epoch console progress (12-field format)
  - Live ETA and completion percentage
  - Per-experiment start/end banners
  - Structured JSONL epoch logs + stdout capture
  - Auto-save partial results after each experiment

Usage:
  # Interactive (default)
  python experiments/phase7_full.py

  # Non-interactive (skip all prompts)
  python experiments/phase7_full.py --yes

  # Run specific sub-phase only
  python experiments/phase7_full.py --phase 7A
  python experiments/phase7_full.py --phase 7B

  # Custom epochs
  python experiments/phase7_full.py --epochs 50

  # Pipe-friendly (auto-non-interactive)
  python -u experiments/phase7_full.py 2>&1 | tee results/phase7_log.txt
"""
import os
import sys
import time
import json
import copy
import argparse
import importlib
import traceback
import datetime
import subprocess

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import load_config, set_seed, count_parameters
from train.trainer import Trainer
from eval.metrics import compute_metrics, compute_confusion_matrix
from utils.flops_stub import flops_of
from utils.progress import (
    log_phase_start, log_phase_end, log_experiment_progress,
    log_experiment_end, log_data_split, ask_user_continue, ask_user_choice,
    EpochLogger, StdoutCapture, _sepline,
)

# ── Backward-compat imports (RSN project) ──
try:
    from data.dataset import build_bbd_dataset, create_dataloaders, lobo_split
    _has_rsn_data = True
except ImportError:
    _has_rsn_data = False

try:
    from models.rsn import RSN, RSNConfig, create_model as create_rsn_model
    _has_rsn_model = True
except ImportError:
    _has_rsn_model = False

try:
    from baselines.factory import create_baseline, load_baselines_from_config, \
        create_baseline_from_config, list_baselines_from_config
    _has_factory = True
except ImportError:
    _has_factory = False


# ═══════════════════════════════════════════════════════════════════════
# Model registry (config-driven with backward-compat fallback)
# ═══════════════════════════════════════════════════════════════════════

# Default model list (used only if config has no baselines.list)
_MODELS_FALLBACK_7A = [
    'CNN1D', 'ResNet1D', 'LSTM', 'STFT_CNN',
    'CWT_CNN', 'WST_SVM', 'KAN1D',
    'TCN', 'InceptionTime', 'DLinear', 'PatchTST', 'TimesNet', 'TiLaTime', 'Mamba',
    'RSN',
]

# Default ablation variants (used only if config has no phase7.phase7b.ablations)
_ABLATIONS_FALLBACK = [
    ('RSN_Full', {}, 'Full RSN (all components)'),
    ('RSN_Kreduced', {'model': {'K1': 4, 'K2': 8, 'K3': 16}},
     'Reduced K (fewer frequency bins)'),
    ('RSN_Mreduced', {'model': {'M': 1024}},
     'Reduced M (smaller hidden dim)'),
    ('RSN_nodropout', {'model': {'dropout': 0.0}},
     'No dropout regularization'),
]

# Default seeds / noise stds
_SEEDS_FALLBACK = [1, 2, 3, 4]
_NOISE_STDS_FALLBACK = [0.01, 0.02, 0.05]


# ═══════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════

def _get_commit_sha() -> str:
    try:
        r = subprocess.run(['git', 'rev-parse', '--short=8', 'HEAD'],
                          capture_output=True, text=True, timeout=5)
        return r.stdout.strip() if r.returncode == 0 else 'unknown'
    except Exception:
        return 'unknown'


def _build_model(name: str, cfg: dict, device: torch.device):
    """Build a model by name.

    Uses config-driven importlib path if cfg['model']['registry'] is set
    (universal mode). Falls back to hardcoded RSN logic otherwise.
    """
    mc = cfg['model']
    model_registry = cfg.get('model', {}).get('registry', None)

    # ── Universal path: importlib dynamic import ──
    if model_registry:
        try:
            mod = importlib.import_module(model_registry)
            create_fn = getattr(mod, cfg['model']['create_fn'])
            config_cls_name = cfg['model'].get('config_class', None)
            if config_cls_name:
                config_cls = getattr(mod, config_cls_name)
                # Build config from cfg['model'] kwargs + overrides
                config_kwargs = {k: v for k, v in mc.items()
                                if k not in ('registry', 'create_fn', 'config_class',
                                             'core_model_name', 'name')}
                return create_fn(name, config=config_cls(**config_kwargs)).to(device)
            else:
                return create_fn(name, **{k: v for k, v in mc.items()
                       if k not in ('registry', 'create_fn', 'config_class',
                                    'core_model_name', 'name')}).to(device)
        except Exception as e:
            print(f'  [WARN] universal model build failed for {name}: {e}', flush=True)
            print(f'  [WARN] falling back to hardcoded factory', flush=True)

    # ── RSN-specific hardcoded path (backward compat) ──
    if name == 'RSN' and _has_rsn_model:
        return create_rsn_model('RSN', config=RSNConfig(
            K1=mc['K1'], K2=mc['K2'], K3=mc['K3'], M=mc['M'],
            fs=cfg['data']['fs_effective'], f_min=mc['f_min'], f_max=mc['f_max'],
            num_classes=mc['num_classes'], dropout=mc['dropout'])).to(device)

    # ── Baseline factory path ──
    if _has_factory:
        # Try config-driven first
        if cfg.get('baselines', {}).get('list'):
            try:
                return create_baseline_from_config(name, in_channels=1,
                    num_classes=mc.get('num_classes', 3),
                    dropout=mc.get('dropout', 0.3)).to(device)
            except Exception:
                pass
        return create_baseline(name, in_channels=1,
            num_classes=mc.get('num_classes', 3),
            dropout=mc.get('dropout', 0.3)).to(device)

    raise RuntimeError(f"Cannot build model '{name}': no factory available")


def _predict(trainer, loader):
    """Collect predictions from test loader."""
    model = trainer.model
    model.eval()
    all_preds, all_labels, all_probs = [], [], []
    device = trainer.device
    with torch.no_grad():
        for x, y in loader:
            x = x.to(device)
            probs = torch.softmax(model(x), dim=1)
            all_preds.append(probs.argmax(1).cpu().numpy())
            all_labels.append(y.numpy())
            all_probs.append(probs.cpu().numpy())
    return (np.concatenate(all_labels), np.concatenate(all_preds),
            np.concatenate(all_probs))


def run_one_experiment(name: str, cfg: dict, tl, vl, tel, cw,
                       device: torch.device, phase: str = '7A',
                       epochs_override: int = None,
                       interactive: bool = True) -> dict:
    """Run a single experiment with full console progress.

    Returns a result dict matching the Phase 7 spec.
    """
    epochs = epochs_override if epochs_override else cfg['training']['epochs']

    # Build model
    t0 = time.time()
    model = _build_model(name, cfg, device)
    n_params = count_parameters(model)

    # FLOPs
    try:
        info = flops_of(model.eval(), cfg['data']['segment_length'], str(device))
    except Exception:
        info = {'flops_m': 0.0, 'params_k': float(n_params) / 1000}

    # Trainer (handles experiment_start + per-epoch output internally)
    log_dir = os.path.join(cfg['logging']['log_dir'], name)
    ckpt_dir = os.path.join(cfg['logging']['checkpoint_dir'], name)

    trainer = Trainer(
        model, device, cfg['training'],
        log_dir, ckpt_dir,
        class_weights=cw,
        model_name=name,
        phase=phase,
    )

    # Inject config path for the start banner
    cfg['training']['_config_path'] = cfg.get('_config_path', 'configs/default.yaml')

    fit_info = trainer.fit(tl, vl, epochs=epochs)

    # Evaluate on test set
    met = trainer.evaluate(tel)
    y_true, y_pred, y_prob = _predict(trainer, tel)
    cm = compute_confusion_matrix(y_true, y_pred)

    # Inference latency
    try:
        latency_ms = trainer.measure_latency(
            input_shape=(1, 1, cfg['data']['segment_length']))
    except Exception:
        latency_ms = 0.0

    total_time = time.time() - t0
    avg_epoch_time = total_time / max(1, fit_info['stopped_epoch'])

    # ── experiment end banner ──
    log_experiment_end(
        model_name=name,
        best_epoch=fit_info['best_epoch'],
        total_epochs=epochs,
        test_acc=float(met['accuracy']),
        test_f1=float(met['f1']),
        test_precision=float(met.get('precision', 0)),
        test_recall=float(met.get('recall', 0)),
        trainable_params=int(n_params),
        flops_m=float(info.get('flops_m', 0.0)),
        total_train_time=total_time,
        avg_epoch_time=avg_epoch_time,
        inference_latency_ms=latency_ms,
        early_stop_triggered=fit_info['early_stop_triggered'],
        early_stop_epoch=fit_info['stopped_epoch'] if fit_info['early_stop_triggered'] else 0,
    )

    torch.cuda.empty_cache() if device.type == 'cuda' else None

    return {
        'accuracy': float(met['accuracy']),
        'f1': float(met['f1']),
        'macro_f1': float(met.get('macro_f1', met['f1'])),
        'precision': float(met.get('precision', 0)),
        'recall': float(met.get('recall', 0)),
        'n_params': int(n_params),
        'flops_m': float(info.get('flops_m', 0.0)),
        'time_seconds': total_time,
        'epochs': int(epochs),
        'seed': int(cfg.get('seed', 42)),
        'confusion_matrix': cm.tolist(),
        'val_acc_best': float(trainer.best_metric),
        'val_best_epoch': int(fit_info['best_epoch']),
        'early_stop': fit_info['early_stop_triggered'],
        'latency_ms': latency_ms,
        'y_true': y_true.tolist(),
        'y_pred': y_pred.tolist(),
    }


def _print_ascii_table(results: dict, title: str):
    """Print an ASCII results table to console."""
    ok = [(n, r) for n, r in results.items() if 'accuracy' in r]
    if not ok:
        print('  (无结果)', flush=True)
        return
    ok.sort(key=lambda x: x[1]['accuracy'], reverse=True)

    header = f'{"Model":<22} {"Acc":>7} {"F1":>7} {"MacroF1":>7} {"Params(K)":>10} {"FLOPs(M)":>10} {"Time(s)":>8} {"ValBst":>7} {"Rank":>5}'
    print()
    print(title, flush=True)
    print('-' * len(header), flush=True)
    print(header, flush=True)
    print('-' * len(header), flush=True)
    for rc, (name, r) in enumerate(ok, 1):
        marker = ' *' if name.startswith('RSN') else (' ~' if 'Stub' in name else '  ')
        print(f'{name:<22} {r["accuracy"]:>7.4f} {r["f1"]:>7.4f} {r.get("macro_f1", r["f1"]):>7.4f} '
              f'{r["n_params"]/1000:>10.1f} {r["flops_m"]:>10.1f} {r["time_seconds"]:>8.1f} '
              f'{r.get("val_acc_best", 0):>7.4f} {rc:>5}{marker}',
              flush=True)
    print(f'  * = RSN (Ours)   ~ = Stub', flush=True)


def _save_partial_json(data: dict, path: str):
    """Save partial results to JSON (crash-safe)."""
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str, ensure_ascii=False)


def _generate_markdown_report(all_results: dict, timings: dict, cfg: dict,
                              device: torch.device) -> str:
    """Generate the Phase 7D markdown report."""
    phase7a = all_results.get('phase7a', {})
    phase7b = all_results.get('phase7b', {})
    phase7c = all_results.get('phase7c', {})

    lines = [
        '# Phase 7 Final Results',
        '',
        f'*Run on {torch.cuda.get_device_name(0) if device.type == "cuda" else "CPU"}, '
        f'L={cfg["data"]["segment_length"]}, {cfg["training"]["epochs"]} epochs, '
        f'LOBO-CV (val=b{cfg["data"]["val_blade_idx"]}, '
        f'test=b{cfg["data"]["test_blade_indices"]}), '
        f'commit={_get_commit_sha()}*',
        '',
    ]

    # Phase 7A table
    ok_a = [(n, r) for n, r in phase7a.items() if 'accuracy' in r]
    ok_a.sort(key=lambda x: x[1]['accuracy'], reverse=True)
    lines += ['## Phase 7A: Baselines + RSN', '',
              '| Model | Acc | F1 | MacroF1 | Params(K) | FLOPs(M) | Time(s) | ValBest | Latency(ms) | Rank |',
              '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for i, (n, r) in enumerate(ok_a, 1):
        lines.append(f'| {n} | {r["accuracy"]:.4f} | {r["f1"]:.4f} | '
                     f'{r.get("macro_f1", r["f1"]):.4f} | {r["n_params"]/1000:.1f} | '
                     f'{r["flops_m"]:.1f} | {r["time_seconds"]:.1f} | '
                     f'{r.get("val_acc_best", 0):.4f} | {r.get("latency_ms", 0):.2f} | {i} |')

    # Phase 7B table
    lines += ['', '## Phase 7B: RSN Ablation', '',
              '| Variant | Acc | F1 | MacroF1 | Params(K) | FLOPs(M) | Time(s) | ValBest |',
              '|---|---:|---:|---:|---:|---:|---:|']
    for n, r in phase7b.items():
        if 'accuracy' in r:
            lines.append(f'| {n} | {r["accuracy"]:.4f} | {r["f1"]:.4f} | '
                        f'{r.get("macro_f1", r["f1"]):.4f} | {r["n_params"]/1000:.1f} | '
                        f'{r["flops_m"]:.1f} | {r["time_seconds"]:.1f} | '
                        f'{r.get("val_acc_best", 0):.4f} |')

    # Phase 7C robustness
    if phase7c.get('rsn_mean_acc') is not None:
        lines += ['', '## Phase 7C: Multi-Seed Robustness (RSN)', '',
                   '| Seed | Acc | F1 | MacroF1 | Time(s) |',
                   '|---:|---:|---:|---:|---:|']
        for r in phase7c.get('rsn_seeds', []):
            if 'accuracy' in r:
                lines.append(f'| {r["seed"]} | {r["accuracy"]:.4f} | {r["f1"]:.4f} | '
                            f'{r.get("macro_f1", r["f1"]):.4f} | {r["time_seconds"]:.1f} |')
        lines += ['', f'- **Mean Acc**: {phase7c["rsn_mean_acc"]:.4f} '
                      f'± {phase7c["rsn_std_acc"]:.4f} '
                      f'(CV={phase7c.get("rsn_cv", 0):.4f})']

    # Phase 7C noise robustness
    if phase7c.get('noise_accuracy') and 'error' not in str(phase7c['noise_accuracy']):
        lines += ['', '## Phase 7C: Gaussian Noise Robustness', '',
                   '| Noise Std | Accuracy | Drop vs Base |',
                   '|---|---:|--:|']
        base = phase7c.get('base_accuracy', 0)
        for k, v in phase7c['noise_accuracy'].items():
            if isinstance(v, (int, float)):
                lines.append(f'| {k} | {v:.4f} | {base - v:+.4f} |')

    # Timing
    t_a = timings.get('7a', 0)
    t_b = timings.get('7b', 0)
    t_c = timings.get('7c', 0)
    t_total = t_a + t_b + t_c
    lines += ['', '## Timing', '',
              '| Subphase | Time(s) | Time(min) |',
              '|---|---:|---:|',
              f'| 7A Baselines+RSN | {t_a:.0f} | {t_a/60:.1f} |',
              f'| 7B Ablation | {t_b:.0f} | {t_b/60:.1f} |',
              f'| 7C Robustness | {t_c:.0f} | {t_c/60:.1f} |',
              f'| **Total** | **{t_total:.0f}** | **{t_total/60:.1f}** |',
              '']

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════
# Sub-phase runners
# ═══════════════════════════════════════════════════════════════════════

def run_phase_7a(cfg: dict, tl, vl, tel, cw, device: torch.device,
                 interactive: bool = True,
                 model_list: list = None) -> tuple[dict, float]:
    """Phase 7A: environment check + all baseline training."""
    if model_list is None:
        model_list = _MODELS_FALLBACK_7A
    total = len(model_list)
    log_phase_start('7A', '环境核查 + 全部 Baseline 训练',
                    total_experiments=total,
                    description=f'模型: {", ".join(model_list[:6])}... '
                                f'共{total}个 | Epochs={cfg["training"]["epochs"]}')

    # Environment check
    print(f'\n  环境核查:', flush=True)
    print(f'    PyTorch={torch.__version__}  CUDA={torch.cuda.is_available()}  '
          f'Device={device}', flush=True)
    if device.type == 'cuda':
        print(f'    GPU={torch.cuda.get_device_name(0)}  '
              f'VRAM={torch.cuda.get_device_properties(0).total_memory/1024**3:.1f}GB',
              flush=True)
    print(f'    NumPy={np.__version__}', flush=True)

    # Data confirmation
    tr_size = len(tl.dataset)
    va_size = len(vl.dataset)
    te_size = len(tel.dataset)
    tr_labels = [tl.dataset[i][1].item() if torch.is_tensor(tl.dataset[i][1])
                 else tl.dataset[i][1] for i in range(min(1000, tr_size))]
    va_labels = [vl.dataset[i][1].item() if torch.is_tensor(vl.dataset[i][1])
                 else vl.dataset[i][1] for i in range(min(1000, va_size))]
    te_labels = [tel.dataset[i][1].item() if torch.is_tensor(tel.dataset[i][1])
                 else tel.dataset[i][1] for i in range(min(1000, te_size))]
    from collections import Counter
    log_data_split(
        split_rule=f'LOBO(val_blade={cfg["data"]["val_blade_idx"]}, '
                   f'test_blades={cfg["data"]["test_blade_indices"]})',
        n_train=tr_size, n_val=va_size, n_test=te_size,
        train_class_dist=dict(Counter(tr_labels)),
        val_class_dist=dict(Counter(va_labels)),
        test_class_dist=dict(Counter(te_labels)),
    )

    if interactive:
        if not ask_user_continue(f'即将开始训练 {total} 个模型，预计耗时较长。确认开始 Phase 7A?'):
            print('  用户跳过 Phase 7A', flush=True)
            return {}, 0.0

    phase7a = {}
    t_begin = time.time()
    n_ok, n_fail = 0, 0

    for i, name in enumerate(model_list, 1):
        log_experiment_progress('7A', i, total, name)
        t0 = time.time()
        try:
            r = run_one_experiment(name, cfg, tl, vl, tel, cw, device,
                                   phase='7A', interactive=interactive)
            dt = time.time() - t0
            phase7a[name] = r
            n_ok += 1
            log_experiment_progress('7A', i, total, name,
                                    acc=r['accuracy'], f1=r['f1'],
                                    elapsed=dt, eta=dt * (total - i))
        except Exception as e:
            dt = time.time() - t0
            n_fail += 1
            print(f'\n  [ERROR] {name}: {e}', flush=True)
            traceback.print_exc()
            phase7a[name] = {'error': str(e)}

        torch.cuda.empty_cache() if device.type == 'cuda' else None
        # Partial save after each experiment
        _save_partial_json(phase7a, 'results/phase7a.json')

    t_total = time.time() - t_begin
    log_phase_end('7A', t_total, n_ok, n_fail)

    # Show intermediate results
    _print_ascii_table(phase7a, 'PHASE 7A RESULTS (interim)')

    return phase7a, t_total


def run_phase_7b(cfg: dict, tl, vl, tel, cw, device: torch.device,
                 interactive: bool = True,
                 ablations: list = None) -> tuple[dict, float]:
    """Phase 7B: core method training + ablation matrix."""
    if ablations is None:
        ablations = DEFAULT_ABLATIONS

    total = len(ablations)
    log_phase_start('7B', '核心方法训练 + 消融实验',
                    total_experiments=total,
                    description=f'消融组: {", ".join(a[0] for a in ablations)}')

    if interactive:
        if not ask_user_continue(f'即将运行 {total} 组消融实验。确认开始 Phase 7B?'):
            print('  用户跳过 Phase 7B', flush=True)
            return {}, 0.0

    phase7b = {}
    t_begin = time.time()
    n_ok, n_fail = 0, 0

    for i, (name, overrides, desc) in enumerate(ablations, 1):
        log_experiment_progress('7B', i, total, f'{name} ({desc})')
        t0 = time.time()

        # Merge overrides into config
        cfg_a = copy.deepcopy(cfg)
        for sec, d in overrides.items():
            if sec not in cfg_a:
                cfg_a[sec] = {}
            cfg_a[sec].update(d)

        try:
            r = run_one_experiment('RSN', cfg_a, tl, vl, tel, cw, device,
                                   phase='7B', interactive=interactive)
            phase7b[name] = {'description': desc, **r}
            n_ok += 1
            dt = time.time() - t0
            log_experiment_progress('7B', i, total, name,
                                    acc=r['accuracy'], f1=r['f1'],
                                    elapsed=dt, eta=dt * (total - i))
        except Exception as e:
            n_fail += 1
            print(f'\n  [ERROR] {name}: {e}', flush=True)
            traceback.print_exc()
            phase7b[name] = {'description': desc, 'error': str(e)}

        torch.cuda.empty_cache() if device.type == 'cuda' else None
        _save_partial_json(phase7b, 'results/phase7b.json')

    t_total = time.time() - t_begin
    log_phase_end('7B', t_total, n_ok, n_fail)
    _print_ascii_table(phase7b, 'PHASE 7B ABLATION RESULTS')

    return phase7b, t_total


def run_phase_7c(cfg: dict, tl, vl, tel, cw, device: torch.device,
                 interactive: bool = True,
                 seeds: list = None,
                 noise_stds: list = None) -> tuple[dict, float]:
    """Phase 7C: robustness (multi-seed) + noise + efficiency."""
    if seeds is None:
        seeds = DEFAULT_SEEDS
    if noise_stds is None:
        noise_stds = DEFAULT_NOISE_STDS

    total = len(seeds) + len(noise_stds)
    log_phase_start('7C', '鲁棒性 + 效率评估',
                    total_experiments=total,
                    description=f'Seeds={seeds} | Noise stds={noise_stds}')

    if interactive:
        if not ask_user_continue(f'即将运行鲁棒性测试 ({len(seeds)} seeds + '
                                 f'{len(noise_stds)} noise levels)。确认开始 Phase 7C?'):
            print('  用户跳过 Phase 7C', flush=True)
            return {}, 0.0

    phase7c = {}
    t_begin = time.time()

    # ── Multi-seed robustness ──
    print(f'\n  --- 多种子鲁棒性 ({len(seeds)} seeds) ---', flush=True)
    robust_runs = []
    for i, seed in enumerate(seeds, 1):
        log_experiment_progress('7C', i, len(seeds), f'RSN_seed={seed}')
        t0 = time.time()
        set_seed(seed)
        cfg_r = copy.deepcopy(cfg)
        cfg_r['seed'] = seed
        try:
            r = run_one_experiment('RSN', cfg_r, tl, vl, tel, cw, device,
                                   phase='7C', interactive=interactive)
            robust_runs.append({'seed': seed, **r})
            log_experiment_progress('7C', i, len(seeds), f'RSN_seed={seed}',
                                    acc=r['accuracy'], f1=r['f1'],
                                    elapsed=time.time() - t0)
        except Exception as e:
            print(f'\n  [ERROR] seed={seed}: {e}', flush=True)
            traceback.print_exc()
            robust_runs.append({'seed': seed, 'error': str(e)})

    phase7c['rsn_seeds'] = robust_runs
    accs = [r['accuracy'] for r in robust_runs if 'accuracy' in r]
    if accs:
        phase7c['rsn_mean_acc'] = float(np.mean(accs))
        phase7c['rsn_std_acc'] = float(np.std(accs))
        phase7c['rsn_cv'] = float(np.std(accs) / max(1e-9, np.mean(accs)))
        print(f'\n  Seeds summary: mean={phase7c["rsn_mean_acc"]:.4f}  '
              f'std={phase7c["rsn_std_acc"]:.4f}  CV={phase7c["rsn_cv"]:.4f}',
              flush=True)

    # ── Gaussian noise robustness ──
    print(f'\n  --- 高斯噪声鲁棒性 ({len(noise_stds)} levels) ---', flush=True)
    try:
        set_seed(cfg.get('seed', 42))
        rsn_cfg = copy.deepcopy(cfg)
        r = run_one_experiment('RSN', rsn_cfg, tl, vl, tel, cw, device,
                               phase='7C', interactive=interactive)
        base_acc = r['accuracy']
        noise_accs = {}
        from torch.utils.data import DataLoader, TensorDataset

        for i, std in enumerate(noise_stds, 1):
            print(f'  [{i}/{len(noise_stds)}] noise std={std:.2f} ...', flush=True)
            # Build noisy test set
            xs, ys = [], []
            for xb, yb in tel:
                xb_n = xb + std * torch.randn_like(xb)
                xs.append(xb_n)
                ys.append(yb)
            noisy_x = torch.cat(xs)
            noisy_y = torch.cat(ys)
            noisy_loader = DataLoader(
                TensorDataset(noisy_x, noisy_y),
                batch_size=cfg['training']['batch_size'], shuffle=False)

            model = _build_model('RSN', rsn_cfg, device)
            model.eval()
            total_c, correct = 0, 0
            with torch.no_grad():
                for xb, yb in noisy_loader:
                    xb = xb.to(device)
                    pr = model(xb).argmax(dim=1).cpu()
                    correct += (pr == yb).sum().item()
                    total_c += yb.size(0)
            noise_acc = float(correct) / float(total_c)
            noise_accs[f'std_{std:.2f}'] = noise_acc
            print(f'    noise std={std:.2f}  acc={noise_acc:.4f}  '
                  f'drop={base_acc - noise_acc:+.4f}', flush=True)

        phase7c['noise_accuracy'] = noise_accs
        phase7c['base_accuracy'] = float(base_acc)
    except Exception as e:
        print(f'\n  [ERROR] noise robustness: {e}', flush=True)
        traceback.print_exc()
        phase7c['noise_accuracy'] = {'error': str(e)}

    _save_partial_json(phase7c, 'results/phase7c.json')
    t_total = time.time() - t_begin
    log_phase_end('7C', t_total,
                  n_ok=len(accs) + (1 if 'error' not in str(phase7c.get('noise_accuracy', {})) else 0),
                  n_fail=sum(1 for r in robust_runs if 'error' in r))

    return phase7c, t_total


def run_phase_7d(all_results: dict, timings: dict, cfg: dict,
                 device: torch.device, interactive: bool = True):
    """Phase 7D: final tables + figure data + review report."""
    print()
    print(_sepline('█'), flush=True)
    print('  PHASE 7D — 汇总 + 目标期刊风格总表 + 绘图数据', flush=True)
    print(_sepline('█'), flush=True)

    phase7a = all_results.get('phase7a', {})
    phase7b = all_results.get('phase7b', {})
    phase7c = all_results.get('phase7c', {})

    # ── 7D.1 Assemble JSON ──
    print('>>> [7D] 汇总 JSON ........................', end=' ', flush=True)
    master = {
        'phase7a': phase7a,
        'phase7b': phase7b,
        'phase7c': phase7c,
        'timings': timings,
        'config': {
            'epochs': cfg['training']['epochs'],
            'segment_length': cfg['data']['segment_length'],
            'seed': cfg.get('seed', 42),
            'val_blade_idx': cfg['data']['val_blade_idx'],
            'test_blade_indices': cfg['data']['test_blade_indices'],
        },
        'commit': _get_commit_sha(),
    }
    ts = time.strftime('%Y%m%d_%H%M%S')
    _save_partial_json(master, f'results/phase7_full_{ts}.json')
    _save_partial_json(master, 'results/phase7_full.json')
    print('OK', flush=True)

    # ── 7D.2 Final tables ──
    print('>>> [7D] 目标期刊风格总表 ..................', end=' ', flush=True)
    md_report = _generate_markdown_report(all_results, timings, cfg, device)
    os.makedirs('docs/工作流与指南', exist_ok=True)
    with open('docs/工作流与指南/phase7_最终总表.md', 'w', encoding='utf-8') as f:
        f.write(md_report)
    print('OK', flush=True)

    # ── 7D.3 Figure data ──
    print('>>> [7D] figure_data ........................', end=' ', flush=True)
    figure_data = {
        'confusion_matrices': {},
        'ablation_bars': {},
        'efficiency_scatter': [],
    }
    # Confusion matrices from 7A
    for name, r in phase7a.items():
        if 'confusion_matrix' in r:
            figure_data['confusion_matrices'][name] = r['confusion_matrix']
    # Ablation bar data from 7B
    for name, r in phase7b.items():
        if 'accuracy' in r:
            figure_data['ablation_bars'][name] = {
                'accuracy': r['accuracy'], 'f1': r['f1'],
                'n_params': r['n_params'], 'flops_m': r['flops_m'],
            }
    # Efficiency scatter: accuracy vs FLOPs for all models in 7A
    for name, r in phase7a.items():
        if 'accuracy' in r and 'flops_m' in r:
            figure_data['efficiency_scatter'].append({
                'model': name, 'accuracy': r['accuracy'],
                'flops_m': r['flops_m'], 'n_params': r['n_params'],
                'time_s': r['time_seconds'],
            })
    _save_partial_json(figure_data, 'results/phase7_figure_data.json')
    print('OK', flush=True)

    # ── 7D.4 Final ASCII summary ──
    print()
    print(_sepline('='), flush=True)
    print('  PHASE 7 最终结果总表', flush=True)
    print(_sepline('='), flush=True)
    _print_ascii_table(phase7a, 'Phase 7A: All Baselines + RSN')
    if phase7b:
        _print_ascii_table(phase7b, 'Phase 7B: RSN Ablation')

    # ── 7D.5 Phase 8 readiness check ──
    print()
    print(_sepline('─'), flush=True)
    print('  Phase 8 就绪检查:', flush=True)
    n_ok_a = sum(1 for v in phase7a.values() if 'accuracy' in v)
    n_fail_a = sum(1 for v in phase7a.values() if 'error' in v)
    checks = [
        ('7A 基线训练完成', n_ok_a >= 1,
         f'{n_ok_a}/{len(phase7a)} 成功'),
        ('7B 消融实验完成', len([v for v in phase7b.values() if 'accuracy' in v]) >= 2,
         f'{len([v for v in phase7b.values() if "accuracy" in v])}/{len(phase7b)} 成功'),
        ('7C 鲁棒性完成', phase7c.get('rsn_mean_acc') is not None,
         f'CV={phase7c.get("rsn_cv", "N/A"):.4f}' if phase7c.get('rsn_cv') else 'N/A'),
        ('总表已生成', os.path.exists('docs/工作流与指南/phase7_最终总表.md'), ''),
        ('JSON完整', os.path.exists('results/phase7_full.json'), ''),
    ]
    all_pass = True
    for label, ok, detail in checks:
        mark = '✅' if ok else '❌'
        print(f'    {mark} {label}: {detail}', flush=True)
        if not ok:
            all_pass = False

    t_total = sum(timings.values())
    print(f'\n  总耗时: {t_total:.0f}s ({t_total/60:.1f}min)', flush=True)
    if all_pass:
        print(f'\n  ✅ Phase 7 全部完成，可以进入 Phase 8 (结果审查与复现检查)',
              flush=True)
    else:
        print(f'\n  ⚠️  部分检查未通过，请修复后重新运行对应子阶段', flush=True)


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='Phase 7 Interactive Experiment Runner')
    parser.add_argument('--config', type=str, default='configs/default.yaml')
    parser.add_argument('--epochs', type=int, default=None,
                       help='Override epochs (default: from config)')
    parser.add_argument('--phase', type=str, default=None,
                       choices=['7A', '7B', '7C', '7D'],
                       help='Run only one sub-phase (7A/7B/7C/7D)')
    parser.add_argument('--yes', '-y', action='store_true',
                       help='Skip all interactive prompts (non-interactive mode)')
    parser.add_argument('--models', type=str, nargs='*',
                       help='Override model list for 7A (space-separated)')
    parser.add_argument('--seeds', type=int, nargs='*',
                       help='Override seeds for 7C')
    args = parser.parse_args()

    interactive = not args.yes and sys.stdin.isatty()

    # ═══════════════════════════════════════════════════════════════
    # Welcome banner
    # ═══════════════════════════════════════════════════════════════
    print()
    print(_sepline('█'), flush=True)
    print('  ╔══════════════════════════════════════════════════════════════╗', flush=True)
    print('  ║           P H A S E   7   实 验 核 心                       ║', flush=True)
    print('  ║           Experiment Core  (P7A ~ P7D)                      ║', flush=True)
    print('  ╚══════════════════════════════════════════════════════════════╝', flush=True)
    print(_sepline('█'), flush=True)

    # ═══════════════════════════════════════════════════════════════
    # Load config
    # ═══════════════════════════════════════════════════════════════
    cfg = load_config(args.config)
    cfg['_config_path'] = args.config
    if args.epochs:
        cfg['training']['epochs'] = args.epochs
    epochs = cfg['training']['epochs']
    cfg['training']['early_stop_patience'] = min(30, epochs)
    set_seed(cfg.get('seed', 42))
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    print(f'\n  配置摘要:', flush=True)
    print(f'    Config:    {args.config}', flush=True)
    print(f'    Device:    {device}', flush=True)
    if device.type == 'cuda':
        print(f'    GPU:       {torch.cuda.get_device_name(0)}', flush=True)
    print(f'    Epochs:    {epochs}', flush=True)
    print(f'    Seed:      {cfg.get("seed", 42)}', flush=True)
    print(f'    BatchSize: {cfg["training"]["batch_size"]}', flush=True)
    print(f'    LR:        {cfg["training"]["lr"]}', flush=True)
    print(f'    Mode:      {"交互式 (interactive)" if interactive else "自动 (non-interactive)"}',
          flush=True)
    print(f'    Commit:    {_get_commit_sha()}', flush=True)

    # ═══════════════════════════════════════════════════════════════
    # Dataset (config-driven with backward-compat fallback)
    # ═══════════════════════════════════════════════════════════════
    print(f'\n>>> 构建数据集 ...', flush=True)
    t0 = time.time()

    # Load baseline registry from config if present
    if cfg.get('baselines', {}).get('list') and _has_factory:
        load_baselines_from_config(cfg)

    # Universal path: use config['data']['builder_*']
    data_cfg = cfg.get('data', {})
    if data_cfg.get('builder_fn'):
        data_mod = importlib.import_module(data_cfg['builder_module'])
        build_fn = getattr(data_mod, data_cfg['builder_fn'])
        builder_kwargs = data_cfg.get('builder_kwargs', {})
        if 'data_root' in builder_kwargs:
            builder_kwargs['data_root'] = builder_kwargs.pop('data_root')
        result = build_fn(**{k: v for k, v in builder_kwargs.items()})
        if isinstance(result, tuple) and len(result) >= 6:
            X, y_s, y_m, y_t, blade_ids, metadata = result
            print(f'    完成: X={X.shape}  samples={len(y_s)}  耗时={time.time()-t0:.1f}s', flush=True)
        else:
            X, y_s = result[0], result[1]
            y_m, y_t, blade_ids, metadata = None, None, np.arange(len(y_s)), {}
            print(f'    完成: X={X.shape}  samples={len(y_s)}  耗时={time.time()-t0:.1f}s', flush=True)

        # Split
        split_fn_name = data_cfg.get('split_fn', None)
        if split_fn_name:
            split_fn = getattr(data_mod, split_fn_name)
            split_kwargs = data_cfg.get('split_kwargs', {})
            tr_mask, va_mask, te_mask = split_fn(blade_ids, **split_kwargs)
        else:
            n = len(y_s)
            tr_mask = np.zeros(n, dtype=bool); tr_mask[:int(n*0.7)] = True
            va_mask = np.zeros(n, dtype=bool); va_mask[int(n*0.7):int(n*0.85)] = True
            te_mask = np.zeros(n, dtype=bool); te_mask[int(n*0.85):] = True

        # Dataloader
        dl_fn_name = data_cfg.get('dataloader_fn', 'create_dataloaders')
        dl_fn = getattr(data_mod, dl_fn_name)
        dl_kwargs = data_cfg.get('dataloader_kwargs', {})
        tl, vl, tel, cw = dl_fn(X, y_s, y_m, y_t, blade_ids,
                                 batch_size=cfg['training']['batch_size'],
                                 num_workers=0, use_augmentation=True,
                                 **{k: v for k, v in dl_kwargs.items()
                                    if k not in ('batch_size', 'num_workers', 'use_augmentation')})
    else:
        # RSN backward-compat path
        X, y_s, y_m, y_t, blade_ids, metadata = build_bbd_dataset(
            cfg['data']['bbd_root'],
            L=cfg['data']['segment_length'],
            dec_factor=cfg['data']['decimate_factor'],
            stride=cfg['data']['window_stride'])
        print(f'    完成: X={X.shape}  samples={len(y_s)}  blades={len(np.unique(blade_ids))}  '
              f'耗时={time.time()-t0:.1f}s', flush=True)

        tr_mask, va_mask, te_mask = lobo_split(
            blade_ids, cfg['data']['val_blade_idx'], cfg['data']['test_blade_indices'])
        tl, vl, tel, cw = create_dataloaders(
            X, y_s, y_m, y_t, blade_ids,
            cfg['data']['val_blade_idx'], cfg['data']['test_blade_indices'],
            batch_size=cfg['training']['batch_size'], num_workers=0, use_augmentation=True)

    os.makedirs('results', exist_ok=True)
    os.makedirs(cfg['logging']['log_dir'], exist_ok=True)
    os.makedirs(cfg['logging']['checkpoint_dir'], exist_ok=True)

    all_results: dict = {}
    timings: dict = {}

    # ═══════════════════════════════════════════════════════════════
    # Phase selection
    # ═══════════════════════════════════════════════════════════════
    run_all = args.phase is None

    if interactive and run_all:
        opts = ['运行全部 Phase 7A→7B→7C→7D (完整流程)',
                '仅运行 Phase 7A (基线训练)',
                '仅运行 Phase 7B (消融实验)',
                '仅运行 Phase 7C (鲁棒性+效率)',
                '仅运行 Phase 7D (汇总出表，需已有结果JSON)']
        choice = ask_user_choice('请选择要运行的阶段:', opts, default=0)
        if choice < 0:
            return
        phase_map = {0: None, 1: '7A', 2: '7B', 3: '7C', 4: '7D'}
        args.phase = phase_map.get(choice, None)
        run_all = args.phase is None

    # ═══════════════════════════════════════════════════════════════
    # Execute sub-phases
    # ═══════════════════════════════════════════════════════════════

    if run_all or args.phase == '7A':
        # Determine model list: CLI override > config > fallback
        if args.models:
            models_7a = args.models
        elif cfg.get('baselines', {}).get('list'):
            models_7a = [b['name'] for b in cfg['baselines']['list']]
            if cfg['model'].get('core_model_name') and cfg['phase7']['phase7a'].get('models_include_core', True):
                core = cfg['model']['core_model_name']
                if core not in models_7a:
                    models_7a.append(core)
        else:
            models_7a = list(_MODELS_FALLBACK_7A)
        results_a, t_a = run_phase_7a(cfg, tl, vl, tel, cw, device, interactive,
                                      model_list=models_7a)
        all_results['phase7a'] = results_a
        timings['7a'] = t_a
        if interactive and run_all and results_a:
            ask_user_continue('Phase 7A 完成。继续 Phase 7B (消融实验)?')

    if run_all or args.phase == '7B':
        # Determine ablation list: config > fallback
        ablations_cfg = cfg.get('phase7', {}).get('phase7b', {}).get('ablations', None)
        if ablations_cfg:
            ablations_7b = [(a['label'], a['overrides'], a['description'])
                          for a in ablations_cfg]
        else:
            ablations_7b = list(_ABLATIONS_FALLBACK)
        results_b, t_b = run_phase_7b(cfg, tl, vl, tel, cw, device, interactive,
                                      ablations=ablations_7b)
        all_results['phase7b'] = results_b
        timings['7b'] = t_b
        if interactive and run_all:
            ask_user_continue('Phase 7B 完成。继续 Phase 7C (鲁棒性测试)?')

    if run_all or args.phase == '7C':
        seeds_7c = args.seeds if args.seeds else cfg.get('phase7', {}).get('phase7c', {}).get('seeds', _SEEDS_FALLBACK)
        noise_7c = cfg.get('phase7', {}).get('phase7c', {}).get('noise_stds', _NOISE_STDS_FALLBACK)
        results_c, t_c = run_phase_7c(cfg, tl, vl, tel, cw, device,
                                      interactive,
                                      seeds=seeds_7c,
                                      noise_stds=noise_7c)
        all_results['phase7c'] = results_c
        timings['7c'] = t_c
        if interactive and run_all:
            ask_user_continue('Phase 7C 完成。继续 Phase 7D (汇总出表)?')

    if run_all or args.phase == '7D':
        # If only running 7D, try to load existing results
        if args.phase == '7D' and not all_results:
            for fname, key in [('results/phase7a.json', 'phase7a'),
                               ('results/phase7b.json', 'phase7b'),
                               ('results/phase7c.json', 'phase7c')]:
                if os.path.exists(fname):
                    with open(fname, 'r', encoding='utf-8') as f:
                        all_results[key] = json.load(f)
                    print(f'  加载 {fname} -> {len(all_results[key])} 条记录', flush=True)

        run_phase_7d(all_results, timings, cfg, device, interactive)

    # ═══════════════════════════════════════════════════════════════
    # Final
    # ═══════════════════════════════════════════════════════════════
    print()
    print(_sepline('█'), flush=True)
    print('  Phase 7 结束。', flush=True)
    print(f'  产物: results/phase7_full.json', flush=True)
    print(f'         docs/工作流与指南/phase7_最终总表.md', flush=True)
    print(f'         results/phase7_figure_data.json', flush=True)
    print(_sepline('█'), flush=True)


if __name__ == '__main__':
    main()
