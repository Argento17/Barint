"""TASK-276 — Generate _corpus_report_full.md from _corpus_run_full.json.

Run after run_full.py. Reads the run output and produces a markdown report
with yield %, per-method + per-brand + per-active breakdown, grade distribution,
scored product table, and unscoreable residue table.
"""
import sys, json, pathlib, datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = pathlib.Path(__file__).resolve().parent
RUN_PATH = HERE / "_corpus_run_full.json"
REPORT_PATH = HERE / "_corpus_report_full.md"

run = json.loads(RUN_PATH.read_text(encoding='utf-8'))
counts = run['counts']
grades = run['grade_distribution']
scored_n = counts['scored']
total = counts['attempted']
premarket_n = counts.get('unscoreable_premarket', 0)
incomplete_n = counts.get('unscoreable_incomplete', 0)

lines = []
lines.append("# TASK-276 Full Addressable Shelf Run — Corpus Report")
lines.append(f"\n**Generated:** {run['generated_at']}")
lines.append(f"**EDPG:** {run['edpg_note']}")
lines.append(f"\n---\n")

lines.append("## Run Summary\n")
lines.append(f"| Metric | Value |")
lines.append(f"|---|---|")
lines.append(f"| Shelf size (addressable) | {total} SKUs |")
lines.append(f"| Scored | {scored_n} |")
lines.append(f"| Scoreable yield | {run['scoreable_yield_pct']}% |")
lines.append(f"| Unscoreable (pre-marked: out-of-ontology, no-panel) | {premarket_n} |")
lines.append(f"| Unscoreable (incomplete dose from panel) | {incomplete_n} |")
lines.append(f"| Engine errors | {counts.get('engine_error', 0)} |")
lines.append("")

lines.append("## Grade Distribution (Scored = {})".format(scored_n))
lines.append("")
lines.append("| Grade | N | % of Scored |")
lines.append("|---|---|---|")
for g in ['S', 'B', 'C', 'D', 'E']:
    n = grades.get(g, 0)
    pct = round(100*n/max(1, scored_n), 1)
    lines.append(f"| {g} | {n} | {pct}% |")
lines.append("")

lines.append("## Per-Acquisition Method")
lines.append("")
lines.append("| Method | Scored SKUs |")
lines.append("|---|---|")
for m, n in sorted(run['per_acquisition_method'].items()):
    lines.append(f"| {m} | {n} |")
lines.append("")

lines.append("## Per-Brand Bucket (Scored)")
lines.append("")
lines.append("| Brand | Scored SKUs |")
lines.append("|---|---|")
for b, n in sorted(run['per_brand_bucket'].items(), key=lambda x: -x[1]):
    lines.append(f"| {b} | {n} |")
lines.append("")

lines.append("## Per-Active Slug (Scored)")
lines.append("")
lines.append("| Active | Scored SKUs |")
lines.append("|---|---|")
for a, n in sorted(run['per_active_slug'].items(), key=lambda x: -x[1]):
    lines.append(f"| {a} | {n} |")
lines.append("")

lines.append("## Scored Product Table (sorted by score DESC)")
lines.append("")
lines.append("| Barcode | Grade | Score | Active | Method | Binding Constraint | Name (Hebrew) |")
lines.append("|---|---|---|---|---|---|---|")
scored_results = [r for r in run['results'] if r['outcome'] == 'scored']
scored_results.sort(key=lambda r: r['engine_output']['score'], reverse=True)
for r in scored_results:
    e = r['engine_output']
    bc_str = r['barcode']
    name = r['name_he'][:40]
    method = r.get('acquisition_method', '?')
    bind = e['binding_constraint'].get('mechanism', '?')
    lines.append(f"| {bc_str} | {e['grade']} | {e['score']} | {r['engine_active']} | {method} | {bind} | {name} |")
lines.append("")

lines.append("## Unscoreable Residue")
lines.append("")
lines.append("### Pre-marked (out-of-ontology / no panel found)")
lines.append("")
lines.append("| Barcode | Active | Reason | Name (Hebrew) |")
lines.append("|---|---|---|---|")
for r in run['results']:
    if r['outcome'] == 'unscoreable_premarket':
        # look up unscoreable reason from cache
        bc = r['barcode']
        cache_fp = HERE / "cache" / f"{bc}.json"
        reason = "see cache"
        if cache_fp.exists():
            try:
                obj = json.loads(cache_fp.read_text(encoding='utf-8'))
                reason = obj.get('unscoreable_reason', 'see cache')[:80]
            except Exception:
                pass
        lines.append(f"| {bc} | {r['engine_active']} | {reason} | {r['name_he'][:45]} |")
lines.append("")

lines.append("### Incomplete (panel found; dose null or unmappable)")
lines.append("")
lines.append("| Barcode | Active | Brand | Missing | Name (Hebrew) |")
lines.append("|---|---|---|---|---|")
for r in run['results']:
    if r['outcome'] == 'unscoreable_incomplete':
        lossy = ", ".join(r.get('lossy', []))[:80]
        lines.append(f"| {r['barcode']} | {r['engine_active']} | {r['brand_bucket']} | {lossy} | {r['name_he'][:40]} |")
lines.append("")

lines.append("---")
lines.append(f"\n*Report generated {datetime.datetime.utcnow().isoformat()}Z by generate_report.py (TASK-276)*")

REPORT_PATH.write_text("\n".join(lines), encoding='utf-8')
print(f"Report written: {REPORT_PATH}")
print(f"  Lines: {len(lines)}")
