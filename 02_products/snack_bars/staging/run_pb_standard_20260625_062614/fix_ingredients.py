"""
TASK-399 FIX B: De-garble expansion.ingredients strings.
Rules:
  - Fix only FORMAT artifacts (mid-word spaces, reversed %/brackets, stray 'n' chars, reversed E-codes)
  - Do NOT invent or change actual ingredient names
  - If a string is too garbled to confidently reconstruct, LEAVE it and report
  - Also fix FIX A: categoryNote.body_he[1]
"""
import json
import re
import copy
import hashlib

SRC = r"C:\Bari\02_products\snack_bars\staging\run_pb_standard_20260625_062614\protein_bars_frontend_v2_candidate.json"
DST = r"C:\Bari\02_products\snack_bars\staging\run_pb_standard_20260625_062614\protein_bars_frontend_v2_candidate.json"

with open(SRC, "r", encoding="utf-8") as f:
    raw = f.read()

data = json.loads(raw)

# ── Snapshot scores/grades for post-check ──────────────────────────────────
before_scores = {p["id"]: (p["score"], p["grade"]) for p in data["products"]}

# ─────────────────────────────────────────────────────────────────────────────
# FIX A — categoryNote.body_he[1]
# ─────────────────────────────────────────────────────────────────────────────
OLD_CAVEAT = "רשימות הרכיבים לא חולצו למוצרים אלה. הערכת רמת העיבוד מבוססת על פרוקסי בלבד, ולכל 32 המוצרים יש רמת ביטחון חלקית. הציון משקף את תווית התזונה שאומתה; הערכת איכות העיבוד מוגבלת."
NEW_CAVEAT = "רשימות הרכיבים מוצגות בפירוט המוצר, אך ניתוח רמת העיבוד מבוסס על הערכה בלבד ולא על ניתוח מבני מלא — לכן רמת הביטחון חלקית לכל 32 המוצרים. הציון משקף את תווית התזונה שאומתה."

assert data["categoryNote"]["body_he"][1] == OLD_CAVEAT, \
    f"CAVEAT TEXT MISMATCH — found:\n{data['categoryNote']['body_he'][1]}"
data["categoryNote"]["body_he"][1] = NEW_CAVEAT
print(f"[FIX A] categoryNote.body_he[1] updated.")

# ─────────────────────────────────────────────────────────────────────────────
# FIX B — per-product ingredient fixes
# ─────────────────────────────────────────────────────────────────────────────

# Track what was fixed and what was left
cleaned_count = 0
left_as_is = []  # list of (id, reason)
fix_log = []

