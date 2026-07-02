/**
 * Bari Retailer Normalisation Map
 *
 * Converts the raw per-product `retailer` string (or _meta.retailer fallback)
 * into the canonical BariRetailerRefVM shape used by the inventory dashboard.
 *
 * Rules (from orchestrator decision, 2026-07-01):
 *   - {"shufersal","שופרסל"}         → { id:"shufersal", nameHe:"שופרסל" }
 *   - {"yohananof","yochananof"}      → { id:"yohananof", nameHe:"יוחננוף" }
 *   - compound (contains "+")         → { id:"multi",     nameHe:"מספר רשתות" }
 *   - absent / null                   → falls back to _meta.retailer, then "other"
 *   - unmatched                       → { id:"other",     nameHe:"אחר" }
 *
 * This module is the single reusable normalisation boundary.
 * It never touches scoring, nutrition, or any display field beyond retailer.
 */

import type { BariRetailerRefVM } from "@/lib/view-models";

// Canonical entries
export const RETAILER_SHUFERSAL: BariRetailerRefVM = {
  id: "shufersal",
  nameHe: "שופרסל",
};

export const RETAILER_YOHANANOF: BariRetailerRefVM = {
  id: "yohananof",
  nameHe: "יוחננוף",
};

export const RETAILER_MULTI: BariRetailerRefVM = {
  id: "multi",
  nameHe: "מספר רשתות",
};

export const RETAILER_OTHER: BariRetailerRefVM = {
  id: "other",
  nameHe: "אחר",
};

/**
 * Normalise a raw retailer string to the canonical BariRetailerRefVM.
 * Returns RETAILER_OTHER for any unrecognised value.
 * Never returns null — every product resolves to exactly one canonical retailer.
 */
export function normalizeRetailer(
  raw: string | null | undefined
): BariRetailerRefVM {
  if (!raw) return RETAILER_OTHER;

  const lower = raw.toLowerCase().trim();

  // Compound value: contains "+" → multi-retailer
  if (lower.includes("+")) return RETAILER_MULTI;

  // Shufersal variants
  if (lower === "shufersal" || lower === "שופרסל") return RETAILER_SHUFERSAL;

  // Yohananof / Yochananof spelling variants
  if (lower === "yohananof" || lower === "yochananof" || lower === "יוחננוף")
    return RETAILER_YOHANANOF;

  return RETAILER_OTHER;
}
