import { ChevronLeft } from "lucide-react";

import { guides } from "./content";
import { HomeContainer } from "./section-frame";

export function HomeGuides() {
  return (
    <section className="relative overflow-hidden py-16 md:py-20" id="guides">
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_84%_24%,rgba(16,185,129,0.07),transparent_32%)]"
        aria-hidden
      />
      <HomeContainer>
        <div className="relative mx-auto mb-10 max-w-3xl text-center md:mb-12">
          <p className="text-xs font-bold uppercase tracking-[0.22em] text-emerald-200/80">Food intelligence briefings</p>
          <h2 className="mt-3 text-balance text-3xl font-extrabold tracking-[-0.045em] text-white md:text-5xl">
            ניתוחים אחרונים
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-base leading-relaxed text-zinc-400 md:text-lg">
            דירוגים, מדריכים והשוואות שמתרגמים מוצרי מזון לאותות ברורים.
          </p>
        </div>

        <div className="relative grid gap-4 sm:grid-cols-2 lg:grid-cols-4 lg:gap-5">
          {guides.map((article) => {
            const Icon = article.icon;
            return (
              <article
                key={article.title}
                className="group cursor-pointer rounded-[1.45rem] border border-emerald-300/10 bg-white/[0.045] p-6 text-white shadow-[0_24px_78px_-62px_rgba(0,0,0,0.95)] backdrop-blur-xl transition duration-300 hover:-translate-y-1 hover:border-emerald-300/22"
              >
                <div className="mb-4 flex size-12 items-center justify-center rounded-2xl border border-emerald-300/12 bg-emerald-300/[0.055] text-emerald-200 shadow-sm transition-transform group-hover:scale-105">
                  <Icon className="size-6" aria-hidden />
                </div>
                <div className="mb-2 flex flex-wrap items-center gap-2 text-xs font-semibold text-emerald-200/85">
                  <span>{article.type}</span>
                  <span className="text-zinc-600">•</span>
                  <span className="font-medium text-zinc-500">{article.time}</span>
                </div>
                <h3 className="mb-3 text-lg font-semibold text-white">{article.title}</h3>
                <div className="inline-flex items-center gap-1 text-sm font-semibold text-emerald-200 transition-all group-hover:gap-2">
                  <span>קראו</span>
                  <ChevronLeft className="size-4" aria-hidden />
                </div>
              </article>
            );
          })}
        </div>
      </HomeContainer>
    </section>
  );
}