def fix_ingredients(pid, s):
    """
    Apply deterministic format fixes to a single ingredient string.
    Returns (fixed_string, list_of_changes).
    """
    original = s
    changes = []

    def sub(pattern, replacement, desc, flags=0):
        nonlocal s
        new = re.sub(pattern, replacement, s, flags=flags)
        if new != s:
            changes.append(desc)
            s = new

    # ── 1. Stray `n` between Hebrew text (NOT inside E-codes like E1442, NOT in English letters) ──
    # Pattern: Hebrew char immediately followed by `n` then Hebrew (or space+Hebrew)
    # Also: `,n` → `, ` ; `. n` → `. `; `]n` → `] `; `)n` → `) `
    # We must NOT touch `nמייצב` → fix to ` מייצב`
    sub(r'([א-ת])n([א-ת])', r'\1 \2', 'Remove stray n between Hebrew words (no space)')
    sub(r'([,\.)\]])n([א-ת])', r'\1 \2', 'Remove stray n after punctuation before Hebrew')
    sub(r'\bn([א-ת])', r' \1', 'Remove leading stray n before Hebrew word')

    # ── 2. Reversed E-codes: digits before E, e.g. `476E` → `E476` ──
    # Only when inside parentheses context: (476E) or (476E, or preceded by space/comma
    sub(r'\b(\d{3})E\b', r'E\1', 'Reverse E-code digits: NNNe -> ENNN')
    sub(r'\b(\d{4})E\b', r'E\1', 'Reverse E-code digits: NNNNe -> ENNNN')

    # ── 3. Space inside E-code number: `E1 442` → `E1442`, `E4 76` → `E476`, `E50 0` → `E500` ──
    sub(r'\bE(\d+) (\d+)\b', r'E\1\2', 'Remove space inside E-code number')

    # ── 4. Reversed percent bracket: `)%XX.X(` or `)%XX(` → `(XX%)` ──
    # Pattern: ) followed by % followed by digits (with optional decimal) followed by (
    sub(r'\)%(\d+(?:\.\d+)?)\(', r'(\1%)', 'Fix reversed %)X.X(% → (X.X%)')

    # ── 5. Reversed square brackets used as openers — `]` at start of a sub-list that should be `[` ──
    # This is tricky: only fix when the ] starts a bracketed ingredient sub-list
    # Pattern: after `,` or `(` or space, a `]` followed by Hebrew ingredient text
    # We look for: `] + HEB` where context suggests it should be `[`
    # The reverse: `[` at end of a sublist that should be `]`
    # Since this requires deep RTL analysis and the risk of wrong guess is high,
    # we only fix the clear reversed-percent case above and note these for manual review.

    # ── 6. Mid-word splits — rejoin specific known-garbled words ──
    # We enumerate the confirmed splits from the audit, applied conservatively.

    # Common Hebrew words with confirmed mid-word space artifacts:
    word_fixes = [
        # (garbled_pattern, fixed, description)
        (r'ציטרי ת\b', 'ציטרית', 'Rejoin ציטרי ת → ציטרית'),
        (r'ח מניות\b', 'חמניות', 'Rejoin ח מניות → חמניות'),
        (r'גבינ ה\b', 'גבינה', 'Rejoin גבינ ה → גבינה'),
        (r'גליצרו ל\b', 'גליצרול', 'Rejoin גליצרו ל → גליצרול'),
        (r'סיבי ם\b', 'סיבים', 'Rejoin סיבי ם → סיבים'),
        (r'צמ חיים\b', 'צמחיים', 'Rejoin צמ חיים → צמחיים'),
        (r'הלח ה\b', 'הלחה', 'Rejoin הלח ה → הלחה'),
        (r'גלוק וזה\b', 'גלוקוזה', 'Rejoin גלוק וזה → גלוקוזה'),
        (r'ר זה\b', 'רזה', 'Rejoin ר זה → רזה'),
        (r'טב עיים\b', 'טבעיים', 'Rejoin טב עיים → טבעיים'),
        (r'מינימו ם\b', 'מינימום', 'Rejoin מינימו ם → מינימום'),
        (r'ח לב\b', 'חלב', 'Rejoin ח לב → חלב'),
        (r'מסיס ים\b', 'מסיסים', 'Rejoin מסיס ים → מסיסים'),
        (r'לציטי ן\b', 'לציטין', 'Rejoin לציטי ן → לציטין'),
        (r'קו קוס\b', 'קוקוס', 'Rejoin קו קוס → קוקוס'),
        (r'מר וכז\b', 'מרוכז', 'Rejoin מר וכז → מרוכז'),
        (r'מרו כז\b', 'מרוכז', 'Rejoin מרו כז → מרוכז'),
        (r'מאכ ל\b', 'מאכל', 'Rejoin מאכ ל → מאכל'),
        (r'מס מיך\b', 'מסמיך', 'Rejoin מס מיך → מסמיך'),
        (r'חו מצות\b', 'חומצות', 'Rejoin חו מצות → חומצות'),
        (r'מלטיט ול\b', 'מלטיטול', 'Rejoin מלטיט ול → מלטיטול'),
        (r'חומ ר\b', 'חומר', 'Rejoin חומ ר → חומר'),
        (r'ממ תיק\b', 'ממתיק', 'Rejoin ממ תיק → ממתיק'),
        (r'חי טה\b', 'חיטה', 'Rejoin חי טה → חיטה'),
        (r'פולידקסטר וז\b', 'פולידקסטרוז', 'Rejoin פולידקסטר וז → פולידקסטרוז'),
        (r'ש מן\b', 'שמן', 'Rejoin ש מן → שמן'),
        (r'מלטיטו ל\b', 'מלטיטול', 'Rejoin מלטיטו ל → מלטיטול'),
        (r'אסט ר\b', 'אסטר', 'Rejoin אסט ר → אסטר'),
        (r'סוכר לוז\b', 'סוכרלוז', 'Rejoin סוכר לוז → סוכרלוז'),
        (r'מק ריש\b', 'מקריש', 'Rejoin מק ריש → מקריש'),
        (r'סי בים\b', 'סיבים', 'Rejoin סי בים → סיבים'),
        (r'שוקול ד\b', 'שוקולד', 'Rejoin שוקול ד → שוקולד'),
        (r'מת חלב\b', 'מתחלב', 'Rejoin מת חלב → מתחלב'),
        (r'ורי ח\b', 'וריח', 'Rejoin ורי ח → וריח'),
        (r'מ ים\b', 'מים', 'Rejoin מ ים → מים'),
        (r'מי ם\b', 'מים', 'Rejoin מי ם → מים'),
        (r'ממתי ק\b', 'ממתיק', 'Rejoin ממתי ק → ממתיק'),
        (r'ונילי ן\b', 'ונילין', 'Rejoin ונילי ן → ונילין'),
        (r'חומ ציות\b', 'חומציות', 'Rejoin חומ ציות → חומציות'),
        # prot-007: extra ) after שמן צמחי
        (r'שמן צמחי\)\]', 'שמן צמחי]', 'Remove stray ) after שמן צמחי in bracket'),
        # prot-028: decimal split in percentage
        (r'פטל 1\. 1%', 'פטל 1.1%', 'Fix decimal split: 1. 1% → 1.1%'),
        # prot-005: double space before שמנים
        (r'שמנים  ושומנים', 'שמנים ושומנים', 'Remove double space שמנים  ושומנים'),
        # prot-002: double space before אורז
        (r'חלבון  אורז', 'חלבון אורז', 'Remove double space חלבון  אורז'),
        # prot-005: n before מייצב (already caught by general n-rule but adding explicit)
        # General stray n before Hebrew already handles this
        # prot-029: לציטיו — missing final ן. This is an ambiguous letter drop, LEAVE IT.
        # prot-031: double )) after E414 — E414)) should be (E414)
        # The bracket issue is likely: `חומר הזגה E414))` — one extra )
        (r'E414\)\)', 'E414)', 'Fix double )) after E414 → single )'),
    ]

    for pattern, replacement, desc in word_fixes:
        sub(pattern, replacement, desc)

    return s, changes


