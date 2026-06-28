#!/usr/bin/env python
"""Initialize a new project from the universal paper-workflow template.

Usage:
    python scripts/init_project.py --name MyProject --discipline cv --task classification

This script:
  1. Creates the standard project directory structure
  2. Copies configs/default.yaml as a starting template
  3. Generates docs/project_meta.yaml with discipline defaults
  4. Creates a minimal docs/README.md
  5. Initializes git (if --git flag)

After running, fill in project-specific details in docs/project_meta.yaml
and configs/default.yaml, then start Phase 0.
"""
import os
import sys
import shutil
import argparse
import datetime
import subprocess

import yaml


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STANDARD_DIRS = [
    "models",
    "data",
    "train",
    "eval",
    "baselines",
    "utils",
    "configs",
    "experiments",
    "scripts",
    "tests",
    "docs/参考文献",
    "docs/创新点",
    "docs/写作",
    "docs/投稿",
    "docs/项目工作阶段记录",
    "docs/工作流与指南",
    "docs/figure",
    "logs",
    "checkpoints",
    "results",
]

TEMPLATE_FILES = {
    "configs/default.yaml": "configs/default.yaml",
    "docs/project_meta.yaml": "docs/project_meta.yaml",
}


def load_discipline_profile(name: str) -> dict:
    """Load a discipline YAML profile."""
    path = os.path.join(PROJECT_ROOT, "docs", "disciplines", f"{name}.yaml")
    if not os.path.exists(path):
        print(f"[WARN] Discipline profile '{name}.yaml' not found in docs/disciplines/")
        return {}
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)


def create_directory_structure(target_dir: str):
    """Create the standard project directory tree."""
    for d in STANDARD_DIRS:
        os.makedirs(os.path.join(target_dir, d), exist_ok=True)
    print(f"  Created {len(STANDARD_DIRS)} directories")


def generate_project_meta(args, profile: dict) -> dict:
    """Generate docs/project_meta.yaml from args + discipline profile."""
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    # Determine primary metric and task type defaults from profile
    task_types = profile.get('task_types', {})
    task_defaults = task_types.get(args.task, {}) if args.task else {}

    meta = {
        'project': {
            'name': args.name,
            'short_name': args.short or args.name[:4].upper(),
            'repo_url': '',
            'description': '',
        },
        'discipline': {
            'field': profile.get('discipline', args.discipline),
            'subfield': args.task,
            'matched_profile': args.discipline,
            'additional_keywords': [],
        },
        'task': {
            'type': args.task,
            'primary_metric': task_defaults.get('primary_metric', 'accuracy'),
            'secondary_metrics': task_defaults.get('metrics', [])[:6],
            'efficiency_metrics': ['n_params', 'flops', 'inference_time_ms'],
            'eval_protocol': task_defaults.get('eval_protocol', ''),
            'typical_epochs': task_defaults.get('typical_epochs', ''),
        },
        'data': {
            'types': [],
            'sources': [],
            'split_strategy': profile.get('split_strategies', ['random_80_20'])[0],
            'num_classes_or_output_dim': 0,
            'notes': '',
        },
        'innovation': {
            'type': [],
            'claims': [],
        },
        'baselines': {
            'source': 'discipline_profile',
            'count_min': 10,
            'custom_list': [],
        },
        'journals': {
            'recommended': profile.get('target_journals', [])[:6],
            'user_pref': None,
        },
        'constraints': {
            'compute_budget': '',
            'time_budget_days': 30,
            'must_baselines': [],
            'must_ablations': [],
        },
        'phase0': {
            'completed': True,
            'date': ts,
            'reviewed_by': 'init_project.py',
        },
    }
    return meta


def create_readme(target_dir: str, meta: dict):
    """Generate a minimal docs/README.md with workflow progress placeholders."""
    name = meta['project']['name']
    discipline = meta['discipline']['field']
    task = meta['task']['type']

    content = f"""# {name}

> **领域**: {discipline} | **任务**: {task} | **初始化**: {meta['phase0']['date']}

## 工作流进度

| Phase | 状态 | 产物 |
|---|---|---|
| -1 全局统筹 | ⬜ | — |
| 0  项目启动 | ✅ | `docs/project_meta.yaml` |
| 1  论文解析 | ⬜ | — |
| 2  文献调研 | ⬜ | — |
| 2A 创新点识别 | ⬜ | — |
| 3  RQ定义 | ⬜ | — |
| 4  项目建立 | ⬜ | — |
| 5  PRD+实验计划 | ⬜ | — |
| 5A 期刊推荐 | ⬜ | — |
| 6  架构搭建 | ⬜ | — |
| 7A 基线训练 | ⬜ | — |
| 7B 消融实验 | ⬜ | — |
| 7C 鲁棒性 | ⬜ | — |
| 7D 汇总出表 | ⬜ | — |
| 8  结果审查 | ⬜ | — |
| 9  可视化 | ⬜ | — |
| 10A 风格迁移 | ⬜ | — |
| 10 论文初稿 | ⬜ | — |
| 11 参考文献 | ⬜ | — |
| 12 投稿前检查 | ⬜ | — |

## 快速开始

```bash
# 运行实验
python experiments/phase7_full.py --yes
```

## 目录结构

```
{name}/
├── models/          # 模型定义
├── data/            # 数据管线
├── train/           # 训练循环
├── eval/            # 评估指标
├── baselines/       # Baseline 工厂
├── configs/         # 配置文件
├── experiments/     # 实验脚本（Phase 7）
├── scripts/         # 工具脚本
├── tests/           # 冒烟测试
├── docs/            # 文档与工作产物
├── results/         # 实验结果 JSON/CSV
├── logs/            # 训练日志
└── checkpoints/     # 模型权重
```
"""
    path = os.path.join(target_dir, 'docs', 'README.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Written: docs/README.md")


def copy_template_files(target_dir: str):
    """Copy config template and other starter files."""
    for src_rel, dst_rel in TEMPLATE_FILES.items():
        src = os.path.join(PROJECT_ROOT, src_rel)
        dst = os.path.join(target_dir, dst_rel)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"  Copied: {dst_rel}")


