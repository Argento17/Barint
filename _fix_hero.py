from pathlib import Path
p = Path(r"c:\Bari\bari-web\src\components\home\home-hero.tsx")
t = p.read_text(encoding="utf-8")
t = t.replace('className="py-[62px_0_48px]"', 'className="hero-v5-grid py-14 md:py-[62px]"')
t = t.replace("            gridTemplateAreas: \"'visual copy'\",", "            gridTemplateAreas: \"'copy' 'visual'\",\n            // md+ flips to visual | copy via CSS below")
# fix - better use responsive approach with class
