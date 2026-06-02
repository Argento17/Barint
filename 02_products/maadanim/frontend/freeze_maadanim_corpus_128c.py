#!/usr/bin/env python3
"""
TASK-128C — Maadanim displayed-corpus finalization + freeze (v2 activation gate).

Per maadanim_confidence_audit_128c.md:
  - P0 #1 (confidence-prose blocker): CLEARED — 0 genuine relabels. No hardening needed.
  - P0 #3 / §2.2: 3 category-instability survivors are mis-routed DRINKS, not maadanim.
    Action = EXCLUDE from the displayed shelf (re-route target = beverages, not live).
  - §2.1: formalize a written `excluded_products` list (re-run safety); items already
    absent from the displayed 90.

HARD CONSTRAINTS:
  - NO score / grade changes (CLAUDE.md invariant; run_maadanim_001 frozen). Asserted.
  - Removal only changes shelf MEMBERSHIP; surviving rows are byte-identical.
  - Idempotent: re-running after exclusion is a no-op.

Writes both:
  - deployed  : C:\\bari\\bari-web\\src\\data\\comparisons\\maadanim_frontend_v2.json
  - workspace : C:\\bari\\02_products\\maadanim\\maadanim_frontend_v2.json
"""
import json, os, io, sys, collections, datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

WEB = r"C:\bari\bari-web\src\data\comparisons\maadanim_frontend_v2.json"
WS  = r"C:\bari\02_products\maadanim\maadanim_frontend_v2.json"

# §2.2 instability survivors — EXCLUDE (mis-routed drinks; cat_conf<=0.55, instability=true)
EXCLUDE_DISPLAYED = {
    "bsip1_maadanim_4584306":       "סופר גמדים תות בננה מארז (squeezable kids' drink, route=default, cat_conf 0.30)",
    "bsip1_maadanim_7290010472307": "גמדים לשתיה תות בננה (drinkable, route=default, cat_conf 0.30)",
    "bsip1_maadanim_7290119375356": "דנונה מולטי קולגן (collagen drink, route=dessert, cat_conf 0.55)",
}

# §2.1 written exclusion list (re-run safety; already absent from displayed 90).
# Name-keyed because these never reached the curated frontend (no stable display id).
EXCLUDE_CORPUS_NONMAADANIM = [
    "שריר הזרוע (8) בעדני",      # arm-muscle meat
    "המבורגר ילדים",              # hamburger
    "חסה מעודנת הידרופונית",      # lettuce
    "גבינת בולגרית 5% גד ארוז",  # brined cheese
    "בולגרית מעודנת 24%",         # brined cheese
    "ביו LR 25 בד\"ץ", "ביו 25", "מיקס לילד",
]
EXCLUDE_CORPUS_SUPPLEMENTS = [
    "ביו בליס פרוביוטיקה", "מגה פרוביוטיק 500", "פרוביוטיק SHAPE",
    "ביוגאיה טיפות", "יומי פרוביוטיק", "ביו 25 פרוביוטיקה",
]


def main():
    doc = json.load(open(WEB, encoding="utf-8"))
    prods = doc["products"]

    before_n = len(prods)
    before_dist = collections.Counter(p.get("confidence") for p in prods)
    before_scores = {p["id"]: (p.get("score"), p.get("grade")) for p in prods}

    removed = [(p["id"], p.get("name"), p.get("score"), p.get("grade"))
               for p in prods if p["id"] in EXCLUDE_DISPLAYED]
    kept = [p for p in prods if p["id"] not in EXCLUDE_DISPLAYED]

    # HARD GUARANTEE: every surviving row keeps its exact score/grade.
    after_scores = {p["id"]: (p.get("score"), p.get("grade")) for p in kept}
    for pid, sg in after_scores.items():
        assert before_scores[pid] == sg, f"SCORE MOVED on {pid} — aborting"

    doc["products"] = kept
    doc["_meta"]["product_count"] = len(kept)
    doc["_meta"]["scored_count"] = len(kept)
    doc["_meta"]["confidence_distribution"] = dict(collections.Counter(p["confidence"] for p in kept))
    doc["_meta"]["excluded_products"] = {
        "task": "TASK-128C",
        "source_audit": "maadanim_confidence_audit_128c.md (re-audit §2.1 + §2.2)",
        "frozen": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "displayed_excluded_instability_survivors": EXCLUDE_DISPLAYED,
        "corpus_excluded_non_maadanim": EXCLUDE_CORPUS_NONMAADANIM,
        "corpus_excluded_supplements": EXCLUDE_CORPUS_SUPPLEMENTS,
        "score_changes": 0,
        "note": "Removal changes shelf membership only; surviving rows byte-identical. "
                "run_maadanim_001 scores frozen. P0 #1 confidence-prose blocker was inflated "
                "(0 genuine relabels) — see audit report.",
    }

    for path in (WEB, WS):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)

    print("TASK-128C — maadanim corpus finalization + freeze")
    print(f"  displayed: {before_n} -> {len(kept)}")
    print(f"  before conf: {dict(before_dist)}")
    print(f"  after  conf: {doc['_meta']['confidence_distribution']}")
    print(f"  excluded (instability survivors): {len(removed)}")
    for pid, name, score, grade in removed:
        print(f"    [{pid}] {name} | {score}/{grade}")
    print(f"  formal excluded_products list written: "
          f"{len(EXCLUDE_DISPLAYED)} displayed + "
          f"{len(EXCLUDE_CORPUS_NONMAADANIM)} non-maadanim + "
          f"{len(EXCLUDE_CORPUS_SUPPLEMENTS)} supplements")
    print("  score/grade changes: 0 (asserted on every surviving row)")


if __name__ == "__main__":
    main()
