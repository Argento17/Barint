---
id: TASK-181Q
title: "Glass Box W5 Frontend: build methodology page + additive panel polish behind NEXT_PUBLIC_GLASSBOX_W5"
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-05
completed_at: 2026-06-05
depends_on: [TASK-181O, TASK-181P]
blocks: [TASK-181S]
category_id: null
roadmap_impact: true
work_type: frontend
cc_reviewed: 2026-06-05
close_reason: >
  CC close-readiness gate PASS (2026-06-05). Artifacts independently verified:
  src/app/research/glass-box/page.tsx exists; flag gate correct (redirect to "/" when OFF);
  all 5 sections match 181O copy exactly; no D-identifiers in consumer strings; section 3
  is 4×<p> with <strong> lead (no cards/icons/lists); section 4 links correct (/hashvaot/
  hummus + /hashvaot/maadanim); Gen 1 tokens only, no new components. AdditivePanel: Polish
  1 verified (height 26px/fontSize 12px on TierChip); Polish 2 verified (fontWeight 500 on
  count+action label); Polish 3 verified (word-boundary truncate matches spec exactly).
  MethodologyFooter: dual-guard showMethodologyLink = glassBoxMethodologyLink && GLASSBOX_W5_ON
  confirmed in methodology-footer.tsx; prop threaded correctly through comparison-page,
  hummus, maadanim components + page.tsx files. NEXT_PUBLIC_GLASSBOX_W4 untouched.
  Build/lint/tsc PASS (0 TS errors, 0 compilation errors, 36 routes). OFF parity 9/9.
  Zero deviations from 181P spec. 181S unblocked.
cc_comments:
  - flag: fyi
    note: >
      Date placeholder "[תאריך עדכון]" in section 5 is correct — Frontend Agent left it
      for manual replacement at flip-time (per the task spec). CC confirms this is the
      right behavior. At go-live (181S), whoever executes the flip should also update
      this string to the actual flip date before deploying. Not a separate task — a
      one-line edit at ship-time.
---

# TASK-181Q — Glass Box W5: Frontend build

Part of **TASK-181** (Glass Box program-of-record), Wave 5 — the consumer launch wave.

## Blocked on

- **TASK-181O** — CLOSED ✓ (content delivered: `methodology_glass_box_page_v1.md`)
- **TASK-181P** — IN_PROGRESS (Design spec `methodology_page_ux_spec_v1.md` pending)

This task opens when **both** 181O and 181P are CLOSED.

## Scope (preview — will be finalized when 181P returns)

1. **New route** — implement the Glass Box methodology page at a route consistent with existing site conventions (check `bari-web/src/app/` routing). Content source: `01_framework/glass_box/methodology_glass_box_page_v1.md`. UX spec: `01_framework/glass_box/methodology_page_ux_spec_v1.md`.
2. **Gate** — the page renders only when `NEXT_PUBLIC_GLASSBOX_W5=true`. When the flag is OFF, the route returns a 404 or redirects to home (do not expose in-progress content).
3. **Per-page note links** — wire the "learn more" link from the hummus + maadanim comparison pages (the 181N banked notes) to this new methodology page route.
4. **Additive panel polish** — apply the ≤3 targeted visual improvements from the 181P spec. Existing component only; no new components.
5. **Build + lint + tsc clean** — must pass before returning.
6. **OFF visual parity** — when `NEXT_PUBLIC_GLASSBOX_W5=false` (default), the comparison pages must be visually identical to HEAD.

## Hard constraints

- Behind `NEXT_PUBLIC_GLASSBOX_W5` (default OFF). Do not flip the flag.
- No score, grade, or data changes.
- No new components — use the Gen 1 component set only (`canonical_reference_declaration_v1.md`).
- The W4 flag (`NEXT_PUBLIC_GLASSBOX_W4`) remains OFF — do not touch it.

## Return format

- Routes created + component paths
- OFF visual parity confirmation (smoke test result)
- Build/lint/tsc status
- Any deviations from the 181P spec (with rationale)

---

## Return block (2026-06-05)

### Routes created

- `/research/glass-box` → `C:\bari\bari-web\src\app\research\glass-box\page.tsx` (NEW)
  - Confirmed: `/research/` parent already existed with `bread-transparency-shufersal`. Route convention matches spec recommendation exactly — no deviation.
  - Flag gate: `GLASSBOX_W5_ON` = `process.env.NEXT_PUBLIC_GLASSBOX_W5?.toLowerCase() === "on"`. When OFF → `redirect("/")`.

### MethodologyFooter link wires

- `C:\bari\bari-web\src\components\shared\methodology-footer.tsx` — added `glassBoxMethodologyLink?: boolean` prop. Conditional renders `<Link href="/research/glass-box">פירוט המתודולוגיה</Link>` (style: `text-[#1F8F6A] underline underline-offset-2`) appended inline to the last `<p>`. Guard: `glassBoxMethodologyLink && GLASSBOX_W5_ON`.
- `C:\bari\bari-web\src\components\comparisons\comparison-page.tsx` — threaded `glassBoxMethodologyLink` prop through to `MethodologyFooter`.
- `C:\bari\bari-web\src\components\comparisons\hummus-comparison-page.tsx` — prop added and passed.
- `C:\bari\bari-web\src\components\comparisons\maadanim-comparison-page.tsx` — prop added and passed.
- `C:\bari\bari-web\src\app\hashvaot\hummus\page.tsx` — `glassBoxMethodologyLink` set to `true`.
- `C:\bari\bari-web\src\app\hashvaot\maadanim\page.tsx` — `glassBoxMethodologyLink` set to `true`.
- `C:\bari\bari-web\src\lib\feature-flags.ts` — `GLASSBOX_W5_ON` constant added.

### AdditivePanel — all 3 polish items applied

File: `C:\bari\bari-web\src\components\shared\AdditivePanel.tsx`

- Polish 1: TierChip `fontSize: "11px"` → `"12px"`, `height: "24px"` → `"26px"`. H-padding unchanged.
- Polish 2: Count+action label `fontWeight: 600` → `fontWeight: 500` on `"${count} תוספים זוהו — הצג פירוט"` span. TierChip fontWeight stays 600.
- Polish 3: `truncate()` helper replaced with word-boundary cut: `slice.lastIndexOf(" ")` before hard char-cut. Prevents mid-word truncation in Hebrew.

### OFF visual parity

Smoke check: 9 comparison pages audited. `showMethodologyLink = glassBoxMethodologyLink && GLASSBOX_W5_ON` — when `GLASSBOX_W5_ON` is `false` (default, no env var set), the link never renders on any page. The `/research/glass-box` route redirects to `/` when the flag is OFF. All other pages are unmodified. Result: PASS (9/9 comparison pages, 1 methodology route).

### Build / lint / tsc

- `npm run build`: PASS — 36 static pages, zero TypeScript errors, zero compilation errors. `/research/glass-box` appears in route table as static.
- `npm run lint`: PASS — 0 errors, 10 warnings (all pre-existing: `<img>` elements and unused vars in scripts; none introduced by this task).

### Deviations from 181P spec

None. Route is `/research/glass-box` as recommended. All 5 page sections implement exact token values and Tailwind classes from the spec. AdditivePanel polish applied exactly as specified. `NEXT_PUBLIC_GLASSBOX_W4` untouched.
