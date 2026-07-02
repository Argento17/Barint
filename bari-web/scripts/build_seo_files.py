# -*- coding: utf-8 -*-
"""One-shot writer for SEO discoverability files."""
from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def w(rel: str, content: str) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8", newline="\n")
    print("wrote", rel)


def main() -> None:
    w(
        "src/lib/seo/faq-registry.ts",
        """import breadFaq from "@/data/seo/bread_faq_schema.json";
import breakfastCerealsFaq from "@/data/seo/breakfast_cereals_faq_schema.json";
import brinedCheesesFaq from "@/data/seo/brined_cheeses_faq_schema.json";
import cookiesCoffeeFaq from "@/data/seo/cookies_coffee_faq_schema.json";
import granolaFaq from "@/data/seo/granola_faq_schema.json";
import hardCheesesFaq from "@/data/seo/hard_cheeses_faq_schema.json";
import hummusFaq from "@/data/seo/hummus_faq_schema.json";
import juicesFaq from "@/data/seo/juices_faq_schema.json";

const FAQ_BY_KEY: Record<string, Record<string, unknown>> = {
  bread: breadFaq as Record<string, unknown>,
  breakfast_cereals: breakfastCerealsFaq as Record<string, unknown>,
  brined_cheeses: brinedCheesesFaq as Record<string, unknown>,
  cookies_coffee: cookiesCoffeeFaq as Record<string, unknown>,
  granola: granolaFaq as Record<string, unknown>,
  hard_cheeses: hardCheesesFaq as Record<string, unknown>,
  hummus: hummusFaq as Record<string, unknown>,
  juices: juicesFaq as Record<string, unknown>,
};

export function getFaqSchema(faqKey: string | undefined): Record<string, unknown> | null {
  if (!faqKey) return null;
  const raw = FAQ_BY_KEY[faqKey];
  if (!raw) return null;
  const { _bari_meta: _dropped, ...schema } = raw;
  void _dropped;
  return schema;
}
""",
    )

    w(
        "src/lib/seo/item-list-schema.ts",
        """import { absoluteUrl } from "@/lib/site-url";
import type { BariProductVM } from "@/lib/view-models";

export function buildItemListSchema(products: BariProductVM[], pageUrl: string) {
  const page = pageUrl.startsWith("http") ? pageUrl : absoluteUrl(pageUrl);
  return {
    "@context": "https://schema.org",
    "@type": "ItemList",
    url: page,
    numberOfItems: products.length,
    itemListElement: products.map((product, index) => {
      const qs = new URLSearchParams({ product: product.id }).toString();
      const productUrl = `${page}?${qs}`;
      const additionalProperty: {
        "@type": "PropertyValue";
        name: string;
        value: string | number;
      }[] = [];
      if (product.score != null) {
        additionalProperty.push({ "@type": "PropertyValue", name: "Bari score", value: product.score });
      }
      if (product.grade) {
        additionalProperty.push({ "@type": "PropertyValue", name: "Bari grade", value: product.grade });
      }
      return {
        "@type": "ListItem",
        position: index + 1,
        item: {
          "@type": "Product",
          name: product.name,
          ...(product.brand ? { brand: { "@type": "Brand", name: product.brand } } : {}),
          url: productUrl,
          ...(additionalProperty.length ? { additionalProperty } : {}),
        },
      };
    }),
  };
}
""",
    )

    w(
        "src/lib/seo/article-schema.ts",
        """import { absoluteUrl } from "@/lib/site-url";

export function buildArticleSchema({
  title,
  description,
  url,
  datePublished,
  inLanguage = "he",
}: {
  title: string;
  description: string;
  url: string;
  datePublished?: string;
  inLanguage?: string;
}) {
  const pageUrl = url.startsWith("http") ? url : absoluteUrl(url);
  return {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: title,
    description,
    url: pageUrl,
    mainEntityOfPage: pageUrl,
    inLanguage,
    publisher: {
      "@type": "Organization",
      name: "Bari",
      url: absoluteUrl("/"),
    },
    ...(datePublished ? { datePublished } : {}),
  };
}
""",
    )

    w(
        "src/lib/seo/organization-schema.ts",
        """import { SITE_URL, absoluteUrl } from "@/lib/site-url";

export function buildOrganizationSchema() {
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "Bari",
    url: SITE_URL,
    logo: absoluteUrl("/favicon.ico"),
  };
}

export function buildWebSiteSchema() {
  return {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "Bari",
    url: SITE_URL,
    inLanguage: "he",
  };
}

export function buildSiteJsonLd() {
  return [buildOrganizationSchema(), buildWebSiteSchema()];
}
""",
    )

    print("batch1 done")


if __name__ == "__main__":
    main()
