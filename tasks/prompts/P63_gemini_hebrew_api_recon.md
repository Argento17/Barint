# P63 / TASK-274 — Hebrew NLP/content API recon + wiring spec (route: C1-GEMINI)

You are the C1-GEMINI investigator on TASK-274 (repo root C:\Bari). This is RESEARCH + a wiring spec — do NOT close the task; return findings and propose RETURNED. Read tasks/TASK-274.md first.

## Why
Bari's Content Agent writes consumer-facing Hebrew copy (hero sentences, prologue, product verdicts, methodology). The owner finds its Hebrew under-powered and wants it reinforced with real Hebrew NLP/content libraries + APIs. Today the ONLY wired Hebrew tools are:
- `integrations/clients/hebrew_readability.py` — an OFFLINE heuristic (sentence/word length, leakage scan). Useful but not generative.
- HeBERT/hebEMO HF models (`avichr/heBERT_sentiment_analysis`, `avichr/hebEMO_anger`, `avichr/hebEMO_disgust`) — VERIFIED WORKING offline, but they are a sentiment/anger CLASSIFIER (a tone GATE), not a generator or lexical enrichment.
- DICTA Nakdan documented at `https://nakdan.dicta.org.il/api` — **this URL is DEAD (404). DICTA moved it.**

Environment facts (already verified by the orchestrator): `transformers`, `torch`, `huggingface_hub`, `requests` are installed; `HF_TOKEN` is set in `.env`; HF models cache + run offline.

## Your job — find what's CURRENT and LIVE, verify it, and spec the wiring
Investigate (use web search + actually hit the endpoints to confirm they respond — do NOT trust documentation, the Nakdan 404 proves docs go stale):

1. **DICTA API suite (https://dicta.org.il / https://api.dicta.org.il)** — find the CURRENT live endpoints for:
   - Nakdan / diacritization (the working URL + request shape).
   - Morphological analysis (lemma, POS, gender/number/person, construct state) — the highest-value tool for catching Hebrew agreement errors.
   - Any synonym / lexicon / "Hebrew thesaurus" service.
   For each: exact URL, HTTP method, request/response JSON shape, auth (key needed?), rate limits, and a REAL curl/python call you ran with its actual output.

2. **Generative Hebrew** — evaluate `dicta-il/dictalm2.0-instruct` (and any newer Dicta-LM) on Hugging Face as a local generative Hebrew model for phrasing enrichment: size, VRAM/CPU feasibility on a Windows box with torch installed (no dedicated GPU assumed), license, and whether it's realistically runnable here or needs an API. Note any hosted Hebrew-generation API alternatives.

3. **Hebrew lexical resources** — Hebrew WordNet, synonym lists, idiom/collocation resources usable offline or via free API, for varied non-repetitive phrasing.

4. **Agreement/grammar checker** — what's the best available way (DICTA morphology or otherwise) to programmatically catch Hebrew gender/number/construct-state agreement errors in a short copy string.

## Hard guards
- This is consumer COPY tooling, NOT a data source. **The OFF (Open Food Facts) ban is irrelevant here but do not introduce any nutrition/ingredient data source.**
- Verify reachability for REAL — paste the actual command + actual response for every endpoint you claim is live. An unverified "it should work" is worthless (that's how the Nakdan 404 shipped). If you cannot reach an endpoint from this environment, say so explicitly.
- Do NOT install heavy models or write client code in this pass — this is recon + a spec. (Wiring happens next, by the orchestrator/Cursor, from your spec.)
- No web deploy, no commits.

## Return (propose RETURNED, do not close)
- A ranked table of recommended Hebrew tools to wire: name | type (gate/generator/lexicon/morphology/diacritization) | live endpoint or HF id | auth | verified? (paste proof) | feasibility here | what Content gains.
- For the top 3: a concrete wiring spec (a `integrations/clients/<name>.py` signature sketch + how content-agent.md should reference it + the gate rule).
- An honest call on `dictalm2.0-instruct` runnability on this box.
- The machine-readable return contract JSON (01_framework/operations/return_contract_v1.md).
