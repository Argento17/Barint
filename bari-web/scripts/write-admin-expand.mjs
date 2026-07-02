import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
function write(rel, content) {
  const abs = path.join(ROOT, rel);
  fs.mkdirSync(path.dirname(abs), { recursive: true });
  fs.writeFileSync(abs, content, "utf8");
  console.log("wrote", rel);
}
function patch(rel, fn) {
  const abs = path.join(ROOT, rel);
  const before = fs.readFileSync(abs, "utf8");
  const after = fn(before);
  if (after !== before) { fs.writeFileSync(abs, after, "utf8"); console.log("patched", rel); }
}
function hx(hex) { return Buffer.from(hex, "hex").toString("utf8"); }

write("src/lib/admin/content-registry.ts", `/**
 * Admin site-content registry (hub, homepage, page chrome).
 */
import comparisonPages from "@/data/site-content/comparison-pages.json";

export const PAGE_CHROME_FILE = "comparison-pages.json";

export interface SiteContentEntry {
  id: string;
  file: string;
  labelHe: string;
}

export const SITE_CONTENT_ENTRIES: SiteContentEntry[] = [
  { id: "hashvaot-hub", file: "hashvaot-hub.json", labelHe: ${JSON.stringify(hx("d79ed7a8d79bd79620d794d7a9d795d795d790d795d7aa202848756229"))} },
  { id: "hashvaot-categories", file: "hashvaot-categories.json", labelHe: ${JSON.stringify(hx("d7a7d798d792d795d7a8d799d795d7aa20d794d7a9d795d795d790d795d7aa"))} },
  { id: "homepage-marketing", file: "homepage-marketing.json", labelHe: ${JSON.stringify(hx("d793d7a320d794d791d799d7aa20e2809420d7a9d799d795d795d7a7"))} },
  { id: "page-chrome", file: PAGE_CHROME_FILE, labelHe: ${JSON.stringify(hx("d79bd7a8d795d79d20d793d7a4d79920d794d7a9d795d795d790d794"))} },
];

export function listComparisonEntries(): { slug: string; nameHe: string }[] {
  const pages = comparisonPages as Record<string, { hero?: { title?: string }; metadata?: { title?: string } }>;
  return Object.keys(pages)
    .sort()
    .map((slug) => ({
      slug,
      nameHe: pages[slug]?.hero?.title ?? pages[slug]?.metadata?.title ?? slug,
    }));
}

export function getSiteContentEntry(id: string): SiteContentEntry | undefined {
  return SITE_CONTENT_ENTRIES.find((e) => e.id === id);
}
`);

write("src/lib/site-content/comparison-page-chrome.ts", `import comparisonPages from "@/data/site-content/comparison-pages.json";

export interface ComparisonPageChrome {
  hero: { eyebrow: string; title: string };
  prologue: readonly string[];
  methodology: readonly string[];
  categoryNote: string;
  metadata: { title: string; description: string };
}

const pages = comparisonPages as Record<string, ComparisonPageChrome>;

export function getComparisonPageChrome(slug: string): ComparisonPageChrome {
  const chrome = pages[slug];
  if (!chrome) {
    throw new Error(\`Unknown comparison page chrome slug: \${slug}\`);
  }
  return chrome;
}

export function listComparisonChromeSlugs(): string[] {
  return Object.keys(pages).sort();
}
`);

patch("src/lib/admin/fields.ts", (t) => {
  const block = `export const LIVE_COMPARISON_FILES: Record<string, string> = {
  bread: "bread_frontend_v3.json",
  brined_cheeses: "brined_cheeses_frontend_v2.json",
  cakes_hard_cookies: "cakes_hard_cookies_frontend_v1.json",
  cereals: "cereals_frontend_v2.json",
  cheese: "cheese_frontend_v4.json",
  chocolate_bars: "chocolate_bars_frontend_v1.json",
  chocolate_tablets: "chocolate_tablets_frontend_v1.json",
  cookies_coffee: "cookies_coffee_frontend_v2.json",
  granola: "granola_frontend_v1.json",
  hard_cheeses: "hard_cheeses_frontend_v2.json",
  hummus: "hummus_frontend_v5.json",
  juices: "juices_frontend_v3.json",
  milk: "milk_frontend_v1.json",
  protein_bars: "protein_combined_frontend_v2.json",
  snacks: "snacks_frontend_v5.json",
};
`;
  return t.replace(/export const LIVE_COMPARISON_FILES[\s\S]*?};\r?\n/, block);
});

