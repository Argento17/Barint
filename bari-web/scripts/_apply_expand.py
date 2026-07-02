from pathlib import Path
import json, re

ROOT = Path(r"c:/Bari/bari-web")

def write(rel, content):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print("wrote", rel)

# ========== fields.ts ==========
fields = (ROOT / "src/lib/admin/fields.ts").read_text(encoding="utf-8")
live_lines = [
  "export const LIVE_COMPARISON_FILES: Record<string, string> = {",
  '  bread: "bread_frontend_v3.json",',
  '  brined_cheeses: "brined_cheeses_frontend_v2.json",',
  '  cakes_hard_cookies: "cakes_hard_cookies_frontend_v1.json",',
  '  cereals: "cereals_frontend_v2.json",',
  '  cheese: "cheese_frontend_v4.json",',
  '  chocolate_bars: "chocolate_bars_frontend_v1.json",',
  '  chocolate_tablets: "chocolate_tablets_frontend_v1.json",',
  '  cookies_coffee: "cookies_coffee_frontend_v2.json",',
  '  granola: "granola_frontend_v1.json",',
  '  hard_cheeses: "hard_cheeses_frontend_v2.json",',
  '  hummus: "hummus_frontend_v5.json",',
  '  juices: "juices_frontend_v3.json",',
  '  milk: "milk_frontend_v1.json",',
  '  protein_bars: "protein_combined_frontend_v2.json",',
  '  snacks: "snacks_frontend_v5.json",',
  "};",
]
live = "\n".join(live_lines)
fields = re.sub(r"export const LIVE_COMPARISON_FILES:[\s\S]*?};", live, fields, count=1)
write("src/lib/admin/fields.ts", fields)

print("fields ok")
from pathlib import Path
import json, re

ROOT = Path(r"c:/Bari/bari-web")

def write(rel, content):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print("wrote", rel)

# ========== content-registry.ts ==========
write("src/lib/admin/content-registry.ts", """import { LIVE_COMPARISON_FILES } from \"./fields\";

export const PAGE_CHROME_FILE = \"comparison-pages.json\";

export type SiteContentKind = \"site\" | \"page_chrome\";

export interface SiteContentEntry {
  id: string;
  file: string;
  labelHe: string;
  kind: SiteContentKind;
}

export const SITE_CONTENT_ENTRIES: SiteContentEntry[] = [
  {
    id: \"hashvaot-hub\",
    file: \"hashvaot-hub.json\",
    labelHe: \"דף השוואות (מרכז)\",
    kind: \"site\",
  },
  {
    id: \"hashvaot-categories\",
    file: \"hashvaot-categories.json\",
    labelHe: \"קטגוריות השוואה\",
    kind: \"site\",
  },
  {
    id: \"homepage-marketing\",
    file: \"homepage-marketing.json\",
    labelHe: \"דף הבית — שיווק\",
    kind: \"site\",
  },
  {
    id: \"page-chrome\",
    file: PAGE_CHROME_FILE,
    labelHe: \"כותרות עמודי השוואה (לפי קטגוריה)\",
    kind: \"page_chrome\",
  },
];

export interface ComparisonRegistryEntry {
  slug: string;
  file: string;
}

/** Live comparison categories (product copy JSON). */
export function listComparisonEntries(): ComparisonRegistryEntry[] {
  return Object.entries(LIVE_COMPARISON_FILES)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([slug, file]) => ({ slug, file }));
}

export function getSiteContentEntry(id: string): SiteContentEntry | undefined {
  return SITE_CONTENT_ENTRIES.find((entry) => entry.id === id);
}

export function siteContentFileForId(id: string): string | undefined {
  return getSiteContentEntry(id)?.file;
}
""")

# ========== site-fields.ts ==========
write("src/lib/admin/site-fields.ts", """/**
 * Generic JSON copy editor for site-content blobs (flat string + string[] fields).
 */

export type SiteFieldKind = \"text\" | \"list\";

export interface SiteField {
  path: string;
  label: string;
  kind: SiteFieldKind;
  value: string | string[];
}

export interface SiteEditResult {
  applied: number;
  rejected: string[];
}

const PATH_LABELS: Record<string, string> = {
  \"metadata.title\": \"כותרת SEO\",
  \"metadata.description\": \"תיאור SEO\",
  \"hero.eyebrow\": \"כותרת משנה (eyebrow)\",
  \"hero.title\": \"כותרת ראשית\",
  \"categoryNote\": \"הערת קטגוריה\",
  \"eyebrowEn\": \"Eyebrow (EN)\",
  \"title\": \"כותרת\",
  \"subtitle\": \"תת-כותרת\",
  \"body\": \"גוף\",
  \"backLink\": \"קישור חזרה\",
};

function isStr(v: unknown): v is string {
  return typeof v === \"string\";
}

function isStrList(v: unknown): v is string[] {
  return Array.isArray(v) && v.every((x) => typeof x === \"string\");
}

function labelFor(path: string): string {
  if (PATH_LABELS[path]) return PATH_LABELS[path];
  if (path.startsWith(\"prologue.\")) return `פתיחה — פסקה ${Number(path.split(\".\")[1]) + 1}`;
  if (path.startsWith(\"methodology.\")) return `מתודולוגיה — שורה ${Number(path.split(\".\")[1]) + 1}`;
  if (path.startsWith(\"trust.items.\")) {
    const m = path.match(/^trust\\.items\\.(\\d+)\\.(title|text)$/);
    if (m) return m[2] === \"title\" ? `אמון #${Number(m[1]) + 1} — כותרת` : `אמון #${Number(m[1]) + 1} — טקסט`;
  }
  if (path.startsWith(\"categories.\")) {
    const m = path.match(/^categories\\.(\\d+)\\.(title|description|countLabel|comingSoonSubtext)$/);
    if (m) {
      const field = m[2];
      const idx = Number(m[1]) + 1;
      const map: Record<string, string> = {
        title: \"כותרת\",
        description: \"תיאור\",
        countLabel: \"תווית מונה\",
        comingSoonSubtext: \"טקסט בקרוב\",
      };
      return `קטגוריה ${idx} — ${map[field] ?? field}`;
    }
  }
  return path;
}

function readAt(root: unknown, path: string): unknown {
  const parts = path.split(\".\");
  let cur: unknown = root;
  for (const part of parts) {
    if (cur === null || cur === undefined) return undefined;
    if (/^\\d+$/.test(part)) {
      if (!Array.isArray(cur)) return undefined;
      cur = cur[Number(part)];
      continue;
    }
    if (typeof cur !== \"object\") return undefined;
    cur = (cur as Record<string, unknown>)[part];
  }
  return cur;
}

function writeAt(root: Record<string, unknown>, path: string, value: string | string[]): void {
  const parts = path.split(\".\");
  let cur: Record<string, unknown> | unknown[] = root;
  for (let i = 0; i < parts.length - 1; i++) {
    const part = parts[i];
    const nextPart = parts[i + 1];
    if (/^\\d+$/.test(part)) {
      const idx = Number(part);
      if (!Array.isArray(cur)) throw new Error(\"invalid path\");
      if (cur[idx] === undefined) {
        cur[idx] = /^\\d+$/.test(nextPart) ? [] : {};
      }
      cur = cur[idx] as Record<string, unknown> | unknown[];
      continue;
    }
    const obj = cur as Record<string, unknown>;
    if (obj[part] === undefined) {
      obj[part] = /^\\d+$/.test(nextPart) ? [] : {};
    }
    cur = obj[part] as Record<string, unknown> | unknown[];
  }
  const last = parts[parts.length - 1];
  if (/^\\d+$/.test(last)) {
    (cur as unknown[])[Number(last)] = value;
    return;
  }
  (cur as Record<string, unknown>)[last] = value;
}

/** Walk JSON and collect editable string / string[] leaf paths. */
export function extractSiteFields(data: unknown, options?: { prefix?: string; skipKeys?: Set<string> }): SiteField[] {
  const skip = options?.skipKeys ?? new Set([\"id\", \"href\", \"accent\", \"status\", \"heroStat\"]);
  const fields: SiteField[] = [];

  function walk(node: unknown, prefix: string): void {
    if (isStr(node)) {
      if (prefix) fields.push({ path: prefix, label: labelFor(prefix), kind: \"text\", value: node });
      return;
    }
    if (isStrList(node)) {
      if (prefix) fields.push({ path: prefix, label: labelFor(prefix), kind: \"list\", value: node });
      return;
    }
    if (Array.isArray(node)) {
      node.forEach((item, index) => {
        const p = prefix ? `${prefix}.${index}` : String(index);
        walk(item, p);
      });
      return;
    }
    if (node && typeof node === \"object\") {
      for (const [key, val] of Object.entries(node as Record<string, unknown>)) {
        if (!prefix && skip.has(key)) continue;
        const p = prefix ? `${prefix}.${key}` : key;
        if (typeof val === \"object\" && val !== null && !Array.isArray(val)) {
          walk(val, p);
        } else {
          walk(val, p);
        }
      }
    }
  }

  walk(data, options?.prefix ?? \"\");
  return fields.sort((a, b) => a.path.localeCompare(b.path));
}

export function extractPageChromeFields(slug: string, chrome: Record<string, unknown>): SiteField[] {
  const fields = extractSiteFields(chrome);
  return fields.map((f) => ({
    ...f,
    label: f.path.startsWith(\"hero.\") || f.path.startsWith(\"metadata.\") ? f.label : `[${slug}] ${f.label}`,
  }));
}

export function applySiteEdits(
  data: Record<string, unknown>,
  edits: Record<string, unknown>,
): SiteEditResult {
  const allowed = new Set(extractSiteFields(data).map((f) => f.path));
  const result: SiteEditResult = { applied: 0, rejected: [] };

  for (const [path, raw] of Object.entries(edits)) {
    if (!allowed.has(path)) {
      result.rejected.push(path);
      continue;
    }
    const current = readAt(data, path);
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
    writeAt(data, path, raw as string | string[]);
    result.applied += 1;
  }

  return result;
}
""")

