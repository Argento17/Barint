#!/usr/bin/env python3
"""
onboard_category.py — guided hard-gate for finishing a new-category full cycle.

The owner's rule: "I don't want to say 'let's go full scrape', get a live page, then
realize days later it doesn't conform to the spine." This tool is the END-OF-CYCLE
gate that makes that impossible: it runs the real spine-conformance contract
(conformance.py) for one category and REFUSES to declare it done unless every HARD
check passes — and for each failure it prints the EXACT remediation.

It deliberately does NOT auto-edit scoring governance (shadow_registry flags, config
baselines): the registry's per-category engine `flags` decide how the category is
SCORED, and guessing them would silently produce wrong scores. Same philosophy as the
scaffolder not fabricating Hebrew copy — the gate tells you precisely what to add and
where; a human/owner confirms the scoring-governance values.

Where a new category sits in the full cycle:
    scrape -> BSIP0/1/2 -> config (configs/<stem>.json) -> register corpus
    (shadow_registry_v1.json) -> rescore -> scaffold_category.py (frontend) ->
    author copy -> build -> [ onboard_category.py --slug X ]  <-- the gate
The gate is the last step; if it is not green, the category is NOT live-ready.

Usage:
  python 03_operations/page_generator/onboard_category.py --slug cakes
  python 03_operations/page_generator/onboard_category.py --slug breakfast-cereals

Exit code: 0 = conforms, live-ready (subject to copy/build, which it reminds about).
           1 = HARD conformance failure (NOT live-ready) — remediation printed.
           3 = no config for slug (earlier in the cycle than this gate).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from conformance import (  # noqa: E402
    evaluate, load_configs, load_manifest_entries, load_registry,
    manifest_for_category, norm, real_stem_to_corpora, resolve_stem,
)


def remediation(stem: str, cfg: dict, result: dict, entries: list[dict]) -> list[str]:
    """Map each HARD failure id to a concrete, copy-pasteable fix."""
    lines: list[str] = []
    fails = set(result["hard_failures"])
    cat_norm = norm(cfg.get("category"))

    if "HARD-1-corpus_dirs" in fails:
        lines.append(
            "  [HARD-1] Config corpus dirs missing. Fix corpus_dirs / run_products_dir in\n"
            f"           configs/{stem}.json to point at the BSIP1/BSIP2 output dirs that exist."
        )
    if "HARD-2-flip_reachable" in fails:
        # derive a candidate source dir from the config for the registry template
        src = ""
        for key in ("run_products_dir", "corpus_dirs"):
            val = cfg.get(key)
            cand = (val[0] if isinstance(val, list) and val else val) or ""
            if cand:
                src = str(cand)
                break
        lines.append(
            "  [HARD-2] No registered corpus maps to this shelf -> a score-flip will SKIP it.\n"
            "           Add a corpus entry to 03_operations/shadow/shadow_registry_v1.json\n"
            "           (set `flags` to THIS category's batch-runner engine flags — do NOT guess):\n"
            "             {\n"
            f'               "name": "{stem}",\n'
            "               \"class\": \"candidate\",            // candidate|published|frozen (owner call)\n"
            f'               "source": "{src or "<BSIP1 output dir>"}",\n'
            "               \"flags\": { /* TODO: copy from batch_run_" + stem + ".py */ },\n"
            "               \"invariants\": [],\n"
            f'               "note": "Registered for spine re-flow ({stem})."\n'
            "             }\n"
            "           Then re-run this gate."
        )
    if "HARD-3-baseline_served" in fails:
        served = [Path(e.get("path", "")).name
                  for e in manifest_for_category(cat_norm, entries)]
        lines.append(
            "  [HARD-3] config.baseline_json must equal the frontend JSON the live route serves\n"
            f"           (live_manifest serves for '{cfg.get('category')}': {served or 'NOTHING'}).\n"
            f"           Set \"baseline_json\" in configs/{stem}.json to that file's absolute path,\n"
            "           so copy_stage writes the flip's new scores to the page the site reads."
        )
    if "HARD-7-off_zero" in fails:
        lines.append(
            "  [HARD-7] OFF (Open Food Facts) data found in SERVED products — project-wide ban,\n"
            "           launch blocker. Remove the OFF-sourced product(s) from the frontend JSON\n"
            "           (exclude in config) and regenerate. Unknown is acceptable; OFF is not."
        )
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(
        description="End-of-cycle spine-conformance gate for one category."
    )
    parser.add_argument("--slug", required=True,
                        help="route slug, category name, or config stem")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]

    configs = load_configs()
    stem = resolve_stem(args.slug, configs)
    if stem is None:
        print(f"NOT LIVE-READY: no config for '{args.slug}'.")
        print("  This gate runs at the END of the cycle. First scrape -> score -> create")
        print(f"  configs/<stem>.json (then register corpus, scaffold, author copy).")
        print(f"  Known config stems: {', '.join(sorted(configs))}")
        return 3

    entries = load_manifest_entries()
    registry = load_registry()
    stem_corpora = real_stem_to_corpora()
    result = evaluate(stem, configs[stem], entries=entries, registry=registry,
                      stem_corpora=stem_corpora)

    print(f"=== onboard gate: {stem} (category: {result['category']}) ===")
    for c in result["checks"]:
        mark = "PASS" if c["ok"] else ("FAIL" if c["hard"] else "warn")
        print(f"  {mark:4s} {c['id']:24s} {c['detail']}")

    if result["conforms"]:
        print("\nCONFORMS: this category will re-flow correctly on a score-flip.")
        print("Before calling it LIVE-READY, confirm the non-scoring steps:")
        print("  - frontend scaffolded (route + registry + union + sitemap) — scaffold_category.py")
        print("  - Hebrew copy authored (no PENDING_COPY) — Content Agent")
        print("  - npm run build is green")
        print("  - red-team gate clean (Stage 9)")
        if result["soft_warnings"]:
            print(f"  NOTE soft warnings: {', '.join(result['soft_warnings'])}")
        return 0

    print("\nNOT LIVE-READY: this category would go STALE on the next score-flip.")
    print("Fix each HARD failure, then re-run this gate:\n")
    for line in remediation(stem, configs[stem], result, entries):
        print(line)
    return 1


if __name__ == "__main__":
    sys.exit(main())
