path = "C:/Bari/bari-web/src/components/shared/comparison-row.tsx"
with open(path, encoding="utf-8") as f:
    txt = f.read()

# Remove the unknown magnesiumBadges prop from the ExpansionSection call
old = "                magnesiumBadges={product.magnesiumBadges}\n"
if old in txt:
    txt = txt.replace(old, "", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("removed magnesiumBadges prop")
else:
    print("NOT FOUND")
