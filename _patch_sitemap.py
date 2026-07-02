path = "C:/Bari/bari-web/src/app/sitemap.ts"
with open(path, encoding="utf-8") as f:
    txt = f.read()
old = '  "/hashvaot/supplements",'
new = '  "/hashvaot/supermarket",\n  "/hashvaot/supplements",'
if old not in txt:
    print("OLD NOT FOUND:", repr(old[:60]))
else:
    txt = txt.replace(old, new, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("patched")
