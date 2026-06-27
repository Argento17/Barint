import type { BariProductVM } from "@/lib/view-models";

const DASH_SEPARATORS = [" \u2014 ", " \u2013 ", " - "] as const;

function escapeRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

export function stripBrandFromName(name: string, brand: string): string {
  const trimmedName = name.trim();
  const trimmedBrand = brand.trim();
  if (!trimmedName || !trimmedBrand) return trimmedName;

  const nameLower = trimmedName.toLowerCase();
  const brandLower = trimmedBrand.toLowerCase();

  for (const sep of DASH_SEPARATORS) {
    const suffix = `${sep}${trimmedBrand}`;
    if (nameLower.endsWith(suffix.toLowerCase())) {
      return trimmedName.slice(0, -suffix.length).trim();
    }
  }

  if (nameLower.startsWith(brandLower)) {
    const rest = trimmedName.slice(trimmedBrand.length).trim();
    const withoutSep = rest.replace(/^[\s:\u060C\-–—]+/, "").trim();
    if (withoutSep) return withoutSep;
  }

  // Brand token embedded mid-title (e.g. "בריסטה אלפרו 500").
  const inline = new RegExp(`\\s+${escapeRegExp(trimmedBrand)}(?=\\s|$)`, "i");
  if (inline.test(trimmedName)) {
    const cleaned = trimmedName.replace(inline, "").replace(/\s+/g, " ").trim();
    if (cleaned) return cleaned;
  }

  return trimmedName;
}

export function normalizeProductBrandDisplay(product: BariProductVM): BariProductVM {
  const brand = product.brand?.trim();
  if (!brand) return product;

  const name = stripBrandFromName(product.name, brand);
  if (name === product.name) return product;

  return { ...product, name };
}
