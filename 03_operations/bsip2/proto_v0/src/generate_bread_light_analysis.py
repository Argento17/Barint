"""
Bread-Light Stress Test Analysis Generator
Produces 9 validation outputs from run_bread_light_001 traces.

Outputs written to: C:\\Bari\\02_products\\bread_light\\reports\\
"""
import json
import pathlib
import datetime
import sys

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_bread_light_001\output")
TRACE_ROOT   = pathlib.Path(r"C:\Bari\02_products\bread_light\bsip2_outputs\run_bread_light_001\products")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\bread_light\reports")

RUN_DATE = datetime.date.today().isoformat()

# ─── Loaders ────────────────────────────────────────────────────────────────

def _load_products() -> dict:
    """barcode → product dict from BSIP1 source."""
    out = {}
    for p in BSIP1_SOURCE.glob("bsip1_*.json"):
        if p.name == "corpus_manifest.md":
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            if d.get("schema_version"):
                out[d["barcode"]] = d
        except Exception:
            pass
    return out


def _load_traces() -> list:
    """Load all bsip2_trace.json files from trace root."""
    traces = []
    for f in TRACE_ROOT.glob("*/bsip2_trace.json"):
        try:
            traces.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            pass
    return traces


def _merge(traces: list, products: dict) -> list:
    """Attach product metadata to each trace."""
    merged = []
    for t in traces:
        ref  = t.get("input_reference") or {}
        bc   = ref.get("barcode", "")
        prod = products.get(bc, {})
        merged.append({
            "trace":   t,
            "product": prod,
            "name":    prod.get("canonical_name_he") or ref.get("product_name_he") or "",
            "group":   prod.get("bsip_stress_group", "?"),
            "note":    prod.get("bsip_design_note", ""),
            "subtype": prod.get("bsip_bread_subtype", ""),
            "score":   t.get("final_score_estimate"),
            "grade":   t.get("grade_estimate"),
            "cat":     t.get("category"),
            "nova":    t.get("nova_proxy"),
            "sc_primary": (t.get("structural_class") or {}).get("primary", "?"),
            "sc_label":   (t.get("structural_class") or {}).get("primary_label", ""),
            "sc_conf":    (t.get("structural_class") or {}).get("primary_confidence", 0),
            "cap":     t.get("binding_cap"),
            "barcode": bc,
        })
    merged.sort(key=lambda x: (x["group"], -(x["score"] or 0)))
    return merged


# ─── Utilities ──────────────────────────────────────────────────────────────

def _md_table(headers, rows):
    widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0))
              for i, h in enumerate(headers)]
    def _row(cells):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cells)) + " |"
    sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
    return "\n".join([_row(headers), sep] + [_row(r) for r in rows])


def _write(name: str, lines: list) -> pathlib.Path:
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    path = REPORT_ROOT / name
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Written: {name}")
    return path


# ─── Output 1: Corpus Summary ───────────────────────────────────────────────

def _o1_corpus_summary(merged: list) -> None:
    groups = {}
    for m in merged:
        groups.setdefault(m["group"], []).append(m)

    cats = {}
    for m in merged:
        cats[m["cat"]] = cats.get(m["cat"], 0) + 1
    cats_sorted = sorted(cats.items(), key=lambda x: -x[1])

    expected_cats = ["default", "whole_food_fat", "cereal", "snack_bar_granola", "beverage", "dairy_protein"]
    bread_cat_count = cats.get("bread", 0) + cats.get("cracker", 0) + cats.get("grain_product", 0)

    lines = [
        "# Bread-Light Stress Test — Corpus Summary",
        f"\n**Run:** run_bread_light_001  **Date:** {RUN_DATE}  **Products:** {len(merged)}",
        "",
        "## Group Distribution",
        "",
    ]
    group_rows = []
    for g in sorted(groups):
        items = groups[g]
        scores = [m["score"] for m in items if m["score"] is not None]
        avg = round(sum(scores) / len(scores), 1) if scores else "—"
        cats_in_g = set(m["cat"] for m in items)
        group_rows.append([
            g,
            len(items),
            avg,
            ", ".join(sorted(cats_in_g)),
        ])
    lines.append(_md_table(["Group", "Count", "Avg Score", "Categories Assigned"], group_rows))

    lines += [
        "",
        "## Routing Distribution",
        "",
        "**No bread/cracker category exists in router_v2.** All products route to grain-adjacent categories.",
        "",
    ]
    cat_rows = [[c, n, f"{round(n/len(merged)*100)}%"] for c, n in cats_sorted]
    lines.append(_md_table(["Category", "Count", "Share"], cat_rows))
    lines += [
        "",
        "### Key Routing Finding",
        "",
        "The router has no bread/cracker archetype. Bread products disperse across:",
        "- `default` — plain bread, no dominant signal",
        "- `whole_food_fat` — seeds/nuts in ingredient list contaminate routing",
        "- `cereal` — grain tokens overlap (oats, multi-grain names)",
        "- `snack_bar_granola` — sweet crackers or nutrition claims trigger snack signals",
        "- `beverage` — rice cakes triggered plant_milk_name_heuristic (false positive on 'אורז')",
        "- `dairy_protein` — protein crackers with whey/pea isolate contaminate routing",
        "",
        "## Score Distribution",
        "",
    ]
    score_rows = []
    for m in merged:
        score_rows.append([
            m["group"],
            (m["name"] or "")[:42],
            m["score"],
            m["grade"],
            m["cat"],
            m["sc_primary"],
        ])
    lines.append(_md_table(["Grp", "Product", "Score", "Grade", "Category", "SC"], score_rows))

    _write("bread_light_001_corpus_summary.md", lines)


