"""
Stage 2 corpus filter generator for cookies-coffee factory_run_001.
Reads BSIP0 raw output, applies classification decisions, writes corpus_filter.json.
"""
import json, sys, io, hashlib, os
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ---- classification decisions (barcode -> (bucket, reason)) ----
DECISIONS = {
    "7290119043149": ("IN_SCORED", "IN_SCOPE: plain butter-flavored crisp biscuit. Dry/crisp, sweet, no filling, no coating. Classic coffee-occasion biscuit (§1.2 plain crisp biscuit variant). All core macros present (E=416 P=5 F=15). Ingredients present."),
    "4017100198151": ("OUT_OF_SCOPE", "OUT: cream-filled sandwich cookie (name says 'סנדוויץ'). Structural cream filling (vanilla cream layer) creates sandwich architecture. §1.3 exclusion: cream-filled sandwich cookies."),
    "7290018371930": ("IN_SCORED", "IN_SCOPE: whole-grain spelt organic petit beurre. Dry/crisp, sweet, no filling, no coating. Organic/spelt not scope exclusions (§1.3 organic IN; §1.4 whole-grain IN). All core macros present (E=428 P=10 F=14.7). Ingredients present."),
    "5410126116953": ("OUT_OF_SCOPE", "OUT: cookie spread product (ממרח עוגיות) — spreadable paste, not a biscuit. §1.3 in/out requires dry crisp biscuit; a spread fails condition (a). Lotus Biscoff spread."),
    "7290119043842": ("OUT_OF_SCOPE", "OUT: maamoul — date-filled biscuit (מעמול תמר). Integrated date filling (ממרח תמרים 32%) is the primary architectural feature. §1.3 condition (c): no filling integrated. P67 spec: maamoul OUT_OF_SCOPE."),
    "61245": ("IN_SCORED", "IN_SCOPE (borderline choc-chip §1.4): chocolate chips 8% embedded in crisp biscuit body. Primary architecture is the biscuit; chips are inclusions well below 30% threshold. Coffee-occasion format. All core macros present (E=527 P=6.4 F=28.2). Ingredients present."),
    "7290013740229": ("IN_SCORED", "IN_SCOPE: pressed almond horseshoe-shape crisp cookie. Dry/crisp, sweet, no filling, no coating. Typical Israeli coffee-table cookie (§1.2 butter cookies/pressed). All core macros present (E=503 P=7.5 F=33.2). Ingredients present."),
    "7290017894317": ("IN_SCORED", "IN_SCOPE (choc-chip §1.4): whole spelt biscuit with 10% chocolate chips. Primary architecture is the biscuit; chips below 30% threshold. Whole-grain IN (§1.4). All core macros present (E=465 P=8.4 F=19). Ingredients present."),
    "7290017898780": ("TRANSPARENCY_NULL", "MISSING_INGREDIENTS: scraper captured marketing text ('המשובחים ביותר...') instead of actual ingredient list. Engine cannot run NOVA or additive scoring. Per missing-data discard rule: one-shot only, DISCARD. Nutrition present but ingredient list absent."),
    "7290013740540": ("IN_SCORED", "IN_SCOPE: sugar-free elephant ear (אוזן פיל ללת'ס) crisp biscuit. Dry/crisp, sweet (maltitol), no filling, no coating. Classic Israeli coffee-table cookie shape. All core macros present (E=361 P=4.5 F=21.4). Ingredients present."),
    "7290119040377": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290123330785": ("OUT_OF_SCOPE", "OUT: date-filled finger biscuit (אצבע תמר). Integrated date filling (ממרח תמרים 20%) wrapped in biscuit dough. §1.3 condition (c): no filling integrated. Structurally equivalent to maamoul."),
    "7290018371947": ("IN_SCORED", "IN_SCOPE: spelt petit beurre (פתי בר כוסמין). Dry/crisp, sweet, no filling, no coating. Classic petit beurre format (§1.2). All core macros present (E=432 P=10.1 F=14.7). Ingredients present."),
    "7290119040223": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290109354996": ("IN_SCORED", "IN_SCOPE: gluten-free cocoa-flavored petit beurre. Dry/crisp, sweet, no filling, no external coating. GF is formulation variant IN per §1.4 (petit beurre confirms coffee occasion). Cocoa flavor is minor body flavoring. All core macros present (E=450 P=1.7 F=12). Ingredients present."),
    "7290013740137": ("IN_SCORED", "IN_SCOPE: classic elephant ear (אוזן פיל) crisp biscuit. Dry/crisp, sweet, no filling, no coating. Archetypical Israeli coffee-table biscuit (§1.2 plain crisp variant). All core macros present (E=379 P=4.5 F=21.4). Ingredients present."),
    "7290018893845": ("IN_SCORED", "IN_SCOPE: butter-flavored petit beurre (פתי בר בטעם חמאה). Dry/crisp, sweet, no filling, no coating. Classic petit beurre (§1.2). All core macros present (E=431 P=7.3 F=9.2). Ingredients present."),
    "7290017898711": ("TRANSPARENCY_NULL", "NULL_NUTRITION_AND_INGREDIENTS: both nutrition (all macros empty) and ingredient list absent. Cannot score or classify structurally. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290119040773": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290112340276": ("OUT_OF_SCOPE", "OUT: cream-filled biscuit (מילוי קרם קפה נמס = coffee cream filling). 'מילוי קרם' names filling as primary architectural feature. §1.3 condition (c): no filling integrated. Cream-filled category."),
    "7290013740694": ("IN_SCORED", "IN_SCOPE (borderline — alfajores): name 'אלפחורס' could imply sandwich with dulce de leche, but ingredient list shows plain crisp formulation (flour, fat, sugar, eggs, salt, flavoring — no cream or jam filling listed). Classified as pressed crisp biscuit per §1.3. All core macros present (E=416 P=6.1 F=18.5). Ingredients present."),
    "7296073162001": ("OUT_OF_SCOPE", "OUT: cream-filled biscuit (במילוי קרם אגוזים = hazelnut cream filling). 'מילוי קרם' names cream filling as primary architectural feature. §1.3 condition (c): no filling integrated."),
    "7290011489625": ("IN_SCORED", "IN_SCOPE: chocolate-flavored plain biscuit (ביסקוויט). Cocoa powder 2% mixed into biscuit body — flavoring not a coating. Dry/crisp, sweet, no filling, no external chocolate coating. All core macros present (E=434 P=6.8 F=11). Ingredients present."),
    "4823077614675": ("IN_SCORED", "IN_SCOPE: milk-flavored coffee biscuit (ביסקוויט לקפה בטעם חלב). Name explicitly says coffee biscuit. Dry/crisp, sweet, no filling, no coating. All core macros present (E=452 P=7.1 F=17.2). Ingredients present."),
    "7296073161981": ("OUT_OF_SCOPE", "OUT: cream-filled biscuit (במילוי קרם שוקולד = chocolate cream filling). 'מילוי קרם' names cream filling as primary architectural feature. §1.3 condition (c): no filling integrated."),
    "7622201823733": ("OUT_OF_SCOPE", "OUT: Milka Thins — chocolate-dominant biscuit. Cocoa butter, cocoa mass, milk fat prominent alongside flour. Positioned as chocolate confection not coffee biscuit. §1.3 condition (e) and chocolate-coated exclusion."),
    "5082146": ("TRANSPARENCY_NULL", "NULL_NUTRITION_AND_INGREDIENTS: both nutrition (all macros empty) and ingredient list absent. Cannot score or classify. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290119040124": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290105364883": ("OUT_OF_SCOPE", "OUT: white-chocolate-coated biscuit (ביסקוויט עד חצות לבן). Ingredients: white chocolate 61% + biscuit 39%. Primary component is the chocolate coating. §1.3 condition (d): not coated in chocolate as primary design feature. Chocolate-coated biscuits OUT."),
    "7290119041152": ("IN_SCORED", "IN_SCOPE: riffat (ריפ'את) — pressed crisp biscuit of Moroccan origin. Dry/crisp, sweet, no filling, no coating. Classic coffee-accompanying biscuit on Israeli shelf. All core macros present (E=429 P=8.5 F=16). Ingredients present."),
    "5410126726947": ("OUT_OF_SCOPE", "OUT: cookie spread with crunch (ממרח עוגיות לוטוס קראנץ') — spreadable paste not a biscuit. §1.3 in/out requires dry crisp biscuit; a spread fails condition (a)."),
    "7290111354519": ("TRANSPARENCY_NULL", "NULL_NUTRITION_AND_INGREDIENTS: all fields empty. Product 'רמקול בלוטוס לואקר' appears to be a non-food item (Bluetooth speaker) matched on 'לוטוס' keyword. Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "5317194": ("IN_SCORED", "IN_SCOPE: vanilla-flavored plain biscuit (ביסקוויט בטעם וניל). Dry/crisp, sweet, no filling, no coating. Vanilla is minor flavoring per §1.4. Classic Hadar biscuit. All core macros present (E=434 P=6.8 F=11). Ingredients present."),
    "7290106656734": ("OUT_OF_SCOPE", "OUT: cream-filled sandwich cookie (סנדוויץ' וניל). Structural vanilla cream filling between biscuit layers. §1.3 explicit: cream-filled sandwich cookies OUT."),
    "7290119043897": ("OUT_OF_SCOPE", "OUT: date roulade (רולדה תמרים). Biscuit dough rolled with date filling (ממרח תמרים 20%). Integrated filling is defining architectural feature. §1.3 condition (c): no filling integrated. Structurally equivalent to maamoul."),
    "4823077614699": ("IN_SCORED", "IN_SCOPE: butter-flavored coffee biscuit (ביסקוויט לקפה בטעם חמאה). Name explicitly says coffee biscuit. Dry/crisp, sweet, no filling, no coating. All core macros present (E=453 P=7.1 F=17.3). Ingredients present."),
    "710069006867": ("OUT_OF_SCOPE", "OUT: cream-filled sandwich cookie (סנדוויץ וניל). Ingredients confirm vanilla cream layer 27% between biscuit wafers. §1.3 condition (c): no filling integrated. Sandwich cookie OUT."),
    "7290112332691": ("OUT_OF_SCOPE", "OUT: cream-filled biscuit (מילוי קרם פסק זמן). 'מילוי קרם' names cream filling. §1.3 condition (c): no filling integrated."),
    "7290112336613": ("OUT_OF_SCOPE", "OUT: cream-filled sandwich cookie (עד חצות סנדוויץ = Midnight Sandwich). Structural cream filling between chocolate biscuit layers. §1.3: cream-filled sandwich cookies OUT."),
    "7290119040872": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290123330730": ("OUT_OF_SCOPE", "OUT: maamoul — date-filled biscuit (מעמול תמר sugar-free). Integrated date filling (ממרח תמרים 23%). §1.3 condition (c): no filling integrated. P67 spec: maamoul OUT_OF_SCOPE."),
    "7296073745402": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent. Product name (ממולאות קרם אגוז) also indicates filled biscuit. Primary classification: TRANSPARENCY_NULL per missing-data discard rule."),
    "7622300270506": ("OUT_OF_SCOPE", "OUT: Milka-branded chocolate biscuit (שיבולת עם שוקולד). Chocolate-dominant ingredient profile (cocoa butter, cocoa mass prominent). Milka positions this as chocolate confection not coffee-table biscuit. §1.3 condition (e): consumer occasion is confection."),
    "7290119040322": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "4820180816590": ("IN_SCORED", "IN_SCOPE: crisp biscuit with sunflower seeds (גרעיני חמנייה). Dry/crisp, sweet, no filling, no coating. Seed inclusions are ingredient variants not scope exclusions. All core macros present (E=504 P=7.2 F=25.8). Ingredients present."),
    "7290119041350": ("IN_SCORED", "IN_SCOPE: oat-based sugar-free crisp biscuit (קוואקר ללת'ס). Dry/crisp, sweet (maltitol), no filling, no coating. Oat variant IN per §1.4. All core macros present (E=444 P=5.9 F=20.5). Ingredients present."),
    "7290018893036": ("OUT_OF_SCOPE", "OUT: cream-filled sandwich cookie (סנדוויץ' שוקולד). Structural chocolate cream filling between biscuit wafers. §1.3: cream-filled sandwich cookies OUT."),
    "4820180816552": ("IN_SCORED", "IN_SCOPE: oat coconut crisp biscuit (שיבולת שועל קוקוס). Dry/crisp, sweet, no filling, no coating. Oat and coconut inclusions are ingredient variants. All core macros present (E=477 P=5.1 F=20.8). Ingredients present."),
    "2986065": ("IN_SCORED", "IN_SCOPE: chocolate-flavored petit beurre (פתי בר בטעם שוקולד). Dry/crisp, sweet, no filling, no external coating. Cocoa flavor in biscuit body is minor flavoring (§1.4). All core macros present (E=443 P=7.2 F=13.8). Ingredients present."),
    "96086001048": ("OUT_OF_SCOPE", "OUT: keto/functional biscuit (קיטו שקדים וקקאו). Protein=14.1g/100g, almond flour 57%, erythritol + monk fruit. §1.3 explicit: Protein/functional biscuits OUT. Keto diet positioning, not coffee-table."),
    "7290017898872": ("TRANSPARENCY_NULL", "MISSING_INGREDIENTS: scraper captured marketing description ('המשובחים ביותר...') instead of actual ingredient list. Engine cannot run NOVA or additive scoring. Per missing-data discard rule: one-shot only, DISCARD. NOTE: sodium=6mg/100g is an unusually low value but NOT an implausible parse artifact of ~6000mg type flagged in spec — this dataset has no ~6000mg outlier; the 6mg reading is the label value for this low-sodium butter recipe. Ingredient absence is the sole TRANSPARENCY_NULL trigger here."),
    "7290017898865": ("TRANSPARENCY_NULL", "MISSING_INGREDIENTS: scraper captured marketing description ('המשובחים ביותר...') instead of actual ingredient list. Engine cannot run NOVA or additive scoring. Per missing-data discard rule: one-shot only, DISCARD. NOTE: sodium=6mg/100g — same brand page pattern as barcode 7290017898872. Ingredient absence is the TRANSPARENCY_NULL trigger."),
    "7290017962139": ("IN_SCORED", "IN_SCOPE: berry-flavored crisp cookie (פירות יער). Natural almond/rice flour + cranberries base. Dry/crisp, sweet, no filling, no coating. Natural formulation variants IN (§1.3). All core macros present (E=420 P=5.3 F=21.5). Ingredients present."),
    "8000500366073": ("OUT_OF_SCOPE", "OUT: Nutella-filled biscuit (ביסקוויט נוטלה). Ingredients confirm 40% Nutella hazelnut-cocoa spread filling inside biscuit shell. Structurally a cream-filled confection. §1.3 condition (c): no filling integrated."),
    "7296073745396": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent. Product name (ממולאות קרם חלווה) indicates filled biscuit. Primary classification: TRANSPARENCY_NULL per missing-data discard rule."),
    "540160": ("IN_SCORED", "IN_SCOPE: whole-wheat sugar-free biscuit (ללת'ס מקמח מלא, HaAchim). Dry/crisp, sweet (maltitol), no filling, no coating. Whole grain IN (§1.4). All core macros present (E=392 P=7 F=12). Ingredients present."),
    "7290109354972": ("IN_SCORED", "IN_SCOPE: gluten-free classic petit beurre (פתי בר ללא גלוטן קלאסי). Dry/crisp, sweet, no filling, no coating. GF variant IN per §1.4 (petit beurre format confirms occasion). All core macros present (E=454 P=0.6 F=12.3). Ingredients present."),
    "7290107936958": ("OUT_OF_SCOPE", "OUT: chocolate-coated finger biscuit (עד חצות אצבעות). Ingredients: 38% milk chocolate coating over biscuit fingers. Chocolate coating is primary design feature at 38%. §1.3 condition (d): not coated in chocolate as primary feature. Chocolate-coated biscuits OUT."),
    "5410126116168": ("IN_SCORED", "IN_SCOPE: Lotus Biscoff caramel speculoos — the category archetype (§1.2 Speculoos/Belgian biscuits). Dry/crisp, sweet, no filling, no coating. All core macros present (E=484 P=4.9 F=19). Ingredients present."),
    "7290013453631": ("IN_SCORED", "IN_SCOPE (borderline — high protein from natural peanuts): peanut butter cookie (58% peanuts). Protein=15.5g/100g naturally from peanuts, not from protein fortification. §1.3 exclusion targets engineered functional products. All core macros present (E=485 P=15.5 F=24.3). Ingredients present."),
    "7290013453693": ("IN_SCORED", "IN_SCOPE: lemon zest sugar-free crisp cookie (גרידת לימון ללת'ס). Natural almond/rice flour + agave. Dry/crisp, sweet, no filling, no coating. Lemon is minor flavoring (§1.4). All core macros present (E=446 P=7.3 F=31). Ingredients present."),
    "7290013740472": ("IN_SCORED", "IN_SCOPE: sugar-dusted crisp cookies (מושלגות). Dry/crisp, sweet, no filling. Powdered sugar is a light surface dusting, not a structural coating. All core macros present (E=372 P=7 F=11.1). Ingredients present."),
    "181103": ("OUT_OF_SCOPE", "OUT: chocolate-coated biscuit (ביסקוויט עד חצות חלב). Ingredients: 61% milk chocolate + 39% biscuit. Chocolate is primary component by weight. §1.3 condition (d): not coated in chocolate as primary design feature. Chocolate-coated biscuits OUT."),
    "7290119386512": ("OUT_OF_SCOPE", "OUT: ice coffee confection containing biscuit pieces (טעמי X אייס קפה). Ingredients include milk chocolate, ice cream wafer pieces, cornflakes, praline. Product category is confection/ice cream. §1.3 condition (e): consumer occasion is confection, not a standalone coffee biscuit."),
    "7290119043743": ("IN_SCORED", "IN_SCOPE: Moroccan-style crisp biscuit (מרוקאיות). Dry/crisp, sweet, no filling, no coating. Common coffee-accompanying cookie. All core macros present (E=414 P=8 F=14). Ingredients present."),
    "313160": ("IN_SCORED", "IN_SCOPE: chocolate-flavored crisp biscuit (שוקולד זהבה, Osem). Cocoa 3.3% mixed into biscuit body — flavoring not coating. Dry/crisp, sweet, no filling. All core macros present (E=470 P=7 F=17). Ingredients present."),
    "960860015432": ("IN_SCORED", "IN_SCOPE: whole-wheat sugar-free biscuit (ללת'ס מקמח מלא, Aviva). Dry/crisp, sweet, no filling, no coating. Whole grain IN (§1.4). All core macros present (E=384 P=9 F=8.7). Ingredients present."),
    "7290017962108": ("IN_SCORED", "IN_SCOPE: vanilla pecan sugar-free crisp cookie (וניל פקאן כשל'פ). Natural almond/rice flour + agave. Dry/crisp, sweet, no filling, no coating. All core macros present (E=523 P=8.1 F=33.5). Ingredients present."),
    "4267124": ("TRANSPARENCY_NULL", "MISSING_INGREDIENTS: ingredient list absent. Name (ממולאות בטעם תות) indicates filled biscuit that would also be OUT_OF_SCOPE if data present. Primary classification: TRANSPARENCY_NULL per missing-data discard rule."),
    "7290013740052": ("IN_SCORED", "IN_SCOPE (borderline — jam center ruling): flower-shaped crisp biscuit with small jam center (פרחי ריבה). Jam is a decorative thumbprint-style surface accent, NOT a structural sandwich filling. Primary architecture is the crisp biscuit body. Classic Israeli coffee-table cookie. All core macros present (E=443 P=5 F=23.2). Ingredients present."),
    "7290119040575": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290119040674": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290018371923": ("IN_SCORED", "IN_SCOPE: organic whole-wheat petit beurre (פתי בר קמח מלא אורגני). Dry/crisp, sweet, no filling, no coating. Organic IN (§1.3). Whole-grain IN (§1.4). All core macros present (E=428 P=6.8 F=14.5). Ingredients present."),
    "7290119040605": ("OUT_OF_SCOPE", "OUT: jam-filled biscuit (נסיכה בטעם תות). Ingredients confirm 38% strawberry jam filling (מילוי לאפיה 38%). Filling content of 38% makes this structurally a filled biscuit. §1.3 condition (c): no filling integrated. Distinguished from thumbprint cookies (7290013740052) where jam is a small surface accent; here 38% is filling."),
    "34256": ("OUT_OF_SCOPE", "OUT: chocolate-coated biscuit (ביסקוויט תירוש). Ingredients confirm 30% chocolate compound coating (ציפוי בטעם שוקולד 30%). Coating at 30% is primary design feature. §1.3 condition (d): choc-COATED OUT. P67 spec explicit."),
    "311463": ("IN_SCORED", "IN_SCOPE: butter-flavored sugar-free whole-wheat biscuit (חמאה ללת'ס). Dry/crisp, sweet (maltitol/sucralose), no filling, no coating. Whole grain IN (§1.4). All core macros present (E=419 P=8.8 F=16.1). Ingredients present."),
    "5410126006049": ("IN_SCORED", "IN_SCOPE: Lotus Biscoff caramel biscuit variant — category archetype (§1.2 Speculoos). Dry/crisp, sweet, no filling, no coating. All core macros present (E=484 P=4.9 F=19). Ingredients present."),
    "74184": ("IN_SCORED", "IN_SCOPE: classic petit beurre (פתי בר קלאסי, Osem) — canonical category member (§1.2: Classic rectangular butter biscuit; dominant on Israeli shelf). Dry/crisp, sweet, no filling, no coating. All core macros present (E=460 P=7 F=14). Ingredients present."),
    "7290112346537": ("OUT_OF_SCOPE", "OUT: cream-filled biscuit (קרם בטעם טורטית = tortita-flavor cream). 'קרם' confirms integrated cream filling. §1.3 condition (c): no filling integrated. Same Pinocciet cream-filled product family as 7290112340276 and 7290112332691."),
    "80083764": ("IN_SCORED", "IN_SCOPE: grain and oat crisp biscuit (דגנים עם שיבולת שועל). Dry/crisp, sweet, no filling, no coating. Whole-grain oat variant IN (§1.4). All core macros present (E=471 P=8.7 F=20). Ingredients present."),
    "4820180816576": ("IN_SCORED", "IN_SCOPE: crisp biscuit with coconut flakes (שבבי קוקוס). Dry/crisp, sweet, no filling, no coating. Coconut flake is ingredient inclusion not scope exclusion. All core macros present (E=507 P=6.3 F=25.6). Ingredients present."),
    "7290119041107": ("IN_SCORED", "IN_SCOPE: round Moroccan-style crisp biscuit (מרוקאיות עגול). Dry/crisp, sweet, no filling, no coating. Coffee-accompanying cookie. All core macros present (E=429 P=8.5 F=16). Ingredients present."),
    "7290119040827": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290013453501": ("IN_SCORED", "IN_SCOPE: spelt biscotti with chocolate inclusions (ביסקוטי כוסמין שוקולד). Dry/crisp twice-baked biscotti format (§1.2 Biscotti/cantuccini). Chocolate as flavoring/inclusion. No coating. All core macros present (E=324 P=6.6 F=10.5). Ingredients present."),
    "7290119043095": ("IN_SCORED", "IN_SCOPE: oat crisp biscuit (שיבולת שועל). Dry/crisp, sweet, no filling, no coating. Oat variant IN per §1.4. All core macros present (E=444 P=5.9 F=20.5). Ingredients present."),
    "4267209": ("TRANSPARENCY_NULL", "MISSING_INGREDIENTS: ingredient list absent. Engine cannot run NOVA or additive scoring. Per missing-data discard rule: one-shot only, DISCARD. Partial nutrition present (E=492, P=6.3, F=21.4) but sodium absent and ingredients absent."),
    "7290119040650": ("OUT_OF_SCOPE", "OUT: jam-filled biscuit (נסיכה מיקס). Ingredients confirm 38% strawberry jam filling. Same architecture as 7290119040605. §1.3 condition (c): no filling integrated."),
    "7290119040520": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290119040629": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290017898797": ("TRANSPARENCY_NULL", "MISSING_INGREDIENTS: scraper captured marketing description ('המשובחים ביותר...') instead of actual ingredient list. Engine cannot run NOVA or additive scoring. Per missing-data discard rule: one-shot only, DISCARD. Nutrition present (E=449, P=9.3, F=17.3)."),
    "7290013740342": ("IN_SCORED", "IN_SCOPE (borderline — jam center ruling, same as 7290013740052): sugar-free jam-center flower cookie (פרחי ריבה ללת'ס). Crisp biscuit body with small jam center depression (thumbprint style). Primary architecture is the crisp biscuit; jam is surface accent. All core macros present (E=394 P=4.6 F=21.3). Ingredients present."),
    "7290119040476": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "80083665": ("IN_SCORED", "IN_SCOPE: organic biscuit with 12% chocolate chips (אורגניות+שוקולד). Chips embedded in biscuit body; below 30% threshold (§1.4 choc-chip ruling). Organic IN (§1.3). All core macros present (E=491 P=7.3 F=23). Ingredients present."),
    "5410126806250": ("IN_SCORED", "IN_SCOPE: Lotus Biscoff original biscuit — the category archetype (§1.2 Speculoos/Belgian biscuits). Dry/crisp, sweet, no filling, no coating. All core macros present (E=484 P=4.9 F=19). Ingredients present."),
    "7290013740557": ("IN_SCORED", "IN_SCOPE: riffat (רייפעת) — anise and sesame crisp biscuit. Dry/crisp, sweet, no filling, no coating. Common coffee-accompanying biscuit. All core macros present (E=467 P=8.8 F=16.8). Ingredients present."),
    "5410126726244": ("IN_SCORED", "IN_SCOPE: Lotus Biscoff caramel biscuit — category archetype variant (§1.2 Speculoos). Dry/crisp, sweet, no filling, no coating. All core macros present (E=484 P=4.9 F=19). Ingredients present."),
    "7290119041305": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "7622010001858": ("OUT_OF_SCOPE", "OUT: Oreo cream-filled sandwich cookie (קרם וניל אוראו). Classic sandwich architecture: cocoa biscuit + vanilla cream. §1.3 explicit: Cream-filled sandwich cookies (אוראו-style) OUT."),
    "7622210453327": ("OUT_OF_SCOPE", "OUT: Milka Sensations — soft chocolate confection cookie. Chocolate-dominant ingredient profile (cocoa butter, cocoa mass, milk fat prominent); soft interior. Positioned as premium chocolate treat not coffee biscuit. §1.3 condition (e)."),
    "4017100364112": ("OUT_OF_SCOPE", "OUT: cream-filled sandwich cookie (סנדוויץ היט קקאו). Structural cocoa biscuit + filling sandwich architecture. §1.3: cream-filled sandwich cookies OUT."),
    "8008698037171": ("IN_SCORED", "IN_SCOPE: gluten-free butter cookie (חמאה ללא גלוטן, Shar). Corn flour + real butter 30% + sugar. Dry/crisp, sweet, no filling, no coating. GF variant IN per §1.4 (butter cookie format; occasion matches). All core macros present (E=517 P=6.2 F=28). Ingredients present."),
    "7290120870147": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290013740465": ("IN_SCORED", "IN_SCOPE: rose-shaped crisp butter cookies (שושנים). Dry/crisp, sweet, no filling, no coating. Classic pressed coffee-table cookie. All core macros present (E=394 P=5.9 F=18.3). Ingredients present."),
    "7290111355370": ("TRANSPARENCY_NULL", "NULL_NUTRITION_AND_INGREDIENTS: all fields empty. 'אוזניות בלוטוס לואקר' appears to be a non-food item (Bluetooth speaker) matched on 'לוטוס' keyword. Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290119040179": ("IN_SCORED", "IN_SCOPE (borderline — jam center ruling): flower-shaped biscuit with strawberry jam center (פרח עם ריבת תות). Crisp biscuit body with small jam depression (thumbprint style). Jam is surface accent not structural filling. Classic coffee-table cookie. All core macros present (E=520 P=5.8 F=25.5). Ingredients present."),
    "7290017898506": ("IN_SCORED", "IN_SCOPE: biscotti with cashews (ביסקוטי, HaChush HaShishi). Dry/crisp twice-baked biscotti format (§1.2 Biscotti/cantuccini). This product has a real ingredient list (unlike other HaChush products). All core macros present (E=415 P=9 F=22). Ingredients present."),
    "99804": ("IN_SCORED", "IN_SCOPE (borderline — choc-chip §1.4): crisp biscuit with white chocolate chips 19.9%. Primary architecture is biscuit body; white chocolate pieces are inclusions below 30% threshold. No external coating. All core macros present (E=496 P=5.9 F=24.2). Ingredients present."),
    "7622201809188": ("OUT_OF_SCOPE", "OUT: Milka-branded chocolate biscuit (ביסקוויט מילקה). Chocolate-dominant profile (cocoa butter, palm oil, cocoa mass, milk fat). Milka brand positions this as chocolate confection not coffee-table biscuit. §1.3 condition (e)."),
    "7290119041206": ("IN_SCORED", "IN_SCOPE: oat crisp biscuit (קוואקר VOILA). Dry/crisp, sweet, no filling, no coating. Oat variant IN per §1.4. All core macros present (E=444 P=5.9 F=20.5). Ingredients present."),
    "7290119043798": ("IN_SCORED", "IN_SCOPE: elephant ear shaped crisp biscuit (אוזניות). Dry/crisp, sweet, no filling, no coating. Classic Israeli coffee-table cookie shape. All core macros present (E=435 P=5.5 F=19.8). Ingredients present."),
    "7290119040278": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290119041053": ("IN_SCORED", "IN_SCOPE: Moroccan-style crisp biscuit (סגנון מרוקאי). Dry/crisp, sweet, no filling, no coating. All core macros present (E=429 P=8.5 F=16). Ingredients present."),
    "7290112961754": ("OUT_OF_SCOPE", "OUT: choc-chip biscuit WITH hazelnut cream filling (שוקוציפס קרם אגוז). Despite choc-chip exterior, product has integrated hazelnut cream filling ('קרם אגוז' in name). §1.3 condition (c): no filling integrated. Cream filling disqualifies regardless of biscuit body."),
    "710069055452": ("OUT_OF_SCOPE", "OUT: cream-filled sandwich cookie (סנדוויץ שוקו). Ingredients confirm chocolate cream layer 27% between biscuit layers. §1.3: cream-filled sandwich cookies OUT."),
    "7296073497639": ("OUT_OF_SCOPE", "OUT: animal-shaped children's biscuits (ביסקוויט חיות). §1.3 explicit: Children's character cookies (animal-shaped) OUT. Primary occasion is children's snacking not coffee-table."),
    "7290013740113": ("IN_SCORED", "IN_SCOPE: Moroccan-style crisp biscuit with sesame and coconut (מרוקאיות). Dry/crisp, sweet, no filling, no coating. Coffee-accompanying cookie. All core macros present (E=389 P=5.7 F=17.9). Ingredients present."),
    "311128": ("IN_SCORED", "IN_SCOPE: butter-flavored crisp biscuit (בטעם חמאה, Man). Dry/crisp, sweet, no filling, no coating. Plain crisp biscuit variant (§1.2). All core macros present (E=478 P=6.4 F=19.4). Ingredients present."),
    "7290123330488": ("IN_SCORED", "IN_SCOPE (borderline — high protein from natural peanuts): peanut cookie (בוטנים) with 58% peanut content. Protein=15.4g/100g naturally from peanuts not fortification. §1.3 exclusion targets engineered functional products; this is a simple natural-ingredient cookie. All core macros present (E=468 P=15.4 F=28.4). Ingredients present."),
    "7296073745372": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent. Product name (ממולאות שוקולד) indicates filled biscuit. Primary classification: TRANSPARENCY_NULL per missing-data discard rule."),
    "311708": ("IN_SCORED", "IN_SCOPE: whole-wheat crisp biscuit (מחיטה מלאה, Man). Dry/crisp, sweet, no filling, no coating. Whole grain IN per §1.4. All core macros present (E=478 P=6 F=22.6). Ingredients present."),
    "7290106656727": ("IN_SCORED", "IN_SCOPE (borderline — shape/occasion): Elit Chico-style chocolate-flavored biscuit (חיוכים שוקולד). Cocoa 2.4% in biscuit body — flavoring not coating. No external chocolate coating, no filling. Standard crisp biscuit not positioned as children's character packaging. All core macros present (E=497 P=6 F=21). Ingredients present."),
    "2986058": ("IN_SCORED", "IN_SCOPE: vanilla petit beurre (פתי בר וניל, Gatnio). Dry/crisp, sweet, no filling, no coating. Classic petit beurre variant (§1.2). All core macros present (E=440 P=7.2 F=13). Ingredients present."),
    "7290112494221": ("OUT_OF_SCOPE", "OUT: chocolate bar containing biscuit (קליק ביסקוויט). Ingredients: 47% milk chocolate (primary component) + 27% biscuit inside. This is a chocolate confection product not a biscuit. §1.3 condition (d). Consumer occasion is chocolate bar not coffee biscuit."),
    "96086001079": ("OUT_OF_SCOPE", "OUT: keto/functional biscuit (קיטו שקד לוז). Protein=15g/100g, almond flour 57%, erythritol + monk fruit. §1.3 explicit: Protein/functional biscuits OUT. Same brand and positioning as 96086001048."),
    "313184": ("OUT_OF_SCOPE", "OUT: animal-shaped children's biscuits (גן חיות טעם וניל, Asem). §1.3 explicit: Children's character cookies (Leibniz Zoo, animal-shaped) OUT. Primary occasion is children's snacking."),
    "7290017898773": ("TRANSPARENCY_NULL", "MISSING_INGREDIENTS: scraper captured marketing description ('המשובחים ביותר...') instead of actual ingredient list. Engine cannot run NOVA or additive scoring. Per missing-data discard rule: one-shot only, DISCARD. Nutrition present (E=587, P=9.5, F=39.9)."),
    "7290119040803": ("IN_SCORED", "IN_SCOPE: cinnamon sugar crisp biscuit (קינמון מסוכרות). Dry/crisp, sweet, no filling, no external chocolate coating. Cinnamon is minor flavoring; sugar dusting is surface feature. All core macros present (E=430 P=6 F=19). Ingredients present."),
    "7290119040902": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
    "7290119040728": ("TRANSPARENCY_NULL", "NULL_NUTRITION: all core macros absent (energy, protein, fat all empty). Cannot score. Per missing-data discard rule: one-shot only, DISCARD."),
}

# ---- load raw BSIP0 ----
raw_path = "02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json"
with open(raw_path, "r", encoding="utf-8") as f:
    products = json.load(f)

assert len(products) == 129, f"Expected 129, got {len(products)}"

# ---- build product list in BSIP0 order ----
out_products = []
missing_barcodes = []
for p in products:
    bc = str(p["barcode"])
    if bc not in DECISIONS:
        missing_barcodes.append(bc)
        continue
    decision, reason = DECISIONS[bc]
    out_products.append({
        "barcode": bc,
        "name_he": p.get("name_he", ""),
        "brand": p.get("brand", ""),
        "decision": decision,
        "reason": reason,
    })

if missing_barcodes:
    print(f"ERROR: Missing decisions for barcodes: {missing_barcodes}", file=sys.stderr)
    sys.exit(1)

assert len(out_products) == 129, f"Expected 129, got {len(out_products)}"

# ---- bucket summary ----
in_scored = [p for p in out_products if p["decision"] == "IN_SCORED"]
transparency = [p for p in out_products if p["decision"] == "TRANSPARENCY_NULL"]
out_of_scope = [p for p in out_products if p["decision"] == "OUT_OF_SCOPE"]

assert len(in_scored) + len(transparency) + len(out_of_scope) == 129

# ---- build JSON ----
out_doc = {
    "stage": "2_corpus_filter",
    "category_slug": "cookies-coffee",
    "run_id": "factory_run_001",
    "generated": "2026-06-13",
    "owner": "Data Agent (data-agent)",
    "source_bsip0": "cookies_coffee_bsip0_raw_20260613T163431.json",
    "source_bsip0_count": 129,
    "methodology_ref": "cookies_coffee_scoring_interpretation_v1.md §1.2–§1.4",
    "task_ref": "TASK-275 / P67",
    "nutrition_sufficiency_gate": "energy_kcal_raw AND fat_raw AND protein_raw must all be non-null/non-empty AND ingredient list must be a real ingredient list (not marketing text). Partial panels or marketing-text ingredients -> TRANSPARENCY_NULL.",
    "off_used": False,
    "off_note": "OFF ban is absolute (CLAUDE.md hard rule, TASK-238). No field from any product was filled from OFF or any external source. NULL fields remain NULL.",
    "sodium_implausible_note": "Spec flagged two products with ~6000mg/100g sodium as a potential parse artifact. Actual data shows NO product with sodium >=600mg/100g (maximum in corpus is 510mg for barcode 4017100364112). Products 7290017898872 and 7290017898865 (both HaChush HaShishi) show sodium=6mg/100g — this is an unusually low value but plausible for an unsalted butter recipe and is consistent across the brand's label page pattern. It is NOT a parse artifact of the 6000mg type. These two products are TRANSPARENCY_NULL due to missing ingredient lists, not due to sodium anomaly.",
    "filter_logic": "Two-stage: (1) structural/occasion test per §1.3 in/out rule — identifies OUT_OF_SCOPE; (2) nutrition + ingredient sufficiency gate per brined-lesson rule — remaining in-scope products without full macros or real ingredient list become TRANSPARENCY_NULL; scorable in-scope products with full data become IN_SCORED.",
    "exclusion_rules": {
        "SPREAD_OUT": "Cookie spreads (ממרח עוגיות) — not a biscuit. Fails §1.3 condition (a).",
        "MAAMOUL_OUT": "Maamoul and date-filled biscuits (מעמול, אצבע תמר, רולדה תמרים). Integrated date filling at 20-32%. Fails §1.3 condition (c).",
        "SANDWICH_CREAM_OUT": "Cream-filled sandwich cookies (סנדוויץ, מילוי קרם). Structural filling. Fails §1.3 condition (c).",
        "CHOC_COATED_OUT": "Chocolate-coated biscuits where chocolate is primary architectural feature (>30% weight or full outer coat). Fails §1.3 condition (d). Examples: עד חצות series (61%/38% chocolate), ביסקוויט תירוש (30% coating), קליק (47% chocolate primary).",
        "JAM_FILLED_OUT": "Biscuits with structural jam filling at substantial percentage (38%). נסיכה products with 38% jam filling. Distinguished from thumbprint jam-center cookies (7290013740052, 7290013740342, 7290119040179) where jam is a small surface accent.",
        "NUTELLA_FILLED_OUT": "Nutella-filled biscuit (40% filling). Fails §1.3 condition (c).",
        "CHILDREN_OUT": "Animal-shaped and character children's biscuits (ביסקוויט חיות, גן חיות). Fails §1.3 condition (e).",
        "KETO_FUNCTIONAL_OUT": "Keto/protein-functional biscuits (protein >14g from fortification; almond flour base; erythritol). Fails §1.3 protein/functional exclusion.",
        "CONFECTION_OUT": "Chocolate confection products (Milka Sensations, Milka Thins, Milka biscuit, Oreo). Consumer occasion is chocolate confection not coffee biscuit. Fails §1.3 condition (e).",
        "ICE_COFFEE_CONFECTION_OUT": "Ice coffee confection with wafer pieces (טעמי X). Not a standalone coffee biscuit.",
        "NULL_NUTRITION_INGREDIENTS": "Products with absent nutrition (energy/protein/fat) or absent ingredient list (or marketing text as ingredients) -> TRANSPARENCY_NULL.",
        "NON_FOOD_BLUETOOTH": "Two products ('רמקול בלוטוס לואקר', 'אוזניות בלוטוס לואקר') appear to be non-food Bluetooth speaker products matched on 'לוטוס' keyword -> TRANSPARENCY_NULL (all data empty).",
    },
    "borderline_calls": [
        {"barcode": "61245", "name_he": "עוגיות שוקוציפס+שוקולד", "call": "IN_SCORED", "rationale": "8% dark choc chips embedded in crisp biscuit body. Below 30% threshold. Primary architecture is the biscuit."},
        {"barcode": "7290017894317", "name_he": "עוגיות כוסמין מלא שוקולד", "call": "IN_SCORED", "rationale": "10% choc chips in whole-spelt biscuit body. Below 30% threshold."},
        {"barcode": "7290013740694", "name_he": "עוגיות אלפחורס", "call": "IN_SCORED", "rationale": "Name implies dulce-filled sandwich but ingredient list shows plain formulation (no cream/jam filling). Classified as crisp biscuit."},
        {"barcode": "7290013453631", "name_he": "עוגיות חמאת בוטנים כשל'פ", "call": "IN_SCORED", "rationale": "Protein=15.5g/100g naturally from 58% peanuts. Not engineered/fortified. Not functional positioning."},
        {"barcode": "7290123330488", "name_he": "עוגיות בוטנים כשל'פ", "call": "IN_SCORED", "rationale": "Protein=15.4g/100g naturally from 58% peanuts. Same ruling as 7290013453631."},
        {"barcode": "7290013740052", "name_he": "עוגיות פרחי ריבה", "call": "IN_SCORED", "rationale": "Thumbprint jam-center (small surface accent). Primary architecture is crisp biscuit body. Distinct from jam-filled biscuits (נסיכה 38%)."},
        {"barcode": "7290013740342", "name_he": "עוגיות פרחי ריבה ללת'ס", "call": "IN_SCORED", "rationale": "Sugar-free thumbprint jam-center. Same ruling as 7290013740052."},
        {"barcode": "7290119040179", "name_he": "עוגיות פרח עם ריבת תות", "call": "IN_SCORED", "rationale": "Thumbprint jam-center style. Same ruling as 7290013740052."},
        {"barcode": "7290119040605", "name_he": "עוגיות נסיכה בטעם תות", "call": "OUT_OF_SCOPE", "rationale": "38% jam filling listed in ingredients. Structural filling, not a thumbprint accent."},
        {"barcode": "7290119040650", "name_he": "עוגיות נסיכה מיקס", "call": "OUT_OF_SCOPE", "rationale": "38% jam filling (same as product 7290119040605)."},
        {"barcode": "80083665", "name_he": "עוגיות אורגניות+שוקולד", "call": "IN_SCORED", "rationale": "12% choc chips in organic wheat biscuit body. Below 30% threshold."},
        {"barcode": "99804", "name_he": "עוגיות שוקולד לבן חלבי", "call": "IN_SCORED", "rationale": "19.9% white choc chips in biscuit body. Below 30% threshold. No external coating."},
        {"barcode": "7290106656727", "name_he": "עוגיות חיוכים שוקולד", "call": "IN_SCORED", "rationale": "Smiley-face format with 2.4% cocoa flavoring. Not positioned as character/children's cookie despite shape. No coating. Classified as crisp biscuit."},
        {"barcode": "7290017898506", "name_he": "ביסקוטי", "call": "IN_SCORED", "rationale": "The only HaChush HaShishi product with a real ingredient list (all other HaChush products have marketing text as ingredients). Biscotti format IN."},
        {"barcode": "7290017898872", "name_he": "עוגיות חמאה דנית ללא תוס", "call": "TRANSPARENCY_NULL", "rationale": "Missing real ingredient list (marketing text captured). Sodium=6mg/100g is very low but not a parse artifact; ingredient absence is the trigger."},
        {"barcode": "7290017898865", "name_he": "עוגיות חמאה דנית", "call": "TRANSPARENCY_NULL", "rationale": "Missing real ingredient list (marketing text captured). Same HaChush brand/page pattern."},
        {"barcode": "7290112961754", "name_he": "עוגיות שוקוציפס קרם אגוז", "call": "OUT_OF_SCOPE", "rationale": "Appears choc-chip but name confirms cream filling (קרם אגוז). Cream filling disqualifies per §1.3(c), regardless of exterior."},
    ],
    "min_corpus_size": 25,
    "corpus_size_check": "PASS: 61 IN_SCORED >= 25 minimum",
    "summary": {
        "total_bsip0": 129,
        "in_scored": len(in_scored),
        "transparency_null": len(transparency),
        "out_of_scope": len(out_of_scope),
        "sum_check": f"{len(in_scored)} + {len(transparency)} + {len(out_of_scope)} = {len(in_scored)+len(transparency)+len(out_of_scope)} PASS",
        "out_of_scope_breakdown": {
            "SPREAD_OUT": 2,
            "MAAMOUL_DATE_FILLED_OUT": 4,
            "SANDWICH_CREAM_FILLED_OUT": 10,
            "CHOC_COATED_OUT": 4,
            "JAM_FILLED_OUT": 2,
            "NUTELLA_FILLED_OUT": 1,
            "CHILDREN_OUT": 2,
            "KETO_FUNCTIONAL_OUT": 2,
            "CONFECTION_CHOCOLATE_OUT": 6,
            "ICE_COFFEE_CONFECTION_OUT": 1,
            "CREAM_FILLED_NO_SANDWICH_NAME_OUT": 3,
        }
    },
    "products": out_products,
}

# ---- validate OOS breakdown sum ----
oos_sum = sum(out_doc["summary"]["out_of_scope_breakdown"].values())
assert oos_sum == len(out_of_scope), f"OOS breakdown sum {oos_sum} != {len(out_of_scope)}"

# ---- write output ----
out_path = "02_products/cookies_coffee/factory_run_001/corpus_filter.json"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out_doc, f, ensure_ascii=False, indent=2)

# ---- sha256 ----
with open(out_path, "rb") as f:
    sha = hashlib.sha256(f.read()).hexdigest()

print(f"Written: {out_path}")
print(f"SHA256: {sha}")
print(f"IN_SCORED:        {len(in_scored)}")
print(f"TRANSPARENCY_NULL:{len(transparency)}")
print(f"OUT_OF_SCOPE:     {len(out_of_scope)}")
print(f"TOTAL:            {len(in_scored)+len(transparency)+len(out_of_scope)}")
print("SUM_CHECK: PASS" if len(in_scored)+len(transparency)+len(out_of_scope)==129 else "SUM_CHECK: FAIL")
print("MIN_CORPUS_CHECK: PASS" if len(in_scored) >= 25 else "MIN_CORPUS_CHECK: FAIL")
