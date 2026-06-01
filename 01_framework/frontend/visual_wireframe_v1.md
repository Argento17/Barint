# Bari Operating Model — Visual Design System v1
### Wireframes, Color System, Layouts, Command-Center Architecture

**Issued:** 2026-05-29  
**Status:** Active  
**Applies to:** operating_model_v2.md / org_chart_v2.md / any presentation rendition

---

## 1. Color System

### Role Color Palette

| Role | Primary | Secondary | Text On Primary | Usage |
|---|---|---|---|---|
| Tom | `#1A1A2E` | `#16213E` | `#FFFFFF` | Command nodes, authority borders |
| ChatGPT | `#10A37F` | `#0D8A6C` | `#FFFFFF` | Strategy cards, flow arrows |
| Claude CE | `#CC785C` | `#B56344` | `#FFFFFF` | Intelligence nodes, content outputs |
| Cursor IDE | `#646CFF` | `#4B52E0` | `#FFFFFF` | Engineering blocks, build artifacts |
| OpenAI Codex | `#2D3561` | `#1F2547` | `#FFFFFF` | Audit lane, verification stamps |

### System Colors

| Token | Value | Usage |
|---|---|---|
| Background | `#F8F9FA` | Page/slide background |
| Surface | `#FFFFFF` | Cards, panels |
| Divider | `#E5E7EB` | Separators, borders |
| Text Primary | `#111827` | Headings, key labels |
| Text Secondary | `#6B7280` | Descriptions, metadata |
| Success | `#059669` | QA pass, verified |
| Warning | `#D97706` | Conditional pass, review |
| Danger | `#DC2626` | QA fail, escalation, blocked |
| Audit Line | `#94A3B8` | Dashed Codex access lines |

---

## 2. Card Layouts

### 2.1 Role Card — Standard (portrait orientation)

```
┌─────────────────────────────────────────────────────┐
│  [ROLE COLOR BACKGROUND]              [BADGE TOP-R] │
│                                                     │
│  [SYMBOL 32px]  [ROLE NAME 20px bold]               │
│                 [TITLE 13px regular]                │
│                                                     │
├─────────────────────────────────────────────────────┤
│  OWNS                                               │
│  · [Responsibility 1]                               │
│  · [Responsibility 2]                               │
│  · [Responsibility 3]                               │
│                                                     │
│  REPORTS TO    [Role name]                          │
│  FEEDS INTO    [Role name]                          │
├─────────────────────────────────────────────────────┤
│  [ARTIFACT TAG 1]  [ARTIFACT TAG 2]  [ARTIFACT 3]  │
└─────────────────────────────────────────────────────┘

Dimensions: 320px × 240px (portrait) or 480px × 160px (landscape)
Corner radius: 12px
Shadow: 0 4px 16px rgba(0,0,0,0.10)
```

### 2.2 Artifact Tag Chip

```
┌───────────────────────┐
│  ▪ BSIP2 JSON         │    Background: role color at 15% opacity
└───────────────────────┘    Border: role color at 40% opacity
                             Font: 11px monospace, role color
                             Padding: 4px 8px, radius: 4px
```

### 2.3 Decision Badge

```
┌─────────────────────────┐
│  ✓ APPROVED             │   Green: #059669 bg, white text
│  ⟳ PENDING REVIEW       │   Amber: #D97706 bg, white text
│  ✗ BLOCKED / QA FAIL    │   Red:   #DC2626 bg, white text
│  ↑ ESCALATED TO TOM     │   Navy:  #1A1A2E bg, white text
└─────────────────────────┘   All: 11px caps, 4px radius, 4px 10px padding
```

---

## 3. Page Architecture

### 3.1 Operating Model Slide (16:9 Presentation)

```
┌──────────────────────────────────────────────────────────────────────┐
│  HEADER BAND [72px]                                                  │
│  BARI OPERATING MODEL v2              [Navy #1A1A2E bg, white text]  │
│  "Five-role hybrid intelligence organization"                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  LEFT COLUMN (320px)        │   CENTER (680px)   │  RIGHT (320px)  │
│                             │                    │                  │
│  [Tom Card]                 │   [Hierarchy       │  [Codex Card]   │
│  Authority Layer            │    Swimlane]        │  Verification   │
│                             │                    │  Layer          │
│  [ChatGPT Card]             │                    │                 │
│  Strategy Layer             │                    │                 │
│                             │                    │                 │
│  [Claude CE Card]           │                    │                 │
│  Intelligence Layer         │                    │                 │
│                             │                    │                 │
│  [Cursor Card]              │                    │                 │
│  Execution Layer            │                    │                 │
│                             │                    │                 │
├──────────────────────────────────────────────────────────────────────┤
│  FOOTER BAND [40px]  Layer legend  ·  Date  ·  Bari Intelligence    │
└──────────────────────────────────────────────────────────────────────┘

Grid: 24px gutter, 16px outer padding
```

