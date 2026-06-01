# Hummus Category — Launch Plan

**Task:** TASK-058  
**Owner:** Frontend Agent  
**Date:** 2026-05-31  
**Goal:** `/hashvaot/hummus` live in production as Bari's reference Gen 1 comparison category  
**Input documents:** hummus_status_audit.md, hummus_gap_analysis.md

---

## Launch Readiness Summary

| Layer | Ready? | Blocker |
|---|---|---|
| BSIP0 corpus | YES | — |
| BSIP1 canonical | YES (with caveats) | Fat data corrupted — decision required |
| BSIP2 scoring | YES | run_002 is authoritative |
| QA validation | YES | PASS verdict on file |
| Frontend dataset JSON | NO | Must be built from run_002 output |
| Website integration | NO | 5 frontend files missing |
| Hebrew category copy | NO | Not authored |
| Product insight lines | NO | 69 lines required |
| QA — frontend page | NO | Cannot begin until page exists |
| Go-live approval | NO | Downstream of all above |

---

## Phase Overview

| Phase | Name | Duration estimate | Output |
|---|---|---|---|
| 0 | Decision gate | 1 day | Product Agent decision on HUM-001 fat data |
| 1 | Data preparation | 3–5 days | `hummus_frontend_v1.json` ready for website repo |
| 2 | Website integration | 3–5 days | Route, registry, component live on feature branch |
| 3 | Content | 5–10 days | Hebrew copy + 69 insight lines |
| 4 | QA + approval | 2–3 days | QA PASS + go-live approval |
| **Total** | | **~2–4 weeks** | **`/hashvaot/hummus` in production** |

Phases 1 and 3 can proceed in parallel from Day 2 onward. Phase 2 depends on Phase 1. Phase 4 depends on Phases 2 and 3.

---

## Phase 0 — Decision Gate

**Duration:** 1 day  
**Owner:** Product Agent  
**Output:** Written decision on HUM-001 fat data handling

### Step 0.1 — Product Agent decides fat data strategy

**Issue:** 59 of 69 BSIP1 records have corrupted `fat_g` values (scraper captured saturated fat sub-row instead of total fat). Scores are valid (`allowed_with_warning`). The corruption is a display problem only.

**Decision required:**

| Option | Action | Launch impact |
|---|---|---|
| **B — Suppress** (recommended) | Exclude `fat_g` from nutrition display panel in hummus frontend JSON | No delay. Add one sentence to MethodologyFooter: "ערכי שומן לא מוצגים בגרסה זו עקב איכות נתוני המקור." |
| **C — Flag** | Show fat values with `"ערך חלקי"` indicator where `fat_g < 1.0` and product contains tahini | +S effort for Frontend Agent |
| **A — Re-scrape** | Manually correct 59 fat values before building frontend dataset | +1–2 week delay |

**Recommended:** Option B. Suppressing fat display is cleaner than showing wrong data. BSIP2 scores are unaffected. Nutrition Agent should confirm this is acceptable.

**Deliverable:** Product Agent communicates decision in writing to Data Agent, Content Agent, and Frontend Agent.

---

## Phase 1 — Data Preparation

**Duration:** 3–5 days  
**Owner:** Data Agent  
**Dependency:** Phase 0 decision  
**Output:** `hummus_frontend_v1.json` copied to `C:\Users\HP\bari\src\data\comparisons\`

### Step 1.1 — Adapt build script for hummus

**File:** `C:\Bari\03_operations\bsip2\build_frontend_dataset.py` (or equivalent)

Adaptations required:
- Category ID: `"hummus"`
- Data source: `C:\Bari\02_products\hummus\canonical_bsip1\` + `C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_002\`
- **Do not use run_hummus_001** — it is INVALID
- Apply fat handling per Phase 0 decision (suppress if Option B)
- Filter dimensions: 3 maximum. Recommended for hummus:
  - `"הכל"` (all products — always first)
  - `"טיב ציון"` (score tier: A–B / C / D–E)
  - `"סוג מוצר"` (product type: חומוס / מטבוחה / סלטים אחרים)
- Confidence field: populate from QA trace (`verified` / `partial` / `insufficient`) per product
- `insightLine`: leave empty string (`""`) at this stage — Content Agent fills in Phase 3

**Validation checklist for Data Agent after build:**
- [ ] 69 products present in output
- [ ] All products have score + grade populated
- [ ] `fat_g` absent from nutrition object (if Option B)
- [ ] `imageUrl` present for all 69 (100% image coverage confirmed in BSIP0)
- [ ] All `insightLine` values are `""` (placeholder)
- [ ] Schema validates against `BariCategoryPageVM` type definition
- [ ] No BSIP, NOVA, or framework vocabulary in any string field

### Step 1.2 — Run build script

```powershell
# From C:\Bari\03_operations\bsip2
python build_frontend_dataset.py --category hummus --run run_hummus_002 --output hummus_frontend_v1.json
```

**Output location:** `C:\Bari\03_operations\bsip2\outputs\hummus_frontend_v1.json`

### Step 1.3 — Schema validation

Validate output against `BariCategoryPageVM` schema before copying to website repo. Any schema violation must be fixed before proceeding.

### Step 1.4 — Copy to website repo

```powershell
Copy-Item "C:\Bari\03_operations\bsip2\outputs\hummus_frontend_v1.json" `
          "C:\Users\HP\bari\src\data\comparisons\hummus_frontend_v1.json"
```

