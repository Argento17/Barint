P268 baseline contract drift report
========================================================================
SUMMARY: 5 conform, 8 non-conforming (of 13 shelves checked).

[NON-CONFORMING] bread  (bread_frontend_v3.json, 29 products)
  missing-required x58; forbidden-present (bestUseCases x29, consumerTakeaway x29, expansion.bottomLine x29, expansion.consumerExplanation x29); copy-hygiene x14
  missing-required:
    - bsip1_bread_7290016245325 missing-required:rank
    - bsip1_bread_7290016245325 missing-required:categoryTotal
    - bsip1_bread_3268429 missing-required:rank
    - bsip1_bread_3268429 missing-required:categoryTotal
    - bsip1_bread_3268252 missing-required:rank
    - bsip1_bread_3268252 missing-required:categoryTotal
    - bsip1_bread_481203 missing-required:rank
    - bsip1_bread_481203 missing-required:categoryTotal
    - bsip1_bread_481197 missing-required:rank
    - bsip1_bread_481197 missing-required:categoryTotal
    - bsip1_bread_574370 missing-required:rank
    - bsip1_bread_574370 missing-required:categoryTotal
    - bsip1_bread_3054183 missing-required:rank
    - bsip1_bread_3054183 missing-required:categoryTotal
    - bsip1_bread_2079033 missing-required:rank
    - bsip1_bread_2079033 missing-required:categoryTotal
    - bsip1_bread_2079927 missing-required:rank
    - bsip1_bread_2079927 missing-required:categoryTotal
    - bsip1_bread_497044 missing-required:rank
    - bsip1_bread_497044 missing-required:categoryTotal
    ... +38 more
  forbidden-present:
    - bestUseCases x29
    - consumerTakeaway x29
    - expansion.bottomLine x29
    - expansion.consumerExplanation x29
  copy-hygiene (14):
    - bsip1_bread_2079927 rowVerdict: E-code
    - bsip1_bread_2079927 expansion.comparisonContext: E-code
    - bsip1_bread_497044 expansion.comparisonContext: E-code
    - bsip1_bread_2079996 insightLine: E-code
    - bsip1_bread_2079996 rowVerdict: E-code
    - bsip1_bread_2079996 expansion.comparisonContext: E-code
    - bsip1_bread_7290018540329 insightLine: E-code
    - bsip1_bread_7290018540329 rowVerdict: E-code
    - bsip1_bread_7290018540329 expansion.comparisonContext: E-code
    - bsip1_bread_2079477 insightLine: E-code
    ... +4 more

[NON-CONFORMING] brined_cheeses  (brined_cheeses_frontend_v2.json, 36 products)
  missing-required x43; copy-hygiene x7
  missing-required:
    - bc-001 missing-required:expansion.comparisonContext
    - bc-004 missing-required:expansion.comparisonContext
    - bc-004 missing-required:expansion.limitingFactors (not array)
    - bc-005 missing-required:expansion.comparisonContext
    - bc-005 missing-required:expansion.limitingFactors (not array)
    - bc-003 missing-required:expansion.comparisonContext
    - bc-002 missing-required:expansion.comparisonContext
    - bc-008 missing-required:expansion.comparisonContext
    - bc-007 missing-required:expansion.comparisonContext
    - bc-009 missing-required:expansion.comparisonContext
    - bc-010 missing-required:expansion.comparisonContext
    - bc-013 missing-required:expansion.comparisonContext
    - bc-013 missing-required:expansion.limitingFactors (not array)
    - bc-006 missing-required:expansion.comparisonContext
    - bc-012 missing-required:expansion.comparisonContext
    - bc-011 missing-required:expansion.comparisonContext
    - bc-029 missing-required:expansion.comparisonContext
    - bc-014 missing-required:expansion.comparisonContext
    - bc-031 missing-required:expansion.comparisonContext
    - bc-031 missing-required:expansion.limitingFactors (not array)
    ... +23 more
  copy-hygiene (7):
    - bc-008 rowVerdict: E-code
    - bc-009 insightLine: E-code
    - bc-009 rowVerdict: E-code
    - bc-010 rowVerdict: E-code
    - bc-012 rowVerdict: E-code
    - bc-025 rowVerdict: E-code
    - bc-037 rowVerdict: E-code

