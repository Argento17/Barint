import Link from "next/link";
import { ChevronLeft } from "lucide-react";

import { BariSignalMark } from "@/components/brand/bari-brand-logo";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

import { heroTrust } from "./content";
import { PlantHeroBackground } from "./plant-hero-background";
import { HomeContainer } from "./section-frame";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

export function HomeHero() {
  return (
    <section
      className={cn(
        "relative flex min-h-[72vh] items-center overflow-hidden border-b border-black/[0.06] md:min-h-[78vh]",
        siteHeaderOffsetClass
      )}
    >
      <div
        className="pointer-events-none absolute inset-x-0 top-0 -z-10 h-full max-h-[44rem] bg-transparent"
        aria-hidden
      />
      <div className="pointer-events-none absolute inset-0 -z-10" aria-hidden>
        <PlantHeroBackground />
      </div>
      <div
        className="pointer-events-none absolute -end-24 top-8 -z-10 size-[28rem] rounded-full bg-[#2FAE82]/[0.035] blur-3xl"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute -start-16 top-24 -z-10 size-[22rem] rounded-full bg-[#F7F7F2]/70 blur-3xl"
        aria-hidden
      />
      <HomeContainer className="py-[4.5rem] md:py-24">
        <div className="mx-auto max-w-5xl text-center">
          <Badge
            variant="outline"
            className="reveal-up mb-7 inline-flex items-center gap-2 rounded-full border-black/[0.08] bg-[#FFFFFF]/68 px-4 py-2 text-sm font-semibold text-[#1F8F6A] shadow-sm shadow-slate-900/20 backdrop-blur-sm"
            asChild
          >
            <Link href="#analysis-engine">
              <BariSignalMark className="size-4" />
              ניתוח מוצרים · המדף הישראלי
            </Link>
          </Badge>

          <h1 className="reveal-up delay-100 text-balance bg-gradient-to-l from-[#111318] via-[#111318] to-[#4E5663] bg-clip-text text-4xl font-extrabold leading-[1.08] tracking-[-0.045em] text-transparent sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl">
            Bari מנתחת מוצרי מזון
            <br />
            ומזהה את מה שחשוב באמת
          </h1>

          <p className="reveal-up delay-200 mx-auto mt-7 max-w-2xl text-pretty text-lg leading-relaxed text-[#4E5663] md:text-xl md:leading-relaxed">
            פלטפורמה שמפרקת מוצרים מהמדף — רכיבים, עיבוד והקשר קטגוריאלי, לא נתון בודד.
          </p>

          <div className="reveal-up delay-300 mt-7 flex flex-col items-center justify-center gap-3 sm:mt-11 sm:flex-row sm:gap-4">
            <Button
              size="lg"
              className="group h-12 w-full rounded-2xl border border-[#1F8F6A]/10 bg-[#1F8F6A] px-8 text-base font-semibold text-[#F7F7F2] shadow-lg shadow-slate-900/10 transition-[box-shadow,transform,background-color] duration-500 ease-out hover:-translate-y-px hover:bg-[#1F8F6A] hover:shadow-xl hover:shadow-slate-900/10 sm:w-auto"
              asChild
            >
              <a href="#analysis-engine" className="inline-flex items-center justify-center gap-2">
                איך Bari מנתחת מוצרים
                <ChevronLeft
                  className="size-5 transition-transform group-hover:-translate-x-0.5"
                  aria-hidden
                />
              </a>
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="h-12 w-full rounded-2xl border-black/[0.08] bg-[#FFFFFF]/68 px-8 text-base font-semibold text-[#111318] shadow-sm shadow-slate-900/10 backdrop-blur-sm transition-[background-color,box-shadow,transform] duration-500 ease-out hover:-translate-y-px hover:bg-[#FFFFFF]/82 hover:shadow-md hover:shadow-slate-900/10 sm:w-auto"
              asChild
            >
              <Link href="/hashvaot">השוואות מהמדף</Link>
            </Button>
          </div>

          <div className="reveal-up delay-300 mx-auto mt-10 flex max-w-3xl flex-wrap items-center justify-center gap-x-9 gap-y-4 text-sm text-[#4E5663] sm:mt-16">
            {heroTrust.map((item) => {
              const Icon = item.icon;
              return (
                <div key={item.label} className="flex items-center gap-2">
                  <Icon className="size-5 shrink-0 text-[#2FAE82]" aria-hidden />
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
