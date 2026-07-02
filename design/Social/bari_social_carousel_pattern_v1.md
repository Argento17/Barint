# Bari Social Carousel — Design Pattern v1

> Extracted from the owner-provided reference `design/Social/38ccf47c-...png` (2026-07-02).
> This is the **quality bar** for Bari social/marketing collateral produced in Canva.
> Copy in any panel is a **draft until the two-gate sign-off** (Content Agent + Adversarial QA).
> Mascots are canonical per `01_framework/brand/bari_character_bible_v1.md`.

## Hard rule for producing these in Canva
Reproduce the **layout** with AI; **never the characters or logo**. LUMO / OLI / NORI / ATOM
and the wordmark come in ONLY as the real uploaded image assets. Text-to-image
(`generate-design`) invents generic mascots — do not ship AI-invented characters.

## Format
- Instagram carousel, 6 panels, 1:1 (1080×1080 each).
- Uniform warm-cream background across all panels.

## Tokens
- Background (canvas): warm cream `#F7F7F2`
- Headline text: near-black navy (`~#12211C` / logo navy)
- Body/secondary text: slate `#4E5663`
- Accent: Bari green `#1F8F6A` (logo sprout, thin rules, line-icons, gauge arc, pills)
- Type: clean geometric Hebrew sans (Heebo / Assistant family), **RTL, right-aligned**

## Reusable components
- **Logo lockup** — `Bari_logo_concept3_transparent_highres.png` (wordmark + green/navy sprout) + "Food Intelligence" tagline.
- **Panel number badge** — dark-green filled circle, white numeral, top corner.
- **Score gauge** — circular green arc, big number over `/100`, caption `ציון בארי`.
- **Line-icon-in-circle** — single-weight dark-green icons (magnifier, flask, shield, target, leaf, scales, person, heart) in a pale-green disc.
- **Green callout box** — pale-green rounded rectangle for a supportive line.
- **URL pill** — dark-green rounded pill, centered bottom: `https://bari.digital`.
- **Phone mockup** — device frame showing the app screen (logo, product image, gauge, `ציון בארי`).

## Mascots (canonical assets)
- **LUMO** `mascots/mascot-leaf.png` — investigator (leaf + magnifier). Face of Bari.
- **OLI** `mascots/mascot-olive.png` — healthy guide (olive).
- **NORI** `mascots/mascot-nori-desk-v2.png` — ingredient expert (tile).
- **ATOM** `blog/food-dyes/atom-food-dyes.png` — AI engine (molecule).
Pick by job-to-be-done, not decoration (Character Bible §"How to invoke").

## Panel roles (reference carousel)
1. **Cover** — logo lockup + tagline; big headline; LUMO + OLI waving; URL pill.
2. **"We do the hard work"** — 3 icon rows (scan / analyze ingredients+nutrition / evidence-only); LUMO with grocery basket + magnifier.
3. **"We translate complex → clear"** — LUMO + OLI with a tablet showing the 72 gauge; supportive line in green callout box.
4. **"How it looks"** — phone mockup (product + 72/100 gauge + `ציון בארי`); 4 icon rows (fit / ingredient quality / additives / nutrition value).
5. **"We don't tell you what to eat — we give you the information"** — 4 line-icons in a row (more transparency / fewer marketing traps / control in your hands / better choices for the family); mascots high-fiving.
6. **Closing** — big `ברי.` + "Food Intelligence" + tagline; mascots in hero capes; URL pill.

## Production path in Canva
1. Upload assets once (logo done; mascots pending — from local files until the `feature/homepage-mascots` branch deploys).
2. Build ONE master 6-panel design placing real assets per above.
3. Save as a Brand Template; future carousels swap only copy (two-gate) + product image + gauge number.
