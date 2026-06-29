/** Safe JSON-LD serialization for inline script tags. */
export function toJsonLdScript(data: unknown): string {
  return JSON.stringify(data).replace(/</g, "\\u003c");
}
