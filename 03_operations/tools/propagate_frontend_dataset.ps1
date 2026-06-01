#Requires -Version 5.1
<#
.SYNOPSIS
    Copies one BSIP2 frontend dataset JSON into the website comparison data directory.

.PARAMETER SourceFile
    Full path to the source JSON file.
    Must be inside C:\Bari\03_operations\bsip2\proto_v0\outputs\.

.PARAMETER DestName
    Target filename only — no path component.
    Example: snacks_frontend_v3.json

.EXAMPLE
    .\propagate_frontend_dataset.ps1 `
        -SourceFile "C:\Bari\03_operations\bsip2\proto_v0\outputs\snacks_frontend_v3.json" `
        -DestName   "snacks_frontend_v3.json"
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$SourceFile,

    [Parameter(Mandatory = $true)]
    [string]$DestName
)

Set-StrictMode -Version Latest

$APPROVED_SRC = 'C:\Bari\02_products'
$DEST_DIR     = 'C:\Users\HP\bari\src\data\comparisons'

function Abort([string]$reason) {
    Write-Host "FAIL: $reason"
    exit 1
}

# V1 — Source path exists
if (-not (Test-Path -LiteralPath $SourceFile -PathType Leaf)) {
    Abort "Source not found: $SourceFile"
}

# V2 — Source is inside the approved BSIP2 outputs directory
$srcAbs      = (Resolve-Path -LiteralPath $SourceFile).ProviderPath
$approvedAbs = [IO.Path]::GetFullPath($APPROVED_SRC).TrimEnd('\') + '\'
if (-not $srcAbs.StartsWith($approvedAbs, [StringComparison]::OrdinalIgnoreCase)) {
    Abort "Source is outside approved directory.`n  Source   : $srcAbs`n  Approved : $approvedAbs"
}

# V5 — Destination filename ends with .json (must resolve before V3)
if (-not $DestName.EndsWith('.json', [StringComparison]::OrdinalIgnoreCase)) {
    Abort "DestName must end with .json: $DestName"
}

# V3 — Destination path stays inside the website comparison data directory
$destAbs    = [IO.Path]::GetFullPath([IO.Path]::Combine($DEST_DIR, $DestName))
$destDirAbs = [IO.Path]::GetFullPath($DEST_DIR).TrimEnd('\') + '\'
if (-not $destAbs.StartsWith($destDirAbs, [StringComparison]::OrdinalIgnoreCase)) {
    Abort "DestName escapes the approved directory.`n  Resolved : $destAbs`n  Approved : $destDirAbs"
}

# V4 — Source is valid JSON
try {
    $raw  = [IO.File]::ReadAllText($SourceFile, [Text.Encoding]::UTF8)
    $null = $raw | ConvertFrom-Json
} catch {
    Abort "Source is not valid JSON: $($_.Exception.Message)"
}

# V6 — Destination directory exists
if (-not (Test-Path -LiteralPath $DEST_DIR -PathType Container)) {
    Abort "Destination directory not found: $DEST_DIR"
}

# Backup existing destination file if present
$backupPath = $destAbs + '.bak'
$backedUp   = $false
if (Test-Path -LiteralPath $destAbs -PathType Leaf) {
    Copy-Item -LiteralPath $destAbs -Destination $backupPath -Force
    $backedUp = $true
    Write-Host "Backup : $backupPath"
}

# Copy
try {
    Copy-Item -LiteralPath $SourceFile -Destination $destAbs -Force
} catch {
    if ($backedUp -and (Test-Path -LiteralPath $backupPath -PathType Leaf)) {
        Move-Item -LiteralPath $backupPath -Destination $destAbs -Force
        Write-Host "Rollback: previous file restored from backup."
    }
    Abort "Copy failed: $($_.Exception.Message)"
}

# V7 — Byte count match
$srcBytes = (Get-Item -LiteralPath $SourceFile).Length
$dstBytes = (Get-Item -LiteralPath $destAbs).Length
if ($srcBytes -ne $dstBytes) {
    if ($backedUp -and (Test-Path -LiteralPath $backupPath -PathType Leaf)) {
        Move-Item -LiteralPath $backupPath -Destination $destAbs -Force
        Write-Host "Rollback: previous file restored from backup."
    }
    Abort "Byte count mismatch. Source: $srcBytes bytes  Dest: $dstBytes bytes"
}

# Done
Write-Host ""
Write-Host "PROPAGATION COMPLETE"
Write-Host "Source   : $SourceFile"
Write-Host "Dest     : $destAbs"
Write-Host "Bytes    : $srcBytes (match confirmed)"
if ($backedUp) { Write-Host "Backup   : $backupPath" }
Write-Host ""
Write-Host "Next (Frontend Architect):"
Write-Host "  1. Confirm or update import in page-data file:"
Write-Host "       @/data/comparisons/$DestName"
Write-Host "  2. npm run build"
Write-Host "  3. npx tsc --noEmit"
Write-Host "  4. Notify QA & Audit Lead when both pass."
