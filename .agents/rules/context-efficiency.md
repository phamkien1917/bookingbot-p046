# Context Efficiency

- Use the minimum context required for correctness.
- Search before reading files.
- Do not scan the repository by default.
- Do not load unrelated historical memory.
- Do not reread unchanged files unnecessarily.
- Prefer targeted code/log reads.
- Maintain a compact working state (`.agents/context/WORKING_STATE.md`).
- Stop gathering context once enough evidence exists.
- Correctness has priority over token savings.
- Unnecessary context is considered a defect.
