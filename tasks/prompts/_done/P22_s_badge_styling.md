P22 / TASK-256 — S-grade badge visual treatment (Design Agent). Go-live gate for
the yogurts launch: the data layer now emits grade "S" (corpus.ts:51 score>=90→"S";
view-models BariGrade includes "S"), but the live site has NEVER rendered an S grade.
P19 correctly produced yogurts_frontend_v4.json (2 S products: 90.6, 92.6) but did
NOT improvise the visual — that's this task.

CONTEXT / CONSTRAINTS (read before designing):
- Memory `bari_score_presentation_v1`: score display is numeric/grade only; **color
  encoding is FORBIDDEN** — grades are NOT distinguished by green/red/etc. So S must
  NOT introduce a new color semantic. Differentiate within the sanctioned system
  (typographic weight/size, a restrained mark, the existing chip treatment) — recommend
  the single best treatment, do not present an A/B menu.
- Memory `bari_canonical_reference_v1` + frozen pixel values: extend the CANONICAL
  score-badge / grade-chip component; do not fork a new one or improvise pixels.
- RTL Hebrew layout; S must sort ABOVE A wherever grades are ordered.
- This is reversible: implement the styling so the S badge renders correctly, but do
  NOT flip the live-route import (v3→v4) — wiring the page live is the owner's go-live
  act, tracked separately.

DO:
1. Locate the canonical component(s) that render the grade chip / score badge (the
   one drawing A/B/C/D/E today) and the comparison page that orders products. Cite paths.
2. Extend it to render "S" consistently with the constraints above. Verify: S chip
   renders, S sorts above A, RTL correct, no new color semantic introduced.
3. Fix the now-stale doc comment at bari-web/src/lib/comparisons/corpus.ts:42-43
   (it still says "the UI palette has no S" / "S≥90 folds into A" — both false now;
   the code returns "S"). Rewrite to describe the 6-grade S≥90 behavior accurately.
4. Validate with the v4 file (2 S products) on a local/preview render — screenshot
   the S badge in context. Do NOT change scores, grades, copy, or the live import.

RULES: no score/grade/data changes; no live-route import flip; no new color encoding;
canonical component only; frozen pixels respected; no OFF.

RETURN BLOCK: component path(s) changed; the S treatment chosen + one-line rationale
vs the color-encoding ban; confirm S sorts above A + RTL ok; corpus.ts comment fixed;
screenshot/preview evidence; the exact one-line import change still pending for go-live.
Propose RETURNED.

---
After you send this to the agent: open tasks\DISPATCH_BOARD.md and put an `x` in the
P22 line under 📬 Signals.
