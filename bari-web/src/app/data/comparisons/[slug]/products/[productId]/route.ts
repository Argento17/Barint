import { NextResponse } from "next/server";

import { getCorpusBySlug } from "@/lib/seo/public-corpus-registry";

export const revalidate = 3600;

type Params = { params: Promise<{ slug: string; productId: string }> };

export async function GET(_request: Request, { params }: Params) {
  const { slug, productId } = await params;
  const corpus = getCorpusBySlug(slug);
  if (!corpus) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
  const products = corpus.products as Array<{ id: string }>;
  const product = products.find((p) => p.id === productId);
  if (!product) {
    return NextResponse.json({ error: "Product not found" }, { status: 404 });
  }
  return NextResponse.json(product, {
    headers: {
      "Cache-Control": "public, max-age=3600",
    },
  });
}
