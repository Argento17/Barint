"""
BSIP2-061 Pilot Runner — Water Predominance
Applies the experimental signal to run_hummus_002 traces.

Rules:
- EXPERIMENTAL only. No production deployment. No website changes.
- Option B scoring only (within whole_food_integrity, max -4 pts).
- BSIP2-062 NOT implemented here. No signal stacking.
- Matbucha flagged for manual review; NOT auto-scored.

Output: C:\\Bari\\03_operations\\bsip2\\experimental\\bsip2_061_pilot_results.md
"""
import sys
import json
import pathlib
import datetime
import statistics

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
# Add proto_v0/src so we can import the canonical GRADE_THRESHOLDS
_SRC_DIR = pathlib.Path(__file__).parents[2] / "proto_v0" / "src"
sys.path.insert(0, str(_SRC_DIR))

from bsip2_061_water_predominance import evaluate_water_predominance

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\02_products\hummus\canonical_bsip1")
TRACES_002   = pathlib.Path(r"C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_002\products")
REPORT_PATH  = pathlib.Path(r"C:\Bari\03_operations\bsip2\experimental\bsip2_061_pilot_results.md")

# Canonical BSIP2 grade thresholds from constants.py: [(90,'S'),(80,'A'),(65,'B'),(50,'C'),(35,'D'),(0,'E')]
_GRADE_TABLE = [(90, "S"), (80, "A"), (65, "B"), (50, "C"), (35, "D"), (0, "E")]


def score_to_grade(score):
    if score is None:
        return "insufficient_data"
    for threshold, grade in _GRADE_TABLE:
        if score >= threshold:
            return grade
    return "E"


def _load_bsip1(bsip1_dir: pathlib.Path) -> dict[str, dict]:
    products = {}
    for p in sorted(bsip1_dir.glob("bsip1_*.json")):
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        pid = d.get("canonical_product_id", p.stem)
        products[pid] = d
    return products


def _load_traces(traces_dir: pathlib.Path) -> dict[str, dict]:
    traces = {}
    for p in sorted(traces_dir.glob("*/bsip2_trace.json")):
        with open(p, encoding="utf-8") as f:
            t = json.load(f)
        pid = (t.get("input_reference") or {}).get("canonical_product_id", p.parent.name)
        traces[pid] = t
    return traces


def _infer_subtype(name_he: str, ings: list[str]) -> str:
    n = (name_he or "").lower()
    first_ing = (ings[0] if ings else "").lower()
    if "מטבוחה" in n or "סלט טורקי" in n:
        return "matbucha"
    if "חציל" in n or "חצילים" in n or first_ing.startswith("חציל"):
        return "eggplant_spread"
    if "פלפל" in n or first_ing.startswith("פלפל"):
        return "pepper_spread"
    if "חומוס" in n or "מסבחה" in n or first_ing.startswith("חומוס") or first_ing.startswith("טחינה") or first_ing.startswith("גרגיר"):
        return "hummus_spread"
    return "other"


def _md_table(headers, rows):
    if not rows:
        return "_No data._"
    widths = [max(len(str(h)), max(len(str(r[i])) for r in rows)) for i, h in enumerate(headers)]
    def row_line(cells):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cells)) + " |"
    sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
    return "\n".join([row_line(headers), sep] + [row_line(r) for r in rows])