[NON-CONFORMING] cakes  (cakes_hard_cookies_frontend_v1.json, 65 products)
  missing-required x65; forbidden-present (bariInterpretation x65, bestUseCases x65, consumerTakeaway x65, expansion.bottomLine x65); copy-hygiene x2
  missing-required:
    - cake_7290119030095 missing-required:expansion.comparisonContext
    - cake_7296073346340 missing-required:expansion.comparisonContext
    - cake_5718021 missing-required:expansion.comparisonContext
    - cake_7290119045013 missing-required:expansion.comparisonContext
    - cake_7290016162264 missing-required:expansion.comparisonContext
    - cake_5431920 missing-required:expansion.comparisonContext
    - cake_7290006983787 missing-required:expansion.comparisonContext
    - cake_5431913 missing-required:expansion.comparisonContext
    - cake_4504670 missing-required:expansion.comparisonContext
    - cake_2472261 missing-required:expansion.comparisonContext
    - cake_7290119039746 missing-required:expansion.comparisonContext
    - cake_9399288 missing-required:expansion.comparisonContext
    - cake_2472254 missing-required:expansion.comparisonContext
    - cake_1361207 missing-required:expansion.comparisonContext
    - cake_2472186 missing-required:expansion.comparisonContext
    - cake_5718038 missing-required:expansion.comparisonContext
    - cake_4504649 missing-required:expansion.comparisonContext
    - cake_4504656 missing-required:expansion.comparisonContext
    - cake_7290018893661 missing-required:expansion.comparisonContext
    - cake_4504687 missing-required:expansion.comparisonContext
    ... +45 more
  forbidden-present:
    - bariInterpretation x65
    - bestUseCases x65
    - consumerTakeaway x65
    - expansion.bottomLine x65
  copy-hygiene (2):
    - cake_7290119045013 rowVerdict: E-code
    - cake_7290016162264 rowVerdict: E-code

[CONFORMS] cereals  (cereals_frontend_v2.json, 20 products)
  CONFORMS (0 violations)

[NON-CONFORMING] cheese  (cheese_frontend_v4.json, 53 products)
  missing-required x106; forbidden-present (bariInterpretation x53, bestUseCases x53, consumerTakeaway x53, expansion.consumerExplanation x53); size-duplicate-sets x2; copy-hygiene x3
  missing-required:
    - bsip1_cheese_7290014758681 missing-required:rank
    - bsip1_cheese_7290014758681 missing-required:categoryTotal
    - bsip1_cheese_6040619 missing-required:rank
    - bsip1_cheese_6040619 missing-required:categoryTotal
    - bsip1_cheese_4127077 missing-required:rank
    - bsip1_cheese_4127077 missing-required:categoryTotal
    - bsip1_cheese_4127329 missing-required:rank
    - bsip1_cheese_4127329 missing-required:categoryTotal
    - bsip1_cheese_41445 missing-required:rank
    - bsip1_cheese_41445 missing-required:categoryTotal
    - bsip1_cheese_7290110321277 missing-required:rank
    - bsip1_cheese_7290110321277 missing-required:categoryTotal
    - bsip1_cheese_474502 missing-required:rank
    - bsip1_cheese_474502 missing-required:categoryTotal
    - bsip1_cheese_7290010945481 missing-required:rank
    - bsip1_cheese_7290010945481 missing-required:categoryTotal
    - bsip1_cheese_7290102393268 missing-required:rank
    - bsip1_cheese_7290102393268 missing-required:categoryTotal
    - bsip1_cheese_7290116934280 missing-required:rank
    - bsip1_cheese_7290116934280 missing-required:categoryTotal
    ... +86 more
  forbidden-present:
    - bariInterpretation x53
    - bestUseCases x53
    - consumerTakeaway x53
    - expansion.consumerExplanation x53
  size-duplicate-sets (2):
    - bsip1_cheese_4127329, bsip1_cheese_2868996, bsip1_cheese_7290011194246
    - bsip1_cheese_474502, bsip1_cheese_7290010945481, bsip1_cheese_7290102393268
  copy-hygiene (3):
    - bsip1_cheese_7290108504378 rowVerdict: E-code
    - bsip1_cheese_7290108502541 rowVerdict: E-code
    - bsip1_cheese_7622201521493 rowVerdict: E-code

