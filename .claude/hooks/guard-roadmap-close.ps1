# PreToolUse guard: block marking a task CLOSED while it still has
# roadmap_impact: true and no cc_reviewed date. Enforcement, not reminder —
# a roadmap-impacting return cannot be closed before CC Agent has reviewed it.
# Fails OPEN on any parse uncertainty (never bricks an unrelated edit).
$ErrorActionPreference = 'SilentlyContinue'

$raw = [Console]::In.ReadToEnd()
try { $j = $raw | ConvertFrom-Json } catch { exit 0 }
$ti = $j.tool_input
$fp = $ti.file_path
if (-not $fp) { exit 0 }
if ($fp -notmatch 'tasks[\\/]TASK-[^\\/]*\.md$') { exit 0 }

# Reconstruct the resulting file content for Write or Edit
$result = $null
if ($null -ne $ti.content) {
  $result = $ti.content                      # Write: full new content
} elseif ($null -ne $ti.new_string) {
  $cur = Get-Content -Raw -LiteralPath $fp   # Edit: apply the replacement in-memory
  if ($null -eq $cur) { exit 0 }
  $result = $cur.Replace([string]$ti.old_string, [string]$ti.new_string)
} else {
  exit 0                                     # MultiEdit/unknown shape → fail open
}

# Only the frontmatter matters
$front = ''
if ($result -match '(?s)^---(.*?)\r?\n---') { $front = $matches[1] } else { exit 0 }

$willClose = $front -match 'status:\s*CLOSED'
$hasImpact = $front -match 'roadmap_impact:\s*true'
$reviewed  = $front -match 'cc_reviewed:\s*\S'

if ($willClose -and $hasImpact -and -not $reviewed) {
  $tid = 'this task'
  if ($fp -match '(TASK-[0-9A-Za-z]+)\.md$') { $tid = $matches[1] }
  [Console]::Error.WriteLine("BLOCKED: $tid has roadmap_impact: true and no cc_reviewed date. CC Agent must review the roadmap impact (attach cc_comments) and set 'cc_reviewed: <date>' in the frontmatter BEFORE this task can be CLOSED.")
  exit 2   # deny the tool call; stderr is shown to the model
}
exit 0
