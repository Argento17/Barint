"""
Diagnose il_prices access for Victory and check what file types exist.
"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Bari")

from integrations.clients import il_prices as ip

VICTORY_CHAIN_ID = "7290696200003"

print("Fetching Victory file listing from laibcatalog...", flush=True)
try:
    files = ip.list_laibcatalog_files(VICTORY_CHAIN_ID)
    print(f"Files found: {len(files)}", flush=True)
    # Show all file types
    from collections import Counter
    type_counts = Counter(f.type for f in files)
    print(f"File types: {dict(type_counts)}", flush=True)
    for f in files[:20]:
        print(f"  {f.type}  {getattr(f, 'filename', '')}  {getattr(f, 'url', '')}", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)
    import traceback
    traceback.print_exc()
