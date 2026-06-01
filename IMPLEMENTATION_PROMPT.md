# Task: Add subtle per-product photo theming to the comparison cards on `/hashvaot`

## Context
All comparison cards on `/hashvaot` render through one shared component,
`src/components/comparisons/comparison-intelligence-hero.tsx`. Because they share the
same green wave backdrop, every card looks identical and users can't tell them apart.

Goal: give each card a **subtle, product-specific photograph** bled into the bottom-left
corner (the empty side in our RTL layout), desaturated and soft-masked so it reads as quiet
background texture — NOT an illustration. The existing green brand system (CTA, badge,
"Bari Intel", insight box, grid backdrop) must stay 100% intact. The effect should be
quiet enough that the page still reads as one family, but distinct enough that the milk box,
bread box, hummus box, etc. are recognizable at a glance.

This was approved from a design prototype. Implement it exactly as specified below.

## Step 1 — Add a `theme` prop to `ComparisonIntelligenceHero`

In `comparison-intelligence-hero.tsx`:

1. Extend the props type:
   ```ts
   export type ComparisonHeroTheme = {
     /** muted product hue, used ONLY for the faint tint wash + (optional) future accents */
     accent: string;
     /** image URL — a /public path (preferred) or remote URL */
     photo: string;
   };
   // add to ComparisonIntelligenceHeroProps:
   theme?: ComparisonHeroTheme;
   ```

2. Inside the root card `<div className="relative overflow-hidden rounded-[1.35rem] ...">`,
   render the photo + tint layers **after** the two existing gradient `<div>`s and
   **before** `<ComparisonIntelligenceBackdrop />`. They must sit at `z-0`; the content
   wrapper already uses `z-[1]`, so text stays above them. All decorative, `aria-hidden`.

   ```tsx
   {theme ? (
     <>
       {/* product photo — bled in from the bottom-left, faded into the card */}
       <div
         aria-hidden
         className="pointer-events-none absolute inset-y-0 left-0 z-0 h-full w-[60%]"
         style={{
           backgroundImage: `url(${theme.photo})`,
           backgroundSize: "cover",
           backgroundPosition: "center",
           opacity: 0.62,
           filter: "grayscale(0.08) contrast(1.02) saturate(1.02)",
           WebkitMaskImage:
             "radial-gradient(135% 145% at 0% 100%, #000 30%, rgba(0,0,0,0.5) 56%, transparent 80%)",
           maskImage:
             "radial-gradient(135% 145% at 0% 100%, #000 30%, rgba(0,0,0,0.5) 56%, transparent 80%)",
         }}
       />
       {/* white veil so foreground text stays crisp over the photo */}
       <div
         aria-hidden
         className="pointer-events-none absolute inset-0 z-0"
         style={{
           background:
             "linear-gradient(105deg, transparent 0%, rgba(253,253,248,0.10) 38%, rgba(253,253,248,0.62) 64%, rgba(253,253,248,0.86) 100%)",
         }}
       />
       {/* faint product-hue tint wash in the corner */}
       <div
         aria-hidden
         className="pointer-events-none absolute inset-0 z-0 mix-blend-multiply"
         style={{
           background: `radial-gradient(60% 80% at 14% 96%, color-mix(in oklab, ${theme.accent} 13%, transparent), transparent 70%)`,
         }}
       />
     </>
   ) : null}
   ```

   Note: keep `<ComparisonIntelligenceBackdrop />` and `<ComparisonAnalysisParticles />` —
   the grid + waves should still show faintly OVER the photo, which keeps the brand feel.

## Step 2 — Pass a `theme` from each featured card

Each card component already wraps `ComparisonIntelligenceHero`. Add the matching `theme={...}`
prop to each. Mapping (accent hue chosen to be muted + on-brand; swap photos for real
Bari product photography when available):

