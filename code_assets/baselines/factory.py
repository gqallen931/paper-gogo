"""Baseline model factory (CS direction, with graceful stubs).

Two modes:
  1. Hardcoded _MODELS dict (backward compat, RSN project)
  2. Config-driven: load_baselines_from_config(cfg) -> dynamic registry
"""
import importlib

from .cnn1d import CNN1D
from .resnet1d import ResNet1D
from .lstm import LSTMModel
from .stft_cnn import STFT_CNN

try:
    from .cwt_cnn import CWT_CNN, CWT_CNN_Stub
except ImportError:
    from .cwt_cnn import CWT_CNN_Stub as CWT_CNN, CWT_CNN_Stub

try:
    from .wst_svm import WST_SVM, WST_CNN_Stub
except ImportError:
    from .wst_svm import WST_CNN_Stub as WST_SVM, WST_CNN_Stub

try:
    from .kan1d import KAN1D, KAN1D_Stub
except ImportError:
    from .kan1d import KAN1D_Stub as KAN1D, KAN1D_Stub

from .tcn import TCN
from .inceptiontime import InceptionTime
from .dlinear import DLinear
from .patchtst import PatchTST
from .timesnet import TimesNet
from .tilatime import TiLaTime
from .mamba import MambaTimeSeries


_MODELS = {
    'CNN1D': CNN1D,
    'ResNet1D': ResNet1D,
    'LSTM': LSTMModel,
    'STFT_CNN': STFT_CNN,
    'CWT_CNN': CWT_CNN,
    'CWT_CNN_Stub': CWT_CNN_Stub,
    'WST_SVM': WST_SVM,
    'WST_CNN_Stub': WST_CNN_Stub,
    'KAN1D': KAN1D,
    'KAN1D_Stub': KAN1D_Stub,
    'TCN': TCN,
    'InceptionTime': InceptionTime,
    'DLinear': DLinear,
    'PatchTST': PatchTST,
    'TimesNet': TimesNet,
    'TiLaTime': TiLaTime,
    'Mamba': MambaTimeSeries,
}

_CAN_INSTANTIATE_IN_STUB_ENV = [
    'CNN1D', 'ResNet1D', 'LSTM', 'STFT_CNN',
    'CWT_CNN_Stub', 'WST_CNN_Stub', 'KAN1D_Stub',
    'TCN', 'InceptionTime', 'DLinear', 'PatchTST', 'TimesNet', 'TiLaTime', 'Mamba',
]

_REQUIRE_EXTRA_DEPS = {
    'CWT_CNN': 'PyWavelets (pip install PyWavelets)',
    'WST_SVM': 'kymatio (pip install kymatio)',
    'KAN1D': 'efficient-kan (pip install efficient-kan)',
}


_SKLEARN_STUBS = {'WST_SVM'}
_PY_STUBS = {'KAN1D'}


def _make_sklearn_stub(name: str, **kwargs):
    if name == 'WST_SVM':
        return WST_CNN_Stub(
            in_channels=kwargs.get('in_channels', 1),
            num_classes=kwargs.get('num_classes', 3),
            dropout=kwargs.get('dropout', 0.3),
        )
    raise ValueError(f"No sklearn stub for '{name}'")


def _make_py_stub(name: str, **kwargs):
    if name == 'KAN1D':
        return KAN1D_Stub(
            in_channels=kwargs.get('in_channels', 1),
            num_classes=kwargs.get('num_classes', 3),
            dropout=kwargs.get('dropout', 0.3),
        )
    raise ValueError(f"No py stub for '{name}'")


def create_baseline(name: str, **kwargs):
    if name not in _MODELS:
        raise ValueError(f"Unknown baseline '{name}'. Available: {list(_MODELS.keys())}")
    if name in _SKLEARN_STUBS:
        return _make_sklearn_stub(name, **kwargs)
    if name in _PY_STUBS:
        return _make_py_stub(name, **kwargs)
    return _MODELS[name](**kwargs)


def list_baselines(stubs: bool = False):
    if stubs:
        return list(_MODELS.keys())
    return [k for k in _MODELS.keys() if '_Stub' not in k]


def can_instantiate_in_stub_env():
    return _CAN_INSTANTIATE_IN_STUB_ENV


def dependency_status():
    out = {}
    for name, pkg in _REQUIRE_EXTRA_DEPS.items():
        try:
            create_baseline(name)
            out[name] = 'OK'
        except ImportError:
            out[name] = f'MISSING -> using _Stub'
    return out


# ═══════════════════════════════════════════════════════════════════════
# Config-driven baseline registry (v3.0 — universal)
# ═══════════════════════════════════════════════════════════════════════

_config_registry: dict = {}          # {name: builder_fn} loaded from config
_config_stubs: set = set()           # names that are stubs
_config_stub_fns: dict = {}          # {name: stub_builder_fn}


def load_baselines_from_config(config: dict) -> dict:
    """Dynamically build baseline registry from config['baselines']['list'].

    Returns dict of {name: builder_fn_or_NULL}.
    Entries that fail to import are marked with None.

    Example config:
        baselines:
          list:
            - {name: "CNN1D", module: "baselines.cnn1d", build_fn: "create_baseline", stub: null}
            - {name: "CWT_CNN", module: "baselines.cwt_cnn", build_fn: "create_baseline", stub: "CWT_CNN_Stub"}
    """
    global _config_registry, _config_stubs, _config_stub_fns
    _config_registry.clear()
    _config_stubs.clear()
    _config_stub_fns.clear()

    bl = config.get('baselines', {})
    bl_list = bl.get('list', [])

    for entry in bl_list:
        name = entry['name']
        module_name = entry['module']
        build_fn_name = entry.get('build_fn', 'create_baseline')
        stub_name = entry.get('stub', None)

        try:
            mod = importlib.import_module(module_name)
            builder = getattr(mod, build_fn_name)
            _config_registry[name] = builder
            if stub_name:
                try:
                    stub_builder = getattr(mod, stub_name)
                    _config_stub_fns[name] = stub_builder
                    _config_stubs.add(name)
                except AttributeError:
                    pass
        except (ImportError, AttributeError) as e:
            # If main import fails, try stub as fallback
            if stub_name:
                try:
                    stub_builder = getattr(mod, stub_name)
                    _config_registry[name] = stub_builder
                    _config_stubs.add(name)
                except (ImportError, AttributeError):
                    _config_registry[name] = None
            else:
                _config_registry[name] = None

    return _config_registry


def create_baseline_from_config(name: str, **kwargs):
    """Create a baseline model using the config-driven registry.

    Must call load_baselines_from_config() first.
    Falls back to the hardcoded create_baseline() if name not in config registry.
    """
    if name in _config_registry and _config_registry[name] is not None:
        return _config_registry[name](**kwargs)
    # Fallback to hardcoded registry
    return create_baseline(name, **kwargs)


def list_baselines_from_config(include_stubs: bool = False) -> list:
    """Return baseline names from the config-driven registry."""
    if not _config_registry:
        return []
    if include_stubs:
        return list(_config_registry.keys())
    return [k for k in _config_registry if k not in _config_stubs]


def config_registry_status() -> dict:
    """Return {name: 'OK' | 'STUB' | 'MISSING'} for each config baseline."""
    out = {}
    for name in _config_registry:
        if _config_registry[name] is None:
            out[name] = 'MISSING'
        elif name in _config_stubs:
            out[name] = 'STUB'
        else:
            out[name] = 'OK'
    return out
