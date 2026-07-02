# -*- coding: utf-8 -*-
from pathlib import Path
ROOT = Path(r"C:\Bari\bari-web")

content_registry = r'''/**
 * Admin site-content registry (hub, homepage, page chrome slugs).
 */
import comparisonPages from "@/data/site-content/comparison-pages.json";

export const PAGE_CHROME_FILE = "comparison-pages.json";

export interface SiteContentEntry {
  id: string;
  file: string;
  labelHe: string;
}

export const SITE_CONTENT_ENTRIES: SiteContentEntry[] = [
  { id: "hashvaot-hub", file: "hashvaot-hub.json", labelHe: "\u05de\u05e8\u05db\u05d6 \u05d4\u05d4\u05e9\u05d5\u05d5\u05d0\u05d5\u05ea (Hub)" },
  { id: "hashvaot-categories", file: "hashvaot-categories.json", labelHe: "\u05e7\u05d8\u05d2\u05d5\u05e8\u05d9\u05d5\u05ea \u05d4\u05d4\u05e9\u05d5\u05d5\u05d0\u05d5\u05ea" },
  { id: "homepage-marketing", file: "homepage-marketing.json", labelHe: "\u05d3\u05e3 \u05d4\u05d1\u05d9\u05ea \u2014 \u05e9\u05d9\u05d5\u05d5\u05d5\u05d9\u05d9\u05d5\u05df" },
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
'''

categories = r'''import { NextResponse } from "next/server";

import { isAuthed } from "@/lib/admin/auth";
import { LIVE_BLOG_DOCS } from "@/lib/admin/blog";
import { listComparisonEntries, SITE_CONTENT_ENTRIES } from "@/lib/admin/content-registry";
import { LIVE_COMPARISON_FILES } from "@/lib/admin/fields";
import { getComparisonFile } from "@/lib/admin/github";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  if (!(await isAuthed())) {
    return NextResponse.json({ ok: false, error: "unauthorized" }, { status: 401 });
  }

  const slugs = Object.keys(LIVE_COMPARISON_FILES).sort();
  const comparisons = await Promise.all(
    slugs.map(async (slug) => {
      const file = LIVE_COMPARISON_FILES[slug];
      try {
        const { data } = await getComparisonFile(file);
        const meta = data._meta ?? {};
        return {
          kind: "comparison" as const,
          slug,
          file,
          nameHe: typeof meta.name_he === "string" ? meta.name_he : slug,
          productCount: (data.products ?? []).length,
        };
      } catch {
        return { kind: "comparison" as const, slug, file, nameHe: slug, productCount: 0, unavailable: true };
      }
    }),
  );

  const blog = LIVE_BLOG_DOCS.map((d) => ({
    kind: "blog" as const,
    slug: d.slug,
    nameHe: d.labelHe,
    route: d.route,
  }));

  const pageChrome = listComparisonEntries().map((e) => ({
    kind: "page_chrome" as const,
    slug: e.slug,
    nameHe: e.nameHe,
  }));

  const site = SITE_CONTENT_ENTRIES.map((entry) => ({
    kind: "site" as const,
    id: entry.id,
    slug: entry.id,
    nameHe: entry.labelHe,
    file: entry.file,
  }));

  return NextResponse.json({ comparisons, blog, pageChrome, site });
}
'''

