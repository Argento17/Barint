# Sync Design — Raw Store on VM, Pulled to Repo Machine

## Architecture

```
┌─────────────────────┐          ┌──────────────────────┐
│  Kamatera VM         │          │  Repo machine (Win)   │
│  (Israeli IP)        │          │  (parsing, scoring)   │
│                      │  pull    │                       │
│  /opt/bari/          │ ←─────── │  rclone copy / ssh    │
│    raw_store/        │  on      │                       │
│      YYYY-MM-DD/     │  demand  │  + /opt/bari/parse/   │
│        *.html        │          │                       │
│        manifest.jsonl│          │  C:\Bari\ is NOT      │
│  ...                 │          │  touched by VM        │
└─────────────────────┘          └──────────────────────┘
```

- VM does **only**: fetch page → hash → if changed, save raw HTML → append to manifest.
- All parsing, scoring, corpus-building happens **on the repo machine** (offline, no live-site dependency).
- No git on the VM for raw HTML. Raw HTML is often megabytes; git would bloat the repo.
- A lightweight `manifest.jsonl` (one JSON line per fetched URL) CAN be git-synced for traceability.

## Directory layout on VM (`/opt/bari/raw_store/`)

```
raw_store/
  2026-06-12/                  # date of fetch run
    001_shufersal_yogurt/
      listing_search_יוגורט_20260612T120000.html
      listing_cat_A4002_20260612T120500.html
      product_7290008316037_20260612T121000.html
      product_7290014972572_20260612T121500.html
      ...
    manifest.jsonl             # one line per fetched URL
  …
  2026-06-19/                  # next week's run
    …
```

### manifest.jsonl format

```jsonl
{"ts":"2026-06-12T12:10:00Z","retailer":"shufersal","category":"yogurt","type":"product","url":"https://…/A7290008316037","barcode":"7290008316037","sha256":"abc123…","path":"2026-06-12/001_shufersal_yogurt/product_7290008316037_20260612T121000.html","size":45231,"status":200}
{"ts":"2026-06-12T12:05:00Z","retailer":"shufersal","category":"yogurt","type":"listing","url":"https://…/search?q=יוגורט","sha256":"def456…","path":"2026-06-12/001_shufersal_yogurt/listing_search_יוגורט_20260612T120000.html","size":128340,"status":200}
```

## Pull command (run on repo machine to sync)

```bash
rclone copy \
    --progress \
    --include "*.html" \
    --include "manifest.jsonl" \
    vm-bari:/opt/bari/raw_store/ \
    /opt/bari/raw_store/
```

Where `vm-bari` is an rclone remote configured via:
```bash
rclone config create vm-bari sftp host=5.xxx.xxx.xxx user=ubuntu key_file=~/.ssh/id_ed25519
```

Or without rclone (simpler, requires no config):
```bash
rsync -avz --include='*.html' --include='manifest.jsonl' --exclude='*' \
    ubuntu@5.xxx.xxx.xxx:/opt/bari/raw_store/ \
    /opt/bari/raw_store/
```

On Windows (repo machine), use `scp` or WinSCP from WSL.

## What gets pulled vs parsed

| Step | Where | What |
|---|---|---|
| Fetch + hash | VM | Raw HTML → `/opt/bari/raw_store/` |
| Pull raw | Repo machine | `rclone pull` → local copy |
| Parse | Repo machine | `bsip0_nutrition` + BSIP0 gate → BSIP1 → BSIP2 |
| Diff | Repo machine | Compare against existing corpus |
| Git track | Repo machine | Only manifest.jsonl (optional) |

## Why not git for raw HTML

- A single listing page is ~100–200 KB. A weekly yogurt sweep (30 listings × 100 KB + 100 products × 50 KB) = ~8 MB/week. Over a year ≈ 400 MB in git history.
- Raw HTML has no diff value — the content hash tells us if it changed; the full file is needed only for re-parsing.
- `manifest.jsonl` is small (a few KB per run) and CAN be git-tracked for an audit trail of "what was fetched when."

## Rclone config for the owner

On the repo machine, run once:
```bash
rclone config create vm-bari sftp host=5.xxx.xxx.xxx user=ubuntu \
    key_file=~/.ssh/id_ed25519
```

Then pull with:
```bash
rclone sync vm-bari:/opt/bari/raw_store/ /opt/bari/raw_store/ --progress
```
