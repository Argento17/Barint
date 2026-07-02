import type { Metadata } from "next";

/** Matches root layout default OG card (`bari-web/src/app/layout.tsx`). */
export const DEFAULT_OG_IMAGE = {
  url: "/bari-logo-optimized.webp",
  width: 512,
  height: 512,
} as const;

export function blogOpenGraph(partial: {
  title: string;
  description: string;
  type?: "article";
}): NonNullable<Metadata["openGraph"]> {
  return {
    ...partial,
    type: partial.type ?? "article",
    images: [DEFAULT_OG_IMAGE],
  };
}

/** Derives og:title/og:description from existing page metadata strings only. */
export function comparisonOpenGraph(
  title: string,
  description: string
): NonNullable<Metadata["openGraph"]> {
  return {
    title,
    description,
    type: "website",
    locale: "he_IL",
  };
}

export function withComparisonOpenGraph(metadata: {
  title: string;
  description: string;
}): Metadata {
  return {
    ...metadata,
    openGraph: comparisonOpenGraph(metadata.title, metadata.description),
  };
}
