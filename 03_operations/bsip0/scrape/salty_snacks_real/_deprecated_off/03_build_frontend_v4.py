"""
Build salty_snacks_frontend_v4.json from BSIP2 run_salty_snacks_002 traces (REAL rebuild).
TASK-228 base + TASK-231 remediation (TASK-230 corrected copy spec applied).

Engine unchanged (engine-baseline-2026-06-04 + TASK-216 extrusion signal). Editorial
content DERIVED FROM THE REAL TRACE (signals/caps/penalties). TASK-231 remediation:
  - Copy spec COPY_SPEC_v4_TASK230.md applied: no NOVA/framework leak, no raw decimals
    as text, no recommendation language, reworded confidence labels. Every consumer
    string is gate-checked with hebrew_readability.is_clean and the build fails on any leak.
  - Bamba clutter cut to 2 canonical (classic + sweet); 6 near-dup variants dropped.
  - Brand field normalized corpus-wide to one canonical per maker.
  - Garbled/English ingredient strings omitted + product marked panel-only (no fabricated He).
  - Apropo/2 others: sodium genuinely null at source (OFF has no salt field) -> marked honestly.
  - novaGroup<->copy contradiction removed (copy driven off nova integer, not rule name).
  - Beet cracker trans corrected upstream (fix_beet_cracker_trans.py); re-scored 0/E -> 60/C.
  - d4_additives preserved by merge from the prior JSON (added by wire_d4_salty_snacks_v4.py).
"""
import sys, json, pathlib, datetime
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Bari\integrations\clients")
import hebrew_readability as hr  # noqa: E402
# TASK-233B: shared packaging core owns grade derivation, confidence derivation (7-state),
# image-URL selection, and the VM field strip. Local grade_from_score / confidence_fields
# kept only as thin wrappers around the core to preserve this generator's call sites.
sys.path.insert(0, r"C:\Bari\03_operations\bsip2\proto_v0\src")
import frontend_core as FC  # noqa: E402

TRACES_DIR = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_002\products")
BSIP1_DIR  = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip1_outputs")
OUT_LOCAL  = pathlib.Path(r"C:\Bari\02_products\salty_snacks\salty_snacks_frontend_v4.json")
OUT_WEB    = pathlib.Path(r"C:\bari\bari-web\src\data\comparisons\salty_snacks_frontend_v4.json")

# ── TASK-231 curation: drop 6 near-duplicate Bamba variants ────────────────────
# Keep canonical classic (7290000066318, 61/C) + distinct sweet Bamba
# (7290000066295, 30/E). Cut: birthday (garbled ingredients), 10-pack (pack variant
# of classic), 3 Bisli-mix variants (near-identical to each other), nougat-cream
# filling (redundant 2nd sweet Bamba).
DROP_IDS = {
    "bsip1_snack_7290000068770",  # במבה יום הולדת 80 גרם (garbled ingredients; pack variant)
    "bsip1_snack_7290105693341",  # במבה מארז 10*25 גרם (pack variant of classic)
    "bsip1_snack_7290118426202",  # במבה ביסלי גריל מיקס 70 גרם
    "bsip1_snack_7290118426226",  # במבה ביסלי בצל מיקס 70 גרם
    "bsip1_snack_7290118426240",  # במבה ביסלי ברביקיו מיקס 70 גרם
    "bsip1_snack_7290100687109",  # במבה במילוי קרם נוגט (redundant sweet Bamba)
}

# ── TASK-234 (RT-5 MEDIUM): whole-panel per-100g basis error — drop from shelf ──
# Three "chips" carry 128/139/145 kcal/100g; Atwater(macros) reproduces the stated kcal,
# so the ENTIRE panel (every macro) is on a per-serving basis mislabeled per-100g (a real
# fried/baked potato crisp is ~450-540 kcal/100g). OFF carries no serving_size to recover
# the scale factor -> the per-100g basis is UNRECOVERABLE. Honest action: drop from the
# scored shelf rather than publish/score a panel known to be on the wrong basis (which
# inflates the score by suppressing calorie-density + fat penalties). See
# fix_trans_artifacts_corpus.py BASIS_ERROR_CHIPS + BSIP1 data_corrections.
BASIS_ERROR_EXCLUDE = {
    "bsip1_snack_7290018198254": "128 kcal/100g — per-serving panel mislabeled per-100g; unrecoverable",
    "bsip1_snack_7290018198148": "139 kcal/100g — per-serving panel mislabeled per-100g; unrecoverable",
    "bsip1_snack_7290004943738": "145 kcal/100g — per-serving panel mislabeled per-100g; unrecoverable",
}

