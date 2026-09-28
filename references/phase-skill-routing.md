# Paper-gogo v6 phase-to-skill routing

This file defines the executable routing contract for `paper-workflow-v6.md`.

Use only skills that exist as unpacked directories with a readable `SKILL.md`.

Rule precedence is: root `SKILL.md` boundaries → `paper-workflow-v6.md` gates → this routing table → inherited v5 wording. A lower-level instruction cannot bypass truth, evidence, ethics, or journal-policy verification.

## Invocation protocol

For every phase or slash command:

1. Resolve the requested Phase or command; do not advance adjacent phases automatically.
2. Load the primary skill's `SKILL.md` completely before acting.
3. Load only the references required by the current subtask.
4. Check the skill-specific entry gate and required inputs.
5. Execute the smallest scoped task that produces the phase output.
6. Record skill name, input, output, evidence state, unresolved items, and next legal phase in the phase log.
7. If the primary skill is unavailable or its entry gate fails, use the stated fallback; never pretend it ran.

Auxiliary skills are conditional. Do not load every listed skill by default.

## Phase routing matrix

| Phase | Primary skill | Conditional auxiliary skill | Trigger | Expected output |
|---:|---|---|---|---|
| 0 | `world-model-method` | `understand` | Use `understand` only when a substantial codebase exists and its plugin/Node/agent preflight passes | project model, objective, constraints, material inventory |
| 1 | `domain-modeling` | `grilling` | Use grilling only when terms, problem boundaries, or assumptions remain ambiguous and the user accepts interview mode | glossary, phenomenon-mechanism-condition question, boundary decisions |
| 2 | `nature-academic-search` | `nature-reader`, `nature-citation` | Build a core set (normally 8–15) plus an extensible set; read/convert supplied papers with reader; add citation skill for claim verification or ENW/RIS/RDF | search log, tiered deduplicated library, verified metadata |
| 3 | `nature-reader` | `nature-writing`, `nature-paper2ppt` | Full-read the core set and promote directly relevant/conflicting extended papers; use writing for synthesis; PPT is opt-in | source-grounded reading artifacts, evidence map, synthesis; optional real PPTX |
| 4 | `world-model-method` | `domain-modeling`, `nature-writing` | Use domain modeling for domain constraints; use writing self-review guidance for claim-evidence audit | novelty classification, domain-bias map, candidate-path comparison |
| 5 | `world-model-method` | `domain-modeling`, `paper-framework-figure-studio-pro` | Use figure studio only for explicitly requested S0-S3 steps, one step per user turn | study design, claim-experiment matrix, approved figure direction |
| 6 | `codebase-design` | `tdd`, `python-expert`, `karpathy-guidelines`, `understand` | TDD for behavior changes; Python expert for Python work; understand only after dependency preflight | implementation plan, tested modules, reproducible configuration |
| 7 | `python-expert` | `diagnosing-bugs`, `tdd`, `karpathy-guidelines` | Diagnose only when runs fail, regress, hang, or become non-deterministic | executable experiment, logs, structured results, regression checks |
| 8 | `world-model-method` | `understand-diff`, `tdd` | Use diff analysis when code changed; use TDD to lock down reproducibility failures | evidence audit, leakage/fairness report, repair decision |
| 9 | `nature-figure` | `paper-framework-figure-studio-pro` | `nature-figure` requires explicit Python/R choice; continue only `framework-concept` S4-S7; a manuscript may have at most one graphical abstract when required | publication plots, per-figure briefs, optional single graphical abstract, staged concept-framework candidates |
| 10 | `nature-writing` | `nature-reader`, `nature-citation`, `domain-modeling` | Reader grounds source claims; citation skill verifies support; domain modeling locks terminology | section drafts, claim-evidence map, missing-input list |
| 11 | `nature-writing` | `world-model-method`, `nature-citation`, `nature-data` | Load writing self-review guidance; use data skill for availability/repository issues | three-perspective review, risk-ranked revision plan |
| 12 | `nature-polishing` | `nature-writing`, `nature-citation`, `nature-data` | Route back to writing when structure is broken; polish only after argument is sound | revised prose, verified citations, data statement, revision ledger |
| 13 | `paper-framework-figure-studio-pro` | `nature-figure` | Create independent state `framework-final`; execute one S0-S7 step per user turn; nature-figure is only for quantitative panels | final framework bundle and joint semantic audit |
| 14 | `world-model-method` | `nature-writing`, `nature-citation`, `nature-data` | Use writing self-review checklist for whole-manuscript consistency | integrated manuscript, submission checklist, unresolved risks |
| 15 | `nature-polishing` | `nature-writing`, `domain-modeling` | Use writing for section reconstruction; domain modeling for term drift | publication-quality language with stable meaning and terminology |
| 16 | `world-model-method` | `nature-writing`, `nature-academic-search` | Literature search only when comparing venue literature; current journal policies require verified official guidance | qualitative desk-reject risk, reviewer simulation, transfer conditions |
| 17 | `nature-response` | `nature-writing`, `nature-polishing`, `nature-citation` | Add citation skill only when the revision introduces or disputes references | traceable response and manuscript-change checklist |