[NON-CONFORMING] cookies_coffee  (cookies_coffee_frontend_v2.json, 119 products)
  missing-required x119; forbidden-present (bariInterpretation x119, bestUseCases x119, consumerTakeaway x63, expansion.bottomLine x119); size-duplicate-sets x1; copy-hygiene x1
  missing-required:
    - ck-7290013453693 missing-required:expansion.comparisonContext
    - ck-7290119043149 missing-required:expansion.comparisonContext
    - bsip1_cookies_80083764 missing-required:expansion.comparisonContext
    - ck-7290017962139 missing-required:expansion.comparisonContext
    - ck-7290020030184 missing-required:expansion.comparisonContext
    - ck-7290122781359 missing-required:expansion.comparisonContext
    - ck-7290013740113 missing-required:expansion.comparisonContext
    - ck-7290013453068 missing-required:expansion.comparisonContext
    - ck-540160 missing-required:expansion.comparisonContext
    - ck-7290013740137 missing-required:expansion.comparisonContext
    - ck-7290119043743 missing-required:expansion.comparisonContext
    - ck-7290013740557 missing-required:expansion.comparisonContext
    - ck-7290013740229 missing-required:expansion.comparisonContext
    - ck-960860015432 missing-required:expansion.comparisonContext
    - ck-7290013740472 missing-required:expansion.comparisonContext
    - ck-311463 missing-required:expansion.comparisonContext
    - ck-7290013453501 missing-required:expansion.comparisonContext
    - ck-7290013740052 missing-required:expansion.comparisonContext
    - ck-7290013740540 missing-required:expansion.comparisonContext
    - ck-7290013740465 missing-required:expansion.comparisonContext
    ... +99 more
  forbidden-present:
    - bariInterpretation x119
    - bestUseCases x119
    - consumerTakeaway x63
    - expansion.bottomLine x119
  size-duplicate-sets (1):
    - ck-46214731552, ck-46214930207, ck-7622300356767
  copy-hygiene (1):
    - ck-7290019816232 rowVerdict: E-code

[NON-CONFORMING] granola  (granola_frontend_v1.json, 25 products)
  missing-required x15; size-duplicate-sets x1
  missing-required:
    - bsip1_cereal_1164266 missing-required:expansion.limitingFactors
    - bsip1_cereal_7290017962047 missing-required:expansion.limitingFactors
    - bsip1_cereal_7290017962023 missing-required:expansion.positiveSignals
    - bsip1_cereal_7290017962023 missing-required:expansion.limitingFactors
    - bsip1_cereal_7290013433244 missing-required:expansion.limitingFactors
    - bsip1_cereal_7290013433336 missing-required:expansion.positiveSignals
    - bsip1_cereal_7290013433336 missing-required:expansion.limitingFactors
    - bsip1_cereal_1164273 missing-required:expansion.limitingFactors
    - bsip1_cereal_7290106771161 missing-required:expansion.positiveSignals
    - bsip1_cereal_7290013433091 missing-required:expansion.positiveSignals
    - bsip1_cereal_7290013433091 missing-required:expansion.limitingFactors
    - bsip1_cereal_7613037012095 missing-required:expansion.positiveSignals
    - bsip1_cereal_7290011131050 missing-required:expansion.positiveSignals
    - bsip1_cereal_7613035622623 missing-required:expansion.positiveSignals
    - bsip1_cereal_7290011131975 missing-required:expansion.positiveSignals
  size-duplicate-sets (1):
    - bsip1_cereal_7290014471443, bsip1_cereal_7290011131968

[CONFORMS] hard_cheeses  (hard_cheeses_frontend_v2.json, 23 products)
  CONFORMS (0 violations)

