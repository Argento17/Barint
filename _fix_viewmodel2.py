path = "C:/Bari/bari-web/src/lib/view-models/index.ts"
with open(path, encoding="utf-8") as f:
    txt = f.read()

# Insert before the closing brace of BariProductVM interface
old = "  bariInterpretation?: Array<\n    | { key: string; label: string; score: number; strength: string; interpretation: string }\n    | { dimension: string; score: number; label_he: string; explanation_he: string }\n  >;\n}"
new = "  bariInterpretation?: Array<\n    | { key: string; label: string; score: number; strength: string; interpretation: string }\n    | { dimension: string; score: number; label_he: string; explanation_he: string }\n  >;\n  /** TASK-384A: short Hebrew badge string for magnesium dose warning. Display-only. */\n  claimShortfallFlag?: string | null;\n  /** TASK-384A: pre-rendered Hebrew pill showing estimated absorbed mg. Display-only. */\n  absorbedMgPill?: string | null;\n  /** TASK-384A: short Hebrew badge string for value-for-money warning. Display-only. */\n  valueFlag?: string | null;\n}"

if old not in txt:
    print("NOT FOUND")
    # Try alternate
    print(repr(txt[txt.index("bariInterpretation"):txt.index("bariInterpretation")+300]))
else:
    txt = txt.replace(old, new, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("patched")
