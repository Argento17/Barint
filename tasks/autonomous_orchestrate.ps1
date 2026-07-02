# Bari Autonomous Orchestrate — 3 AM self-firing /orchestrate pass.
# Created 2026-06-22. Operationalizes [[owner-interaction-contract]].
# Runs ONE headless /orchestrate pass against C:\Bari\tasks\, logs + digests.
# Disable:  Disable-ScheduledTask -TaskName 'Bari Autonomous Orchestrate'
# Delete:   Unregister-ScheduledTask -TaskName 'Bari Autonomous Orchestrate' -Confirm:$false

$ErrorActionPreference = 'Stop'
$today  = Get-Date -Format 'yyyy-MM-dd'
$logDir = 'C:\Bari\tasks\digests'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir "$today-orchestrate.log"
Set-Location 'C:\Bari'

$prompt = @'
/orchestrate

UNATTENDED 3AM RUN — operating constraints:
- Run ONE full dispatch pass against C:\Bari\tasks\. Full autonomous close on non-tripwire work: verify each return-block claim against artifacts at file:line, then set status CLOSED with a close_reason citing the evidence.
- HALT and park for the owner on ANY of the 5 strategic tripwires, ANY consumer-facing deploy, or when out of ready work. Never move a published score, never deploy.
- You are unattended: you MAY run native subagent (Sonnet) C1 work, verification, registry closes, and commits to a DEDICATED BRANCH (never master).
- Do NOT dispatch the cloud CLI lanes (Cursor / Grok / Gemini-agy) unattended — they bulk-upload the tree and can wipe untracked files with no human to catch it. QUEUE any work needing those lanes and surface it in the digest for the owner's supervised morning kick.
- Write a single digest to C:\Bari\tasks\digests\<today>-orchestrate.md with sections: Dispatched / Closed (with evidence) / Blocked / Parked-for-owner (tripwires) / Queued-for-supervised-lanes.
'@

claude -p $prompt --dangerously-skip-permissions --add-dir C:\Bari *>&1 | Tee-Object -FilePath $log
