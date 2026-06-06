# Bari — Nutrition Expert Partnership Deck
_Slide-by-slide spec. Generated from build_deck.py (single source of truth)._

**Grounding:** all figures trace to the live frontend corpus, the TASK registry (TASK-170 external clients, TASK-171 SIE), the evidence registry (EV-024, EV-029, COV-006) and frozen invariants (milk run_004). No product/nutrition data invented.

---

## Slide 1 — COVER · Bari — Building Nutrition Intelligence
- **Subtitle:** A partnership conversation for a senior nutrition scientist
- **Footer:** Confidential  ·  Prepared for nutrition-expert evaluation  ·  June 2026
- **Speaker notes:** Open warm but get to the point in 30 seconds. 'You know nutrition deeply. You've also watched the public information layer around food rot — scores that contradict each other, labels nobody can read, influencers filling the vacuum. Bari is an attempt to fix that layer with real engineering and real evidence discipline. I'm not here to pitch you a logo — I'm here to show you a system that already exists, and to ask whether you want to put your name and judgement inside it while it's still being shaped.' Set expectation: ~25 slides, heavy on what's built, honest about what isn't.

## Slide 2 — SECTION 1 · The Problem
- **Objective / sub:** The consumer nutrition-information layer is broken — and trust is leaving with it.
- **Speaker notes:** Frame the problem as a SCIENTIST would feel it, not a marketer. The expert has personally seen patients act on garbage scores. Validate that frustration first; it earns the right to everything after.

## Slide 3 — Nutrition information is structurally broken
- **Section:** The Problem · 1 of 5
- **Lead:** The failure is not a lack of data. It is the absence of a trustworthy interpretation layer between the label and the person.
- **Key messages:**
    - **Data exists, meaning doesn't.** Every package has a panel; almost no consumer can convert it into a decision.
    - **Interpretation is outsourced to whoever shouts loudest.** Influencers and brands fill the vacuum the science left open.
    - **Context collapses.** A number with no category, no confidence, and no reasoning is noise dressed as authority.
- **Suggested visual:** Split image — a dense ingredient panel on the left, a confused shopper on the right; one arrow between them labelled 'missing layer'.
- **Speaker notes:** Land the core thesis early: the gap is interpretation, not raw data. Everything Bari builds sits in that gap. Don't rush — let the scientist nod at 'meaning doesn't exist'.

## Slide 4 — Consumers are confused — predictably so
- **Section:** The Problem · 2 of 5
- **Key messages:**
    - **Marketing language mimics health language.** ‘טבעי’, ‘ללא’, ‘עשיר ב־’ carry no consistent meaning.
    - **Front-of-pack claims contradict the back-of-pack reality.** The diet-yogurt that scores worse than the full-fat one.
    - **Health-by-omission.** ‘No sugar’ says nothing about what replaced it.
    - **No category sense.** Shoppers compare a cracker to a yogurt because nothing tells them not to.
- **Suggested visual:** Three real front-of-pack claims with a red 'says nothing about…' annotation under each.
- **Speaker notes:** Use a concrete Israeli-shelf example the expert recognises: a 'diet' dessert that is engineered worse than its plain sibling. This previews our maadanim (מילקי = E) finding without naming the section yet.

## Slide 5 — Ingredient lists are effectively unreadable
- **Section:** The Problem · 3 of 5
- **Key messages:**
    - **Length is weaponised.** 20+ ingredients, additives behind code numbers, function hidden.
    - **Order obscures dose.** Position implies quantity but never states it.
    - **Named-additive identity is lost.** ‘חלבון חלב’, emulsifiers, stabilisers read as one grey blur.
    - Even a trained dietitian needs minutes per product. A shopper has seconds.
- **Suggested visual:** A real long ingredient list with additive codes highlighted and a stopwatch overlay ('avg shopper attention: 6s').
- **Speaker notes:** This is where you signal technical seriousness: Bari's engine actually parses named additives and reasons about them (named-additive identity, engine 0.4.0). Tease, don't explain yet.

