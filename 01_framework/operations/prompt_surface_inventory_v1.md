# Prompt & LLM-Output Surface Inventory — v1

**Task:** TASK-BARI-PROMPT-REGISTRY-CI-EVAL-V1 (Deliverable 5)
**Status:** Discovery complete — PASS (see §8)
**Created:** 2026-06-10
**Author:** dev-agent (discovery pass)
**Scope:** Identify every Bari prompt / LLM-output surface that may affect product
quality, data quality, scoring, explanations, Hebrew copy, comparison pages,
routing, or task closure. **This is discovery only** — no registry built, no
production prompts modified, no scoring changed, no eval examples created.

---

## 1. Central architectural finding (read first)

**Bari makes ZERO programmatic LLM API calls in its own production code.** Every
`anthropic` / `openai` / `litellm` SDK import in the tree lives under `.venv/`
(third-party libraries). The data pipeline is **fully deterministic**:

- `category_classifier.py` / `router_v2.py` → rule-based Hebrew keyword routing.
- `signal_extractor.py` / `ingredient_taxonomy.py` → deterministic extraction.
- `build_*_frontend*.py` / `build_*_explanation*.py` → fixed phrase-table copy;
  `build_hummus_explanation_v1.py` states it explicitly: *"DETERMINISTIC ONLY.
  No LLM-generated copy … the same evidence always yields byte-identical output."*
- `score_engine.py`, `nova_proxy.py`, `structural_classifier.py` → deterministic.

LLM involvement enters Bari through **two distinct, non-runtime channels**:

- **Channel A — LLM-as-operator (Agent OS).** Claude Code agents read instruction
  files (`.claude/agents/*.md`, commands, skills, operations specs) and *do the
  work* — authoring copy, extracting evidence, closing tasks, routing. These
  instruction files **are** the "system prompts." They affect product/data quality
  **indirectly**, through what the agent produces.
- **Channel B — LLM-authored artifacts (copy).** Consumer-facing Hebrew copy
  (insightLines, rowVerdicts, category caveats, hero/methodology text) is generated
  by the Content Agent (LLM) and then **frozen into `.ts` / `.json` files**. These
  are the actual LLM *outputs* that reach consumers.

**Implication for the later deliverables (registry/CI/eval):** there is no live
inference boundary to wrap. A "prompt regression" in Bari = a change to an agent
instruction file or editorial spec that changes how *future* artifacts are
produced. Eval must therefore run at the **artifact-generation level** (regenerate
copy from a candidate spec/agent prompt → compare to baseline artifact), not at an
API call site. This reframes the CI design and must be carried into Deliverable 3.

A second consequence: the deterministic surfaces (§5) should be guarded by **diff
/ schema regression** (much of which already exists — `router_regression_corpus.json`,
`run_regression_check.py`, `run_router_regression.py`), **not** by an LLM eval.
They are listed here for completeness and to mark the boundary, but they do **not**
need pairwise-judge eval coverage.

---

## 2. Tier 1 — LLM-output surfaces, consumer-facing (HIGH risk)

These are authored by the Content Agent (LLM) and shipped to consumers. Highest
priority for registry + eval.

| # | File / location | Surface name | Type | Affects | Risk | Needs |
|---|-----------------|--------------|------|---------|------|-------|
| T1-01 | `bari-web/src/lib/comparisons/*-page-data.ts` (milk, bread, snacks, cheese, hard-cheeses, hummus, cereals, granola, butter, juices, maadanim, salty-snacks, yogurts, vegetable-spreads) | Comparison-page copy: `insightLine` / `rowVerdict` per product | Hebrew copy prompt | explanation, consumer copy | **high** | registry, eval, pairwise judge, manual review |
| T1-02 | `milk-editorial-content.ts`, `bread-editorial-content.ts`, `milk-product-insights.ts` | Per-product editorial insight blocks | Hebrew copy prompt | consumer copy | **high** | registry, eval, pairwise judge |
| T1-03 | Each `*-page-data.ts` (category caveat box) | "הערת קטגוריה" category caveat — standard on every page | Hebrew copy prompt | consumer copy | **high** | registry, eval, pairwise judge, manual review |
| T1-04 | `*-page-data.ts` expansion arrays + `consumer-explanation-view.ts` | Score explanation: `positiveSignals` / `limitingFactors` / `unknowns` / `caveats` (where authored, not phrase-table) | scoring explanation prompt | explanation, consumer copy | **high** | registry, eval, pairwise judge, schema validation |
| T1-05 | `bari-web/src/components/home/content.ts`, `home-hero.tsx`, `home-methodology.tsx`, `home-flagship-analysis.tsx`, `home-category-intelligence.tsx` | Homepage + methodology consumer copy | Hebrew copy prompt | consumer copy | **high** | registry, eval, pairwise judge |
| T1-06 | `02_products/hummus/hummus_content_v3.json`, `02_products/bread_retail_002/wolt_venue_content.json` | Authored content JSON (caveated product messages, venue copy) | Hebrew copy prompt | consumer copy | medium | registry, eval, pairwise judge |
| T1-07 | `01_framework/glass_box/methodology_glass_box_page_v1.md`, `w1_disclosure_copy_v1.md`, `w2_additive_copy_v1.md`, `d3_demoralization_spec_v1.md` | Glass-box / methodology consumer copy specs | Hebrew copy prompt | consumer copy, explanation | **high** | registry, eval, pairwise judge, manual review |

