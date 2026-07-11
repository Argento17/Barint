import sys, json
sys.path.insert(0, r"C:\Bari")
from integrations.clients import literature as lit

queries = {
    "mechanism": "GLP-1 receptor agonist mechanism appetite suppression gastric emptying review",
    "micronutrient": "GLP-1 receptor agonist micronutrient deficiency weight loss",
    "gi_side_effects": "GLP-1 receptor agonist nausea vomiting gastrointestinal adverse events prevalence",
    "food_aversion": "GLP-1 receptor agonist food aversion eating behavior changes semaglutide",
    "hydration": "GLP-1 receptor agonist dehydration acute kidney injury nausea vomiting",
    "protein_target_practical": "protein intake recommendation GLP-1 receptor agonist weight loss sarcopenia guideline",
    "micronutrient_deficiency_bariatric_analog": "reduced caloric intake micronutrient deficiency risk weight loss medication",
}

out = {}
for key, q in queries.items():
    try:
        papers = lit.pubmed(q, retmax=6)
        out[key] = [
            {"pmid": p.id, "title": p.title, "journal": p.journal, "year": p.year,
             "doi": p.doi, "pub_types": p.pub_types, "abstract": (p.abstract or "")[:600]}
            for p in papers
        ]
    except Exception as e:
        out[key] = {"error": str(e)}

print(json.dumps(out, indent=2, ensure_ascii=False))