## Slide 6 — Existing scores fail — and fail quietly
- **Section:** The Problem · 4 of 5
- **Key messages (columns):**
    - _Why current scores break_
        - **One global formula.** A bread rule applied to yogurt is wrong by construction.
        - **No confidence.** A guess and a verified result look identical.
        - **No reasoning.** A letter with no ‘why’ can't be trusted or challenged.
        - **Gamed.** Reformulate to beat the metric, not to improve the food.
    - _What a credible score needs_
        - **Category-relative judgement.** Compare like with like.
        - **Explicit confidence.** Verified / partial / insufficient — never hidden.
        - **Traceable reasoning.** Every grade defends itself from real signals.
        - **Evidence-anchored rules.** Not opinion, not vibes.
- **Suggested visual:** Two-column 'Today vs. What's required' table; left column greyed, right column in Bari teal.
- **Speaker notes:** This slide quietly defines the evaluation criteria the expert will use on US — and we happen to meet all four. Let them feel they wrote the requirements.

## Slide 7 — Trust is deteriorating — that's the opening
- **Section:** The Problem · 5 of 5
- **Lead:** When institutions go quiet, the loudest voice wins. The result is a market actively hungry for a source that is rigorous and readable at the same time.
- **Key messages:**
    - **The authority vacuum is real.** Regulators are slow; brands are conflicted; social media is fast and wrong.
    - **Consumers know they're being sold to.** Skepticism is high — credibility is scarce and therefore valuable.
    - **The winner is whoever is both trusted AND usable.** Rigor alone is ignored; usability alone is dangerous. Bari targets the intersection.
- **Suggested visual:** Trust-vs-time line trending down for ‘brands/influencers’, with a gap labelled ‘the position Bari is building toward’.
- **Speaker notes:** Transition line: 'So the question isn't whether this layer is needed — it's whether anyone can build it credibly. Here's what we are building.'

## Slide 8 — SECTION 2 · The Bari Vision
- **Objective / sub:** One rigorous engine powering three audiences — consumer, professional, industry — and a trusted commerce marketplace.
- **Speaker notes:** Shift energy from problem to ambition. Keep it grounded: vision slides are where skeptics disengage if you over-claim. Anchor every layer to something that already exists.

## Slide 9 — What Bari is
- **Section:** The Vision
- **Lead:** Bari is a nutrition-intelligence platform: an evidence-anchored engine that turns messy real-world food labels into honest, category-aware, explainable judgement — and the trusted place to act on it.
- **Key messages:**
    - **Not a blog. Not a single score.** An interpretation engine with governance, confidence and provenance built in.
    - **Starts consumer-facing in Hebrew.** Live comparison pages on the Israeli shelf today.
    - **Three intelligence audiences, one engine.** Consumer, professional and industry — same engine, progressively deeper surfaces.
    - **And a trusted marketplace.** Bari is also where trust converts to action — discovering and buying better products — without ever putting a grade up for sale.
- **Suggested visual:** One-engine / four-surface diagram: central engine (BSIP) feeding Consumer, Professional, Industry and a Commerce/Marketplace layer.
- **Speaker notes:** Repeat the spine: ONE engine, THREE audiences, PLUS a marketplace. The consumer site is the proof and the data flywheel; professional + industry are where defensibility lives; the marketplace is where trust becomes revenue. Stress the integrity line: we monetise the transaction, never the grade.

## Slide 10 — Three audiences + a marketplace, one engine
- **Section:** The Vision
- **Lead:** The same engine serves three intelligence audiences — and a commerce layer that turns earned trust into transactions.
- **Key messages (columns):**
    - _Consumer layer  (live)_
        - Category comparison pages on the real Israeli shelf
        - Honest grades + plain-language verdicts
        - Confidence shown, never hidden
    - _Professional + commerce  (next)_
        - Decision-support for dietitians & clinicians
        - Category dossiers, evidence trails, defensible reasoning
        - A marketplace: discover → buy better products (grade stays unsellable)
- **Suggested visual:** Four horizontal bands (Consumer / Professional / Industry-Data / Commerce-Marketplace) sharing one engine column on the left.
- **Speaker notes:** Note explicitly: the DATA layer underneath (proprietary scored corpus + evidence registry) is what makes the upper layers possible and hard to copy; the marketplace is what makes the trust pay. The integrity guardrail is structural — you can buy a product through Bari, you can never buy a better grade.

