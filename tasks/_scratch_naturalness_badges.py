import re, sys
sys.path.insert(0, r'C:\Bari\integrations\clients')
from naturalness_gate import analyze

files = [
    r'C:\Bari\bari-web\src\components\shared\magnesium-safety-box.tsx',
    r'C:\Bari\bari-web\src\components\shared\magnesium-badge-grid.tsx',
    r'C:\Bari\bari-web\src\lib\comparisons\magnesium-page-data.ts',
]
hebrew = re.compile('[֐-׿]')
seen = set()
high = 0
total = 0
for fp in files:
    src = open(fp, encoding='utf-8').read()
    strings = re.findall(r'"((?:[^"\\]|\\.)*)"', src) + re.findall(r'`([^`]*)`', src)
    for s in strings:
        txt = s.replace('\\"', '"').strip()
        if not hebrew.search(txt):
            continue
        if len(txt) < 20:
            continue
        if txt in seen:
            continue
        seen.add(txt)
        total += 1
        rep = analyze(txt)
        if not rep.is_clean:
            high += 1
            print("HIGH (%d): %s" % (len(rep.high_flags), txt[:95]))

print("\nScanned %d Hebrew strings; %d HIGH." % (total, high))
