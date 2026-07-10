// Rubric `display_suppression_rule` (01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml)
// — TASK-504C.
//
// Computes, from the LIVE product array (never a hardcoded per-guide/per-bar
// exclusion list — the rubric's own re_evaluated_per_build clause), which bars are
// display-suppressed for a given guide build: a bar suppresses IFF its computed state
// is `cannot_verify` for 100% of the currently displayed products — not "mostly," not
// any other uniform state. A uniform FAIL or uniform PASS must NEVER suppress (rubric
// guardrail_never_hides_a_fail) — this function enforces that by construction, since it
// only ever tests for the `cannot_verify` state specifically.
//
// DISPLAY-only: callers must not feed this back into bucket_logic. bucket_logic already
// evaluated all 6 bars before this function ever runs (product.bucket is fixed input),
// and this function does not read or touch `product.bucket`.

import type { GuideBarKey, GuideProductVM } from "@/lib/view-models";

export function computeSuppressedBars(
  products: GuideProductVM[],
  barOrder: readonly GuideBarKey[]
): GuideBarKey[] {
  if (products.length === 0) return [];

  return barOrder.filter((bar) =>
    products.every((product) => {
      const result = product.bars.find((b) => b.bar === bar);
      return result?.state === "cannot_verify";
    })
  );
}

/**
 * Band-gating exclusion (rubric `band_gating_exclusion_rule`, TASK-504 v2) — SEPARATE
 * from `computeSuppressedBars`. A bar is excluded from tier-GATING when, across the
 * ranked domestic pool, NO product resolves it to `pass` AND NO product resolves it to
 * `fail` (two ANDed existential negations — no ratio/threshold). Excluded bars still
 * render per-product; they are NOT added to `suppressedBars`.
 */
export function computeBandExcludedBars(
  products: GuideProductVM[],
  barOrder: readonly GuideBarKey[]
): GuideBarKey[] {
  if (products.length === 0) return [];

  return barOrder.filter((bar) => {
    const hasPass = products.some((product) => {
      const result = product.bars.find((b) => b.bar === bar);
      return result?.state === "pass";
    });
    const hasFail = products.some((product) => {
      const result = product.bars.find((b) => b.bar === bar);
      return result?.state === "fail";
    });
    return !hasPass && !hasFail;
  });
}