print("registry + site-fields ok")
# ========== github.ts ==========
write("src/lib/admin/github.ts", """/**
 * Admin copy editor — GitHub read/write for comparison + site-content JSON.
 */

const API = \"https://api.github.com\";
const COMPARISONS_DIR = \"bari-web/src/data/comparisons\";
const SITE_CONTENT_DIR = \"bari-web/src/data/site-content\";

function cfg() {
  const token = process.env.ADMIN_GITHUB_TOKEN || \"\";
  const repo = process.env.ADMIN_GITHUB_REPO || \"Argento17/Barint\";
  const branch = process.env.ADMIN_GITHUB_BRANCH || \"master\";
  return { token, repo, branch };
}

export function githubConfigured(): boolean {
  return Boolean(process.env.ADMIN_GITHUB_TOKEN);
}

async function gh(path: string, init?: RequestInit): Promise<Response> {
  const { token } = cfg();
  return fetch(`${API}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: \"application/vnd.github+json\",
      \"X-GitHub-Api-Version\": \"2022-11-28\",
      \"User-Agent\": \"bari-admin-copy-editor\",
      ...(init?.headers || {}),
    },
    cache: \"no-store\",
  });
}

export interface FetchedFile<T = unknown> {
  data: T;
  sha: string;
}

export async function getRepoFileAt<T = unknown>(dir: string, file: string): Promise<FetchedFile<T>> {
  const { repo, branch } = cfg();
  const res = await gh(
    `/repos/${repo}/contents/${dir}/${encodeURIComponent(file)}?ref=${encodeURIComponent(branch)}`,
  );
  if (!res.ok) {
    throw new Error(`GitHub getFile ${dir}/${file} failed: ${res.status} ${await res.text()}`);
  }
  const body = (await res.json()) as { content: string; sha: string; encoding: string };
  const raw = Buffer.from(body.content, body.encoding === \"base64\" ? \"base64\" : \"utf8\").toString(\"utf8\");
  return { data: JSON.parse(raw) as T, sha: body.sha };
}

export async function putRepoFileAt(
  dir: string,
  file: string,
  data: unknown,
  sha: string,
  message: string,
): Promise<{ commitSha: string }> {
  const { repo, branch } = cfg();
  const text = JSON.stringify(data, null, 2);
  const res = await gh(`/repos/${repo}/contents/${dir}/${encodeURIComponent(file)}`, {
    method: \"PUT\",
    body: JSON.stringify({
      message,
      content: Buffer.from(text, \"utf8\").toString(\"base64\"),
      sha,
      branch,
    }),
  });
  if (!res.ok) {
    throw new Error(`GitHub putFile ${dir}/${file} failed: ${res.status} ${await res.text()}`);
  }
  const body = (await res.json()) as { commit: { sha: string } };
  return { commitSha: body.commit.sha };
}

export type ComparisonFileData = {
  _meta?: Record<string, unknown>;
  products?: Record<string, unknown>[];
};

export async function getComparisonFile(file: string): Promise<FetchedFile<ComparisonFileData>> {
  return getRepoFileAt<ComparisonFileData>(COMPARISONS_DIR, file);
}

export async function putComparisonFile(
  file: string,
  data: unknown,
  sha: string,
  message: string,
): Promise<{ commitSha: string }> {
  return putRepoFileAt(COMPARISONS_DIR, file, data, sha, message);
}

export async function getSiteContentFile<T = Record<string, unknown>>(file: string): Promise<FetchedFile<T>> {
  return getRepoFileAt<T>(SITE_CONTENT_DIR, file);
}

export async function putSiteContentFile(
  file: string,
  data: unknown,
  sha: string,
  message: string,
): Promise<{ commitSha: string }> {
  return putRepoFileAt(SITE_CONTENT_DIR, file, data, sha, message);
}
""")

# ========== comparison-page-chrome.ts ==========
write("src/lib/site-content/comparison-page-chrome.ts", """import type { Metadata } from \"next\";

import comparisonPages from \"@/data/site-content/comparison-pages.json\";

export interface ComparisonPageChrome {
  hero: { eyebrow: string; title: string };
  prologue: readonly string[];
  methodology: readonly string[];
  categoryNote: string;
  metadata: Metadata;
}

type RawEntry = {
  hero: { eyebrow: string; title: string };
  prologue: string[];
  methodology: string[];
  categoryNote?: string;
  metadata: { title: string; description: string };
};

const PAGES = comparisonPages as Record<string, RawEntry>;

export function listComparisonChromeSlugs(): string[] {
  return Object.keys(PAGES).sort();
}

export function getComparisonPageChrome(slug: string): ComparisonPageChrome {
  const entry = PAGES[slug];
  if (!entry) {
    throw new Error(`Unknown comparison page chrome slug: ${slug}`);
  }
  return {
    hero: entry.hero,
    prologue: entry.prologue,
    methodology: entry.methodology,
    categoryNote: entry.categoryNote ?? \"\",
    metadata: entry.metadata,
  };
}
""")