### 3.2 RACI Slide

```
┌──────────────────────────────────────────────────────────────────────┐
│  RESPONSIBILITY MATRIX (RACI)                          [Header band] │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [COLUMN HEADERS — role colored chips]                               │
│  Decision Area    │  Tom  │  GPT  │  CE   │  Cursor │  Codex       │
│  ─────────────────┼───────┼───────┼───────┼─────────┼──────────     │
│  Category launch  │   A   │   C   │   C   │    I    │    I         │
│  [row color-bands alternate: white / #F8F9FA]                        │
│                                                                      │
│  LEGEND BAND (bottom):  R=Responsible  A=Accountable                │
│                         C=Consulted    I=Informed                    │
├──────────────────────────────────────────────────────────────────────┤
│  R cells: role color fill 20% · A cells: role color fill 80% bold   │
│  C cells: gray border only   · I cells: plain text                  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 4. Swimlane Layout

### 4.1 Execution Flow Swimlane (horizontal, left→right)

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  SWIMLANE DIAGRAM — STANDARD CATEGORY EXECUTION FLOW                                 │
├────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                      │
│  TOM              [Category brief issued] ──────────────────────────► [APPROVE]     │
│  #1A1A2E          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                                      │
│  CHATGPT          [Receive brief] ── [Produce XP spec] ─────────────► [Strategy OK] │
│  #10A37F          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                                      │
│  CLAUDE CE  [BSIP0]─[BSIP1]─[BSIP2]─[Editorial]─[Frontend JSON] ──► [JSON READY]  │
│  #CC785C          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                                      │
│  CURSOR     [Receive JSON + spec] ────── [Build components] ────────► [DEPLOYED]    │
│  #646CFF          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                                      │
│  CODEX            [QA: JSON] ───────────────── [QA: Frontend] ──────► [SIGNED OFF]  │
│  #2D3561          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                                      │
│  ────────────────────────────────────────────────────────────────────────────────    │
│  PHASE:    [BRIEF]─────[SPEC]────[PIPELINE]────[BUILD]────[QA]────[LIVE]             │
└──────────────────────────────────────────────────────────────────────────────────────┘

Lane height: 80px each · Phase markers: 60px wide · Arrows: role color
```

### 4.2 Escalation Swimlane (vertical, top→bottom)

```
┌──────────────────────────────────────────────────────┐
│  ESCALATION LADDER                                   │
│                                                      │
│  Tier 0   Any role         [Issue identified]        │
│     │                           │                   │
│     ▼     ───────────────────   │                   │
│  Tier 1   Peer pair        [24h resolution window]  │
│     │     (CE + Cursor)         │                   │
│     │     (Codex + CE)          │                   │
│     ▼    if unresolved ─────────┘                   │
│  Tier 2   ChatGPT          [48h arbitation]         │
│     │     (strategy scope)      │                   │
│     ▼    if unresolved ─────────┘                   │
│  Tier 3   Tom              [72h final decision]      │
│           (all disputes)                             │
│                                                      │
│  Emergency:  Codex ──────────────► Tom (direct)     │
│  (data integrity failures only)                      │
└──────────────────────────────────────────────────────┘
```

---

## 5. Command-Center Concept

The command-center view is the single-screen control panel showing live status across all five roles. Intended as an internal operations dashboard (not consumer-facing).

