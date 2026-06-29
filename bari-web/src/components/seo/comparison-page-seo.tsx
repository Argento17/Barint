import { JsonLdScript } from "@/components/seo/json-ld-script";
import { getFaqSchema } from "@/lib/seo/faq-registry";
import { buildItemListSchema } from "@/lib/seo/item-list-schema";
import type { BariProductVM } from "@/lib/view-models";

export function ComparisonPageSeo({
  pagePath,
  faqKey,
  products,
}: {
  pagePath: string;
  faqKey?: string;
  products: BariProductVM[];
}) {
  const faq = getFaqSchema(faqKey);
  const itemList = buildItemListSchema(products, pagePath);

  return (
    <>
      {faq ? <JsonLdScript data={faq} /> : null}
      <JsonLdScript data={itemList} />
      <section className="sr-only" aria-label="Product index for search">
        <h2>Products on this comparison</h2>
        <ul>
          {products.map((product) => {
            const qs = new URLSearchParams({ product: product.id }).toString();
            const href = `${pagePath}?${qs}`;
            return (
              <li key={product.id}>
                <a href={href}>{product.name}</a>
                {product.score != null ? (
                  <span>
                    {" "}
                    — Bari score {product.score}
                    {product.grade ? `, grade ${product.grade}` : ""}
                  </span>
                ) : null}
                {product.insightLine ? <p>{product.insightLine}</p> : null}
              </li>
            );
          })}
        </ul>
      </section>
    </>
  );
}
