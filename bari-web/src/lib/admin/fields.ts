/**
 * Admin copy editor — editable-field whitelist + extract/apply.
 *
 * SECURITY CORE. This module is the single definition of what the admin editor
 * may touch. Only carry-safe *copy* fields appear here. Scores, grades,
 * nutrition, confidence, retailer and every other structural/derived field are
 * intentionally absent, so they can never be edited from the panel.
 *
 * "Carry-safe" = the field is treated as copy by the score-switch copy stage
 * (03_operations/page_generator/copy_stage.py), so an edited value is carried
 * forward on the next re-score for grade-unchanged products. We deliberately
 * exclude fields copy_stage treats as structural (e.g. servingNote,
 * positiveSignals, limitingFactors) — editing those would be overwritten by the
 * engine on the next rescore.
 */

// Live category -> live comparison JSON file.
// Derived from the `*-page-data.ts` imports under src/lib/comparisons/ (the
// authoritative "what is live" mapping). Regenerate with:
//   grep -rn "data/comparisons/.*\.json" src/lib/comparisons
export const LIVE_COMPARISON_FILES: Record<string, string> = {
  bread: "bread_frontend_v3.json",
  brined_cheeses: "brined_cheeses_frontend_v2.json",
  cakes_hard_cookies: "cakes_hard_cookies_frontend_v1.json",
  cereals: "cereals_frontend_v2.json",
  cheese: "cheese_frontend_v4.json",
  cookies_coffee: "cookies_coffee_frontend_v2.json",
  granola: "granola_frontend_v1.json",
  hard_cheeses: "hard_cheeses_frontend_v2.json",
  hummus: "hummus_frontend_v5.json",
  juices: "juices_frontend_v3.json",
  milk: "milk_frontend_v1.json",
  snacks: "snacks_frontend_v5.json",
  protein_bars: "protein_bars_frontend_v1.json",
};

// Top-level single-string copy fields.
const TEXT_FIELDS_TOP = [
  "insightLine",
  "rowVerdict",
  "consumerTakeaway",
  "consumerExplanation",
] as const;

// Top-level list-of-strings copy fields.
const LIST_FIELDS_TOP = ["bestUseCases"] as const;

// expansion.* single-string copy fields.
const TEXT_FIELDS_EXP = [
  "comparisonContext",
  "consumerExplanation",
  "bottomLine",
] as const;

// expansion.* list-of-strings copy fields.
const LIST_FIELDS_EXP = ["caveats", "unknowns"] as const;

// Hebrew labels shown in the editor.
const LABELS: Record<string, string> = {
  insightLine: "שורת תובנה",
  rowVerdict: "שורת שיפוט (שורה מכווצת)",
  consumerTakeaway: "שורה תחתונה לצרכן",
  consumerExplanation: "הסבר לצרכן",
  bestUseCases: "שימושים מומלצים",
  "expansion.comparisonContext": "הקשר השוואתי",
  "expansion.consumerExplanation": "הסבר לצרכן (מורחב)",
  "expansion.bottomLine": "שורה תחתונה",
  "expansion.caveats": "הסתייגויות",
  "expansion.unknowns": "מה לא ידוע",
  bariInterpretation: "פרשנות Bari",
};

export type FieldKind = "text" | "list";

export interface EditableField {
  /** Stable, unique path within the product, e.g. "insightLine",
   *  "expansion.caveats", "bariInterpretation.0.interpretation". */
  path: string;
  label: string;
  kind: FieldKind;
  value: string | string[];
}

function isStr(v: unknown): v is string {
  return typeof v === "string";
}

function isStrList(v: unknown): v is string[] {
  return Array.isArray(v) && v.every((x) => typeof x === "string");
}

/**
 * Compute the set of editable paths that actually exist on this product.
 * Both extract (read) and apply (write) go through this, so the editor can
 * never read or write a path outside the whitelist.
 */