### 5.1 Layout

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│  BARI COMMAND CENTER                                            [Date / Session] │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                                                  │
│  ┌───────────────────────────────────────────────────────────────────────────┐   │
│  │  ACTIVE CATEGORY: מעדנים                STATUS: ✓ LIVE                   │   │
│  │  Phase: Consumer Interaction Validation   Products: 90 / Verified: 88    │   │
│  └───────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                 │
│  │  ◈ TOM          │  │  ◉ CHATGPT      │  │  ⊟ CODEX        │                 │
│  │  #1A1A2E        │  │  #10A37F        │  │  #2D3561        │                 │
│  │                 │  │                 │  │                 │                 │
│  │  Status: ACTIVE │  │  Status: IDLE   │  │  Status: ACTIVE │                 │
│  │                 │  │                 │  │                 │                 │
│  │  Last action:   │  │  Last:          │  │  QA queue:      │                 │
│  │  Approved v2    │  │  Category brief │  │  0 pending      │                 │
│  │  publication    │  │  (לחם next)     │  │                 │                 │
│  │                 │  │                 │  │  Last report:   │                 │
│  │  Next:          │  │  Next:          │  │  PASS (v2 JSON) │                 │
│  │  Authorize      │  │  חלב strategy   │  │                 │                 │
│  │  חלב pipeline   │  │  memo           │  │                 │                 │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                 │
│                                                                                  │
│  ┌───────────────────────────────┐  ┌───────────────────────────────────────┐   │
│  │  ⬡ CLAUDE CODE (CE)           │  │  ▣ CURSOR IDE                         │   │
│  │  #CC785C                      │  │  #646CFF                               │   │
│  │                               │  │                                       │   │
│  │  Status: PIPELINE COMPLETE    │  │  Status: BUILD COMPLETE               │   │
│  │                               │  │                                       │   │
│  │  Active category: מעדנים ✓    │  │  Active: מעדנים page                  │   │
│  │  Next: חלב BSIP0              │  │  Next: חלב page                       │   │
│  │                               │  │                                       │   │
│  │  Outputs ready:               │  │  Components live:                     │   │
│  │  · maadanim_frontend_v2.json  │  │  · ProductRow ✓                       │   │
│  │  · 90 products scored         │  │  · ScoreChip ✓                        │   │
│  │  · 0 QA flags                 │  │  · ExpansionSection ✓                 │   │
│  │                               │  │  · FilterBar ✓                        │   │
│  │  Framework:                   │  │                                       │   │
│  │  · DISTORTION-001 logged      │  │  QA open issues: 0                    │   │
│  │  · Governance_v1 updated      │  │                                       │   │
│  └───────────────────────────────┘  └───────────────────────────────────────┘   │
│                                                                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  PIPELINE STATUS:  מעדנים [████████████] LIVE  │  לחם [████████░░] BUILD READY  │
│  FRAMEWORK STATUS: governance_v1 ✓  │  editorial_v3 ✓  │  DISTORTION-001 logged  │
│  NEXT CATEGORY:  חלב   │  Target: BSIP0 scrape → scoring → frontend → live      │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Status Chip Conventions (command center)

| State | Color | Label |
|---|---|---|
| LIVE | `#059669` | ✓ LIVE |
| BUILD READY | `#10A37F` | ⟳ BUILD READY |
| PIPELINE ACTIVE | `#CC785C` | ⬡ PIPELINE RUNNING |
| QA IN PROGRESS | `#2D3561` | ⊟ QA REVIEW |
| BLOCKED | `#DC2626` | ✗ BLOCKED |
| IDLE | `#6B7280` | ○ IDLE |
| ESCALATED | `#1A1A2E` | ↑ ESCALATED |

---

## 6. Typography

| Element | Font | Size | Weight | Case |
|---|---|---|---|---|
| Org chart name | Inter / Helvetica Neue | 20px | 700 Bold | Title |
| Role title | Inter | 13px | 400 Regular | Title |
| Badge label | Inter | 10px | 600 Semi-bold | ALL CAPS |
| Card section label | Inter | 11px | 600 Semi-bold | ALL CAPS |
| Card body | Inter | 13px | 400 Regular | Sentence |
| Symbol | System | 24–32px | — | — |
| Swimlane phase | Inter Mono | 11px | 500 | ALL CAPS |
| Command center metric | Inter Mono | 14px | 600 | Mixed |

---

## 7. Diagram Conventions

| Element | Style |
|---|---|
| Reporting line (solid) | 2px, role color, straight connector |
| Audit line (Codex) | 1px dashed, `#94A3B8` slate, reaches all nodes |
| Data flow arrow | 1.5px, source role color, arrowhead at target |
| Escalation arrow | 2px, `#DC2626` red, solid, upward |
| Phase boundary | 1px, `#E5E7EB`, vertical divider |
| Card border | 1px solid, role color at 30% opacity |
| Section divider (inside card) | 0.5px, `#E5E7EB` |

---

## 8. Responsive / Print Variants

| Format | Layout |
|---|---|
| Presentation (16:9) | Full swimlane or card grid, 1280×720 |
| A4 Print | Vertical hierarchy, 2-column card grid, condensed command center |
| A3 Print | Full swimlane, all roles visible at once |
| Web embed | Collapsible accordion per role, command center as live dashboard |
| Mobile | Single-column card stack, swipe between roles |

---

## 9. What Not to Do

- Do not use gradient backgrounds on role cards — flat color only
- Do not mix role colors within a single card
- Do not use more than 5 levels in the escalation ladder
- Do not display Codex as a subordinate — it is a lateral/independent audit lane
- Do not render Tom's card with the same visual weight as AI-role cards — authority layer should be visually distinct (larger, darker, centered)
- Do not add decorative icons that are not role symbols
- Do not use rounded symbol shapes that imply "friendly" (circles) — Bari is analytical, not consumer-friendly at the ops layer

---

*Visual Design System v1 — Bari Operating Model / 2026-05-29*
