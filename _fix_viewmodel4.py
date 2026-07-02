path = "C:/Bari/bari-web/src/lib/view-models/index.ts"
with open(path, encoding="utf-8") as f:
    txt = f.read()

# Add magnesiumBadges to BariProductVM (before the closing })
marker = "  valueFlag?: string | null;\n}"
addition_before_close = "  /** TASK-384A: full magnesium badge grid data for the expansion panel. Display-only. */\n  magnesiumBadges?: MagnesiumBadgesVM | null;\n"

if marker not in txt:
    print("NOT FOUND")
else:
    txt = txt.replace(marker, "  " + "valueFlag?: string | null;\n  " + addition_before_close.lstrip() + "}", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("patched")