write("src/lib/admin/github.ts", `/**
 * Admin copy editor — GitHub read/write for comparison + site-content JSON.
 */
const API = "https://api.github.com";
export const COMPARISONS_REPO_DIR = "bari-web/src/data/comparisons";
export const SITE_CONTENT_REPO_DIR = "bari-web/src/data/site-content";

function cfg() {
  const token = process.env.ADMIN_GITHUB_TOKEN || "";
  const repo = process.env.ADMIN_GITHUB_REPO || "Argento17/Barint";
  const branch = process.env.ADMIN_GITHUB_BRANCH || "master";
  return { token, repo, branch };
}

export function githubConfigured(): boolean {
  return Boolean(process.env.ADMIN_GITHUB_TOKEN);
}

async function gh(path: string, init?: RequestInit): Promise<Response> {
  const { token } = cfg();
  return fetch(\`\${API}\${path}\`, {
    ...init,
    headers: {
      Authorization: \`Bearer \${token}\`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "bari-admin-copy-editor",
      ...(init?.headers || {}),
    },
    cache: "no-store",
  });
}

export interface FetchedFile {
  data: Record<string, unknown>;
  sha: string;
}

export async function getRepoFileAt(dir: string, file: string): Promise<FetchedFile> {
  const { repo, branch } = cfg();
  const res = await gh(
    \`/repos/\${repo}/contents/\${dir}/\${encodeURIComponent(file)}?ref=\${encodeURIComponent(branch)}\`,
  );
  if (!res.ok) {
    throw new Error(\`GitHub getFile \${dir}/\${file} failed: \${res.status} \${await res.text()}\`);
  }
  const body = (await res.json()) as { content: string; sha: string; encoding: string };
  const raw = Buffer.from(body.content, body.encoding === "base64" ? "base64" : "utf8").toString("utf8");
  return { data: JSON.parse(raw), sha: body.sha };
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
  const res = await gh(\`/repos/\${repo}/contents/\${dir}/\${encodeURIComponent(file)}\`, {
    method: "PUT",
    body: JSON.stringify({
      message,
      content: Buffer.from(text, "utf8").toString("base64"),
      sha,
      branch,
    }),
  });
  if (!res.ok) {
    throw new Error(\`GitHub putFile \${dir}/\${file} failed: \${res.status} \${await res.text()}\`);
  }
  const body = (await res.json()) as { commit: { sha: string } };
  return { commitSha: body.commit.sha };
}

export async function getComparisonFile(file: string): Promise<FetchedFile> {
  const { data, sha } = await getRepoFileAt(COMPARISONS_REPO_DIR, file);
  return { data, sha };
}

export async function putComparisonFile(
  file: string,
  data: unknown,
  sha: string,
  message: string,
): Promise<{ commitSha: string }> {
  return putRepoFileAt(COMPARISONS_REPO_DIR, file, data, sha, message);
}

export async function getSiteContentFile(file: string): Promise<FetchedFile> {
  return getRepoFileAt(SITE_CONTENT_REPO_DIR, file);
}

export async function putSiteContentFile(
  file: string,
  data: unknown,
  sha: string,
  message: string,
): Promise<{ commitSha: string }> {
  return putRepoFileAt(SITE_CONTENT_REPO_DIR, file, data, sha, message);
}
`);

const PAGE_CHROME_LABELS = {
  "hero.eyebrow": hx("d79bd795d7aad7a8d7aa20d7a2d79c"),
  "hero.title": hx("d79bd795d7aad7a8d7aa20d7a8d790d7a9d799d7aa"),
  categoryNote: hx("d794d7a2d7a8d7aa20d7a7d798d792d795d7a8d799d794"),
  "metadata.title": hx("d79bd795d7aad7a8d7aa2053454f"),
  "metadata.description": hx("d7aad799d790d795d7a82053454f"),
  prologue: hx("d7a4d7aad799d7972028d79ed7a9d7a4d798d799d79d29"),
  methodology: hx("d79ed7aad795d793d795d79cd795d792d799d7942028d7a9d795d7a8d795d7aa29"),
};

write("src/lib/admin/site-fields.ts", `/**
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
    cur = cur[key];
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
    const pathKey = prefix ? \`\${prefix}.\${key}\` : key;
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

const PAGE_CHROME_LABELS: Record<string, string> = ${JSON.stringify(PAGE_CHROME_LABELS, null, 2)};

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
`);

