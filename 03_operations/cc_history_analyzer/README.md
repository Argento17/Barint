# Claude Code History Analyzer

A **re-runnable** workflow that reads *every* Claude Code conversation on this
machine, mines it for patterns, and produces one self-contained HTML report.

## Run it

```bash
cd C:\Bari\03_operations\cc_history_analyzer
python analyze.py
```

Then open **`cc_history_report.html`** in any browser. No dependencies, no internet.

## What it reads

- All transcripts under `~/.claude/projects/**/*.jsonl`.
  Claude Code stores history keyed by the working-directory path, so this
  **already includes worktree sessions** (each worktree = its own path = its own
  folder under `projects/`). There is no separate per-worktree history store.

## What it extracts

| Output | Meaning |
|---|---|
| KPIs | conversations, messages, your prompts, tool calls, sub-agent runs, tokens, list-price value, median session |
| The headline | auto-derived pros / friction (cache reuse, error rate, interrupts, delegation) |
| Activity over time | messages per day |
| When you work | day-of-week + hour-of-day heat strips |
| Tools / models / branches / files | where the work goes |
| What you keep asking for | intent-word frequency across real prompts |
| Recurring phrasings | normalized prompts that repeat verbatim |
| **Skills worth creating** | high-frequency intents → concrete `/command` proposals, flagged `NEW` vs already-covered |
| Automation candidates | repeated manual asks worth scripting |
| Token footprint | cache-read vs input vs output, with a rough list-price estimate |

## Files

- `analyze.py` — scanner + miner (streams the corpus, writes `cc_history_data.json`)
- `report.py` — turns the JSON into the HTML (pure stdlib, CSS visuals)
- `cc_history_data.json` — raw aggregates (re-generated each run)
- `cc_history_report.html` — the report (re-generated each run)

Re-run anytime to refresh against your latest history.
