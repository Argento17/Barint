# Bari Router v4.2 — Orchestrator Routing Law

*Owner-directed 2026-06-14. Canonical routing law for all dispatched work. Supersedes
`lane_routing_rules_v1.md` (retained as the wire-level implementation appendix). Referenced by
`.claude/commands/orchestrate.md`, `tasks/DISPATCH_BOARD.md`, `AGENTS.md`.*

> **One sentence:** the Orchestrator routes every task by **band** (what function / whose authority),
> picks the **engine** that is best at that function, runs builders **in parallel** by decomposing the
> work, and **nothing ships until a deterministic C0 validator passes** — no model's opinion can override
> C0.

---

## The bands — one number per function (top = most authority)

A **band is a function**, not an engine. Some engines wear more than one hat (Gemini builds *and*
researches; Grok builds *and* designs). The band says *what role*; the engine says *who does it*.

| Band | Function | Engine(s) | Closes work? |
|---|---|---|---|
| **C5** | **Owner (Tom)** — final product release, the 5 strategic tripwires | Tom | **only band that authorizes public launch** |
| **C4** | **Orchestrator** — routes, decomposes, verifies, closes; never routine-codes | Opus via `/orchestrate` | closes tracked work on **C0** evidence |
| **C3** | **Strategic challenge / advisor** — devil's advocate before big calls | ChatGPT (gpt-5.5) | **never** — advises only, never builds or closes |
| **C2.1** | **Audit** — cheap validation + contradiction-hunting; *nothing complex routes here* | **DeepSeek** (only) | proposes findings; never closes |
| **C2.2** | **Research** — web-grounded research / source packs | **Gemini** | proposes evidence; never closes |
| **C2.3** | **Design** — visual / design concepts (mood, illustration, layout spikes) | **Grok** | proposes concepts; never closes |
| **C1** | **Build** — write the code / data / copy, **decomposed and run in parallel** | **Sonnet + Gemini + Grok** | proposes RETURNED; never closes |
| **C0** | **Validators** — deterministic, non-AI truth; the launch gate | scripts/tests/Shadow | **beats every model**; pass/fail is final |

**Engine → hats (so nothing is ambiguous):**
- **DeepSeek** → C2.1 Audit only (cheap/simple: validation, contradiction-hunting, zero-judgment bulk passes).
- **Gemini** → C2.2 Research **+** C1 Build.
- **Grok** → C2.3 Design **+** C1 Build.
- **Sonnet** → C1 Build only.
- **ChatGPT** → C3 only.
- **C0** → scripts; no engine, no opinion.

---

## C1 Build — the parallelism rule

The orchestrator has **three build resources: Sonnet, Gemini, Grok.** There is **no default builder.**
For each build:

1. **Decompose** the task into independent pieces (different files/dirs, no two writers on the same file).
2. **Distribute** the pieces concurrently across Sonnet / Gemini / Grok, each piece to whichever fits best
   (judgment-heavy → Sonnet; long-context / repo-wide / tests → Gemini; UI spike / punchy copy / bold
   alternative → Grok).
3. **Collapse to one builder** only when the work genuinely can't be split (a single tight change).
4. **Reconverge:** the orchestrator integrates the pieces and runs **C0** on the whole.

This is for **speed** (wall-time) and it spreads load off metered Sonnet onto the flat-rate lanes
(Gemini/Grok), so cost and speed both improve. Per-owner WIP limits and "never two writers on one file"
still apply. *(This replaces the earlier "Sonnet is the default builder" — owner rejected a single
default 2026-06-14.)*

### ⚠️ The native-subagent trap (mechanism = policy)
The **Agent tool** (native `subagent_type:` — Data/Frontend/Content/Red-Team/…) is pinned `model: sonnet`
in its frontmatter, so **reaching for it is *choosing Sonnet*, silently.** Defaulting all C1 to native
subagents re-creates the rejected single-default-builder and **drains the metered Sonnet budget** —
run #8 ran **100% on Sonnet, idled Grok + Gemini, and exhausted a week's budget** (audit F-1). **Rule:**
decompose first, then route **mechanical / spec-complete work — data re-exports, bulk edits,
stale-string / JSON fixes, renames — to the flat-rate wires `(route: C1-GROK)` / `(route: C1-GEMINI)`**,
never the native tool. Reserve native-Sonnet for genuine reasoning, Hebrew editorial copy, and red-team.
A ledger that is ~100% one C1 engine is a routing failure (rule 8). *(Memory: `native_subagent_pins_sonnet_trap`.)*

---

## C0 Validators — what they are and why they win

**C0 is the deterministic truth layer: plain scripts that return pass/fail with no opinion — not AI.**
A model can be confident and wrong; a script can't be charmed. On the cookies page, **four rounds of AI
review all said "clean"; one C0 script found 9 broken products in a single run.** That is why **C0 beats
every model and gates every launch.**

What lives in C0 (each is a yes/no check, run before anything ships):

