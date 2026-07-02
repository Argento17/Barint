# Bari Character Bible v1 — Mascot Cast, Roles & Animations

> **Status:** canonical brand reference (owner-provided, 2026-07-01).
> **Owners of use:** Design Agent (visual/placement/motion conformance) + Content Agent
> (voice per character). Invoke either or both to produce mascot content — individually or
> as a team scene. Copy still passes the **two-gate sign-off** (Content + Adversarial QA);
> the mascots do not exempt any consumer-facing string.
> **Source:** owner "Bari Character Bible — Our mascots. Our roles. Our animations." board.

"A living cast that brings Bari's food intelligence to life. Use them consistently to build
trust, delight and a memorable experience across every touchpoint."

---

## The Cast

| Char | Icon | Title | Role | Personality | Color |
|------|------|-------|------|-------------|-------|
| **LUMO** | The Leaf 🔍 | The Investigator | The **face of Bari**. Curious, observant, always on a mission to find the truth about products. | Curious, calm, smart, kind, observant | Fresh Bari Green (`#1F8F6A`) |
| **OLI** | The Olive | The Healthy Guide | Represents Mediterranean nutrition & healthy choices. Promotes quality ingredients and balanced living. | Warm, positive, encouraging, trustworthy | Olive Green |
| **NORI** | The Ingredient Tile ✅ | The Expert | Expert in ingredients. Reads labels, explains additives, educates in a simple way. | Smart, precise, evidence-based, helpful | Soft Mint Green |
| **ATOM** | The Molecule ⚛ | The AI Engine | The **brain behind Bari**. Compares products, analyzes data, finds the best options. | Intelligent, neutral, precise, powerful | Tech Purple |
| **GRAIN** | The Oat | The Whole-Food Ambassador | Whole-food ambassador (raw / unprocessed foods). | (per animation set below) | Oat/wheat tone |

Legend the owner attached to the cast: 🔍 Investigator of products · 💚 Guide to healthy
choices · 🟩 Expert in ingredients · ⚛ AI comparison engine · 🌾 Whole-food ambassador.

---

## Animation Library (30 per character)

**LUMO — The Investigator:** Idle floating · Blink · Look left · Look right · Look up · Smile ·
Wave · Walk in · Walk out · Fly in · Fly out · Inspect (magnifying glass) · Take notes ·
Point left · Point right · Point upward · Point to ingredient · Celebrate quietly · Tiny jump ·
Thinking · Scratch chin · Look surprised · Shake head gently · Nod yes · Peek from behind
product · Peek from behind card · Carry score badge · Carry ingredient list · Read label ·
Sleep (404).

**OLI — The Healthy Guide:** Roll onto screen · Bounce · Smile · Tiny thumbs up · Carry olive
oil bottle · Carry tomato · Hold "95" · Point toward winner · Meditate · Relax · Stretch · Float ·
Peek · Wave · Celebrate · Laugh · Look concerned · Shake head · High five Leaf · Carry grocery
basket · Push shopping cart · Read ingredient label · Walk · Sit · Drink coffee · Tiny dance ·
Spin · Rest · Exit.

**NORI — The Ingredient Expert:** Appear · Disappear · Stack · Unstack · Flip · Rotate · Scan ·
Highlight ingredient · Underline ingredient · Explain · Raise eyebrow · Blink · Think · Glow ·
Hold E-number · Hold fiber icon · Hold protein icon · Show warning · Show checkmark · Slide ·
Bounce · Pop · Celebrate · Carry paper · Read paper · Point · Fold · Wave · Peek · Sleep.

**ATOM — The AI Engine:** Orbit · Pulse · Glow · Connect nodes · Disconnect · Compare ·
Calculate · Radar grows · Radar shrinks · Rotate · Float · Expand · Contract · Network grows ·
Network disappears · Score appears · Score counts up · Evidence nodes connect · Hover · Think ·
Split · Merge · Spin slowly · Tiny sparkle · Idle · Connect products · Compare products ·
Data upload · Download · Loop.

**GRAIN — The Oat Ambassador:** Hop · Roll · Stretch · Wave · Smile · Hold oats · Hold cereal ·
Carry spoon · Look happy · Think · Blink · Point · Read label · Run · Jump · Celebrate · Sit ·
Float · Look left · Look right · Sleep · Wake · Peek · Carry bowl · Carry yogurt · High five Leaf ·
Carry score · Carry fiber badge · Exit · Loop.

---

## Team Interactions — Example Scenes

1. **Investigation** — LUMO inspects a product while OLI supports and NORI reads the label.
2. **Analysis** — NORI extracts ingredients and ATOM analyzes the data.
3. **Comparison** — ATOM connects multiple products and compares them instantly.
4. **Verdict** — LUMO delivers the final score (e.g. "87 Great Choice") and explains why.
5. **Healthy Choice** — OLI confirms it's a healthy choice and celebrates.
6. **Learning** — NORI teaches the user about ingredients and nutrition.
7. **Teamwork** — all characters work together to make Bari intelligent.
8. **Celebration** — the team celebrates a great product for the user.

---

## How to invoke (for the orchestrator / agents)

- **Design Agent** owns *which* character, *where*, at *what* size, and *which* animation state —
  grounded in the frozen token/geometry system. Character color must map to the design token
  (LUMO/`--bari-green`; the rest to their named tone). Mascots are **decorative** in UI
  (`aria-hidden`, `pointer-events:none`) unless a scene is the content itself.
- **Content Agent** owns the *voice* each character speaks in — match the personality column.
  LUMO = curious/observant framing; OLI = warm encouragement; NORI = precise label-literate
  explanation; ATOM = neutral engine narration; GRAIN = whole-food framing.
- Pair them by scene (see the 8 above) when producing multi-character content.
- Pick the character by **job-to-be-done**, not decoration: investigation → LUMO, healthy-choice
  nudge → OLI, ingredient/additive explainer → NORI, scoring/compare engine → ATOM, raw/whole
  food → GRAIN.

## Live usage so far (2026-07-01)
- **LUMO (leaf)** — `/hashvaot` comparisons index header (investigator hooks the section).
- **OLI (olive)** — homepage newsletter signup action row (healthy guide hosts the invite).
- Optimized assets: `bari-web/public/mascots/mascot-leaf.png`, `…/mascot-olive.png`
  (backgrounds keyed to transparent, cropped to figure).
