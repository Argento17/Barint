# Implement: Animated "Bari sprout" hero background

Add the animated logo background to the homepage hero. The Bari sprout assembles
from a burst on load, breathes at rest, and every few seconds bursts apart into a
connected data-constellation and reassembles. It replaces the current
`home-hero-signal-network` SVG decoration.

Reference prototype (works in a browser): `Bari Hero.html` + `plant.js` + the 5 sliced
PNGs in `assets/plant/`. These files are provided alongside this prompt — use them as
the source of truth for behaviour and timing.

---

## Step 1 — Generate the sliced logo assets

The animation drives 5 **pixel-sliced** pieces of the real icon (NOT a redrawn SVG),
each kept full-frame so they stack back into the exact logo. Generate them from the
existing `public/Bari_icon_concept3_transparent_highres.png`.

Add `pngjs` if not present (`npm i -D pngjs`) and run this once (e.g. `scripts/slice-logo.mjs`):

```js
import fs from "node:fs";
import { PNG } from "pngjs";

const src = PNG.sync.read(fs.readFileSync("public/Bari_icon_concept3_transparent_highres.png"));
const { width: W, height: H, data } = src;
const cx = W / 2, dotMaxY = H * 0.38;           // dot lives in the top ~38%
const ids = ["dot", "greenL", "greenR", "navyL", "navyR"];
const out = Object.fromEntries(ids.map((id) => {
  const p = new PNG({ width: W, height: H }); p.data.fill(0); return [id, p];
}));

for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
  const i = (W * y + x) << 2, a = data[i + 3];
  if (a < 24) continue;
  const r = data[i], g = data[i + 1], b = data[i + 2];
  const greenScore = g - Math.max(r, b);
  let p;
  if (greenScore > 8 && g > 70) p = x < cx ? "greenL" : "greenR";   // green leaves
  else p = y < dotMaxY ? "dot" : (x < cx ? "navyL" : "navyR");      // dot / navy base
  const o = out[p].data; o[i] = r; o[i + 1] = g; o[i + 2] = b; o[i + 3] = a;
}

fs.mkdirSync("public/plant", { recursive: true });
for (const id of ids) fs.writeFileSync(`public/plant/${id}.png`, PNG.sync.write(out[id]));
console.log("wrote public/plant/{dot,greenL,greenR,navyL,navyR}.png");
```