print("github + chrome ok")
# ========== site content JSON ==========
hub = {
  "metadata": {
    "title": "השוואות | Bari",
    "description": "השוואות אינטראקטיביות מהמדף — מזון, תוספים ועוד. ניתוח רב-פרמטרי של מוצרים דומים.",
  },
  "eyebrowEn": "Bari comparisons",
  "title": "השוואות מהמדף",
  "subtitle": "בארי בודקת מוצרים אמיתיים מהסופרמרקט ובתי המרקחת כדי לתת לכם חווית השוואה אינטראקטיבית בין מוצרים. כל דף השוואה בוחן מוצרים דומים לפי פרמטרים מוגדרים מראש על ידי אלגוריתם מכונה לומדת ומציג חסרונות ויתרונות בהקשר הנכון.",
  "backLink": "חזרה לדף הבית",
}
write("src/data/site-content/hashvaot-hub.json", json.dumps(hub, ensure_ascii=False, indent=2) + "\n")

categories = {
  "comingSoonSubtextByCategory": {
    "raw-foods": "ירקות, פירות, דגנים וקטניות — לפני שמישהו אורז אותם.",
    "personal-care": "קרמים, שמפו ומוצרי טיפוח — ניתוח מרכיבים ותוויות, כמו בכל קטגוריה אחרת.",
  },
  "categories": [
    {
      "id": "supermarket",
      "title": "מוצרי סופרמרקט אמיתיים",
      "status": "live",
      "countLabel": "16 השוואות",
      "href": "/hashvaot/supermarket",
      "description": "חלב, לחם, חטיפים, עוגות, גבינות ועוד",
      "accent": "#BC6A33",
      "heroStat": {"value": "16", "label": "השוואות פעילות"},
    },
    {
      "id": "supplements",
      "title": "תוספי תזונה",
      "status": "live",
      "countLabel": "1 השוואה",
      "href": "/hashvaot/supplements",
      "description": "תוספי תזונה מנותחים באופן שונה ממוצרי מזון — ספיגה, אפקטיביות ועוד",
      "accent": "#4A7B8C",
      "heroStat": {"value": "1", "label": "השוואות פעילות"},
    },
    {
      "id": "raw-foods",
      "title": "מזון גולמי",
      "status": "building",
      "href": "/hashvaot/raw-foods",
      "comingSoonSubtext": "ירקות, פירות, דגנים וקטניות — לפני שמישהו אורז אותם.",
      "accent": "#7A8C5E",
    },
    {
      "id": "personal-care",
      "title": "טיפוח אישי",
      "status": "building",
      "href": "/hashvaot/personal-care",
      "comingSoonSubtext": "קרמים, שמפו ומוצרי טיפוח — ניתוח מרכיבים ותוויות, כמו בכל קטגוריה אחרת.",
      "accent": "#8B7BA8",
    },
  ],
}
write("src/data/site-content/hashvaot-categories.json", json.dumps(categories, ensure_ascii=False, indent=2) + "\n")

homepage = {
  "hero": {
    "badge": "ניתוח מוצרים · המדף הישראלי",
    "titleLine1": "Bari מנתחת מוצרי מזון",
    "titleLine2": "ומזהה את מה שחשוב באמת",
    "subtitle": "מנוע השוואה שמפרק מוצרים דומים לפי רכיבים, עיבוד וערכים — כדי שתדעו מה באמת שונה בין האריזות.",
  },
  "trust": {
    "eyebrow": "שקיפות",
    "title": "עצמאית, אנליטית, ללא אג׳נדה שיווקית",
    "footer": "הנתונים נאספים ממקורות ציבוריים ומתוויות מוצר; הציון משקף את מודל Bari ואינו תחליף לייעוץ רפואי או תזונתי אישי.",
    "items": [
      {"title": "מידע, לא המלצה", "text": "Bari מפרקת מבנה ונתונים — לא אומרת מה «כדאי» לאכול."},
      {"title": "ציון Bari", "text": "מדד מבנה: רכיבים, עיבוד, תרומה תזונתית והקשר קטגוריאלי — בהשוואה למוצרים דומים."},
      {"title": "בלוג מול השוואה", "text": "הבלוג מספר סיפור עיתונאי; מנוע ההשוואה מציג את כל המוצרים בפירוט אינטראקטיבי."},
    ],
  },
  "comparisonsSection": {
    "title": "מוצרים שנראים דומים — לא תמיד אותו דבר",
    "subtitle": "חלב, לחם, גרנולה, דגנים — השוואות, ממצאים ופירוט מבני לפי קטגוריה.",
  },
  "methodologySection": {
    "eyebrow": "איך Bari מנתחת",
    "title": "ניתוח רב-ממדי של מספר רב של פרמטרים.",
    "subtitle": "Bari לא מסתמכת על מספר בודד. המערכת בוחנת רכיבים, עיבוד, צפיפות תזונתית והקשר קטגוריאלי — ומציגה את התמונה המלאה.",
  },
}
write("src/data/site-content/homepage-marketing.json", json.dumps(homepage, ensure_ascii=False, indent=2) + "\n")

cp = ROOT / "src/data/site-content/comparison-pages.json"
if cp.exists():
  print("comparison-pages.json present", cp.stat().st_size)
else:
  raise SystemExit("missing comparison-pages.json")

print("json ok")
PAGE_DATA = [
  ("bread-comparison-page-data.ts", "bread", "bread"),
  ("brined-cheeses-page-data.ts", "brined_cheeses", "brinedCheeses"),
  ("cakes-hard-cookies-page-data.ts", "cakes_hard_cookies", "cakesHardCookies"),
  ("cereals-page-data.ts", "cereals", "cereals"),
  ("cheese-page-data.ts", "cheese", "cheese"),
  ("chocolate-bars-comparison-page-data.ts", "chocolate_bars", "chocolateBars"),
  ("chocolate-tablets-comparison-page-data.ts", "chocolate_tablets", "chocolateTablets"),
  ("cookies-coffee-page-data.ts", "cookies_coffee", "cookiesCoffee"),
  ("granola-page-data.ts", "granola", "granola"),
  ("hard-cheeses-page-data.ts", "hard_cheeses", "hardCheeses"),
  ("hummus-comparison-page-data.ts", "hummus", "hummus"),
  ("juices-page-data.ts", "juices", "juices"),
  ("protein-bars-comparison-page-data.ts", "protein_bars", "proteinBars"),
  ("snacks-comparison-page-data.ts", "snacks", "snacks"),
]

