import re
src = open(r'C:\Bari\bari-web\src\lib\comparisons\magnesium-page-data.ts', encoding='utf-8').read()
blocks = re.split(r'\n  \{\n', src)
for b in blocks:
    name = re.search(r'name:\s*"([^"]+)"', b)
    flag = re.search(r'claimShortfallFlag:\s*"((?:[^"\\]|\\.)*)"', b)
    rv = re.search(r'rowVerdict:\s*\n?\s*"((?:[^"\\]|\\.)*)"', b)
    il = re.search(r'insightLine:\s*"((?:[^"\\]|\\.)*)"', b)
    if not name:
        continue
    print("- " + name.group(1)[:44])
    if flag:
        print("   PILL:    " + flag.group(1).replace('\\"', '"'))
    if rv:
        print("   VERDICT: " + rv.group(1).replace('\\"', '"'))
    print()