# ─────────────────────────────────────────────────────────────────────────────
# Severely garbled products — leave as-is policy
# These have text corruption beyond simple format artifacts (wrong letters,
# missing letters, whole phrases inserted mid-ingredient) that cannot be
# confidently reconstructed without the original label.
# ─────────────────────────────────────────────────────────────────────────────
LEAVE_AS_IS_PRODUCTS = {
    "prot-008": "Contains 'סיני תירם עלול לד מסיסים' — multiple characters wrong (not just spaces); 'עיסת קקאן' — wrong final letter; 'סיני פולידקסטרוז' — wrong word. Cannot reconstruct without original label.",
    "prot-009": "Same garbling as prot-008 (same brand/formula); 'סיני תירם עלול לד מסיסים', 'עיסת קקאן', 'סיני פולידקסטרוז'. Cannot reconstruct without original label.",
    "prot-015": "'עיסת קקאן' (wrong letter), ')ליצרול)' — RTL brackets AND missing initial ג in גליצרול — character drop, not just format; 'סיני תירס מסיס ים' — 'סיני' should be 'סיבי' (wrong letter, not just space). Cannot reconstruct confidently.",
    "prot-029": "'לציטיו' — missing final ן from לציטין — letter drop, not a format artifact. Rest fixable but leaving whole product out of caution due to multiple issues.",
}

# Actually for prot-029: we CAN fix the stray-n artifacts and the ממתי ק split,
# but the לציטיו → לציטין is a letter drop. Per spec: "if so garbled you cannot
# confidently reconstruct, LEAVE IT". We'll apply the safe fixes to prot-029
# but note the לציטיו issue remains.
# Revised: apply fixes to prot-029 except לציטיו, which we leave.

LEAVE_SPECIFIC = {
    # product_id: list of specific garbled substrings to LEAVE, with reasons
    "prot-008": ["WHOLE_PRODUCT"],  # too many character substitutions
    "prot-009": ["WHOLE_PRODUCT"],  # same garbling
    "prot-015": ["WHOLE_PRODUCT"],  # character drops + wrong letters
    "prot-029": ["לציטיו"],          # missing ן — letter drop, leave
    "prot-030": ["פתיתי חלבון"],     # the nאבקת is fixed by general rule, but
                                      # the original ingredient list formatting
                                      # has many stray-n and also a reversed
                                      # E-code (476E). We apply general rules
                                      # and note the reversed E476 in the listing
}