def patch_page_data(content, slug, prefix):
    if "getComparisonPageChrome" in content:
        return content

    if not re.search(r'import type \{ Metadata \} from "next";', content):
        content = 'import type { Metadata } from "next";\n' + content
    if "getComparisonPageChrome" not in content:
        content = content.replace(
            'import type { Metadata } from "next";\n',
            'import type { Metadata } from "next";\n\nimport { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";\n',
            1,
        )

    # cheese: drop page_copy typing block
    content = re.sub(r"\ntype CheeseRaw[\s\S]*?;\n\nconst _typedRaw[\s\S]*?const _pageCopy = _typedRaw\.page_copy;\n\n", "\n", content)

    patterns = [
        rf"export const {prefix}Hero =[\s\S]*?\n;\n",
        rf"export const {prefix}Hero =[\s\S]*?;\n",
        rf"export const {prefix}PrologueSentences[\s\S]*?;\n",
        rf"export const {prefix}CategoryNote[\s\S]*?;\n",
        rf"export const {prefix}CategoryNote =[\s\S]*?\n  \.join\([^\)]*\);\n",
        rf"export const {prefix}MethodologyLines[\s\S]*?;\n",
        rf"export const {prefix}ComparisonMetadata: Metadata =[\s\S]*?}};\n",
    ]
    for pat in patterns:
        content = re.sub(pat, "", content)

    # remove blog imports only used for copy (best-effort)
    content = re.sub(r"import \{ breadComparisonMeta \} from \"@/lib/blog/bread-analysis-content\";\n", "", content)
    content = re.sub(r"import \{\n  snacksShelfMethodologyLines,\n  snackComparisonMeta,\n\} from \"@/lib/blog/snack-analysis-content\";\n", "", content)

    chrome_block = f"""
const _{prefix}PageChrome = getComparisonPageChrome(\"{slug}\");
export const {prefix}Hero = _{prefix}PageChrome.hero;
export const {prefix}PrologueSentences = _{prefix}PageChrome.prologue;
export const {prefix}MethodologyLines = _{prefix}PageChrome.methodology;
export const {prefix}CategoryNote = _{prefix}PageChrome.categoryNote;
export const {prefix}ComparisonMetadata: Metadata = _{prefix}PageChrome.metadata;
"""
    anchor = f"export const {prefix}MetadataLine"
    if anchor in content:
        content = content.replace(anchor, chrome_block + anchor, 1)
    else:
        content += "\n" + chrome_block

    return content

for fname, slug, prefix in PAGE_DATA:
    path = ROOT / "src/lib/comparisons" / fname
    patched = patch_page_data(path.read_text(encoding="utf-8"), slug, prefix)
    write(f"src/lib/comparisons/{fname}", patched)

print("page-data patched")

# ========== hashvaot-categories.ts ==========
write("src/lib/hashvaot/hashvaot-categories.ts", """/**
 * Hashvaot category registry — editable copy from site-content JSON.
 */

import rawCategories from \"@/data/site-content/hashvaot-categories.json\";

export type HashvaotCategoryStatus = \"live\" | \"building\";

export interface HashvaotCategory {
  id: string;
  title: string;
  status: HashvaotCategoryStatus;
  countLabel?: string;
  href?: string;
  description?: string;
  comingSoonSubtext?: string;
  accent: string;
  heroStat?: { value: string; label: string };
}

type RawCategoriesFile = {
  comingSoonSubtextByCategory: Record<string, string>;
  categories: HashvaotCategory[];
};

const parsed = rawCategories as RawCategoriesFile;

export const RAW_FOODS_COMING_SOON_SUBTEXT =
  parsed.comingSoonSubtextByCategory[\"raw-foods\"] ?? \"\";
export const PERSONAL_CARE_COMING_SOON_SUBTEXT =
  parsed.comingSoonSubtextByCategory[\"personal-care\"] ?? \"\";

export const HASHVAOT_CATEGORIES: HashvaotCategory[] = parsed.categories;

export function getHashvaotCategory(id: string): HashvaotCategory | undefined {
  return HASHVAOT_CATEGORIES.find((c) => c.id === id);
}
""")

# ========== hashvaot/page.tsx ==========
write("src/app/hashvaot/page.tsx", """import type { Metadata } from \"next\";
import Link from \"next/link\";
import { ArrowLeft } from \"lucide-react\";

import { HomeContainer } from \"@/components/home/section-frame\";
import { HashvaotCategoryBox } from \"@/components/hashvaot/hashvaot-category-box\";
import hubCopy from \"@/data/site-content/hashvaot-hub.json\";
import { HASHVAOT_CATEGORIES } from \"@/lib/hashvaot/hashvaot-categories\";
import { cn } from \"@/lib/utils\";
import { siteHeaderOffsetClass } from \"@/lib/site-layout\";

type HubCopy = {
  metadata: { title: string; description: string };
  eyebrowEn: string;
  title: string;
  subtitle: string;
  backLink: string;
};

const copy = hubCopy as HubCopy;

export const metadata: Metadata = {
  title: copy.metadata.title,
  description: copy.metadata.description,
};

export default function HashvaotIndexPage() {
  return (
    <main
      className={cn(
        \"relative min-h-screen bg-[#F7F7F2] text-[#111318]\",
        siteHeaderOffsetClass
      )}
    >
      <HomeContainer className=\"py-14 md:py-20\">
        <p className=\"text-xs font-bold uppercase tracking-[0.22em] text-[#1F8F6A]/80\">
          {copy.eyebrowEn}
        </p>
        <h1 className=\"mt-3 max-w-3xl text-balance text-4xl font-extrabold tracking-[-0.05em] md:text-5xl\">
          {copy.title}
        </h1>
        <p className=\"mt-5 max-w-2xl text-pretty text-lg leading-relaxed text-[#4E5663]\">
          {copy.subtitle}
        </p>

        <div className=\"mt-12 grid gap-5 sm:grid-cols-2\">
          {HASHVAOT_CATEGORIES.map((cat) => (
            <HashvaotCategoryBox key={cat.id} category={cat} />
          ))}
        </div>

        <Link
          href=\"/\"
          className=\"mt-10 inline-flex items-center gap-2 text-sm font-semibold text-[#4E5663] transition-colors hover:text-[#111318]\"
        >
          <ArrowLeft className=\"size-4\" aria-hidden />
          {copy.backLink}
        </Link>
      </HomeContainer>
    </main>
  );
}
""")

print("hashvaot ok")
write("src/app/api/admin/categories/route.ts", """import { NextResponse } from \"next/server\";

import { isAuthed } from \"@/lib/admin/auth\";
import {
  listComparisonEntries,
  SITE_CONTENT_ENTRIES,
} from \"@/lib/admin/content-registry\";
import { LIVE_COMPARISON_FILES } from \"@/lib/admin/fields\";
import { getComparisonFile } from \"@/lib/admin/github\";

export const runtime = \"nodejs\";
export const dynamic = \"force-dynamic\";

export async function GET() {
  if (!(await isAuthed())) {
    return NextResponse.json({ ok: false, error: \"unauthorized\" }, { status: 401 });
  }

  const slugs = Object.keys(LIVE_COMPARISON_FILES).sort();
  const categories = await Promise.all(
    slugs.map(async (slug) => {
      const file = LIVE_COMPARISON_FILES[slug];
      try {
        const { data } = await getComparisonFile(file);
        const meta = data._meta ?? {};
        return {
          slug,
          file,
          nameHe: typeof meta.name_he === \"string\" ? meta.name_he : slug,
          productCount: (data.products ?? []).length,
        };
      } catch {
        return { slug, file, nameHe: slug, productCount: 0, unavailable: true };
      }
    }),
  );

  const site = SITE_CONTENT_ENTRIES.map((entry) => ({
    id: entry.id,
    file: entry.file,
    labelHe: entry.labelHe,
    kind: entry.kind,
  }));

  const pageChromeSlugs = listComparisonEntries().map((e) => e.slug);

  return NextResponse.json({
    sections: {
      products: categories,
      site,
      pageChromeSlugs,
    },
  });
}
""")

