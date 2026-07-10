<#
register_shelf_watch_task.ps1 - install the Shelf Watch pilot (TASK-570) as a WEEKLY Windows
Scheduled Task. Mirrors the Hebrew Health Scan local-scheduling precedent
(01_framework/operations/hebrew_health_scan/register_local_scan_task.ps1) because cloud
lanes cannot push in this repo and this monitor's whole point is to run unattended, locally,
off-hours.

Runs `python shelf_watch.py` every Sunday at 03:00 local. That process runs the canary
adapter-health check, then (if healthy) re-fetches nutrition + ingredients for every product
in the live cereals + bread corpora, diffs against the served frontend JSON, classifies each
delta, and writes a report JSON under 03_operations/shelf_watch/runs/. ALERT-ONLY: it never
writes to bari-web/src/data/comparisons/, never changes a score, never auto-publishes.

Usage (from an elevated-or-normal PowerShell):
  powershell -ExecutionPolicy Bypass -File register_shelf_watch_task.ps1
  powershell -ExecutionPolicy Bypass -File register_shelf_watch_task.ps1 -Unregister   # remove it
#>
param([switch]$Unregister)

$ErrorActionPreference = "Stop"
$TaskName   = "Bari - Shelf Watch (local)"
$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$WatchScript = Join-Path $ScriptDir "shelf_watch.py"

function Remove-TaskIfPresent($name) {
    $t = Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
    if ($t) { Unregister-ScheduledTask -TaskName $name -Confirm:$false; Write-Host "removed task: $name" }
}

if ($Unregister) {
    Remove-TaskIfPresent $TaskName
    Write-Host "done (unregistered)."
    return
}

$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) { throw "python not found on PATH - install/enable Python or edit this script." }
if (-not (Test-Path $WatchScript)) { throw "shelf_watch.py not found at $WatchScript" }

# Idempotent re-registration.
Remove-TaskIfPresent $TaskName

$action    = New-ScheduledTaskAction -Execute $python -Argument "`"$WatchScript`"" -WorkingDirectory $ScriptDir
# Sunday 03:00 local — off-hours, distinct from the Hebrew Health Scan's 08:30 daily slot and
# Project Comp's 20:30 evening slot (see design doc section 7).
$trigger   = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 3:00am
$settings  = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 30) `
               -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings `
    -Principal $principal -Description "Bari Shelf Watch (TASK-570) - weekly alert-only label-change monitor for the live cereals + bread corpora. Re-fetches nutrition/ingredients via the Shufersal BSIP0 engine, diffs against the served frontend JSON, classifies cosmetic/nutrition_drift/ingredient_change/page_gone, writes a report. Never changes scores, never touches served JSON, never auto-publishes." | Out-Null

Write-Host "registered task: $TaskName  (weekly Sunday 03:00, runs: $python `"$WatchScript`")"
Write-Host "verify: Get-ScheduledTask -TaskName '$TaskName' | Get-ScheduledTaskInfo"
