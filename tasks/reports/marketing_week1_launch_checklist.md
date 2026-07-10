---
doc: marketing_week1_launch_checklist_v1
owner: marketing-agent
created: 2026-07-03
status: DRAFT — for owner execution
source: tasks/reports/launch_readiness_and_strategy_investigation_2026-07-02.md (item 8, §3 network-effect playbook)
related: TASK-473 (10 FB/IG finding-posts, in-flight fix round as of 2026-07-03)
---

# Bari — Week 1 Launch Marketing Checklist

**Who this is for:** Tom, solo, non-programmer, limited hours/day, ~$150 total search budget.
**What this is:** a day-by-day punch list you can just DO. Not a strategy memo — that's item 8's source report. This is the execution layer under it.
**What this is not:** consumer-facing copy. Any post text below marked **DRAFT** still needs the two-gate (Content + Adversarial QA/Red-Team) before it goes live, per the hard content sign-off rule. This doc itself needs no gate — it's internal planning.

---

## 0. Ground truth check (do this first, 10 minutes)

Before you post anything, confirm these three things still hold — they're the foundation everything below stands on:

1. **Channels are live.** WhatsApp Channel `0029VbDGpnr7j6g4xM62910s`, Instagram `bari_nutrition`, Facebook page `61591403370117` — all three render on the homepage footer/community band today (verified in TASK-467/469, build-checked against rendered HTML). Open each link once from your phone and confirm you can post as admin.
2. **WhatsApp share cards work.** Open any comparison page (e.g. `/hashvaot/brined-cheeses`) and share the raw URL to yourself in WhatsApp. If the preview card shows a generic logo instead of that category's image, **this is a same-day blocker** — route an OG-image fix request to Product Agent → Frontend Agent before doing any group/channel push. Every share you make this week rides on this card looking right.
3. **TASK-473's 10 posts status.** As of now they're in an active Adversarial QA/Red-Team fix round (9/10 clean, 3 posts getting corrected: sodium exposure wrapper, an invented count, a scare-quote issue). Do not post any of them until you get the "gate closed, GO" signal — check `tasks/TASK-473.md` status field before pulling from it. Everything in Days 3–7 below assumes this resolves within the week; if it doesn't, use the "manual finding-post engine" in Day 2 as your fallback so you're not blocked.

---

## Day 1 — Setup (target: 2–3 hours)

**1a. Pin an intro post on the WhatsApp Channel.**
Why: the Channel has zero content today; the first message sets the tone for every forward it earns afterward.
First step: write one message, pin it. Suggested shape (Hebrew, first-person, per your authentic voice — bold number, verb CTA, no health claim):

> **DRAFT — needs two-gate before any public use, this is a shape example only:**
> "בדקתי [X] מוצרים במדף ה[קטגוריה]. ההפרש בין הכי-גבוה להכי-נמוך: [N] נקודות. בלי לספר לכם מה לקנות — רק להראות מה שקוף. עוקבים? כל שבוע ממצא אחד."

Time cost: 20 min to draft + your own read-through. Do NOT ship the exact wording above as final copy — it's a shape reference, not gated copy. If you want a gated version, route through Content Agent this week; otherwise write your own single sentence in your own voice and post it — a channel intro post is low-stakes enough that a plain, honest, non-superlative sentence in your own words is fine without a formal gate, as long as it makes no product claim beyond "I compared X and here's what differs."

**1b. Confirm bio/links are consistent across all three channels.**
Why: someone landing on Instagram after seeing a WhatsApp forward should find the same channel-hop path everywhere.
First step: on each of the 3 profiles, make sure the bio links to `bari.digital` and mentions the other two channels (or at minimum, all point to the same homepage where the community band lives).
Time cost: 15 min.

