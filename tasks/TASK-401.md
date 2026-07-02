---
id: TASK-401
title: Project Pop — Bari go-live (website readiness, legal/compliance, analytics, SEO, social)
owner: orchestrator
status: IN_PROGRESS
priority: CRITICAL
created_at: 2026-06-25
depends_on: []
blocks: []
category_id: null
summary: >
  Go-live program. WS0 deploy (verified: Argento17/Barint/master/bari-web/Vercel). WS1 website readiness sweep (waits on other chat pages+rescore). WS-Legal (5 docs + WCAG, drafts v2 market-aligned at tasks/scratch/P404_legal_drafts_he.md, opt-in CMP built). WS-Analytics (GA4 consent-gated + Search Console). WS-SEO. WS-Social. Goal=traffic/visibility.
---

# TASK-401 — Project Pop — Bari go-live (website readiness, legal/compliance, analytics, SEO, social)

## Progress log

**2026-06-25 — WS-Legal CLOSED + footer fixed (LIVE).** 5 legal docs filled
(coordinator תום בר-חיים, בארי טכנולוגיות, דב פרידמן 5 רמת גן, tbarhaim@gmail.com,
054-2626673), opt-in cookie CMP (mechanism B), /methodology page created + linked
from terms, noindex removed from all legal pages + added to sitemap, blank-footer
compositing bug fixed (`relative z-10 isolate`), footer cleanup (removed
השוואות/מדריכים + redundant separator). Master 2091d2b13 → 3e9d52192.

**2026-06-25 — WS-SEO phase 1 CLOSED (LIVE, master c1addcdc7).** Audited SEO
foundation on master: metadata on every route ✓, robots+sitemap ✓, OG defaults
he_IL ✓, FAQ-schema lib exists (wired 2/17 pages). Shipped 2 clean gaps via
worktree off master (build-verified, push, live-verified, worktree removed):
(1) self-referential canonicals — `alternates.canonical "./"` at root, inherited
by all routes (home→bari.digital, /hashvaot/hummus→.../hummus, confirmed in
prod HTML); (2) sitewide Organization + WebSite JSON-LD (new
`components/seo/site-structured-data.tsx`), owner-sourced values, no SearchAction
(no search endpoint). No scoring/corpus/order impact.

**2026-06-26 — WS-Analytics wiring DONE (LIVE, master 837d11d52).**
- GSC HTML verification file `public/google6709ceea1fb4f2e9.html` shipped
  (master 46bae08ce); live-verified 200 + correct content at site root. Owner
  to click VERIFY in Search Console, then submit sitemap.xml.
- GA4 Measurement ID **G-2KBNY4XZHS** (property "Bari", IL tz/₪) wired as the
  committed default for `NEXT_PUBLIC_GA_ID` (Vercel env still overrides; GA ID
  is non-secret). Build-verified the ID inlines into a client chunk; consent
  gate unchanged (opt-in only). Owner declined the manual gtag snippet (would
  double-count + bypass the CMP) — correct.
  - Definitive live test (owner): visit bari.digital → accept cookies → GA4 →
    Reports → Realtime should show 1 active user.

**2026-06-26 — GA4 send-bug FOUND + FIXED (LIVE, master f9fcb1caf).** Owner
red-team caught it: in prod with consent accepted, `gtag/js?id=G-2KBNY4XZHS`
loaded (200) but **zero `/collect` hits** ever fired (Realtime stuck at 0).
Root cause = two defects in the consent-gated loader: (1) gtag stub pushed a
plain ARRAY to dataLayer instead of the `arguments` object → gtag.js never
processed the queued commands; (2) `config` (pageview) was queued at mount
before gtag.js loaded, relying on a replay that never sent. Fix: canonical
`arguments` stub + fire consent→granted/js/config in the Script `onLoad` (after
library present AND consent granted). **Verified end-to-end** (next start +
Playwright, consent pre-seeded): browser now POSTs
`.../g/collect?...&en=page_view&tid=G-2KBNY4XZHS` (gcs=G101). The "0 collect"
the owner observed is exactly the symptom; this is the real fix, not a guess.

**2026-06-26 — GA4 CONFIRMED LIVE (owner-verified).** In Incognito (no blocker):
`collect` returns **204**, GA4 Realtime shows **1 active user** + page_view/scroll
events + correct page title. Earlier prod "blocked" rows were a browser extension
on the owner's main browser (client-side, not a site issue — normal analytics
undercount). **WS-Analytics COMPLETE.** Remaining go-live lever: Search Console
VERIFY (file live) + submit sitemap.xml.