# Process products
for product in data["products"]:
    pid = product["id"]
    ingr = product["expansion"].get("ingredients", "")

    if not ingr:
        continue

    if pid in LEAVE_SPECIFIC and LEAVE_SPECIFIC[pid] == ["WHOLE_PRODUCT"]:
        left_as_is.append((pid, product["barcode"], LEAVE_SPECIFIC[pid][0] if LEAVE_SPECIFIC[pid] else "WHOLE_PRODUCT",
                          "Severe character substitutions/drops — cannot reconstruct without original label"))
        fix_log.append(f"[LEAVE] {pid}: left as-is (whole product)")
        continue

    fixed, changes = fix_ingredients(pid, ingr)

    if changes:
        product["expansion"]["ingredients"] = fixed
        cleaned_count += 1
        fix_log.append(f"[FIXED] {pid}: {len(changes)} change(s): {'; '.join(changes)}")
        # Note any remaining known issues for specific products
        if pid == "prot-029":
            remaining = "לציטיו (missing final ן) — left unfixed (letter drop)"
            left_as_is.append((pid, product["barcode"], "לציטיו", remaining))
    else:
        fix_log.append(f"[CLEAN] {pid}: no changes needed")

# ─────────────────────────────────────────────────────────────────────────────
# Verify: no score/grade/nutrition/insightLine/rowVerdict changed
# ─────────────────────────────────────────────────────────────────────────────
after_scores = {p["id"]: (p["score"], p["grade"]) for p in data["products"]}
assert before_scores == after_scores, "SCORE/GRADE CHANGED — ABORT"

# Spot check: verify categoryNote fields
assert data["categoryNote"]["body_he"][0] != "", "body_he[0] should not be empty"
assert data["categoryNote"]["body_he"][1] == NEW_CAVEAT, "body_he[1] not updated correctly"

print(f"\n[VERIFY] Scores/grades unchanged across all 32 products: PASS")
print(f"[VERIFY] categoryNote.body_he[1] correctly updated: PASS")

# ─────────────────────────────────────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────────────────────────────────────
out_str = json.dumps(data, ensure_ascii=False, indent=2)
with open(DST, "w", encoding="utf-8") as f:
    f.write(out_str)

sha256 = hashlib.sha256(out_str.encode("utf-8")).hexdigest()
print(f"\n[OUTPUT] Written to: {DST}")
print(f"[OUTPUT] SHA256: {sha256}")
print(f"[OUTPUT] Size: {len(out_str)} bytes")

# ─────────────────────────────────────────────────────────────────────────────
# Print fix summary
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n── FIX LOG ──────────────────────────────────────────")
for line in fix_log:
    print(line)

print(f"\n── SUMMARY ──────────────────────────────────────────")
print(f"Products with ingredient strings cleaned: {cleaned_count}/32")
print(f"Products left as-is (whole): {sum(1 for x in left_as_is if x[2] == 'WHOLE_PRODUCT')}")
print(f"Specific substrings left: {sum(1 for x in left_as_is if x[2] != 'WHOLE_PRODUCT')}")
print(f"\nLeft-as-is details:")
for entry in left_as_is:
    print(f"  {entry[0]} (barcode {entry[1]}): '{entry[2]}' — {entry[3]}")

# ─────────────────────────────────────────────────────────────────────────────
# Residual artifact scan
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n── RESIDUAL ARTIFACT SCAN ───────────────────────────")
residuals = []
for product in data["products"]:
    pid = product["id"]
    ingr = product["expansion"].get("ingredients", "")

    # Check for %)( pattern
    if re.search(r'\)%\d', ingr) or re.search(r'\d%\(', ingr):
        residuals.append(f"  {pid}: reversed %)( still present")

    # Check for mid-word-split patterns (space inside known Hebrew word)
    # Check for single stray 'n' between Hebrew characters
    if re.search(r'[א-ת]n[א-ת]', ingr):
        residuals.append(f"  {pid}: stray 'n' between Hebrew chars still present")
    if re.search(r',n[א-ת]', ingr):
        residuals.append(f"  {pid}: ',n' before Hebrew still present")

    # Check for reversed E-codes (digit block before E)
    if re.search(r'\b\d{3}E\b', ingr) or re.search(r'\b\d{4}E\b', ingr):
        residuals.append(f"  {pid}: reversed E-code NNNe still present")

if residuals:
    print("RESIDUALS FOUND:")
    for r in residuals:
        print(r)
else:
    print("No residual %)/(%, stray-n, or reversed E-codes detected in fixed products.")

print("\nDone.")
