# -*- coding: utf-8 -*-
import json, sys
import integrations.clients.naturalness_gate as nat
import integrations.clients.hebrew_readability as read
RUN_GRAMMAR = "--grammar" in sys.argv

STRINGS = {
"S-40": 'רשות רגולטורית עצמאית',
"S-41": 'מה שאמרה על זה הרשות האירופית לבטיחות מזון',
"S-42": 'הרשות האירופית לבטיחות מזון (EFSA) היא הגוף הרגולטורי העצמאי שבוחן את בטיחות המזון באיחוד האירופי. היא לא יצרנית ולא איגוד תעשייה, וזה בדיוק מה שנותן משקל לקביעה שלה כאן.',
"S-43": 'בחוות דעת מדעית משנת 2011 קבעה EFSA שצריכת מזון או משקה שבהם תחליפי סוכר כמו מלטיטול תופסים את מקום הסוכר מובילה לעלייה נמוכה יותר של הסוכר בדם אחרי האכילה, בהשוואה למזון או משקה שמכילים סוכר. זו בדיוק התמונה שהמאמר הזה מתאר: נמוך יותר, מאותו מקור עצמאי.',
"S-44": 'חשוב לקרוא את זה מדויק. EFSA דיברה על עלייה נמוכה יותר של הסוכר בדם, לא על היעדר עלייה ולא על המלצה בריאותית. זו אמירה על תגובת הסוכר בדם, ושום דבר מעבר לזה.',
"S-45": 'לחוות הדעת המקורית של EFSA (EFSA Journal 2011)',
}

gram = None
if RUN_GRAMMAR:
    import integrations.clients.hebrew_grammar_gate as gg
    gram = gg

results = {}
hi_total = med_total = 0
read_clean = 0
gram_clean = 0
gram_total = 0
for k, t in STRINGS.items():
    rr = read.analyze(t)
    nr = nat.analyze(t)
    hi = [f for f in nr.flags if getattr(f, 'severity', '') == 'HIGH']
    med = [f for f in nr.flags if getattr(f, 'severity', '') == 'MEDIUM']
    hi_total += len(hi)
    med_total += len(med)
    if rr.is_clean:
        read_clean += 1
    entry = {
        "read_clean": rr.is_clean,
        "read_leaks": [str(l) for l in getattr(rr, 'leaks', [])],
        "nat_clean": nr.is_clean,
        "high": [{"tell": f.tell, "match": f.match, "note": f.note} for f in hi],
        "medium": [{"tell": f.tell, "match": f.match, "note": f.note} for f in med],
        "f2": getattr(nr, 'f2_signal', None),
    }
    if gram is not None:
        gr = gram.analyze(t)
        gram_total += 1
        if gr.is_clean:
            gram_clean += 1
        entry["gram_clean"] = gr.is_clean
        entry["gram_flags"] = [f.to_dict() for f in gr.flags]
    results[k] = entry

out = {
  "summary": {
    "n_strings": len(STRINGS),
    "readability_clean": read_clean,
    "naturalness_high_total": hi_total,
    "naturalness_medium_total": med_total,
  },
  "per_string": results,
}
with open(r"C:\Bari\02_products\snack_bars\_gate_run_379_efsa_out.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
out["summary"]["grammar_clean"] = gram_clean
out["summary"]["grammar_total"] = gram_total
print("readability_clean", read_clean, "/", len(STRINGS))
print("naturalness_high_total", hi_total)
print("naturalness_medium_total", med_total)
if RUN_GRAMMAR:
    print("grammar_clean", gram_clean, "/", gram_total)