load_route = r'''import { NextResponse } from "next/server";

import { isAuthed } from "@/lib/admin/auth";
import { BLOG_DIR, blogDoc, extractProse } from "@/lib/admin/blog";
import { getSiteContentEntry, PAGE_CHROME_FILE } from "@/lib/admin/content-registry";
import { extractEditableFields, LIVE_COMPARISON_FILES } from "@/lib/admin/fields";
import { extractPageChromeFields, extractSiteFields } from "@/lib/admin/site-fields";
import { getComparisonFile, getRepoJson, getSiteContentFile } from "@/lib/admin/github";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  if (!(await isAuthed())) {
    return NextResponse.json({ ok: false, error: "unauthorized" }, { status: 401 });
  }

  const params = new URL(request.url).searchParams;
  const slug = params.get("slug") ?? "";
  const kind = params.get("kind") ?? "comparison";

  if (kind === "blog") {
    const doc = blogDoc(slug);
    if (!doc) {
      return NextResponse.json({ ok: false, error: "unknown_blog_doc" }, { status: 404 });
    }
    try {
      const { data, sha } = await getRepoJson(`${BLOG_DIR}/${doc.file}`);
      return NextResponse.json({
        ok: true,
        kind: "blog",
        slug,
        sha,
        nameHe: doc.labelHe,
        products: [
          { id: slug, name: doc.labelHe, score: null, grade: null, fields: extractProse(data) },
        ],
      });
    } catch (err) {
      return NextResponse.json(
        { ok: false, error: "load_failed", detail: String(err) },
        { status: 502 },
      );
    }
  }

  if (kind === "site") {
    const id = slug || params.get("id") || "";
    const entry = getSiteContentEntry(id);
    if (!entry) {
      return NextResponse.json({ ok: false, error: "unknown_site_id" }, { status: 404 });
    }
    try {
      const { data, sha } = await getSiteContentFile(entry.file);
      const fields = extractSiteFields(data as Record<string, unknown>);
      return NextResponse.json({
        ok: true,
        kind: "site",
        slug: id,
        id,
        file: entry.file,
        sha,
        nameHe: entry.labelHe,
        products: [{ id, name: entry.labelHe, score: null, grade: null, fields }],
      });
    } catch (err) {
      return NextResponse.json({ ok: false, error: "load_failed", detail: String(err) }, { status: 502 });
    }
  }

  if (kind === "page_chrome") {
    if (!slug) {
      return NextResponse.json({ ok: false, error: "unknown_slug" }, { status: 404 });
    }
    try {
      const { data, sha } = await getSiteContentFile(PAGE_CHROME_FILE);
      const pages = data as Record<string, Record<string, unknown>>;
      const chrome = pages[slug];
      if (!chrome) {
        return NextResponse.json({ ok: false, error: "unknown_slug" }, { status: 404 });
      }
      const fields = extractPageChromeFields(chrome);
      const nameHe =
        typeof chrome.metadata === "object" && chrome.metadata && typeof (chrome.metadata as Record<string, unknown>).title === "string"
          ? ((chrome.metadata as Record<string, unknown>).title as string)
          : slug;
      return NextResponse.json({
        ok: true,
        kind: "page_chrome",
        slug,
        file: PAGE_CHROME_FILE,
        sha,
        nameHe,
        products: [{ id: slug, name: nameHe, score: null, grade: null, fields }],
      });
    } catch (err) {
      return NextResponse.json({ ok: false, error: "load_failed", detail: String(err) }, { status: 502 });
    }
  }

  const file = LIVE_COMPARISON_FILES[slug];
  if (!file) {
    return NextResponse.json({ ok: false, error: "unknown_category" }, { status: 404 });
  }

  try {
    const { data, sha } = await getComparisonFile(file);
    const products = (data.products ?? []).map((p) => ({
      id: String(p.id ?? p.barcode ?? ""),
      name: typeof p.name === "string" ? p.name : "",
      score: p.score ?? null,
      grade: p.grade ?? null,
      fields: extractEditableFields(p),
    }));
    const nameHe =
      data._meta && typeof data._meta.name_he === "string" ? data._meta.name_he : slug;
    return NextResponse.json({ ok: true, kind: "comparison", slug, file, sha, nameHe, products });
  } catch (err) {
    return NextResponse.json(
      { ok: false, error: "load_failed", detail: String(err) },
      { status: 502 },
    );
  }
}
'''