## Slide 11 — A credible five-year path
- **Section:** The Vision · 5-year arc
- **Lead:** Audience → trust → tools → industry → geography. Each year funds and de-risks the next; no leap is unbacked.
- **Key messages:**
    - **Years 1–2 — earn the shelf.** A live Israeli comparison platform, then deepening category intelligence.
    - **Year 3 — professional tools.** Subscriptions for dietitians & clinics, once the engine is category-proven.
    - **Years 4–5 — commerce, industry & geography.** Retail integration and a product marketplace, then US expansion + a nutrition-intelligence ecosystem others build on.
- **Suggested visual:** Horizontal 5-year roadmap ribbon with a widening 'defensibility / revenue' wedge beneath it.
- **Speaker notes:** Stress the LOGIC of the order, not the dates. Audience first because trust is the scarce asset; professional tools only after the engine has been validated on real categories; US last because the engine must be proven portable before geography multiplies cost.

## Slide 12 — SECTION 3 · What We've Already Built
- **Objective / sub:** This is not a concept deck. A working pipeline, a scoring engine, governance, and a live site already exist.
- **Speaker notes:** This is the credibility core. Pace slows here. The expert must leave this section thinking 'this is further along and more disciplined than I expected.'

## Slide 13 — A three-stage data pipeline: BSIP0 → BSIP1 → BSIP2
- **Section:** What We Built · pipeline
- **Key messages (columns):**
    - _Ingestion & consolidation_
        - **BSIP0 — acquisition.** Real retailer scraping (Shufersal), label & nutrition parsing, raw-source persistence for offline replay.
        - **BSIP1 — trust layer.** Cross-retailer consolidation, observation-quality + canonical trust scoring, 10-field semantic enrichment. Not scoring.
    - _Scoring & interpretation_
        - **BSIP2 — the engine.** Four interpretive layers: Structural, Nutritional, Metabolic, Engineering.
        - **Universal core + archetypes.** One core, category-specific interpretation via a 3-stage router (anchor → signal → resolution). Engine v0.4.0.
- **Suggested visual:** Left-to-right pipeline diagram with three labelled stages and a 'raw source preserved' callout under BSIP0.
- **Speaker notes:** Key message: scoring is DELIBERATELY isolated downstream. Ingestion, consolidation, and judgement are separate layers — so the expert can audit the judgement layer without touching plumbing. That separation is itself a rigor signal.

## Slide 14 — Evidence, confidence and validation are built in — not bolted on
- **Section:** What We Built · rigor infrastructure
- **Key messages:**
    - **Evidence Registry.** 20 food findings + 20 guardrails + 20 deferred domains; every rule traces to a catalogued finding, not opinion. Each finding has a tracking id so we can say exactly why a rule exists.
    - **Confidence system.** Three explicit states — verified / partial / insufficient. When the label can't support a score we publish no score at all, rather than fake certainty.
    - **Validation system.** A fixed set of 12 hand-checked reference products plus an automated regression test that re-scores them on every change — so a parsing mistake is caught before it can reach the site.
    - **Governance.** A written constitution: 6-article comparison governance, use-case guardrails, an exception registry for every deliberate deviation.
- **Suggested visual:** Four-quadrant 'rigor stack': Evidence / Confidence / Validation / Governance, each with its real artifact name.
- **Speaker notes:** This is the slide that separates Bari from every content startup. Emphasise: we have a MECHANISM to refuse to answer (null on insufficient) and a MECHANISM to record every exception. A scientist trusts a system that knows its own limits.

## Slide 15 — A live platform and an operating model behind it
- **Section:** What We Built · surfaces & operations
- **Key messages (columns):**
    - _Product surfaces (live)_
        - **Category framework.** Repeatable factory: shelf-map → corpus → score → QA → publish.
        - **Comparison platform.** Live Hebrew RTL pages with grades, verdicts, expandable reasoning.
        - **External data layer.** 10 read-only authoritative clients — OFF, gov data, PubMed, DSLD, Tzameret…
    - _Operating model_
        - **Command Center.** Authoritative task registry → derived dashboard; nothing ships untracked.
        - **Agent OS.** Specialist agents (nutrition, data, QA, content) with a verification gate before close.
        - **Provenance discipline.** Frozen invariants, dated rulings, no silent score changes.
- **Suggested visual:** Screenshot of a live comparison page beside a Command Center dashboard view.
- **Speaker notes:** The operating model is the unsung moat: an auditable trail from a raw label to a published grade, with a registry that records who decided what and why. Most teams have none of this. Mention the 10 live external clients as evidence we reason from authoritative sources, not scraping guesses.

