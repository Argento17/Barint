"""
P75b Bleed Simulation — TASK-275
Run ALL biscuit anchors from router_v2.py against EVERY live category BSIP1 corpus.
HARD GATE: must be 0 hits. Any hit = STOP.

Live corpora checked:
  milk         : run_milk_001/output
  yogurt       : run_yogurt_001/output
  bread        : run_001/output (bread retail corpus)
  cereals      : run_cereals_001/output
  brined-cheese: run_brined_cheeses_001/output
  cheese-spread: run_cheese_001/output
  hard-cheese  : run_hard_cheeses_001/output
  hummus       : run_hummus_001/output
  juices       : run_juices_001/output

Biscuit anchors tested (all of them from router_v2.py):
  פתי בר, פתי-בר, פתיבר, פטי בר, פטי-בר, פטיבר,
  ביסקוויט בלגי, ביסקוויט תה, מרי ביסקוויט, ביסקוויט מרי,
  עוגיות חמאה, ביסקוויט, לוטוס, דייג'סטיב, ביסקוטי, שורטברד,
  עוגיות  (bare — the risk anchor, exclusions applied)

Exclusion logic from ANCHOR_EXCLUSIONS is applied during matching.
"""
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(r"C:\Bari")
BSIP1_ROOT = ROOT / "03_operations" / "bsip1"

# Live corpora: (label, bsip1_dir_path)
LIVE_CORPORA = [
    ("milk",         BSIP1_ROOT / "run_milk_001" / "output"),
    ("yogurt",       BSIP1_ROOT / "run_yogurt_001" / "output"),
    ("bread",        BSIP1_ROOT / "run_001" / "output"),
    ("cereals",      BSIP1_ROOT / "run_cereals_001" / "output"),
    ("brined-cheese",BSIP1_ROOT / "run_brined_cheeses_001" / "output"),
    ("cheese-spread",BSIP1_ROOT / "run_cheese_001" / "output"),
    ("hard-cheese",  BSIP1_ROOT / "run_hard_cheeses_001" / "output"),
    ("hummus",       BSIP1_ROOT / "run_hummus_001" / "output"),
    ("juices",       BSIP1_ROOT / "run_juices_001" / "output"),
]

# Biscuit anchors from router_v2.py — (term, ANCHOR_EXCLUSIONS for that term)
BISCUIT_ANCHORS = [
    ("ביסקוויט בלגי",  []),
    ("ביסקוויט תה",    []),
    ("מרי ביסקוויט",   []),
    ("ביסקוויט מרי",   []),
    ("עוגיות חמאה",    ["ממולא", "שוקולד", "ציפוי", "מצופה", "חטיף", "גרנולה", "דגנים"]),
    ("פטי-בר",         []),
    ("פטי בר",         []),
    ("פתי-בר",         []),
    ("פתי בר",         []),
    ("פתיבר",          []),
    ("פטיבר",          []),
    ("ביסקוויט",       ["מילוי", "שכבת", "ציפוי", "קרם", "טחינה", "מצופה", "גבינה", "שוקולד ביסקוויט"]),
    ("לוטוס",          ["מילוי", "ציפוי", "שכבת", "רוטב", "קרם", "מצופה", "גלידה"]),
    ("דייג'סטיב",      ["חטיף", "ציפוי"]),
    ("ביסקוטי",        ["גלידה", "מילוי"]),
    ("שורטברד",        ["גלידה", "מילוי"]),
    # EV-058 / P89 oat-cookie anchor (must run before bare עוגיות)
    ("עוגיות שיבולת שועל", ["גרנולה", "מוזלי", "מוסלי", "חטיף", "ברים",
                             "ממרח", "וופל", "קרקר", "פריכיות", "ציפוי",
                             "מילוי", "קרם", "שכבת", "אנרגיה", "חלבון"]),
    # Bare עוגיות — the risk anchor
    ("עוגיות",         ["אורז", "גרנולה", "דגנים", "מוזלי", "מוסלי", "חטיף",
                        "ברים", "ממרח", "וופל", "קרקר", "פריכיות", "ציפוי",
                        "מילוי", "קרם", "שכבת", "אנרגיה", "חלבון"]),
]


def load_corpus(bsip1_dir: pathlib.Path) -> list:
    records = []
    if not bsip1_dir.exists():
        print(f"  WARNING: dir not found: {bsip1_dir}")
        return records
    for p in sorted(bsip1_dir.glob("bsip1_*.json")):
        try:
            records.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"  WARNING: load error {p.name}: {e}")
    return records


def anchor_fires(name: str, term: str, exclusions: list) -> bool:
    """Return True if the anchor would fire on this name (after applying exclusions)."""
    if term not in name:
        return False
    # Apply exclusions
    if any(excl in name for excl in exclusions):
        return False
    return True


def main():
    print("=" * 70)
    print("P75b BLEED SIMULATION — biscuit anchors vs ALL live corpora")
    print("HARD GATE: must be 0 hits across all anchors x all corpora")
    print("=" * 70)
    print()

    total_hits = 0
    hit_detail = []
    corpus_stats = []

    for corpus_label, bsip1_dir in LIVE_CORPORA:
        records = load_corpus(bsip1_dir)
        n = len(records)
        corpus_hits = []

        for doc in records:
            name = (doc.get("canonical_name_he") or "").lower()
            barcode = doc.get("barcode", "?")
            for term, exclusions in BISCUIT_ANCHORS:
                if anchor_fires(name, term, exclusions):
                    corpus_hits.append({
                        "corpus": corpus_label,
                        "barcode": barcode,
                        "name": doc.get("canonical_name_he", "?"),
                        "matched_term": term,
                    })

        corpus_stats.append((corpus_label, n, len(corpus_hits)))
        total_hits += len(corpus_hits)
        hit_detail.extend(corpus_hits)

        status = "PASS" if len(corpus_hits) == 0 else f"FAIL ({len(corpus_hits)} hits)"
        print(f"  {corpus_label:<20s} {n:>4d} products   {status}")
        if corpus_hits:
            for h in corpus_hits:
                print(f"    HIT: [{h['matched_term']}] barcode={h['barcode']}  name={h['name']}")

    print()
    print("=" * 70)
    gate = "PASS" if total_hits == 0 else "FAIL"
    print(f"BLEED SIMULATION GATE: {gate} ({total_hits} total hits across all corpora)")
    print("=" * 70)

    if total_hits > 0:
        print()
        print("CRITICAL: Bleed detected. STOP — do NOT proceed to re-score.")
        print("Hits detail:")
        for h in hit_detail:
            print(f"  corpus={h['corpus']}  term={h['matched_term']}  barcode={h['barcode']}  name={h['name']}")

    # Machine-readable summary
    summary = {
        "gate": gate,
        "total_hits": total_hits,
        "corpora_checked": len(LIVE_CORPORA),
        "biscuit_anchors_checked": len(BISCUIT_ANCHORS),
        "corpus_stats": [{"corpus": c, "products": n, "hits": h} for c, n, h in corpus_stats],
        "hits": hit_detail,
    }
    out_path = ROOT / "02_products" / "cookies_coffee" / "bsip2_outputs" / "p75b_bleed_sim_report.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nBleed sim report: {out_path}")

    return total_hits


if __name__ == "__main__":
    hits = main()
    sys.exit(0 if hits == 0 else 1)
