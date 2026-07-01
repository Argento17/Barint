<#
register_local_scan_task.ps1 - install the fully-local Hebrew Health Scan as a daily Windows
Scheduled Task (TASK-381, owner ruling 2026-07-01: completely automatic, no cloud, no trigger).

Runs `python local_scan.py` every day at 08:30 local. That one process reads a real Israeli
health article (this machine reaches .co.il; the cloud routine could not), runs the deterministic
no-harvest firewall, folds surviving register moves into
content_voice/tom_bari_voice/2b_learned_register_moves.md, and commits - no human, no Notion.

Also removes the now-obsolete "Bari - Hebrew Health Scan apply" task (the old Notion drain), which
is dead now that there is no Notion hop.

Usage (from an elevated-or-normal PowerShell):
  powershell -ExecutionPolicy Bypass -File register_local_scan_task.ps1
  powershell -ExecutionPolicy Bypass -File register_local_scan_task.ps1 -Unregister   # remove it
#>
param([switch]$Unregister)

$ErrorActionPreference = "Stop"
$TaskName    = "Bari - Hebrew Health Scan (local)"
$OldTaskName = "Bari - Hebrew Health Scan apply"
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScanScript  = Join-Path $ScriptDir "local_scan.py"

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
if (-not (Test-Path $ScanScript)) { throw "local_scan.py not found at $ScanScript" }

# Retire the obsolete Notion-drain task and any prior copy of this one (idempotent).
Remove-TaskIfPresent $OldTaskName
Remove-TaskIfPresent $TaskName

$action   = New-ScheduledTaskAction -Execute $python -Argument "`"$ScanScript`"" -WorkingDirectory $ScriptDir
$trigger  = New-ScheduledTaskTrigger -Daily -At 8:30am
# Fire even if the 08:30 slot was missed (machine asleep/off), and don't stop it early.
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 30) `
              -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings `
    -Principal $principal -Description "Bari Hebrew Health Scan - daily local read of Israeli health writing; auto-folds register moves into the Content Agent voice corpus (file 2b). Fully autonomous, no Notion." | Out-Null

Write-Host "registered task: $TaskName  (daily 08:30, runs: $python `"$ScanScript`")"
Write-Host "verify: Get-ScheduledTask -TaskName '$TaskName' | Get-ScheduledTaskInfo"
