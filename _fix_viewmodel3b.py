path = "C:/Bari/bari-web/src/lib/view-models/index.ts"
with open(path, encoding="utf-8") as f:
    txt = f.read()

addition = (
    "\n// \u2500\u2500\u2500 Magnesium supplement badges (TASK-384A) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n"
    "// Per-product badge data for the 6-slot expansion grid.\n"
    "// All fields are pre-rendered Hebrew strings from the pipeline.\n"
    "export interface MagnesiumBadgesVM {\n"
    "  elemental_mg_label: string;\n"
    "  form_label: string;\n"
    "  bav_label: string;\n"
    "  suitability_label: string;\n"
    "  label_confidence_label: string;\n"
    "  safety_flags: string[];\n"
    "  compound_transparency?: string | null;\n"
    "}\n"
)

# Find the end of BariProductVM and insert after it
marker = "  valueFlag?: string | null;\n}"
if marker not in txt:
    print("NOT FOUND")
else:
    idx = txt.index(marker) + len(marker)
    txt = txt[:idx] + addition + txt[idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("patched")
