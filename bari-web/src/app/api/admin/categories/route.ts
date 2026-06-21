import { NextResponse } from "next/server";

import { isAuthed } from "@/lib/admin/auth";
import { LIVE_BLOG_DOCS } from "@/lib/admin/blog";
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

  return NextResponse.json({ comparisons, blog });
}
