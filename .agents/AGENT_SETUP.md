# Unified Agent Setup & Portability Guide

# Antigravity / Gemini
- **Status:** Installed & active in `.agents/`.
- **Rules:** `.agents/rules/context-efficiency.md` (always-on).
- **Skills:** `.agents/skills/` (`ponytail`, `caveman`, `token-saver`, `ai-product-report-writer`).
- **Context:** `.agents/context/WORKING_STATE.md` (compact working memory).

# Claude Code
- **Configuration:** Claude Code automatically reads `.agents/skills/` or `CLAUDE.md`.
- **Setup:** Symlink or copy `.agents/rules/context-efficiency.md` into `CLAUDE.md` if running in standard mode.
- **Command:** `ln -s .agents/rules/context-efficiency.md CLAUDE.md` (or copy on Windows).

# Codex
- **Configuration:** Codex reads repository instructions from `.agents/rules/` or `AGENTS.md`.
- **Setup:** Reference `.agents/skills/` in `AGENTS.md`.
- **Command:** `Copy-Item .agents/rules/context-efficiency.md AGENTS.md` (on Windows).

# Shared skills
- `.agents/skills/ponytail/SKILL.md` (Radical simplicity & YAGNI)
- `.agents/skills/caveman/SKILL.md` (Ultra-concise output)
- `.agents/skills/token-saver/SKILL.md` (Context & token minimization)
- `.agents/skills/ai-product-report-writer/SKILL.md` (Evidence-based product reports)

# Quick verification
- Verify files: `Get-ChildItem -Path .agents -Recurse`
- Check working state: `Get-Content .agents/context/WORKING_STATE.md`
