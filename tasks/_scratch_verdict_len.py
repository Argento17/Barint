import re
src = open(r'C:\Bari\bari-web\src\lib\comparisons\magnesium-page-data.ts', encoding='utf-8').read()
rvs = re.findall(r'rowVerdict:\s*\n?\s*"((?:[^"\\]|\\.)*)"', src)
print("rowVerdict count:", len(rvs))
bad_cion = 0
longn = 0
for i, v in enumerate(rvs, 1):
    t = v.replace('\\"', '"')
    L = len(t)
    flagc = bool(re.search(r'ציון\s*[A-E]\.?$', t))
    flagm = bool(re.search(r'מעל הגבול|×', t))
    mark = []
    if flagc:
        mark.append("CION")
        bad_cion += 1
    if flagm:
        mark.append("PILLDUP")
    if L > 72:
        mark.append("LONG")
        longn += 1
    print("%2d %3d %-12s %s" % (i, L, '  '.join(mark), t))
print()
print("ending-in-cion:", bad_cion, "| over-72:", longn)
