import { JsonLdScript } from "@/components/seo/json-ld-script";
import { buildArticleSchema } from "@/lib/seo/article-schema";

export function BlogArticleSeo({
  title,
  description,
  url,
  datePublished,
}: {
  title: string;
  description: string;
  url: string;
  datePublished?: string;
}) {
  return (
    <JsonLdScript
      data={buildArticleSchema({ title, description, url, datePublished })}
    />
  );
}