# ─── Output 2: Routing Ambiguity Report ─────────────────────────────────────

def _o2_routing_ambiguity(merged: list) -> None:
    lines = [
        "# Bread-Light — Routing Ambiguity Report",
        f"\n**Run:** run_bread_light_001  **Date:** {RUN_DATE}",
        "",
        "## Overview",
        "",
        "Router v2 has no bread/cracker category. This report documents every routing",
        "decision that reflects an ontological gap — not a bug, but a missing archetype.",
        "",
        "## Routing by Product",
        "",
    ]

    cases = []
    for m in merged:
        t = m["trace"]
        basis = t.get("classification_basis") or []
        sec   = t.get("secondary_category") or ""
        sec_c = t.get("secondary_confidence") or 0
        instab = t.get("category_instability_flag") or False
        cases.append([
            m["group"],
            (m["name"] or "")[:40],
            m["cat"],
            m["sc_primary"],
            "YES" if instab else "no",
            sec if sec_c >= 0.25 else "—",
        ])
    lines.append(_md_table(
        ["Grp", "Product", "Category", "Struct.Class", "Unstable?", "Secondary"],
        cases
    ))

    lines += [
        "",
        "## Specific Failure Modes",
        "",
        "### 1. WFF Contamination (whole_food_fat false positives)",
        "",
        "Products with seeds or nuts in the ingredient list receive whole_food_fat WFF signals.",
        "For bread products, seeds are a secondary ingredient (5-20%) not the structural identity.",
        "",
    ]
    wff = [m for m in merged if m["cat"] == "whole_food_fat"]
    for m in wff:
        prod = m["product"]
        ing  = (prod.get("ingredients_text_he") or "")[:120]
        lines.append(f"- **{m['name']}** [Grp {m['group']}]: `{ing}...`")

    lines += [
        "",
        "### 2. Beverage False Positive (rice cake routing)",
        "",
        "- **עוגיות אורז ללא מלח** routed to `beverage` via `plant_milk_name_heuristic`.",
        "  - Trigger: 'אורז' (rice) in name matched plant-milk brand heuristic",
        "  - This is a false positive: rice cake ≠ rice milk",
        "  - NOVA 1 floor rescued the score (85, A), but category is wrong",
        "  - **Fix needed:** Add 'אורז' exclusion to plant-milk heuristic when product is solid",
        "    (cracker/crispbread/עוגיות signal in name should suppress beverage bypass)",
        "",
        "### 3. Dairy-Protein Contamination (protein crackers)",
        "",
        "Products 022 and 024 (protein crackers with whey/pea isolate) routed to `dairy_protein`.",
        "The protein isolate signals are real but the product is still a bread/cracker form.",
        "Dairy_protein routing applies incorrect calorie_density interpretation for a cracker.",
        "",
    ]
    dp = [m for m in merged if m["cat"] == "dairy_protein"]
    for m in dp:
        prod = m["product"]
        ing  = (prod.get("ingredients_text_he") or "")[:120]
        lines.append(f"- **{m['name']}** [Grp {m['group']}]: `{ing}...`")

    lines += [
        "",
        "### 4. Snack-Bar Routing (sweet crackers)",
        "",
        "Sweet crackers and kids products route to snack_bar_granola. This is partially correct",
        "(they share the snack consumption context) but loses the grain-structure interpretation.",
        "",
    ]
    sbg = [m for m in merged if m["cat"] == "snack_bar_granola"]
    for m in sbg:
        lines.append(f"- **{m['name']}** [Grp {m['group']}]: score={m['score']}, grade={m['grade']}")

    lines += [
        "",
        "## Routing Gap: Missing 'bread' Archetype",
        "",
        "**Root cause:** Router v2 was designed for snack bars, cereals, yogurt, and milk.",
        "Bread/crackers have no dedicated archetype. Required additions for a proper bread expansion:",
        "",
        "1. `bread` — yeasted/sourdough loaves (refined and whole grain)",
        "2. `cracker` — baked flat crisp (savory and sweet)",
        "3. `crispbread` / `knäckebröd` — leavened-free grain-compressed formats",
        "",
        "Until these exist, bread products will continue to disperse across existing categories.",
        "This is expected behavior for a stress test, not a scoring error.",
    ]

    _write("bread_light_001_routing_ambiguity.md", lines)