Confirm file is present in `C:\Users\HP\bari\src\data\comparisons\` before signaling Phase 2.

---

## Phase 2 — Website Integration

**Duration:** 3–5 days  
**Owner:** Frontend Agent  
**Dependency:** Phase 1 complete (JSON in website repo)  
**Output:** Feature branch with all 5 website files, building cleanly, page rendering on localhost

### Step 2.1 — Create feature branch

```powershell
# From C:\Users\HP\bari
git checkout -b feature/hummus-category
```

All Phase 2 work is done on this branch. Do not merge to main until Phase 4 approval.

### Step 2.2 — Create category definition file

**Create:** `C:\Users\HP\bari\src\lib\comparisons\registry\categories\hummus.ts`

Template from `maadanim.ts`. Key fields:

```typescript
export const hummusCategoryDefinition: ComparisonCategoryDefinition = {
  id: 'hummus',
  routePath: '/hashvaot/hummus',
  metadata: {
    title: 'השוואת חומוס — 2026 | ברי',      // Content Agent provides in Phase 3
    description: '...',                         // Content Agent provides in Phase 3
  },
  getPageData: async () => {
    // transform hummusData → BariCategoryPageVM
  },
  getCorpusPayload: () => ({
    products: hummusData.products,
    meta: { category: 'hummus', productCount: 69 }
  }),
}
```

**Note:** Leave `metadata.description` as a placeholder (`'TODO'`) until Content Agent delivers copy in Phase 3. The build should not fail on this.

### Step 2.3 — Update category registry

**Edit `C:\Users\HP\bari\src\lib\comparisons\registry\types.ts`:**

```typescript
// Add "hummus" to the union
export type ComparisonCategoryId = "maadanim" | "bread" | "snacks" | "yogurts" | "hummus"
```

**Edit `C:\Users\HP\bari\src\lib\comparisons\registry\index.ts`:**

```typescript
import { hummusCategoryDefinition } from './categories/hummus'
// Add hummusCategoryDefinition to the registry map
```

Run `npm run lint` and `npm run build` after this step. TypeScript must compile cleanly before proceeding.

### Step 2.4 — Create route page

**Create:** `C:\Users\HP\bari\src\app\hashvaot\hummus\page.tsx`

Template from `maadanim/page.tsx`. Standard Next.js App Router pattern — call `getComparisonCategory('hummus')`, render the comparison page component.

Generate `generateMetadata` function alongside the page component for Next.js metadata.

### Step 2.5 — Create comparison page component

**Create:** `C:\Users\HP\bari\src\components\comparisons\hummus-comparison-page.tsx`

**This is the reference Gen 1 implementation.** Must conform strictly to all Gen 1 rules:

**Mandatory structure (4 sections, exact order):**
```
[1] CategoryHero      — hero.tagline, hero.productCount
[2] CategoryPrologue  — prologue.sentences[]
[3] ProductTable      — products[], filters[]
[4] MethodologyFooter — methodology text (12px / #AAAAAA)
```

**Forbidden patterns (any of these = QA FAIL):**
- Grade chip background that varies by grade value
- Grade letter with label text ("B · גבוה")
- Expansion that opens as sheet, modal, or overlay
- Heading tags inside expansion section
- Methodology wrapped in card, border, or `<details>`
- Filter visible at 0px scroll
- More than 3 filter dimensions
- Any framework vocabulary in rendered text (NOVA, BSIP, cap, floor, structural_class, matrix_integrity)

**Desktop split:**
```typescript
<>
  {/* Mobile — max-lg */}
  <div className="max-lg:block hidden">
    <ComparisonShelfPage data={data} />
  </div>
  {/* Desktop — lg+ */}
  <div className="hidden lg:block">
    <BariComparisonDesktopPage data={data} />
  </div>
</>
```

**RTL checklist:**
- Product names: `text-right`
- Insight lines: `text-right`
- Score chip: top-right of row
- Nutrition grid: right-aligned
- Sticky filter button: `fixed bottom-right`

### Step 2.6 — Local build verification

```powershell
# From C:\Users\HP\bari
npm run lint
npm run build
```

Both must pass cleanly before Phase 3 begins. Lint errors or TypeScript errors on the hummus files are not acceptable — fix immediately.

Verify on localhost:
- `/hashvaot/hummus` loads without errors
- 69 product rows render
- Expansion sections open (inline, not as sheet/modal)
- Filters render and work
- Mobile layout correct at 375px viewport
- Desktop layout correct at 1280px viewport

**Note:** At this stage, insight lines will be empty and meta description will be placeholder. This is expected — Phase 3 fills them in.

---

## Phase 3 — Content

**Duration:** 5–10 days  
**Owner:** Content Agent (primary), Nutrition Agent (review)  
**Dependency:** Phase 1 (needs data for accuracy). Runs in parallel with Phase 2.  
**Output:** Hebrew copy for all 4 text slots + 69 product insight lines, Nutrition Agent reviewed

### Step 3.1 — Category copy (4 slots)

Content Agent delivers:

| Slot | Field | Where it goes |
|---|---|---|
| Meta title | `metadata.title` | `hummus.ts` |
| Meta description | `metadata.description` | `hummus.ts` |
| Hero tagline | `hero.tagline` (in build script or JSON) | `hummus_frontend_v1.json` |
| Prologue sentences | `prologue.sentences[]` (2–3 sentences) | `hummus_frontend_v1.json` |
| Methodology text | `methodology.text` (2–4 sentences) | `hummus_frontend_v1.json` |

**Constraints for all copy:**
- No NOVA, BSIP, cap, floor, structural_class, matrix_integrity, pillar, dimension
- No health claims
- No ALL CAPS in Hebrew text
- Meta title: ≤60 characters
- Meta description: ≤155 characters
- Hero tagline: must fit ≤280px mobile height (single sentence)
- Prologue: 2–3 sentences, consumer language, include product count (69)
- Methodology: 2–4 sentences at 12px / #AAAAAA — explains what the comparison measures, not how

If Option B (fat suppression) was selected in Phase 0, include one sentence in methodology: "ערכי שומן לא מוצגים בגרסה זו עקב איכות נתוני המקור."

### Step 3.2 — Product insight lines (69 products)

Content Agent writes one insight line per product. Each line:
- Brief (1 sentence or phrase, < 80 chars in Hebrew)
- Describes the product, not the scoring mechanism
- Positive, negative, or neutral — no moralizing
- Must be accurate — cross-referenced against BSIP2 trace signals from run_hummus_002
- No framework vocabulary

**Approach for 69 lines:**
Work in batches by product type:
1. Plain hummus (estimated 15–20 products) — batch 1
2. Flavored hummus (10–15 products) — batch 2
3. Light hummus (5–8 products) — batch 3
4. Eggplant / matbucha / other spreads (20–25 products) — batch 4

**Nutrition Agent review:** All 69 insight lines reviewed for factual accuracy before handoff to Frontend Agent. Any line that implies a health benefit ("מגן על הלב", "מחזק עצמות") must be flagged and rewritten.

### Step 3.3 — Integrate copy into frontend

After Nutrition Agent and Product Agent approve copy:

**Data Agent** updates `hummus_frontend_v1.json` with:
- `prologue.sentences[]`
- `methodology.text`
- `hero.tagline`
- `insightLine` per product (69 values)

**Frontend Agent** updates `hummus.ts` with:
- `metadata.title`
- `metadata.description`

Re-copy updated JSON to website repo:
```powershell
Copy-Item "C:\Bari\03_operations\bsip2\outputs\hummus_frontend_v1.json" `
          "C:\Users\HP\bari\src\data\comparisons\hummus_frontend_v1.json" -Force
```

---

## Phase 4 — QA and Go-Live

**Duration:** 2–3 days  
**Owner:** QA Agent (audit), Product Agent (go-live approval)  
**Dependency:** Phase 2 + Phase 3 both complete  
**Output:** Go-live approval → merge feature branch to main

### Step 4.1 — QA Agent audit

QA Agent runs the hummus comparison page audit. Checklist:

**Content checks:**
- [ ] All 69 products render with name, score chip, insight line
- [ ] No insight line uses framework vocabulary
- [ ] No insight line makes a health claim
- [ ] Hero tagline present and fits mobile viewport (≤280px height)
- [ ] Prologue renders (2–3 visible sentences)
- [ ] Methodology renders at 12px / #AAAAAA, no card/border wrapper

**Layout checks (mobile, 375px):**
- [ ] Collapsed row height ≤80px
- [ ] Product image 48px
- [ ] Score chip: grade-agnostic, no color variation by grade
- [ ] Expansion opens inline (no sheet, no modal, no overlay)
- [ ] Sticky filter button: fixed bottom-right, hidden until 300px scroll
- [ ] Filter panel: 3 dimensions maximum
- [ ] `dir="rtl"` applied

**Layout checks (desktop, 1280px):**
- [ ] Two-column layout renders via `BariComparisonDesktopPage`
- [ ] No overlap with mobile layout (proper breakpoint split)

**Technical checks:**
- [ ] `<title>` in `<head>` contains Hebrew title
- [ ] `<meta name="description">` present and ≤155 chars
- [ ] `hreflang="he"` present
- [ ] `lang="he"` on `<html>`
- [ ] `dir="rtl"` on `<html>`
- [ ] No Gen 0 component imports in hummus-comparison-page.tsx
- [ ] `npm run build` passes cleanly on the branch

**QA verdict:** PASS / FAIL. Any FAIL item blocks go-live approval. WARN items are logged and deferred.

### Step 4.2 — Fix QA findings

Frontend Agent addresses any FAIL items. QA Agent re-verifies each fix.

### Step 4.3 — Product Agent go-live approval

Product Agent reviews:
- QA PASS verdict
- Content Agent and Nutrition Agent sign-off on copy
- Data Agent confirmation that run_hummus_002 is the live dataset source
- Decision from Phase 0 implemented correctly

If all inputs are present, Product Agent issues go-live approval in writing.

### Step 4.4 — Merge and deploy

```powershell
# From C:\Users\HP\bari, on feature branch
git checkout main
git merge feature/hummus-category
```

Deploy per standard deployment procedure.

**Post-launch verification (Marketing Agent):**
- Confirm `/hashvaot/hummus` is indexed by Google Search Console (submit sitemap)
- Confirm `hreflang` visible in GSC International Targeting report
- Add hummus to newsletter content calendar (first issue within 2 weeks of launch)
- Draft 5 Pillar 3 social findings from run_hummus_002 data for WhatsApp distribution

---

## Reference Implementation Declaration

When this launch is complete, `/hashvaot/hummus` becomes Bari's **reference Gen 1 implementation**. All future category launches copy this pattern.

**What "reference implementation" means:**

| Future category | Uses hummus as template for |
|---|---|
| דגני בוקר | Category definition file structure, route pattern, component structure |
| גבינות רכות | Gen 1 component checklist, RTL rules, expansion pattern |
| Any new category | BSIP2 → frontend JSON build script (adapted per category) |
| Any content team member | Insight line format, copy constraints, methodology text pattern |

Frontend Agent must annotate `hummus-comparison-page.tsx` with a single comment at the top of the file:

```typescript
// Reference implementation for Bari Gen 1 comparison categories.
// New categories: copy this file, rename, update data import.
```

That is the only comment permitted in the file.

---

## Timeline (Optimistic / Conservative)

| Phase | Optimistic | Conservative |
|---|---|---|
| Phase 0 — Decision | Day 1 | Day 2 |
| Phase 1 — Data (starts Day 2) | Day 2–4 | Day 2–7 |
| Phase 2 — Frontend (starts when Phase 1 done) | Day 5–8 | Day 8–14 |
| Phase 3 — Content (starts Day 2, parallel) | Day 2–10 | Day 2–18 |
| Phase 4 — QA + approval (starts when 2+3 done) | Day 11–13 | Day 19–23 |
| **Launch** | **Day 13** | **Day 23** |

Content (Phase 3) is on the critical path if insight lines take longer than expected. 69 insight lines × 15 minutes each = ~17 hours of writing. Batching by product type reduces context-switching and speeds this up.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Phase 0 decision delayed | Medium | Delays Phase 1 | Escalate to Product Agent on Day 1 |
| Insight line volume underestimated | High | Delays Phase 4 | Start Content Agent on Day 2, do not wait for Phase 2 |
| Build script incompatible with hummus data shape | Medium | Delays Phase 1 by 1–3 days | Data Agent tests against first 5 products before batch run |
| QA finds Gen 0 pattern in component | Low | Minor rework | Frontend Agent self-reviews against forbidden patterns list before submitting to QA |
| Fat values shown despite suppression decision | Low | Consumer-facing bad data | QA Agent explicitly checks fat display in nutrition panel |
| run_hummus_001 data accidentally used | Low | Wrong scores for 44 products | Data Agent must verify `run_hummus_002` in every pipeline step |