# ── TASK-231 brand normalization: one canonical string per maker ───────────────
# Resolves: Osem/אסם/اوسم/Some/Same -> אסם ; Fitness/פיטנס -> פיטנס ;
# Click/קליק -> קליק ; geresh variants of תפוצ'יפס -> one (U+05F3) ; Salty/empty -> real maker.
BRAND_CANONICAL = {
    "osem": "אסם", "אסם": "אסם", "اوسم": "אסם", "some": "אסם", "same": "אסם",
    "fitness": "פיטנס", "פיטנס": "פיטנס",
    "click": "קליק", "קליק": "קליק",
    "energy": "Energy", "nestlé": "נסטלה", "nestle": "נסטלה",
    "real foods": "Real Foods",
    "calbee": "Calbee", "pop star": "Pop Star", "hotpop": "Hotpop",
    "werther's original": "Werther's Original",
    "meir bagel": "מאיר בייגל", "milotal": "מילוטל", "מילוטל": "מילוטל",
    "עלית": "עלית", "עלית דוריטוס": "עלית",
    "יוחננוף": "יוחננוף",
}
# barcode-specific brand assignment (empty/garbage brand -> real maker from name/identity)
BRAND_BY_BARCODE = {
    "7290111564291": "נסטלה",     # פריכיות קינואה (Nestlé Craquottes line; sibling 7290111564277=Nestlé)
    "7290017928661": "סמאש",       # שברי בייגלה צ'דר (name_off "Smash")
    "4011800528416": "Corny",      # קורני חטיפי דגנים (name_off "corny Snack bar")
    "7290018893654": "צ'וקטה",     # בייגלה צ'וקטה (brand garbage "Salty"; maker = Choctta)
    "7290018198254": "תפוגן",      # קריספי צ'יפס תפוגן (brand garbage "תפו״א")
    "7290110551926": "תפוצ'יפס",   # geresh U+05F4 variant -> canonical U+05F3
    "7290008745239": "תפוצ'יפס",   # already U+05F3, keep canonical
    "7290104500572": "אפרופו",
    "7290118421603": "אפרופו",
}

# ── TASK-231: ingredient strings to OMIT (garbled or English -> panel-only) ─────
# No fabricated Hebrew; OFF has no Hebrew ingredient variant for these.
INGREDIENTS_OMIT = {
    "7290000068770",  # garbled RTL scanner output (dropped product anyway)
    "9322969000022",  # English: "Maize (89%), Linseed (6%)..."
    "7290000069364",  # English: "whole rice (99.9%), soy lecithin"
    "4014400925319",  # English: "sugar, corn, glucose syrup..."
    "7290112968807",  # English: "whole wheat flour (31%)..."
    "7290112494313",  # partially garbled Hebrew ("9תות תירס", "מלת מתחלב") — don't ship degraded
}


def grade_from_score(s):
    # Delegates to the shared core so disk grade == corpus.ts runtime grade. Fixes the
    # DA-009 boundary drift (e.g. 7290000066332 = 65 was shipping disk 'C' while the
    # runtime normalizer derived 'B'). None -> None (unscored chip), never a bespoke '?'.
    return FC.grade_from_score(s)


def retailer_he(r):
    return {"yochananof": "יוחננוף", "shufersal": "שופרסל", "carrefour": "קרפור"}.get(r, r)


import re as _re