---

## 3. Tier 2 — LLM-instruction surfaces governing copy generation (the "prompts")

These specs **are** the prompts that constrain Channel-B generation. A change here
changes all future copy → they are the true "prompt_id"s for consumer copy.

| # | File | Surface name | Type | Affects | Risk | Needs |
|---|------|--------------|------|---------|------|-------|
| T2-01 | `.claude/agents/content-agent.md` (230 lines) | Content Agent system prompt — author of all consumer copy | system prompt / agent instruction | consumer copy, explanation | **high** | registry, eval (regen-vs-baseline), pairwise judge |
| T2-02 | `01_framework/editorial/insight_line_spec_v1.md` | Insight line generation spec | user template / copy prompt | consumer copy | **high** | registry, eval, pairwise judge |
| T2-03 | `01_framework/editorial/assertive_writing_v1.md` | Assertive-writing rules + phrase library + no-apology rule | copy prompt | consumer copy | **high** | registry, eval, pairwise judge |
| T2-04 | `01_framework/editorial/editorial_intelligence_v3.md` | Canonical editorial OS (insight-first, framework invisibility) | copy prompt | consumer copy | **high** | registry, manual review |
| T2-05 | `01_framework/editorial/row_description_standard_v1.md`, `row_description_grounding_v1.md` | Row verdict standard + grounding rules | copy prompt | consumer copy | **high** | registry, eval, pairwise judge, schema validation |
| T2-06 | `01_framework/editorial/bsip2_to_web_translation_contract_v1.md` | BSIP2→web copy translation contract | copy prompt / schema contract | explanation, consumer copy | **high** | registry, schema validation, eval |
| T2-07 | `01_framework/editorial/score_presentation_v1.md` | Score display rules (numeric/grade only; no strength labels) | copy prompt / schema contract | consumer copy, explanation | medium | registry, schema validation |
| T2-08 | `01_framework/editorial/bari_explanation_framework_v1.md`, `editorial_interpretation_v1.md` | Explanation framework + interpretation rules | scoring explanation prompt | explanation | **high** | registry, eval, pairwise judge |
| T2-09 | `01_framework/editorial/hebrew_content_golden_eval_v1.md` (TASK-220) | **Existing** Hebrew content golden-eval framework (D1–Dn dimensions, 30–50 set) | eval harness spec | consumer copy | n/a (this is the eval, not a prompt) | adopt as Deliverable 2 seed |
| T2-10 | `01_framework/editorial/blog_template_v1.md` | Blog/long-form content template | copy prompt | consumer copy (marketing) | low | registry, manual review |

---

## 4. Tier 3 — Agent OS operational LLM surfaces (data/registry quality, MEDIUM)

Channel-A instruction surfaces. They don't emit consumer copy directly but govern
agents whose output affects data quality, evidence, scoring decisions, and registry
state (incl. the closure-verification gate).

