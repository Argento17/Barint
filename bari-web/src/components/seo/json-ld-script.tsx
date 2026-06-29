import { toJsonLdScript } from "@/lib/seo/json-ld";

export function JsonLdScript({ data }: { data: unknown }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: toJsonLdScript(data) }}
    />
  );
}
