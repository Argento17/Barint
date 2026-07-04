import { absoluteUrl, SITE_URL } from "@/lib/site-url";
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

      // A scored product is expressed as a schema.org Product carrying Bari's
      // editorial rating as a `review`. Google requires a Product to specify at
      // least one of offers / review / aggregateRating; the Bari score IS that
      // review — an independent third-party evaluation, which schema.org and
      // Google's review-snippet policy both permit (the self-serving-review ban
      // only covers a merchant rating its own goods). The rating mirrors the
      // score already published on the page; it is not a new claim.
      // Bari's scale is 0–100 (integer, already rounded).
      const item =
        product.score != null
          ? {
              "@type": "Product",
              name: product.name,
              ...(product.brand ? { brand: { "@type": "Brand", name: product.brand } } : {}),
              url: productUrl,
              review: {
                "@type": "Review",
                reviewRating: {
                  "@type": "Rating",
                  ratingValue: product.score,
                  bestRating: 100,
                  worstRating: 0,
                },
                author: {
                  "@type": "Organization",
                  name: "Bari",
                  url: SITE_URL,
                },
              },
              ...(additionalProperty.length ? { additionalProperty } : {}),
            }
          : {
              // Unscored product: no rating exists, so it must NOT be typed as a
              // Product (that would re-trigger the "offers/review/aggregateRating
              // required" error). A plain Thing carries name + url with no
              // required fields.
              "@type": "Thing",
              name: product.name,
              url: productUrl,
            };

      return {
        "@type": "ListItem",
        position: index + 1,
        item,
      };
    }),
  };
}
