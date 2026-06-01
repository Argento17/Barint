# Hook 3 — BSIP2 Regression Reminder (PostToolUse)
# Fires after Write or Edit on any of the core BSIP2 engine files.
# Reminds the operator to run the regression suite before treating outputs as valid.

$raw = [Console]::In.ReadToEnd()

try {
    $data = $raw | ConvertFrom-Json
    $path = $data.tool_input.file_path
} catch {
    exit 0
}

if ($null -eq $path) { exit 0 }

# Core engine files that affect scoring — changes require regression validation
$engineFiles = @(
    'score_engine.py',
    'constants.py',
    'matrix_integrity.py',
    'router_v2.py',
    'signal_extractor.py',
    'nova_proxy.py',
    'structural_classifier.py'
)

try {
    $filename = [System.IO.Path]::GetFileName($path)
} catch {
    exit 0
}

# Must be an engine file AND live under the bsip2/proto_v0 tree
$norm         = $path -replace '/', '\'
$inProtoV0    = $norm -match '\\bsip2\\proto_v0\\'
$isEngineFile = $engineFiles -contains $filename

if ($inProtoV0 -and $isEngineFile) {
    Write-Host ""
    Write-Host "--- BSIP2 ENGINE MODIFIED ---"
    Write-Host "  File: $filename"
    Write-Host ""
    Write-Host "  Run regression checks before treating any outputs as valid:"
    Write-Host ""
    Write-Host "    cd C:\Bari\03_operations\bsip2\proto_v0\src"
    Write-Host "    python run_regression_check.py    # must pass 12/12"
    Write-Host "    python run_router_regression.py   # must pass 12/12"
    Write-Host ""
    Write-Host "  Do not copy frontend JSON or publish scores until both pass."
    Write-Host "---"
    Write-Host ""
}

exit 0
