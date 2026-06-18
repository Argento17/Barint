"use client";

import { CheckCircle2, XCircle } from "lucide-react";

import { HomeContainer } from "@/components/home/section-frame";
import { breadArticle } from "@/lib/blog/bread-article-content";

/**
 * BreadKeyProductMatrix — comparison table of 8 key products.
 * Data: breadArticle.keyProductMatrix — all rows from the scored corpus.
 * Corpus: Shufersal only. Display-only: no filtering or augmentation.
 */
export function BreadKeyProductMatrix() {
  const { keyProductMatrix } = breadArticle;

  return (
    <HomeContainer className="py-10 md:py-14">
      <div className="mx-auto max-w-4xl">
        <header className="mb-6 text-right">
          <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
            השוואת מוצרים נבחרים
          </p>
          <h2 className="mt-2 text-2xl font-extrabold tracking-tighter text-[#111318] md:text-3xl">
            {keyProductMatrix.title}
          </h2>
          <p className="mt-2 text-sm leading-relaxed text-[#4E5663]">
            {keyProductMatrix.subtitle}
          </p>
        </header>

        <div className="overflow-x-auto">
          <table
            className="w-full min-w-[44rem] border-collapse text-right"
            dir="rtl"
          >
            <thead>
              <tr className="border-b border-black/[0.09]">
                <th className="pb-3 pl-4 text-right text-[0.65rem] font-bold uppercase tracking-[0.16em] text-[#7A817C]">
                  מוצר
                </th>
                <th className="pb-3 pl-3 text-center text-[0.65rem] font-bold uppercase tracking-[0.16em] text-[#7A817C]">
                  ציון
                </th>
                <th className="pb-3 pl-3 text-center text-[0.65rem] font-bold uppercase tracking-[0.16em] text-[#7A817C]">
                  סיבים
                </th>
                <th className="pb-3 pl-3 text-center text-[0.65rem] font-bold uppercase tracking-[0.16em] text-[#7A817C]">
                  מחמצת אמיתית
                </th>
                <th className="pb-3 pl-3 text-center text-[0.65rem] font-bold uppercase tracking-[0.16em] text-[#7A817C]">
                  דגן מלא
                </th>
                <th className="pb-3 text-right text-[0.65rem] font-bold uppercase tracking-[0.16em] text-[#7A817C]">
                  הערה
                </th>
              </tr>
            </thead>
            <tbody>
              {keyProductMatrix.products.map((product, i) => {
                const isA = product.score.includes("A");
                return (
                  <tr
                    key={product.name}
                    className={`border-b border-black/[0.05] ${
                      i % 2 === 0 ? "bg-[#F7F7F2]/60" : "bg-[#FFFFFF]"
                    }`}
                  >
                    <td className="py-3 pl-4 text-sm font-semibold text-[#111318]">
                      {product.name}
                    </td>
                    <td className="py-3 pl-3 text-center">
                      <span
                        className={`inline-block rounded px-2 py-0.5 text-xs font-extrabold ${
                          isA
                            ? "bg-[#7A9450]/12 text-[#7A9450]"
                            : "bg-[#4E5663]/10 text-[#4E5663]"
                        }`}
                      >
                        {product.score}
                      </span>
                    </td>
                    <td className="py-3 pl-3 text-center text-sm text-[#111318]">
                      {product.fiber}
                    </td>
                    <td className="py-3 pl-3 text-center">
                      {product.fermentation ? (
                        <CheckCircle2 className="mx-auto size-4 text-[#7A9450]" aria-label="כן" />
                      ) : (
                        <XCircle className="mx-auto size-4 text-[#9B1C1C]/70" aria-label="לא" />
                      )}
                    </td>
                    <td className="py-3 pl-3 text-center">
                      {product.wholeGrainBase ? (
                        <CheckCircle2 className="mx-auto size-4 text-[#7A9450]" aria-label="כן" />
                      ) : (
                        <XCircle className="mx-auto size-4 text-[#9B1C1C]/70" aria-label="לא" />
                      )}
                    </td>
                    <td className="py-3 text-right text-xs leading-relaxed text-[#7A817C]">
                      {product.note}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        <p className="mt-4 text-xs leading-relaxed text-[#7A817C]">
          נתוני ציון מתוך הניתוח של מדף שופרסל (מאי–יוני 2026, 24 מוצרים). נתוני סיבים ל-100 גרם. מחמצת אמיתית = מחמצת מאומתת כרכיב ברשימת הרכיבים.
        </p>
      </div>
    </HomeContainer>
  );
}
