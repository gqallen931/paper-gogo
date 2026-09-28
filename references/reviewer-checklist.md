# Reviewer-first quality checklist

## Pre-review

- Confirm subject expertise and conflicts of interest.
- Preserve manuscript confidentiality.
- Check journal scope and article type before line editing.

## Fast screen

- Title, abstract, keywords, highlights, and graphical abstract agree.
- The work has sufficient depth for the target venue.
- The central problem and claimed advance are identifiable.

## Deep review

### Novelty

- Is the contribution more than model replacement or parameter tuning?
- Is a domain-specific mechanism or constraint encoded or tested?
- Is each priority claim grounded in literature and evidence?

### Importance

- Does the work solve a meaningful scientific or real-world problem?
- Are practical implications credible under the tested conditions?

### Evidence

- Are controls, representative baselines, and fair tuning present?
- Are data splits leakage-resistant?
- Are uncertainty, repeated runs, and statistical reporting adequate?
- Do ablations discriminate between competing explanations?
- Are robustness, generalization, efficiency, and failure cases addressed where relevant?
- Does every conclusion map to a figure, table, analysis, or verified source?

### Writing and structure

- Does the introduction begin from a puzzle or consequential problem?
- Does related work form an argument rather than a bibliography list?
- Does the method explain why each design choice exists?
- Do results interpret patterns rather than restate tables?
- Are limitations and boundary conditions explicit?

## Decision logic

- `Reject`: fatal scientific error, unsupported central claim, clear lack of novelty, out of scope, or substantiated integrity failure.
- `Major revision`: central idea is viable but important evidence or reasoning is missing.
- `Minor revision`: central claims are supported and remaining issues are local.
- `Accept`: claims, evidence, reproducibility, and presentation are publication-ready.

Keep confidential editor comments separate from author-facing feedback. Report suspected misconduct as a concern requiring editorial verification, not as a proven fact unless evidence is conclusive.