## Slide 16 — Why this is hard to replicate
- **Section:** What We Built · the moat
- **Key messages:**
    - **It's not the model — it's the accumulated judgement.** Every category adds calibrated rules, evidence links and stress-tested edge cases that don't transfer for free.
    - **Real-shelf data is messy and earned.** Parsing real Israeli labels (and surviving their traps) took real failures to fix — e.g. the fat-overwrite bug below.
    - **Governance compounds.** An exception registry and frozen invariants mean the system gets MORE trustworthy over time, not noisier.
    - **Honesty is a feature competitors can't fake late.** ‘We score this null because we can't verify it’ is a trust posture you build from day one.
- **Suggested visual:** Layered-moat diagram: Data → Calibration → Evidence → Governance → Trust, each ring wider and harder to cross.
- **Speaker notes:** Tie replication difficulty to TIME and DISCIPLINE, not secrecy. Anyone can copy a UI in a week; nobody can copy two years of calibrated category judgement and a governance trail. This is the slide an investor remembers.

## Slide 17 — SECTION 4 · Scientific Depth
- **Objective / sub:** The methodology a nutrition scientist would actually respect — shown through real rulings, not slogans.
- **Speaker notes:** Now speak peer-to-peer. This section is for the scientist's internal credibility test. Lead with philosophy, then prove each principle with a real category ruling.

## Slide 18 — The methodology, stated plainly
- **Section:** Scientific Depth · principles
- **Key messages:**
    - **Evidence-based.** Rules derive from a registry of findings, each with an id and rationale — challengeable, versioned.
    - **Label-observability.** We only score what the label actually lets us observe. No invented values; unverifiable → insufficient.
    - **Food reality over opinion.** We interpret the food as engineered, not the marketing story around it.
    - **Processing read with nuance.** NOVA-aware but not NOVA-blind; named additives and matrix effects reasoned about, not just counted.
    - **Category-specific calibration.** Protein, fat, fortification all judged category-relative — a yogurt rule never touches bread.
    - **Stress-tested.** Every category passes an adversarial governance audit before it can go live.
- **Suggested visual:** Six-principle hexagon, each tile linking to the real example slide that proves it.
- **Speaker notes:** Read these as a manifesto, then say: 'Principles are cheap — let me show you five times this changed an actual grade.' Hand over to the examples.

## Slide 19 — Hummus — defining the prepared/raw boundary correctly
- **Section:** Scientific Depth · real ruling 1
- **Lead:** A naïve engine splits hummus by protein or by the word ‘סלט’. Both are wrong.
- **Key messages:**
    - **The real boundary is tahini + sodium + energy density.** Not protein, never the label noun. Tahini-based salads are correctly kept in scope.
    - **Result: a defensible 64-product comparison.** Recalibration moved the distribution toward truth (B-tier widened as cultures/quality were credited correctly).
    - **Why it matters scientifically.** It shows the engine reasons about food structure, not keywords.
- **Suggested visual:** Scatter of hummus products on tahini×sodium axes with the prepared/raw boundary drawn through it.
- **Speaker notes:** This is the 'they actually think about food' proof. The protein-trap correction (raw-vs-prepared boundary) is exactly the kind of subtle call a dietitian respects and a keyword classifier gets wrong.

## Slide 20 — Yogurts — crediting live cultures, and refusing to overclaim
- **Section:** Scientific Depth · real ruling 2
- **Key messages:**
    - **We found a real bug in our own pipeline.** Live cultures were being detected when we read the label, but the scoring step looked at a different list and never counted them — 49 products had cultures detected, 0 credited.
    - **We fixed it at the source.** We made the scorer read the same culture list; 12 products correctly moved from C up to B once their live cultures actually counted.
    - **Then we held the line.** Even after the fix, no yogurt reached an A. A score of 78.7 (a high B) is the honest ceiling — the cleanest candidates simply don't publish enough on their label to justify more.
- **Suggested visual:** Before/after grade-distribution bars for yogurt with the two corrected steps annotated.
- **Speaker notes:** This is the most persuasive slide for a skeptic: we improved scores when evidence justified it AND refused to inflate to an A when the data didn't support one. That asymmetry — quick to credit, slow to crown — is the whole trust thesis in one example.