save_route = r'''import { NextResponse } from "next/server";

import { isAuthed } from "@/lib/admin/auth";
import { applyProse, BLOG_DIR, blogDoc } from "@/lib/admin/blog";
import { getSiteContentEntry, PAGE_CHROME_FILE } from "@/lib/admin/content-registry";
import { applyEdits, LIVE_COMPARISON_FILES } from "@/lib/admin/fields";
import { applySiteEdits, extractPageChromeFields, extractSiteFields } from "@/lib/admin/site-fields";
import {
  getComparisonFile,
  getRepoJson,
  githubConfigured,
  putComparisonFile,
  putRepoJson,
  getSiteContentFile,
  putSiteContentFile,
} from "@/lib/admin/github";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * Body: { kind?: "comparison" | "blog" | "page_chrome" | "site", slug, edits: { [itemId]: { [path]: value } } }
 */
export async function POST(request: Request) {
  if (!(await isAuthed())) {
    return NextResponse.json({ ok: false, error: "unauthorized" }, { status: 401 });
  }
  if (!githubConfigured()) {
    return NextResponse.json({ ok: false, error: "github_not_configured" }, { status: 503 });
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ ok: false, error: "bad_request" }, { status: 400 });
  }
  if (!body || typeof body !== "object") {
    return NextResponse.json({ ok: false, error: "bad_request" }, { status: 400 });
  }

  const { slug, edits, kind } = body as { slug?: unknown; edits?: unknown; kind?: unknown };
  if (typeof slug !== "string") {
    return NextResponse.json({ ok: false, error: "bad_request" }, { status: 400 });
  }
  if (!edits || typeof edits !== "object") {
    return NextResponse.json({ ok: false, error: "no_edits" }, { status: 400 });
  }

  const docKind = typeof kind === "string" ? kind : "comparison";

  if (docKind === "blog") return saveBlog(slug, edits as Record<string, unknown>);
  if (docKind === "site") return saveSite(slug, edits as Record<string, unknown>);
  if (docKind === "page_chrome") return savePageChrome(slug, edits as Record<string, unknown>);
  return saveComparison(slug, edits as Record<string, unknown>);
}

async function saveBlog(slug: string, edits: Record<string, unknown>) {
  const doc = blogDoc(slug);
  if (!doc) {
    return NextResponse.json({ ok: false, error: "unknown_blog_doc" }, { status: 404 });
  }
  const repoPath = `${BLOG_DIR}/${doc.file}`;

  let data: Record<string, unknown>;
  let sha: string;
  try {
    ({ data, sha } = await getRepoJson(repoPath));
  } catch (err) {
    return NextResponse.json({ ok: false, error: "load_failed", detail: String(err) }, { status: 502 });
  }

  const fieldEdits = edits[slug];
  if (!fieldEdits || typeof fieldEdits !== "object") {
    return NextResponse.json({ ok: false, error: "no_edits" }, { status: 400 });
  }
  const result = applyProse(data, fieldEdits as Record<string, unknown>);
  if (result.applied === 0) {
    return NextResponse.json({ ok: false, error: "no_valid_edits", rejected: result.rejected }, { status: 400 });
  }

  const message = `Admin blog edit: ${slug} — ${result.applied} field(s) [TASK-350]`;
  try {
    const { commitSha } = await putRepoJson(repoPath, data, sha, message);
    return NextResponse.json({ ok: true, applied: result.applied, productsTouched: 1, rejected: result.rejected, commitSha });
  } catch (err) {
    return NextResponse.json({ ok: false, error: "commit_failed", detail: String(err) }, { status: 502 });
  }
}

async function saveSite(slug: string, edits: Record<string, unknown>) {
  const entry = getSiteContentEntry(slug);
  if (!entry) {
    return NextResponse.json({ ok: false, error: "unknown_site_id" }, { status: 404 });
  }
  let data: Record<string, unknown>;
  let sha: string;
  try {
    ({ data, sha } = await getSiteContentFile(entry.file));
  } catch (err) {
    return NextResponse.json({ ok: false, error: "load_failed", detail: String(err) }, { status: 502 });
  }
  const fieldEdits = edits[slug];
  if (!fieldEdits || typeof fieldEdits !== "object") {
    return NextResponse.json({ ok: false, error: "no_edits" }, { status: 400 });
  }
  const allowed = new Set(extractSiteFields(data).map((f) => f.path));
  const result = applySiteEdits(data, fieldEdits as Record<string, unknown>, allowed);
  if (result.applied === 0) {
    return NextResponse.json({ ok: false, error: "no_valid_edits", rejected: result.rejected }, { status: 400 });
  }
  const message = `Admin site edit: ${slug} — ${result.applied} field(s)`;
  try {
    const { commitSha } = await putSiteContentFile(entry.file, data, sha, message);
    return NextResponse.json({ ok: true, applied: result.applied, productsTouched: 1, rejected: result.rejected, commitSha });
  } catch (err) {
    return NextResponse.json({ ok: false, error: "commit_failed", detail: String(err) }, { status: 502 });
  }
}

async function savePageChrome(slug: string, edits: Record<string, unknown>) {
  let data: Record<string, unknown>;
  let sha: string;
  try {
    ({ data, sha } = await getSiteContentFile(PAGE_CHROME_FILE));
  } catch (err) {
    return NextResponse.json({ ok: false, error: "load_failed", detail: String(err) }, { status: 502 });
  }
  const pages = data as Record<string, Record<string, unknown>>;
  const chrome = pages[slug];
  if (!chrome) {
    return NextResponse.json({ ok: false, error: "unknown_slug" }, { status: 404 });
  }
  const fieldEdits = edits[slug];
  if (!fieldEdits || typeof fieldEdits !== "object") {
    return NextResponse.json({ ok: false, error: "no_edits" }, { status: 400 });
  }
  const allowed = new Set(extractPageChromeFields(chrome).map((f) => f.path));
  const result = applySiteEdits(chrome, fieldEdits as Record<string, unknown>, allowed);
  if (result.applied === 0) {
    return NextResponse.json({ ok: false, error: "no_valid_edits", rejected: result.rejected }, { status: 400 });
  }
  pages[slug] = chrome;
  const message = `Admin page chrome edit: ${slug} — ${result.applied} field(s)`;
  try {
    const { commitSha } = await putSiteContentFile(PAGE_CHROME_FILE, data, sha, message);
    return NextResponse.json({ ok: true, applied: result.applied, productsTouched: 1, rejected: result.rejected, commitSha });
  } catch (err) {
    return NextResponse.json({ ok: false, error: "commit_failed", detail: String(err) }, { status: 502 });
  }
}

async function saveComparison(slug: string, edits: Record<string, unknown>) {
  if (!LIVE_COMPARISON_FILES[slug]) {
    return NextResponse.json({ ok: false, error: "unknown_category" }, { status: 404 });
  }
  const file = LIVE_COMPARISON_FILES[slug];

  let data: Awaited<ReturnType<typeof getComparisonFile>>["data"];
  let sha: string;
  try {
    ({ data, sha } = await getComparisonFile(file));
  } catch (err) {
    return NextResponse.json({ ok: false, error: "load_failed", detail: String(err) }, { status: 502 });
  }

  const products = data.products ?? [];
  const index = new Map<string, Record<string, unknown>>();
  for (const p of products) index.set(String(p.id ?? p.barcode ?? ""), p);

  let applied = 0;
  let productsTouched = 0;
  const rejected: string[] = [];

  for (const [productId, rawFieldEdits] of Object.entries(edits)) {
    const product = index.get(productId);
    if (!product) {
      rejected.push(`product:${productId}`);
      continue;
    }
    if (!rawFieldEdits || typeof rawFieldEdits !== "object") {
      rejected.push(`product:${productId}:bad_shape`);
      continue;
    }
    const result = applyEdits(product, rawFieldEdits as Record<string, unknown>);
    applied += result.applied;
    rejected.push(...result.rejected.map((path) => `${productId}:${path}`));
    if (result.applied > 0) productsTouched += 1;
  }

  if (applied === 0) {
    return NextResponse.json({ ok: false, error: "no_valid_edits", rejected }, { status: 400 });
  }

  const message = `Admin copy edit: ${slug} — ${applied} field(s) across ${productsTouched} product(s) [TASK-340]`;
  try {
    const { commitSha } = await putComparisonFile(file, data, sha, message);
    return NextResponse.json({ ok: true, applied, productsTouched, rejected, commitSha });
  } catch (err) {
    return NextResponse.json({ ok: false, error: "commit_failed", detail: String(err) }, { status: 502 });
  }
}
'''

files = {
    ROOT / "src/lib/admin/content-registry.ts": content_registry,
    ROOT / "src/app/api/admin/categories/route.ts": categories,
    ROOT / "src/app/api/admin/load/route.ts": load_route,
    ROOT / "src/app/api/admin/save/route.ts": save_route,
}

for path, text in files.items():
    path.write_text(text.lstrip("\n"), encoding="utf-8")
    print("wrote", path.relative_to(ROOT))