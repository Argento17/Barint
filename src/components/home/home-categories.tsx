import { ChevronLeft } from "lucide-react";

import { categories } from "./content";
import { HomeContainer, SectionHeading } from "./section-frame";

const signalLabels = ["עיבוד", "שונות", "תוספים"] as const;

export function HomeCategories() {
  return (
    <section className="relative py-16 md:py-20" id="categories">
      <HomeContainer>
        <SectionHeading
          title="תחומי ניתוח"
          description="כל קטגוריה היא מרחב השוואה עם דפוסי רכיבים, עיבוד וציפיות תזונתיות משלה."
        />

        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 md:grid-cols-4 md:gap-4">
          {categories.map((category) => {
            const Icon = category.icon;
            return (
              <a
                key={category.name}
                href={category.href}
                className="group relative min-h-[14.5rem] overflow-hidden rounded-[1.65rem] border border-stone-200/80 bg-white/90 p-5 shadow-sm shadow-zinc-950/[0.025] transition-[border-color,box-shadow,transform,background-color] duration-500 ease-out hover:-translate-y-0.5 hover:border-emerald-900/15 hover:bg-white hover:shadow-[0_22px_68px_-52px_rgba(24,24,27,0.5)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-800/20 md:p-5"
              >
                <div
                  className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_82%_8%,rgba(4,120,87,0.075),transparent_34%),linear-gradient(135deg,rgba(245,245,244,0.9),rgba(255,255,255,0.25)_44%,rgba(236,253,245,0.24))] opacity-80 transition-opacity duration-500 group-hover:opacity-100"
                  aria-hidden
                />
                <div
                  className="pointer-events-none absolute inset-0 opacity-[0.035] mix-blend-multiply"
                  style={{
                    backgroundImage:
                      "linear-gradient(rgba(24,24,27,0.55) 1px, transparent 1px), linear-gradient(90deg, rgba(24,24,27,0.55) 1px, transparent 1px)",
                    backgroundSize: "28px 28px",
                  }}
                  aria-hidden
                />
                <div
                  className="pointer-events-none absolute -end-16 -top-16 size-36 rounded-full bg-white/90 blur-3xl transition-transform duration-700 ease-out group-hover:-translate-x-3 group-hover:translate-y-2"
                  aria-hidden
                />
                <div
                  className="pointer-events-none absolute inset-x-5 bottom-0 h-20 rounded-t-full bg-gradient-to-t from-zinc-950/[0.035] to-transparent opacity-60"
                  aria-hidden
                />

                <div className="relative z-10 flex h-full flex-col">
                  <div className="mb-5 flex items-start justify-between gap-3">
                    <div
                      className="flex size-11 items-center justify-center rounded-2xl border border-stone-200/80 bg-white/75 text-zinc-800 shadow-sm shadow-zinc-950/[0.025] backdrop-blur-sm transition-[transform,border-color,background-color,color] duration-500 ease-out group-hover:-translate-y-0.5 group-hover:border-emerald-900/15 group-hover:bg-emerald-50/70 group-hover:text-emerald-900 md:size-12"
                    >
                      <Icon
                        className="size-5 transition-transform duration-500 ease-out group-hover:scale-105"
                        aria-hidden
                      />
                    </div>
                    <div className="rounded-full border border-stone-200/80 bg-white/75 px-2.5 py-1 text-[0.68rem] font-bold text-zinc-500 shadow-sm shadow-zinc-950/[0.02] backdrop-blur-sm">
                      {category.products}
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-extrabold tracking-[-0.035em] text-zinc-950 md:text-xl">
                      {category.name}
                    </h3>
                    <p className="mt-2 min-h-10 text-sm leading-relaxed text-zinc-600">
                      {category.insight}
                    </p>
                  </div>

                  <div className="mt-auto pt-6">
                    <div className="space-y-2.5">
                      {category.signals.map((value, index) => (
                        <div key={signalLabels[index]} className="grid grid-cols-[3.2rem_1fr] items-center gap-2">
                          <span className="text-[0.68rem] font-semibold text-zinc-500">
                            {signalLabels[index]}
                          </span>
                          <span className="relative h-1.5 overflow-hidden rounded-full bg-stone-200/80 shadow-inner shadow-zinc-950/[0.035]">
                            <span
                              className="absolute inset-y-0 end-0 rounded-full bg-zinc-800 transition-[width,background-color] duration-700 ease-out group-hover:bg-emerald-800"
                              style={{ width: `${value}%` }}
                            />
                          </span>
                        </div>
                      ))}
                    </div>

                    <div className="mt-5 flex items-center justify-between gap-3 text-sm">
                      <span className="font-semibold text-zinc-700 transition-colors duration-300 group-hover:text-zinc-950">
                        תחום אנליטי
                      </span>
                      <span className="flex items-center gap-1 font-bold text-emerald-800">
                        עיינו
                        <ChevronLeft
                          className="size-4 transition-transform duration-300 group-hover:-translate-x-1"
                          aria-hidden
                        />
                      </span>
                    </div>
                  </div>
                </div>

                <div
                  className="pointer-events-none absolute inset-0 rounded-[1.65rem] shadow-[inset_0_1px_0_rgba(255,255,255,0.7),inset_0_-1px_0_rgba(24,24,27,0.04)]"
                  aria-hidden
                />
              </a>
            );
          })}
        </div>
      </HomeContainer>
    </section>
  );
}