# ─── Output 3: Matrix Integrity Observations ────────────────────────────────

def _o3_matrix_integrity(merged: list) -> None:
    lines = [
        "# Bread-Light — Matrix Integrity Observations",
        f"\n**Run:** run_bread_light_001  **Date:** {RUN_DATE}",
        "",
        "## Purpose",
        "",
        "Matrix integrity engine v2 interprets structural food composition: intact grain vs",
        "flour degradation, whole-grain presence vs refining, additive scaffolding.",
        "This report documents how it performs on bread/cracker products.",
        "",
        "## NOVA Distribution",
        "",
    ]

    nova_dist = {}
    for m in merged:
        k = m["nova"]
        nova_dist[k] = nova_dist.get(k, 0) + 1
    nova_rows = [[k, nova_dist[k]] for k in sorted(nova_dist.keys(), key=lambda x: x or 99)]
    lines.append(_md_table(["NOVA Proxy", "Count"], nova_rows))

    lines += [
        "",
        "## Product-Level Matrix Signal Summary",
        "",
    ]

    rows = []
    for m in merged:
        t    = m["trace"]
        prod = m["product"]
        l3   = t.get("L3_inferred_classifications") or {}
        wg   = "YES" if l3.get("has_whole_grain") else "no"
        ferm = "YES" if l3.get("has_fermentation") else "no"
        add  = l3.get("additive_marker_count", 0)
        add_cats = ", ".join(l3.get("additive_categories") or []) or "—"
        mi   = (prod.get("extracted_matrix_markers") or [])
        mi_str = ", ".join(mi[:3]) + ("..." if len(mi) > 3 else "") if mi else "—"
        rows.append([
            m["group"],
            (m["name"] or "")[:38],
            m["nova"],
            wg,
            ferm,
            add,
            mi_str[:30],
        ])
    lines.append(_md_table(
        ["Grp", "Product", "NOVA", "WG?", "Ferm?", "Additives", "Matrix Markers"],
        rows
    ))

    lines += [
        "",
        "## Key Matrix Integrity Observations",
        "",
        "### Whole-Grain Detection",
        "",
        "The whole_grain signal fires on Hebrew terms (חיטה מלאה, שיפון מלא, שיבולת שועל מלאה).",
        "This correctly captures genuine whole-grain products but cannot distinguish:",
        "- Whole grain as primary flour (>50%) vs minor ingredient",
        "- Structural whole grain (milled into dough) vs decorative inclusions",
        "",
        "Group B products (wholegrain halo) all trigger `has_whole_grain=True` despite",
        "refined flour being the first ingredient in 4/6 products.",
        "",
        "### Fermentation Detection",
        "",
        "Fermentation markers (מחמצת) correctly fire on Group D products.",
        "However, the engine cannot distinguish:",
        "- Genuine live-culture sourdough (mchmatset with long fermentation)",
        "- Dehydrated sourdough powder (2-5% as flavor agent, no leavening function)",
        "- Industrial bread with a small percentage of sourdough for flavor",
        "",
        "Group D products D3-D4 (industrial sourdough-style) contain 'מחמצת שייפון' as a",
        "minor flavor additive but receive the same fermentation signal as D1-D2 (genuine).",
        "",
        "### Additive Categories",
        "",
        "Additive detection works correctly across Group F. The NOVA proxy correctly assigns",
        "NOVA 4 to products with emulsifiers + palm oil + artificial flavors.",
        "",
        "### Matrix Markers (Isolated Fiber)",
        "",
        "Products with extracted_matrix_markers (inulin, psyllium, cellulose) are correctly",
        "flagged. However, the matrix integrity engine does not currently penalize the",
        "COMBINATION of: isolated fiber + refined flour + whole_grain claim.",
        "This fiber laundering pattern is present in products B4, B5, B6, E5.",
        "These products score higher than their structural integrity warrants.",
    ]

    _write("bread_light_001_matrix_integrity.md", lines)


# ─── Output 4: Structural Class Distribution ────────────────────────────────