def init_git(target_dir: str):
    """Initialize git repo if --git flag is set."""
    try:
        subprocess.run(['git', 'init'], cwd=target_dir, check=True,
                      capture_output=True)
        print("  git init: OK")

        # Create .gitignore
        gitignore = """# Python
__pycache__/
*.py[cod]
*.egg-info/
.eggs/
*.egg

# Virtual environments
venv/
.venv/
env/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Project
logs/
checkpoints/
results/
*.pth
*.pt

# Data (large files)
Data/
*.csv
*.mat
*.h5

# OS
.DS_Store
Thumbs.db
"""
        with open(os.path.join(target_dir, '.gitignore'), 'w') as f:
            f.write(gitignore)
        print("  .gitignore: created")
    except subprocess.CalledProcessError:
        print("  [WARN] git init failed (git may not be installed)")


def main():
    # Load discipline index for help text
    index_path = os.path.join(PROJECT_ROOT, 'docs', 'disciplines', '_index.yaml')
    available = {}
    if os.path.exists(index_path):
        with open(index_path, encoding='utf-8') as f:
            available = yaml.safe_load(f)

    parser = argparse.ArgumentParser(
        description='Initialize a new paper-workflow project')
    parser.add_argument('--name', type=str, required=True,
                       help='Project name')
    parser.add_argument('--short', type=str, default=None,
                       help='Short name/abbreviation (default: first 4 chars of --name)')
    parser.add_argument('--discipline', type=str, required=True,
                       choices=list(available.keys()) if available else None,
                       help=f'Discipline key: {", ".join(available.keys()) if available else "cv/nlp/llm/kg/medical/phm/timeseries/rl/speech/tabular"}')
    parser.add_argument('--task', type=str, default='classification',
                       help='Task type (e.g. classification, object_detection, ner)')
    parser.add_argument('--target', type=str, default=None,
                       help='Target directory (default: ./projects/<name>)')
    parser.add_argument('--git', action='store_true',
                       help='Initialize git repository')
    args = parser.parse_args()

    target_dir = args.target or os.path.join(PROJECT_ROOT, 'projects', args.name)
    if os.path.exists(target_dir):
        print(f"[ERROR] Target directory already exists: {target_dir}")
        print("  Remove it or use --target to specify a different directory.")
        sys.exit(1)

    # Load discipline profile
    profile = load_discipline_profile(args.discipline)

    print(f"\n{'='*60}")
    print(f"  Initializing project: {args.name}")
    print(f"  Discipline: {profile.get('discipline', args.discipline)}")
    print(f"  Task: {args.task}")
    print(f"  Target: {target_dir}")
    print(f"{'='*60}\n")

    # Step 1: Directory structure
    print("[1/4] Creating directory structure...")
    create_directory_structure(target_dir)

    # Step 2: project_meta.yaml
    print("[2/4] Generating docs/project_meta.yaml...")
    meta = generate_project_meta(args, profile)
    meta_path = os.path.join(target_dir, 'docs', 'project_meta.yaml')
    with open(meta_path, 'w', encoding='utf-8') as f:
        yaml.dump(meta, f, allow_unicode=True, default_flow_style=False,
                 sort_keys=False, width=120)
    print(f"  Written: docs/project_meta.yaml")

    # Step 3: README.md + config copy
    print("[3/4] Creating README.md and copying templates...")
    create_readme(target_dir, meta)
    copy_template_files(target_dir)

    # Step 4: git init
    if args.git:
        print("[4/4] Initializing git...")
        init_git(target_dir)
    else:
        print("[4/4] Skipping git init (use --git to enable)")

    # Done
    print(f"\n{'='*60}")
    print(f"  Project '{args.name}' initialized!")
    print(f"  Location: {target_dir}")
    print(f"\n  Next steps:")
    print(f"    1. cd {target_dir}")
    print(f"    2. Edit docs/project_meta.yaml with your details")
    print(f"    3. Edit configs/default.yaml with your model+baseline config")
    print(f"    4. Start Phase 0 with the workflow doc at:")
    print(f"       docs/工作流与指南/论文工作流.md")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
