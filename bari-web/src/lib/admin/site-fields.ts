/**
 * Generic JSON string field extract/apply for site-content admin.
 */

export type SiteFieldKind = "text" | "list";

export interface SiteEditableField {
  path: string;
  label: string;
  kind: SiteFieldKind;
  value: string | string[];
}

export interface SiteEditResult {
  applied: number;
  rejected: string[];
}

function isStr(v: unknown): v is string {
  return typeof v === "string";
}

function isStrList(v: unknown): v is string[] {
  return Array.isArray(v) && v.every((x) => typeof x === "string");
}

function readAt(obj: Record<string, unknown>, path: string): unknown {
  const parts = path.split(".");
  let cur: unknown = obj;
  for (const part of parts) {
    if (cur == null || typeof cur !== "object") return undefined;
    cur = (cur as Record<string, unknown>)[part];
  }
  return cur;
}

function writeAt(obj: Record<string, unknown>, path: string, value: string | string[]): void {
  const parts = path.split(".");
  let cur: Record<string, unknown> = obj;
  for (let i = 0; i < parts.length - 1; i++) {
    const key = parts[i];
    if (!cur[key] || typeof cur[key] !== "object") cur[key] = {};
    cur = cur[key] as Record<string, unknown>;
  }
  cur[parts[parts.length - 1]] = value;
}

export function extractSiteFields(
  data: Record<string, unknown>,
  labels: Record<string, string> = {},
  prefix = "",
): SiteEditableField[] {
  const out: SiteEditableField[] = [];
  for (const [key, value] of Object.entries(data)) {
    const pathKey = prefix ? `${prefix}.${key}` : key;
    if (isStr(value)) {
      out.push({ path: pathKey, label: labels[pathKey] ?? pathKey, kind: "text", value });
    } else if (isStrList(value)) {
      out.push({ path: pathKey, label: labels[pathKey] ?? pathKey, kind: "list", value });
    } else if (value && typeof value === "object" && !Array.isArray(value)) {
      out.push(...extractSiteFields(value as Record<string, unknown>, labels, pathKey));
    }
  }
  return out.sort((a, b) => a.path.localeCompare(b.path));
}

export function applySiteEdits(
  data: Record<string, unknown>,
  edits: Record<string, unknown>,
  allowed?: Set<string>,
): SiteEditResult {
  const result: SiteEditResult = { applied: 0, rejected: [] };
  for (const [pathKey, raw] of Object.entries(edits)) {
    if (allowed && !allowed.has(pathKey)) {
      result.rejected.push(pathKey);
      continue;
    }
    const current = readAt(data, pathKey);
    if (isStrList(current)) {
      if (!isStrList(raw)) {
        result.rejected.push(pathKey);
        continue;
      }
    } else if (isStr(current)) {
      if (!isStr(raw)) {
        result.rejected.push(pathKey);
        continue;
      }
    } else {
      result.rejected.push(pathKey);
      continue;
    }
    writeAt(data, pathKey, raw);
    result.applied += 1;
  }
  return result;
}

const PAGE_CHROME_LABELS: Record<string, string> = {
  "hero.eyebrow": "כותרת על",
  "hero.title": "כותרת ראשית",
  "categoryNote": "הערת קטגוריה",
  "metadata.title": "כותרת SEO",
  "metadata.description": "תיאור SEO",
  "prologue": "פתיח (משפטים)",
  "methodology": "מתודולוגיה (שורות)"
};

export function extractPageChromeFields(chrome: Record<string, unknown>): SiteEditableField[] {
  const fields: SiteEditableField[] = [];
  const hero = chrome.hero;
  if (hero && typeof hero === "object") {
    fields.push(...extractSiteFields({ hero }, PAGE_CHROME_LABELS));
  }
  const meta = chrome.metadata;
  if (meta && typeof meta === "object") {
    fields.push(...extractSiteFields({ metadata: meta }, PAGE_CHROME_LABELS));
  }
  if (isStr(chrome.categoryNote)) {
    fields.push({
      path: "categoryNote",
      label: PAGE_CHROME_LABELS.categoryNote,
      kind: "text",
      value: chrome.categoryNote,
    });
  }
  if (isStrList(chrome.prologue)) {
    fields.push({
      path: "prologue",
      label: PAGE_CHROME_LABELS.prologue,
      kind: "list",
      value: chrome.prologue,
    });
  }
  if (isStrList(chrome.methodology)) {
    fields.push({
      path: "methodology",
      label: PAGE_CHROME_LABELS.methodology,
      kind: "list",
      value: chrome.methodology,
    });
  }
  return fields;
}