// --- site-content JSON (skip if comparison-pages exists) ---
const hubPage = fs.readFileSync(path.join(ROOT, "src/app/hashvaot/page.tsx"), "utf8");
const hubMetaTitle = hubPage.match(/title:\s*"([^"]+)"/)?.[1] ?? "";
const hubMetaDesc = hubPage.match(/description:\s*\n\s*"([^"]+)"/)?.[1] ?? "";
const hubEyebrow = hubPage.match(/tracking-\[0\.22em\][^>]*>\s*\n\s*([^<]+)/)?.[1]?.trim() ?? "Bari comparisons";
const hubTitle = hubPage.match(/<h1[^>]*>\s*\n\s*([^<]+)/)?.[1]?.trim() ?? "";
const hubLead = hubPage.match(/<p className="mt-5[\s\S]*?>\s*\n\s*([^<]+)/)?.[1]?.trim() ?? "";
const hubBack = hubPage.match(/ArrowLeft[\s\S]*?\n\s*([^<]+)/)?.[1]?.trim() ?? "";

write("src/data/site-content/hashvaot-hub.json", JSON.stringify({
  metadata: { title: hubMetaTitle, description: hubMetaDesc },
  eyebrow: hubEyebrow,
  title: hubTitle,
  lead: hubLead,
  backLinkLabel: hubBack,
}, null, 2));

const catTs = fs.readFileSync(path.join(ROOT, "src/lib/hashvaot/hashvaot-categories.ts"), "utf8");
const rawSoon = catTs.match(/RAW_FOODS_COMING_SOON_SUBTEXT =\s*\n\s*"([^"]+)"/)?.[1] ?? "";
const careSoon = catTs.match(/PERSONAL_CARE_COMING_SOON_SUBTEXT =\s*\n\s*"([^"]+)"/)?.[1] ?? "";
const catJson = {
  comingSoonSubtexts: { "raw-foods": rawSoon, "personal-care": careSoon },
  categories: [
    { id: "supermarket", status: "live", href: "/hashvaot/supermarket", accent: "#BC6A33", title: "מוצרי סופרמרקט אמיתיים", countLabel: "16 השוואות", description: "חלב, לחם, חטיפים, עוגות, גבינות ועוד", heroStat: { value: "16", label: "השוואות פעילות" } },
    { id: "supplements", status: "live", href: "/hashvaot/supplements", accent: "#4A7B8C", title: "תוספי תזונה", countLabel: "1 השוואה", description: "תוספי תזונה מנותחים באופן שונה ממוצרי מזון — ספיגה, אפקטיביות ועוד", heroStat: { value: "1", label: "השוואות פעילות" } },
    { id: "raw-foods", status: "building", href: "/hashvaot/raw-foods", accent: "#7A8C5E", title: "מזון גולמי" },
    { id: "personal-care", status: "building", href: "/hashvaot/personal-care", accent: "#8B7BA8", title: "טיפוח אישי" },
  ],
};
write("src/data/site-content/hashvaot-categories.json", JSON.stringify(catJson, null, 2));