Result: `public/plant/dot.png`, `greenL.png`, `greenR.png`, `navyL.png`, `navyR.png`.
(They're mostly transparent, so each is small.) Alternatively, just copy the 5 PNGs
from the provided `assets/plant/` folder into `public/plant/`.

---

## Step 2 — Add the engine

Copy the provided `plant.js` into `src/components/home/plant-hero-engine.js` and change
the **last line** from:

```js
window.PlantHero = PlantHero;
```
to:
```js
export default PlantHero;
```

That's the only change — it's a framework-agnostic class. Key API:
- `new PlantHero({ stage, assetBase, size, opacity, mode, shatter, period, constellation, particles, parallax })`
- `.setConfig(partial)` — live updates
- `.replay()` — replays the assemble animation
- `.destroy()` — cancels RAF + removes listeners (call on unmount)
- Honors `prefers-reduced-motion` automatically (renders assembled, no motion/particles).

---

## Step 3 — CSS

Add `src/components/home/plant-hero.module.css` (values copied verbatim from the prototype):

```css
.stage { position: absolute; inset: 0; margin: auto; width: var(--plant-size, 520px);
  height: calc(var(--plant-size, 520px) * 1.031); z-index: 1; will-change: transform; pointer-events: none; }
.stage[data-mode="mascot"] { inset: 5% 0 auto 0; }

/* the engine injects these elements into .stage / its parent */
.stage :global(.plant) { position: absolute; inset: 0; transition: opacity .5s; }
.stage :global(.piece) { position: absolute; inset: 0; transform-origin: 50% 50%; will-change: transform, opacity; }
.stage :global(.piece img) { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; }
.stage :global(.plant-constellation) { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; transition: opacity .4s; }
.stage :global(.plant-net) { opacity: 0; }
.stage :global(.plant-edge) { stroke: rgba(7,147,111,.55); stroke-width: .3; vector-effect: non-scaling-stroke; }
.stage :global(.plant-node) { fill: rgba(15,29,41,.55); }

:global(.plant-particles) { position: absolute; inset: 0; z-index: 2; pointer-events: none; will-change: transform; }
:global(.ppart) { position: absolute; animation-name: pfloat, pfade; animation-timing-function: linear, ease-in-out;
  animation-iteration-count: infinite; will-change: transform, opacity; }
:global(.ppart-seed) { border-radius: 50%; background: #07936F; --pop: .20; }
:global(.ppart-leaf) { background: #0F1D29; border-radius: 0 72% 0 72%; --pop: .09; }
@keyframes pfloat { from { transform: translateY(0) translateX(0) rotate(0); }
  to { transform: translateY(-130px) translateX(var(--drift, 0)) rotate(40deg); } }
@keyframes pfade { 0%,100% { opacity: 0; } 18%,82% { opacity: var(--pop, .3); } }

/* legibility scrim so the centered headline stays crisp over the watermark */
.scrim { position: absolute; inset: 0; z-index: 3; pointer-events: none;
  background: radial-gradient(62% 56% at 50% 47%,
    rgba(247,247,242,.88) 0%, rgba(247,247,242,.55) 44%, rgba(247,247,242,0) 74%); }
```

> Note: the engine appends a `.plant-particles` layer to the stage's **parent**, so the
> particle styles are global (`:global`). Keep them global as shown.

---

## Step 4 — React wrapper

`src/components/home/plant-hero-background.tsx`:

```tsx
"use client";
import { useEffect, useRef } from "react";
import PlantHero from "./plant-hero-engine";
import styles from "./plant-hero.module.css";

export function PlantHeroBackground() {
  const stageRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!stageRef.current) return;
    const inst = new PlantHero({
      stage: stageRef.current,
      assetBase: "/plant/",
      size: 540, opacity: 0.22, mode: "watermark",
      shatter: true, period: 7, constellation: true, particles: 0.6, parallax: true,
    });
    return () => inst.destroy();
  }, []);
  return (
    <>
      <div ref={stageRef} className={styles.stage} aria-hidden />
      <div className={styles.scrim} aria-hidden />
    </>
  );
}
```

---

## Step 5 — Wire into the hero (`src/components/home/home-hero.tsx`)

- **Remove** the existing `home-hero-signal-network` `<div>…<svg>…</svg></div>` block
  (the decorative constellation) — the sprout now provides that motif.
- Inside the hero `<section>`, before `<HomeContainer>`, render the background layer:

```tsx
<div className="pointer-events-none absolute inset-0 -z-10" aria-hidden>
  <PlantHeroBackground />
</div>
```

Keep the two soft `bg-[#2FAE82]` glow blobs if you like them. The hero text/buttons
already sit above (they're inside `HomeContainer`); the scrim keeps the headline
readable over the watermark.

---

## Config & behaviour notes
- **mode**: `"watermark"` (default — big, faint, behind text, requested look) or `"mascot"`
  (full-color, anchored near the top). `opacity` only applies to watermark mode.
- **period**: seconds between bursts. **constellation**: the connecting lines during a burst.
- **particles**: 0–1 ambient density. **parallax**: pointer/scroll drift.
- Defaults above match the approved prototype. Tune `opacity` up if you want the sprout
  more present.

## A11y / perf
- Whole background is `aria-hidden` and `pointer-events: none`.
- `prefers-reduced-motion: reduce` → engine renders the assembled sprout statically,
  no particles, no parallax. Already handled.
- One `requestAnimationFrame` loop; `.destroy()` on unmount cancels it. Optional: wrap in
  an `IntersectionObserver` to pause when the hero scrolls out of view.

## Acceptance
- Sprout assembles on load (base leaves → green leaves → seed-dot), breathes, and every
  ~7s bursts into a constellation and reforms.
- Headline + badge + buttons + trust row stay crisp and readable.
- No layout shift; respects reduced-motion; no console errors.