## Writing and polishing routing

| Draft state | Route | Reason |
|---|---|---|
| Core claim/evidence/boundary missing | `nature-writing` scaffold mode | expose missing science before prose |
| Section logic or paragraph jobs are broken | `nature-writing` restructure mode | rebuild argument architecture |
| Logic is sound but prose is rough | `nature-polishing` | improve language without changing meaning |
| Claims need literature support | `nature-citation` | segment, search, grade support, export |
| Source paper must be read or translated | `nature-reader` | preserve source anchors and figures |
| Reviewer comments must be answered | `nature-response` | create auditable point-by-point package |

When `nature-writing` handles Phase 10, load only the matching reference:

- Abstract: `nature-skills/nature-writing/references/abstract.md`
- Introduction: `nature-skills/nature-writing/references/introduction.md`
- Related Work: `nature-skills/nature-writing/references/related-work.md`
- Method: `nature-skills/nature-writing/references/method.md`
- Experiments/Results: `nature-skills/nature-writing/references/experiments.md`
- Conclusion: `nature-skills/nature-writing/references/conclusion.md`
- Full self-review: `nature-skills/nature-writing/references/paper-review.md`

For Discussion, use article architecture plus claim-evidence-boundary logic. Do not confuse Results observations with Discussion interpretations.

## Figure routing gates

### `nature-figure`

- If neither Python nor R is explicitly chosen, ask “Python or R?” and stop.
- Once chosen, use that backend exclusively for drawing, preview, export, and visual QA.
- Define conclusion, evidence chain, archetype, dimensions, statistics, source data, and export formats before plotting.

### `paper-framework-figure-studio-pro`

- Never run the whole S0-S7 sequence automatically.
- The user must explicitly request the current S-step.
- Execute at most one S-step per user turn and stop.
- Phase 5 creates `framework-concept` and may cover explicit S0-S3 turns; Phase 9 may continue that same state through S4-S7.
- Phase 13 creates a separate `framework-final` state and restarts at S0 from the final manuscript; never overwrite or silently reuse `framework-concept`.
- S7 is complete only after the figure, caption, legend, and body-reference text jointly pass.

## Code routing gates

- Apply `karpathy-guidelines` as coding guardrails, not as a standalone phase deliverable.
- Use `codebase-design` before introducing new module interfaces.
- Use `tdd` one behavior at a time through public interfaces.
- Use `diagnosing-bugs` only after constructing a red-capable feedback loop.
- Treat `understand` as optional because it requires an external plugin root, agents, Node.js, and pnpm; if preflight fails, fall back to direct scoped code inspection.

## Command routing additions

| Command | Skill |
|---|---|
| `/生成汇报PPT` | `nature-paper2ppt` |
| `/补充引用` | `nature-citation` |
| `/数据可用性` | `nature-data` |
| `/生成结果图` | `nature-figure` |
| `/生成图文摘要` | `nature-figure` + manuscript evidence gate |
| `/生成框架图` | `paper-framework-figure-studio-pro` |
| `/代码实现` | `codebase-design` + conditional `tdd`/`python-expert` |
| `/诊断实验错误` | `diagnosing-bugs` |

## Fallback policy

- Missing installed skill: perform a bounded manual fallback and mark `SKILL_UNAVAILABLE`.
- Missing input: produce a scaffold with `AUTHOR_INPUT_NEEDED` fields.
- Network-dependent search unavailable: preserve queries and pending verification; do not invent references.
- Figure backend/runtime unavailable: stop before rendering; do not cross-render with another backend.
- Framework-figure S-step not explicitly authorized: provide only the next legal prompt.
