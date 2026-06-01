<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

# Work Classification + Registry First (MANDATORY)

This is the **website** repo. Tracked tasks and their governance live in the **Agent OS** at `C:\Bari` — not here.

**Classify first.** Conversation Work (quick advice, clarifications, prompt edits, minor copy, one-offs, lightweight reviews) → handle inline: no TASK, no registry, no dashboard. Registry Work (multi-step / reviewed deliverable / a dependency / changes shipped/governed artifacts / explicitly assigned `TASK-XXX`) → tracked.

**Registry First.** Any task-management request (**status / close / accept / reject / block / resume / reopen** of a `TASK-XXX`) **must begin by consulting the authoritative registry `C:\Bari\tasks\`** (one `TASK-NNN.md` per task; state in YAML `status:`). The registry is authoritative; conversation history is not. On conflict, the registry wins and you surface it. Unknown id → "not registered."

- Lifecycle (no other states): `IN_PROGRESS · BLOCKED · RETURNED · CHANGES_REQUESTED · CLOSED`. Only the Central Controller records `CLOSED`; agents propose `RETURNED` / `BLOCKED`.
- Canonical governance: `C:\Bari\01_framework\operations\` — `work_classification_v1.md`, `registry_first_rule_v1.md`, `registry_protocol_v1.md`.
- The old `Bari/` Agent-OS snapshot was removed from this repo (TASK-131) and `/Bari/` is now gitignored. There is **no** registry copy here — consult `C:\Bari\tasks\` only.
