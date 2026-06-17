/**
 * Strips the internal `_bari_meta` block from a generated FAQ schema
 * and serialises it for safe inline injection as a JSON-LD script tag.
 *
 * Usage in a Server Component:
 *   import rawFaqSchema from "@/data/seo/cheese_faq_schema.json";
 *   <script type="application/ld+json"
 *     dangerouslySetInnerHTML={{ __html: buildFaqScript(rawFaqSchema) }} />
 */
export function buildFaqScript(raw: Record<string, unknown>): string {
  const { _bari_meta: _dropped, ...schema } = raw;
  return JSON.stringify(schema);
}
