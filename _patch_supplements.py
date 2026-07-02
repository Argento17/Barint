path = "C:/Bari/bari-web/src/app/hashvaot/supplements/page.tsx"
with open(path, encoding="utf-8") as f:
    txt = f.read()
old = "\u05d7\u05d6\u05e8\u05d4 \u05dc\u05d4\u05e9\u05d5\u05d5\u05d0\u05d5\u05ea \u05d4\u05de\u05d6\u05d5\u05df"
new = "\u05d7\u05d6\u05e8\u05d4 \u05dc\u05db\u05dc \u05d4\u05e7\u05d8\u05d2\u05d5\u05e8\u05d9\u05d5\u05ea"
if old not in txt:
    print("OLD NOT FOUND")
else:
    txt = txt.replace(old, new, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("patched")