| Check | Question it answers |
|---|---|
| `validate_comparison_page.py` | runs the whole battery below in one command |
| build-exit | does the site compile? (`npm run build` → exit 0) |
| `score==trace` | does every displayed score equal its scoring trace? |
| `OFF=0` | is there any Open Food Facts data anywhere? (must be zero) |
| PENDING-render | any placeholder text left on a rendered field? (must be zero) |
| count-consistency | do all the product counts on the page agree? |
| ingredient sanity | any truncated / marketing-bleed ingredient strings? |
| image presence | does every product have a working image? |
| **`additive-schema`** *(new, run #8)* | does every `d4_additives` entry match the `AdditiveEntry` VM (5 keys, valid tier)? — *RT-1 CRITICAL slipped to stage 9 for lack of this* |
| **`display==data`** *(new, run #8)* | does every hardcoded number in a card / SEO / page-data string match the live data stat? — *no stale 50.5 / 122 / 56* |
| **`nutrition-bounds`** *(new, run #8)* | is every nutrient within physical-plausibility per 100 g? — *no sodium 7000 mg* |
| **`in-category`** *(new, run #8)* | is every product genuinely in-category? — *no breakfast cereal scored 65/B inside the cakes corpus* |
| **Shadow** (TASK-253) | re-scores a frozen baseline to catch unintended score drift |

**Rule:** no launch without the relevant C0 gate passing. A green C0 is the only thing that turns
"the AI says it's done" into "it's actually done."

---

## Control — autonomous vs delegated

- **Autonomous** (router/native; returns RETURNED-UNVERIFIED; orchestrator verifies + closes):
  Sonnet, DeepSeek, Gemini (build + web-grounded research), Grok (build + design/image), ChatGPT-as-advisor,
  local C0 tools.
- **Delegated** (a human drives it, pastes the result back, never a close): **Tom's final approval (C5)**;
  and the *heavy* external products if ever used — Gemini Deep Research Agent (Interactions API, **not
  wired**), NotebookLM (**manual**), Jules (GitHub agent, **not wired**). Never auto-route a delegated lane.

> **Lane wiring states (honest):** LIVE = Sonnet, DeepSeek, ChatGPT, **Gemini CLI** (build + research),
> **Grok CLI** (build + image/design). NOT-WIRED / DELEGATED = Gemini Deep Research Agent API, NotebookLM,
> Jules. A lane is not LIVE until its `--selftest` passes.

---

## Default routing recipes (each ends at a real C0 gate)

| Task type | Route | C0 gate |
|---|---|---|
| **New category corpus** | scrape (BSIP0/BSIP1) → **G-0.5 post-scrape integrity gate** → BSIP2 score → C1 build → **C0** | `nutrition-bounds`, `in-category`, names-clean, ingredients-not-`text_fallback` |
| **Frontend bug** | C1 build (pick: Sonnet/Gemini/Grok) → C2.1 DeepSeek audit → **C0** | build-exit, `validate_comparison_page.py` |
| **Bulk data cleanup** | C2.1 DeepSeek (zero-judgment) → C1 build if judgment needed → **C0** | schema, `score==trace`, `OFF=0` |
| **Scoring change** | C3 ChatGPT challenge → C2.2 Gemini research if thin → C1 build (parallel) → **Shadow + C0** → **C5 Tom if public** | Shadow diff vs baseline, frozen-invariant byte-check |
| **Major public page** | C2.3 Grok design spike → C3 ChatGPT critique → C1 build (decomposed parallel) → C2.1 DeepSeek QA → **C0** → **C5 Tom** | `validate_comparison_page.py` exit 0, red-team zero-CRITICAL |
| **Research-heavy** | C2.2 Gemini research → C3 ChatGPT challenge → C1 execution | evidence logged with sources; no fabrication |
| **Visual / motion** | C2.3 Grok design (image_gen/edit) → C1 Sonnet if implemented | **orchestrator reads the pixels itself** + build-exit |

Visual corollary (unchanged): **the build is delegable, the pixel look is not** — the orchestrator renders
and *reads the screenshot itself*. **Data-exact visuals (charts) are built in code, never image-generated**
(Grok's own imagine guidance agrees). Capture the **real** build exit code.

**G-0.5 corollary (new, run #8): the scrape is the dirtiest, least-gated stage — gate it at origin.**
Immediately after BSIP0/BSIP1 and **before scoring**, run a post-scrape integrity + red-team review that
fails closed (flagged products are **discarded or held, never scored**): names clean (no price/promo/unit
strings) · every product genuinely **in-category** · nutrient values within plausibility bounds ·
ingredients a **real list, not `bsip1_text_fallback` ad copy** · images resolve-or-null. Run #8 proof of
need: a breakfast cereal scored 65/B, ingredients pulled from marketing text, sodium 7000 mg, and price
text in names **all reached the stage-9 red-team** because nothing reviewed the scrape. A defect born at
stage 0 caught at stage 9 cost everything built between — **push the catch to origin.**
*(Pipeline lessons: `factory_run8_lessons_learned_v1.md` → G-0.5, P-11…P-14.)*

---

## Cloud boundary (data-exposure rule)

Sonnet, Grok, Gemini, ChatGPT all run the model **in the vendor cloud** — files a task touches leave the
building (accepted risk class, = the retired Cursor lane). Two hard rules:

1. **No whole-repo uploads.** Grok Build defaults to bulk-uploading the entire repo (~800MB of
   `02_products`) to xAI on start. The router **self-heals + fails closed** (`_ensure_grok_hardening`:
   asserts `codebase_indexing=false` + `respect_gitignore=true`, forces `GROK_RESPECT_GITIGNORE=1`,
   refuses to dispatch if unconfirmed). See [[c1-grok-lane]], [[gemini_lane_full_executor]].
2. **Scope cwd to the smallest subtree** a task needs. Anything that must not leave the building → local
   **C0** only, no cloud lane.
3. **Free-tier API credits = overflow only, never the scoring brain (owner-approved 2026-06-14).** The
   subscription CLIs (SuperGrok, Gemini Advanced) are already our **free Grok/Gemini compute** — flat sub,
   zero marginal cost, **paid-tier data terms (no training on our data)** — and are the *primary* lanes.
   The *separate* free API credits (xAI ~$175/mo via the data-sharing program; Gemini free key) are
   **"free" because they train on your data.** Therefore they are used **only as overflow for
   non-sensitive work** — public research, image/design concepts, generic drafts from public facts.
   **The proprietary core NEVER goes to a free-training tier:** the scoring engine, BSIP traces,
   unpublished scores, and methodology stay on the subscription CLIs or local C0. If a sensitive task
   needs API access, use the **paid** tier (which buys the no-training guarantee), not the free one.

---

## Rules (the constitution)

1. **The orchestrator routes and decomposes; it does not routine-code.**
2. **Authority is clean at the top:** C5 Owner, C4 Orchestrator, C3 ChatGPT — approved, unambiguous.
3. **C3 (ChatGPT) is advice only** — never builds, never closes. C3 consult is **mandatory** before an
   honest-vs-artifact scoring call, a precedent/governance question, or any tripwire-adjacent ruling.
4. **C2 is three specific single-engine lanes:** Audit=DeepSeek, Research=Gemini, Design=Grok. Nothing is
   lumped; each is its own number.
5. **C1 has no default builder** — decompose and run Sonnet + Gemini + Grok in parallel; pick per piece.
6. **C0 beats every model. No launch without deterministic validation.**
7. **Delegated/not-wired lanes are never auto-routed** and never close work.
8. **Log the lane split at every report/wall.** A ledger that is ~100% one lane is a routing-failure signal.
9. **Escalation:** one in-lane retry, then one lane up; quota/auth exhaustion = exit 75 lane outage →
   re-route + mark DOWN on the board.
10. **Hard rules every lane carries:** OFF ban (absolute) · frozen invariants untouchable · registry
    first · return contract on every dispatched prompt · domain agents propose RETURNED, never CLOSED.
11. **Citations discipline (provenance — the free Claude-Citations equivalent).** Every research finding,
    evidence claim, nutrition/ingredient fact, and consumer-facing claim **names its source inline** — a
    URL, a doc path, a BSIP trace, or literally "direct product scrape". **No claim ships without a
    traceable source.** Fabricated or vague provenance ("official food source", "studies show",
    "experts agree") is **banned** — if the source can't be named, the claim is cut or marked unknown.
    Applies to all lanes (C1/C2/C3) and especially generated copy; every dispatched prompt's return format
    must carry sources, and **a claim with no citable source is a C0/red-team finding.** This is enforced
    by prompt + gate at zero cost (no paid Citations API). Born from the false "official food source"
    line that once shipped live ([[feedback_read_copy_before_ship]], [[off_ban_hard_rule]]).

---

## Wire mapping (so dispatch.py is unchanged)

Bands are reasoning; the router still parses these literal route tags on a prompt's title line:

| Band / function | Engine | Wire route tag | dispatch.py |
|---|---|---|---|
| C2.1 Audit | DeepSeek | `(route: C2)` | opencode HTTP |
| C3 Challenge | ChatGPT | `(route: C3)` | opencode HTTP (advice-only) |
| C2.2 Research / C1 Build | Gemini | `(route: C1-GEMINI)` | `_dispatch_gemini` (web search on) |
| C2.3 Design / C1 Build | Grok | `(route: C1-GROK)` | `_dispatch_grok` (image_gen/edit; legacy `C1-CURSOR` aliases here) |
| C1 Build | Sonnet | *(native)* | Agent tool — orchestrator dispatches directly |
| C0 | scripts | *(scripts)* | `03_operations/spine/validate_comparison_page.py`, Shadow, gates |

`--selftest`, `--selftest-gemini`, `--selftest-grok` verify the live lanes. A new lane is not LIVE until
its selftest passes.