write("src/app/api/admin/load/route.ts", """import { NextResponse } from \"next/server\";

import { isAuthed } from \"@/lib/admin/auth\";
import {
  PAGE_CHROME_FILE,
  getSiteContentEntry,
  siteContentFileForId,
} from \"@/lib/admin/content-registry\";
import { extractEditableFields, LIVE_COMPARISON_FILES } from \"@/lib/admin/fields\";
import { getComparisonFile, getSiteContentFile } from \"@/lib/admin/github\";
import {
  extractPageChromeFields,
  extractSiteFields,
} from \"@/lib/admin/site-fields\";

export const runtime = \"nodejs\";
export const dynamic = \"force-dynamic\";

export async function GET(request: Request) {
  if (!(await isAuthed())) {
    return NextResponse.json({ ok: false, error: \"unauthorized\" }, { status: 401 });
  }

  const url = new URL(request.url);
  const type = url.searchParams.get(\"type\") ?? \"products\";

  if (type === \"site\") {
    const id = url.searchParams.get(\"id\") ?? \"\";
    const file = siteContentFileForId(id);
    const entry = getSiteContentEntry(id);
    if (!file || !entry) {
      return NextResponse.json({ ok: false, error: \"unknown_site_content\" }, { status: 404 });
    }
    try {
      const { data, sha } = await getSiteContentFile<Record<string, unknown>>(file);
      return NextResponse.json({
        ok: true,
        type: \"site\",
        id,
        file,
        labelHe: entry.labelHe,
        sha,
        fields: extractSiteFields(data),
        data,
      });
    } catch (err) {
      return NextResponse.json(
        { ok: false, error: \"load_failed\", detail: String(err) },
        { status: 502 },
      );
    }
  }

  if (type === \"page_chrome\") {
    const slug = url.searchParams.get(\"slug\") ?? \"\";
    if (!LIVE_COMPARISON_FILES[slug]) {
      return NextResponse.json({ ok: false, error: \"unknown_category\" }, { status: 404 });
    }
    try {
      const { data, sha } = await getSiteContentFile<Record<string, Record<string, unknown>>>(
        PAGE_CHROME_FILE,
      );
      const chrome = data[slug];
      if (!chrome || typeof chrome !== \"object\") {
        return NextResponse.json({ ok: false, error: \"missing_chrome\" }, { status: 404 });
      }
      return NextResponse.json({
        ok: true,
        type: \"page_chrome\",
        slug,
        file: PAGE_CHROME_FILE,
        sha,
        fields: extractPageChromeFields(slug, chrome as Record<string, unknown>),
        data: chrome,
      });
    } catch (err) {
      return NextResponse.json(
        { ok: false, error: \"load_failed\", detail: String(err) },
        { status: 502 },
      );
    }
  }

  const slug = url.searchParams.get(\"slug\") ?? \"\";
  const file = LIVE_COMPARISON_FILES[slug];
  if (!file) {
    return NextResponse.json({ ok: false, error: \"unknown_category\" }, { status: 404 });
  }

  try {
    const { data, sha } = await getComparisonFile(file);
    const products = (data.products ?? []).map((p) => ({
      id: String(p.id ?? p.barcode ?? \"\"),
      name: typeof p.name === \"string\" ? p.name : \"\",
      score: p.score ?? null,
      grade: p.grade ?? null,
      fields: extractEditableFields(p),
    }));
    const nameHe =
      data._meta && typeof data._meta.name_he === \"string\" ? data._meta.name_he : slug;
    return NextResponse.json({ ok: true, type: \"products\", slug, file, sha, nameHe, products });
  } catch (err) {
    return NextResponse.json(
      { ok: false, error: \"load_failed\", detail: String(err) },
      { status: 502 },
    );
  }
}
""")