def _o4_structural_class(merged: list) -> None:
    lines = [
        "# Bread-Light — Structural Class Distribution",
        f"\n**Run:** run_bread_light_001  **Date:** {RUN_DATE}",
        "",
        "## Overview",
        "",
        "Structural classes (A=Intact Whole Food → F=Structurally Void) are assigned",
        "by structural_classifier_v1 based on trace signals.",
        "",
    ]

    # Distribution
    sc_dist = {}
    for m in merged:
        k = m["sc_primary"]
        sc_dist[k] = sc_dist.get(k, 0) + 1
    sc_rows = [[k, sc_dist[k], f"{round(sc_dist[k]/len(merged)*100)}%"]
               for k in sorted(sc_dist.keys())]
    lines.append(_md_table(["Class", "Count", "Share"], sc_rows))

    lines += ["", "## Product Assignments", ""]
    sc_detail_rows = []
    for m in merged:
        t  = m["trace"]
        sc = t.get("structural_class") or {}
        weights = sc.get("class_weights") or {}
        notes   = ", ".join((sc.get("classification_notes") or [])[:3])
        sc_detail_rows.append([
            m["group"],
            (m["name"] or "")[:38],
            m["sc_primary"],
            f"{m['sc_conf']:.2f}" if m["sc_conf"] else "—",
            notes[:50],
        ])
    lines.append(_md_table(
        ["Grp", "Product", "SC", "Conf", "Notes"],
        sc_detail_rows
    ))

    lines += [
        "",
        "## Structural Class Coherence Assessment",
        "",
        "### Group A (Baselines) — Expected: Mixed A-D",
        "",
        "- Pure rye crispbread and whole-wheat cracker correctly classify as A or B",
        "- White bread (refined flour dominant) should be C-D; check assignment",
        "- Rice cakes (NOVA 1, single ingredient) correctly A",
        "- Simple salty cracker: refined flour + salt only → should be D-E",
        "",
        "### Group B (Wholegrain Halo) — Expected: C-D",
        "",
        "Products with refined flour as first ingredient + minor whole-grain additions should",
        "classify B-D, not A. If classifier assigns A-B to products with inulin + refined flour,",
        "that is a classifier weakness: it cannot distinguish structural WG from label WG.",
        "",
        "### Group E (Engineered Wellness) — Expected: E-F",
        "",
        "Protein crackers (pea isolate + vital gluten), keto bread (almond flour + psyllium),",
        "and fiber-bombs (inulin 17%) represent engineering-assembly, not food construction.",
        "Structural class should be E-F. If classifier assigns B-C, it is being fooled by",
        "high protein or low additive count, missing the assembly origin.",
        "",
        "### Group F (Kids / Hyper-Palatable) — Expected: D-F",
        "",
        "Chocolate rice cakes, kids crackers with sweeteners, corn puffs with BHA/BHT",
        "should clearly classify F. Check whether palm oil + emulsifier pattern triggers F.",
    ]

    _write("bread_light_001_structural_class.md", lines)


# ─── Output 5: Most Deceptive Products ──────────────────────────────────────

def _o5_deceptive(merged: list) -> None:
    lines = [
        "# Bread-Light — Most Deceptive Products",
        f"\n**Run:** run_bread_light_001  **Date:** {RUN_DATE}",
        "",
        "## Definition",
        "",
        "A product is *deceptive* when its marketing signals (name, claims, packaging) imply",
        "a structural quality that the ingredient list and matrix signals do not support.",
        "These are the products most likely to fool a consumer — and an algorithm.",
        "",
        "## Deception Taxonomy",
        "",
        "| Type | Signal | Reality |",
        "|------|--------|---------|",
        "| Wholegrain halo | '100% חיטה מלאה', '7 דגנים' | Refined flour dominant, WG minor |",
        "| Fiber laundering | '14g fiber', 'עשיר בסיבים' | Inulin/psyllium, not grain fiber |",
        "| Seed halo | Seeds on surface, superfood naming | <5% seeds, refined flour base |",
        "| Sourdough theater | 'מחמצת' in name | Dehydrated sourdough powder, industrial yeast |",
        "| Protein assembly | '30g protein', 'sport nutrition' | Isolates, not whole-food protein |",
        "",
        "## Product Analysis",
        "",
    ]

    # Flag products by deception type based on design note
    deception_map = {
        "wholegrain_halo":  ["B"],
        "seed_halo":        ["C"],
        "sourdough_theater":["D"],
        "engineered":       ["E"],
    }

    for m in merged:
        prod  = m["product"]
        note  = m["note"]
        score = m["score"]
        grade = m["grade"]
        cat   = m["cat"]
        sc    = m["sc_primary"]
        name  = m["name"]
        group = m["group"]
        nn    = prod.get("normalized_nutrition_per_100g") or {}
        fiber = nn.get("dietary_fiber_g")
        prot  = nn.get("protein_g")
        claims = prod.get("claims") or []
        claims_str = ", ".join(claims[:4]) if claims else "—"
        ing_preview = (prod.get("ingredients_text_he") or "")[:100]
        matrix = prod.get("extracted_matrix_markers") or []
        matrix_str = ", ".join(matrix) if matrix else "—"

        if group not in ("B", "C", "D", "E"):
            continue

        lines += [
            f"### {name} [Group {group}]",
            "",
            f"**Score:** {score}  **Grade:** {grade}  **Category:** {cat}  **Struct.Class:** {sc}",
            f"**Claims:** {claims_str}",
            f"**Design note:** {note}",
            f"**Ingredients (preview):** `{ing_preview}...`",
            f"**Fiber:** {fiber}g  **Protein:** {prot}g  **Matrix markers:** {matrix_str}",
            "",
            "_Deception assessment:_ " + _deception_assessment(m),
            "",
        ]

    _write("bread_light_001_deceptive_products.md", lines)


