# PreToolUse guard — go-live close integrity (v3, 2026-06-13)
#
# Post-command-center / post-CC rewrite. The orchestrator now holds undivided
# closing authority and runs verify-before-close itself, so the old cc_reviewed
# gates are gone. What remains is the ONE close guard that checks a real artifact,
# not a process field:
#
# HARD BLOCK (exit 2 — denies the tool call):
#   work_type contains "go_live"/"launch" + no red_team_cleared → red-team gate required
#
# ADVISORY WARNING (exit 0 — allows the write, prints to stderr so the model sees it):
#   Any CLOSED task with no close_reason → nudge to add one
#
# Fails OPEN on any parse uncertainty (never bricks an unrelated edit).

$ErrorActionPreference = 'SilentlyContinue'

$raw = [Console]::In.ReadToEnd()
try { $j = $raw | ConvertFrom-Json } catch { exit 0 }
$ti = $j.tool_input
$fp = $ti.file_path
if (-not $fp) { exit 0 }
if ($fp -notmatch 'tasks[\\/]TASK-[^\\/]*\.md$') { exit 0 }

# ── Reconstruct resulting file content ───────────────────────────────────────
$result = $null
if ($null -ne $ti.content) {
  $result = $ti.content
} elseif ($null -ne $ti.new_string) {
  $cur = Get-Content -Raw -LiteralPath $fp
  if ($null -eq $cur) { exit 0 }
  $result = $cur.Replace([string]$ti.old_string, [string]$ti.new_string)
} else {
  exit 0   # MultiEdit/unknown → fail open
}

# ── Extract frontmatter ───────────────────────────────────────────────────────
$front = ''
if ($result -match '(?s)^---(.*?)\r?\n---') { $front = $matches[1] } else { exit 0 }

$tid = 'this task'
if ($fp -match '(TASK-[0-9A-Za-z]+)\.md$') { $tid = $matches[1] }

$willClose = $front -match 'status:\s*CLOSED'
$hasClose  = $front -match 'close_reason:\s*\S'
$isGoLive  = $front -match 'work_type:\s*(go_live|launch)'
$rtCleared = $front -match 'red_team_cleared:\s*\S'

# ── HARD BLOCK: go_live work_type + no red_team_cleared ──────────────────────
if ($willClose -and $isGoLive -and -not $rtCleared) {
  [Console]::Error.WriteLine(
    "BLOCKED: $tid has work_type: go_live and no red_team_cleared date. " +
    "A red-team challenge report (02_products/{category}/reports/red_team_*.md) " +
    "with no open CRITICAL findings is required before a go-live task can be CLOSED. " +
    "Dispatch red-team-agent, then set 'red_team_cleared: <date>' in frontmatter."
  )
  exit 2
}

# ── ADVISORY: CLOSED with no close_reason ────────────────────────────────────
if ($willClose -and -not $hasClose) {
  [Console]::Error.WriteLine(
    "ADVISORY: $tid is being marked CLOSED with no close_reason. " +
    "Orchestrator discipline: add 'close_reason: >' citing the evidence verified " +
    "(file:line or run output). Write is allowed; please add close_reason after."
  )
  # exit 0 — advisory only
}

exit 0
