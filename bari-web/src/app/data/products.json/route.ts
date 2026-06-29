import { NextResponse } from "next/server";

import { buildProductsIndex } from "@/lib/seo/products-index";

export const revalidate = 3600;

export function GET() {
  const body = buildProductsIndex();
  return NextResponse.json(body, {
    headers: {
      "Cache-Control": "public, max-age=3600",
    },
  });
}
