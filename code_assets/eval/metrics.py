"""Evaluation metrics supporting multiple task types.

Task types: classification (default), regression, multilabel, detection.
The dispatcher compute_metrics(y_true, y_pred, y_prob, task_type=..., **kwargs)
routes to the appropriate implementation.
"""
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    confusion_matrix, roc_auc_score, classification_report,
    mean_squared_error, mean_absolute_error, r2_score,
    mean_absolute_percentage_error,
)


# ═══════════════════════════════════════════════════════════════════════
# Dispatcher
# ═══════════════════════════════════════════════════════════════════════

def compute_metrics(y_true, y_pred, y_prob=None, task_type='classification',
                    average='macro', **kwargs):
    """Compute evaluation metrics for any supported task type.

    Args:
        y_true: ground-truth labels/targets, shape (N,) or (N, C)
        y_pred: predicted labels/targets, shape (N,) or (N, C)
        y_prob: predicted probabilities (classification) or None
        task_type: 'classification' | 'regression' | 'multilabel' | 'detection'
        average: 'macro' | 'micro' | 'weighted' | None (per-class)

    Returns:
        dict with at minimum {'accuracy': ..., 'f1': ...} (classification)
        or {'mse': ..., 'mae': ..., 'rmse': ..., 'r2': ...} (regression).
    """
    if task_type == 'regression':
        return _regression_metrics(y_true, y_pred, **kwargs)
    elif task_type == 'multilabel':
        return _multilabel_metrics(y_true, y_pred, y_prob, **kwargs)
    elif task_type == 'detection':
        return _detection_metrics(y_true, y_pred, **kwargs)
    else:
        return _classification_metrics(y_true, y_pred, y_prob, average, **kwargs)


# ═══════════════════════════════════════════════════════════════════════
# Classification (existing logic, extracted)
# ═══════════════════════════════════════════════════════════════════════

def _classification_metrics(y_true, y_pred, y_prob=None, average='macro', **kwargs):
    """Standard multi-class classification metrics."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    acc = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average=average, zero_division=0)
    results = {'accuracy': acc, 'precision': precision,
               'recall': recall, 'f1': f1}

    # Macro-F1 (always compute regardless of average param)
    _, _, macro_f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='macro', zero_division=0)
    results['macro_f1'] = macro_f1

    # Per-class metrics
    per_class = precision_recall_fscore_support(
        y_true, y_pred, average=None, zero_division=0)
    for i, (p, r, f) in enumerate(zip(*per_class[:3])):
        results[f'class_{i}_precision'] = p
        results[f'class_{i}_recall'] = r
        results[f'class_{i}_f1'] = f

    # ROC AUC
    if y_prob is not None:
        try:
            n_classes = y_prob.shape[1]
            if n_classes == 2:
                results['roc_auc'] = roc_auc_score(y_true, y_prob[:, 1])
            else:
                results['roc_auc'] = roc_auc_score(y_true, y_prob, multi_class='ovr',
                                                    average=average if average != 'macro' else 'macro')
        except (ValueError, IndexError):
            results['roc_auc'] = float('nan')

    return results


# ═══════════════════════════════════════════════════════════════════════
# Regression
# ═══════════════════════════════════════════════════════════════════════

def _regression_metrics(y_true, y_pred, **kwargs):
    """Regression metrics: MSE, MAE, RMSE, MAPE, R²."""
    y_true = np.asarray(y_true, dtype=np.float64).flatten()
    y_pred = np.asarray(y_pred, dtype=np.float64).flatten()

    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)

    results = {
        'mse': float(mse),
        'mae': float(mae),
        'rmse': float(rmse),
        'r2': float(r2),
    }

    # MAPE (may fail if y_true contains zeros)
    try:
        mape = mean_absolute_percentage_error(y_true, y_pred)
        results['mape'] = float(mape)
    except (ValueError, ZeroDivisionError):
        results['mape'] = float('nan')

    # Pearson / Spearman correlation
    try:
        results['pearson_r'] = float(np.corrcoef(y_true, y_pred)[0, 1])
    except (ValueError, IndexError):
        results['pearson_r'] = float('nan')

    return results


# ═══════════════════════════════════════════════════════════════════════
# Multi-label classification
# ═══════════════════════════════════════════════════════════════════════

def _multilabel_metrics(y_true, y_pred, y_prob=None, threshold=0.5, **kwargs):
    """Multi-label classification metrics (subset accuracy, micro/macro/samples F1)."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    # If y_pred is probabilities, binarize
    if y_pred.dtype in (np.float32, np.float64) and y_pred.max() <= 1.0:
        y_pred = (y_pred >= threshold).astype(int)

    # Subset accuracy (exact match)
    subset_acc = accuracy_score(y_true, y_pred)

    # Micro / Macro / Samples / Weighted F1
    micro_prec, micro_rec, micro_f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='micro', zero_division=0)
    macro_prec, macro_rec, macro_f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='macro', zero_division=0)

    results = {
        'subset_accuracy': float(subset_acc),
        'micro_f1': float(micro_f1),
        'macro_f1': float(macro_f1),
        'f1': float(macro_f1),  # alias for compatibility
        'precision': float(macro_prec),
        'recall': float(macro_rec),
    }

    # ROC AUC per label (if probabilities provided)
    if y_prob is not None:
        try:
            aucs = []
            for i in range(y_true.shape[1]):
                if len(np.unique(y_true[:, i])) >= 2:
                    aucs.append(roc_auc_score(y_true[:, i], y_prob[:, i]))
            if aucs:
                results['roc_auc'] = float(np.mean(aucs))
        except (ValueError, IndexError):
            results['roc_auc'] = float('nan')

    return results


# ═══════════════════════════════════════════════════════════════════════
# Detection (stub for custom extension)
# ═══════════════════════════════════════════════════════════════════════

def _detection_metrics(y_true, y_pred, **kwargs):
    """Object detection metrics stub.

    y_true and y_pred are expected to be lists of dicts:
      [{'boxes': [[x1,y1,x2,y2],...], 'labels': [...], 'scores': [...]}, ...]

    For now returns empty dict — replace with actual COCO eval / mAP code.
    """
    results = {'mAP50': float('nan'), 'mAP50-95': float('nan'), 'note': 'detection metrics stub'}
    try:
        from pycocotools.coco import COCO
        from pycocotools.cocoeval import COCOeval
        # Real COCO evaluation would go here
        results['note'] = 'pycocotools available — implement COCOeval'
    except ImportError:
        results['note'] = 'pycocotools not installed'
    return results


# ═══════════════════════════════════════════════════════════════════════
# Legacy helpers (preserved for backward compat)
# ═══════════════════════════════════════════════════════════════════════

def compute_confusion_matrix(y_true, y_pred, labels=None):
    """Return confusion matrix as numpy array."""
    return confusion_matrix(y_true, y_pred, labels=labels)


def compute_roc_auc(y_true, y_prob):
    """Compute ROC AUC (multi-class ovr)."""
    try:
        if y_prob.shape[1] == 2:
            return roc_auc_score(y_true, y_prob[:, 1])
        return roc_auc_score(y_true, y_prob, multi_class='ovr')
    except ValueError:
        return float('nan')


def classification_report_dict(y_true, y_pred, target_names=None):
    """Return sklearn classification report as dict."""
    return classification_report(y_true, y_pred, target_names=target_names,
                                 output_dict=True, zero_division=0)


class AverageMeter:
    """Track running averages."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0.0
        self.avg = 0.0
        self.sum = 0.0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
