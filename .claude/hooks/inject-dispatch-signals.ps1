# inject-dispatch-signals.ps1 — UserPromptSubmit hook (TASK: dispatch board signals)
# Prints the board's signal-checkbox lines; stdout is injected into Claude's context
# with every user message. Deterministic, no LLM, ~10 lines of output max.
$root = $env:CLAUDE_PROJECT_DIR
if (-not $root) { $root = 'C:\Bari' }
$board = Join-Path $root 'tasks\DISPATCH_BOARD.md'
if (-not (Test-Path $board)) { exit 0 }
$lines = Select-String -Path $board -Pattern '^- \[.\] P\d' -Encoding UTF8 | ForEach-Object { $_.Line }
if ($lines) {
    Write-Output 'Dispatch board signals (auto-injected from tasks\DISPATCH_BOARD.md; [x] = owner has sent that prompt to its agent):'
    $lines | Write-Output
}
exit 0
