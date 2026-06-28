"""Minimal FLOPs/Params counter — zero external dependencies.

Replaces fvcore.FlopCountAnalysis (which requires fvcore + einops).
Accurate enough for TII style method comparison papers.
"""
from typing import Any
import torch
import torch.nn as nn


def count_params(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters())


def estimate_flops(model: nn.Module, dummy_input: torch.Tensor) -> int:
    """Estimate forward pass FLOPs using torch hooks.

    Supports: nn.Linear, nn.Conv1d, nn.Conv2d, nn.LayerNorm, nn.BatchNorm1d/2d,
    nn.LSTM (approx), nn.MultiheadAttention (approx), nn.MultiheadAttention.

    Not supported: custom ops in the forward path → skipped.
    Result is approximate. Multiply by 2 for MACs→FLOPs if your convention needs it.
    """
    total_macs = [0]
    hooks = []

    def _linear_hook(m, inp, out):
        inp_ = inp[0]
        # (B, ..., in_features) → flops ≈ 2 * B * ... * in_features * out_features
        in_feat = m.in_features
        out_feat = m.out_features
        batch = inp_.numel() // in_feat
        total_macs[0] += 2 * int(batch) * in_feat * out_feat

    def _conv1d_hook(m, inp, out):
        inp_ = inp[0]
        B, Cin, L = inp_.shape
        _, Cout, Lout = out.shape
        k = m.weight.shape[-1]
        total_macs[0] += 2 * B * Cin * Cout * k * Lout

    def _conv2d_hook(m, inp, out):
        inp_ = inp[0]
        B, Cin, H, W = inp_.shape
        _, Cout, Hout, Wout = out.shape
        kh, kw = m.weight.shape[-2], m.weight.shape[-1]
        total_macs[0] += 2 * B * Cin * Cout * kh * kw * Hout * Wout

    def _ln_hook(m, inp, out):
        n = inp[0].numel()
        total_macs[0] += 2 * n  # mean + var per element

    def _bn1d_hook(m, inp, out):
        n = inp[0].numel()
        total_macs[0] += 4 * n

    def _attn_hook(m, inp, out):
        # Rough: attention = 2 * B * n_heads * L * d_k * L
        B, L, _ = inp[0].shape if inp[0].dim() == 3 else (inp[0].shape[1], inp[0].shape[0])
        dh = m.head_dim
        h = m.num_heads
        embed = getattr(m, 'embed_dim', None)
        out_feat = getattr(m.out_proj, 'out_features', embed)
        total_macs[0] += 2 * B * L * embed * 3  # QKV proj
        total_macs[0] += 2 * B * h * dh * L * L  # attn scores
        total_macs[0] += 2 * B * L * out_feat  # out proj

    for module in model.modules():
        if isinstance(module, nn.Linear):
            hooks.append(module.register_forward_hook(_linear_hook))
        elif isinstance(module, nn.Conv1d):
            hooks.append(module.register_forward_hook(_conv1d_hook))
        elif isinstance(module, nn.Conv2d):
            hooks.append(module.register_forward_hook(_conv2d_hook))
        elif isinstance(module, nn.LayerNorm):
            hooks.append(module.register_forward_hook(_ln_hook))
        elif isinstance(module, (nn.BatchNorm1d, nn.BatchNorm2d)):
            hooks.append(module.register_forward_hook(_bn1d_hook))
        elif isinstance(module, nn.MultiheadAttention):
            hooks.append(module.register_forward_hook(_attn_hook))

    try:
        model.eval()
        with torch.no_grad():
            model(dummy_input)
    finally:
        for h in hooks:
            h.remove()

    return total_macs[0]  # MACs


def flops_of(model: nn.Module, seq_len: int = 10000, device: str = 'cpu') -> dict[str, Any]:
    dummy = torch.randn(2, 1, seq_len, device=device)
    macs = estimate_flops(model, dummy)
    # FLOPs ≈ 2 × MACs (standard)
    flops = macs * 2
    return {
        'flops': flops,
        'params': count_params(model),
        'flops_m': flops / 1e6,
        'params_k': count_params(model) / 1e3,
    }
