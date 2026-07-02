# Return: P455

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P455_c3_deanchor_rollout_consult.md` |
| Model | `openai/gpt-5.5` |
| Started | 2026-07-02T07:37:13.140641+00:00 |
| Finished | 2026-07-02T07:38:45.204880+00:00 |
| Exit code | 0 |

---

## Output

```
**Ranked Findings**

| severity | area | the problem | why it can't be defended / what's unverified | suggested direction |
|---|---|---|---|---|
| CRITICAL | Owner intent / scoring philosophy | The implementation may not match “drift away almost completely from the red-label thing.” It does not make red labels broadly matter less; it removes cliffs but makes threshold proximity continuously matter, including below-label products. | Publicly, this is easy to attack as “Bari still scores around red-label thresholds, just less visibly.” If the owner meant “reduce dependence on red-label logic,” this is a philosophy mismatch, not an implementation detail. | Require an explicit owner ruling: “continuous threshold-distance scoring is the intended replacement,” including acceptance of below-threshold penalties. |
| HIGH | Clean-product tax | Clean products with no red label can lose points solely for being near a red-label threshold. | A consumer or competitor can reasonably ask: “Why was this product lowered if the regulator does not mark it red?” The answer “because it is near the line” is defensible only if Bari openly claims a stricter gradient than the label system. | Decide whether near-threshold clean products should be taxed at all, or whether continuous penalties should start only after the red-label threshold. |
| HIGH | Removal of hard caps | A 5%-weight regulatory dimension may be too weak to prevent an otherwise attractive but nutritionally poor product from scoring surprisingly high once cliff caps disappear. | The current safety claim proves monotonicity, not public plausibility. A high-protein / high-fiber / “natural” snack bar or cereal with very high sugar and saturated fat could regain enough points elsewhere to look better than a consumer would expect. | Run archetype audits: top-scoring products with 1, 2, and 3 red labels after flag ON, by category. Owner should inspect whether any are publicly indefensible. |
| HIGH | Measurement trust | ON-vs-OFF movement was measured on a corpus with known baseline-reproduction drift. | ON-vs-OFF isolates the flag mechanically, but it does not prove the announced live impact. The “~20 flips” number may be directionally useful but is weak as an owner-facing rollout promise if published baselines do not reproduce. | Separate two numbers: “flag-only movement on current reproducible corpus” and “expected public movement from currently published site.” Do not present one as the other. |
| HIGH | Cross-category consistency during rollout | Category-by-category activation means the same red-label philosophy is live in some shelves but not others. | A user comparing cheese, snacks, cereals, and cakes during the rollout can see Bari applying two scoring philosophies at once. That is hard to defend if copy says Bari changed how red labels work generally. | Use either a short private activation window, a global feature cutover after category content is ready, or explicit temporary rollout language. |
| MEDIUM | Cocoa gate | A ≥70% cocoa relief line creates a new cliff while removing old cliffs. | The rationale may be nutritionally valid, but 69% vs 70% will look arbitrary unless tied to a cited evidence standard and actual product-label observability. | Prefer a continuous cocoa-solids relief curve, or document why 70% is the defended nutrition threshold. |
| MEDIUM | Copy implications | Existing category copy may still explain outcomes using red-label cliff logic or “red label = ceiling” assumptions. | If scores move but explanatory copy still references old cliffs, Bari creates visible inconsistency between score, badge, and explanation. | Inventory all score-explanation copy, not only grade-mover pages. |
| MEDIUM | Boundary flip framing | “Every flip is single-band boundary-straddle” may understate consumer impact. | A grade flip is consumer-salient even if numerically small. Saying it is only a boundary issue can sound evasive when a product moves from B to C or C to B. | Treat every grade flip as content-significant and require per-product explanation review. |
| MEDIUM | Label coverage / observability | The facts mention sodium observability in cereals, but not coverage confidence for sugar, saturated fat, and 2+-label detection across all live shelves. | A continuous rule is more sensitive to exact values than a binary cap. Missing or imprecise nutrition fields can now create subtler ranking errors. | Require coverage and null-rate tables per affected label and shelf before activation. |

**Axes That Look Clean**

| axis | status |
|---|---|
| OFF byte-identical behavior | Clean, based on stated A/B verification. |
| ON moves scores | Clean. |
| Inversion invariant / monotonicity | Clean as a safety property, but not sufficient for public plausibility. |
| Trans-fat safety veto | Clean, stated untouched. |
| Sodium double-count interaction | Clean for cereals/granola based on stated construction and corpus check. |
| Chocolate immediate rollout | Clean only because it is deferred. The cocoa rule itself is not yet clean. |
| Safe zero-move shelves | Mechanically lower risk, but not philosophically clean if they begin a mixed live regime. |

