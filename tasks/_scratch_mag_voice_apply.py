"""Apply Tom's-Voice insightLine/rowVerdict rewrites to magnesium-page-data.ts, scoped by barcode block."""
import re, json

PATH = r"C:\bari\bari-web\src\lib\comparisons\magnesium-page-data.ts"
upd = json.load(open(r"C:\Bari\tasks\_scratch_mag_voice_apply.json", encoding="utf-8"))
src = open(PATH, encoding="utf-8").read()

def js_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')

# Block boundaries: each product starts at `id: "<barcode>"`. Build (barcode, start) list.
id_iter = list(re.finditer(r'id:\s*"(\d+)"', src))
spans = {}
for i, m in enumerate(id_iter):
    bc = m.group(1)
    start = m.start()
    end = id_iter[i + 1].start() if i + 1 < len(id_iter) else len(src)
    spans[bc] = (start, end)

INSIGHT_RE = re.compile(r'(insightLine:\s*)"(?:[^"\\]|\\.)*"')
ROW_RE = re.compile(r'(rowVerdict:\s*\n\s*)"(?:[^"\\]|\\.)*"')

changed = {"insightLine": 0, "rowVerdict": 0}
missing = []

# Apply per-barcode within its block. Work back-to-front so indices stay valid.
ops = []  # (block_start, block_end, barcode)
for bc in spans:
    ops.append((spans[bc][0], spans[bc][1], bc))
ops.sort(reverse=True)

for start, end, bc in ops:
    block = src[start:end]
    newblock = block
    if bc in upd["insightLine"]:
        rep = upd["insightLine"][bc]
        nb, n = INSIGHT_RE.subn(lambda m: m.group(1) + '"' + js_escape(rep) + '"', newblock, count=1)
        if n == 1:
            newblock = nb; changed["insightLine"] += 1
        else:
            missing.append(("insightLine", bc))
    if bc in upd["rowVerdict"]:
        rep = upd["rowVerdict"][bc]
        nb, n = ROW_RE.subn(lambda m: m.group(1) + '"' + js_escape(rep) + '"', newblock, count=1)
        if n == 1:
            newblock = nb; changed["rowVerdict"] += 1
        else:
            missing.append(("rowVerdict", bc))
    if newblock != block:
        src = src[:start] + newblock + src[end:]

open(PATH, "w", encoding="utf-8").write(src)
print("changed:", changed)
print("expected: insightLine=18 rowVerdict=3")
print("missing:", missing)
