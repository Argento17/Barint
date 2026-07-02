# Handoff: Homepage Hero — "אתם יודעים באמת מה יש במוצרים שאתם צורכים?"

## Overview
The redesigned **homepage hero** for Bari (bari.digital). Full-viewport, RTL, on Bari's warm-paper canvas `#F7F7F2`. A bold two-line Hebrew headline with a green value line + a single "search a product" CTA on the **right**; a large, premium product still-life photograph bleeding off the **left** edge and dissolving into the page on every side. Goal: within three seconds a visitor understands what Bari does — it tells you what's really inside the packaged foods you buy.

## About the Design Files
The files here are a **design reference built in HTML** (`Hero.dc.html`, a streaming "Design Component" prototype). It shows intended look, spacing, copy, and motion — **not production code to ship**. Recreate it in the existing **Bari Next.js app** using its own stack: App Router, TypeScript, Tailwind v4 + shadcn/ui, framer-motion, lucide-react, `next/font` (Inter / Heebo / Geist Mono). Ignore the `<x-dc>` / `<helmet>` / `support.js` wrapper — that's prototype scaffolding. The meaningful markup is `<nav>` + `<section data-screen-label="Hero">`.

## Fidelity
**High-fidelity.** Colors, type, spacing, copy, motion are final. Rebuild pixel-accurately with the codebase's primitives (Tailwind bound to the existing CSS variables, shadcn `Button`, framer-motion entrances, lucide `Search`).

---

## Layout
- Page root: `dir="rtl"`, `lang="he"`, background `var(--canvas)` = `#F7F7F2`.
- **Sticky nav**, height `72px`, then the hero fills the rest of the viewport.
- **Hero = CSS grid, 2 columns:** `grid-template-columns: 0.92fr 1.12fr;` (RTL → **col 1 = right = headline**, **col 2 = left = photo**), `align-items:center`, `gap:clamp(16px,2vw,44px)`, `min-height:calc(100vh - 72px)`, `padding-block:clamp(32px,5vh,64px)`.
- The photo column **bleeds off the left page edge**; the headline column carries the right/inner padding.