def clean_ingredient_text(text):
    """Light, meaning-preserving cleanup for an otherwise-clean Hebrew ingredient list:
    fix European decimal commas in percentages (70,5% -> 70.5%) and drop a trailing
    standalone English token that duplicates a Hebrew term already present (e.g. an
    appended 'aspartam' after 'אספרטיים'). E-number additive codes are kept (real, legible)."""
    if not text:
        return text
    text = _re.sub(r"(\d),(\d)", r"\1.\2", text)            # 70,5% -> 70.5%
    text = _re.sub(r"[,\s]+[A-Za-z]{3,}\s*$", "", text)     # drop a single trailing English word
    return text.strip().rstrip(",").strip()


def canonical_brand(raw_brand, barcode):
    if barcode in BRAND_BY_BARCODE:
        return BRAND_BY_BARCODE[barcode]
    key = (raw_brand or "").strip().lower()
    if key in BRAND_CANONICAL:
        return BRAND_CANONICAL[key]
    return (raw_brand or "").strip()


def load_bsip1():
    by = {}
    for f in BSIP1_DIR.glob("bsip1_snack_*.json"):
        d = json.loads(f.read_text("utf-8"))
        by[d["canonical_product_id"]] = d
    return by


def load_traces():
    out = []
    for pd in TRACES_DIR.iterdir():
        tp = pd / "bsip2_trace.json"
        if tp.exists():
            out.append(json.loads(tp.read_text("utf-8")))
    return out


def load_existing_d4():
    """Preserve d4_additives wired onto the JSON by wire_d4_salty_snacks_v4.py."""
    d4 = {}
    if OUT_WEB.exists():
        try:
            prev = json.loads(OUT_WEB.read_text("utf-8"))
            for p in prev.get("products", []):
                if p.get("d4_additives"):
                    d4[p.get("barcode") or p.get("id")] = p["d4_additives"]
        except Exception:
            pass
    return d4


# ── Copy generation (COPY_SPEC_v4_TASK230) ─────────────────────────────────────

def positive_signals(sig):
    """Plain consumer facts, varied lead. Integer grams (one-dp is false precision on
    per-100g panels and trips the score-mechanic gate); no leakage."""
    out = []
    fib = sig.get("dietary_fiber_g"); prot = sig.get("protein_g")
    sod = sig.get("sodium_mg"); sugar = sig.get("sugars_g")
    if fib is not None and fib >= 6:
        out.append(f"{round(fib)} גרם סיבים ל-100 גרם")
    if prot is not None and prot >= 10:
        out.append(f"{round(prot)} גרם חלבון ל-100 גרם")
    if sod is not None and sod <= 120:
        out.append(f"נתרן נמוך: {round(sod)} מ\"ג ל-100 גרם")
    if sugar is not None and sugar <= 2:
        out.append("כמעט בלי סוכר")
    return out[:3]


def processing_line(nova_group):
    """Spec §2 — driven off the nova INTEGER, never the rule name, never the word NOVA."""
    if nova_group == 4:
        return "מעובד מאוד, עם רשימת רכיבים ארוכה ורחוקה מהחומר הגלם."
    return None


def limiting_signals(sig, nova_group):
    """Nutrient facts first (cap at 3); processing line only for nova 4. No NOVA string."""
    out = []
    sod = sig.get("sodium_mg"); sat = sig.get("fat_saturated_g")
    fat = sig.get("fat_g"); sugar = sig.get("sugars_g")
    if sod is not None and sod >= 500:
        out.append(f"{round(sod)} מ\"ג נתרן ל-100 גרם")
    if sat is not None and sat >= 5:
        out.append(f"{round(sat)} גרם שומן רווי ל-100 גרם")
    if sugar is not None and sugar >= 15:
        out.append(f"{round(sugar)} גרם סוכר ל-100 גרם")
    if fat is not None and fat >= 25 and not any("שומן" in x for x in out):
        out.append(f"{round(fat)} גרם שומן ל-100 גרם")
    if len(out) < 3:
        pl = processing_line(nova_group)
        if pl:
            out.append(pl)
    return out[:3]