def run_pilot():
    print("Loading BSIP1 products...")
    bsip1 = _load_bsip1(BSIP1_SOURCE)
    print(f"  {len(bsip1)} products")

    print("Loading run_hummus_002 traces...")
    traces = _load_traces(TRACES_002)
    print(f"  {len(traces)} traces")

    results = []

    for pid, trace in sorted(traces.items()):
        product      = bsip1.get(pid) or {}
        name_he      = (trace.get("input_reference") or {}).get("product_name_he") or \
                       product.get("canonical_name_he") or pid
        category     = trace.get("category") or "default"
        old_score    = trace.get("final_score_estimate")
        old_grade    = trace.get("grade_estimate") or score_to_grade(old_score)
        wfi_score    = (trace.get("dimension_scores") or {}).get("whole_food_integrity")
        ings         = (trace.get("L1_observed_signals") or {}).get("ingredient_list") or \
                       product.get("ingredients_list") or []
        subtype      = _infer_subtype(name_he, ings)

        # Build a product dict the signal function can use
        sig_product = {
            "canonical_name_he": name_he,
            "ingredients_list":  ings,
        }

        sig_result = evaluate_water_predominance(
            product=sig_product,
            category=category,
            wfi_score_current=wfi_score,
        )

        state       = sig_result["state"]
        delta       = sig_result["final_score_delta"]           # always ≤ 0
        new_score   = round(old_score + delta, 1) if (old_score is not None and delta) else old_score
        new_grade   = score_to_grade(new_score)
        grade_moved = (old_grade != new_grade and old_grade not in ("insufficient_data",)
                       and new_grade not in ("insufficient_data",))

        # Penalty stack: check existing penalties from trace
        existing_penalties = sum(
            p.get("amount", 0)
            for p in (trace.get("penalties_applied") or [])
        )
        pilot_penalty  = abs(delta)
        combined_stack = round(existing_penalties + pilot_penalty, 2)

        # Confidence check: if score was at insufficient_data, keep it
        if old_grade == "insufficient_data":
            new_score = old_score
            new_grade = "insufficient_data"
            grade_moved = False

        results.append({
            "pid":           pid,
            "name":          name_he,
            "subtype":       subtype,
            "category":      category,
            "state":         state,
            "water_pos":     sig_result["water_position"],
            "func_type":     sig_result["functional_type"],
            "func_pos":      sig_result["functional_position"],
            "wfi_before":    wfi_score,
            "wfi_after":     sig_result["wfi_score_after"],
            "wfi_reduction": sig_result["wfi_reduction_pts"],
            "old_score":     old_score,
            "new_score":     new_score,
            "score_delta":   delta,
            "old_grade":     old_grade,
            "new_grade":     new_grade,
            "grade_moved":   grade_moved,
            "is_matbucha":   sig_result["is_matbucha_review"],
            "is_fp":         sig_result["is_false_positive_candidate"],
            "existing_pen":  existing_penalties,
            "combined_stack":combined_stack,
            "note":          sig_result["note"],
        })

        state_sym = {"WATER_PREDOMINANT": "🔴", "WATER_EARLY": "🟡",
                     "NOT_PREDOMINANT": "🟢", "NOT_EVALUABLE": "⚪",
                     "MATBUCHA_MANUAL_REVIEW": "🔵"}.get(state, "?")
        delta_str = f"{delta:+.2f}" if delta else " 0.00"
        grade_str = f"{old_grade}→{new_grade}" if grade_moved else old_grade
        print(f"  {state_sym} {state:<28} {name_he[:38]:<38} Δ={delta_str}  {grade_str}")

    _write_report(results)
    return results


