# P245 / Zinc worldwide benchmark (route: C3)

You are the outside-the-family research lane. Build an evidence-grounded WORLDWIDE BENCHMARK for ZINC
oral supplements, same structure as a prior magnesium benchmark. Evidence only — no code, no scoring.
Every numeric value carries an inline citation (URL/reference). Do NOT use Open Food Facts for anything.

========================  ACTIVE PARAMETERS  ========================
ACTIVE: zinc
ELEMENTAL FRACTIONS (compound → elemental Zn; correct any with a better cited source):
  zinc oxide ~80%, zinc sulfate monohydrate ~36% / heptahydrate ~22.7%, zinc citrate ~31%,
  zinc acetate dihydrate ~30%, zinc picolinate ~20%, zinc methionine ~20%,
  zinc gluconate ~14.3%, zinc bisglycinate ~14–20% (varies)
COMMON USES/CLAIMS: RDA repletion, immune support, common-cold duration (lozenges),
  skin/acne, wound healing, taste/smell (deficiency), male fertility/testosterone
=====================================================================

## Deliver (same sections as the magnesium benchmark)
1. **Reference-perfect anchor table** by use/claim: defensible elemental dose band, evidence tier
   (Strong/Moderate/Weak/Insufficient), best reference form, UL, authority/claim position.
   Ground in: NIH ODS Zinc fact sheet; IOM/NAM DRI (RDA men 11 / women 8 mg; UL 40 mg); EFSA DRV +
   Article 13.1 authorized claims (immune, cognition, fertility, bone, etc.); WHO/FAO; Cochrane on
   zinc for common cold; relevant meta-analyses. Note the elemental-vs-compound trap (zinc oxide ~80%
   elemental but variable absorption; the picolinate/citrate/gluconate absorption debate).
2. **Form ranking + honest-label bar** — rank by direct human bioavailability evidence; flag where
   marketing outruns evidence (as glycinate did for magnesium). Label-honesty: elemental Zn per serving,
   named species, claim matched to evidence, copper-balance note for long-term high-dose zinc.
3. **Safety** — UL 40 mg elemental (basis: copper-deficiency / immune effects, not just GI). Note the
   copper-depletion risk at chronic high intake — distinctive to zinc.
4. **Per-region real-shelf sample** (US / EU / Canada): real zinc-primary products with brand, form,
   elemental mg/day, claim, price+currency+retailer+date, source URL. State sample sizes; EU partial.
   (Price recorded per-region only; not compared across countries.)
5. **Divergences & limitations** — RDA/UL differences across authorities; phytate-dependent EFSA
   requirements; data gaps.

## Return — IMPORTANT output handling
Write your full benchmark to the file `03_operations/supplement_engine/proto_v0/benchmark/zinc_benchmark_v1_draft.md`
(NOT to any tasks/returns/ path — that path gets overwritten). THEN ALSO paste the ENTIRE benchmark
verbatim as your final text response (so it is captured even if the file is lost).
Content: the benchmark spec table, form ranking, safety, the per-region shelf sample,
divergences/limitations, and a source list with URLs. Mark anything unverifiable as "not found".