| Component file | accent | photo — download to `/public/hashvaot/themes/` |
|---|---|---|
| `featured-milk-intelligence-card.tsx` | `#5C7FB0` | `milk.jpg` — https://images.unsplash.com/photo-1550583724-b2692b85b150?w=900&q=80 |
| `featured-bread-intelligence-card-lite.tsx` | `#B0823C` | `bread.jpg` — https://images.unsplash.com/photo-1509440159596-0249088772ff?w=900&q=80 |
| `featured-snacks-intelligence-card.tsx` | `#BC6A33` | `snacks.jpg` — https://images.pexels.com/photos/6167333/pexels-photo-6167333.jpeg?auto=compress&cs=tinysrgb&w=900 |
| `featured-yogurts-intelligence-card.tsx` | `#BC7AA0` | `yogurt.jpg` — https://images.pexels.com/photos/8892364/pexels-photo-8892364.jpeg?auto=compress&cs=tinysrgb&w=900 |
| `featured-hummus-intelligence-card.tsx` | `#BF9540` | `hummus.jpg` — https://images.pexels.com/photos/6145895/pexels-photo-6145895.jpeg?auto=compress&cs=tinysrgb&w=900 |
| `featured-vegetable-spreads-intelligence-card.tsx` | `#7E68A6` | `eggplant.jpg` — https://images.pexels.com/photos/321551/pexels-photo-321551.jpeg?auto=compress&cs=tinysrgb&w=900 |

**IMPORTANT — use exactly these photos (or real Bari product shots of the same subject).**
Do NOT substitute arbitrary stock. Each photo must show the actual product on a light/clean
background: milk (glass/pour), artisan bread loaf, chocolate/snack pieces, yogurt+berries,
a bowl of hummus, whole eggplants. Busy or dark images (salads, landscapes) break the
subtle look — the treatment only stays quiet when the subject is light and uncluttered.

Example (milk card):
```tsx
<ComparisonIntelligenceHero
  // ...existing props...
  theme={{ accent: "#5C7FB0", photo: "/hashvaot/themes/milk.jpg" }}
/>
```

## Step 3 — Images

Prefer **local assets** in `public/hashvaot/themes/` (e.g. `milk.jpg`, `bread.jpg`,
`snacks.jpg`, `yogurt.jpg`, `hummus.jpg`, `eggplant.jpg`), ~900px wide, optimized.
Use real Bari product photography if we have it; otherwise royalty-free food photos
(Pexels/Unsplash, no attribution required) are fine as placeholders.

Because these are decorative `background-image`s (not `next/image`), no `next.config`
remote-domain setup is needed. If you'd rather use `next/image fill`, add the domains to
`images.remotePatterns` and keep `object-cover` + the same mask/opacity/filter via a
wrapper `<div>`.

## Constraints / acceptance
- Do NOT change the green palette, CTA, badge, insight box, stats row, or layout.
- The photo must stay subtle: at rest it's a ghosted corner vignette, never competing with
  the title or insight text. Verify text contrast is unaffected (the veil handles this).
- Keep everything `aria-hidden` and `pointer-events-none` (the photo layers are decorative).
- RTL must be preserved — photo anchors the **left** (far) side; text stays right-aligned.
- Respect `prefers-reduced-motion` as the component already does (no new motion added).
- Verify on mobile widths: at narrow widths the `w-[60%]` photo + veil should still keep
  the title legible; if needed, drop photo opacity slightly under `sm`.

## Optional follow-ups (ask before doing)
- A layout variant where the photo runs as a full-height strip down the side instead of a
  corner vignette.
- Exposing accent/photo on the comparison **page heroes** too (not just the hub cards).

---

## Concrete before / after

### A) `comparison-intelligence-hero.tsx`

**Props type — BEFORE**
```tsx
export type ComparisonIntelligenceHeroProps = {
  badge: string;
  categoryTags: string;
  title: string;
  description: string;
  insightLines: readonly string[];
  stats: readonly ComparisonHeroStat[];
  updatedLabel?: string;
  ctaLabel?: string;
  ctaTargetId?: string;
  asLinkChild?: boolean;
  className?: string;
};
```

**Props type — AFTER** (add `ComparisonHeroTheme` + one prop)
```tsx
export type ComparisonHeroTheme = {
  accent: string; // muted product hue for the tint wash
  photo: string;  // /public path (preferred) or remote URL
};

export type ComparisonIntelligenceHeroProps = {
  badge: string;
  categoryTags: string;
  title: string;
  description: string;
  insightLines: readonly string[];
  stats: readonly ComparisonHeroStat[];
  updatedLabel?: string;
  ctaLabel?: string;
  ctaTargetId?: string;
  asLinkChild?: boolean;
  className?: string;
  theme?: ComparisonHeroTheme; // <-- added
};
```
Also add `theme,` to the destructured params in the function signature.