print("categories+load api ok")
write("src/app/api/admin/save/route.ts", """import { NextResponse } from \"next/server\";

import { isAuthed } from \"@/lib/admin/auth\";
import { PAGE_CHROME_FILE, siteContentFileForId } from \"@/lib/admin/content-registry\";
import { applyEdits, LIVE_COMPARISON_FILES } from \"@/lib/admin/fields\";
import {
  getComparisonFile,
  getSiteContentFile,
  githubConfigured,
  putComparisonFile,
  putSiteContentFile,
} from \"@/lib/admin/github\";
import { applySiteEdits } from \"@/lib/admin/site-fields\";

export const runtime = \"nodejs\";
export const dynamic = \"force-dynamic\";

type SaveBody = {
  type?: \"products\" | \"site\" | \"page_chrome\";
  slug?: string;
  id?: string;
  edits?: unknown;
  siteEdits?: Record<string, unknown>;
  productEdits?: Record<string, Record<string, unknown>>;
};

export async function POST(request: Request) {
  if (!(await isAuthed())) {
    return NextResponse.json({ ok: false, error: \"unauthorized\" }, { status: 401 });
  }
  if (!githubConfigured()) {
    return NextResponse.json({ ok: false, error: \"github_not_configured\" }, { status: 503 });
  }

  let body: SaveBody;
  try {
    body = (await request.json()) as SaveBody;
  } catch {
    return NextResponse.json({ ok: false, error: \"bad_request\" }, { status: 400 });
  }

  const type = body.type ?? \"products\";

  if (type === \"site\") {
    const id = body.id;
    const file = typeof id === \"string\" ? siteContentFileForId(id) : undefined;
    if (!id || !file) {
      return NextResponse.json({ ok: false, error: \"unknown_site_content\" }, { status: 404 });
    }
    const edits = body.siteEdits ?? body.edits;
    if (!edits || typeof edits !== \"object\") {
      return NextResponse.json({ ok: false, error: \"no_edits\" }, { status: 400 });
    }
    let data: Record<string, unknown>;
    let sha: string;
    try {
      ({ data, sha } = await getSiteContentFile<Record<string, unknown>>(file));
    } catch (err) {
      return NextResponse.json(
        { ok: false, error: \"load_failed\", detail: String(err) },
        { status: 502 },
      );
    }
    const result = applySiteEdits(data, edits as Record<string, unknown>);
    if (result.applied === 0) {
      return NextResponse.json({ ok: false, error: \"no_valid_edits\", rejected: result.rejected }, { status: 400 });
    }
    const message = `Admin site content: ${id} — ${result.applied} field(s)`;
    try {
      const { commitSha } = await putSiteContentFile(file, data, sha, message);
      return NextResponse.json({ ok: true, applied: result.applied, rejected: result.rejected, commitSha });
    } catch (err) {
      return NextResponse.json(
        { ok: false, error: \"commit_failed\", detail: String(err) },
        { status: 502 },
      );
    }
  }

  if (type === \"page_chrome\") {
    const slug = body.slug;
    if (typeof slug !== \"string\" || !LIVE_COMPARISON_FILES[slug]) {
      return NextResponse.json({ ok: false, error: \"unknown_category\" }, { status: 404 });
    }
    const edits = body.siteEdits ?? body.edits;
    if (!edits || typeof edits !== \"object\") {
      return NextResponse.json({ ok: false, error: \"no_edits\" }, { status: 400 });
    }
    let data: Record<string, Record<string, unknown>>;
    let sha: string;
    try {
      ({ data, sha } = await getSiteContentFile(PAGE_CHROME_FILE));
    } catch (err) {
      return NextResponse.json(
        { ok: false, error: \"load_failed\", detail: String(err) },
        { status: 502 },
      );
    }
    const chrome = data[slug];
    if (!chrome || typeof chrome !== \"object\") {
      return NextResponse.json({ ok: false, error: \"missing_chrome\" }, { status: 404 });
    }
    const result = applySiteEdits(chrome as Record<string, unknown>, edits as Record<string, unknown>);
    if (result.applied === 0) {
      return NextResponse.json({ ok: false, error: \"no_valid_edits\", rejected: result.rejected }, { status: 400 });
    }
    data[slug] = chrome;
    const message = `Admin page chrome: ${slug} — ${result.applied} field(s)`;
    try {
      const { commitSha } = await putSiteContentFile(PAGE_CHROME_FILE, data, sha, message);
      return NextResponse.json({ ok: true, applied: result.applied, rejected: result.rejected, commitSha });
    } catch (err) {
      return NextResponse.json(
        { ok: false, error: \"commit_failed\", detail: String(err) },
        { status: 502 },
      );
    }
  }

  const slug = body.slug;
  const edits = body.productEdits ?? body.edits;
  if (typeof slug !== \"string\" || !LIVE_COMPARISON_FILES[slug]) {
    return NextResponse.json({ ok: false, error: \"unknown_category\" }, { status: 404 });
  }
  if (!edits || typeof edits !== \"object\") {
    return NextResponse.json({ ok: false, error: \"no_edits\" }, { status: 400 });
  }

  const file = LIVE_COMPARISON_FILES[slug];
  let data: Awaited<ReturnType<typeof getComparisonFile>>[\"data\"];
  let sha: string;
  try {
    ({ data, sha } = await getComparisonFile(file));
  } catch (err) {
    return NextResponse.json(
      { ok: false, error: \"load_failed\", detail: String(err) },
      { status: 502 },
    );
  }

  const products = data.products ?? [];
  const index = new Map<string, Record<string, unknown>>();
  for (const p of products) {
    index.set(String(p.id ?? p.barcode ?? \"\"), p);
  }

  let applied = 0;
  let productsTouched = 0;
  const rejected: string[] = [];

  for (const [productId, rawFieldEdits] of Object.entries(edits as Record<string, unknown>)) {
    const product = index.get(productId);
    if (!product) {
      rejected.push(`product:${productId}`);
      continue;
    }
    if (!rawFieldEdits || typeof rawFieldEdits !== \"object\") {
      rejected.push(`product:${productId}:bad_shape`);
      continue;
    }
    const result = applyEdits(product, rawFieldEdits as Record<string, unknown>);
    applied += result.applied;
    rejected.push(...result.rejected.map((path) => `${productId}:${path}`));
    if (result.applied > 0) productsTouched += 1;
  }

  if (applied === 0) {
    return NextResponse.json({ ok: false, error: \"no_valid_edits\", rejected }, { status: 400 });
  }

  const message = `Admin copy edit: ${slug} — ${applied} field(s) across ${productsTouched} product(s)`;
  try {
    const { commitSha } = await putComparisonFile(file, data, sha, message);
    return NextResponse.json({ ok: true, applied, productsTouched, rejected, commitSha });
  } catch (err) {
    return NextResponse.json(
      { ok: false, error: \"commit_failed\", detail: String(err) },
      { status: 502 },
    );
  }
}
""")

print("save api ok")
# fix categories route shape
write("src/app/api/admin/categories/route.ts", """import { NextResponse } from \"next/server\";

import { isAuthed } from \"@/lib/admin/auth\";
import { SITE_CONTENT_ENTRIES } from \"@/lib/admin/content-registry\";
import { LIVE_COMPARISON_FILES } from \"@/lib/admin/fields\";
import { getComparisonFile } from \"@/lib/admin/github\";

export const runtime = \"nodejs\";
export const dynamic = \"force-dynamic\";

export async function GET() {
  if (!(await isAuthed())) {
    return NextResponse.json({ ok: false, error: \"unauthorized\" }, { status: 401 });
  }

  const slugs = Object.keys(LIVE_COMPARISON_FILES).sort();
  const products = await Promise.all(
    slugs.map(async (slug) => {
      const file = LIVE_COMPARISON_FILES[slug];
      try {
        const { data } = await getComparisonFile(file);
        const meta = data._meta ?? {};
        return {
          slug,
          file,
          nameHe: typeof meta.name_he === \"string\" ? meta.name_he : slug,
          productCount: (data.products ?? []).length,
        };
      } catch {
        return { slug, file, nameHe: slug, productCount: 0, unavailable: true };
      }
    }),
  );

  const site = SITE_CONTENT_ENTRIES.filter((e) => e.kind === \"site\").map((entry) => ({
    id: entry.id,
    file: entry.file,
    labelHe: entry.labelHe,
    kind: entry.kind,
  }));

  return NextResponse.json({ sections: { products, site } });
}
""")

