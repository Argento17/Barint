---
name: bari-score-presentation-v1
description: "Bari Score Presentation Philosophy v1 — primary display format, forbidden labels (חזק/בינוני/חלש), grade ranges, confidence states, secondary evidence lines, color encoding prohibition"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0992f16e-b33f-475c-a0cf-6a0c70b3da1d
---

Built 2026-05-27. Master document at `C:\Bari\01_framework\editorial\score_presentation_v1.md`.

**Why:** UX drift toward recommendation/emotional language (חזק, בינוני, חלש) weakens Bari's positioning as an investigative interpretation platform. These labels hide multidimensional reasoning, introduce judgment framing, and create legal/commercial exposure.

**How to apply:** All consumer-facing score display — web, app, blog, API frontend — follows these rules. When any display element pushes toward recommendation or sentiment, remove it.

## Core Rules

**Primary display:** `72 / B` — numeric score + grade letter only. Nothing else.

**Grade ranges:**
- A: 80–100 (consistent alignment across most dimensions)
- B: 65–79 (partial alignment; at least one strong dimension)
- C: 50–64 (label positioning outpaces ingredient evidence)
- D: <50 (recurring gap between presentation and reality)

Grade descriptions are for internal understanding. The letter is the only consumer-facing element.

**Secondary display (optional):** 1–3 evidence lines.
Format: `[dimension]: [finding]`
Example: `תסיסה: שמרים תעשייתיים בלבד`
These are observations from ingredient list / nutrition panel. Not interpretations.

**Contextual insight (optional):** One sentence in editorial contexts only. Describes the finding, never recommends.

**Confidence states:**
- Verified: `72 / B` (no qualifier)
- Partial: `72 / B · ניתוח חלקי` + mandatory explanation line
- Insufficient: `לא נוקד` + mandatory reason sentence

Never use: blank, `—`, `N/A`, or a score without confidence indication when data is partial.

## Forbidden Labels

חזק, בינוני, חלש, מצוין, מומלץ, לא מומלץ, ✓ טוב, ⚠ הימנע, כדאי לקנות, הכי טוב בקטגוריה, colored score backgrounds (red/yellow/green).

Color encoding is functionally identical to verbal labels — the prohibition applies to both.

## The Core Rule

Bari shows what it found. The consumer decides what to do with it. The score is a finding. The grade is a range marker. Neither is a recommendation.

[[bari-editorial-intelligence-v1]]
