# guard-two-gate-commit.ps1 -- PreToolUse hook (Bash|PowerShell)
# Enforces the two-gate content sign-off (CLAUDE.md hard rule, owner ruling 2026-06-20) at the
# COMMIT boundary: a git commit that STAGES consumer-facing comparison JSON is blocked unless a
# sign-off marker exists for each staged file. ASCII-only file (PS 5.1 reads no-BOM as ANSI).
#
# Marker convention (written by the ORCHESTRATOR only, after BOTH gates pass):
#   C:\Bari\tasks\signoffs\<json-basename>.ok   (e.g. milk_frontend_v1.json.ok)
# containing one line: date + content-gate ref + red-team report path.
# The marker must be NEWER than the JSON file.
# Exit 2 = block. Fails open on script error (never blocks unrelated work).
#
# 2026-07-04 fix: gate on STAGED files only (a commit never includes unstaged working-tree
#   changes -- the old `git status --porcelain` inclusion produced false-positives that blocked
#   UNRELATED commits whenever any comparison JSON was merely dirty). Also scope the staged-file
#   check to the ACTUAL commit's repo/worktree (payload cwd) rather than a fixed CLAUDE_PROJECT_DIR,
#   so worktree-dispatched commits are gated correctly. Sign-off markers always live in the main
#   registry (CLAUDE_PROJECT_DIR).

$ErrorActionPreference = "Stop"
try {
    $raw = [Console]::In.ReadToEnd()
    if (-not $raw) { exit 0 }
    $payload = $raw | ConvertFrom-Json
    $cmd = "$($payload.tool_input.command)"
    # 2026-07-10 fix (TASK-555): trigger on ANY real `git ... commit` invocation. The old
    # regex (git\s+commit) missed `git -C <path> commit` -- the standard worktree commit
    # pattern -- so every such commit bypassed this guard entirely. `commit` must be the
    # SUBCOMMAND (git + global options like -C/-c/--flags, then commit), not merely a word
    # anywhere in the command -- otherwise filenames like guard-two-gate-commit.ps1
    # false-trigger and the hook blocks its own remediation commands.
    $gitCommitRe = '\bgit\b(\s+(-C\s+("[^"]+"|''[^'']+''|[^\s|;&]+)|-c\s+\S+|--[\w-]+(=\S+)?))*\s+commit\b'
    if ($cmd -notmatch $gitCommitRe) { exit 0 }

    # Marker registry = main project dir (markers live in C:\Bari\tasks\signoffs regardless of worktree).
    $markerRoot = $env:CLAUDE_PROJECT_DIR
    if (-not $markerRoot) { $markerRoot = "C:\Bari" }

    # Commit repo = the actual working dir the git commit runs in (worktree-aware), else fall back.
    $cwd = "$($payload.cwd)"
    # 2026-07-10 (TASK-555): `git -C <path> commit` runs against <path>, not the shell cwd --
    # scope the staged-file check to the -C target so the right repo is gated.
    if ($cmd -match '\bgit\b\s+-C\s+(?:"([^"]+)"|''([^'']+)''|([^\s|;&]+))') {
        $cTarget = if ($Matches[1]) { $Matches[1] } elseif ($Matches[2]) { $Matches[2] } else { $Matches[3] }
        if ($cTarget -and (Test-Path $cTarget)) { $cwd = $cTarget }
    }
    if (-not $cwd -or -not (Test-Path $cwd)) { $cwd = $markerRoot }
    $commitRepo = git -C $cwd rev-parse --show-toplevel 2>$null
    if (-not $commitRepo) { $commitRepo = $cwd }

    # Gate on STAGED files only -- that is exactly what the commit will contain.
    $staged = git -C $commitRepo diff --cached --name-only 2>$null
    $candidates = @($staged) | Where-Object { $_ -match "bari-web/src/data/comparisons/.*\.json$" } | Sort-Object -Unique
    if (-not $candidates -or $candidates.Count -eq 0) { exit 0 }

    $missing = @()
    foreach ($f in $candidates) {
        $base = Split-Path $f -Leaf
        $marker = Join-Path $markerRoot "tasks\signoffs\$base.ok"
        $full = Join-Path $commitRepo ($f -replace "/", "\")
        if (-not (Test-Path $marker)) { $missing += "$base (no marker tasks\signoffs\$base.ok)"; continue }
        if ((Test-Path $full) -and ((Get-Item $marker).LastWriteTime -lt (Get-Item $full).LastWriteTime)) {
            $missing += "$base (marker older than the JSON - re-run both gates)"
        }
    }
    if ($missing.Count -gt 0) {
        [Console]::Error.WriteLine("BLOCKED by guard-two-gate-commit.ps1: comparison JSON staged without two-gate sign-off (Content Agent + Adversarial QA / Red-Team; CLAUDE.md hard rule 2026-06-20):")
        foreach ($m in $missing) { [Console]::Error.WriteLine("  > $m") }
        [Console]::Error.WriteLine("After BOTH gates pass, the orchestrator writes tasks\signoffs\<json-basename>.ok (date + content-gate ref + red-team report path), then commit.")
        exit 2
    }

    # 2026-07-08 (TASK-541, owner ruling): third enforcement layer -- staged comparison JSON must
    # also pass the deterministic copy-authored gate (banned data-state narration phrases,
    # mass-repeated sentences, baseline template fingerprints). Runs only when the validator exists;
    # infrastructure errors fail OPEN (this try/catch), but a real validator FAIL blocks the commit.
    $validator = Join-Path $markerRoot "03_operations\spine\validate_copy_authored.py"
    if (Test-Path $validator) {
        $copyFails = @()
        foreach ($f in $candidates) {
            $full = Join-Path $commitRepo ($f -replace "/", "\")
            if (-not (Test-Path $full)) { continue }
            # cmd /c wrapper: PS 5.1 wraps native stderr into ErrorRecords under EAP=Stop,
            # which would throw into the outer catch and silently fail OPEN. cmd absorbs it.
            cmd /c "python ""$validator"" --json ""$full"" >NUL 2>&1"
            if ($LASTEXITCODE -eq 1) { $copyFails += $f }
        }
        if ($copyFails.Count -gt 0) {
            [Console]::Error.WriteLine("BLOCKED by guard-two-gate-commit.ps1: staged comparison JSON FAILS the copy-authored gate (banned data-state/mechanism narration, mass-repeated sentences, or baseline template fingerprints -- owner ruling 2026-07-08, TASK-541):")
            foreach ($f in $copyFails) { [Console]::Error.WriteLine("  > $f") }
            [Console]::Error.WriteLine("Run: python 03_operations\spine\validate_copy_authored.py --json <file> for the finding list. Fix the copy (never the gate) and re-gate.")
            exit 2
        }
    }
    exit 0
} catch {
    exit 0
}
