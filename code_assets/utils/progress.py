"""Unified progress logging for Phase 7 experiments.

Provides the 4 mandatory output functions required by the workflow spec:
  log_experiment_start  — 10-field initialization banner
  log_epoch             — 12-field per-epoch line
  log_best_ckpt         — best-checkpoint notification
  log_experiment_end    — 12-field completion summary

Plus helpers: log_data_split, phase_banner, ask_user_continue.
"""
import os
import sys
import time
import json
import datetime


# ═══════════════════════════════════════════════════════════════════════
# Internal helpers
# ═══════════════════════════════════════════════════════════════════════

def _ts() -> str:
    return datetime.datetime.now().strftime('%H:%M:%S')


def _sepline(char: str = '=', width: int = 100) -> str:
    return char * width


# ═══════════════════════════════════════════════════════════════════════
# Public API
# ═══════════════════════════════════════════════════════════════════════

def log_data_split(split_rule: str, n_train: int, n_val: int, n_test: int,
                   train_class_dist: dict, val_class_dist: dict,
                   test_class_dist: dict) -> None:
    """Phase 7A专用：数据划分确认输出。"""
    print(_sepline('='), flush=True)
    print(f'[数据确认] Split={split_rule} | '
          f'Train={n_train} samples ({train_class_dist}) | '
          f'Val={n_val} samples ({val_class_dist}) | '
          f'Test={n_test} samples ({test_class_dist})',
          flush=True)
    print(_sepline('='), flush=True)


def log_experiment_start(*, phase: str, model_name: str, seed: int,
                         device: str, batch_size: int, optimizer: str,
                         init_lr: float, patience: int, config_path: str,
                         commit_sha: str = '', total_epochs: int = 0,
                         n_train: int = 0, n_val: int = 0, n_test: int = 0,
                         n_params: int = 0, flops_m: float = 0.0) -> dict:
    """每实验开始时的初始化输出（强制10+字段）。

    Returns a dict with start_time for later use by log_experiment_end.
    """
    print()
    print(_sepline('='), flush=True)
    fields = [
        f'Phase={phase}',
        f'Model={model_name}',
        f'Seed={seed}',
        f'Device={device}',
        f'BatchSize={batch_size}',
        f'Optim={optimizer}',
        f'LR={init_lr}',
        f'Patience={patience}',
        f'Config={config_path}',
    ]
    if commit_sha:
        fields.append(f'Commit={commit_sha[:8]}')
    if total_epochs:
        fields.append(f'Epochs={total_epochs}')
    if n_train:
        fields.append(f'TrainSamples={n_train}')
    if n_val:
        fields.append(f'ValSamples={n_val}')
    if n_test:
        fields.append(f'TestSamples={n_test}')
    if n_params:
        fields.append(f'Params={n_params:,}')
    if flops_m:
        fields.append(f'FLOPs={flops_m:.2f}M')
    print(f'[实验开始] {" | ".join(fields)}', flush=True)
    print(_sepline('='), flush=True)
    return {'start_time': time.time(), 'epoch_times': []}


def log_epoch(*, current_epoch: int, total_epochs: int, train_loss: float,
              val_loss: float, val_acc: float, val_f1: float,
              best_val_acc: float, best_epoch: int, current_lr: float,
              epoch_time: float, total_elapsed: float, eta: float,
              train_acc: float = None, gpu_mem_allocated: float = None,
              gpu_mem_total: float = None) -> None:
    """每epoch结束后的控制台输出（强制12字段）。"""
    parts = [
        f'[Epoch {current_epoch:>3d}/{total_epochs:<3d}]',
        f'TrainLoss={train_loss:.4f}',
        f'ValLoss={val_loss:.4f}',
        f'ValAcc={val_acc:.4f}',
        f'ValF1={val_f1:.4f}',
        f'BestValAcc={best_val_acc:.4f}(ep{best_epoch})',
        f'LR={current_lr:.2e}',
        f'EpTime={epoch_time:.1f}s',
        f'Total={total_elapsed:.0f}s',
        f'ETA={eta:.0f}s',
    ]
    if train_acc is not None:
        parts.insert(3, f'TrainAcc={train_acc:.4f}')
    if gpu_mem_allocated is not None and gpu_mem_total is not None:
        parts.append(f'GPU={gpu_mem_allocated:.0f}/{gpu_mem_total:.0f}MB')
    print('  '.join(parts), flush=True)


