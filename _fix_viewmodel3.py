path = "C:/Bari/bari-web/src/lib/view-models/index.ts"
with open(path, encoding="utf-8") as f:
    txt = f.read()

# Add MagnesiumBadgesVM type after the BariProductVM interface
addition = """
// --- Magnesium supplement badges (TASK-384A) ---------------------------------
// Per-product badge data for the 6-slot expansion grid.
// All fields are pre-rendered Hebrew strings from the pipeline.
export interface MagnesiumBadgesVM {
  elemental_mg_label: string;
  form_label: string;
  bav_label: string;
  suitability_label: string;
  label_confidence_label: string;
  safety_flags: string[];
  compound_transparency?: string | null;
}
"""

# Insert after closing brace of BariProductVM
insert_after = "}\n\n// --- Filter ---"
if insert_after not in txt:
    print("NOT FOUND")
else:
    txt = txt.replace(insert_after, "}\n" + addition + "\n// --- Filter ---", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("patched")
