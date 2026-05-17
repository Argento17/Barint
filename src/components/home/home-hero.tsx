import { ChevronLeft } from "lucide-react";

import { BariSignalMark } from "@/components/brand/bari-brand-logo";
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
        className="pointer-events-none absolute inset-x-0 top-0 -z-10 h-full max-h-[44rem] bg-gradient-to-b from-zinc-200/45 via-zinc-50/10 to-transparent"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute -end-24 top-8 -z-10 size-[28rem] rounded-full bg-emerald-900/10 blur-3xl"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute -start-16 top-24 -z-10 size-[22rem] rounded-full bg-zinc-950/[0.04] blur-3xl"
        aria-hidden
      />
      <HomeContainer className="py-[4.5rem] md:py-24">
        <div className="mx-auto max-w-5xl text-center">
          <Badge
            variant="outline"
            className="reveal-up mb-7 inline-flex items-center gap-2 rounded-full border-emerald-900/10 bg-white/60 px-4 py-2 text-sm font-semibold text-emerald-900 shadow-sm shadow-zinc-950/[0.03] backdrop-blur-sm"
          >
            <BariSignalMark className="size-4" />
            מערכת השוואות מזון מבוססת נתונים
          </Badge>

          <h1 className="reveal-up delay-100 text-balance bg-gradient-to-l from-zinc-950 via-zinc-900 to-zinc-950 bg-clip-text text-4xl font-extrabold leading-[1.08] tracking-[-0.045em] text-transparent sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl">
            Bari מנתחת מוצרי מזון
            <br />
            ומזהה את מה שחשוב באמת
          </h1>

          <p className="reveal-up delay-200 mx-auto mt-7 max-w-2xl text-pretty text-lg leading-relaxed text-zinc-600 md:text-xl md:leading-relaxed">
            Bari מנתח מוצרים דרך עשרות אותות תזונתיים ורכיביים — ולא לפי נתון בודד.
          </p>

          <div className="reveal-up delay-300 mt-11 flex flex-col items-center justify-center gap-3 sm:flex-row sm:gap-4">
            <Button
              size="lg"
              className="group h-12 w-full rounded-2xl bg-zinc-950 px-8 text-base font-semibold text-white shadow-lg shadow-zinc-950/10 transition-[box-shadow,transform,background-color] duration-500 ease-out hover:-translate-y-px hover:bg-zinc-900 hover:shadow-xl hover:shadow-zinc-950/15 sm:w-auto"
              asChild
            >
              <a href="#methodology" className="inline-flex items-center justify-center gap-2">
                איך Bari מנתח מזון
                <ChevronLeft
                  className="size-5 transition-transform group-hover:-translate-x-0.5"
                  aria-hidden
                />
              </a>
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="h-12 w-full rounded-2xl border-zinc-200/80 bg-white/65 px-8 text-base font-semibold text-zinc-800 shadow-sm shadow-zinc-950/[0.03] backdrop-blur-sm transition-[background-color,box-shadow,transform] duration-500 ease-out hover:-translate-y-px hover:bg-white hover:shadow-md hover:shadow-zinc-950/[0.06] sm:w-auto"
              asChild
            >
              <a href="#comparisons">כך Bari משווה מוצרים</a>
            </Button>
          </div>

          <div className="reveal-up delay-300 mx-auto mt-16 flex max-w-3xl flex-wrap items-center justify-center gap-x-9 gap-y-4 text-sm text-zinc-600">
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
