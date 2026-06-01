# BSIP2 Prototype v0 — Top Failure Candidates & Most Correct

## 5 Most Suspicious Products

These products show the most signs of scoring unreliability or architectural mismatch.

### bsip1_16000548909
**קראנצ'י חטיף שיבולת שועל מיקס חמישייה**  
Score: 32.3 (insufficient_data) | Category: cereal | NOVA: 3 | Confidence: 27 (insufficient)  
Flags: 2 | Instability: True | Status: context_limited  

**Flags:**
- CATEGORY_INSTABILITY: primary=cereal secondary=snack_bar_granola, confidence=0.63
- CONTEXT_LIMITED: per-100g score may be misleading (no_nutrition_data)

**Score drivers:**
- DOMINANT: Confidence ceiling active at 50 (data quality limitation)
- DOMINANT: Binding cap=75 from rules: ['NOVA_PROXY_3_PROCESSED']

### bsip1_8423207206501
**סלים דליס חטיף רב דגנים מצופה שוקולד לבן בטעם יוגורט**  
Score: 23.0 (E) | Category: snack_bar_granola | NOVA: 3 | Confidence: 82 (high)  
Flags: 1 | Instability: True | Status: standard  

**Flags:**
- CATEGORY_INSTABILITY: primary=snack_bar_granola secondary=dairy_protein, confidence=0.52

**Score drivers:**
- DOMINANT: Binding cap=45 from rules: ['HIGH_CAL_HIGH_SUGAR_MODERATE', 'HIGH_SUGAR_25G_PLUS', 'SNACK_BAR_HIGH_CAL_SUGAR', 'SNACK_BAR_RED_SUGAR_LABEL', 'ISRAELI_RED_LABEL_1_SUGAR', 'ISRAELI_RED_LABELS_2_PLUS', 'SNACK_BAR_HIGH_CAL', 'NOVA_PROXY_3_PROCESSED', 'ISRAELI_RED_LABEL_1_SAT_FAT']
- PENALTIES: ['HIGH_CAL_HIGH_SUGAR_SOFT', 'HIGH_CAL_LOW_SATIETY_SOFT', 'HP_FAT_SUGAR_COMBO']

### bsip1_5900020015174
**חטיפי דגנים פיטנס שוקולד מריר שישייה**  
Score: 27.8 (E) | Category: snack_bar_granola | NOVA: 4 | Confidence: 87 (high)  
Flags: 1 | Instability: True | Status: standard  

**Flags:**
- CATEGORY_INSTABILITY: primary=snack_bar_granola secondary=cereal, confidence=0.57

**Score drivers:**
- DOMINANT: Binding cap=55 from rules: ['SNACK_BAR_RED_SUGAR_LABEL', 'ISRAELI_RED_LABEL_1_SUGAR', 'NOVA_PROXY_4_ULTRA_PROCESSED', 'ADDITIVE_MARKERS_3_PLUS']
- PENALTIES: ['MULTIPLE_ADDED_SUGAR_MARKERS', 'LONG_INGREDIENT_LIST', 'SEED_OIL_PRESENT']

### bsip1_7290018333952
**חטיף אגוזים וחמוציות רפאלס 5*30 גרם**  
Score: 50 (insufficient_data) | Category: whole_food_fat | NOVA: 2 | Confidence: 5 (insufficient)  
Flags: 2 | Instability: False | Status: context_limited  

**Flags:**
- CONTEXT_LIMITED: per-100g score may be misleading (no_nutrition_data)
- LOW_NOVA_CONFIDENCE: NOVA inference unreliable (0.2)

**Score drivers:**
- DOMINANT: Confidence ceiling active at 50 (data quality limitation)
- FLOOR APPLIED: whole_food_fat_nova1_2 → minimum 65

### bsip1_7290019545545
**חטיף פאי פקאן רפאלס 5*30 גרם**  
Score: 50 (insufficient_data) | Category: snack_bar_granola | NOVA: 2 | Confidence: 5 (insufficient)  
Flags: 2 | Instability: False | Status: context_limited  

**Flags:**
- CONTEXT_LIMITED: per-100g score may be misleading (no_nutrition_data)
- LOW_NOVA_CONFIDENCE: NOVA inference unreliable (0.2)

**Score drivers:**
- DOMINANT: Confidence ceiling active at 50 (data quality limitation)

## 5 Most Correct Products

These products show the clearest, most defensible scoring traces.

### bsip1_7290011498870
**חטיף תמרים במילוי חמאת שקדים**  
Score: 65 (C) | Category: whole_food_fat | NOVA: 2 | Confidence: 80 (high)  

**Drivers:**
- PRIMARY SIGNAL: nutrient_density=5.2 (lowest dimension)
- FLOOR APPLIED: whole_food_fat_nova1_2 → minimum 65

### bsip1_8423207206495
**מרבה סלים דליס שוקולד מריר חדש**  
Score: 56.7 (C) | Category: snack_bar_granola | NOVA: 3 | Confidence: 90 (high)  

**Drivers:**
- DOMINANT: Binding cap=75 from rules: ['NOVA_PROXY_3_PROCESSED']

### bsip1_8423207210287
**מרבה סלים דליס שוקולד לבן בטעם יוגורט**  
Score: 55.5 (C) | Category: dairy_protein | NOVA: 3 | Confidence: 82 (high)  

**Drivers:**
- DOMINANT: Binding cap=75 from rules: ['NOVA_PROXY_3_PROCESSED']

### bsip1_7290011498894
**חטיף תמרים במילוי חמאת בוטנים**  
Score: 55.0 (C) | Category: snack_bar_granola | NOVA: 2 | Confidence: 82 (high)  

**Drivers:**
- DOMINANT: Binding cap=55 from rules: ['HIGH_SUGAR_25G_PLUS', 'SNACK_BAR_RED_SUGAR_LABEL', 'ISRAELI_RED_LABEL_1_SUGAR']

### bsip1_16000548404
**קראנצ'י חטיף שיבולת שועל עם דבש חמישייה**  
Score: 51.4 (D) | Category: cereal | NOVA: 3 | Confidence: 90 (high)  

**Drivers:**
- DOMINANT: Binding cap=75 from rules: ['NOVA_PROXY_3_PROCESSED']
- PENALTIES: ['MULTIPLE_ADDED_SUGAR_MARKERS', 'SEED_OIL_PRESENT']