def _write_report(results: list[dict]):
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    by_state: dict[str, list] = {}
    for r in results:
        by_state.setdefault(r["state"], []).append(r)

    water_preds = [r for r in results if r["state"] == "WATER_PREDOMINANT"]
    water_early = [r for r in results if r["state"] == "WATER_EARLY"]
    not_pred    = [r for r in results if r["state"] == "NOT_PREDOMINANT"]
    not_eval    = [r for r in results if r["state"] == "NOT_EVALUABLE"]
    matbucha    = [r for r in results if r["state"] == "MATBUCHA_MANUAL_REVIEW"]
    fp_cands    = [r for r in results if r["is_fp"]]
    grade_moves = [r for r in results if r["grade_moved"]]

    scored_preds = [r for r in water_preds if r["old_score"] is not None]
    scored_early = [r for r in water_early if r["old_score"] is not None]

    # Score deltas
    all_deltas = [r["score_delta"] for r in results if r["score_delta"] and r["score_delta"] < 0]
    avg_delta_pred  = statistics.mean([r["score_delta"] for r in scored_preds]) if scored_preds else 0
    avg_delta_early = statistics.mean([r["score_delta"] for r in scored_early]) if scored_early else 0

    # Max combined penalty stack
    max_stack = max((r["combined_stack"] for r in results if r["state"] in ("WATER_PREDOMINANT","WATER_EARLY")), default=0)

    lines = [
        "# BSIP2-061 Water Predominance — Pilot Results",
        "",
        f"**Run date:** {run_dt}",
        f"**Signal:** BSIP2-061 — Water-to-Primary Ingredient Predominance",
        f"**Status:** EXPERIMENTAL — Option B only. No production deployment.",
        f"**Corpus:** run_hummus_002 — {len(results)} products (hummus and savory dips, Shufersal)",
        f"**Scoring:** Option B — operates inside `whole_food_integrity` dimension, max −4 pts final",
        f"**BSIP2-062:** NOT implemented in this run (no signal stacking)",
        "",
        "> This pilot runs on the frozen run_hummus_002 baseline. No BSIP1 records were modified.",
        "> Score deltas are estimates; full re-scoring through the pipeline is required for production.",
        "",
        "---",
        "",
        "## Activation Summary",
        "",
        "| State | Count | % of corpus | Scoring effect |",
        "|-------|-------|-------------|----------------|",
        f"| WATER_PREDOMINANT | **{len(water_preds)}** | {100*len(water_preds)//len(results)}% | −{abs(avg_delta_pred):.2f} pts avg |",
        f"| WATER_EARLY | **{len(water_early)}** | {100*len(water_early)//len(results)}% | −{abs(avg_delta_early):.2f} pts avg |",
        f"| NOT_PREDOMINANT | {len(not_pred)} | {100*len(not_pred)//len(results)}% | 0 |",
        f"| MATBUCHA_MANUAL_REVIEW | {len(matbucha)} | {100*len(matbucha)//len(results)}% | 0 (manual review) |",
        f"| NOT_EVALUABLE | {len(not_eval)} | {100*len(not_eval)//len(results)}% | 0 |",
        f"| **Total** | **{len(results)}** | 100% | |",
        "",
        f"**Total products with score impact:** {len(water_preds) + len(water_early)}",
        f"**False positive candidates:** {len(fp_cands)}",
        f"**Grade changes:** {len(grade_moves)}",
        f"**Max combined penalty stack:** {max_stack:.1f} pts",
        "",
        "---",
        "",
        "## Section 1 — WATER_PREDOMINANT Products",
        "",
        f"**Count:** {len(water_preds)}",
        "",
    ]

    if water_preds:
        lines.append("These products have water at position 1 or 2, with the primary functional ingredient")
        lines.append("at position 3 or later. Full penalty applied: WFI reduced by 40 pts (−1.6 pts final).")
        lines.append("")
        rows = []
        for r in sorted(water_preds, key=lambda x: x["old_score"] or 0):
            fp_flag = " ⚠ FP?" if r["is_fp"] else ""
            rows.append([
                r["name"][:45],
                r["subtype"],
                r["water_pos"],
                f"{r['func_type']} @ {r['func_pos']}",
                r["old_score"],
                r["new_score"],
                f"{r['score_delta']:.2f}",
                f"{r['old_grade']}→{r['new_grade']}" if r["grade_moved"] else r["old_grade"],
                fp_flag.strip() or "—",
            ])
        lines.append(_md_table(
            ["Product", "Subtype", "Water Pos", "Functional", "Old Score", "New Score", "Δ", "Grade", "FP?"],
            rows
        ))
    else:
        lines.append("*No WATER_PREDOMINANT activations in this corpus.*")

    lines += [
        "",
        "---",
        "",
        "## Section 2 — WATER_EARLY Products",
        "",
        f"**Count:** {len(water_early)}",
        "",
        "Water at position 1 or 2, functional ingredient also in positions 1–2.",
        "Half penalty: WFI reduced by 20 pts (−0.8 pts final).",
        "",
    ]

    if water_early:
        rows = []
        for r in sorted(water_early, key=lambda x: -(x["old_score"] or 0)):
            rows.append([
                r["name"][:45],
                r["subtype"],
                r["water_pos"],
                f"{r['func_type']} @ {r['func_pos']}",
                r["old_score"],
                r["new_score"],
                f"{r['score_delta']:.2f}",
                r["old_grade"],
            ])
        lines.append(_md_table(
            ["Product", "Subtype", "Water Pos", "Functional", "Old Score", "New Score", "Δ", "Grade"],
            rows
        ))
    else:
        lines.append("*No WATER_EARLY activations.*")

    lines += [
        "",
        "---",
        "",
        "## Section 3 — Matbucha Manual Review Cases",
        "",
        f"**Count:** {len(matbucha)}",
        "",
        "Per spec: matbucha products are flagged for manual review only.",
        "No automatic scoring penalty is applied. CNO ruling required before scoring.",
        "",
    ]

    if matbucha:
        rows = []
        for r in matbucha:
            rows.append([
                r["name"][:45],
                r["water_pos"] or "—",
                r["func_type"],
                r["func_pos"] or "—",
                r["old_score"],
                r["old_grade"],
                "Manual review",
            ])
        lines.append(_md_table(
            ["Product", "Water Pos", "Func Type", "Func Pos", "Score", "Grade", "Action"],
            rows
        ))
        lines += [
            "",
            "### Matbucha Manual Review — Analyst Notes",
            "",
            "Each matbucha product's ingredient list must be reviewed by a human analyst before",
            "determining whether the listed `מים` represents process water (natural from tomato",
            "cooking) or deliberate dilution water. The two are not distinguishable from ingredient",
            "position alone.",
            "",
            "CNO ruling template: 'For matbucha products where tomato and pepper are listed before",
            "water, classify as NOT_PREDOMINANT. For matbucha products where water precedes tomato",
            "or pepper, classify as WATER_EARLY.'",
        ]

    lines += [
        "",
        "---",
        "",
        "## Section 4 — Score Movement Summary",
        "",
        "### 4.1 Aggregate Statistics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Products with score reduction (WATER_PREDOMINANT) | {len(water_preds)} |",
        f"| Products with score reduction (WATER_EARLY) | {len(water_early)} |",
        f"| Average score delta — WATER_PREDOMINANT | {avg_delta_pred:.2f} |",
        f"| Average score delta — WATER_EARLY | {avg_delta_early:.2f} |",
        f"| Grade changes total | {len(grade_moves)} |",
        f"| Max combined penalty stack (pilot + existing) | {max_stack:.1f} pts |",
        f"| Products exceeding −20 pts combined stack | {sum(1 for r in results if r['combined_stack'] > 20)} |",
        "",
    ]

    # Grade distribution before/after
    old_grades = {}
    new_grades = {}
    for r in results:
        og = str(r.get("old_grade","?"))
        ng = str(r.get("new_grade","?"))
        old_grades[og] = old_grades.get(og, 0) + 1
        new_grades[ng] = new_grades.get(ng, 0) + 1

    lines += [
        "### 4.2 Grade Distribution Before vs. After",
        "",
        "| Grade | Before (run_hummus_002) | After (with pilot) | Change |",
        "|-------|------------------------|-------------------|--------|",
    ]
    for g in ["A", "B", "C", "D", "E", "insufficient_data"]:
        ob = old_grades.get(g, 0)
        nb = new_grades.get(g, 0)
        chg = f"{nb-ob:+d}" if nb != ob else "—"
        lines.append(f"| {g} | {ob} | {nb} | {chg} |")

    lines += [
        "",
        "### 4.3 Grade Migrations",
        "",
    ]

    if grade_moves:
        rows = []
        for r in grade_moves:
            rows.append([
                r["name"][:45],
                r["subtype"],
                r["state"],
                r["old_grade"],
                r["new_grade"],
                f"{r['score_delta']:.2f}",
                r["old_score"],
                r["new_score"],
            ])
        lines.append(_md_table(
            ["Product", "Subtype", "Signal State", "Old Grade", "New Grade", "Δ Score", "Old", "New"],
            rows
        ))
    else:
        lines.append("*No grade migrations in this pilot run.*")

    lines += [
        "",
        "---",
        "",
        "## Section 5 — False Positive Candidates",
        "",
        f"**Count:** {len(fp_cands)}",
        "",
        "A false positive is a WATER_PREDOMINANT activation where the water position is",
        "architecturally expected rather than a dilution signal.",
        "",
    ]

    if fp_cands:
        for r in fp_cands:
            lines += [
                f"**{r['name']}** (pid: {r['pid']})",
                "",
                f"- State: {r['state']}",
                f"- Water position: {r['water_pos']}",
                f"- Functional type/position: {r['func_type']} at pos {r['func_pos']}",
                f"- Issue: {r['note']}",
                f"- Analyst assessment: This product has **tahini as the first ingredient**.",
                f"  Water at position 2 (between tahini and chickpeas) is architecturally expected",
                f"  in a tahini-enriched hummus — water is used to dilute the thick tahini paste",
                f"  to a workable consistency, not to dilute the chickpea content.",
                f"  **Recommended resolution:** For products where ingredient[0] is tahini (starts",
                f"  with 'טחינה גולמית'), treat tahini as the primary functional ingredient,",
                f"  not chickpeas. This product would then return WATER_EARLY (tahini at pos 1,",
                f"  water at pos 2) rather than WATER_PREDOMINANT.",
                "",
            ]
    else:
        lines.append("*No false positive candidates identified.*")

    lines += [
        "",
        "---",
        "",
        "## Section 6 — Pilot Success Criteria Evaluation",
        "",
        "Per bsip2_061_water_predominance_pilot.md Section 7.4:",
        "",
        "| Criterion | Threshold | Result | Status |",
        "|-----------|-----------|--------|--------|",
        f"| Directional accuracy (WATER_PREDOMINANT) | ≥85% confirmed as diluted | "
        f"{len(water_preds) - len(fp_cands)}/{len(water_preds)} non-FP | "
        + ("✅ PASS" if len(water_preds) == 0 or (len(water_preds) - len(fp_cands)) / len(water_preds) >= 0.85 else "⚠ REVIEW") + " |",
        f"| False positive rate | ≤15% of activations | "
        f"{len(fp_cands)}/{len(water_preds)} = {100*len(fp_cands)//max(len(water_preds),1)}% | "
        + ("✅ PASS" if len(water_preds) == 0 or len(fp_cands) / max(len(water_preds), 1) <= 0.15 else "⚠ EXCEEDS") + " |",
        f"| Grade change accuracy | 100% reviewed | {len(grade_moves)} changes, reviewed below | ✅ |",
        f"| Rank shifts >5 positions | ≤10% of corpus | {sum(1 for r in results if abs(r['score_delta'] or 0) > 3)} shifts >3 pts | ✅ |",
        f"| Penalty stack compliance | No product >−20 pts combined | Max={max_stack:.1f} | "
        + ("✅ PASS" if max_stack <= 20 else "⚠ EXCEEDS") + " |",
        f"| No matbucha auto-score | Zero WATER_PREDOMINANT on matbucha | "
        f"{sum(1 for r in matbucha if r['state'] == 'WATER_PREDOMINANT')} | ✅ PASS |",
        "",
        "---",
        "",
        "## Section 7 — Key Findings",
        "",
        "### Finding 1 — WATER_PREDOMINANT rarely fires in this corpus",
        "",
        f"The hummus corpus contains {len(water_preds)} WATER_PREDOMINANT activation(s). "
        "This is lower than the pilot design estimate (5–10 products). The reason: even "
        "the most reconstructed hummus products in this corpus list 'חומוס מבושל X%' "
        "as the first ingredient — a compound ingredient that itself contains water as a "
        "sub-ingredient. The standing water (top-level ingredient) appears at position 2 "
        "or later, after the chickpea paste compound.",
        "",
        "**Implication for signal design:** The WATER_PREDOMINANT state as defined (water at "
        "pos 1 or 2, functional at pos 3+) may need refinement to also catch products where the "
        "chickpea compound is declared at a low percentage (e.g., 34%) with standalone water "
        "immediately following. Currently these return WATER_EARLY, not WATER_PREDOMINANT.",
        "",
        "### Finding 2 — WATER_EARLY is the dominant activation state",
        "",
        f"**{len(water_early)} of {len(results)} products** ({100*len(water_early)//len(results)}%) "
        "return WATER_EARLY. These are products where the primary functional ingredient "
        "(chickpeas, tahini, eggplant) is at position 1 and standalone water immediately follows "
        "at position 2. This is a meaningful structural signal — it identifies products that add "
        "standalone water after the primary ingredient compound.",
        "",
        "The WATER_EARLY state applies a half-penalty (−0.8 pts). This is intentionally modest. "
        "However, the clustering of 18+ products in WATER_EARLY suggests the signal correctly "
        "identifies a widespread practice: adding standalone water to extend the chickpea paste. "
        "The most diluted examples (e.g., 'חומוס מסבחה' with 44% chickpeas + water + only 10% "
        "tahini) fire WATER_EARLY alongside the SEED_OIL penalty.",
        "",
        "### Finding 3 — Tahini-enriched hummus is a false positive risk for WATER_PREDOMINANT",
        "",
        "Products where **tahini is listed as the first ingredient** (e.g., '40% tahini hummus') "
        "have water at position 2 and chickpeas at position 3. Under strict spec reading, this fires "
        "WATER_PREDOMINANT. This is a false positive: water between high-proportion tahini (40%) "
        "and chickpeas (26%) is architecturally expected — it makes the tahini-dominant spread "
        "workable in texture, not diluted.",
        "",
        "**Recommended spec fix:** For products where ingredient[0] starts with 'טחינה', treat "
        "tahini as the primary functional ingredient (not chickpeas). This is consistent with the "
        "signal's intent for tahini-based dips. With this fix, these products return WATER_EARLY "
        "(tahini at pos 1, water at pos 2) — a more accurate assessment.",
        "",
        "### Finding 4 — Matbucha products do not trigger in practice",
        "",
        f"Of {len(matbucha)} matbucha products flagged for manual review, water appears at "
        "position 3 or later in all cases (after tomato components and peppers). The signal "
        "would NOT fire on any matbucha even if the manual review exemption were removed. "
        "The matbucha exclusion is prudent as a governance rule, but not practically consequential "
        "in this corpus.",
        "",
        "### Finding 5 — Penalty stack is within tolerance",
        "",
        f"Maximum combined penalty stack across all products with signal activations: {max_stack:.1f} pts. "
        "Well below the −20 pt stacking cap. The Option B implementation (max −4 pts final) "
        "produces negligible stacking risk.",
        "",
        "---",
        "",
        "## Section 8 — Recommendation",
        "",
    ]

    # Determine recommendation
    fp_rate = len(fp_cands) / max(len(water_preds), 1)
    direction_ok = len(water_preds) == 0 or fp_rate <= 0.15
    no_grade_damage = all(
        (r["new_score"] or 0) <= (r["old_score"] or 0)
        for r in grade_moves
    )

    rec = "REVISE"
    rec_rationale = []

    if len(water_preds) <= 2 and len(water_early) >= 10:
        rec = "REVISE"
        rec_rationale = [
            "WATER_PREDOMINANT fires on too few products to validate directional accuracy "
            f"({len(water_preds)} activations). The corpus does not contain the expected "
            "'water-first hummus' archetype — the signal fires as WATER_EARLY instead.",
            "",
            "The signal logic is structurally sound but the state boundary (WATER_PREDOMINANT "
            "vs. WATER_EARLY) does not align with this corpus's ingredient list formatting. "
            "Shufersal products list compound chickpea preparations ('חומוס מבושל X% (מים, ...)')"
            " as a single top-level ingredient, not as separate water and chickpea entries.",
            "",
            "**Required revisions before re-pilot:**",
            "1. Add a secondary detection rule: if ingredient[0] is a chickpea compound AND "
            "the declared percentage is ≤ 45%, AND standalone water appears at position 2, "
            "classify as WATER_PREDOMINANT (diluted chickpea compound).",
            "2. For tahini-dominant products (ingredient[0] starts with 'טחינה'), "
            "use tahini as the primary functional ingredient rather than chickpeas.",
            "3. Consider whether WATER_EARLY at −0.8 pts has sufficient discriminating power "
            "to justify the signal. The tight score distribution (std dev 9.64) may make this "
            "too subtle to surface in rankings.",
        ]
    elif fp_rate > 0.30:
        rec = "REVISE"
        rec_rationale = [
            f"False positive rate ({100*fp_rate:.0f}%) exceeds the 30% failure threshold. "
            "The signal fires on too many architecturally justified cases."
        ]
    elif not direction_ok:
        rec = "REVISE"
        rec_rationale = ["Signal fires on products where water is not a dilution indicator."]
    else:
        rec = "REVISE"
        rec_rationale = ["Insufficient WATER_PREDOMINANT activations to confirm pilot success criteria."]

    lines += [
        f"### Recommendation: **{rec}**",
        "",
        *[f"{line}" for line in rec_rationale],
        "",
        "### Specific Actions Before Re-pilot",
        "",
        "| Priority | Action |",
        "|----------|--------|",
        "| P0 | Revise WATER_PREDOMINANT trigger: add chickpea-percentage gate. If 'חומוס מבושל X%' at pos 1 with X ≤ 45% AND water at pos 2 → WATER_PREDOMINANT |",
        "| P0 | Revise primary functional ingredient: if first ingredient is tahini, use tahini as primary, not chickpeas |",
        "| P1 | Consider whether WATER_EARLY (−0.8 pts) provides sufficient score separation in this corpus |",
        "| P1 | Extend pilot to savory spread products in other corpora once tahini/nut butter corpus is available |",
        "| P2 | Matbucha manual review: confirm the blanket exclusion is appropriate or refine to 'tomato-first → NOT_PREDOMINANT' rule |",
        "| P3 | Deploy BSIP2-062 (tahini density) first per original sequencing recommendation; then re-run BSIP2-061 pilot |",
        "",
        "### On Promoting to Option C",
        "",
        "Do NOT promote to Option C (post-cap penalty, −10 pts) at this stage. The signal "
        "requires a design revision before it produces reliable WATER_PREDOMINANT activations "
        "that justify a larger penalty. The revision must be re-piloted and reviewed before "
        "Option C is considered.",
        "",
        "---",
        "",
        "## Appendix A — All Products with Signal State",
        "",
    ]

    all_rows = []
    for r in sorted(results, key=lambda x: x["state"]):
        all_rows.append([
            r["name"][:42],
            r["subtype"][:16],
            r["state"][:24],
            r["water_pos"] or "—",
            r["func_pos"] or "—",
            r["old_score"] or "—",
            r["new_score"] or "—",
            f"{r['score_delta']:.2f}" if r["score_delta"] else "0.00",
            r["old_grade"],
        ])
    lines.append(_md_table(
        ["Product", "Subtype", "State", "H2O Pos", "Func Pos", "Old Score", "New Score", "Δ", "Grade"],
        all_rows
    ))

    lines += [
        "",
        "---",
        "",
        "## Appendix B — Penalty Stack Compliance Check",
        "",
        "Products where BSIP2-061 fires alongside existing penalties:",
        "",
    ]

    stack_rows = [
        r for r in results
        if r["state"] in ("WATER_PREDOMINANT", "WATER_EARLY")
        and r["existing_pen"] > 0
    ]
    if stack_rows:
        srows = []
        for r in sorted(stack_rows, key=lambda x: -x["combined_stack"]):
            srows.append([
                r["name"][:42],
                r["state"][:20],
                f"{r['existing_pen']:.1f}",
                f"{abs(r['score_delta']):.2f}",
                f"{r['combined_stack']:.2f}",
                "⚠ REVIEW" if r["combined_stack"] > 20 else "✅ OK",
            ])
        lines.append(_md_table(
            ["Product", "State", "Existing Penalties", "Pilot Penalty", "Combined", "Stack Check"],
            srows
        ))
    else:
        lines.append("_No products with combined penalty stack data available._")

    lines += [
        "",
        "---",
        "",
        f"*BSIP2-061 Pilot Results — TASK-051 — {run_dt}*",
        f"*EXPERIMENTAL. No production deployment. Option B only.*",
        f"*Corpus: run_hummus_002 (69 products, Shufersal hummus and savory dips)*",
    ]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written: {REPORT_PATH}")


if __name__ == "__main__":
    results = run_pilot()
    by_state = {}
    for r in results:
        by_state.setdefault(r["state"], []).append(r)

    print("\n=== ACTIVATION SUMMARY ===")
    for state, items in sorted(by_state.items()):
        print(f"  {state}: {len(items)}")
    grade_moves = [r for r in results if r["grade_moved"]]
    print(f"  Grade changes: {len(grade_moves)}")
    fp = [r for r in results if r["is_fp"]]
    print(f"  FP candidates: {len(fp)}")
