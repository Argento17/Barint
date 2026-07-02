"""
Leakage scan + voice/coherence checks on protein_bars copy.
"""
import json, io, sys, re

out = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('C:/Bari/bari-web/src/data/comparisons/protein_bars_frontend_v1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['products']

# Collect all copy text per product
def get_copy_texts(p):
    texts = []
    texts.append(('insightLine', p.get('insightLine', '')))
    texts.append(('rowVerdict', p.get('rowVerdict', '')))
    exp = p.get('expansion', {})
    texts.append(('comparisonContext', exp.get('comparisonContext', '')))
    for i, s in enumerate(exp.get('positiveSignals', [])):
        texts.append(('positiveSignals[' + str(i) + ']', s))
    for i, lf in enumerate(exp.get('limitingFactors', [])):
        texts.append(('limitingFactors[' + str(i) + ']', lf.get('text', '')))
    return texts

# --- LEAKAGE PATTERNS ---
LEAKAGE_PATTERNS = [
    # Framework internals
    r'\bNOVA\b',
    r'\bBSIP\b',
    r'structural_class',
    r'matrix_integrity',
    r'pillar',
    r'dimension',
    r'snack_bar_granola',
    r'whole_food_fat',
    r'prot-\d+',
    r'\bnull\b',
    # Score mechanics
    r'\b\d{2}\.\d/[A-E]\b',  # raw score like 71.5/B
    # E-codes
    r'\bE\d{3,4}\b',
    r'\bE[0-9]{3}[a-z]?\b',
    # OFF reference
    r'Open Food Facts',
    r'\bOFF\b',
]

out.write("====== LEAKAGE SCAN ======\n\n")
leakage_found = False
for p in products:
    pid = p['id']
    for field, text in get_copy_texts(p):
        for pat in LEAKAGE_PATTERNS:
            matches = re.findall(pat, text, re.IGNORECASE)
            if matches:
                out.write("LEAKAGE " + pid + " | " + field + " | pattern=" + pat + " match=" + str(matches) + "\n")
                out.write("  TEXT: " + text[:120] + "\n")
                leakage_found = True

if not leakage_found:
    out.write("No leakage patterns found - PASS\n")

out.write("\n====== MARKETING ECHO SCAN ======\n")
out.write("(Looking for brand claims presented as Bari findings)\n\n")
MARKETING_ECHO = [
    "עשיר בחלבון",
    "אנרגיה",
    "טבעי",
    "בריאותי",
    "בריאות",
    "מומלץ",
    "פרמיום",
    "איכות",
]
for p in products:
    pid = p['id']
    for field, text in get_copy_texts(p):
        for phrase in MARKETING_ECHO:
            if phrase in text:
                out.write("ECHO " + pid + " | " + field + " | phrase: " + phrase + "\n")
                out.write("  TEXT: " + text[:120] + "\n")

out.write("\n====== REPEATED PHRASE SCAN ======\n")
out.write("(Signature phrases used >2x across 16 products)\n\n")
# Collect all insightLines and rowVerdicts
insight_lines = [p.get('insightLine', '') for p in products]
row_verdicts = [p.get('rowVerdict', '') for p in products]

# Common clause starters/enders to detect signature phrase repetition
PHRASES_TO_CHECK = [
    "תוסף חלבון",
    "תוסף חלבון נוח",
    "ממזון שלם",
    "תערובת מבודדים",
    "תחליפי מתיקות",
    "לא מזון שלם",
    "לא מהפחתה אמיתית",
    "מהפחתה אמיתית",
    "בסיס תערובת חלבונים",
    "הבסיס תערובת",
    "אותו מתכון",
    "רחוק ממזון",
    "לא נשנוש",
    "מבודדים בלבד",
    "מחומר מילוי",
    "ממזון",
    "ממתק",
]

all_copy_flat = []
for p in products:
    for field, text in get_copy_texts(p):
        all_copy_flat.append(text)

all_copy_combined = ' '.join(all_copy_flat)

for phrase in PHRASES_TO_CHECK:
    count = all_copy_combined.count(phrase)
    if count > 4:
        out.write("REPEATED(x" + str(count) + "): " + phrase + "\n")
    elif count > 2:
        out.write("NOTABLE(x" + str(count) + "): " + phrase + "\n")

out.write("\n====== NULL FIBER CHECK (prot-014, prot-015, prot-016) ======\n")
for p in products:
    pid = p['id']
    n = p.get('nutrition_per_100g', {})
    fiber = n.get('dietary_fiber_g')
    exp = p.get('expansion', {})
    exp_fiber = exp.get('nutrition', {}).get('fiber')
    if fiber is None or fiber == 0.0:
        out.write(pid + ": nutrition fiber=" + str(fiber) + " expansion.nutrition.fiber=" + str(exp_fiber) + "\n")
        # Check if copy mentions fiber for these products
        for field, text in get_copy_texts(p):
            if "סיב" in text:
                out.write("  COPY MENTIONS FIBER in " + field + ": " + text[:100] + "\n")

out.write("\n====== RECITATION vs VERDICT CHECK ======\n")
out.write("(insightLine: does it translate or just list?)\n\n")
# Check if insightLine is just a nutrient list with no interpretive framing
for p in products:
    pid = p['id']
    il = p.get('insightLine', '')
    # Signs of recitation: starts with a number, ends with a number, no evaluative language
    starts_with_num = bool(re.match(r'^\d', il))
    has_evaluative = any(w in il for w in [
        "ממתק", "מעבדה", "מהונדס", "אמיתי", "תוסף", "בעצם", "מה ש",
        "הסיפור", "תעשייתי", "מבטיח", "שנמכר", "מוכר",
    ])
    is_pure_list = starts_with_num and not has_evaluative
    if is_pure_list:
        out.write("POSSIBLE RECITATION " + pid + ": " + il[:120] + "\n")

out.write("\n====== SODIUM DISCIPLINE CHECK ======\n")
out.write("Does sodium lead only when genuinely the single standout?\n\n")
for p in products:
    pid = p['id']
    n = p.get('nutrition_per_100g', {})
    sodium = n.get('sodium_mg', 0)
    il = p.get('insightLine', '')
    # sodium-led: insightLine mentions sodium first or prominently as the lead finding
    if "נתרן" in il[:50]:
        out.write("SODIUM-LED insightLine " + pid + " sodium=" + str(sodium) + "mg: " + il[:120] + "\n")

out.flush()