const trustTs = fs.readFileSync(path.join(ROOT, "src/components/home/home-trust.tsx"), "utf8");
const trustEyebrow = trustTs.match(/tracking-\[0\.24em\][^>]*>\s*\n\s*([^<]+)/)?.[1]?.trim() ?? "";
const trustTitle = trustTs.match(/<h2 className="mt-3[\s\S]*?>\s*\n\s*([^<]+)/)?.[1]?.trim() ?? "";
const trustFoot = trustTs.match(/mt-6 max-w-2xl[\s\S]*?>\s*\n\s*([^<]+)/)?.[1]?.trim() ?? "";
const compTs = fs.readFileSync(path.join(ROOT, "src/components/home/home-comparisons.tsx"), "utf8");
const compTitle = compTs.match(/text-3xl font-extrabold[\s\S]*?>\s*\n\s*([^<]+)/)?.[1]?.trim() ?? "";
const compSub = compTs.match(/text-pretty text-base leading-relaxed[\s\S]*?>\s*\n\s*([^<]+)/)?.[1]?.trim() ?? "";
const methTs = fs.readFileSync(path.join(ROOT, "src/components/home/home-methodology.tsx"), "utf8");
const methTitle = methTs.match(/md:text-5xl[\s\S]*?>\s*\r?\n\s*([^<]+)/)?.[1]?.trim() ?? "";
const heroTs = fs.readFileSync(path.join(ROOT, "src/components/home/home-hero.tsx"), "utf8");
const heroBadge = heroTs.match(/ניתוח מוצרים[^<]*/)?.[0]?.trim() ?? "";
const contentTs = fs.readFileSync(path.join(ROOT, "src/components/home/content.ts"), "utf8");
const heroTrustLabels = [...contentTs.matchAll(/label:\s*"([^"]+)"/g)].slice(0, 3).map((m) => m[1]);

write("src/data/site-content/homepage-marketing.json", JSON.stringify({
  hero: { badgeLink: heroBadge },
  heroTrust: heroTrustLabels,
  trust: { eyebrow: trustEyebrow, title: trustTitle, footnote: trustFoot },
  comparisons: { title: compTitle, subtitle: compSub },
  methodology: { title: methTitle },
}, null, 2));

if (!fs.existsSync(path.join(ROOT, "src/data/site-content/comparison-pages.json"))) {
  console.error("missing comparison-pages.json");
} else {
  console.log("verified comparison-pages.json");
}

const PAGE_DATA_FILES = [
  ["bread-comparison-page-data.ts", "bread"],
  ["brined-cheeses-page-data.ts", "brined_cheeses"],
  ["cakes-hard-cookies-page-data.ts", "cakes_hard_cookies"],
  ["cereals-page-data.ts", "cereals"],
  ["cheese-page-data.ts", "cheese"],
  ["chocolate-bars-comparison-page-data.ts", "chocolate_bars"],
  ["chocolate-tablets-comparison-page-data.ts", "chocolate_tablets"],
  ["cookies-coffee-page-data.ts", "cookies_coffee"],
  ["granola-page-data.ts", "granola"],
  ["hard-cheeses-page-data.ts", "hard_cheeses"],
  ["hummus-comparison-page-data.ts", "hummus"],
  ["juices-page-data.ts", "juices"],
  ["protein-bars-comparison-page-data.ts", "protein_bars"],
  ["snacks-comparison-page-data.ts", "snacks"],
];

function patchPageData(file, slug) {
  patch(path.join("src/lib/comparisons", file), (t) => {
    if (t.includes("getComparisonPageChrome")) return t;
    const heroM = t.match(/export const (\w+)Hero\b/);
    if (!heroM) return t;
    const pfx = heroM[1];
    const metaM = t.match(/export const (\w+(?:Comparison)?Metadata)\b/);
    const metaName = metaM ? metaM[1] : pfx + "ComparisonMetadata";
    t = t.replace(
      /import type \{ Metadata \} from "next";\r?\n/,
      'import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";\nimport type { Metadata } from "next";\n',
    );
    t = t.replace(/export const \w+Hero = [\s\S]*?as const;\r?\n\r?\n/g, "");
    t = t.replace(/export const \w+PrologueSentences = [\s\S]*?as const;\r?\n\r?\n/g, "");
    t = t.replace(/export const \w+CategoryNote = [\s\S]*?;\r?\n\r?\n/g, "");
    t = t.replace(/export const \w+MethodologyLines = [\s\S]*?;\r?\n\r?\n/g, "");
    t = t.replace(/export const \w+(?:Comparison)?Metadata: Metadata = [\s\S]*?};\r?\n\r?\n/g, "");
    const chromeVar = pfx + "PageChrome";
    const block = [
      "",
      "const " + chromeVar + ' = getComparisonPageChrome("' + slug + '");',
      "export const " + pfx + "Hero = " + chromeVar + ".hero;",
      "export const " + pfx + "PrologueSentences = " + chromeVar + ".prologue;",
      "export const " + pfx + "CategoryNote = " + chromeVar + ".categoryNote;",
      "export const " + pfx + "MethodologyLines = " + chromeVar + ".methodology;",
      "export const " + metaName + ": Metadata = " + chromeVar + ".metadata;",
      "",
    ].join("\n");
    const fnM = t.match(/export function get\w+PageData/);
    if (fnM) t = t.replace(fnM[0], block + fnM[0]);
    else t += block;
    return t;
  });
}

for (const [file, slug] of PAGE_DATA_FILES) patchPageData(file, slug);