def log_best_ckpt(epoch: int, old_best: float, new_best: float,
                  ckpt_path: str) -> None:
    """Best checkpoint保存时的输出。"""
    print(f'[BestCkpt] Epoch={epoch} | '
          f'ValAcc {old_best:.4f} -> {new_best:.4f} | '
          f'Saved={ckpt_path}',
          flush=True)


def log_experiment_end(*, model_name: str, best_epoch: int, total_epochs: int,
                       test_acc: float, test_f1: float, test_precision: float,
                       test_recall: float, trainable_params: int, flops_m: float,
                       total_train_time: float, avg_epoch_time: float,
                       inference_latency_ms: float = 0.0,
                       early_stop_triggered: bool = False,
                       early_stop_epoch: int = 0) -> None:
    """每实验完成后的汇总输出（强制12字段）。"""
    print(_sepline('-'), flush=True)
    fields = [
        f'Model={model_name}',
        f'BestEp={best_epoch}/{total_epochs}',
        f'TestAcc={test_acc:.4f}',
        f'TestF1={test_f1:.4f}',
        f'Precision={test_precision:.4f}',
        f'Recall={test_recall:.4f}',
        f'Params={trainable_params:,}',
        f'FLOPs={flops_m:.2f}M',
        f'TrainTime={total_train_time:.1f}s',
        f'AvgEpTime={avg_epoch_time:.1f}s',
    ]
    if inference_latency_ms > 0:
        fields.append(f'Latency={inference_latency_ms:.2f}ms')
    if early_stop_triggered:
        fields.append(f'EarlyStop@ep{early_stop_epoch}')
    print(f'[实验完成] {" | ".join(fields)}', flush=True)
    print(_sepline('='), flush=True)


def log_phase_start(phase: str, title: str, total_experiments: int = 0,
                    description: str = '') -> None:
    """子阶段开始的横幅输出。"""
    print()
    print(_sepline('█'), flush=True)
    print(f'  ╔{" PHASE " + phase + " ":=^90s}╗', flush=True)
    print(f'  ║ {title:<90s} ║', flush=True)
    if total_experiments:
        print(f'  ║ {"计划实验数: " + str(total_experiments):<90s} ║', flush=True)
    if description:
        print(f'  ║ {description:<90s} ║', flush=True)
    print(f'  ╚{"=" * 90}╝', flush=True)
    print(_sepline('█'), flush=True)


def log_phase_end(phase: str, total_time: float, n_ok: int, n_fail: int) -> None:
    """子阶段结束的汇总输出。"""
    print()
    print(_sepline('█'), flush=True)
    status = 'OK' if n_fail == 0 else f'OK({n_ok}/{n_ok+n_fail})'
    print(f'  [{phase} 完成] 耗时={total_time:.0f}s ({total_time/60:.1f}min) | '
          f'成功={n_ok} | 失败={n_fail} | 状态={status}',
          flush=True)
    print(_sepline('█'), flush=True)


def log_experiment_progress(subphase: str, i: int, total: int, name: str,
                            acc: float = None, f1: float = None,
                            elapsed: float = None, eta: float = None) -> None:
    """单个实验级别的进度输出（7A/7B/7C通用）。"""
    parts = [f'>>> [{subphase}] [{i}/{total}] {name}']
    if acc is not None:
        parts.append(f'acc={acc:.4f}')
    if f1 is not None:
        parts.append(f'f1={f1:.4f}')
    if elapsed is not None:
        parts.append(f't={elapsed:.0f}s')
    if eta is not None:
        parts.append(f'ETA={eta/60:.1f}min')
    print('  '.join(parts), flush=True)


