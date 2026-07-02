# Project Gen Z — Agent Handover

**Last updated:** 2026-06-29  
**Audience:** Next AI agent (Frontend, Content, Orchestrator) picking up Gen Z homepage work  
**Conversation source:** [097f6435-b403-4963-8422-b189ee607c02](C:/Users/HP/.cursor/projects/c-Bari/agent-transcripts/097f6435-b403-4963-8422-b189ee607c02/097f6435-b403-4963-8422-b189ee607c02.jsonl)

---

## 1. What this project is

**Project Gen Z** modernizes bari.digital for Israeli audience 18–28 without turning Bari into alarmist wellness, bro-science, or winner/loser shopping advice.

**Strategic frame (five-agent review):** Evolve Bari into a **consumer intelligence app** — fast, visual, evidence-backed shelf decoding. Backbone = external proposal Bundle C; selective Bundle A; **reject Bundle B** wholesale (dark UI, Buy/Skip, lie-detected framing).

**Repo home:** `c:\Bari\project_gen_z\` (specs, mocks, copy)  
**Implementation home:** `c:\Bari\bari-web\` (Next.js — only touch when implementing)

---

## 2. Hard rules (non-negotiable)

| Rule | Detail |
|------|--------|
| **OFF banned forever** | No Open Food Facts — any field, any purpose. Scrape-only corpus. |
| **No invented data** | Product names, scores, nutrition, images must come from Bari corpus or approved scrape URLs. |
| **No scoring changes** | Unless explicit TASK instructs it. |
| **No Buy/Skip / lie framing** | No "פער שיווקי", no red loser / green winner moral labels. |
| **Category-relative tone** | Scores differ by grade palette OK; copy stays neutral, not מנצח/מפסיד. |
| **Hebrew consumer copy** | **Content Agent + Adversarial QA / Red Team** sign-off before owner sees it. Orchestrator must NOT author Hebrew inline. |
| **Palette** | Cream `#F7F7F2`, green `#167A58` / `#1F8F6A`. No dark-primary rebrand. |
| **Hero visual style** | **Clean stage + smart overlays + one product story.** NOT a CSS collage of floating PNGs. See v5 spec. |

---

## 3. Phase 1 scope (owner locked)

### Approved (build)

| ID | Item | Status in bari-web |
|----|------|-------------------|
| P1-01 | Homepage hero | **In progress** — pass 4 (v5 layout) on branch/local, **not deployed** |
| P1-02 | Carousel | Live carousel exists; copy/visual fixes only — do not remove cards |
| P1-03 | Product card | Not started — prototype on `/dev/project-genz` when opened |
| P1-05 | Product Battle | Not started |
| P1-06 | Comparison tool MVP | Not started |
| P1-07 | Shelf flow | Not started |
| P1-10 | About + methodology | Not started |
| P1-11 | Share card | Not started |
| P1-12 | AI / data | SEO deploy done separately on production (sitemap, /ai-index, etc.) |

### Dropped (do not build)

- P1-04 Hashvaot hub refresh  
- P1-08 Percentile + signal strip  
- P1-09 Disclaimer footer  

Full list: `SCOPE.md`, `OWNER_DECISIONS.md`, `dropped/DROPPED_ITEMS.md`

---

## 4. Hero + comparison — what the owner wants (v5 authority)

**Layout authority:** `prototypes/HERO_V5_LAYOUT_SPEC.md`  
**Owner reference file:** `c:\Users\HP\Downloads\bari_homepage_v5_layout_fix.html`  
**Locked copy:** `content/HERO_COPY_DRAFT.md`, `src/lib/home/hero-copy.ts` in bari-web

### Hero layout (critical)