ADMIN_PAGE = r'''"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

export const dynamic = "force-dynamic";

type FieldKind = "text" | "list";
type SectionTab = "products" | "page_chrome" | "site";

interface EditableField {
  path: string;
  label: string;
  kind: FieldKind;
  value: string | string[];
}

interface ProductSummary {
  slug: string;
  file: string;
  nameHe: string;
  productCount: number;
  unavailable?: boolean;
}

interface SiteSummary {
  id: string;
  file: string;
  labelHe: string;
  kind: string;
}

interface LoadedProducts {
  type: "products";
  slug: string;
  file: string;
  sha: string;
  nameHe: string;
  products: Array<{
    id: string;
    name: string;
    score: number | null;
    grade: string | null;
    fields: EditableField[];
  }>;
}

interface LoadedSiteLike {
  type: "site" | "page_chrome";
  sha: string;
  file: string;
  fields: EditableField[];
  slug?: string;
  id?: string;
  labelHe?: string;
}

type Loaded = LoadedProducts | LoadedSiteLike;
type Draft = Record<string, Record<string, string | string[]>>;

function sameValue(a: string | string[], b: string | string[]): boolean {
  return JSON.stringify(a) === JSON.stringify(b);
}

export default function AdminPage() {
  const [status, setStatus] = useState<"loading" | "login" | "ready">("loading");
  const [githubReady, setGithubReady] = useState(true);
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");

  const [tab, setTab] = useState<SectionTab>("products");
  const [productCategories, setProductCategories] = useState<ProductSummary[]>([]);
  const [siteEntries, setSiteEntries] = useState<SiteSummary[]>([]);
  const [loaded, setLoaded] = useState<Loaded | null>(null);
  const [draft, setDraft] = useState<Draft>({});
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<{ kind: "ok" | "err"; text: string } | null>(null);

  const loadCategories = useCallback(async () => {
    const res = await fetch("/api/admin/categories");
    if (!res.ok) return;
    const data = await res.json();
    setProductCategories(data.sections?.products ?? []);
    setSiteEntries(data.sections?.site ?? []);
  }, []);

  useEffect(() => {
    void (async () => {
      try {
        const res = await fetch("/api/admin/session");
        const data = await res.json();
        setGithubReady(Boolean(data.githubConfigured));
        if (data.authed) {
          setStatus("ready");
          await loadCategories();
        } else {
          setStatus("login");
        }
      } catch {
        setStatus("login");
      }
    })();
  }, [loadCategories]);

  async function doLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoginError("");
    const res = await fetch("/api/admin/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });
    if (res.ok) {
      setPassword("");
      setStatus("ready");
      const session = await (await fetch("/api/admin/session")).json();
      setGithubReady(Boolean(session.githubConfigured));
      await loadCategories();
    } else if (res.status === 503) {
      setLoginError("העורך לא מוגדר עדיין (חסרים סודות בשרת).");
    } else {
      setLoginError("סיסמה שגויה.");
    }
  }

  async function doLogout() {
    await fetch("/api/admin/logout", { method: "POST" });
    setLoaded(null);
    setDraft({});
    setStatus("login");
  }

  async function openProduct(slug: string) {
    setNotice(null);
    setBusy(true);
    setLoaded(null);
    setDraft({});
    try {
      const res = await fetch(`/api/admin/load?type=products&slug=${encodeURIComponent(slug)}`);
      const data = await res.json();
      if (data.ok) setLoaded(data as LoadedProducts);
      else setNotice({ kind: "err", text: "טעינת הקטגוריה נכשלה." });
    } finally {
      setBusy(false);
    }
  }

  async function openPageChrome(slug: string) {
    setNotice(null);
    setBusy(true);
    setLoaded(null);
    setDraft({});
    try {
      const res = await fetch(
        `/api/admin/load?type=page_chrome&slug=${encodeURIComponent(slug)}`,
      );
      const data = await res.json();
      if (data.ok) {
        setLoaded({
          type: "page_chrome",
          slug: data.slug,
          file: data.file,
          sha: data.sha,
          fields: data.fields,
          labelHe: data.slug,
        });
        setDraft({ __root: Object.fromEntries(data.fields.map((f: EditableField) => [f.path, f.value])) });
      } else setNotice({ kind: "err", text: "טעינת כותרות העמוד נכשלה." });
    } finally {
      setBusy(false);
    }
  }

  async function openSite(id: string) {
    setNotice(null);
    setBusy(true);
    setLoaded(null);
    setDraft({});
    try {
      const res = await fetch(`/api/admin/load?type=site&id=${encodeURIComponent(id)}`);
      const data = await res.json();
      if (data.ok) {
        setLoaded({
          type: "site",
          id: data.id,
          file: data.file,
          sha: data.sha,
          fields: data.fields,
          labelHe: data.labelHe,
        });
        setDraft({ __root: Object.fromEntries(data.fields.map((f: EditableField) => [f.path, f.value])) });
      } else setNotice({ kind: "err", text: "טעינת דף האתר נכשלה." });
    } finally {
      setBusy(false);
    }
  }

  function setField(productId: string, path: string, value: string | string[]) {
    setDraft((prev) => ({
      ...prev,
      [productId]: { ...(prev[productId] ?? {}), [path]: value },
    }));
  }

  const dirtyProductEdits = useMemo<Draft>(() => {
    if (!loaded || loaded.type !== "products") return {};
    const originals = new Map<string, Map<string, string | string[]>>();
    for (const p of loaded.products) {
      const m = new Map<string, string | string[]>();
      for (const f of p.fields) m.set(f.path, f.value);
      originals.set(p.id, m);
    }
    const out: Draft = {};
    for (const [pid, fields] of Object.entries(draft)) {
      for (const [path, value] of Object.entries(fields)) {
        const orig = originals.get(pid)?.get(path);
        if (orig === undefined || !sameValue(orig, value)) {
          (out[pid] ??= {})[path] = value;
        }
      }
    }
    return out;
  }, [draft, loaded]);

  const dirtySiteEdits = useMemo<Record<string, string | string[]>>(() => {
    if (!loaded || loaded.type === "products") return {};
    const root = draft.__root ?? {};
    const out: Record<string, string | string[]> = {};
    for (const f of loaded.fields) {
      const value = root[f.path] ?? f.value;
      if (!sameValue(value, f.value)) out[f.path] = value;
    }
    return out;
  }, [draft, loaded]);

  const dirtyCount =
    loaded?.type === "products"
      ? Object.values(dirtyProductEdits).reduce((n, f) => n + Object.keys(f).length, 0)
      : Object.keys(dirtySiteEdits).length;

  async function save() {
    if (!loaded || dirtyCount === 0) return;
    setBusy(true);
    setNotice(null);
    try {
      let body: Record<string, unknown>;
      if (loaded.type === "products") {
        body = { type: "products", slug: loaded.slug, productEdits: dirtyProductEdits };
      } else if (loaded.type === "page_chrome") {
        body = { type: "page_chrome", slug: loaded.slug, siteEdits: dirtySiteEdits };
      } else {
        body = { type: "site", id: loaded.id, siteEdits: dirtySiteEdits };
      }
      const res = await fetch("/api/admin/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (data.ok) {
        setNotice({
          kind: "ok",
          text: `נשמר ופורסם — ${data.applied} שינוי(ים). העדכון יעלה לאתר תוך כ-2 דקות.`,
        });
        if (loaded.type === "products") await openProduct(loaded.slug);
        else if (loaded.type === "page_chrome" && loaded.slug) await openPageChrome(loaded.slug);
        else if (loaded.type === "site" && loaded.id) await openSite(loaded.id);
      } else if (data.error === "github_not_configured") {
        setNotice({ kind: "err", text: "הפרסום ל-GitHub לא מוגדר בשרת." });
      } else {
        setNotice({ kind: "err", text: "השמירה נכשלה. נסה שוב." });
      }
    } catch {
      setNotice({ kind: "err", text: "שגיאת רשת בשמירה." });
    } finally {
      setBusy(false);
    }
  }

  if (status === "loading") {
    return (
      <Shell>
        <p className="text-neutral-500">טוען…</p>
      </Shell>
    );
  }

  if (status === "login") {
    return (
      <Shell>
        <form onSubmit={doLogin} className="mx-auto mt-16 max-w-sm space-y-4">
          <h1 className="text-xl font-semibold">עורך התוכן של Bari</h1>
          <p className="text-sm text-neutral-500">הזן סיסמה כדי לערוך משפטים וכיתובים.</p>
          <input
            type="password"
            autoFocus
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="סיסמה"
            className="w-full rounded-md border border-neutral-300 px-3 py-2"
          />
          {loginError && <p className="text-sm text-red-600">{loginError}</p>}
          <button type="submit" className="w-full rounded-md bg-neutral-900 px-4 py-2 text-white">
            כניסה
          </button>
        </form>
      </Shell>
    );
  }

  const sidebar =
    tab === "products"
      ? productCategories.map((c) => (
          <SidebarBtn
            key={c.slug}
            active={loaded?.type === "products" && loaded.slug === c.slug}
            disabled={c.unavailable}
            onClick={() => openProduct(c.slug)}
          >
            {c.nameHe}
            <span className="mr-1 text-xs opacity-60">({c.productCount})</span>
          </SidebarBtn>
        ))
      : tab === "page_chrome"
        ? productCategories.map((c) => (
            <SidebarBtn
              key={c.slug}
              active={loaded?.type === "page_chrome" && loaded.slug === c.slug}
              disabled={c.unavailable}
              onClick={() => openPageChrome(c.slug)}
            >
              {c.nameHe}
            </SidebarBtn>
          ))
        : siteEntries.map((s) => (
            <SidebarBtn
              key={s.id}
              active={loaded?.type === "site" && loaded.id === s.id}
              onClick={() => openSite(s.id)}
            >
              {s.labelHe}
            </SidebarBtn>
          ));

  return (
    <Shell wide>
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-xl font-semibold">עורך התוכן של Bari</h1>
        <button onClick={doLogout} className="text-sm text-neutral-500 underline">
          יציאה
        </button>
      </div>

      {!githubReady && (
        <Banner kind="err">
          הפרסום ל-GitHub לא מוגדר בשרת — אפשר לערוך ולצפות, אך שמירה לא תעלה לאתר עד שיוגדרו הסודות.
        </Banner>
      )}

      <div className="mb-4 flex flex-wrap gap-2">
        {(
          [
            ["products", "טקסט מוצרים"],
            ["page_chrome", "כותרות עמודי השוואה"],
            ["site", "דפי אתר"],
          ] as const
        ).map(([id, label]) => (
          <button
            key={id}
            type="button"
            onClick={() => {
              setTab(id);
              setLoaded(null);
              setDraft({});
              setNotice(null);
            }}
            className={`rounded-md px-3 py-2 text-sm ${
              tab === id ? "bg-neutral-900 text-white" : "bg-neutral-100 hover:bg-neutral-200"
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-[240px_1fr]">
        <aside className="space-y-1">{sidebar}</aside>
        <main>
          {notice && <Banner kind={notice.kind}>{notice.text}</Banner>}
          {!loaded && <p className="text-neutral-400">בחר פריט מהרשימה כדי לערוך.</p>}

          {loaded?.type === "products" && (
            <>
              <EditorHeader
                title={loaded.nameHe}
                subtitle={loaded.file}
                dirtyCount={dirtyCount}
                busy={busy}
                onSave={save}
              />
              <div className="space-y-8">
                {loaded.products.map((p) => (
                  <ProductBlock
                    key={p.id}
                    product={p}
                    draft={draft[p.id] ?? {}}
                    onChange={(path, value) => setField(p.id, path, value)}
                  />
                ))}
              </div>
            </>
          )}

          {loaded && loaded.type !== "products" && (
            <>
              <EditorHeader
                title={loaded.labelHe ?? loaded.slug ?? loaded.id ?? ""}
                subtitle={loaded.file}
                dirtyCount={dirtyCount}
                busy={busy}
                onSave={save}
              />
              <SiteFieldsBlock
                fields={loaded.fields}
                draft={draft.__root ?? {}}
                onChange={(path, value) => setField("__root", path, value)}
              />
            </>
          )}
        </main>
      </div>
    </Shell>
  );
}

function EditorHeader({
  title,
  subtitle,
  dirtyCount,
  busy,
  onSave,
}: {
  title: string;
  subtitle: string;
  dirtyCount: number;
  busy: boolean;
  onSave: () => void;
}) {
  return (
    <div className="sticky top-0 z-10 mb-4 flex items-center justify-between border-b border-neutral-200 bg-white/90 py-3 backdrop-blur">
      <div>
        <h2 className="text-lg font-medium">{title}</h2>
        <p className="text-xs text-neutral-400">{subtitle}</p>
      </div>
      <button
        type="button"
        onClick={onSave}
        disabled={busy || dirtyCount === 0}
        className="rounded-md bg-emerald-600 px-4 py-2 text-sm text-white disabled:opacity-40"
      >
        {busy ? "שומר…" : dirtyCount > 0 ? `פרסם ${dirtyCount} שינוי(ים)` : "אין שינויים"}
      </button>
    </div>
  );
}

function SidebarBtn({
  children,
  active,
  disabled,
  onClick,
}: {
  children: React.ReactNode;
  active?: boolean;
  disabled?: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={`block w-full rounded-md px-3 py-2 text-right text-sm ${
        active ? "bg-neutral-900 text-white" : "hover:bg-neutral-100"
      } ${disabled ? "opacity-40" : ""}`}
    >
      {children}
    </button>
  );
}

function SiteFieldsBlock({
  fields,
  draft,
  onChange,
}: {
  fields: EditableField[];
  draft: Record<string, string | string[]>;
  onChange: (path: string, value: string | string[]) => void;
}) {
  return (
    <div className="space-y-4">
      {fields.map((f) => {
        const current = draft[f.path] ?? f.value;
        return (
          <label key={f.path} className="block">
            <span className="mb-1 block text-xs font-medium text-neutral-500">{f.label}</span>
            {f.kind === "list" ? (
              <textarea
                dir="rtl"
                rows={Math.max(2, (current as string[]).length)}
                value={(current as string[]).join("\n")}
                onChange={(e) =>
                  onChange(
                    f.path,
                    e.target.value
                      .split("\n")
                      .filter((s, i, arr) => !(s === "" && i === arr.length - 1)),
                  )
                }
                className="w-full rounded-md border border-neutral-300 px-3 py-2 text-sm leading-relaxed"
              />
            ) : (
              <textarea
                dir="rtl"
                rows={2}
                value={current as string}
                onChange={(e) => onChange(f.path, e.target.value)}
                className="w-full rounded-md border border-neutral-300 px-3 py-2 text-sm leading-relaxed"
              />
            )}
          </label>
        );
      })}
    </div>
  );
}

function ProductBlock({
  product,
  draft,
  onChange,
}: {
  product: {
    id: string;
    name: string;
    score: number | null;
    grade: string | null;
    fields: EditableField[];
  };
  draft: Record<string, string | string[]>;
  onChange: (path: string, value: string | string[]) => void;
}) {
  return (
    <section className="rounded-lg border border-neutral-200 p-4">
      <header className="mb-3 flex items-baseline justify-between">
        <h3 className="font-medium">{product.name || product.id}</h3>
        <span className="text-xs text-neutral-400">
          {product.score ?? "—"} · {product.grade ?? "—"}{" "}
          <span className="opacity-60">(לא ניתן לעריכה)</span>
        </span>
      </header>
      {product.fields.length === 0 && (
        <p className="text-xs text-neutral-400">אין שדות טקסט הניתנים לעריכה במוצר זה.</p>
      )}
      <SiteFieldsBlock fields={product.fields} draft={draft} onChange={onChange} />
    </section>
  );
}

function Shell({ children, wide }: { children: React.ReactNode; wide?: boolean }) {
  return (
    <div dir="rtl" lang="he" className="min-h-screen bg-white px-4 py-8 text-neutral-900">
      <div className={wide ? "mx-auto max-w-6xl" : "mx-auto max-w-4xl"}>{children}</div>
    </div>
  );
}

function Banner({ kind, children }: { kind: "ok" | "err"; children: React.ReactNode }) {
  return (
    <div
      className={`mb-4 rounded-md px-4 py-3 text-sm ${
        kind === "ok" ? "bg-emerald-50 text-emerald-800" : "bg-red-50 text-red-800"
      }`}
    >
      {children}
    </div>
  );
}
'''

write("src/app/admin/page.tsx", ADMIN_PAGE)
print("admin page ok")