| # | File | Surface name | Type | Affects | Risk | Needs |
|---|------|--------------|------|---------|------|-------|
| T3-01 | `.claude/agents/nutrition-agent.md` | Nutrition/scoring-philosophy agent | agent instruction | score, explanation | **high** | registry, manual review |
| T3-02 | `.claude/agents/data-agent.md` | Data pipeline agent (shelf map, corpus, enrichment, JSON gen) | agent instruction | score, ingredients, category, data | **high** | registry, manual review, schema validation |
| T3-03 | `.claude/agents/research-agent.md` | Research / **evidence extraction** agent | extraction/classification prompt | evidence/explanation, score (indirect) | **high** | registry, eval, pairwise judge |
| T3-04 | `.claude/agents/qa-agent.md` | QA / propagation-verification agent | task closure / QA prompt | registry/data state | medium | registry, eval (claim-vs-artifact), manual review |
| T3-05 | `.claude/agents/red-team-agent.md` | Adversarial methodology challenge agent | agent instruction | score (indirect), methodology | medium | registry, manual review |
| T3-06 | `.claude/agents/product-agent.md` | Product strategy / prioritization agent | agent instruction | registry/internal | low | registry, manual review |
| T3-07 | `.claude/agents/design-agent.md`, `frontend-agent.md` | UX/implementation agents | agent instruction | consumer copy (indirect), internal | low–medium | registry, manual review |
| T3-08 | `.claude/agents/marketing-agent.md` | Marketing/SEO agent | agent instruction | consumer copy (marketing) | medium | registry, manual review |
| T3-09 | `.claude/agents/cc-agent.md` | **DEPRECATED (2026-06-10, ADR-004)** CC operational agent | agent instruction | registry state | low (archive) | registry note only |
| T3-10 | `.claude/commands/cc.md`, `roadmap.md` | Registry-query + roadmap command prompts | agent instruction | registry/internal | medium | registry, eval (claim-vs-artifact) |
| T3-11 | `.claude/skills/bari-bsip2-scoring-governance/`, `bari-category-factory/`, `bari-frontend-ui/`, `bari-qa-audit/` | Skill instruction prompts | agent instruction | score, data, consumer copy, QA | medium–**high** | registry, manual review |
| T3-12 | `01_framework/operations/agent_router_v1.md` | **Agent routing** spec | agent instruction (routing) | registry/internal | medium | registry, eval (routing decisions) |
| T3-13 | `01_framework/operations/orchestration_model_v1.md`, `registry_protocol_v1.md`, `registry_first_rule_v1.md`, `work_classification_v1.md` | **Task closure** + orchestration + classification specs | task closure / QA prompt | registry/data state | medium | registry, eval (claim-vs-artifact) |

---

## 5. Deterministic surfaces — look like prompts, are NOT LLM (EXCLUDE from eval)

Documented to mark the boundary. Guard with **diff/schema regression**, not LLM eval.

| # | File | Why excluded |
|---|------|--------------|
| D-01 | `03_operations/bsip2/proto_v0/src/category_classifier.py`, `router_v2.py` | Rule-based Hebrew keyword routing; existing `router_regression_corpus.json` + `run_router_regression.py` |
| D-02 | `signal_extractor.py`, `ingredient_taxonomy.py`, `input_loader.py` | Deterministic ingredient parsing/extraction (regex + taxonomy tables) |
| D-03 | `build_hummus_explanation_v1.py`, `build_cheese_frontend*.py`, all 24 `build_*_frontend*.py` / `build_*_explanation*.py` | Fixed phrase-table copy; byte-identical for identical inputs |
| D-04 | `score_engine.py`, `nova_proxy.py`, `structural_classifier.py`, `score_synthesis.py` | Deterministic scoring; covered by golden corpus + `run_regression_check.py` |
| D-05 | `scrape_bread_retail.py`, `_shared/bsip0_nutrition.py` | Deterministic scrapers/parsers (EV-029 was a parser fix, not LLM) |

---

## 6. Scope-item → surface mapping (task's 7 required scope areas)

| Scope area (task) | Primary surface(s) | LLM? | Risk |
|-------------------|--------------------|------|------|
| Ingredient parsing | D-02 (deterministic) | **No** | low (regression only) |
| Product categorization | D-01 (deterministic) | **No** | low (regression only) |
| Evidence extraction | T3-03 research-agent (agent-mediated) | Yes (Channel A) | **high** |
| Score explanation generation | T1-04, T2-08, T2-06; D-03 where phrase-table | Mixed | **high** where authored |
| Hebrew consumer-facing text | T1-01..T1-07, T2-01..T2-08 | Yes (Channel B) | **high** |
| Comparison page generation | T1-01..T1-04 (copy authored; scores imported/frozen) | Yes (copy only) | **high** |
| Agent routing / task closure | T3-04, T3-10, T3-12, T3-13 | Yes (Channel A) | medium |

---