- Page `dir=rtl`, but **hero grid `direction: ltr`** with `grid-template-areas: "visual copy"`
- **Physical layout:** visual **LEFT**, Hebrew copy **RIGHT** (copy column `direction: rtl`)
- **One composed stage image** inside rounded cream shell — NOT individually positioned pack tiles in CSS
- Eyebrow: `ניתוח מוצרים · המדף הישראלי`
- Headline, subline, CTAs per locked copy (see below)
- Mobile: copy first, then visual

### Hero copy (owner locked)

| Slot | Hebrew |
|------|--------|
| Eyebrow | ניתוח מוצרים · המדף הישראלי |
| Headline 1 | האריזה מספרת סיפור. |
| Headline 2 | בארי בודקת את הרכיבים. (line break after "בארי בודקת את" OK) |
| Subline | חפשו מוצר מהסופר וקבלו תשובה פשוטה: מה טוב, מה בעייתי, ומה בעיקר שיווק. |
| Primary CTA | חפשו מוצר → `/hashvaot` |
| Secondary | סריקת ברקוד בקרוב (muted text below button, not inside button) |

### Comparison section

- **Centered** section head (not left + side blog row)
- Title: `השוואות מהמוצרים שאתם צורכים ביום יום`
- Subtitle: `לא כל מה שנראה דומה — באמת דומה.`
- Featured pilot: דגני בוקר — `מי באמת פחות מתוק?`
- Real corpus duel: **Vitabix** (`bsip1_cereal_5010029000061`, ~75 B, 4.2g sugar) vs **Lyon** (`bsip1_cereal_5900020036407`, 55 C, 24.7g sugar)
- Editorial story card OR single image inside `comparison-shell` — v5 used one PNG; production should use **real data** in HTML matching that panel layout

---

## 5. Implementation history (do not repeat mistakes)

| Attempt | What happened | Verdict |
|---------|---------------|---------|
| v1/v2 wireframes | Clinical, passive, meaningless strip | Rejected |
| v3 | Broken grid, harsh overlays | Rejected |
| v4 | Owner liked structure but **פער שיווקי** badge | Deprecated for hero |
| North-star screenshot | Light palette, still-life, featured card mood | Direction OK; adapt not pixel-copy |
| Pass 1–3 (CSS collage) | 5–6 floating Shufersal packs, radar chips | Owner: "not close" / "beautiful chaos" — **wrong** |
| Pass 3 editorial card | Story column + VS + bullets | Closer on comparison logic; hero still wrong |
| **Pass 4 (v5)** | LTR grid, single hero PNG, centered comparison shell | **Current target** — owner approved direction via v5 HTML |

### Rejected external specs

- Gemini winner/loser duels, invented scores, neon brutalist UI  
- Bundle B rebellious CTAs, Marketing Lie banner  

---

## 6. Current bari-web state (pass 4 — local, not production)

**Build passes** (`npm run build` in `bari-web`). **Not deployed** to bari.digital as of handover.

### Files touched (P1-01)

| File | Role |
|------|------|
| `src/components/home/home-hero.tsx` | v5 LTR grid, typography, eyebrow, gradient CTA |
| `src/components/home/hero-product-stage.tsx` | Single `<img>` in rounded shell |
| `src/lib/home/hero-copy.ts` | Locked Hebrew strings |
| `src/components/home/home-comparisons.tsx` | Centered section head, comparison shell |
| `src/components/home/featured-comparison-card.tsx` | Editorial duel card with real corpus data |
| `src/lib/home/featured-cereal-duel.ts` | Vitabix vs Lyon from `cereals_frontend_v2.json` |
| `public/home/hero-product-stage.png` | Extracted from owner v5 HTML (interim asset) |
| `public/home/featured-cereal-duel-stage.png` | Extracted from owner v5 HTML (reference) |

### Legacy / unused (safe to delete later)

- `hero-still-life.tsx`, `hero-still-life-products.ts`, `hero-decorative-radar.tsx`, `hero-decorative-score-ring.tsx` — collage approach, no longer imported from `home-hero.tsx`

### Known gaps vs v5

