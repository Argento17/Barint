<#
  sync-archive.ps1 — refresh the in-repo archive of agent knowledge + transcripts.

  WHY: Claude Code writes memory + session transcripts to the user's home
  .claude folder (single copy, un-versioned, machine-local). This script
  mirrors that material INTO C:\Bari so it is backed up and consolidated.

  WHAT IT TOUCHES:
    - memory-archive/          <- ~/.claude/projects/c--Bari/memory  (COMMITTED)
    - docs/sessions-index.md   <- regenerated from transcripts        (COMMITTED)
    - archive/transcripts/     <- raw .jsonl session + agent logs      (GITIGNORED)
    - archive/repo-backup/     <- latest bari-monorepo.bundle          (GITIGNORED)

  The archive/ tree is gitignored on purpose (bulky + secret-bearing) and is
  NEVER pushed to the public remote. Only the curated layer is committed.

  Run from anywhere:  pwsh -File C:\Bari\scripts\sync-archive.ps1
#>
$ErrorActionPreference = 'Stop'
$proj = "C:\Users\HP\.claude\projects\c--Bari"
$repo = "C:\Bari"
$arc  = "$repo\archive"

New-Item -ItemType Directory -Force `
  "$repo\memory-archive","$arc\transcripts\main","$arc\transcripts\agents","$arc\repo-backup" | Out-Null

# 1. Memory notes (committed knowledge layer)
Copy-Item "$proj\memory\*" "$repo\memory-archive\" -Recurse -Force

# 2. Raw transcripts (gitignored archive)
Copy-Item "$proj\*.jsonl" "$arc\transcripts\main\" -Force
Get-ChildItem $proj -Directory | Where-Object { $_.Name -ne 'memory' } | ForEach-Object {
  Copy-Item $_.FullName "$arc\transcripts\agents\" -Recurse -Force
}

# 3. Repo backup bundle — already consolidated under archive/repo-backup/.
#    DO NOT read from C:\bari_backups: that folder is DEPRECATED (2026-06-05) and
#    must not be used as a source or target anymore. The in-repo copy is canonical;
#    a fresh bundle, if ever needed, should be written straight into archive/repo-backup/.

# 4. Regenerate the human-readable session index (committed)
$rows = foreach ($f in Get-ChildItem "$proj\*.jsonl") {
  $title = ""
  try {
    foreach ($line in [System.IO.File]::ReadLines($f.FullName)) {
      if ($line -notmatch '"role"\s*:\s*"user"' -and $line -notmatch '"type"\s*:\s*"user"') { continue }
      $o = $line | ConvertFrom-Json
      $c = $o.message.content
      $txt = if ($c -is [string]) { $c } elseif ($c) { ($c | Where-Object { $_.type -eq 'text' } | Select-Object -First 1).text }
      if (-not $txt -or $txt -match '<') { continue }
      $txt = ($txt -replace '\s+',' ').Trim()
      if ($txt.Length -lt 3) { continue }
      $title = if ($txt.Length -gt 90) { $txt.Substring(0,90)+[char]0x2026 } else { $txt }
      break
    }
  } catch {}
  [pscustomobject]@{ Date=$f.LastWriteTime; Id=$f.BaseName.Substring(0,8); MB=[math]::Round($f.Length/1MB,1); Title=$title }
}
$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine("# Session Index — Bari agent work log")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("Readable index of all Claude Code sessions on this project.")
[void]$sb.AppendLine("Raw transcripts live (gitignored) at ``archive/transcripts/main/<id>*.jsonl``;")
[void]$sb.AppendLine("matching sub-agent logs at ``archive/transcripts/agents/<id>/``.")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("| Date | Session | MB | Opening prompt |")
[void]$sb.AppendLine("|------|---------|----|----------------|")
foreach ($r in ($rows | Sort-Object Date)) {
  $d = $r.Date.ToString('yyyy-MM-dd HH:mm')
  $t = ($r.Title -replace '\|','\|'); if (-not $t) { $t = '_(no text prompt)_' }
  [void]$sb.AppendLine("| $d | ``$($r.Id)`` | $($r.MB) | $t |")
}
[void]$sb.AppendLine("")
[void]$sb.AppendLine("_Total: $($rows.Count) main sessions. Generated $(Get-Date -Format 'yyyy-MM-dd')._")
[System.IO.File]::WriteAllText("$repo\docs\sessions-index.md", $sb.ToString())

Write-Host "Archive synced. Commit the curated layer (memory-archive, docs) when ready; archive/ stays local."
