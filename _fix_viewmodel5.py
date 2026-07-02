path = "C:/Bari/bari-web/src/lib/view-models/index.ts"
with open(path, encoding="utf-8") as f:
    txt = f.read()

# Add bandNote to BariProductVM 
marker = "  /** TASK-384A: full magnesium badge grid data for the expansion panel. Display-only. */\n  magnesiumBadges?: MagnesiumBadgesVM | null;\n}"
addition = "  /** TASK-384A: optional safety note shown at a band boundary in the expansion. Display-only. */\n  bandNote?: string | null;\n  "

if marker not in txt:
    print("NOT FOUND - dumping area")
    idx = txt.find("magnesiumBadges")
    print(repr(txt[idx-20:idx+200]))
else:
    txt = txt.replace(marker, "  " + addition + "/** TASK-384A: full magnesium badge grid data for the expansion panel. Display-only. */\n  magnesiumBadges?: MagnesiumBadgesVM | null;\n}", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("patched")