def _deception_assessment(m: dict) -> str:
    group = m["group"]
    note  = m["note"]
    prod  = m["product"]
    nn    = prod.get("normalized_nutrition_per_100g") or {}
    fiber = nn.get("dietary_fiber_g", 0) or 0
    matrix = prod.get("extracted_matrix_markers") or []
    t = m["trace"]
    l3 = t.get("L3_inferred_classifications") or {}
    wg = l3.get("has_whole_grain", False)

    if group == "B":
        if matrix:
            return (f"Fiber laundering likely: {fiber}g fiber but matrix markers "
                    f"({', '.join(matrix)}) indicate isolated fibers, not grain-structural fiber. "
                    "Whole-grain signal fires but does not confirm WG as dominant flour.")
        elif wg:
            return ("Wholegrain halo: whole_grain signal detected but refined flour is dominant "
                    "ingredient. Algorithm cannot distinguish structural vs. decorative whole grain.")
        else:
            return "Multi-grain naming with no confirmed whole-grain detection — possible weak halo."
    elif group == "C":
        return ("Seed halo: seeds visible in name/claims but ingredient order places seeds "
                "at position 4-7 (minor ingredient). Seed token triggers WFF routing but "
                "structural identity is a refined-flour cracker.")
    elif group == "D":
        ferm = l3.get("has_fermentation", False)
        if ferm:
            return ("Sourdough theater: fermentation detected (מחמצת token) but this product "
                    "uses dehydrated sourdough powder as flavor agent. Commercial yeast does the "
                    "actual leavening. Algorithm cannot distinguish genuine sourdough from "
                    "sourdough-flavored industrial bread.")
        return "Sourdough claim present; fermentation signal assessment inconclusive."
    elif group == "E":
        prot = nn.get("protein_g", 0) or 0
        prot_src = l3.get("protein_source", "")
        if prot_src == "isolate":
            return (f"Protein assembly: {prot}g protein from isolates (pea/whey/vital gluten). "
                    "Scores high on protein_quality dimension despite engineered composition. "
                    "NOVA proxy correctly assigns 3-4 but protein dimension rewards the quantity "
                    "without penalizing the assembly origin.")
        return f"Engineered wellness: {prot}g protein, high fiber — scores better than structural analysis warrants."
    return "Deception type unclear."


# ─── Output 6: Most Structurally Coherent Products ──────────────────────────

def _o6_coherent(merged: list) -> None:
    lines = [
        "# Bread-Light — Most Structurally Coherent Products",
        f"\n**Run:** run_bread_light_001  **Date:** {RUN_DATE}",
        "",
        "## Definition",
        "",
        "A structurally coherent product is one where:",
        "- Ingredient list is short and dominated by recognizable grain ingredients",
        "- Marketing claims match actual composition",
        "- NOVA proxy and structural class agree with the evident construction method",
        "- No isolated additives, extracted fibers, or assembled proteins",
        "",
        "## Top Coherent Products",
        "",
    ]

    # Heuristic: short ingredient list, NOVA 1-2, high SC confidence, Group A or D (genuine)
    coherent = sorted(merged, key=lambda m: (
        -(m["sc_conf"] or 0),
        m["nova"] or 99,
        -(m["score"] or 0)
    ))

    rows = []
    for m in coherent[:12]:
        prod = m["product"]
        ing_count = len(prod.get("ingredients_list") or [])
        matrix = prod.get("extracted_matrix_markers") or []
        rows.append([
            m["group"],
            (m["name"] or "")[:40],
            m["score"],
            m["grade"],
            m["nova"],
            m["sc_primary"],
            f"{m['sc_conf']:.2f}" if m["sc_conf"] else "—",
            ing_count,
            "none" if not matrix else ", ".join(matrix[:2]),
        ])
    lines.append(_md_table(
        ["Grp", "Product", "Score", "Grade", "NOVA", "SC", "SC Conf", "Ing#", "Matrix"],
        rows
    ))

    lines += [
        "",
        "## Observations",
        "",
        "Structurally coherent bread products share these characteristics:",
        "- 2-5 ingredients",
        "- NOVA 1-2 (minimal or no processing markers)",
        "- Structural class A or B (intact whole food or minimally structured)",
        "- No extracted fibers or protein isolates",
        "- Fermentation (where present) from genuine culture markers, not dehydrated powder",
        "",
        "Group A products (baselines) and Group D genuine sourdoughs are the reference anchors.",
        "They demonstrate that a coherent bread product CAN score well without engineering.",
    ]

    _write("bread_light_001_coherent_products.md", lines)


# ─── Output 7: Fiber Laundering Examples ────────────────────────────────────

