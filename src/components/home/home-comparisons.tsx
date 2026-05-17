import { ChevronLeft, ShieldCheck } from "lucide-react";

import { Button } from "@/components/ui/button";

import { productComparisonExample } from "./content";
import { HomeContainer } from "./section-frame";

export function HomeComparisons() {
  return (
    <section className="relative py-16 md:py-20" id="comparisons">
      <HomeContainer>
        <div className="reveal-up mb-10 flex flex-col items-start justify-between gap-6 md:mb-12 md:flex-row md:items-end">
          <div className="max-w-2xl space-y-3 text-right">
            <h2 className="text-balance text-3xl font-bold tracking-tight text-zinc-900 md:text-4xl lg:text-5xl">
              דוגמה להשוואת מוצר
            </h2>
            <p className="text-pretty text-base text-zinc-600 md:text-lg">
              Bari משווה מוצרים דומים בתוך אותה קטגוריה ומסבירה למה אחד מהם מקבל עדיפות.
            </p>
          </div>
          <Button
            variant="ghost"
            className="hidden shrink-0 gap-2 text-emerald-700 hover:text-emerald-800 md:inline-flex"
            asChild
          >
            <a href="#guides" className="font-semibold">
              <span>כל התכנים</span>
              <ChevronLeft className="size-5" aria-hidden />
            </a>
          </Button>
        </div>

        <div className="reveal-up delay-100 overflow-hidden rounded-[2rem] border border-zinc-200/65 bg-white/85 shadow-[0_24px_80px_-56px_rgba(24,24,27,0.42)] backdrop-blur-sm">
          <div className="relative border-b border-zinc-200/60 bg-gradient-to-br from-zinc-950 via-zinc-900 to-emerald-950 px-6 py-6 text-white md:px-8">
            <div className="absolute end-6 top-6 rounded-full border border-emerald-300/25 bg-emerald-300/10 px-4 py-2 text-xs font-bold text-emerald-100 shadow-sm backdrop-blur-sm">
              {productComparisonExample.sticker}
            </div>
            <div className="max-w-2xl space-y-3">
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-emerald-200">
                Signal Review · {productComparisonExample.category}
              </p>
              <h3 className="text-2xl font-bold tracking-[-0.03em] md:text-4xl">
                חלב שיבולת שועל A מול חלב שיבולת שועל B
              </h3>
              <p className="text-sm leading-relaxed text-zinc-300 md:text-base">
                {productComparisonExample.summary}
              </p>
              <p className="text-xs font-medium text-zinc-400">{productComparisonExample.basis}</p>
            </div>
          </div>

          <div className="grid gap-0 md:grid-cols-2">
            {productComparisonExample.products.map((product, index) => (
              <div
                key={product.name}
                className={`group flex min-h-full flex-col gap-5 border-b border-zinc-200/60 p-6 transition-colors duration-500 hover:bg-zinc-50/70 md:border-b-0 md:p-7 ${
                  index === 0 ? "md:border-e md:border-zinc-200/60" : ""
                }`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="space-y-2">
                    <p className="text-xs font-semibold text-emerald-800">{product.label}</p>
                    <h4 className="text-2xl font-bold tracking-[-0.03em] text-zinc-950">
                      {product.name}
                    </h4>
                  </div>
                  <div className="rounded-2xl border border-zinc-200/70 bg-white px-4 py-3 text-center shadow-sm shadow-zinc-950/[0.03]">
                    <div className="text-lg font-bold text-zinc-950">{product.score}</div>
                    <div className="text-[0.68rem] font-semibold uppercase tracking-[0.16em] text-zinc-500">
                      ציון יחסי
                    </div>
                  </div>
                </div>

                <div className="space-y-2">
                  {product.signals.map((signal) => (
                    <div
                      key={signal}
                      className="flex items-center justify-between gap-3 rounded-2xl border border-zinc-200/65 bg-white/85 px-3 py-2.5 text-sm shadow-sm shadow-zinc-950/[0.02]"
                    >
                      <span className="font-medium text-zinc-700">{signal}</span>
                      <span
                        className={`size-1.5 rounded-full ${
                          product.tone === "preferred" ? "bg-emerald-800" : "bg-zinc-400"
                        }`}
                        aria-hidden
                      />
                    </div>
                  ))}
                </div>

                <p className="mt-auto rounded-2xl bg-zinc-950 px-4 py-3 text-sm leading-relaxed text-zinc-300">
                  {product.note}
                </p>
              </div>
            ))}
          </div>

          <div className="grid gap-3 border-t border-zinc-200/60 bg-zinc-50/70 p-5 md:grid-cols-3 md:p-6">
            {productComparisonExample.criteria.map((criterion) => (
              <div key={criterion.label} className="rounded-2xl bg-white px-4 py-3 shadow-sm shadow-zinc-950/[0.02]">
                <div className="mb-1 flex items-center justify-between gap-3 text-sm">
                  <span className="font-bold text-zinc-950">{criterion.label}</span>
                  <span className="font-semibold text-emerald-800">{criterion.winner}</span>
                </div>
                <p className="text-xs leading-relaxed text-zinc-500">{criterion.detail}</p>
              </div>
            ))}
            <div className="flex items-center gap-2 rounded-2xl bg-white px-4 py-3 text-xs font-medium text-zinc-500 shadow-sm shadow-zinc-950/[0.02] md:col-span-3">
              <ShieldCheck className="size-4 text-emerald-700" aria-hidden />
              דוגמה להמחשת חוויית המוצר. הנתונים מוצגים באופן איכותי עד לאימות מלא של מקורות.
            </div>
          </div>
        </div>
      </HomeContainer>
    </section>
  );
}
