/** Centralized numeric display — no raw floating-point artifacts in UI */

function cleanFloat(value: number, maxDecimals: number): number {
  const factor = 10 ** maxDecimals;
  return Math.round(value * factor) / factor;
}

export function formatScore(value: number | string | null | undefined): string {
  if (value == null || value === "") return "—";
  const n = typeof value === "number" ? value : Number(value);
  if (!Number.isFinite(n)) return "—";
  return String(Math.round(n));
}

export function formatIngredientCount(value: number | null | undefined): string {
  if (value == null || !Number.isFinite(value)) return "—";
  return String(Math.round(value));
}

export function formatGram(value: number | null | undefined, unit = " ג׳"): string {
  if (value == null || !Number.isFinite(value)) return "לא מוצהר";
  const rounded = cleanFloat(value, 1);
  if (Number.isInteger(rounded)) return `${rounded}${unit}`;
  return `${rounded.toFixed(1)}${unit}`;
}

export function formatPercent(value: number | null | undefined): string {
  if (value == null || !Number.isFinite(value)) return "—";
  const rounded = cleanFloat(value, 1);
  if (Number.isInteger(rounded)) return `${rounded}%`;
  return `${rounded.toFixed(1)}%`;
}

export function formatDecimal(
  value: number | null | undefined,
  maxDecimals = 1
): string {
  if (value == null || !Number.isFinite(value)) return "—";
  const rounded = cleanFloat(value, maxDecimals);
  if (Number.isInteger(rounded)) return String(rounded);
  return rounded.toFixed(maxDecimals);
}
