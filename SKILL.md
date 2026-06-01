---
name: bari-design
description: Use this skill to generate well-branded interfaces and assets for Bari, the Israeli food-intelligence platform that compares packaged foods. Contains essential design guidelines, colors, type, fonts, brand assets, and a high-fidelity UI kit of the comparison experience for prototyping. Hebrew-first, RTL, data-first, evidence-based.
user-invocable: true
---

Read the `README.md` file within this skill first — it holds the full brand context, content fundamentals, visual foundations, and iconography. Then explore the other files:

- `colors_and_type.css` — design foundations: color + grade palette, type scale, radii, shadows, motion, layout tokens. Link or copy this into any artifact.
- `assets/` — current Bari logo (`logo1.png`) + newsletter marks. The signal mark is reconstructed as inline SVG in the preview cards and UI kit.
- `preview/` — design-system cards (colors, type, spacing, components, brand).
- `ui_kits/web/` — high-fidelity, interactive recreation of the **comparison page** (the core product), reflecting the accepted **v-next-2** direction. `index.html` is self-contained React with real data.
- `handoff/comparison-v2-spec.md` — engineering-facing v2 spec (invariants, data contract, layout rules).
- `Bari Comparison UX Analysis.html` / `Bari TASK-091 DEC-002 Decision.html` — the analysis and ship/hold decision behind the current direction.

If creating visual artifacts (mocks, throwaway prototypes, slides), copy assets out and produce static/self-contained HTML for the user to view. If working on production code, copy assets and apply the rules here to design natively in the brand.

**Always honor Bari's non-negotiables:** Hebrew-first RTL; trust before marketing (no health claims, no marketing adjectives, no gamification); data-first and category-relative scoring; one rationed green accent; calm editorial paper canvas; minimal visual noise; line icons only, no emoji. In the comparison product specifically: every product stays individually visible, and corpus-owned ordering is never re-sorted by the client.

If the user invokes this skill without other guidance, ask what they want to build, ask a few focused questions, then act as an expert Bari designer who outputs HTML artifacts or production code, depending on the need.
