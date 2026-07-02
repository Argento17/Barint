from pathlib import Path
p = Path(r"c:\Bari\bari-web\src\components\home\home-hero.tsx")
t = p.read_text(encoding="utf-8")
old = '        <div\n          className="py-[62px_0_48px]"'
new = '        <div\n          className="hero-v5-grid py-14 md:py-[62px]"'
if old in t:
    t = t.replace(old, new)
else:
    t = t.replace('className="py-[62px_0_48px]"', 'className="hero-v5-grid py-14 md:py-[62px]"')
p.write_text(t, encoding="utf-8")
print("fixed")
