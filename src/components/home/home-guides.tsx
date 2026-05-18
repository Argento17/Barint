import { ChevronLeft } from "lucide-react";

import { guides } from "./content";
import { HomeContainer } from "./section-frame";

export function HomeGuides() {
  return (
    <section className="relative overflow-hidden bg-[#F7F7F2] py-16 md:py-20" id="guides">
      <div
        className="pointer-events-none absolute inset-0 bg-transparent"
        aria-hidden
      />
      <HomeContainer>
        <div className="relative mx-auto mb-10 max-w-3xl text-center md:mb-12">
          <p className="text-xs font-bold uppercase tracking-[0.22em] text-[#1F8F6A]/80">Food intelligence briefings</p>
          <h2 className="mt-3 text-balance text-3xl font-extrabold tracking-[-0.045em] text-[#111318] md:text-5xl">
            ניתוחים אחרונים
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-base leading-relaxed text-[#4E5663] md:text-lg">
            דירוגים, מדריכים והשוואות שמתרגמים מוצרי מזון לאותות ברורים.
          </p>
        </div>

        <div className="relative grid gap-4 sm:grid-cols-2 lg:grid-cols-4 lg:gap-5">
          {guides.map((article) => {
            const Icon = article.icon;
            return (
              <article
                key={article.title}
                className="group cursor-pointer rounded-[1.45rem] border border-black/[0.08] bg-[#FFFFFF]/68 p-6 text-[#111318] shadow-[0_24px_78px_-62px_rgba(17,19,24,0.78)] backdrop-blur-xl transition duration-300 hover:-translate-y-1 hover:border-[#1F8F6A]/22"
              >
                <div className="mb-4 flex size-12 items-center justify-center rounded-2xl border border-black/[0.08] bg-[#1F8F6A]/[0.035] text-[#1F8F6A] shadow-sm transition-transform group-hover:scale-105">
                  <Icon className="size-6" aria-hidden />
                </div>
                <div className="mb-2 flex flex-wrap items-center gap-2 text-xs font-semibold text-[#1F8F6A]/85">
                  <span>{article.type}</span>
                  <span className="text-[#7A817C]">•</span>
                  <span className="font-medium text-[#7A817C]">{article.time}</span>
                </div>
                <h3 className="mb-3 text-lg font-semibold text-[#111318]">{article.title}</h3>
                <div className="inline-flex items-center gap-1 text-sm font-semibold text-[#1F8F6A] transition-all group-hover:gap-2">
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
