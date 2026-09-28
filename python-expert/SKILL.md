---
name: python-expert
description: This skill should be used when the user asks to implement, debug, profile, or optimize Python code for scientific computing, data pipelines, ML models, training loops, evaluation, or reproducible experiments in Paper-gogo Phases 4, 6, 7, or 8.
---

# Python Expert

## Goal

Provide scoped Python implementation support for scientific and machine-learning experiments without inventing APIs, results, or project assumptions.

## Boundaries

- Inspect the existing environment and project conventions before editing.
- Make the smallest change required by the experiment protocol.
- Do not fabricate successful runs, metrics, GPU availability, dependencies, or benchmark results.
- Keep data splits, seeds, configuration, logging, and evaluation reproducible.
- Use `diagnosing-bugs` for hard failures and `tdd` when behavior should be locked down test-first.

## Workflow

1. Identify the requested behavior and success criterion.
2. Inspect the relevant code, configuration, data contract, and environment.
3. State assumptions and choose the smallest implementation path.
4. Implement with stable configuration and deterministic seeds where feasible.
5. Run the narrowest relevant test or smoke experiment.
6. Report changed files, verification evidence, remaining risks, and the full-run command.

## Scope

- PyTorch, TensorFlow, JAX, NumPy, and SciPy
- model, loss, metric, and baseline implementation
- training and evaluation loops
- data loading and preprocessing
- configuration, logging, caching, and checkpointing
- vectorization, memory, CPU/GPU, and runtime optimization

## Output

- implementation summary
- changed files
- verification evidence
- reproducibility settings
- unresolved dependencies or full-run actions
