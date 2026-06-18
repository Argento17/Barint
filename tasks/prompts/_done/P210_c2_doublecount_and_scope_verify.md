# P210 — verification grunt: double-count set + scope diff (route: C2)
# DeepSeek audit — ZERO-INFERENCE, deterministic output only. Decide nothing.

**Repo:** `C:\Bari`
This is a mechanical cross-check feeding TASK-327/328/329 orchestrator verification. Output literal results only;
do not edit any file, do not decide which source is "right."

## Task 1 — overlap set (deterministic intersection of two explicit lists)
- List A = additive E-numbers/tokens in `HIGH_RISK_EMULSIFIER_PATTERNS` in
  `03_operations/bsip2/proto_v0/src/signal_extractor.py`.
- List B = entries in `03_operations/bsip2/proto_v0/src/ingredient_taxonomy.py` whose `additive_class` contains
  the substring `concern` (i.e. `is_named_concern=True` concern-class identities).
- Output the **exact intersection** (E-numbers present in BOTH A and B) and its count. (Expected ballpark:
  E466/CMC, E407/carrageenan, E433/polysorbate — but report what you literally find, not what is expected.)

## Task 2 — scoring-path scope state (run verbatim, paste output)
- `git status --short`
- `git diff --stat -- 03_operations/bsip2/proto_v0/src/score_engine.py 03_operations/bsip2/proto_v0/src/constants.py 03_operations/page_generator/configs`
Report whether the scoring path is clean (no diff) — literal output only.

## Boundaries
- Zero inference. If anything requires a judgment call, write `NEEDS-C1` and stop on that item.
- OFF-ban: do not read or reference Open Food Facts.

## Return
The two literal outputs + return-contract JSON (`01_framework/operations/return_contract_v1.md`).
**Do not close anything.**