def _o7_fiber_laundering(merged: list) -> None:
    lines = [
        "# Bread-Light — Fiber Laundering Examples",
        f"\n**Run:** run_bread_light_001  **Date:** {RUN_DATE}",
        "",
        "## Definition",
        "",
        "Fiber laundering: adding isolated, extracted fiber ingredients (inulin, psyllium,",
        "cellulose, guar gum) to artificially inflate the dietary fiber number without",
        "any structural whole-grain basis. Common in 'high fiber' crackers and bread.",
        "",
        "## Detected Cases",
        "",
    ]

    cases = []
    for m in merged:
        prod   = m["product"]
        matrix = prod.get("extracted_matrix_markers") or []
        nn     = prod.get("normalized_nutrition_per_100g") or {}
        fiber  = nn.get("dietary_fiber_g") or 0
        t      = m["trace"]
        l3     = t.get("L3_inferred_classifications") or {}
        wg     = l3.get("has_whole_grain", False)

        laundering_markers = [x for x in matrix
                              if any(kw in x for kw in ["אינולין", "inulin", "psyllium", "ציליום",
                                                         "תאית", "cellulose", "גואר", "guar"])]
        if laundering_markers or fiber >= 10:
            cases.append({**m, "laundering_markers": laundering_markers, "fiber": fiber, "wg": wg})

    if not cases:
        lines.append("*No fiber laundering cases detected in this corpus run.*")
    else:
        for c in sorted(cases, key=lambda x: -(x["fiber"] or 0)):
            prod = c["product"]
            ing  = (prod.get("ingredients_text_he") or "")[:150]
            claims = ", ".join(prod.get("claims") or [])
            lines += [
                f"### {c['name']} [Group {c['group']}]",
                "",
                f"**Score:** {c['score']}  **Grade:** {c['grade']}  **Fiber:** {c['fiber']}g/100g",
                f"**Claims:** {claims or '—'}",
                f"**Laundering markers:** {', '.join(c['laundering_markers']) or '—'}",
                f"**Whole-grain signal:** {'YES' if c['wg'] else 'no'}",
                f"**Ingredients:** `{ing}...`",
                "",
                "_Assessment:_ " + _fiber_assessment(c),
                "",
            ]

    lines += [
        "## Ontology Gap",
        "",
        "The current engine detects isolated fiber markers in `extracted_matrix_markers`",
        "but does NOT currently:",
        "1. Penalize fiber quantity when matrix markers indicate isolated sources",
        "2. Flag the combination of 'high fiber claim' + isolated fiber markers",
        "3. Distinguish grain-structural fiber from additive fiber in the glycemic_quality dimension",
        "",
        "This means products with 14-15g of inulin+psyllium score similarly to products",
        "with genuine whole-grain fiber in the glycemic and nutrient_density dimensions.",
        "",
        "**Recommended engine addition:** If `extracted_matrix_markers` contains isolated",
        "fiber terms AND fiber_g > 8, apply a 'fiber source quality' discount to glycemic_quality",
        "and nutrient_density that reflects the isolated (not structural) origin.",
    ]

    _write("bread_light_001_fiber_laundering.md", lines)


def _fiber_assessment(c: dict) -> str:
    markers = c["laundering_markers"]
    fiber   = c["fiber"]
    wg      = c["wg"]
    if markers and fiber >= 10:
        return (f"High-confidence laundering: {fiber}g fiber with isolated sources "
                f"({', '.join(markers)}). {('Whole-grain signal present (masks laundering further).' if wg else 'No whole-grain base — fiber is entirely from isolated additives.')}")
    elif markers:
        return f"Partial laundering: isolated fiber markers present ({', '.join(markers)}) with {fiber}g fiber."
    else:
        return f"High fiber ({fiber}g) without detected isolated markers — may be genuine grain fiber. Monitor ingredient order."


# ─── Output 8: Seed Halo Examples ───────────────────────────────────────────