**2026-06-26 — Blog index cleanup shipped (master 6e0560ec6) + broken-link audit.**
De-listed 3 empty bread breakdowns from /blog (owner-approved; via master's
JSON architecture, NOT a cherry-pick — branches diverged TS-vs-JSON; live-verified
list = milk/sugar-alcohols/shemen-zayit + coming-soon teasers, owner kept teasers).
Then ran a launch broken-link/dead-route audit on master: 49 routes; header nav,
footer, /hashvaot category directory (all 17 *_COMPARISON_HREF), and 19 literal
links all RESOLVE ✓. Found **4 broken links on 3 indexed blog pages** (stale slugs
from category renames/wipe): `/blog/lechem`→/hashvaot/lechem ×2,
`/blog/sugar-alcohols`(featured)→/hashvaot/snack-bars, `/blog/yogurt`→/hashvaot/yogurt.
**Fixed 2** (master 2e8d94c44): →/hashvaot/bread and →/hashvaot/protein-bars
(build-verified in prerendered HTML). **yogurt NOT fixed — owner decision:** its
CTA "compare all 19 yogurts" targets a WIPED category; recommend noindex/delist
/blog/yogurt until the category exists (or repoint CTA to /hashvaot hub).
Broader flag: several blog routes are indexed but not in the curated index
(yogurt, hummus, bread-analysis, + the 3 bread breakdowns) — may be thin; offer a
launch-readiness pass to noindex non-ready ones.

**2026-06-26 — Owner ruling: blog = 3 curated only. DONE (master e8507281f).**
Owner: "I DON'T WANT THESE BLOGS." Removed all non-curated blog articles from
Google: noindex (robots index:false) on bread-everyday/bread-standouts/
bread-wellness-gap/hummus/lechem/yogurt (6) + sitemap BLOG_PATHS reduced to the 3
keepers (milk-analysis, shemen-zayit, sugar-alcohols), dropping the
/blog/bread-analysis redirect entry too. Routes NOT deleted (zero broken internal
links); pages just won't be indexed/submitted. Build-verified: 6 emit noindex, 3
keepers indexable, sitemap.xml = 3 blog URLs. (Earlier same day: fixed 2 broken
category links on lechem+sugar-alcohols, master 2e8d94c44.)
**Search Console: VERIFIED by owner** (property live, data processing). Pending
owner: Sitemaps → submit sitemap.xml. GA4 already confirmed live.

**2026-06-26 — Growth phase kicked off (owner: "do all three + open social").**
3 lanes dispatched in parallel (background), each returns DRAFTS/SPEC → QA gate →
owner sign-off (nothing consumer-facing ships un-gated):
- Social launch plan → Marketing Agent (platform pick, handle, pillars, 6-8
  grounded draft posts, owner-action list). Account creation = owner tripwire.
- FAQ rich-results PILOT (milk/hummus/magnesium) → content lane (Sonnet
  general-purpose); grounded in real page data, mirrors existing 2 _faq_schema
  examples; drafts only, Adversarial QA fabrication/citation gate before ship.
- OG per-category share-image system → Design Agent (spec + impl rec:
  dynamic Next ImageResponse vs static; conform frozen tokens).
- Text-accuracy sweep = GATED on the other chat's comparison-page rescore; not
  started blind.
Flow: drafts return → I run Adversarial QA → present to owner. FAQ/OG repo
wiring done by orchestrator in isolated worktrees after gate.

Returns:
- Social plan (Marketing) ✅ returned: IG primary + Threads, handle @bari.digital,
  4 pillars, 8 grounded draft posts (each cites a real page+finding), 6 owner
  actions, 3 self-flagged QA items (juices dist freshness, sugar-alcohols blog
  sign-off TASK-379, magnesium no-score count). → Adversarial QA gate RUNNING.
- OG image system (Design) ✅ returned SPEC: dynamic Next `opengraph-image.tsx`
  Option A (co-located per the 17 named dirs) + shared template
  `src/lib/og/category-og-template.tsx` + `og-category-data.ts`; full frozen-token
  layout; 5 flags (needs Heebo font binary in public/fonts/, Hebrew names from
  each page-data hero.eyebrow, twitter card→summary_large_image, null-score chip
  omit, magnesium diff data path). Ready for Frontend impl — QUEUED after FAQ.
