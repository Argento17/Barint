path = "C:/Bari/bari-web/src/lib/view-models/index.ts"
with open(path, encoding="utf-8") as f:
    txt = f.read()

# Insert brand field after `name: string;`
old = "  name: string;\n  imageUrl: string | null;"
new = "  name: string;\n  /** Brand / manufacturer display name. Optional; absent on older datasets. */\n  brand?: string | null;\n  imageUrl: string | null;"

if old not in txt:
    print("OLD NOT FOUND")
else:
    txt = txt.replace(old, new, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("patched")
