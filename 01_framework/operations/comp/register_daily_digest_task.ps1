<#
register_daily_digest_task.ps1 - install the FULLY-LOCAL Bari Daily Digest as a daily Windows
Scheduled Task (owner 2026-07-09, after the cloud routine failed to deliver email or Notion headless).

Runs `python bari_daily_digest.py` every day at 06:00 local. That one process invokes headless
`claude` (this machine reaches .co.il and is logged in), builds ONE 4-category digest (BSIP2
improvements / blog materials / contemporary news / guides), and posts the actionable rows to the
'Bari Routine Log' in Notion via the Notion REST API, archiving a local copy under daily_digests/.
No cloud agent, no MCP connector, no human trigger.

Prereq: a Notion internal-integration token must be available to the task, EITHER as a user env var
BARI_NOTION_TOKEN, OR in the local file 01_framework/operations/comp/.daily_digest_secret
(gitignored). Create at notion.so/my-integrations, then SHARE the 'Bari Routine Log' database with it.

Usage (normal PowerShell, ASCII only - PS 5.1 mangles non-ASCII dashes):
  powershell -ExecutionPolicy Bypass -File register_daily_digest_task.ps1
  powershell -ExecutionPolicy Bypass -File register_daily_digest_task.ps1 -Unregister
#>
param([switch]$Unregister)

$ErrorActionPreference = "Stop"
$TaskName    = "Bari - Daily Digest (local)"
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$DigestScript = Join-Path $ScriptDir "bari_daily_digest.py"

function Remove-TaskIfPresent($name) {
    $t = Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
    if ($t) { Unregister-ScheduledTask -TaskName $name -Confirm:$false; Write-Host "removed task: $name" }
}

if ($Unregister) {
    Remove-TaskIfPresent $TaskName
    Write-Host "done (unregistered)."
    return
}

# Prefer the repo venv python if present (matches local_scan.py convention), else PATH python.
$venvPy = Join-Path (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $ScriptDir))) ".venv\Scripts\python.exe"
if (Test-Path $venvPy) {
    $python = $venvPy
} else {
    $python = (Get-Command python -ErrorAction SilentlyContinue).Source
}
if (-not $python) { throw "python not found (no .venv and none on PATH)." }
if (-not (Test-Path $DigestScript)) { throw "bari_daily_digest.py not found at $DigestScript" }

Remove-TaskIfPresent $TaskName

$action   = New-ScheduledTaskAction -Execute $python -Argument "`"$DigestScript`"" -WorkingDirectory $ScriptDir
$trigger  = New-ScheduledTaskTrigger -Daily -At 6:00am
# Fire even if 06:00 was missed (machine asleep/off); allow on battery; 20-min ceiling.
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 20) `
              -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
# Interactive logon so the already-logged-in `claude` CLI is reachable (same as the Hebrew scan task).
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings `
    -Principal $principal -Description "Bari Daily Digest - daily 06:00 local. Reads web + repo, builds a 4-category intelligence digest (BSIP2 improvements / blog / news / guides), posts rows to the 'Bari Routine Log' in Notion via the REST API. Fully local, no cloud agent, no MCP connector." | Out-Null

Write-Host "registered task: $TaskName  (daily 06:00, runs: $python `"$DigestScript`")"
Write-Host "verify: Get-ScheduledTask -TaskName '$TaskName' | Get-ScheduledTaskInfo"
Write-Host "test now: & '$python' '$DigestScript' --dry-run   (builds + archives, does NOT post to Notion)"