**1c. Group recon list (build it, don't join yet).**
Why: §3 of the source report recommends 8–10 Facebook groups across nutrition, parenting, "צרכנות נבונה" (smart consumerism), and couponing — Bari is couponing-adjacent (price/value angle) without being a coupon page.
First step: search Facebook for these exact categories and list candidates by size and activity (posts/day), not just member count — a 5k-member group posting daily beats a 60k-member group that's dead. I cannot verify specific group names, membership quality, or admin responsiveness from here — **this list is yours to build and vet**; I can tell you the categories to search, not name real groups I haven't seen active.
Categories to search: Israeli parenting/motherhood nutrition groups, "צרכנות נבונה"/consumer-rights groups, couponing/savings groups, general health-conscious shopping groups, city-specific "מה קונים ב[city]" groups.
Time cost: 45–60 min. Output: a spreadsheet or note with 8–10 group names, member count, and your gut read on activity level.

**1d. Draft the admin-DM template (do not send yet).**
Why: §3's core insight — one admin relationship in a 40k group beats 20 cold posts. This is relationship-first, not blast-first.
First step: write one short DM template that (i) says who you are (solo founder, independent, no ads/sponsorship in the site), (ii) offers value to the group specifically (e.g. "happy to run a comparison on a product your members ask about"), (iii) asks permission before posting, not forgiveness after.
Time cost: 30 min. You'll personalize and send these Day 2–3, not today — Day 1 is pure setup.

**Day 1 total: ~2.5–3.5 hrs.**

---

## Day 2 — Send DMs + build your first manual finding-post (target: 1.5–2 hours)

**2a. Send 3–4 admin DMs** from your Day 1 list, personalized per group (mention their group name, why it's relevant).
Why: this is the highest-ROI single action in the whole week per the source report — group access is gated by trust, not content quality.
Time cost: 30–40 min (10 min each, personalized).
What NOT to do: don't send the same templated DM verbatim to all of them — admins compare notes; don't ask to post immediately, ask to introduce yourself.

**2b. Build one manual finding-post as a fallback**, independent of TASK-473, in case that gate isn't closed by Day 3. Use ONE of these three verified hooks (all pulled and confirmed directly from live category JSON on 2026-07-03 — cite the category + number, nothing invented):

- **Crackers:** the top-scoring product (`קרקר כוסמין מלא ושומשום`, score 81.6/A) is a 4-ingredient product — whole spelt, sesame, salt, oregano, no starch filler — while the category's bottom two sit at 44.5/D and 49.6/D. 19 products scored total. Angle: "fewer ingredients isn't a slogan here, it's the actual driver of the top score in this category."
- **Bread:** two products carry the rare S grade — `לחם טחינה פרוס` (90.8) and `לחם ירוק מקמח מלא` (90.1) — out of 23 breads scored, against a bottom of 57.3/C. Angle: "in 23 breads, only 2 landed the top tier — and they're not the ones with the fanciest packaging."
- **Cookies & coffee-biscuits:** only 9 of 117 products scored C or better; the rest are D or E. Angle: "I scored 117 products on this shelf. 108 of them didn't clear a C." (Verify this exact 9/117 split again before publishing if more than a few days pass — corpus can be re-scored on a spine flip and the source doc's re-flow policy means numbers aren't frozen.)

Time cost: 45–60 min to turn one hook into a post (write Hebrew copy, pick screenshot). **This draft still needs the two-gate (Content + Adversarial QA/Red-Team) before it's public** — route it same as TASK-473's posts, don't self-publish.

**Day 2 total: ~1.5–2 hrs.**

---

## Day 3 — First public content (target: 1–1.5 hours, assuming gates already run in background)

**3a. Post the first WhatsApp Channel finding-post.** Use TASK-473's post #1 if the gate has closed by now (check task status first — Registry First rule), otherwise use your Day 2b fallback once it's gated.
Why: the Channel is broadcast-only and low-risk — this is the easiest place to build a rhythm before groups.
Time cost: 10 min to post + screenshot.

**3b. Post to Instagram/Facebook** using the same finding-unit, format style (B) from the source report — "compared N products, price and grade don't correlate" — works well as a carousel or single image with the score table.
Time cost: 20–30 min including image prep (this is where Canva + the existing brand-kit mascot assets come in — TASK-473's chain already has Canva assembly queued for its 10 posts).

**3c. Follow up on Day 1 DMs** that haven't responded — one soft nudge, not a second cold pitch.
Time cost: 10 min.

**Day 3 total: ~1–1.5 hrs.**

---

## Day 4 — Search ads setup (target: 1.5–2 hours)

This is the $150 spend. Per the source report's single recommendation: **Google Search ads, not Facebook boosted posts** — boosted posts buy invisible cold reach, search ads reach people already typing the question Bari answers.

**4a. Build the keyword list (15–20 exact/phrase Hebrew keywords of formed intent).**
Pattern: "האם [X] בריא" (is X healthy) and "[product] בריא" — intent-bearing, not generic ("חלב" alone is too broad and too expensive; "האם חלב עמק בריא" is cheap and converts).
Draw the 15–20 candidate product/category names from categories where you have strong pages to land on: brined cheeses (your golden template page), milk, bread, hummus, crackers — categories with real spread (S/A grades next to D/E) make for a satisfying landing experience when someone clicks through from "is X healthy."
Time cost: 45 min.

**4b. Set up the campaign.**
- Landing page: the *specific* comparison page for that keyword, never the homepage.
- Budget: ~$5–7/day, 20–25 days ≈ your $150.
- No health-outcome claims in ad copy — Bari does not advise on diet/health outcomes; the ad copy should say "compared" / "scored," never "healthy for you."
Time cost: 45 min to set up in Google Ads.

**4c. What "working" looks like this week:** you won't see conversion signal in week 1 — you're just confirming the campaign is live, keywords are approved (Google review can take 24–48h), and clicks are landing on the right page. Don't judge or kill anything before Day 5 of the campaign's own run (which likely falls in Week 2) — the source report's kill-non-converters rule is a day-5-of-campaign rule, not a day-5-of-week-1 rule. Just get it live and correctly wired this week.

**Day 4 total: ~1.5–2 hrs.**

---

## Day 5 — Second content beat + group posting (if any admin said yes) (target: 1–1.5 hours)

**5a.** If any Day 1–2 admin DM got a yes, post your first group finding-post using format (A) or (C) from the source report ((C) — no-link question post, link only in comments — is the safest first move in an unfamiliar group).
**5b.** Second WhatsApp Channel + IG/FB post — keep the 2–3/week cadence the source report specifies for the Channel.
**5c.** Check Google Ads: are keywords approved and serving? Any obvious issue (rejected keyword, low quality score)?

Time cost: 1–1.5 hrs total, mostly gated by whether a group said yes.

---

## Day 6–7 — Consolidate, don't over-post (target: 1 hour total)

Do not post daily to every channel — that's a burnout pattern for a solo founder and reads as spammy. By Day 6–7:
- One more Channel/social post if you have gated content ready (ideally the next post in TASK-473's queue).
- Check in on any group DMs still pending — one gentle follow-up, then let it rest; chasing reads badly.
- Log what happened (see metric below) so Week 2 planning has real numbers, not vibes.

---

## The finding-posts engine (how to keep doing this after Week 1)

The repeatable move: **pick a category → pull one real number contrast → wrap it in one honest sentence → screenshot the actual comparison row.** Never invent a number, never round in the flattering direction, never claim health outcomes. The three hooks in Day 2b show the pattern — score spread, ingredient-count-to-score link, or "X% didn't clear a bar" corpus-wide stats are the three shapes that repeat well. TASK-473 is building 10 of these properly (grounded, two-gate-cleared) — treat that task's output as your primary supply once it closes, and use the manual pattern above only as a gap-filler.

**Hard rule for every future post, not just this week:** verify the exact figure against `origin/master` (the live deploy branch) before publishing — e.g. `git show origin/master:bari-web/src/data/comparisons/<file>.json` — not against a local working-copy file, and not against a doc you wrote earlier. This isn't theoretical: an earlier draft of this very checklist cited bread's top S-grades as 94.8/92.7 from a local read, when origin/master (what's actually live) has them at 90.8/90.1 — a stale local tree, not a re-score, but the failure mode is identical either way. The re-flow policy also means these numbers move on any scoring switch. A stale superlative is a credibility risk for a site whose entire value proposition is "we didn't fabricate this."

---

## Community seeding — what NOT to do

- Don't post identical content to multiple groups the same day (source report's explicit rule).
- Don't post an "announcement" ("I launched a site!") — groups tune these out and some rules ban them outright; post a *finding*.
- Don't drop a bare link with no context — always lead with the finding, link second (or in comments only, for strict groups).
- Don't DM 10 admins in one sitting from a copy-paste template — 3–4/day, personalized, is sustainable and reads as human.
- Don't argue with a skeptical comment defending a specific brand — acknowledge, point to the transparent scoring methodology page, disengage. You are not the site's customer support for every comment.

---

## The one metric to watch this week

**WhatsApp Channel + Instagram + Facebook combined follower/subscriber count, checked once at end of Week 1 vs. Day 1 baseline.**

Why this one, not clicks or ad CTR: it's the number you can see without any analytics setup, it's honest (no vanity-metric inflation), and it's the leading indicator for the "screenshot → forward → new follower" loop the whole playbook depends on. Ad performance (Search Console impressions, click-through) is a Week 2+ read — one week of a slowly-ramping ad campaign won't be statistically meaningful yet.

**Definition of a successful Week 1** (deliberately modest — this is about groundwork, not virality):
- All 3 channels have their intro content live and consistent.
- At least 2 pieces of gated finding-content posted publicly (Channel + social).
- At least 1 admin relationship opened (a DM sent and, ideally, replied to) — doesn't need to convert to a post yet.
- Search campaign live and correctly wired (right landing pages, no health claims, keywords approved).
- Zero copy published without the two-gate.
- You know, in writing, which 8–10 groups are your Week 2–3 targets.

If you hit all six, Week 1 worked — regardless of the follower number, which is a lagging indicator at this scale and shouldn't be over-read after 7 days.

---

## What the owner must decide (not mine to call)

1. **Which Facebook groups actually make the cut** — I listed categories to search, not verified live groups; you have Facebook access and community judgment I don't have visibility into.
2. **The exact Channel intro post wording** — I gave a shape, not final copy; either write it yourself (fine for a low-stakes intro line) or route it through Content Agent this week if you want the full voice-matched version.
3. **Ad budget pacing** — $5 vs $7/day, and whether to extend past day 20–25 if early signal looks promising; that's a spend decision, not a strategy one, and it's yours.
4. **Whether to wait for TASK-473's full 10-post gate closure or run entirely on the Day 2b manual fallback** — I've built the fallback so you're not blocked either way, but which one to lead with in Days 3–5 is your call depending on how fast that gate resolves.

---

```json
{
  "task": "item8-marketing-checklist",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "C:\\Bari\\tasks\\reports\\marketing_week1_launch_checklist.md",
      "sha256": "note: self-referential (this hash is embedded in the file it hashes), so the true final byte-for-byte value can't be recorded here — recompute with `sha256sum tasks/reports/marketing_week1_launch_checklist.md` for the authoritative value. Last computed on the pre-this-line content, post bread-correction: 14660253f8a15fb7258c5206f41044f983e02496788a659ab848169bda91d938"
    }
  ],
  "counts": {
    "categories_scanned_for_hooks": 16,
    "categories_with_verified_hooks_cited": 4,
    "hooks_cited_in_checklist": 3,
    "denominator_note": "16 = all live comparison JSONs under bari-web/src/data/comparisons/*; hooks pulled from crackers (n=19), bread (n=23), cookies_coffee (n=117), hummus (n=57) — each figure read directly from the live frontend JSON, not from a prior doc",
    "channels_verified_live": 3,
    "channels_denominator": "3 = WhatsApp Channel + Instagram + Facebook, all confirmed present in TASK-467/469 closed-task build verification against rendered homepage HTML"
  },
  "commands_run": [
    {"cmd": "grep -n 'item 8|WhatsApp|Week-1|$150' tasks/reports/launch_readiness_and_strategy_investigation_2026-07-02.md", "exit": 0},
    {"cmd": "python3 -c \"json.load(...) per-category scan of 16 comparison JSONs (LOCAL tree) -> grade distributions, top3/bottom2\"", "exit": 0},
    {"cmd": "python3 -c \"detail pull: crackers top nutrition, cookies_coffee C-or-better count, milk/bread grade-A/S lists (LOCAL tree)\"", "exit": 0},
    {"cmd": "grep -n 'wa.me|whatsapp.com|WhatsApp|instagram|facebook' tasks/closed/TASK-467.md tasks/closed/TASK-469.md", "exit": 0},
    {"cmd": "git fetch origin master", "exit": 0},
    {"cmd": "git show origin/master:bari-web/src/data/comparisons/bread_frontend_v4.json > scratch; git show origin/master:.../cookies_coffee_frontend_v2.json; .../hummus_frontend_v5.json; .../milk_frontend_v1.json; .../crackers_frontend_v1.json", "exit": 0},
    {"cmd": "python3 re-verify all 5 cited hooks against the origin/master pulls (not local tree)", "exit": 0}
  ],
  "not_done": [
    "Did not verify specific Facebook group names/membership — flagged explicitly as owner-must-decide, cannot be verified from this environment",
    "Did not wait for TASK-473's fix-round gate to close before writing this doc — referenced its in-flight status and built a fallback finding-post path instead",
    "Did not build final Channel intro-post copy through the two-gate — left as owner's own words or a Content Agent routing decision",
    "Did not set up the actual Google Ads campaign — this is a plan for the owner to execute, not an executed campaign"
  ],
  "self_check": "CORRECTED 2026-07-03: initial draft's data hooks were read from the local working tree, which is diverged from origin/master (the live deploy target). Bread was stale — local read 94.8/92.7 (top S-grades) and 57.7 (bottom) vs the correct origin/master values 90.8/S + 90.1/S and 57.3/C; corrected in the Day 2b hook. All 5 cited hooks (bread, crackers, cookies_coffee, hummus, milk) were then re-pulled directly via `git show origin/master:bari-web/src/data/comparisons/<file>` and re-verified: crackers 81.6/A n=19 (unchanged, was already correct), cookies_coffee 9/117 C-or-better (unchanged), hummus חומוס מסעדות 70.6/B sodium 231mg (unchanged), milk three A-grades at 85 (unchanged). Only bread required correction. Channel/IG/FB identifiers were cross-checked against two independently closed, build-verified tasks (467, 469) rather than assumed from memory. No health claims, no scores fabricated, no group names invented and presented as real. Lesson encoded in the checklist's own 'finding-posts engine' section: verify against the live deploy branch, not whatever local tree happens to be checked out, since this repo's local state can diverge from origin/master."
}
```
