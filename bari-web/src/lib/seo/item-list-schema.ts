import { absoluteUrl } from "@/lib/site-url";
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
