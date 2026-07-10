# guard-off-ban.ps1 — PreToolUse hook (Write|Edit)
# Enforces the project-wide Open Food Facts ban (CLAUDE.md hard rule; off_ban_hard_rule; TASK-238)
# deterministically, per Anthropic guidance: "if it must happen every time, it's a hook."
#
# Blocks any Write/Edit that ADDS OFF usage (URL, import, or client call) to product-data,
# pipeline, or website files. Prose that documents the ban itself is allowed: a matched line
# is ignored when it also contains BANNED/ban/forbidden/asur markers.
# Exit 2 = block (stderr is shown to Claude). Any other outcome = allow.

$ErrorActionPreference = "Stop"
try {
    $raw = [Console]::In.ReadToEnd()
    if (-not $raw) { exit 0 }
    $payload = $raw | ConvertFrom-Json
    $toolInput = $payload.tool_input
    if ($null -eq $toolInput) { exit 0 }

    $filePath = "$($toolInput.file_path)"
    # Only guard data/pipeline/site trees; agent/skill/memory docs may discuss the ban.
    $guarded = @("02_products", "03_operations", "bari-web", "integrations")
    $inScope = $false
    foreach ($g in $guarded) { if ($filePath -match [regex]::Escape($g)) { $inScope = $true; break } }
    if (-not $inScope) { exit 0 }
    # The disabled client file itself is exempt (it exists so it is not re-added).
    if ($filePath -match "open_food_facts\.py$") { exit 0 }

    $newContent = @()
    if ($toolInput.PSObject.Properties["content"])    { $newContent += "$($toolInput.content)" }
    if ($toolInput.PSObject.Properties["new_string"]) { $newContent += "$($toolInput.new_string)" }
    $text = ($newContent -join "`n")
    if (-not $text) { exit 0 }

    $offPattern = "openfoodfacts\.org|open_food_facts|openfoodfacts|off_client"
    $allowPattern = "BANNED|banned|ban |forbidden|DISABLED|do not use|never use"

    $violations = @()
    foreach ($line in ($text -split "`n")) {
        if ($line -match $offPattern -and $line -notmatch $allowPattern) { $violations += $line.Trim() }
    }
    if ($violations.Count -gt 0) {
        [Console]::Error.WriteLine("BLOCKED by guard-off-ban.ps1: Open Food Facts is banned project-wide for EVERY field (CLAUDE.md hard rule, TASK-238). Unknown is acceptable; OFF is not. Offending line(s):")
        foreach ($v in $violations | Select-Object -First 5) { [Console]::Error.WriteLine("  > $v") }
        [Console]::Error.WriteLine("If a field cannot be sourced from the direct product scrape, leave it NULL and show 'data could not be retrieved'.")
        exit 2
    }
    exit 0
} catch {
    # Never let a hook crash block legitimate work.
    exit 0
}
