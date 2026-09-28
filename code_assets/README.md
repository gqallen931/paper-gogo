# Paper Workflow Code Assets

These are template Python files that the `paper-workflow` skill copies into new projects during Phase 4 (Project Setup) and Phase 6 (Architecture + Smoke Test).

## Files

```
code_assets/
├── utils/
│   ├── progress.py      # Unified progress logging (log_epoch, log_experiment_start, etc.)
│   ├── flops_stub.py    # FLOPs estimation stub (works without external packages)
│   └── helpers.py       # load_config, set_seed, count_parameters, etc.
├── train/
│   └── trainer.py       # Phase 7-compatible Trainer with progress callbacks
├── experiments/
│   └── phase7_full.py   # Interactive experiment runner (7A→7B→7C→7D)
├── eval/
│   └── metrics.py       # Multi-task metrics (classification/regression/multilabel)
├── baselines/
│   └── factory.py       # Config-driven baseline factory (dynamic import)
├── configs/
│   └── default.yaml     # 7-section layered config template
├── scripts/
│   └── init_project.py  # New project scaffolding script
└── docs/
    └── project_meta.yaml # Project metadata template
```

## Usage

During Phase 4 or Phase 6, the AI copies these files to the user's project and fills in project-specific values (model name, baseline list, data paths, etc.) based on `docs/project_meta.yaml`.

These files are **universal** — they work for any discipline (CV/NLP/LLM/KG/Medical/PHM/TimeSeries/RL/Speech/Tabular) by reading configuration from `configs/default.yaml` at runtime.
