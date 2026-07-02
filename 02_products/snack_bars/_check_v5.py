import json, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
with open(r'C:\Bari\bari-web\src\data\comparisons\snacks_frontend_v5.json', encoding='utf-8') as f:
    data = json.load(f)
print('Total products:', len(data['products']))
for p in data['products'][:50]:
    score = p.get('score', '?')
    grade = p.get('grade', '?')
    brand = p.get('brand', '')
    name = p.get('name_he', '')[:50]
    print(f'  score={score} grade={grade} | {brand} | {name}')