def build_insight(score, grade, sig):
    """2-paragraph verdict (line1 = finding, line2 = catch/character). Spec §3.
    No score/grade mechanic, no boilerplate, drop clauses on None, rounded numbers."""
    sod = sig.get("sodium_mg"); fib = sig.get("dietary_fiber_g")
    prot = sig.get("protein_g"); sugar = sig.get("sugars_g"); fat = sig.get("fat_g")
    sat = sig.get("fat_saturated_g")

    # ── Line 1: strongest real signal (first match) ──
    l1 = None
    if (fib is not None and fib >= 6) or (prot is not None and prot >= 9):
        if fib is not None and fib >= 6 and prot is not None and prot >= 9:
            l1 = (f"אחד החטיפים הבודדים במדף עם {round(fib)} גרם סיבים "
                  f"ו-{round(prot)} גרם חלבון ל-100 גרם.")
        elif fib is not None and fib >= 6:
            l1 = f"אחד החטיפים הבודדים במדף עם {round(fib)} גרם סיבים ל-100 גרם."
        else:
            l1 = f"אחד החטיפים הבודדים במדף עם {round(prot)} גרם חלבון ל-100 גרם."
    elif sod is not None and sod <= 120:
        l1 = f"מהפרופילים הנקיים במדף: רק {round(sod)} מ\"ג נתרן ל-100 גרם."
    elif sugar is not None and sugar >= 15:
        l1 = f"חטיף מתוק שמתחזה למלוח: {round(sugar)} גרם סוכר ל-100 גרם."
    elif sod is not None and sod >= 600:
        l1 = f"חטיף מלוח מאוד: {round(sod)} מ\"ג נתרן ל-100 גרם."
    elif fat is not None and fat >= 28:
        l1 = f"חטיף עתיר שומן: {round(fat)} גרם שומן ל-100 גרם, רובו מהטיגון והשמן."
    elif grade in ("A", "B"):
        l1 = "נשאר בין הטובים במדף, גם בלי תכונה אחת שבולטת."
    elif grade == "C":
        l1 = "פרופיל ממוצע: לא בולט לטובה אבל גם לא נופל."
    else:
        l1 = "מהחלק התחתון של המדף, עם פרופיל תזונתי חלש."

    sweet_in_l1 = l1.startswith("חטיף מתוק")
    salty_in_l1 = l1.startswith("חטיף מלוח")
    fat_in_l1 = l1.startswith("חטיף עתיר שומן")

    # ── Line 2: catch / character (first true & notable, not repeating line 1) ──
    l2 = None
    if sod is not None and sod >= 600 and not salty_in_l1:
        l2 = "שקית שלמה לבדה מכסה חלק ניכר מהנתרן היומי."
    elif fat is not None and fat >= 28 and not fat_in_l1:
        l2 = "רוב הקלוריות כאן מגיעות מהשומן."
    elif sat is not None and sat >= 7:
        l2 = f"כולל {round(sat)} גרם שומן רווי ל-100 גרם."
    elif sugar is not None and sugar >= 15 and not sweet_in_l1:
        l2 = "הסוכר הוא הסיפור כאן, לא המליחות."
    elif grade in ("A", "B"):
        l2 = "נשאר חטיף מעובד, אבל מהפרופילים הסבירים שתמצאו על המדף הזה."
    elif grade == "C":
        l2 = "נתרן וקלוריות במרכז הטווח של המדף, בלי יתרון תזונתי שמושך תשומת לב."
    else:
        l2 = "פרופיל עתיר שומן, נתרן או סוכר, בלי צד מאזן."

    return l1 + "\n" + l2


def bottom_line(grade, sig):
    """Descriptive close, no prescription. Spec §4."""
    if grade in ("A", "B"):
        return ("מהטובים שתמצאו על המדף הזה, וזה עדיין חטיף מעובד. "
                "\"הכי טוב\" כאן לא אומר \"מצוין\".")
    if grade == "C":
        return "חטיף סביר בלי יתרון תזונתי בולט. נמצא בדיוק במרכז המדף."
    return "מהחלשים במדף: פרופיל עתיר שומן, נתרן או סוכר, בלי צד מאזן."