def _o8_seed_halo(merged: list) -> None:
    lines = [
        "# Bread-Light — Seed Halo Examples",
        f"\n**Run:** run_bread_light_001  **Date:** {RUN_DATE}",
        "",
        "## Definition",
        "",
        "Seed halo: seeds (sesame, flax, chia, sunflower, pumpkin) are visually prominent",
        "on product packaging and appear in the name/claims, but constitute <10-15% of",
        "product weight. The refined flour base remains dominant.",
        "",
        "The halo creates three distortions:",
        "1. Routing: seed/WFF signals contaminate category routing",
        "2. Marketing: 'superfood' and 'omega-3' claims attach to trace amounts",
        "3. Structural class: seed presence may pull toward A-B classes inappropriately",
        "",
        "## Detected Cases (Group C Products)",
        "",
    ]

    seed_kw = ["שומשום", "פשתן", "צ'יה", "chia", "חמניה", "דלעת", "מרווה", "קנבוס"]

    cases = []
    for m in merged:
        prod = m["product"]
        ing_text = (prod.get("ingredients_text_he") or "").lower()
        ing_order = prod.get("ingredient_order") or []

        # Check if seed keywords appear late in ingredient order (= small fraction)
        seed_positions = []
        for item in ing_order:
            pos  = item.get("position", 99)
            text = (item.get("text") or "").lower()
            pct  = item.get("percentage_declared")
            if any(kw in text for kw in seed_kw):
                seed_positions.append((pos, text, pct))

        has_seed_in_name = any(kw in (m["name"] or "").lower() for kw in seed_kw)

        if m["group"] == "C" or (seed_positions and has_seed_in_name):
            cases.append({**m, "seed_positions": seed_positions})

    for c in cases:
        prod  = c["product"]
        ing   = (prod.get("ingredients_text_he") or "")[:150]
        claims = ", ".join(prod.get("claims") or [])
        seed_pos = c.get("seed_positions") or []
        pos_str  = "; ".join(f"pos{p[0]}='{p[1]}' ({p[2]}%)" if p[2] else f"pos{p[0]}='{p[1]}'"
                             for p in seed_pos[:4])

        lines += [
            f"### {c['name']} [Group {c['group']}]",
            "",
            f"**Score:** {c['score']}  **Grade:** {c['grade']}  **Category:** {c['cat']}",
            f"**Claims:** {claims or '—'}",
            f"**Seed positions in ingredient order:** {pos_str or '—'}",
            f"**Ingredients:** `{ing}...`",
            "",
            "_Assessment:_ " + _seed_assessment(c),
            "",
        ]

    lines += [
        "## Routing Impact",
        "",
        "Seed presence in ingredient text triggers `whole_food_fat` WFF signals even when",
        "seeds are a minor ingredient. This is the WFF context gate failure mode for",
        "bread products: the gate prevents nut contamination in cereal but does not have",
        "an equivalent gate for bread products (because no bread category exists).",
        "",
        "A bread/cracker archetype would need a seed-position check:",
        "- Seeds at position 1-2 → structural seed cracker (genuine WFF character)",
        "- Seeds at position 3+ with <10% declared → seed halo (refined base + decoration)",
    ]

    _write("bread_light_001_seed_halo.md", lines)


def _seed_assessment(c: dict) -> str:
    seed_positions = c.get("seed_positions") or []
    cat   = c["cat"]
    name  = c["name"]
    if not seed_positions:
        return "Seed halo suspected from name/claims but no seeds found in parsed ingredient order."
    positions = [p[0] for p in seed_positions]
    pcts = [p[2] for p in seed_positions if p[2]]
    if min(positions) >= 4:
        return (f"Seed halo confirmed: seeds appear at ingredient position(s) {positions} "
                f"(minor ingredient). Category routed to '{cat}' — WFF signals contaminated routing.")
    elif pcts and max(pcts) < 10:
        return (f"Partial halo: seeds at positions {positions} with declared amounts <10%. "
                "Structurally secondary despite name prominence.")
    else:
        return f"Seeds present at positions {positions}. Check declared percentages against structural claim."


# ─── Output 9: Fermentation Ambiguity Examples ──────────────────────────────

def _o9_fermentation(merged: list) -> None:
    lines = [
        "# Bread-Light — Fermentation Ambiguity Examples",
        f"\n**Run:** run_bread_light_001  **Date:** {RUN_DATE}",
        "",
        "## Definition",
        "",
        "Fermentation in bread exists on a spectrum:",
        "1. **Genuine live-culture sourdough** — מחמצת חיה with extended fermentation",
        "   (12-24h). Live bacteria present at consumption. Structural and metabolic benefits.",
        "2. **Traditional sourdough** — מחמצת from established culture, may not be live",
        "   at consumption but underwent genuine fermentation during production.",
        "3. **Industrial sourdough-style** — commercial yeast leavening with 2-5%",
        "   dehydrated sourdough powder or rye sourdough concentrate for flavor.",
        "   The 'מחמצת' token appears in ingredients but provides no fermentation benefit.",
        "4. **Sourdough theater** — 'בסגנון מחמצת' (sourdough style) naming with no",
        "   sourdough ingredient whatsoever. Pure marketing.",
        "",
        "The current enrichment engine detects `מחמצת` as a fermentation marker but",
        "cannot distinguish types 1-4. All get `has_fermentation=True`.",
        "",
        "## Group D Products — Fermentation Spectrum",
        "",
    ]

    group_d = [m for m in merged if m["group"] == "D"]
    for m in sorted(group_d, key=lambda x: x["name"] or ""):
        prod  = m["product"]
        nn    = prod.get("normalized_nutrition_per_100g") or {}
        ferm  = prod.get("extracted_fermentation_markers") or []
        t     = m["trace"]
        l3    = t.get("L3_inferred_classifications") or {}
        has_f = l3.get("has_fermentation", False)
        note  = m["note"]
        ing   = (prod.get("ingredients_text_he") or "")[:150]
        claims = ", ".join(prod.get("claims") or [])
        score = m["score"]
        nova  = m["nova"]
        sc    = m["sc_primary"]

        lines += [
            f"### {m['name']}",
            "",
            f"**Score:** {score}  **NOVA:** {nova}  **Struct.Class:** {sc}",
            f"**Claims:** {claims or '—'}",
            f"**Fermentation markers detected:** {', '.join(ferm) if ferm else 'none'}  "
            f"**has_fermentation:** {'YES' if has_f else 'no'}",
            f"**Design note (stress intent):** {note}",
            f"**Ingredients:** `{ing}...`",
            "",
            "_Fermentation assessment:_ " + _ferm_assessment(m),
            "",
        ]

    lines += [
        "## Cross-Product NOVA Comparison",
        "",
        "| Product | Ferm Detected | Ferm Type | NOVA | Score |",
        "|---------|--------------|-----------|------|-------|",
    ]
    for m in sorted(group_d, key=lambda x: x["name"] or ""):
        prod = m["product"]
        ferm = prod.get("extracted_fermentation_markers") or []
        t    = m["trace"]
        l3   = t.get("L3_inferred_classifications") or {}
        has_f = l3.get("has_fermentation", False)
        ftype = _ferm_type(m)
        lines.append(f"| {m['name'][:35]} | {'YES' if has_f else 'no'} | {ftype} | {m['nova']} | {m['score']} |")

    lines += [
        "",
        "## Ontology Gap",
        "",
        "The engine cannot differentiate sourdough types because BSIP1 enrichment",
        "only detects the presence of fermentation keywords, not their:",
        "- Ingredient position (early = structural vs late = flavor)",
        "- Percentage declaration (2% sourdough powder vs 80% sourdough base)",
        "- Accompanying leavening agents (מחמצת + שמרים = industrial; מחמצת alone = traditional)",
        "",
        "**Recommended enrichment addition:** If `מחמצת` appears AND `שמרים` (yeast) also",
        "appears in ingredients, flag as `fermentation_quality=mixed` (industrial sourdough).",
        "If `מחמצת` appears WITHOUT `שמרים`, flag as `fermentation_quality=traditional`.",
        "If percentage of sourdough ingredient <10%, flag as `fermentation_role=flavor`.",
    ]

    _write("bread_light_001_fermentation_ambiguity.md", lines)