[NON-CONFORMING] hummus  (hummus_frontend_v5.json, 57 products)
  missing-required x80; forbidden-present (expansion.unknowns x57); size-duplicate-sets x6
  missing-required:
    - bsip1_7296073725404 missing-required:expansion.comparisonContext
    - bsip1_6666307 missing-required:expansion.comparisonContext
    - bsip1_7296073725565 missing-required:expansion.comparisonContext
    - bsip1_7296073725589 missing-required:expansion.comparisonContext
    - bsip1_6666444 missing-required:rowVerdict
    - bsip1_6666444 missing-required:expansion.comparisonContext
    - bsip1_7290015858175 missing-required:rowVerdict
    - bsip1_7290015858175 missing-required:expansion.comparisonContext
    - bsip1_7290110564360 missing-required:expansion.comparisonContext
    - bsip1_7290110579319 missing-required:expansion.comparisonContext
    - bsip1_7290110557478 missing-required:expansion.comparisonContext
    - bsip1_7290011800642 missing-required:rowVerdict
    - bsip1_7290011800642 missing-required:expansion.comparisonContext
    - bsip1_7296073725381 missing-required:expansion.comparisonContext
    - bsip1_3727667 missing-required:expansion.comparisonContext
    - bsip1_7290106576513 missing-required:expansion.comparisonContext
    - bsip1_5174551 missing-required:expansion.comparisonContext
    - bsip1_7290105964564 missing-required:expansion.comparisonContext
    - bsip1_2987963 missing-required:expansion.comparisonContext
    - bsip1_8645935 missing-required:expansion.comparisonContext
    ... +60 more
  forbidden-present:
    - expansion.unknowns x57
  size-duplicate-sets (6):
    - bsip1_7296073725589, bsip1_7290105964564, bsip1_2987963, bsip1_8645935
    - bsip1_6666444, bsip1_7290010931330
    - bsip1_7290015858175, bsip1_6724786, bsip1_7296073451969
    - bsip1_7290110579319, bsip1_7290110557478
    - bsip1_3727667, bsip1_7290106576513
    - bsip1_7290104061424, bsip1_7290115202434

[CONFORMS] juices  (juices_frontend_v3.json, 17 products)
  CONFORMS (0 violations)

[NON-CONFORMING] milk  (milk_frontend_v1.json, 18 products)
  missing-required x18
  missing-required:
    - milk_7290000051352 missing-required:confidence_sub_reason
    - milk_7290019790259 missing-required:confidence_sub_reason
    - milk_7290102392094 missing-required:confidence_sub_reason
    - milk_7290114313865 missing-required:confidence_sub_reason
    - milk_7290116936116 missing-required:confidence_sub_reason
    - milk_7290110324926 missing-required:confidence_sub_reason
    - milk_7290107932134 missing-required:confidence_sub_reason
    - milk_7290014760141 missing-required:confidence_sub_reason
    - milk_7394376620904 missing-required:confidence_sub_reason
    - milk_7290119385560 missing-required:confidence_sub_reason
    - milk_7394376619939 missing-required:confidence_sub_reason
    - milk_7394376621451 missing-required:confidence_sub_reason
    - milk_5411188124689 missing-required:confidence_sub_reason
    - milk_8000215204554 missing-required:confidence_sub_reason
    - milk_7290110325619 missing-required:confidence_sub_reason
    - milk_8000215204219 missing-required:confidence_sub_reason
    - milk_5411188112709 missing-required:confidence_sub_reason
    - milk_5411188300328 missing-required:confidence_sub_reason

[CONFORMS] protein_bars  (protein_bars_frontend_v1.json, 16 products)
  CONFORMS (0 violations)

[CONFORMS] snacks  (snacks_frontend_v5.json, 21 products)
  CONFORMS (0 violations)

NON-CONFORMING SHELVES:
  - bread: missing-required x58; forbidden-present (bestUseCases x29, consumerTakeaway x29, expansion.bottomLine x29, expansion.consumerExplanation x29); copy-hygiene x14
  - brined_cheeses: missing-required x43; copy-hygiene x7
  - cakes: missing-required x65; forbidden-present (bariInterpretation x65, bestUseCases x65, consumerTakeaway x65, expansion.bottomLine x65); copy-hygiene x2
  - cheese: missing-required x106; forbidden-present (bariInterpretation x53, bestUseCases x53, consumerTakeaway x53, expansion.consumerExplanation x53); size-duplicate-sets x2; copy-hygiene x3
  - cookies_coffee: missing-required x119; forbidden-present (bariInterpretation x119, bestUseCases x119, consumerTakeaway x63, expansion.bottomLine x119); size-duplicate-sets x1; copy-hygiene x1
  - granola: missing-required x15; size-duplicate-sets x1
  - hummus: missing-required x80; forbidden-present (expansion.unknowns x57); size-duplicate-sets x6
  - milk: missing-required x18
