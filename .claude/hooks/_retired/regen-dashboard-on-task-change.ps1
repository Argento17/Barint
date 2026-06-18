# PostToolUse hook: when a registry file (tasks/TASK-*.md) is written/edited,
# keep the derived dashboard fresh automatically, and — if the change is a
# roadmap-impacting RETURN that CC Agent hasn't reviewed yet — nudge the model
# to invoke CC Agent. Deterministic freshness; the LLM never has to remember to
# regenerate. Exits 0 silently for any non-task file.
$ErrorActionPreference = 'SilentlyContinue'

$raw = [Console]::In.ReadToEnd()
try { $j = $raw | ConvertFrom-Json } catch { exit 0 }
$fp = $j.tool_input.file_path
if (-not $fp) { exit 0 }
# only react to registry task files
if ($fp -notmatch 'tasks[\\/]TASK-[^\\/]*\.md$') { exit 0 }

$root = $env:CLAUDE_PROJECT_DIR
if (-not $root) { $root = 'C:\Bari' }

# 1) regenerate the dashboard from the authoritative registry
$py = Join-Path $root '.venv\Scripts\python.exe'
if (-not (Test-Path $py)) { $py = 'python' }
$gen = Join-Path $root '05_command_center\generate_dashboard.py'
if (Test-Path $gen) { & $py $gen *> $null }

# 2) roadmap-impacting return with no CC review yet → nudge CC Agent
$content = Get-Content -Raw -LiteralPath $fp
$front = ''
if ($content -match '(?s)^---(.*?)\r?\n---') { $front = $matches[1] }
$isReturn  = $front -match 'status:\s*(RETURNED|CHANGES_REQUESTED)'
$hasImpact = $front -match 'roadmap_impact:\s*true'
$reviewed  = $front -match 'cc_reviewed:\s*\S'
if ($isReturn -and $hasImpact -and -not $reviewed) {
  $tid = 'the task'
  if ($fp -match '(TASK-[0-9A-Za-z]+)\.md$') { $tid = $matches[1] }
  $msg = "$tid returned with roadmap_impact and no cc_reviewed date. Invoke the CC Agent to assess roadmap impact, attach cc_comments, and set cc_reviewed: <date> in the task frontmatter before this task is CLOSED."
  $out = @{ hookSpecificOutput = @{ hookEventName = 'PostToolUse'; additionalContext = $msg } } | ConvertTo-Json -Compress
  Write-Output $out
}
exit 0