def confidence_fields(trace):
    """TASK-233B DA-007: confidence (state + canonical 7-state label/tooltip + sub_reason)
    is derived from the BSIP2 trace via the shared core, NOT a bespoke has_ing flag that
    mapped to verified without requiring a full panel. The core guarantees the canonical
    tooltip set and never the retired 'official food source' overclaim. `confidenceLabel`
    (the expansion badge) reuses the core-derived Hebrew label so the row and expansion agree.
    """
    f = FC.confidence_from_trace(trace)
    return {
        "confidence": f["confidence"],
        "confidenceLabel": f["confidence_label_he"],
        "confidence_label_he": f["confidence_label_he"],
        "confidence_tooltip_he": f["confidence_tooltip_he"],
        "confidence_sub_reason": f["confidence_sub_reason"],
    }


def main():
    b1 = load_bsip1()
    traces = load_traces()
    existing_d4 = load_existing_d4()
    products = []
    skipped = {}
    dropped = []
    basis_excluded = []

    for t in traces:
        ref = t.get("input_reference") or {}
        pid = ref.get("canonical_product_id") or t.get("canonical_product_id") or ""
        score = t.get("final_score_estimate")
        if score is None or t.get("data_sufficiency") == "insufficient":
            skipped[pid] = "insufficient"; continue
        if pid in DROP_IDS:
            dropped.append(pid); continue
        if pid in BASIS_ERROR_EXCLUDE:          # TASK-234 RT-5: unrecoverable per-100g basis
            basis_excluded.append(pid); continue

        rec1 = b1.get(pid, {})
        sig = t.get("L1_observed_signals") or {}
        # DA-009: derive grade from the ROUNDED score that actually ships (and that
        # corpus.ts re-derives from), not the raw float — else a 64.8 rounds to 65 on
        # disk but the disk grade computed from 64.8 says C while runtime says B.
        score_int = FC.round_score(score)
        grade = grade_from_score(score_int)
        nova = t.get("nova_proxy")
        barcode = rec1.get("barcode") or ""

        name = rec1.get("canonical_name_he") or ref.get("product_name_he") or ""
        brand = canonical_brand(rec1.get("brand"), barcode)
        retailer = (rec1.get("source_retailers") or ["yochananof"])[0]

        nutrition = {
            "energyKcal": sig.get("energy_kcal"),
            "protein": sig.get("protein_g"),
            "fat": sig.get("fat_g"),
            "carbs": sig.get("carbohydrates_g"),
            "fiber": sig.get("dietary_fiber_g"),
            "sodium": sig.get("sodium_mg"),
            "sugar": sig.get("sugars_g"),
            "saturatedFat": sig.get("fat_saturated_g"),
        }
        sodium_unavailable = sig.get("sodium_mg") is None

        # Ingredients: omit garbled/English -> panel-only; never ship non-Hebrew
        raw_ing = rec1.get("ingredients_text_he") or ""
        omit_ing = barcode in INGREDIENTS_OMIT
        ingredients = "" if omit_ing else clean_ingredient_text(raw_ing)
        # panel-only if ingredients omitted OR bsip1 didn't have clean ingredients
        has_ing = (rec1.get("ingredient_text_quality") == "clean") and not omit_ing

        # ── TASK-234 (RT-7): internal consistency of novaGroup / ingredientCount /
        # ingredient text. The engine ALWAYS infers a NOVA level (proxy), but for
        # panel-only products it does so WITHOUT a visible ingredient list
        # (nova_confidence: low). Publishing a composition-derived NOVA badge next to
        # ingredientCount=0 / ingredients="" is internally contradictory (the exact RT-7
        # finding: the beet cracker 7290112968807 showed NOVA-3 with 0 ingredients while
        # its own BSIP1 record carried a 15-item list + raw OFF NOVA-4). Rule: publish
        # novaGroup ONLY when the consumer can see the composition it summarizes
        # (ingredientCount > 0). Otherwise suppress to null with an explicit reason, so
        # all three fields agree on "composition not shown". Display-only; the engine's
        # internal scoring NOVA is unchanged, so no score moves.
        ingredient_count_pub = 0 if omit_ing else (rec1.get("ingredient_count") or 0)
        nova_pub = nova if ingredient_count_pub > 0 else None
        nova_suppressed_reason = None if nova_pub is not None else (
            "ingredients_unavailable" if not has_ing else None)

        pos = positive_signals(sig)
        lim_text = limiting_signals(sig, nova)
        insight = build_insight(score, grade, sig)
        conf_fields = confidence_fields(t)

        # row-chip limitingFactors tokens (internal enums, not consumer prose)
        lim_tokens = []
        for c in (t.get("caps_applied") or []):
            r = c.get("rule", "")
            if "SODIUM" in r: lim_tokens.append("sodium")
            elif "SUGAR" in r: lim_tokens.append("sugar")
            elif "NOVA" in r: lim_tokens.append("processing")
            elif "SAT" in r: lim_tokens.append("saturated_fat")
        for p in (t.get("penalties_applied") or []):
            r = p.get("rule", "")
            if "SEED_OIL" in r: lim_tokens.append("seed_oil")
            elif "FAT" in r: lim_tokens.append("fat")
        lim_tokens = list(dict.fromkeys(lim_tokens))[:4]

        record = {
            "id": pid,
            "name": name,
            "brand": brand,
            # Real scraped Yochananof catalog image; never a synthesized prefix.
            "imageUrl": FC.select_image_url(rec1) or "",
            "score": FC.round_score(score),
            "grade": grade,
            "insightLine": insight,
            "confidence": conf_fields["confidence"],
            "subPool": rec1.get("sub_pool") or "chips",
            "novaGroup": nova_pub,
            "retailer": retailer,
            "retailer_he": retailer_he(retailer),
            "limitingFactors": lim_tokens,
            "ingredientCount": ingredient_count_pub,
            "expansion": {
                "nutrition": nutrition,
                "sodiumUnavailable": sodium_unavailable,
                "ingredients": ingredients,
                "confidenceLabel": conf_fields["confidenceLabel"],
                "servingNote": "ל-100 גרם",
                "positiveSignals": pos,
                "limitingFactors": lim_text,
                "bottomLine": bottom_line(grade, sig),
                "comparisonContext": "",
            },
            "provenance": "bsip0_yochananof_real_scrape + off_panel",
            "barcode": barcode,
            "source_traceability_status": "resolved" if has_ing else "panel_only",
            "confidence_label_he": conf_fields["confidence_label_he"],
            "confidence_tooltip_he": conf_fields["confidence_tooltip_he"],
            "confidence_sub_reason": conf_fields["confidence_sub_reason"],
            "nova_suppressed_reason": nova_suppressed_reason,  # TASK-234 RT-7
        }
        if sodium_unavailable:
            record["sodium_note_he"] = "ערך הנתרן לא דווח במקור עבור מוצר זה."
        # preserve d4_additives wired by wire_d4_salty_snacks_v4.py
        if barcode in existing_d4:
            record["d4_additives"] = existing_d4[barcode]
        products.append(record)

    products.sort(key=lambda p: -(p.get("score") or 0))

    # ── HARD GATE: every consumer string must pass is_clean (no framework / score /
    #    recommendation leak), and no raw multi-decimal numbers as text. ──
    leak_failures = []
    decimal_failures = []
    import re
    raw_dec = re.compile(r"\d+\.\d{2,}")  # any 2+ decimal place number printed as text
    for p in products:
        strings = {
            "insightLine": p["insightLine"],
            "bottomLine": p["expansion"]["bottomLine"],
            "confidence_label_he": p["confidence_label_he"],
            "confidence_tooltip_he": p["confidence_tooltip_he"],
            "confidenceLabel": p["expansion"]["confidenceLabel"],
        }
        for i, s in enumerate(p["expansion"]["positiveSignals"]):
            strings[f"positiveSignals[{i}]"] = s
        for i, s in enumerate(p["expansion"]["limitingFactors"]):
            strings[f"limitingFactors[{i}]"] = s
        if p.get("sodium_note_he"):
            strings["sodium_note_he"] = p["sodium_note_he"]
        for key, s in strings.items():
            rep = hr.analyze(s)
            if not rep.is_clean:
                leak_failures.append((p["id"], key, s, [l.kind + ":" + l.term for l in rep.leaks
                                                        if l.kind != "english"]))
            if raw_dec.search(s):
                decimal_failures.append((p["id"], key, s))

    # ── HARD GATE: confidence-label ↔ ingredient consistency (TASK-232 gap, 2026-06-10).
    #    A product with NO ingredient list must NOT claim full/verified ("based on the
    #    ingredient list") — that ships a false provenance claim. It must read panel-only. ──
    confidence_failures = []
    for p in products:
        ing = (p["expansion"].get("ingredients") or "").strip()
        label = (p.get("confidence_label_he") or "") + " " + \
                (p.get("confidence_tooltip_he") or "") + " " + \
                (p["expansion"].get("confidenceLabel") or "")
        claims_full = (p.get("confidence") == "verified") or \
                      ("מלאים" in label) or ("רשימת הרכיבים" in label and "לא הי" not in label)
        if claims_full and not ing:
            confidence_failures.append((p["id"], p.get("confidence"), p.get("confidence_label_he")))

    if leak_failures or decimal_failures or confidence_failures:
        print("!!! GATE FAILURES !!!")
        for f in leak_failures:
            print("  LEAK", f)
        for f in decimal_failures:
            print("  RAW DECIMAL", f)
        for f in confidence_failures:
            print("  CONFIDENCE/INGREDIENT MISMATCH (full-data label, no ingredients)", f)
        sys.exit(1)
    print(f"GATE PASS: all consumer strings clean across {len(products)} products "
          f"(no framework/score/recommendation leaks, no raw decimals).")

    grade_dist = dict(Counter(p["grade"] for p in products))
    subpool_dist = dict(Counter(p["subPool"] for p in products))
    nova_dist = dict(Counter(str(p["novaGroup"]) for p in products))
    retailer_dist = dict(Counter(p["retailer"] for p in products))
    ing_cov = sum(1 for p in products if p["source_traceability_status"] == "resolved")
    sodium_unavail_ids = [p["id"] for p in products if p["expansion"].get("sodiumUnavailable")]

    # ── TASK-233B emission strip (DA-012): keep only BariProductVM keys + barcode/retailer
    #    + d4_additives + the load-bearing `subPool` (salty shelf filters read it off the
    #    runtime VM). Drops source_traceability_status, novaGroup, ingredientCount, brand,
    #    retailer_he, provenance, sodiumUnavailable, sodium_note_he and other non-VM keys.
    #    Internal fields used for the _meta report above are already captured. ──
    products = [FC.strip_non_vm_fields(p, keep={"subPool"}) for p in products]

    output = {
        "_meta": {
            "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "category": "salty-snacks",
            "category_he": "חטיפים מלוחים",
            "run_id": "run_salty_snacks_002",
            "product_count": len(products),
            "scored_count": len(products),
            "schema": "BariProductVM[]",
            "version": "v4",
            "change_note": (
                "v4 REAL rebuild (TASK-228) + TASK-231 remediation (TASK-230 copy spec). "
                "Corpus from real Yochananof catalog (real EAN + real image URL, HTTP-200) + "
                "OFF panels by EAN (EDPG candidate->verified via BSIP0/QA). Engine unchanged "
                "(engine-baseline-2026-06-04 + TASK-216). TASK-231: copy de-leaked "
                "(no NOVA/score/recommendation strings, no raw decimals; is_clean gate enforced); "
                "Bamba clutter cut 8->2; brand field normalized; garbled/English ingredients "
                "omitted+panel-only; 3 null-sodium snacks marked honestly; novaGroup<->copy "
                "contradiction removed; beet-cracker (7290112968807) trans corrected "
                "(OFF serving-scaling artifact) and re-scored 0/E -> 60/C."
            ),
            "sub_pools": ["chips", "popcorn", "puffed", "baked", "rice_cakes", "pretzels"],
            "provenance": (
                "TASK-228 real rebuild + TASK-231 remediation. Identity+image: Yochananof "
                "catalog (real EAN). Panel: Open Food Facts by real EAN. "
                f"Corpus: {len(products)} products (6 Bamba variants curated out). "
                f"Ingredient coverage: {ing_cov}/{len(products)}. "
                f"Grade dist: {grade_dist}. NOVA dist: {nova_dist}."
            ),
            "grade_distribution": grade_dist,
            "subpool_distribution": subpool_dist,
            "nova_distribution": nova_dist,
            "retailer_breakdown": retailer_dist,
            "ingredient_coverage": f"{ing_cov}/{len(products)}",
            "task231_remediation": {
                "bamba_dropped": sorted(DROP_IDS),
                "ingredients_omitted_panel_only": sorted(INGREDIENTS_OMIT - DROP_IDS),
                "sodium_unavailable_marked": sodium_unavail_ids,
                "beet_cracker_trans_corrected": "7290112968807: 0/E -> 60/C "
                                                "(OFF trans 2.33g/100g was serving-scaling artifact)",
                "apropo_caramel_trans_corrected": "7290118421603: 0/E -> 18/E "
                                                  "(OFF trans 1.25g/100g was the same serving-scaling "
                                                  "artifact: 0.5g '<1g' declaration / 0.40 serving; TASK-229)",
            },
            "task234_remediation": {
                "trans_artifact_neutralized_corpus_wide": [
                    "7290000066318 (Bamba 0.625->0)", "7290104500572 (Apropo Italiano 0.6->0)",
                    "7290000420325 (Pop Star 0.4->0)", "7290004943738 (Milotal 0.5->0)",
                    "5701932026971 (Hot Pop 0.5->0)", "7290117035009 (Yoh popcorn 0.5->0)",
                    "7290018198254 (Tapugan 0.5->0)", "7290110551926 (Tapuchips bt 0.5->0)",
                    "4011800528416 (Corny 0.5->0)",
                ],
                "trans_artifact_note": ("OFF trans-fat_serving=0.5g is the Israeli '<1g' threshold "
                                        "DECLARATION; scaled by serving fraction it yields phantom "
                                        "per-100g values (0.4/0.6/0.625/1.25/2.33). Neutralized to 0.0 "
                                        "where no PHVO marker present (authoritative OFF serving-level "
                                        "re-probe). Engine unchanged."),
                "fiber_omitted": "7290112494313 (Click cornflakes): fiber 38g/100g impossible "
                                 "(fiber+sugars>carbs); set None. Re-scored 25/E -> 14/E.",
                "basis_error_excluded": sorted(BASIS_ERROR_EXCLUDE),
                "basis_error_note": ("7290018198254/7290018198148/7290004943738: whole-panel "
                                     "per-serving basis mislabeled per-100g (128/139/145 kcal vs real "
                                     "~450-540); unrecoverable (no serving_size) -> dropped from shelf."),
                "rt7_nova_reconciled": ["4014400925319", "7290000069364", "7290112494313",
                                        "7290112968807", "7290116537375"],
                "rt7_note": ("BSIP1 nova_proxy held the raw OFF nova_group (often 4) while the engine "
                             "infers + publishes its own NOVA; reconciled BSIP1 nova_proxy to the "
                             "engine-inferred value (raw OFF kept as nova_group_off_raw). novaGroup is "
                             "published only when ingredientCount>0 (else null) so novaGroup/"
                             "ingredientCount/ingredients are internally consistent. Score-neutral."),
            },
        },
        "products": products,
    }
    OUT_LOCAL.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_WEB.parent.mkdir(parents=True, exist_ok=True)
    OUT_WEB.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Written: {OUT_LOCAL}")
    print(f"Written: {OUT_WEB}")
    print(f"Products: {len(products)}  grades: {grade_dist}")
    print(f"Dropped Bamba variants: {len(dropped)} -> {dropped}")
    print(f"Basis-error excluded (TASK-234 RT-5): {len(basis_excluded)} -> {basis_excluded}")
    print(f"Ingredient coverage: {ing_cov}/{len(products)}")
    print(f"Skipped insufficient: {len(skipped)} -> {list(skipped)}")


if __name__ == "__main__":
    main()
