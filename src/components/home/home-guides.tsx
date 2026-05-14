import { ChevronLeft } from "lucide-react";

import { guides } from "./content";
import { HomeContainer, SectionHeading } from "./section-frame";

export function HomeGuides() {
  return (
    <section className="bg-zinc-50 py-16 md:py-20" id="guides">
      <HomeContainer>
        <SectionHeading
          title="ניתוחים אחרונים"
          description="תכנים חדשים שמתפרסמים באופן קבוע — דירוגים, מדריכים והשוואות."
        />

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 lg:gap-5">
          {guides.map((article) => {
            const Icon = article.icon;
            return (
              <article
                key={article.title}
                className="group cursor-pointer rounded-2xl border border-zinc-200/60 bg-white p-6 shadow-sm transition duration-300 hover:-translate-y-1 hover:shadow-lg"
              >
                <div className="mb-4 flex size-12 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-500 to-emerald-600 shadow-sm transition-transform group-hover:scale-105">
                  <Icon className="size-6 text-white" aria-hidden />
                </div>
                <div className="mb-2 flex flex-wrap items-center gap-2 text-xs font-semibold text-emerald-600">
                  <span>{article.type}</span>
                  <span className="text-zinc-300">•</span>
                  <span className="font-medium text-zinc-500">{article.time}</span>
                </div>
                <h3 className="mb-3 text-lg font-semibold text-zinc-900">{article.title}</h3>
                <div className="inline-flex items-center gap-1 text-sm font-semibold text-emerald-600 transition-all group-hover:gap-2">
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