**RETURNED**

Files changed: none.

What to verify:
`scoring activation brief`: explicit owner acceptance of continuous threshold-distance scoring and clean-product tax.
`movement report`: separate current-corpus ON/OFF movement from published-site movement.
`category QA`: top red-label products after flag ON, per affected shelf.
`copy QA`: all score-explanation copy that references red-label caps or thresholds.

```json
{
  "status": "RETURNED",
  "reviewer_role": "C3_independent_challenger",
  "files_changed": [],
  "finding_counts": {
    "CRITICAL": 1,
    "HIGH": 4,
    "MEDIUM": 4
  },
  "overall_recommendation": "NO-GO",
  "single_decisive_reason": "The activation is not yet publicly defensible because the owner-approved intent to drift away from red-label dependence has not been explicitly reconciled with a continuous threshold-distance model that can lower clean no-red-label products.",
  "axes_clean": [
    "OFF byte-identical behavior",
    "ON score movement",
    "inversion invariant / monotonicity",
    "trans-fat veto unchanged",
    "cereal/granola sodium double-count check",
    "chocolate deferred pending evidence"
  ]
}
```

--- SSE Events ---
  server.connected: {}
  session.created: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"id": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "slug": "proud-circuit", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  session.next.agent.switched: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c2d300197GkatbvEuAgN8", "timestamp": "2026-07-02T07:37:19.826Z", "agent": "build"}
  message.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"id": "msg_f21c2c2d2001mVTix8gE07I2ld", "role": "user", "sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "time": {"created": 1782977839826}, "age
  message.part.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "part": {"type": "text", "text": "You are the outside-the-family independent challenger (C3). Bari is about to begin activating a NEW scoring behavior a
  session.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"id": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "slug": "proud-circuit", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  session.status: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"id": "msg_f21c2c43d001sp3QzMYR2qnVhW", "parentID": "msg_f21c2c2d2001mVTix8gE07I2ld", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"id": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "slug": "proud-circuit", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  session.diff: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "diff": []}
  message.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"role": "user", "time": {"created": 1782977839826}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "id": "msg_f21c2
  session.status: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "status": {"type": "busy"}}
  message.part.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "part": {"id": "prt_f21c2d3d6001ffhA8pMqR2K3b2", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "snapshot
  message.part.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "part": {"id": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "type": "
  session.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"id": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "slug": "proud-circuit", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": "**Considering answer review**\n\nI
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " review"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " answer"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " without"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " using"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " tools"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " which"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " means"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " probably"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " inspect"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " closely"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " user"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " provided"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " facts"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " looking"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " findings"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " I'm"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " thinking"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " comply"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " returning"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " contract"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " JSON"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " which"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " might"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " require"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " some"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " careful"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " reading"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " root"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " seems"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " indicate"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " return"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " block"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " ends"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " JSON"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " could"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " also"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " think"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " about"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " loading"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " scoring"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " skills"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": " governance"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "partID": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "part": {"id": "prt_f21c2d4a2001fjj4zzCKIxvdtw", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "type": "
  message.part.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "part": {"id": "prt_f21c2e213001G67SjV0wv6Km0N", "messageID": "msg_f21c2c43d001sp3QzMYR2qnVhW", "sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "type": "
  message.part.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "part": {"type": "tool", "tool": "skill", "callID": "call_7PvEEI5w8yILv5KRDtR1XQts", "state": {"status": "running", "input": {"name": "bari-bsip2-scorin
  message.part.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "part": {"type": "tool", "tool": "skill", "callID": "call_7PvEEI5w8yILv5KRDtR1XQts", "state": {"status": "completed", "input": {"name": "bari-bsip2-scor
  message.part.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "part": {"id": "prt_f21c2e860001KGDQ132kwVEx9E", "reason": "tool-calls", "snapshot": "f73ff9c7fd67734ea0ae2a29cc292d86756a6f7c", "messageID": "msg_f21c2
  message.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"id": "msg_f21c2c43d001sp3QzMYR2qnVhW", "parentID": "msg_f21c2c2d2001mVTix8gE07I2ld", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"id": "msg_f21c2c43d001sp3QzMYR2qnVhW", "parentID": "msg_f21c2c2d2001mVTix8gE07I2ld", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"id": "msg_f21c2edc2001D4irntyVjfL5Z4", "parentID": "msg_f21c2c2d2001mVTix8gE07I2ld", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"id": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "slug": "proud-circuit", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  session.diff: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "diff": []}
  session.status: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"role": "user", "time": {"created": 1782977839826}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
  message.part.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "part": {"id": "prt_f21c2f9a4001mkMcM6TmcNsot0", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "snapshot
  message.part.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "part": {"id": "prt_f21c2fdc90016deoOxohZZMpuV", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "type": "
  message.part.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "part": {"id": "prt_f21c2fdc90016deoOxohZZMpuV", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "type": "
  message.part.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "part": {"id": "prt_f21c33339001aR05gEyd5KOc11", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "type": "
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "Rank"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ed"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Findings"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "**\n\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " severity"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " area"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " problem"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " why"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " can't"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " defended"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " what's"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " un"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "verified"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " suggested"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " direction"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "---"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "---"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "---"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "---"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "---"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " CR"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ITICAL"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Owner"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " intent"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " scoring"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " philosophy"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " implementation"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " match"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "dr"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ift"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " away"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " almost"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " completely"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " thing"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ".\u201d"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " does"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " make"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " labels"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " broadly"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " matter"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " less"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " removes"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cliffs"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " makes"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " threshold"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " proximity"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " continuously"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " matter"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " including"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " below"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " products"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Public"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ly"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " easy"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " attack"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "B"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ari"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " still"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " scores"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " around"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " thresholds"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " just"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " less"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " visibly"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ".\u201d"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " If"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " owner"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " meant"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "reduce"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " dependence"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " logic"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ",\u201d"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " philosophy"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " mismatch"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " implementation"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " detail"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Require"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " explicit"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " owner"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " ruling"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "continuous"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " threshold"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-distance"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " scoring"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " intended"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " replacement"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ",\u201d"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " including"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " acceptance"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " below"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-th"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "reshold"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " penalties"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " HIGH"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Clean"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-product"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " tax"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Clean"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " products"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " no"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " lose"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " points"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " solely"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " being"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " near"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " threshold"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " competitor"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " reasonably"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " ask"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "Why"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " was"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " lowered"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " regulator"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " does"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " mark"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "?\u201d"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " answer"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "because"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " near"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " line"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " defens"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ible"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Bari"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " openly"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " stric"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ter"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " gradient"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " system"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Decide"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " whether"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " near"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-th"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "reshold"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " clean"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " products"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " taxed"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " at"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " all"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " whether"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " continuous"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " penalties"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " start"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " after"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " threshold"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " HIGH"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Removal"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " hard"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " caps"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "%-"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "weight"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " regulatory"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " dimension"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " too"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " weak"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " prevent"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " otherwise"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " attractive"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " nutr"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "itionally"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " poor"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " scoring"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " surprisingly"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " once"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cliff"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " caps"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " disappear"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " current"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " safety"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " claim"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " proves"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " monot"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "onic"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ity"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " public"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " plaus"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ibility"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-pro"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "tein"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-f"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "iber"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "natural"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " snack"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " bar"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cereal"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " very"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " saturated"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " fat"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " could"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " regain"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " enough"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " points"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " elsewhere"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " look"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " would"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " expect"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Run"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " arche"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "type"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " audits"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " top"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-sc"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "oring"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " products"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " labels"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " after"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " flag"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " ON"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " category"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Owner"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " inspect"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " whether"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " any"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " publicly"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " indef"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ensible"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " HIGH"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Measurement"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " trust"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " ON"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-v"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-O"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "FF"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " movement"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " was"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " measured"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " corpus"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " known"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " baseline"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-re"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "production"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " drift"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  file.watcher.updated: {"file": "C:\\Bari\\.git\\index.lock", "event": "add"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " ON"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-v"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-O"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "FF"}
  file.watcher.updated: {"file": "C:\\Bari\\.git\\index.lock", "event": "unlink"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " isolates"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " flag"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " mechanically"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " does"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " prove"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " announced"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " live"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " impact"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "~"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " flips"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " number"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " direction"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ally"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " useful"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " weak"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " owner"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-facing"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " rollout"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " promise"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " published"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " bas"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "elines"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " do"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " reproduce"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Separate"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " two"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " numbers"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "flag"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-only"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " movement"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " current"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " reproduc"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ible"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " corpus"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "expected"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " public"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " movement"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " currently"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " published"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " site"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ".\u201d"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Do"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " present"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " one"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " other"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " HIGH"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Cross"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-category"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " consistency"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " during"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " rollout"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Category"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-by"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-category"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " activation"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " means"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " same"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " philosophy"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " live"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " some"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " shelves"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " others"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " user"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " comparing"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cheese"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " snacks"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cereals"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cakes"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " during"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " rollout"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " see"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Bari"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " applying"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " two"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " scoring"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " philosophies"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " at"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " once"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " That"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " hard"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " defend"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " copy"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " says"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Bari"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " changed"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " how"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " labels"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " work"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " generally"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Use"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " either"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " short"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " private"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " activation"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " window"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " global"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " feature"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cut"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "over"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " after"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " category"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " content"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " ready"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " explicit"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " temporary"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " rollout"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " language"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " MED"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "IUM"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Cocoa"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " gate"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \u2265"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "70"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cocoa"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " relief"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " line"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " creates"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " new"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cliff"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " while"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " removing"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " old"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cliffs"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " rationale"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " nutr"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "itionally"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " valid"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "69"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " vs"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "70"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " will"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " look"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " arbitrary"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " unless"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " tied"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cited"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " standard"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " actual"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " observ"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ability"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Prefer"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " continuous"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cocoa"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-sol"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ids"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " relief"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " curve"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " document"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " why"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "70"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " defended"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " nutrition"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " threshold"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " MED"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "IUM"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Copy"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " implications"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Existing"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " category"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " copy"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " still"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " explain"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " outcomes"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " using"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cliff"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " logic"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " ceiling"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " assumptions"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " If"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " scores"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " move"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " explanatory"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " copy"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " still"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " references"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " old"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cliffs"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Bari"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " creates"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " visible"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " incons"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "istency"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " between"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " badge"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " explanation"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Inventory"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " all"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-ex"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "planation"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " copy"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " grade"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-m"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "over"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " pages"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " MED"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "IUM"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Boundary"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " flip"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " framing"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "Every"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " flip"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " single"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-band"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " boundary"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-str"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "addle"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "state"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " impact"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " grade"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " flip"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-s"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "al"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ient"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " even"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " numer"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ically"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " small"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Saying"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " boundary"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " issue"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " sound"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " evas"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ive"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " when"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " moves"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " B"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " B"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Treat"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " every"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " grade"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " flip"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " content"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-sign"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ificant"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " require"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-product"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " explanation"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " review"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " MED"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "IUM"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " coverage"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " observ"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ability"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " facts"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " mention"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " sodium"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " observ"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ability"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cereals"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " coverage"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " confidence"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " sugar"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " saturated"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " fat"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "+-"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " detection"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " across"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " all"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " live"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " shelves"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " continuous"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " rule"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " more"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " sensitive"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " exact"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " values"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " binary"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cap"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Missing"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " im"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "prec"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ise"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " nutrition"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " fields"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " now"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " create"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " subt"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ler"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " ranking"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " errors"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Require"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " coverage"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " null"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-rate"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " tables"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " affected"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " shelf"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " before"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " activation"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "Axes"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " That"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Look"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Clean"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "**\n\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " axis"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " status"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "---"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "---"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " OFF"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " byte"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-ident"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ical"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " behavior"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Clean"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " based"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " stated"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "/B"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " verification"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " ON"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " moves"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " scores"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Clean"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " In"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "version"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " invariant"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " monot"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "onic"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ity"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Clean"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " safety"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " property"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " sufficient"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " public"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " plaus"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ibility"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Trans"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-fat"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " safety"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " veto"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Clean"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " stated"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " untouched"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Sodium"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " double"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-count"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " interaction"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Clean"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cereals"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "/gr"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "an"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ola"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " based"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " stated"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " construction"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " corpus"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " check"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Chocolate"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " immediate"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " rollout"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Clean"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " deferred"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " cocoa"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " rule"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " itself"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  file.watcher.updated: {"file": "C:\\Bari\\.git\\index.lock", "event": "add"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " yet"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " clean"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "|"}
  file.watcher.updated: {"file": "C:\\Bari\\.git\\index.lock", "event": "unlink"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Safe"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " zero"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-m"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ove"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " shelves"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " Mechan"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ically"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " lower"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " risk"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " philosoph"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ically"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " clean"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " they"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " begin"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " mixed"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " live"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " regime"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " |\n\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "RETURN"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ED"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "**\n\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "Files"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " changed"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " none"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "What"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " verify"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "sc"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "oring"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " activation"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " brief"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "`:"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " explicit"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " owner"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " acceptance"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " continuous"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " threshold"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-distance"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " scoring"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " clean"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-product"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " tax"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "movement"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " report"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "`:"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " separate"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " current"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-c"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "orpus"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " ON"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "/O"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "FF"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " movement"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " published"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-site"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " movement"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "category"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " QA"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "`:"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " top"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " products"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " after"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " flag"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " ON"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " affected"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " shelf"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "copy"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " QA"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "`:"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " all"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-ex"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "planation"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " copy"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " references"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " caps"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " thresholds"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "```"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "json"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "{\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "status"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\":"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "RETURN"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ED"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\",\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "review"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "er"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "_role"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\":"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "C"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "_ind"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ependent"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "_ch"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "all"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "enger"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\",\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "files"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "_changed"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\":"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " [],\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "finding"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "_counts"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\":"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " {\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "   "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "CR"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ITICAL"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\":"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ",\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "   "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "HIGH"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\":"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ",\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "   "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "MED"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "IUM"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\":"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " },\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "overall"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "_re"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "commend"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ation"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\":"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "NO"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-G"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "O"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\",\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "single"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "_dec"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ive"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "_reason"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\":"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " activation"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " yet"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " publicly"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " defens"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ible"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " owner"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-approved"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " intent"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " drift"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " away"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " dependence"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " been"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " explicitly"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " reconc"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "iled"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " continuous"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " threshold"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-distance"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " model"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " lower"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " clean"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " no"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-red"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-label"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " products"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": ".\",\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "axes"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "_clean"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\":"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " [\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "   "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "OFF"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " byte"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-ident"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ical"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " behavior"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\",\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "   "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ON"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " movement"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\",\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "   "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "in"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "version"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " invariant"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " monot"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "onic"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ity"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\",\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "   "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "trans"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-fat"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " veto"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " unchanged"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\",\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "   "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ereal"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "/gr"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "an"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ola"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " sodium"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " double"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "-count"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " check"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\",\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "   "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ch"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "ocolate"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " deferred"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " pending"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "\"\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": " ]\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "}\n"}
  message.part.delta: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "partID": "prt_f21c33339001aR05gEyd5KOc11", "field": "text", "delta": "```"}
  message.part.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "part": {"id": "prt_f21c33339001aR05gEyd5KOc11", "messageID": "msg_f21c2edc2001D4irntyVjfL5Z4", "sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "type": "
  message.part.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "part": {"id": "prt_f21c3f45f001la00eChXTYHlLJ", "reason": "stop", "snapshot": "f73ff9c7fd67734ea0ae2a29cc292d86756a6f7c", "messageID": "msg_f21c2edc200
  message.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"id": "msg_f21c2edc2001D4irntyVjfL5Z4", "parentID": "msg_f21c2c2d2001mVTix8gE07I2ld", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"id": "msg_f21c2edc2001D4irntyVjfL5Z4", "parentID": "msg_f21c2c2d2001mVTix8gE07I2ld", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "status": {"type": "busy"}}
  session.status: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "status": {"type": "idle"}}
  session.idle: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i"}
  session.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"id": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "slug": "proud-circuit", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  session.diff: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "diff": []}
  message.updated: {"sessionID": "ses_0de3d42fdffeycrmQoOW1S3Y6i", "info": {"role": "user", "time": {"created": 1782977839826}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
M 01_framework/operations/hebrew_health_scan/daily_scans/local_scan_log.txt
 M bari-web/src/app/hashvaot/supermarket/page.tsx
?? 01_framework/operations/hebrew_health_scan/daily_scans/keepers_2026-07-02.json
?? design/Social/
?? scratch2.txt
?? scratch3.txt
?? scratch4.txt
?? scratch_out.txt
?? tasks/HANDOFF_SESSION_2026-07-02.md
?? tasks/prompts/P455_c3_deanchor_rollout_consult.md
```

### After dispatch

```
M 01_framework/operations/hebrew_health_scan/daily_scans/local_scan_log.txt
 M bari-web/src/app/hashvaot/supermarket/page.tsx
?? 01_framework/operations/hebrew_health_scan/daily_scans/keepers_2026-07-02.json
?? design/Social/
?? scratch2.txt
?? scratch3.txt
?? scratch4.txt
?? scratch_out.txt
?? tasks/HANDOFF_SESSION_2026-07-02.md
?? tasks/prompts/P455_c3_deanchor_rollout_consult.md
```

### Delta

*(no changes detected)*