## 7. Recommended first 50-example eval-set composition

Weighted toward the genuinely-LLM, consumer-facing surfaces. Build on the existing
`hebrew_content_golden_eval_v1.md` (TASK-220) D-dimension scoring as the judge rubric.

| Bucket | Surfaces | Examples | Method |
|--------|----------|----------|--------|
| Comparison copy (insightLine + rowVerdict) | T1-01, T1-02, T2-02, T2-05 | **18** | pairwise judge |
| Category caveats ("הערת קטגוריה") | T1-03, T2-04 | **6** | pairwise judge + manual |
| Score explanation arrays | T1-04, T2-06, T2-08 | **10** | schema validation + pairwise judge |
| Homepage / methodology / glass-box copy | T1-05, T1-07 | **4** | pairwise judge |
| Evidence-extraction claim fidelity | T3-03 | **6** | pairwise judge (claim vs source) |
| Task-closure verification (return-block claim vs artifact) | T3-04, T3-10, T3-13 | **6** | pairwise judge (correct accept/return?) |
| **Total** | | **50** | |

Notes:
- Categorization & ingredient parsing are **deliberately excluded** from the 50 —
  they're deterministic and already have regression corpora (§5). Their CI gate is
  schema/diff regression, tracked separately under the registry's "schema validity"
  and "score-affecting classification delta" thresholds.
- The four task thresholds map cleanly: schema validity → T1-04/T2-06 structured
  arrays; classification delta → §5 deterministic regression; unsafe wording →
  pairwise-judge buckets above (assertive_writing + score_presentation rules);
  unexplained score delta → §5 score regression.

---

## 8. PASS / RETURNED recommendation

**Recommendation: PASS** for discovery completeness.

- All eight requested scope locations swept (`03_operations/bsip2/`,
  `01_framework/`, agent defs, command files, explanation engine, Hebrew copy gen,
  comparison page gen, categorization/parsing/enrichment, router/closure/QA, inline
  prompt-like strings). `04_bsip2/` does **not** exist (work lives under
  `03_operations/bsip2/proto_v0/` and `01_framework/bsip2_framework/`) — noted, not
  a gap.
- The decisive finding (no programmatic LLM calls; LLM enters via Channel A/B) is
  established and reframes the later deliverables.
- A pre-existing eval asset (`hebrew_content_golden_eval_v1.md`) was found and
  should seed Deliverable 2.

### Gaps / unknowns to resolve during registry build (Deliverables 1–4)

1. **Per-category authored-vs-deterministic audit.** Only hummus + cheese builders
   were confirmed phrase-table. The remaining `*-page-data.ts` copy needs a
   per-category pass to mark which `insightLine`/`rowVerdict`/explanation strings
   are LLM-authored (eval) vs imported from a deterministic builder (regression).
2. **Evidence extraction has no code surface** — it is agent-mediated. The
   "prompt_id" is `research-agent.md`; the eval must compare *extracted claims to
   cited sources*, not a code output. Confirm this modeling with Research/Nutrition.
3. **No LLM confirmed in scrapers/enrichment**, but enrichment evolves — add a
   CI tripwire that fails if any `anthropic`/`openai`/`litellm` import appears
   **outside `.venv/`**, so a future live LLM call cannot bypass the registry.
4. **Agent/skill instruction versioning** — these `.md` files are currently
   versioned only by git. The registry must assign them `prompt_id` + `version` +
   `rollback_version` distinct from their filename.

**Counts:** see §9.

---

## 9. Discovery summary

- **Files / locations scanned:** ~8 scope trees swept (full `03_operations/bsip2/proto_v0/src/` ≈ 150 py files; `01_framework/` editorial + glass_box + operations; 11 agent defs; 2 command files; 4 skill dirs + persona md; ~48 `bari-web/src/lib/comparisons/*.ts`; home components; product content JSON). SDK-import sweep run across entire tree (only `.venv/` hits).
- **LLM surfaces found (registry candidates):** **30** — Tier 1: 7 · Tier 2: 10 · Tier 3: 13.
- **Deterministic surfaces documented (excluded from eval):** 5 classes (§5).
- **High-risk surfaces:** **17** (T1-01,02,03,04,05,07; T2-01,02,03,04,05,06,08; T3-01,02,03,11-partial).
- **Recommended first eval set:** 50 examples, composition in §7.
- **Verdict:** PASS — discovery complete; 4 gaps logged for the registry-build phase.
