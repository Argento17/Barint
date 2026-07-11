/**
 * Deterministic projections of existing Product Dossier fields for the
 * human-readable Overview tab (TASK-620 / PD-3.1). Every function here reads
 * ONLY fields already present on `ProductDossier` / the resolved `BariProductVM`
 * confidence and produces a plain-English rendering of them — no authored prose,
 * no new claims, no invented thresholds beyond what is documented inline.
 *
 * Section E ("Human insights") rule: if a bucket has no qualifying field, the
 * caller must render nothing for it — these functions return empty arrays in
 * that case rather than padding with placeholder text.
 */
import type { BariConfidence } from "@/lib/view-models";
import { DIMENSION_LABEL, LAYER2_FIELD_META, LAYER4_CHECK_LABEL } from "./overview-labels";
import type { CheckStatus, Layer2Evidence, Layer3, Layer4Check, Layer4Checks } from "./types";

// ─── B. Verification badge ──────────────────────────────────────────────────

export type VerificationState = "verified" | "estimated" | "mismatched" | "untraceable";

export const VERIFICATION_STATE_LABEL: Record<VerificationState, string> = {
  verified: "Verified",
  estimated: "Estimated",
  mismatched: "Mismatched",
  untraceable: "Untraceable",
};

export const VERIFICATION_STATE_DESCRIPTION: Record<VerificationState, string> = {
  verified: "The published score reproduces from trace data, and the underlying evidence is high-confidence.",
  estimated: "The score is not fully confirmed — either reproducibility check found a partial match, or the underlying evidence confidence is not full. Do not read this as equivalent to Verified.",
  mismatched: "The reproducibility check FAILED — the published score could not be reproduced from trace data.",
  untraceable: "No reproducibility verdict is available (no trace / unknown outcome) — this score's origin cannot currently be confirmed.",
};

/**
 * Derivation (documented, deterministic — no new data):
 *   calculation.status === "fail"    -> "mismatched"  (published score does not reproduce)
 *   calculation.status === "unknown" -> "untraceable"  (no reproducibility verdict at all)
 *   calculation.status === "warn"    -> "estimated"    (partial reproducibility signal)
 *   calculation.status === "pass"    -> "verified" IF the matched product's confidence is
 *                                        "verified", ELSE "estimated" (the calculation
 *                                        reproduces, but the underlying evidence itself
 *                                        was not fully confirmed — never label that combo
 *                                        the same as a fully verified row).
 * `confidence` is null when there is no matched live product (unmatched case) — callers
 * should not invoke this without a match; it defaults to "untraceable" defensively.
 */
export function deriveVerificationState(
  calculationCheck: Layer4Check,
  confidence: BariConfidence | null,
): VerificationState {
  switch (calculationCheck.status) {
    case "fail":
      return "mismatched";
    case "unknown":
      return "untraceable";
    case "warn":
      return "estimated";
    case "pass":
      return confidence === "verified" ? "verified" : "estimated";
    default:
      return "untraceable";
  }
}

// ─── E. Human insights ───────────────────────────────────────────────────────

export interface DimensionEntry {
  key: string;
  label: string;
  value: number;
}

function assessmentDimensionEntries(layer3: Layer3): DimensionEntry[] {
  const raw = layer3.assessment.dimension_scores?.value as Record<string, number> | null | undefined;
  if (!raw) return [];
  return Object.entries(raw)
    .filter(([, v]) => typeof v === "number")
    .map(([key, value]) => ({ key, label: DIMENSION_LABEL[key] ?? key, value }));
}

/** Up to 3 highest-scoring assessment axes. Empty when no dimension_scores exist. */
export function deriveStrengths(layer3: Layer3): DimensionEntry[] {
  return [...assessmentDimensionEntries(layer3)].sort((a, b) => b.value - a.value).slice(0, 3);
}

/** Up to 3 lowest-scoring assessment axes, excluding any already listed as a strength. */
export function deriveConcerns(layer3: Layer3): DimensionEntry[] {
  const strengthKeys = new Set(deriveStrengths(layer3).map((d) => d.key));
  return [...assessmentDimensionEntries(layer3)]
    .filter((d) => !strengthKeys.has(d.key))
    .sort((a, b) => a.value - b.value)
    .slice(0, 3);
}

/** Up to 3 layer_2 fields with status "not_retrieved" (spec-literal — not a value-null check). */
export function deriveMissingInformation(layer2: Layer2Evidence): string[] {
  return Object.entries(layer2)
    .filter(([, cell]) => cell.status === "not_retrieved")
    .map(([field]) => LAYER2_FIELD_META[field]?.label ?? field)
    .slice(0, 3);
}

export interface ActionItem {
  checkId: string;
  label: string;
  status: CheckStatus;
  detail: string | null;
}

/** Up to 3 recommended actions, one per failed/warn layer_4 check. */
export function deriveRecommendedActions(layer4: Layer4Checks): ActionItem[] {
  const entries = Object.entries(layer4) as [keyof Layer4Checks, Layer4Check][];
  return entries
    .filter(([, check]) => check.status === "fail" || check.status === "warn")
    .map(([id, check]) => ({
      checkId: id,
      label: LAYER4_CHECK_LABEL[id] ?? id,
      status: check.status,
      detail: check.reason ?? check.evidence[0] ?? null,
    }))
    .slice(0, 3);
}

// ─── F. Checks needing attention ────────────────────────────────────────────

export interface AttentionCheck {
  id: keyof Layer4Checks;
  label: string;
  check: Layer4Check;
}

export function deriveAttentionChecks(layer4: Layer4Checks): {
  attention: AttentionCheck[];
  passedCount: number;
} {
  const entries = Object.entries(layer4) as [keyof Layer4Checks, Layer4Check][];
  const attention = entries
    .filter(([, check]) => check.status !== "pass")
    .map(([id, check]) => ({ id, label: LAYER4_CHECK_LABEL[id] ?? id, check }));
  const passedCount = entries.length - attention.length;
  return { attention, passedCount };
}
