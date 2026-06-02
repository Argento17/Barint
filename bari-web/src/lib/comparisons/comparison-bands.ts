// Score-band helpers for the unified comparison table (comparison-v2-spec §3/§4).
// Bands are derived from `score`, contiguous in corpus order. Used by the band rail
// (scroll-only jump targets) and the in-list dividers. Display-only — never reorders.

import type { BariProductVM } from "@/lib/view-models";

export interface ScoreBand {
  id: string;
  /** Hebrew label shown on the rail and the in-list divider. */
  label: string;
  min: number;
  max: number;
  /** green → amber as the band drops (calm, never red). */
  tone: string;
}

// 80+ · 70–79 · 60–69 · 50–59 · <50 (README §5 / spec §3).
export const SCORE_BANDS: readonly ScoreBand[] = [
  { id: "b80", label: "80+", min: 80, max: Infinity, tone: "#1F8F6A" },
  { id: "b70", label: "70–79", min: 70, max: 79, tone: "#3FA07E" },
  { id: "b60", label: "60–69", min: 60, max: 69, tone: "#9A9A5E" },
  { id: "b50", label: "50–59", min: 50, max: 59, tone: "#C49A4A" },
  { id: "b00", label: "מתחת ל-50", min: 0, max: 49, tone: "#C77F5A" },
];

const UNSCORED_BAND: ScoreBand = {
  id: "bnull",
  label: "ללא ציון",
  min: -Infinity,
  max: -Infinity,
  tone: "#B5BBB6",
};

/** The band a score falls into. `null` (unscored / insufficient) → its own trailing band. */
export function bandOf(score: number | null): ScoreBand {
  if (score == null) return UNSCORED_BAND;
  return SCORE_BANDS.find((b) => score >= b.min && score <= b.max) ?? UNSCORED_BAND;
}

export interface RailBand extends ScoreBand {
  count: number;
  /** id of the first product in this band, in corpus order — the scroll target. */
  firstProductId: string;
}

/**
 * Bands actually present in this product list, in corpus order, with counts and the
 * first product id per band. Empty bands are omitted. Drives the rail.
 */
export function railBandsFor(products: readonly BariProductVM[]): RailBand[] {
  const order: ScoreBand[] = [...SCORE_BANDS, UNSCORED_BAND];
  const out: RailBand[] = [];
  for (const band of order) {
    const inBand = products.filter((p) => bandOf(p.score).id === band.id);
    if (inBand.length === 0) continue;
    out.push({ ...band, count: inBand.length, firstProductId: inBand[0].id });
  }
  return out;
}
