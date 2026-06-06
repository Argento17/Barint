# Evidence Grading SOP v1

**Who this is for:** Research Agent, when adding a study to a registry entry.
**When to use it:** Any time you are asked to add a `study_objects:` block to an EV entry.
**What it produces:** One or more filled-in `EvidenceStudy` records (see `evidence_study_schema.py`).

---

## The 7 fields — plain-language guide

**1. `claim`**
Write one sentence describing exactly what the study measured and found. Use the claim vocabulary below where possible — consistent wording makes entries searchable.
- Good: `"Regular supplementation reduces triglycerides by ~15% at 2–4 g/day EPA+DHA"`
- Too vague: `"Omega-3 is good for the heart"`
- Too narrow: `"EPA ethyl ester at 4 g/day reduces fasting TG from 282 to 235 mg/dL in REDUCE-IT statin users"`

Preferred claim vocabulary: `triglyceride lowering`, `blood pressure reduction`, `fracture reduction`, `fermentation produces SCFA`, `emulsifier disrupts gut barrier`, `live culture detected`, `status correction (raises serum level)`, `sleep-onset reduction`, `ergogenic performance`, `NTD prevention`, `anaemia correction`, `cold duration reduction`.

---

**2. `dose_realistic`**
Ask: "Is the dose in this study something a person would actually get from a real product?"
- True if the study dose is at or below **twice the typical label dose** for that ingredient/food.
- False if the study used 5×, 10×, or 100× a real-world serving.
- For dietary pattern studies (whole-food categories), mark True and note "dietary pattern design" in `notes`.

---

**3. `population_direct`**
Ask: "Are the people in this study similar to a typical Israeli adult consumer?"
- True if: healthy adults, aged 18–65, no diagnosed condition relevant to the claim.
- False if: children, elderly (65+), diagnosed patients (e.g., diagnosed hypertension for a blood pressure claim), elite athletes, animals, or cell lines.
- Always explain False in `notes`.

---

**4. `rob_grade`** — Risk of bias
Pick one:
- `low` — Randomized, blinded, pre-registered, controlled, adequate sample, low dropout.
- `moderate` — Mostly well-designed but one meaningful gap (e.g., open-label, short duration, modest n).
- `high` — Observational or uncontrolled, or an RCT with major protocol problems.
- `very_high` — Case report, self-report only, industry-funded with no independent replication, animal or cell study.

---

**5. `evidence_tier`**
This is your overall quality verdict on THIS study, not the whole body of evidence.
- `A` — Strong: high-quality RCT or a systematic review of multiple consistent RCTs.
- `B` — Moderate: reasonable RCT or consistent observational findings; mechanism plausible.
- `C` — Weak: small samples, short duration, animal/in-vitro data only.
- `D` — Insufficient: single low-quality study, purely theoretical, or anecdotal.

When the registry entry has multiple `study_objects:`, the entry-level `evidence_strength` field synthesizes across all of them. A mix of A and C studies is usually a B overall.

---

**6. `source_doi`**
Provide the DOI in format `"10.XXXX/..."`, or `"PMID:XXXXXXXX"` if no DOI is available, or `"internal:[doc-name]"` for Bari's own research documents.

Before finalizing: run `crossref.get_doi()` on the DOI and check `is_retracted` and `update_types`. If retracted, do not use the study. Note corrections in `notes`.

---

**7. `notes`**
Write anything that affects how to interpret the result. Required when:
- The study was industry-funded — name the funder.
- `dose_realistic` is False — explain the gap.
- `population_direct` is False — describe who was actually studied.
- There is a meaningful effect size worth recording.
- There is a correction, retraction flag, or methodological caveat the tier does not capture.

If nothing applies, write `"None"`.

---

## How many studies per entry?

- Minimum: 1 (the most directly relevant study).
- Preferred: 2–4 representative studies (the strongest, the weakest, and if contested, one on each side).
- Do not list every study in a meta-analysis — cite the meta-analysis as one object.

---

## What this SOP does NOT authorize

- A study object does not create a scoring rule. Scoring rules are governed separately (D7 authority).
- A study object does not change any published score. It is a quality record for the registry entry.
- Evidence tiers here inform, but do not automatically set, the entry-level `evidence_strength` field — that synthesis is a Nutrition Agent judgment.