## Slide 21 — SECTION 5 · Current Progress
- **Objective / sub:** Concrete output to date — categories live, products scored, lessons banked.
- **Speaker notes:** Quantify. The skeptic is asking 'is this real or a demo?'. Numbers from the live corpus answer that.

## Slide 22 — What's live today
- **Section:** Current Progress · by the numbers
- **Lead:** 6 live categories · 250+ curated scored products on the real shelf · 10 authoritative external data clients (live-verified).
- **Key messages:**
    - **Per category, end-to-end.** bread 24 · cheese ~52 · hummus 64 · dairy-desserts 84 · bars 18 · yogurt 11 — each scraped, scored, QA'd, published.
    - **Funnels are honest.** bread: 256 scanned → 81 scored → 31 curated; maadanim: 200 scraped → 169 scored. We publish the defensible subset, not everything.
    - **Next engine in flight.** A supplement-intelligence engine (SIE) — sibling to BSIP2 — is in methodology phase.
- **Suggested visual:** Six category tiles each showing n-products + grade-distribution mini-bar; a totals strip beneath.
- **Speaker notes:** Be precise and modest: these are CURATED counts (the publishable subset), and you should say so — it reinforces that we withhold what we can't defend. The 256→81→31 bread funnel is the single best honesty proof point; lead with it if pressed.

## Slide 23 — Milestones and lessons banked
- **Section:** Current Progress · milestones
- **Key messages (columns):**
    - _Milestones_
        - Repeatable category factory proven across 6 shelves
        - Real-retailer ingestion with raw-source replay
        - Evidence registry + governance constitution in force
        - Command Center + agent operating model running daily
        - 10-client external evidence layer live-verified (Jun 2026)
    - _Lessons learned_
        - **Parsing reality is the hard part.** Real labels hide traps — e.g. a Hebrew-text quirk once let a trans-fat sub-line silently overwrite total fat. Found, fixed once centrally, permanently guarded.
        - **Detecting a signal isn't crediting it.** A value read at one step but ignored at the next is invisible — pipelines must be wired end-to-end (the yogurt-culture fix).
        - **Measure your priors.** We assumed cereal fortification was everywhere; it was only 27% — so we dropped the penalty.
        - **Withholding is a feature.** Benching a category we can't defend yet beats shipping a shaky one.
- **Suggested visual:** A horizontal timeline (categories shipped over time) with lesson callouts pinned to the runs that taught them.
- **Speaker notes:** Lessons matter more than milestones to a scientist — they prove we learn under contact with reality. Each lesson maps to a real EV-id or run, so none of this is abstract.

## Slide 24 — SECTION 6 · Monetization
- **Objective / sub:** A staged path from audience to marketplace to ecosystem — each stage earns the right to the next.
- **Speaker notes:** Be sober here. A scientist distrusts a revenue fairy tale. Pair every stage with its real risk. Credibility now buys believability later.

## Slide 25 — Six stages, each de-risking the next
- **Section:** Monetization · the staircase
- **Lead:** Guardrail on every stage: we monetise the transaction, never the grade.
- **Key messages (columns):**
    - _Stages 1–3_
        - **1 · Audience + trust.** Free comparisons. Cheap reach; slow, indirect revenue.
        - **2 · Content + influence.** Editorial authority. Compounds trust; mustn't sell out.
        - **3 · Professional subs.** Tools for clinics. Real willingness-to-pay; needs depth.
    - _Stages 4–6_
        - **4 · Commerce / marketplace.** Discover → buy better products. Scales with trust; stays grade-blind.
        - **5 · Industry intelligence.** Shelf insight for retailers. High-value; conflicts governed hard.
        - **6 · Retail / ecosystem.** Engine licensing. Durable, defensible; execution + geography cost.
- **Suggested visual:** A six-step staircase rising left-to-right (marketplace = step 4, highlighted); a rising revenue/defensibility trend above.
- **Speaker notes:** Hit the integrity guardrail hard: across EVERY stage — especially the marketplace and industry stages — we monetise the transaction, never the grade. The instant a brand can buy a better score, consumer trust (and the expert's reputation) evaporates. Our governance makes that boundary structural, not a promise. The marketplace is how trust becomes revenue without compromising the science.
