/**
 * Admin blog editor — prose extraction over blog article JSON.
 *
 * Blog article text lives in src/data/blog/*.json (migrated from the old
 * *-content.ts modules, TASK-350). Unlike the comparison pages, blog docs have
 * a free-form nested shape, so instead of a fixed field list we walk the doc and
 * expose every *Hebrew* prose string — that single heuristic naturally excludes
 * URLs, slugs, ids, English citation text, and config tokens (all ASCII).
 *
 * Prose-only by design: we never expose links/slugs/ids, and we skip whole
 * subtrees that are references or config (citations, charts, presets, maps).
 */
import type { EditableField } from "@/lib/admin/fields";

export interface BlogDoc {
  slug: string; // unique editor id, e.g. "hummus"
  file: string; // filename under src/data/blog/
  labelHe: string; // sidebar label
  route: string; // live page, for reference
}

// Registry of editable blog docs. Add an entry when an article's prose is
// migrated to src/data/blog/<file>.json.
export const LIVE_BLOG_DOCS: BlogDoc[] = [
  { slug: "hummus", file: "hummus.json", labelHe: "בלוג — חומוס", route: "/blog/hummus" },
  { slug: "milk-analysis", file: "milk-analysis.json", labelHe: "בלוג — חלב", route: "/blog/milk-analysis" },
  { slug: "yogurt", file: "yogurt.json", labelHe: "בלוג — יוגורט", route: "/blog/yogurt" },
  { slug: "olive-oil", file: "olive-oil.json", labelHe: "בלוג — שמן זית", route: "/blog/shemen-zayit" },
  { slug: "bread-article", file: "bread-article.json", labelHe: "בלוג — לחם", route: "/blog/lechem" },
];

export const BLOG_DIR = "bari-web/src/data/blog";

export function blogDoc(slug: string): BlogDoc | undefined {
  return LIVE_BLOG_DOCS.find((d) => d.slug === slug);
}

// Scalar keys whose value is structural even if it contains Hebrew — never editable.
const EXCLUDE_KEYS = new Set([
  "slug", "href", "url", "id", "key", "category", "readTime", "cta",
  "comingSoon", "icon", "color", "variant", "accent", "tone", "date",
]);

// Subtrees we never descend into (references / config, not article prose).
const SKIP_SUBTREES = new Set([
  "citations", "links", "chart", "chartData", "presets", "enginePresets",
  "map", "blogMap", "categories",
]);

const HEBREW = /[֐-׿]/;

function isProseString(v: unknown): v is string {
  if (typeof v !== "string") return false;
  if (!HEBREW.test(v)) return false; // ASCII-only (urls, ids, English) → not prose
  const t = v.trim();
  if (t.startsWith("http") || t.startsWith("/") || t.startsWith("#")) return false;
  return true;
}

function isProseStringList(v: unknown): v is string[] {
  return Array.isArray(v) && v.length > 0 && v.every(isProseString);
}

/**
 * Recursively collect editable prose fields from a blog doc.
 * Paths are JSON-pointer-ish ("hero/title", "science/paragraphs"), unique and
 * stable for round-tripping through apply.
 */
export function extractProse(doc: unknown): EditableField[] {
  const out: EditableField[] = [];

  const walk = (node: unknown, path: string, keyName: string) => {
    if (isProseStringList(node)) {
      out.push({ path, label: labelFor(path, keyName), kind: "list", value: node });
      return;
    }
    if (isProseString(node)) {
      out.push({ path, label: labelFor(path, keyName), kind: "text", value: node });
      return;
    }
    if (Array.isArray(node)) {
      node.forEach((item, i) => {
        if (item && typeof item === "object") walk(item, `${path}/${i}`, keyName);
      });
      return;
    }
    if (node && typeof node === "object") {
      for (const [k, v] of Object.entries(node as Record<string, unknown>)) {
        if (EXCLUDE_KEYS.has(k) || SKIP_SUBTREES.has(k)) continue;
        const childPath = path ? `${path}/${k}` : k;
        walk(v, childPath, k);
      }
    }
  };

  walk(doc, "", "");
  return out;
}

const KEY_LABELS: Record<string, string> = {
  title: "כותרת",
  subtitle: "כותרת משנה",
  eyebrow: "תווית עליונה",
  meta: "מטא",
  disclaimer: "הסתייגות",
  lead: "פתיח",
  paragraphs: "פסקאות",
  editorialInsights: "תובנות",
  finding: "ממצא",
  whyItMatters: "למה זה חשוב",
  quote: "ציטוט",
  summary: "סיכום",
  synthesis: "סינתזה",
  intro: "מבוא",
  takeaway: "שורה תחתונה",
  description: "תיאור",
};

function labelFor(path: string, keyName: string): string {
  const base = KEY_LABELS[keyName] ?? keyName;
  // append a short path hint so repeated keys are distinguishable
  return `${base}  ·  ${path}`;
}

function getByPath(doc: Record<string, unknown>, path: string): unknown {
  const parts = path.split("/");
  let cur: unknown = doc;
  for (const p of parts) {
    if (cur == null) return undefined;
    if (Array.isArray(cur)) cur = cur[Number(p)];
    else if (typeof cur === "object") cur = (cur as Record<string, unknown>)[p];
    else return undefined;
  }
  return cur;
}

function setByPath(doc: Record<string, unknown>, path: string, value: unknown): boolean {
  const parts = path.split("/");
  let cur: unknown = doc;
  for (let i = 0; i < parts.length - 1; i++) {
    if (cur == null) return false;
    const p = parts[i];
    cur = Array.isArray(cur) ? cur[Number(p)] : (cur as Record<string, unknown>)[p];
  }
  if (cur == null || typeof cur !== "object") return false;
  const last = parts[parts.length - 1];
  if (Array.isArray(cur)) cur[Number(last)] = value;
  else (cur as Record<string, unknown>)[last] = value;
  return true;
}

export interface ProseEditResult {
  applied: number;
  rejected: string[];
}

/**
 * Apply prose edits to a blog doc IN PLACE. Only paths that the extractor would
 * expose (i.e. existing Hebrew-prose fields of matching shape) are written;
 * anything else is rejected — so a crafted edit can't add keys or touch links.
 */
export function applyProse(
  doc: Record<string, unknown>,
  edits: Record<string, unknown>,
): ProseEditResult {
  const allowed = new Map(extractProse(doc).map((f) => [f.path, f]));
  const result: ProseEditResult = { applied: 0, rejected: [] };

  for (const [path, raw] of Object.entries(edits)) {
    const field = allowed.get(path);
    if (!field) {
      result.rejected.push(path);
      continue;
    }
    if (field.kind === "list") {
      if (!Array.isArray(raw) || !raw.every((x) => typeof x === "string")) {
        result.rejected.push(path);
        continue;
      }
    } else if (typeof raw !== "string") {
      result.rejected.push(path);
      continue;
    }
    if (setByPath(doc, path, raw)) result.applied += 1;
    else result.rejected.push(path);
  }

  return result;
}

export { getByPath };
