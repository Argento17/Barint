# BSIP2 Reporting Dashboard

Internal Streamlit dashboard for reviewing BSIP2 scoring runs. Replaces scattered PNG/Markdown reports with an interactive, filterable interface.

## Setup

```bash
# From the repo root, activate the project venv
C:\Bari\.venv\Scripts\activate

# Install dependencies (already installed in .venv)
pip install -r requirements.txt
```

## Run

```bash
cd C:\Bari\03_operations\bsip2\reporting_dashboard
streamlit run app.py
```

The dashboard auto-discovers all runs under `C:\Bari\02_products\*/bsip2_outputs\`.

---

## Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  SIDEBAR                    │  MAIN AREA                        │
│  ─────────────────────────  │  ──────────────────────────────── │
│  Run selector (dropdown)    │  [Leaderboard][Detail][Compare]   │
│                             │  [Charts][Anomalies][Export]       │
│  ── Filters ──              │                                    │
│  Grade (multiselect)        │  TAB: Leaderboard                 │
│  NOVA (multiselect)         │  ┌─────────────────────────────┐  │
│  Archetype (multiselect)    │  │ Horizontal bar chart        │  │
│  Subtype (multiselect)      │  │ grade-colored, score-sorted │  │
│  Score range (slider)       │  └─────────────────────────────┘  │
│  Name search (text)         │  Filterable product table         │
│                             │                                    │
│  ── Flags ──                │  TAB: Product Detail              │
│  Has cap applied            │  [image] score grade NOVA conf    │
│  Routing unstable           │  Radar chart | Waterfall chart    │
│  Has sweetener              │  Dimension scores table           │
│                             │  Drivers | Ingredients | Evidence │
│                             │                                    │
│                             │  TAB: Compare (2 products)        │
│                             │  Metrics row A vs B               │
│                             │  Radar overlay | Grouped bars     │
│                             │  Delta table | Nutrition table    │
│                             │                                    │
│                             │  TAB: Charts                      │
│                             │  Grade dist | NOVA dist           │
│                             │  Score histogram                  │
│                             │  Subtype/archetype dist           │
│                             │  Score-vs-nutrition scatter       │
│                             │                                    │
│                             │  TAB: Anomalies                   │
│                             │  Auto-detected violations:        │
│                             │  NOVA1+cap, vanilla=NOVA4,        │
│                             │  routing instability, etc.        │
│                             │                                    │
│                             │  TAB: Export                      │
│                             │  Filtered table preview           │
│                             │  [Download CSV] button            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Anomaly Detection

The Anomalies tab auto-flags 10 architectural tension patterns:

| Code | Pattern |
|---|---|
| NOVA1+cap | NOVA1 product with a binding cap (floor/cap conflict) |
| vanilla=NOVA4 | "ואניל" in ingredients, NOVA=4 (Evolution #5 bug) |
| routing_unstable | category_instability_flag = True |
| dairy→beverage | "יוגורט"/"קפיר" in name but routed to beverage |
| yogurt→sauce_spread | "יוגורט" in name but routed to sauce_spread |
| non-fat→whole_food_fat | Low fat (<5g) product routed to whole_food_fat |
| 2+_red_labels | cap ≤ 45 (two or more red labels applied) |
| high-conf+low-score | confidence ≥ 0.75, score < 45 |
| NOVA1_floor_masks_routing | NOVA1 floor=85, score=85, routed to beverage |
| sweetener_only_NOVA4 | sweetener detected, no other NOVA4 signals, NOVA=4 |

---

## Missing Fields (for improved reporting)

These fields would materially improve dashboard utility but are absent from current BSIP1/BSIP2 outputs:

| Field | Where missing | Impact |
|---|---|---|
| `image_url` | Null for all synthetic products; only real Yohananof scrapes have it | Product thumbnails blank for stress-test runs |
| `canonical_name_en` | Not in BSIP1 schema | English-language filtering impossible |
| Unified `bsip_subtype` | Each category stores `bsip_cereal_subtype`, `bsip_yogurt_subtype`, etc. — no shared field | Subtype filter must use the generic `bsip_*_subtype` scan; cross-category subtype comparison not possible |
| `is_plant_based` | Not a BSIP1 flag | Plant-based products cannot be filtered directly; must infer from name/ingredients |
| `serving_size_g` | Missing for most products | Satiety and portion-adjusted scoring context unavailable |
| `retailer_price` | Not scraped in BSIP0 | Market positioning analysis (price vs score) not possible |
| Signal match detail in trace | Trace shows aggregate signals, not which specific ingredient matched which regex | Cannot drill into "why additive_count=4" at product detail level |
| `score_after_penalty` rationale | Trace shows the penalty delta but not which penalty rule triggered it | Waterfall "Penalty" step has no tooltip context |
| `nova_evidence_for` per-signal weights | Evidence strings are free text; can't programmatically rank which signal was binding | NOVA breakdown in detail panel is narrative-only |
| `fermentation_quality` dimension | Dimension does not exist in proto_v0 | Kefir, live-culture yogurt, and heat-treated products score identically on this axis |
