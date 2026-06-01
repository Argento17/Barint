# rename_website_phase3.ps1  --  TASK-131 Phase 3
# Renames the website root C:\Users\HP\bari -> C:\bari-web and repoints every
# hardcoded path reference in both the website and the Agent OS, then commits.
#
# WHY A SCRIPT: a directory can't be renamed while VS Code (or Explorer) holds it.
# Run this from a STANDALONE PowerShell with VS Code CLOSED.
#
# USAGE:
#   1. Close VS Code and any Explorer window pointed at C:\Users\HP\bari.
#   2. Win+R -> "powershell" -> Enter, then:
#        & 'C:\Bari\05_command_center\rename_website_phase3.ps1'
#   3. Reopen the project at C:\bari-web. Optionally re-run `npm run dev`.

$ErrorActionPreference = 'Stop'
$old = 'C:\Users\HP\bari'
$new = 'C:\bari-web'

# --- preconditions -----------------------------------------------------------
if (-not (Test-Path $old)) { Write-Host "Source $old not found - already renamed? Aborting."; exit 1 }
if (Test-Path $new)        { Write-Host "Target $new already exists. Aborting.";              exit 1 }

# --- stop any dev server still on :3000 --------------------------------------
$conn = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue
foreach ($c in $conn) { try { Stop-Process -Id $c.OwningProcess -Force; Write-Host "stopped PID $($c.OwningProcess) on :3000" } catch {} }
Start-Sleep -Seconds 1

# --- the rename (same volume = fast metadata move; keeps .git/node_modules) ---
Move-Item -LiteralPath $old -Destination $new
Write-Host "RENAMED  $old  ->  $new"

# --- repoint hardcoded paths (literal, case-sensitive; UTF-8 no BOM) ---------
function Repoint([string[]]$files) {
  foreach ($f in $files) {
    if (-not (Test-Path -LiteralPath $f)) { continue }
    $t = Get-Content -LiteralPath $f -Raw
    $n = $t.Replace('C:\Users\HP\bari','C:\bari-web').
            Replace('c:/Users/HP/bari','c:/bari-web').
            Replace('C:/Users/HP/bari','C:/bari-web').
            Replace('//c/Users/HP/bari','//c/bari-web')
    if ($n -ne $t) {
      [System.IO.File]::WriteAllText($f, $n, (New-Object System.Text.UTF8Encoding($false)))
      Write-Host "  patched $f"
    }
  }
}

# Agent OS docs (text only - never the data/Hebrew trees)
$bariFiles  = Get-ChildItem 'C:\Bari' -File -Filter *.md | ForEach-Object FullName
$bariFiles += Get-ChildItem 'C:\Bari\.claude' -Recurse -File -Include *.md,*.json | ForEach-Object FullName
Repoint $bariFiles

# Website: the one non-build audit script that hardcodes its own path
Repoint @("$new\scripts\audit-snacks-data-lineage.mjs")

# --- commit both repos (website: ONLY the audit script, never your WIP edits)-
git -C $new add scripts/audit-snacks-data-lineage.mjs
git -C $new commit -m "Repoint audit script to C:\bari-web (TASK-131 Phase 3)" 2>$null
git -C 'C:\Bari' add -A
git -C 'C:\Bari' commit -m "Rename website root to C:\bari-web; repoint Agent OS docs (TASK-131 Phase 3)" 2>$null

Write-Host ""
Write-Host "DONE. Verify with:"
Write-Host "  cd C:\bari-web ; npm run lint ; npm run build"
