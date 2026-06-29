import { NextResponse } from "next/server";

import { getCorpusBySlug, listPublicCorpusSlugs } from "@/lib/seo/public-corpus-registry";

export const revalidate = 3600;

type Params = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return listPublicCorpusSlugs().map((slug) => ({ slug }));
}

export async function GET(_request: Request, { params }: Params) {
  const { slug } = await params;
  const corpus = getCorpusBySlug(slug);
  if (!corpus) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
  return NextResponse.json(corpus, {
    headers: {
      "Cache-Control": "public, max-age=3600",
    },
  });
}