## Component: Top Nav
- `position:sticky; top:0; z-index:50; height:72px;` flex, space-between, `padding:0 clamp(24px,4vw,64px)`, `background:rgba(247,247,242,0.82)`, `backdrop-filter:blur(14px)`, `border-bottom:1px solid var(--hairline-faint)` (`rgba(17,19,24,0.05)`).
- Nav is `dir="ltr"` so the **logo sits left, links right** (matches the intended composition even though the page is RTL).
- **Logo:** the real Bari lockup (wordmark + sprout mark). Prototype uses `assets/bari-logo.webp` at `height:56px; width:auto`. **In the app, use the existing `<BariBrandLogo />` component** (`src/components/brand/bari-brand-logo.tsx`, which renders `/bari-logo-optimized.webp`) — just render it a bit larger than default (the site's default is `h-[44px]`; this hero uses ~`h-[56px]`). Do **not** recreate the mark.
- **Links (right):** `השוואות`, `בלוג`, `מדריכים` — `15px/600`, `color:var(--fg2)`, `padding:8px 16px; border-radius:9999px`. Hover: `color:#111318; background:rgba(255,255,255,0.7)`. Wire to real routes.

## Component: Headline column (right)
- `padding-inline:clamp(28px,4.5vw,80px) clamp(16px,2vw,40px)`, flex column, `align-items:flex-start`.
- **H1** — font-heading, weight **800**, `letter-spacing:-0.045em`, `line-height:1.16`, `font-size:clamp(1.9rem,3.25vw,3.4rem)`, color `var(--fg1)` `#111318`. Two lines:
  > אתם יודעים **[באמת]** מה יש במוצרים שאתם צורכים?
  > **[בארי בודקת את זה בשבילכם]**
  - Green (`var(--bari-green)` `#1F8F6A`): the word **`באמת`** and the **entire second line**. Everything else ink.
- **Lead** — `font-size:clamp(1.05rem,1.25vw,1.25rem); line-height:1.7; color:var(--fg2); max-width:27em; margin-top:24px`:
  > חפשו מוצר מהסופר וקבלו תשובה פשוטה: מה טוב, מה בעייתי, ומה בעיקר שיווק.
- **Primary CTA** (shadcn `Button`, restyled): `margin-top:30px; min-width:300px`, inline-flex, `gap:11px`, `background:var(--bari-green); color:#fff; border-radius:14px; padding:18px 32px; font 18px/700`, `box-shadow:var(--shadow-cta)` = `inset 0 1px 0 rgba(255,255,255,0.20), 0 14px 40px -16px rgba(31,143,106,0.58)`. Leading icon **lucide `Search`** (20px, stroke 2.2). Label `חפשו מוצר`. Hover: `translateY(-1px)` + deeper shadow `…0 18px 50px -16px rgba(31,143,106,0.66)`, 500ms, no color change.
  - Action: open product search.
- **Secondary link** — `margin-top:18px; font-size:14px/600; color:var(--fg3); border-bottom:1px solid var(--green-ring)` (`rgba(31,143,106,0.25)`), `white-space:nowrap`:
  > סריקת ברקוד בקרוב  (coming-soon, inert)

## Component: Product photo (left, full-bleed, dissolving)
- Wrapper `position:relative; align-self:center`.
- **Image** — `width:100%; max-width:780px; height:auto; margin-inline-start:auto` (anchors left so it bleeds off-page).
- **Edge dissolve (the key detail)** — a CSS mask feathers every outward edge so the photo melts into `#F7F7F2` with no rectangle:
  ```css
  -webkit-mask-image:
    linear-gradient(to right,  #000 89%, transparent 100%),
    linear-gradient(to bottom, transparent 0%, #000 14%, #000 89%, transparent 100%);
  -webkit-mask-composite: source-in;   /* standard: */ mask-composite: intersect;
  ```
  Right edge fades (~last 11%), top fades (~first 14%), bottom fades (~last 11%); the left edge is untouched (bleeds off the viewport).
- **Background match** — the source photo has a warm cream background; the prototype asset (`assets/products.png`) was **white-balanced** (per-channel multiply ≈ R×1.006, G×1.03, B×1.04) so its background reads as `#F7F7F2` and blends with the page. **In production, prefer a product photo already shot/rendered on `#F7F7F2` (or a transparent PNG)** rather than relying on the mask + white-balance; then the same mask feather makes it dissolve perfectly.
- Products shown (the AI-generated still life, English labels): whole-grain oats box, rolled-oats jar, extra-virgin olive oil, natural yogurt 3%, a protein bar, almonds jar, blueberries, olives, olive branches. If Hebrew packaging is wanted, swap the photo — nothing here depends on the labels.

## Interactions & Motion
- **Entrance** = Bari "reveal-up" (use framer-motion): `opacity 0→1` + `translateY(16px→0)`, `760ms`, easing `cubic-bezier(0.22,1,0.36,1)` (`--ease-out-soft`). Stagger the headline: H1 `+80ms`, lead `+180ms`, CTA `+280ms`, link `+360ms`. The photo uses `translateY(22px→0)`, `1000ms`, delay `200ms`.
- **Respect `prefers-reduced-motion`** — disable entrance/hover motion.
- Nav-link + CTA hover states as above. No parallax / bounce.

## Responsive
Desktop-first. `<= ~768px`: collapse to one column, photo above or below the headline, full-width, drop the left-bleed (center it), keep the mask dissolve. Headline `font-size` is already fluid via `clamp()`. CTA full-width on mobile.

## Design Tokens (already in Bari `colors_and_type.css` / globals)
- **Brand:** `--bari-green #1F8F6A`, `--bari-green-bright #2FAE82`, `--bari-green-deep #176F53`
- **Ink/fg:** `--fg1 #111318`, `--fg2 #4E5663`, `--fg3 #7A817C`
- **Surface:** `--canvas #F7F7F2`, `--surface #FFFFFF`
- **Hairlines:** `--hairline rgba(17,19,24,0.08)`, `--hairline-faint rgba(17,19,24,0.05)`, `--green-ring rgba(31,143,106,0.25)`
- **Radius:** CTA `14px`; nav-link / secondary pills `9999px`
- **Shadow:** `--shadow-cta = inset 0 1px 0 rgba(255,255,255,0.20), 0 14px 40px -16px rgba(31,143,106,0.58)`
- **Motion:** `--ease-out-soft = cubic-bezier(0.22,1,0.36,1)`; reveal `760ms` (photo `1000ms`); hover `500ms`
- **Type:** headings/wordmark = Inter/Heebo 800 tight tracking; body = same stack 400, line-height 1.7; mono/eyebrow = Geist Mono. Use the app's existing `next/font` setup.

## Assets
- `assets/bari-logo.webp` — the real Bari lockup (copied from the repo's `public/bari-logo-optimized.webp`). In-app, render the existing `<BariBrandLogo />` instead of embedding this file.
- `assets/products.png` — hero product photo, white-balanced to `#F7F7F2` (see note above; swap for a clean/`#F7F7F2`-background shot in production). Use `next/image`.

## Files
- `Hero.dc.html` — the design reference (open in a browser to see look + motion).
- `assets/bari-logo.webp`, `assets/products.png` — hero assets.