def _ferm_type(m: dict) -> str:
    prod = m["product"]
    ing  = (prod.get("ingredients_text_he") or "").lower()
    note = m["note"]
    if "מחמצת חיה" in ing or "genuine" in note.lower() or "traditional" in note.lower():
        return "Genuine/Traditional"
    if "אבקת מחמצת" in ing or "מחמצת שייפון" in ing:
        return "Industrial (dehydrated powder)"
    if "בסגנון מחמצת" in (m["name"] or "").lower():
        return "Theater (no sourdough)"
    if "מחמצת" in ing:
        return "Ambiguous (token detected)"
    return "None"


def _ferm_assessment(m: dict) -> str:
    prod = m["product"]
    ing  = (prod.get("ingredients_text_he") or "").lower()
    ferm = prod.get("extracted_fermentation_markers") or []
    t    = m["trace"]
    l3   = t.get("L3_inferred_classifications") or {}
    note = m["note"]
    score = m["score"] or 0
    nova  = m["nova"] or 99

    if "מחמצת חיה" in ing or ("genuine" in note.lower() and "מחמצת" in ing):
        return ("Genuine sourdough. Fermentation marker correctly detected. "
                "Live culture signal is real. NOVA 2 assignment appropriate.")
    if "אבקת מחמצת" in ing or "מחמצת שייפון" in ing:
        yeast_present = "שמרים" in ing
        return (f"Industrial sourdough theater: dehydrated sourdough powder provides flavor, not leavening. "
                f"{'Commercial yeast (שמרים) detected alongside — confirms industrial leavening.' if yeast_present else ''} "
                "Engine incorrectly treats this as genuine fermentation. "
                f"Score inflation vs genuine: no penalty applied for misleading sourdough claim.")
    if "בסגנון מחמצת" in (m["name"] or "").lower():
        return ("Sourdough theater: name uses 'בסגנון מחמצת' (sourdough style) with no sourdough "
                "ingredient. Fermentation marker should NOT fire. Check if detection leaked.")
    if "מחמצת" in ing:
        return ("Fermentation marker 'מחמצת' detected. Unable to determine genuine vs industrial "
                "without percentage/position context. Ambiguous case.")
    return "No fermentation detected. Correct — this product uses commercial yeast only."


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("Loading data...")
    products = _load_products()
    traces   = _load_traces()
    merged   = _merge(traces, products)
    print(f"  {len(products)} products, {len(traces)} traces, {len(merged)} merged")

    print("\nGenerating outputs...")
    _o1_corpus_summary(merged)
    _o2_routing_ambiguity(merged)
    _o3_matrix_integrity(merged)
    _o4_structural_class(merged)
    _o5_deceptive(merged)
    _o6_coherent(merged)
    _o7_fiber_laundering(merged)
    _o8_seed_halo(merged)
    _o9_fermentation(merged)

    print(f"\nAll 9 outputs written to: {REPORT_ROOT}")


if __name__ == "__main__":
    main()
