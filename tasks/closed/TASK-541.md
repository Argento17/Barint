---
id: TASK-541
title: ENGINE: three-layer enforcement — consumer copy can never carry data-state narration or mass-repeated sentences
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-08
closed_at: 2026-07-09
depends_on: []
blocks: []
category_id: null
close_reason: >
  Orchestrator-verified all three enforcement layers against artifacts on 2026-07-09 (unattended run,
  branch task506). LAYER 1 GENERATION: copy_constants.py BANNED_CONSUMER_PHRASES = 25 entries (single
  source); author_copy.py enforce_clean()/BannedPhraseError proven to RAISE on the exact owner-cited
  data-state phrase ('בלי צילום תווית מלא, אנחנו נשארים זהירים'); --selftest PASS over 57 template-bank
  entries, exit 0. LAYER 2 VALIDATION: validate_copy_authored.py (CHECK2 sentence mass-templating /
  CHECK3 baseline fingerprint / CHECK4 field-level) — real shipped yogurt JSONs PASS (spoonable 78,
  drinkable 20; banned=0 sentence_repeat=0 fingerprint=0 mass=0); negative fixtures FAIL exit 1 as
  designed (baseline_fingerprint_negative catches template fingerprints incl bariInterpretation;
  masshedge_negative catches banned 'צילום תווית' + mass-hedge). LAYER 3 COMMIT:
  guard-two-gate-commit.ps1 runs the validator on staged bari-web comparison JSON via a cmd /c wrapper
  (PS5.1 native-stderr trap fixed), blocks the commit on a real FAIL, fails-open only on infrastructure
  error. All DoD controls reproduced live by the orchestrator, not taken on the return's word.
summary: >
  Owner ruling 2026-07-08 (after yogurt disclaimer blowup): PRIMARY failure = the generation layer could produce data-state boilerplate ('בלי צילום תווית מלא...') as consumer copy at all; catching it late is secondary. Fix at 3 layers: (1) GENERATION — copy_constants.py single source of BANNED_CONSUMER_PHRASES; author_copy.py raises at generation time on any banned phrase; content-agent persona hard rule (never narrate data state/confidence/provenance; drop any sentence proposed for >5 products). (2) VALIDATION — validate_copy_authored.py hardened: static+robust banned list, zero-tolerance on all consumer fields, sentence-level repetition check (same sentence >10 products = FAIL, catches shared-closing-sentence that field-dedup missed), wired into validate_comparison_page.py battery. (3) COMMIT — guard-two-gate-commit.ps1 runs the validator on staged comparison JSONs, blocks on FAIL. Proof = 5 controls (clean yogurt PASS, hedge-fixture FAIL, HEAD-original FAIL, brined+crackers PASS, generation-time raise).
---

# TASK-541 — ENGINE: three-layer enforcement — consumer copy can never carry data-state narration or mass-repeated sentences

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
