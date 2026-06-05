# Memory Archive — versioned snapshot of agent memory

This folder is a **committed snapshot** of the Claude Code agent memory that lives at:

```
C:\Users\HP\.claude\projects\c--Bari\memory\
```

## Why this exists

The harness writes agent memory to the user's home `.claude` directory (per-user,
per-machine, un-versioned). That folder holds the living "why" behind Bari —
frozen scoring invariants, the decision-authority law, category-run outcomes,
program history (Glass Box, SIE), and owner feedback preferences — much of which
exists **nowhere in the code**. Single-copy-on-one-disk is a fragility for
knowledge this central.

This archive mirrors that knowledge **into the repo** so it is backed up,
diffable, reviewable, and travels with a fresh checkout.

## Authority

- **Live / authoritative source:** `~/.claude/projects/c--Bari/memory/` (what the
  agent actually reads and writes each session).
- **This archive:** a point-in-time snapshot. It does **not** feed back into the
  agent automatically. Treat it as backup + history, not as the working copy.

## Refreshing

This is a **manual (option 1)** snapshot. To refresh, re-copy the live folder
over this one and commit:

```powershell
Copy-Item "C:\Users\HP\.claude\projects\c--Bari\memory\*" `
          "C:\Bari\memory-archive" -Recurse -Force
```

Last snapshot: 2026-06-05.