1. **Hero image** is owner v5 PNG — production should replace with corpus-composed stage (real packs + Bari UI overlays), still as **one asset**
2. **Comparison** uses HTML `FeaturedComparisonCard` inside shell, not the v5 comparison PNG — verify owner wants live data panel vs static image
3. **Mobile grid** — verify `hero-v5-grid` class applies correctly for copy-first stack
4. **Content + Red Team** — copy is owner-locked for structure; gates still required before production promote

---

## 7. Preview files (no server needed)

| File | Purpose |
|------|---------|
| `prototypes/mocks/hero-pass4-preview.html` | **Use this** — v5 layout, UTF-8 Hebrew, Heebo font |
| `prototypes/mocks/assets/hero-product-stage.png` | Hero stage image for preview |
| `prototypes/mocks/assets/featured-cereal-duel-stage.png` | Comparison reference image |

**Pitfall:** Never write Hebrew HTML via PowerShell `Set-Content` without UTF-8 — causes mojibake (`×”××¨×™×–×”`). Use Python `write_text(encoding="utf-8")` or the Write tool.

---

## 8. Content workflow

1. Authoring: Content Agent (or approved lane — not orchestrator-only)  
2. Gate: Adversarial QA / Red Team  
3. Owner sees copy only after both sign-offs  

Docs: `content/CONTENT_GATES.md`, `content/HERO_COPY_DRAFT.md`

---

## 9. Recommended next steps (priority order)

1. **Owner review** of `hero-pass4-preview.html` or local `npm run dev` homepage  
2. **Replace hero PNG** with production asset: one composed stage from real Shufersal scrape URLs + decorative score/radar/chips (illustrative OK on hero; scores on hero must not be invented if labeled as real)  
3. **Align comparison panel** to v5 comparison image layout while keeping `getFeaturedCerealDuel()` real data  
4. **Content + Red Team** sign-off on any copy drift  
5. **Deploy** via `C:\bari_pub380` worktree → `git push origin master` (owner pattern from prior SEO deploy) — only after owner approves  
6. Continue P1-03+ on `/dev/project-genz` preview route per `PHASE1_PLAN.md`

---

## 10. Key docs index

| Path | Read when |
|------|-----------|
| `README.md` | Orientation (update status — implementation has started) |
| `SCOPE.md` | What is in / out of Phase 1 |
| `OWNER_DECISIONS.md` | Owner verbatim locks |
| `prototypes/HERO_V5_LAYOUT_SPEC.md` | **Hero + comparison layout law** |
| `prototypes/HERO_FRONTEND_BRIEF.md` | Earlier brief (superseded on layout by v5; copy still valid) |
| `PHASE1_PLAN.md` | Build order, gates |
| `AGENT_REVIEWS.md` | Why decisions were made |
| `data/AI_DATA_PHASE1.md` | SEO / AI indexing (partially shipped) |
| `c:\Bari\CLAUDE.md` | Repo hard rules, OFF ban, content sign-off |

---

## 11. Deploy / production notes

- Production site **bari.digital** still has **old homepage hero** until Gen Z pass is merged and deployed  
- SEO work (sitemap, `/ai-index`, robots) already on production — separate from Gen Z hero  
- Google indexing sparse at handover; resubmit sitemap after major homepage deploy  

---

## 12. One-paragraph brief for the next agent

Implement Project Gen Z P1-01 per **v5 layout** (`HERO_V5_LAYOUT_SPEC.md`): LTR-locked hero with visual left / copy right, **one stage image** (not CSS pack collage), locked Hebrew copy with eyebrow, centered comparison section with real Vitabix vs Lyon corpus data in an editorial shell. Respect OFF ban, no lie-detected framing, Content + Red Team gates. Preview at `prototypes/mocks/hero-pass4-preview.html`. Code in `bari-web` pass 4 exists locally — finish asset swap, owner approval, then deploy. Do not rebuild floating collage heroes.
