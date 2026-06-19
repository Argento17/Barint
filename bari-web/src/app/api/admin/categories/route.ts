import { NextResponse } from "next/server";

import { isAuthed } from "@/lib/admin/auth";
import { LIVE_COMPARISON_FILES } from "@/lib/admin/fields";
import { getComparisonFile } from "@/lib/admin/github";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  if (!(await isAuthed())) {
    return NextResponse.json({ ok: false, error: "unauthorized" }, { status: 401 });
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
          nameHe: typeof meta.name_he === "string" ? meta.name_he : slug,
          productCount: (data.products ?? []).length,
        };
      } catch {
        return { slug, file, nameHe: slug, productCount: 0, unavailable: true };
      }
    }),
  );

  return NextResponse.json({ categories });
}
