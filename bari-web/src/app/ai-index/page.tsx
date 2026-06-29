import type { Metadata } from "next";
import Link from "next/link";

import { buildProductsIndex } from "@/lib/seo/products-index";
import { listPublicCorpusSlugs } from "@/lib/seo/public-corpus-registry";
import { absoluteUrl } from "@/lib/site-url";

export const metadata: Metadata = {
  title: "מפת נתונים לסוכני AI — Bari",
  description:
    "קישורים למקורות נתונים ציבוריים של Bari: השוואות מוצרים, אינדקס מוצרים ומפת אתר.",
  robots: { index: true, follow: true },
};

export default function AiIndexPage() {
  const slugs = listPublicCorpusSlugs();
  const productCount = buildProductsIndex().length;

  const resources = [
    { href: "/llms.txt", label: "llms.txt", note: "סיכום אתר לסוכני שפה" },
    {
      href: "/data/products.json",
      label: "products.json",
      note: `אינדקס שטוח של ${productCount} מוצרים`,
    },
    { href: "/sitemap.xml", label: "sitemap.xml", note: "מפת אתר" },
  ] as const;

  return (
    <div dir="rtl" className="mx-auto max-w-2xl px-4 py-12 text-right">
      <h1 className="text-2xl font-extrabold tracking-[-0.03em] text-[#111318]">
        מפת נתונים לסוכני AI
      </h1>
      <p className="mt-2 text-[14px] leading-relaxed text-[#4E5663]">
        עמוד זה מרכז את מקורות הנתונים הציבוריים של Bari לקריאה אוטומטית. הציון המספרי והציון האותי הם מוצר עריכה של מנוע Bari; מרכיבים ותזונה מגיעים מתוויות
        מוצר בלבד.
      </p>

      <section className="mt-8">
        <h2 className="mb-3 text-base font-bold text-[#111318]">מקורות מרכזיים</h2>
        <ul className="space-y-3 text-[14px] text-[#4E5663]">
          {resources.map((item) => (
            <li key={item.href}>
              <Link
                href={item.href}
                className="font-semibold text-[#167A58] underline-offset-2 hover:underline"
              >
                {item.label}
              </Link>
              <span className="text-[#6B7070]"> — {item.note}</span>
              <div className="mt-0.5 text-[12px] text-[#6B7070] ltr:text-left" dir="ltr">
                {absoluteUrl(item.href)}
              </div>
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-10">
        <h2 className="mb-3 text-base font-bold text-[#111318]">קטגוריות השוואה</h2>
        <ul className="space-y-4 text-[14px] text-[#4E5663]">
          {slugs.map((slug) => (
            <li key={slug}>
              <div className="font-semibold text-[#111318]">{slug}</div>
              <div className="mt-1 flex flex-wrap gap-x-4 gap-y-1">
                <Link
                  href={`/hashvaot/${slug}`}
                  className="text-[#167A58] underline-offset-2 hover:underline"
                >
                  דף השוואה
                </Link>
                <Link
                  href={`/data/comparisons/${slug}`}
                  className="text-[#167A58] underline-offset-2 hover:underline"
                >
                  JSON לקטגוריה
                </Link>
              </div>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
