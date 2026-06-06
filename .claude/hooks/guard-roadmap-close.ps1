# PreToolUse guard — task close integrity (v2, 2026-06-04)
#
# HARD BLOCKS (exit 2 — denies the tool call):
#   1. roadmap_impact: true + no cc_reviewed → must be CC-reviewed first
#   2. priority: HIGH + no cc_reviewed → must be CC-verified before closing
#      (closes the enforcement gap for non-roadmap-impact high-stakes tasks)
#   3. work_type contains "go_live" + no red_team_cleared → red-team gate required
#
# ADVISORY WARNINGS (exit 0 — allows the write but prints to stderr so the model sees it):
#   4. Any CLOSED task with no close_reason → nudge to add one
#   5. Any CLOSED task with no cc_reviewed (non-HIGH, non-roadmap) → soft reminder
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

$willClose    = $front -match 'status:\s*CLOSED'
$hasImpact    = $front -match 'roadmap_impact:\s*true'
$isHigh       = $front -match 'priority:\s*HIGH'
$reviewed     = $front -match 'cc_reviewed:\s*\S'
$hasClose     = $front -match 'close_reason:\s*\S'
$isGoLive     = $front -match 'work_type:\s*(go_live|launch)'
$rtCleared    = $front -match 'red_team_cleared:\s*\S'

# ── HARD BLOCK 1: roadmap_impact + no cc_reviewed ────────────────────────────
if ($willClose -and $hasImpact -and -not $reviewed) {
  [Console]::Error.WriteLine(
    "BLOCKED: $tid has roadmap_impact: true and no cc_reviewed date. " +
    "CC Agent must review the roadmap impact (attach cc_comments) and set " +
    "'cc_reviewed: <date>' in the frontmatter BEFORE this task can be CLOSED."
  )
  exit 2
}

# ── HARD BLOCK 2: HIGH priority + no cc_reviewed ─────────────────────────────
if ($willClose -and $isHigh -and -not $reviewed) {
  [Console]::Error.WriteLine(
    "BLOCKED: $tid is priority: HIGH with no cc_reviewed date. " +
    "CC Agent must independently verify the return-block claims against artifacts " +
    "and set 'cc_reviewed: <date>' before this task can be CLOSED. " +
    "(This is the enforcement gate for high-stakes non-roadmap-impact tasks. " +
    "If this is a trivial sub-task inadvertently marked HIGH, downgrade priority first.)"
  )
  exit 2
}

# ── HARD BLOCK 3: go_live work_type + no red_team_cleared ────────────────────
if ($willClose -and $isGoLive -and -not $rtCleared) {
  [Console]::Error.WriteLine(
    "BLOCKED: $tid has work_type: go_live and no red_team_cleared date. " +
    "A red-team challenge report (02_products/{category}/reports/red_team_*.md) " +
    "with no open CRITICAL findings is required before a go-live task can be CLOSED. " +
    "Dispatch red-team-agent, then set 'red_team_cleared: <date>' in frontmatter."
  )
  exit 2
}

# ── ADVISORY 4: CLOSED with no close_reason ──────────────────────────────────
if ($willClose -and -not $hasClose) {
  [Console]::Error.WriteLine(
    "ADVISORY: $tid is being marked CLOSED with no close_reason in frontmatter. " +
    "CC best practice: add 'close_reason: >' with evidence cited (file:line or run output). " +
    "Write is allowed; please add close_reason after."
  )
  # exit 0 — advisory only
}

# ── ADVISORY 5: Non-HIGH non-roadmap CLOSED with no cc_reviewed ──────────────
if ($willClose -and -not $reviewed -and -not $hasImpact -and -not $isHigh) {
  [Console]::Error.WriteLine(
    "ADVISORY: $tid is being marked CLOSED without cc_reviewed. " +
    "For Conversation Work this is expected. For Registry Work, CC should verify " +
    "return-block claims before close. If this is tracked work, run the CC gate first."
  )
  # exit 0 — advisory only
}

exit 0
