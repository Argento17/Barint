import { toJsonLdScript } from "@/lib/seo/json-ld";

/** @deprecated Use getFaqSchema + JsonLdScript or toJsonLdScript directly. */
export function buildFaqScript(raw: Record<string, unknown>): string {
  const { _bari_meta: _dropped, ...schema } = raw;
  void _dropped;
  return toJsonLdScript(schema);
}
