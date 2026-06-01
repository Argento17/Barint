# Hook 2 — Forbidden Terms Checker (PostToolUse)
# Warns (does not block) when prohibited UI language appears in .tsx / .ts / .md files.
# Reference: C:\Bari\01_framework\bsip2_framework\ui_language.md

$raw = [Console]::In.ReadToEnd()

try {
    $data = $raw | ConvertFrom-Json
    $path = $data.tool_input.file_path
} catch {
    exit 0
}

if ($null -eq $path) { exit 0 }

# Only check frontend/editorial file types
if ($path -notmatch '\.(tsx|ts|md)$') { exit 0 }

if (-not (Test-Path $path -ErrorAction SilentlyContinue)) { exit 0 }

# Forbidden term patterns [regex, display label]
# Patterns use .NET regex syntax; -imatch = case-insensitive
$terms = @(
    @{ p = '\b(healthy|unhealthy)\b';        l = 'healthy / unhealthy' }
    @{ p = '\bclean[\s\-]?eating\b';         l = 'clean eating' }
    @{ p = '\bguilt[\s\-]?free\b';           l = 'guilt-free' }
    @{ p = '\bdetox\b';                      l = 'detox' }
    @{ p = '\bsuperfoods?\b';                l = 'superfoods' }
    @{ p = '\bnatural\b';                    l = 'natural (verify: food-descriptor context only)' }
    @{ p = 'AI[\s\-]powered';               l = 'AI-powered' }
    @{ p = 'nutritionist[\s\-]?approved';   l = 'nutritionist approved' }
    @{ p = 'better for you';                l = 'better for you' }
    @{ p = 'boosts?\s+immunity';            l = 'boosts immunity' }
    @{ p = '\bhyper[\s\-]?palatability\b';  l = 'hyper-palatability (consumer-facing)' }
    @{ p = 'our algorithm';                 l = 'our algorithm' }
    @{ p = '\bgood for you\b';              l = 'good for you' }
    @{ p = '\bbad for you\b';               l = 'bad for you' }
)

try {
    $lines = Get-Content $path -Encoding UTF8 -ErrorAction Stop
} catch {
    exit 0
}

$findings = @()
foreach ($term in $terms) {
    $lineNum = 0
    foreach ($line in $lines) {
        $lineNum++
        if ($line -imatch $term.p) {
            $findings += "  L{0,-4} [{1}]" -f $lineNum, $term.l
            $findings += "       $($line.Trim())"
        }
    }
}

if ($findings.Count -gt 0) {
    Write-Host ""
    Write-Host "--- EDITORIAL WARNING: Forbidden UI term(s) ---"
    Write-Host "  File: $path"
    Write-Host ""
    $findings | ForEach-Object { Write-Host $_ }
    Write-Host ""
    Write-Host "  Reference: C:\Bari\01_framework\bsip2_framework\ui_language.md"
    Write-Host "  Note: Imports, variable names, and code comments are likely false positives."
    Write-Host "---"
    Write-Host ""
}

exit 0
