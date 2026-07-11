import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Bari\03_operations\bsip0\scrape\_shared")
from bs4 import BeautifulSoup
from bsip0_nutrition import extract_nutrition_raw_auto, parse_nutrition_numeric

html = open(r"C:\Bari\03_operations\bsip0\scrape\_smoke_probes\outputs\yohananof_modal_full.html", encoding="utf-8").read()
soup = BeautifulSoup(html, "html.parser")
raw = extract_nutrition_raw_auto(soup)
print("selection:", raw["selection"])
print("rows:", raw["rows"])
parsed = parse_nutrition_numeric(raw)
print("parsed numeric:", parsed)

# also check ingredients extraction -- find the tabpanel-0 (ingredients)
tab0 = soup.select_one("#simple-tabpanel-0")
if tab0:
    print("\ningredients tab text:", tab0.get_text(" ", strip=True)[:500])
else:
    print("\nNO tabpanel-0 found")
