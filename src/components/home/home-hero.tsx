import { BookOpen, ChevronLeft } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

import { heroTrust } from "./content";
import { HomeContainer } from "./section-frame";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

export function HomeHero() {
  return (
    <section
      className={cn(
        "relative flex min-h-[82vh] items-center overflow-hidden",
        siteHeaderOffsetClass
      )}
    >
      <div
        className="pointer-events-none absolute inset-x-0 top-0 -z-10 h-full max-h-[44rem] bg-gradient-to-b from-zinc-100/55 via-zinc-50/15 to-transparent"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute -end-24 top-8 -z-10 size-[28rem] rounded-full bg-emerald-200/20 blur-3xl"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute -start-16 top-24 -z-10 size-[22rem] rounded-full bg-sky-100/35 blur-3xl"
        aria-hidden
      />
      <HomeContainer className="py-16 md:py-20">
        <div className="mx-auto max-w-5xl text-center">
          <Badge
            variant="outline"
            className="mb-6 inline-flex items-center gap-2 rounded-full border-emerald-200/80 bg-gradient-to-l from-emerald-50 to-green-50 px-4 py-2 text-sm font-medium text-emerald-800 shadow-sm"
          >
            <BookOpen className="size-4 shrink-0" aria-hidden />
            השוואות, דירוגים ומדריכי מזון מבוססי מקורות
          </Badge>

          <h1 className="text-balance bg-gradient-to-l from-zinc-900 via-zinc-800 to-zinc-900 bg-clip-text text-4xl font-extrabold leading-[1.1] tracking-tight text-transparent sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl">
            אינטליגנציית מזון ישראלית
          </h1>

          <p className="mx-auto mt-6 max-w-3xl text-pretty text-lg leading-relaxed text-zinc-600 md:text-xl md:leading-relaxed">
            Bari בודקת אלפי מוצרים בעזרת אלגוריתמים, מזהה דפוסים תזונתיים, משווה בין מוצרים
            ומדרגת אוכל בצורה שקופה ומבוססת נתונים.
          </p>

          <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row sm:gap-4">
            <Button
              size="lg"
              className="group h-12 w-full rounded-2xl bg-gradient-to-l from-emerald-600 to-emerald-700 px-8 text-base font-semibold text-white shadow-lg shadow-emerald-600/25 transition hover:-translate-y-0.5 hover:shadow-xl sm:w-auto"
              asChild
            >
              <a href="#comparisons" className="inline-flex items-center justify-center gap-2">
                עיינו בדירוגים
                <ChevronLeft
                  className="size-5 transition-transform group-hover:-translate-x-0.5"
                  aria-hidden
                />
              </a>
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="h-12 w-full rounded-2xl border-zinc-200 bg-white/80 px-8 text-base font-semibold text-zinc-800 shadow-sm backdrop-blur-sm transition hover:-translate-y-0.5 hover:bg-white sm:w-auto"
              asChild
            >
              <a href="#comparisons">גלו השוואות</a>
            </Button>
          </div>

          <div className="mx-auto mt-14 flex max-w-3xl flex-wrap items-center justify-center gap-x-8 gap-y-4 text-sm text-zinc-600">
            {heroTrust.map((item) => {
              const Icon = item.icon;
              return (
                <div key={item.label} className="flex items-center gap-2">
                  <Icon className="size-5 shrink-0 text-emerald-600" aria-hidden />
                  <span className="font-medium">{item.label}</span>
                </div>
              );
            })}
          </div>
        </div>
      </HomeContainer>
    </section>
  );
}
