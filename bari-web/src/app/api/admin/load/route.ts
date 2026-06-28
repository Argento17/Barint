import { NextResponse } from "next/server";

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
