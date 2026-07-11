# PreToolUse guard - lesson-resolution CLOSE gate (TASK-604)
#
# Contract: 01_framework/operations/lesson_resolution_contract_v1.md
# Validator: 03_operations/validators/check_lesson_resolution.py (the ONE interpretation -
#            this hook and the required CI job (.github/workflows/lesson_resolution_gate.yml)
#            both call it directly; neither re-implements its logic).
#
# Detects a Write/Edit to tasks/TASK-*.md that sets `status: CLOSED`, reconstructs the
# resulting file content, and hands it to check_lesson_resolution.py against the REAL
# registry (so cross-task references -- lesson_generated_task_id, lesson_related, reciprocal
# provenance -- resolve correctly). The about-to-be-written content is staged in a scratch
# file that deliberately does NOT match the `TASK-*.md` glob (so it can never be picked up
# by board_check.py, the recurrence scan, or any other TASK-file tooling during the brief
# window it exists) and is always removed afterward.
#
# HARD BLOCK (exit 2 -- denies the tool call): the lesson-resolution contract is unsatisfied.
# Fails OPEN on any infra error (missing validator, missing repo root, parse/exec failure) -
# house convention: a broken hook must never brick unrelated local work.

$ErrorActionPreference = 'SilentlyContinue'

$raw = [Console]::In.ReadToEnd()
try { $j = $raw | ConvertFrom-Json } catch { exit 0 }
$ti = $j.tool_input
$fp = $ti.file_path
if (-not $fp) { exit 0 }
if ($fp -notmatch 'tasks[\\/]TASK-[^\\/]*\.md$') { exit 0 }
if ($fp -match 'tasks[\\/]closed[\\/]') { exit 0 }   # archive rewrites are not a close transition

# -- Reconstruct resulting file content --------------------------------------
$result = $null
if ($null -ne $ti.content) {
  $result = $ti.content
} elseif ($null -ne $ti.new_string) {
  $cur = Get-Content -Raw -LiteralPath $fp
  if ($null -eq $cur) { exit 0 }
  $result = $cur.Replace([string]$ti.old_string, [string]$ti.new_string)
} else {
  exit 0   # MultiEdit/unknown shape -> fail open
}

$willClose = $result -match '(?m)^status:\s*CLOSED\s*$'
if (-not $willClose) { exit 0 }

$tid = 'this task'
if ($fp -match '(TASK-[0-9A-Za-z]+)\.md$') { $tid = $matches[1] }

# -- Locate repo root (walk up from the target file for tasks\DISPATCH_BOARD.md) --
$root = Split-Path -Parent (Split-Path -Parent $fp)
$found = $false
for ($i = 0; $i -lt 8; $i++) {
  if (-not $root) { break }
  if (Test-Path (Join-Path $root 'tasks\DISPATCH_BOARD.md')) { $found = $true; break }
  $parent = Split-Path -Parent $root
  if (-not $parent -or $parent -eq $root) { break }
  $root = $parent
}
if (-not $found) { exit 0 }   # can't locate repo root -> fail open

$validator = Join-Path $root '03_operations\validators\check_lesson_resolution.py'
if (-not (Test-Path $validator)) { exit 0 }   # validator missing -> fail open (infra error)

$scratch = Join-Path $root 'tasks\_lesson_check_scratch.md'
$output = $null
$exitCode = 0
try {
  Set-Content -LiteralPath $scratch -Value $result -Encoding utf8 -NoNewline
  $output = & python $validator $scratch --root $root 2>&1 | Out-String
  $exitCode = $LASTEXITCODE
} catch {
  exit 0   # infra error -> fail open
} finally {
  Remove-Item -LiteralPath $scratch -ErrorAction SilentlyContinue
}

if ($exitCode -eq 1) {
  [Console]::Error.WriteLine(
    "BLOCKED: $tid cannot close - lesson-resolution contract unsatisfied " +
    "(01_framework/operations/lesson_resolution_contract_v1.md). Validator output:`n$output"
  )
  exit 2
} elseif ($exitCode -ne 0) {
  # usage/infra error from the validator itself -> fail open, but surface it for visibility
  [Console]::Error.WriteLine("ADVISORY: check_lesson_resolution.py returned exit $exitCode (non-blocking, infra):`n$output")
}

exit 0