- FAQ pilot (content lane) ✅ returned: 3 grounded FAQ JSON drafts (milk 18 prod,
  hummus 35 displayed [not 57], magnesium 18=15+3) w/ per-answer traceability;
  author refused to fabricate price/condition Qs. → Adversarial QA gate RUNNING.

QA gate — SOCIAL (returned): 7/8 SHIP. Post 3 (olive oil) HOLD = real HIGH
decontextualization ("13 בשופרסל" omits "מתוך 19, 2 רשתות") → 1-line fix. Post 5
"CRITICAL dead route /hashvaot/snack-bars" = FALSE POSITIVE: subagent read the
dirty task-374 WORKING TREE; origin/master already has /hashvaot/protein-bars
(my fix 2e8d94c44). LESSON: native QA/content subagents read C:\Bari (task-374),
NOT master — verify their file-state findings against origin/master before acting.
All 8 posts' numbers verified against real data; 0 OFF; 0 health claims.
Naturalness (F1/F2) gate INCOMPLETE — QA got fact-claims not full copy; do a
voice pass on final copy before publish.

QA gate — FAQ (returned): INVALID for our purpose. The QA reviewed STALE
task-374 working-tree artifacts (a hummus_faq_schema.json that does NOT exist on
master; hummus insightLines with "עוצר ב-B"/"מגיע ל-A" grade-mismatch text that
master does NOT have — verified: master hummus data 0 matches, task-374 tree 31
"עוצר"+2 "מגיע") and a self-generated rowVerdict milk FAQ — NOT the content-lane
drafts. So its CRITICAL/HIGH FAQ verdicts don't apply to production OR to the
actual drafts. NO production harm: master has only brined+cookies-coffee FAQ
files, clean hummus data. ACTIONS: (1) FAQ pilot needs a CLEAN re-validation
pointed at the actual drafts + master data before ship — not shippable yet.
(2) SIDE-FLAG for the Tom's Voice (task-374) chat: their in-progress hummus copy
may carry grade-mismatch insightLines ("עוצר ב-B" on a C product) — verify before
that branch merges. Reinforces the lesson: native subagents read task-374, not
master.

**2026-06-26 — SEO optimization program started (owner "let's start").** 9-item
prioritized action list set (titles/desc, FAQ, breadcrumbs, OG, internal links,
star-schema[hold], coverage, authority/social, weekly GSC review). Sitemap
SUBMITTED by owner; live sitemap verified clean (17 hashvaot + 3 blog, 0
noindexed). STARTED #1 (titles+descriptions): audit found all 17 comparison meta
titles are the generic formula "השוואת <cat> | Bari" while each page already has
punchy grounded hero copy → dispatched content lane to draft optimized
title+description per page (keyword + real-finding hook, ≤60/≤155 chars,
grounded, no fabrication) → Adversarial QA → owner sign-off. Queued behind:
breadcrumbs (mechanical, me), OG build (Frontend, spec ready), FAQ re-validation.

**2026-06-26 — Title/desc drafts returned + caught LIVE count bugs.** Content
lane produced 17 grounded optimized title+description drafts (e.g. cereals
"השוואת דגני בוקר|Bari" → "דגני בוקר: 20 מוצרים, אף אחד לא מגיע ל-A|Bari"). The
grounding work surfaced real DATA-INTEGRITY bugs on LIVE pages (verified on
master): breakfast-cereals/page.tsx meta says "37 מוצרי דגני בוקר" but data/hero
= 20 (CONFIRMED master); juices/page.tsx meta "65 מיצים" vs displayed 17
(social-QA-confirmed); hummus meta likely "57" vs displayed ~35 (loader excludes).
The new descriptions FIX these (use correct grounded counts). NEXT: verify every
hard count in the drafts against each page's actual DISPLAYED count (authoritative
= post-loader products length, NOT _meta scanned count) — read origin/master not
task-374 — then Adversarial QA → owner sign-off → wire (also fixes the live count
drift + the stale unused *ComparisonMetadata exports causing it).

### WS-SEO — remaining
- **OWNER-GATED:**
  - GA4: confirm Realtime shows traffic (above). Done once seen.
  - Google Search Console: click VERIFY (file is live), then Sitemaps → submit
    `sitemap.xml`.
- **CONTENT/DESIGN-GATED fast-follows (need two-gate sign-off, NOT inline):**
  - FAQPage JSON-LD rollout to the other 15 comparison pages (infra exists; needs
    real per-category FAQ content → Content Agent + Adversarial QA gate).
  - Per-category OG images (Design lane).
  - BreadcrumbList JSON-LD on hashvaot/blog (mechanical; queued).