export function allowedPaths(product: Record<string, unknown>): Set<string> {
  const paths = new Set<string>();

  for (const f of TEXT_FIELDS_TOP) {
    if (isStr(product[f])) paths.add(f);
  }
  for (const f of LIST_FIELDS_TOP) {
    if (isStrList(product[f])) paths.add(f);
  }

  const exp = product.expansion;
  if (exp && typeof exp === "object") {
    const e = exp as Record<string, unknown>;
    for (const f of TEXT_FIELDS_EXP) {
      if (isStr(e[f])) paths.add(`expansion.${f}`);
    }
    for (const f of LIST_FIELDS_EXP) {
      if (isStrList(e[f])) paths.add(`expansion.${f}`);
    }
  }

  // bariInterpretation: list of { interpretation: string, ... }
  const bi = product.bariInterpretation;
  if (Array.isArray(bi)) {
    bi.forEach((item, i) => {
      if (item && typeof item === "object" && isStr((item as Record<string, unknown>).interpretation)) {
        paths.add(`bariInterpretation.${i}.interpretation`);
      }
    });
  }

  return paths;
}

function labelFor(path: string, product: Record<string, unknown>): string {
  if (LABELS[path]) return LABELS[path];
  const m = path.match(/^bariInterpretation\.(\d+)\.interpretation$/);
  if (m) {
    const idx = Number(m[1]);
    const bi = product.bariInterpretation;
    if (Array.isArray(bi) && bi[idx] && typeof bi[idx] === "object") {
      const item = bi[idx] as Record<string, unknown>;
      const key = (item.label || item.key || item.dimension) as string | undefined;
      return key ? `פרשנות Bari — ${key}` : "פרשנות Bari";
    }
    return "פרשנות Bari";
  }
  return path;
}

function readPath(product: Record<string, unknown>, path: string): string | string[] | undefined {
  if (path.startsWith("expansion.")) {
    const exp = product.expansion as Record<string, unknown> | undefined;
    return exp?.[path.slice("expansion.".length)] as string | string[] | undefined;
  }
  const m = path.match(/^bariInterpretation\.(\d+)\.interpretation$/);
  if (m) {
    const bi = product.bariInterpretation as unknown[] | undefined;
    const item = bi?.[Number(m[1])] as Record<string, unknown> | undefined;
    return item?.interpretation as string | undefined;
  }
  return product[path] as string | string[] | undefined;
}

/** Ordered list of editable fields present on a product. */
export function extractEditableFields(product: Record<string, unknown>): EditableField[] {
  const fields: EditableField[] = [];
  for (const path of allowedPaths(product)) {
    const value = readPath(product, path);
    if (value === undefined) continue;
    fields.push({
      path,
      label: labelFor(path, product),
      kind: Array.isArray(value) ? "list" : "text",
      value,
    });
  }
  // Stable ordering: top-level first, then expansion, then interpretation.
  const rank = (p: string) =>
    p.startsWith("bariInterpretation") ? 2 : p.startsWith("expansion.") ? 1 : 0;
  return fields.sort((a, b) => rank(a.path) - rank(b.path) || a.path.localeCompare(b.path));
}

export interface EditResult {
  applied: number;
  rejected: string[];
}

/**
 * Apply edits to one product IN PLACE, but only for whitelisted paths that
 * already exist and whose value type matches. Any path outside the whitelist —
 * including any score/grade/nutrition path — is rejected, never written.
 */
export function applyEdits(
  product: Record<string, unknown>,
  edits: Record<string, unknown>,
): EditResult {
  const allowed = allowedPaths(product);
  const result: EditResult = { applied: 0, rejected: [] };

  for (const [path, raw] of Object.entries(edits)) {
    if (!allowed.has(path)) {
      result.rejected.push(path);
      continue;
    }
    const current = readPath(product, path);
    const expectsList = Array.isArray(current);

    if (expectsList) {
      if (!isStrList(raw)) {
        result.rejected.push(path);
        continue;
      }
    } else if (!isStr(raw)) {
      result.rejected.push(path);
      continue;
    }

    writePath(product, path, raw as string | string[]);
    result.applied += 1;
  }

  return result;
}

function writePath(
  product: Record<string, unknown>,
  path: string,
  value: string | string[],
): void {
  if (path.startsWith("expansion.")) {
    const exp = (product.expansion ?? {}) as Record<string, unknown>;
    exp[path.slice("expansion.".length)] = value;
    product.expansion = exp;
    return;
  }
  const m = path.match(/^bariInterpretation\.(\d+)\.interpretation$/);
  if (m) {
    const bi = product.bariInterpretation as Record<string, unknown>[] | undefined;
    const item = bi?.[Number(m[1])];
    if (item) item.interpretation = value;
    return;
  }
  product[path] = value;
}
