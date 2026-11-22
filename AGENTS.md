## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## Agent skills

### Issue tracker

Issues and specs live as markdown files in `.scratch/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Canonical triage roles mapped to standard labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context repository layout (`CONTEXT.md` and `docs/adr/`). See `docs/agents/domain.md`.

## poteto-mode (pstack)

This repository is configured with `pstack` (`poteto-mode`). All agent sessions follow poteto-mode playbooks, progressive verification, and minimal-diff discipline.

Skills are installed under `.agents/skills/`.

Runtimes & Model Mappings:
- **Google Antigravity (Google AI Pro):** Uses `~/.gemini/config/pstack-models.md` (`pro` for bug-fix/architecture/judgment, `flash` for features/workers, `flash_lite` for mechanical tasks).
- **OpenCode (Free Models / Zen):** Uses `.opencode/pstack-models.md` configured in `.opencode/opencode.json` (`inherit` parent model across free models like DeepSeek Flash / Beam / MiMo).
- **CommandCode (Go Subscription):** Uses `.commandcode/pstack-models.md` tuned for the Go plan catalog (`DeepSeek V4 Pro` & `Qwen 4 Max` for reasoning/architecture, `DeepSeek V4.1 Flash Fast` & `Qwen 3.8 Flash` for high-throughput features, `Flint` for free fallback).
- **Verification:** Always verify changes using the project verification skill `.agents/skills/verify/` (`.\.venv\Scripts\python.exe .agents/skills/verify/scripts/verify_driver.py`).

