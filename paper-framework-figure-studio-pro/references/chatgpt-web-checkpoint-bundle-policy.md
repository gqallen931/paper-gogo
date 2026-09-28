# ChatGPT Web Checkpoint Bundle Policy

When file artifact creation is available, ChatGPT web replies may provide a full checkpoint package so a workflow can resume in a new conversation.

The checkpoint should include:

- `state/project-state.json`;
- relevant `inputs/`;
- active `outputs/` needed for S0-S7 continuation, inspection, repair, final selection, or final joint audit;
- a skill snapshot or version note.

Use overwrite/latest semantics when possible. If the platform creates duplicates, resolve the latest checkpoint by manifest timestamp and sequence number.

Do not include caches, host-specific absolute paths, or unrelated local files.
