"""Utility functions for RSN project."""
import os
import yaml
import random
import numpy as np
import torch


def load_config(config_path="configs/default.yaml"):
    """Load YAML configuration file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def set_seed(seed=42):
    """Set random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def get_device(device_str="cuda"):
    """Get torch device."""
    if device_str == "cuda" and torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def count_parameters(model):
    """Count trainable parameters."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def compute_class_weights(labels, num_classes):
    """Compute balanced class weights for CrossEntropyLoss."""
    from collections import Counter
    counts = Counter(labels)
    total = len(labels)
    weights = torch.zeros(num_classes)
    for c in range(num_classes):
        weights[c] = total / (num_classes * counts.get(c, 1))
    return weights


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