def ask_user_continue(prompt: str) -> bool:
    """交互式询问用户是否继续。

    如果stdin不可用（管道/重定向），默认自动继续并打印提示。
    """
    if not sys.stdin.isatty():
        print(f'\n[自动继续] {prompt}  (stdin非交互，自动继续)', flush=True)
        return True

    print()
    print(_sepline('─'), flush=True)
    print(f'  ⏸  用户确认点: {prompt}', flush=True)
    print(_sepline('─'), flush=True)
    while True:
        try:
            ans = input('  继续? [Y/n/q(退出)] ').strip().lower()
        except (EOFError, KeyboardInterrupt):
            print('\n[中断] 用户取消', flush=True)
            return False
        if ans in ('', 'y', 'yes'):
            return True
        if ans in ('n', 'no'):
            print('  ⏭  跳过当前步骤', flush=True)
            return False
        if ans in ('q', 'quit', 'exit'):
            print('  ⏹  用户退出', flush=True)
            sys.exit(0)
        print('  请输入 y (继续) / n (跳过) / q (退出)', flush=True)


def ask_user_choice(prompt: str, options: list[str],
                    default: int = 0) -> int:
    """交互式让用户从选项中选一个。

    Returns the index of the selected option.
    """
    if not sys.stdin.isatty():
        print(f'\n[自动选择] {prompt} -> 选项{default+1} (stdin非交互)', flush=True)
        return default

    print()
    print(_sepline('─'), flush=True)
    print(f'  {prompt}', flush=True)
    for i, opt in enumerate(options, 1):
        marker = ' (默认)' if i - 1 == default else ''
        print(f'    [{i}] {opt}{marker}', flush=True)
    print(_sepline('─'), flush=True)
    while True:
        try:
            ans = input(f'  请选择 [1-{len(options)}，默认{default+1}]: ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\n[中断] 用户取消', flush=True)
            return -1
        if ans == '':
            return default
        if ans.lower() in ('q', 'quit', 'exit'):
            print('  ⏹  用户退出', flush=True)
            sys.exit(0)
        try:
            idx = int(ans) - 1
            if 0 <= idx < len(options):
                return idx
        except ValueError:
            pass
        print(f'  请输入 1-{len(options)} 之间的数字', flush=True)


# ═══════════════════════════════════════════════════════════════════════
# JSONL / structured log helpers
# ═══════════════════════════════════════════════════════════════════════

class EpochLogger:
    """Writes one JSON line per epoch to a .jsonl file."""

    def __init__(self, log_dir: str, model_name: str, seed: int):
        os.makedirs(log_dir, exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.path = os.path.join(log_dir, f'{model_name}_s{seed}_{ts}.jsonl')
        self._file = open(self.path, 'w', encoding='utf-8')

    def write(self, record: dict) -> None:
        self._file.write(json.dumps(record, ensure_ascii=False) + '\n')
        self._file.flush()

    def close(self) -> None:
        self._file.close()


class StdoutCapture:
    """Tee stdout to a file while preserving console output."""

    def __init__(self, log_dir: str, model_name: str, seed: int):
        os.makedirs(log_dir, exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.path = os.path.join(log_dir, f'{model_name}_s{seed}_{ts}.stdout')
        self._file = open(self.path, 'w', encoding='utf-8')
        self._original_stdout = sys.stdout

    def __enter__(self):
        sys.stdout = _TeeWriter(self._original_stdout, self._file)
        return self

    def __exit__(self, *args):
        sys.stdout = self._original_stdout
        self._file.close()


class _TeeWriter:
    def __init__(self, *outputs):
        self._outputs = outputs

    def write(self, s):
        for out in self._outputs:
            out.write(s)

    def flush(self):
        for out in self._outputs:
            out.flush()

    def __getattr__(self, name):
        return getattr(self._outputs[0], name)