**Render — BEFORE** (top of the root card)
```tsx
    <div
      className={cn(
        "relative overflow-hidden rounded-[1.35rem]",
        "border border-[#1A1D24]/[0.08] shadow-[0_32px_100px_-60px_rgba(17,19,24,0.35)] ring-1 ring-[#FFFFFF]/80",
        className
      )}
    >
      <div
        className="pointer-events-none absolute inset-0 bg-[linear-gradient(135deg,#FDFDF8_0%,#F4F6F3_42%,#EEF5F1_100%)]"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom_left,rgba(31,143,106,0.045),transparent_48%,transparent_72%,rgba(31,143,106,0.028))]"
        aria-hidden
      />
      <ComparisonIntelligenceBackdrop />
      <ComparisonAnalysisParticles reduceMotion={reduceMotion} />

      <div className="relative z-[1] px-6 pb-10 pt-8 sm:px-8 lg:px-11 lg:py-11">
```

**Render — AFTER** (insert the three layers between the second gradient and the backdrop)
```tsx
    <div
      className={cn(
        "relative overflow-hidden rounded-[1.35rem]",
        "border border-[#1A1D24]/[0.08] shadow-[0_32px_100px_-60px_rgba(17,19,24,0.35)] ring-1 ring-[#FFFFFF]/80",
        className
      )}
    >
      <div
        className="pointer-events-none absolute inset-0 bg-[linear-gradient(135deg,#FDFDF8_0%,#F4F6F3_42%,#EEF5F1_100%)]"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom_left,rgba(31,143,106,0.045),transparent_48%,transparent_72%,rgba(31,143,106,0.028))]"
        aria-hidden
      />

      {/* ── per-product theme: photo + veil + tint (decorative) ── */}
      {theme ? (
        <>
          <div
            aria-hidden
            className="pointer-events-none absolute inset-y-0 left-0 z-0 h-full w-[60%]"
            style={{
              backgroundImage: `url(${theme.photo})`,
              backgroundSize: "cover",
              backgroundPosition: "center",
              opacity: 0.62,
              filter: "grayscale(0.08) contrast(1.02) saturate(1.02)",
              WebkitMaskImage:
                "radial-gradient(135% 145% at 0% 100%, #000 30%, rgba(0,0,0,0.5) 56%, transparent 80%)",
              maskImage:
                "radial-gradient(135% 145% at 0% 100%, #000 30%, rgba(0,0,0,0.5) 56%, transparent 80%)",
            }}
          />
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 z-0"
            style={{
              background:
                "linear-gradient(105deg, transparent 0%, rgba(253,253,248,0.10) 38%, rgba(253,253,248,0.62) 64%, rgba(253,253,248,0.86) 100%)",
            }}
          />
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 z-0 mix-blend-multiply"
            style={{
              background: `radial-gradient(60% 80% at 14% 96%, color-mix(in oklab, ${theme.accent} 13%, transparent), transparent 70%)`,
            }}
          />
        </>
      ) : null}

      <ComparisonIntelligenceBackdrop />
      <ComparisonAnalysisParticles reduceMotion={reduceMotion} />

      <div className="relative z-[1] px-6 pb-10 pt-8 sm:px-8 lg:px-11 lg:py-11">
```
Nothing else in the component changes — the content wrapper is already `z-[1]`, so it stays above the new `z-0` layers.

### B) `featured-milk-intelligence-card.tsx`

**BEFORE**
```tsx
      <ComparisonIntelligenceHero
        badge="דוח ראשון"
        categoryTags="חלב · תחליפי חלב · משקאות חלבון"
        title={milkComparisonPage.comparison_title}
        description={description}
        insightLines={INSIGHT_LINES}
        stats={[
          { value: metadata.productCount, label: "מוצרים נותחו" },
          { value: metadata.paramCount, label: "פרמטרים הושוו" },
          { value: metadata.categoryCount, label: "קטגוריות" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(milkComparisonPage.generated_at)}
        asLinkChild
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
```

**AFTER** (one added prop)
```tsx
      <ComparisonIntelligenceHero
        badge="דוח ראשון"
        categoryTags="חלב · תחליפי חלב · משקאות חלבון"
        title={milkComparisonPage.comparison_title}
        description={description}
        insightLines={INSIGHT_LINES}
        stats={[
          { value: metadata.productCount, label: "מוצרים נותחו" },
          { value: metadata.paramCount, label: "פרמטרים הושוו" },
          { value: metadata.categoryCount, label: "קטגוריות" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(milkComparisonPage.generated_at)}
        asLinkChild
        theme={{ accent: "#5C7FB0", photo: "/hashvaot/themes/milk.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
```

Repeat the single-line `theme={{ accent, photo }}` addition for the other five featured
cards using the mapping table above. That's the entire change.
