# Step Rewind Cleanup Contract

If a user returns to an earlier or current step and that step will be executed again, cleanup is mandatory before execution.

Cleanup scope is the covered span from `target_step` through the previous `current_step`, inclusive.

Cleanup must:

- delete covered output directories and canonical files;
- remove covered active artifact records;
- remove covered image generation events;
- refresh pending outputs and active artifact roles;
- preserve `state/project-state.json`;
- preserve a cleanup event audit trail.

If the user only asks a historical question, status check, or explanation, inspect state/history without cleanup.

Repair mode may read a same-step artifact as repair input, but downstream active outputs after the repaired step must be cleaned because they depended on the earlier artifact.

## S7 Rerun Cleanup

If the user enters `S7-FINAL-JOINT-AUDIT` again, treat it as a same-step rerun. Before executing S7:

- delete prior S7 output directories/files such as `outputs/S7-final-joint-audit`;
- remove prior S7 active artifact records and pending-output records;
- preserve all valid S0-S6 inputs, especially the selected S6 image and figure-text bundle;
- write a cleanup event to `state/project-state.json`;
- only then execute the new bounded S7 audit.
