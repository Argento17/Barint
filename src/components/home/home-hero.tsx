import Link from "next/link";
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
        "relative flex min-h-[56vh] items-center overflow-hidden border-b border-black/[0.06] md:min-h-[62vh]",
        siteHeaderOffsetClass
      )}
    >
      <HomeContainer className="py-[4.5rem] md:py-24">
        <div className="mx-auto max-w-5xl text-center">
          <Badge
            variant="outline"
            className="reveal-up mb-7 inline-flex items-center gap-2 rounded-full border-black/[0.08] bg-[#FFFFFF]/68 px-4 py-2 text-sm font-semibold text-[#1F8F6A] shadow-sm shadow-slate-900/20 backdrop-blur-sm"
            asChild
          >
            <Link href="/blog/milk-analysis">
              <BariSignalMark className="size-4" />
              ניתוח מוביל: מדף החלב בישראל
            </Link>
          </Badge>

          <h1 className="reveal-up delay-100 text-balance text-4xl font-extrabold leading-[1.08] tracking-[-0.045em] text-[#111318] sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl">
            Bari מנתחת מוצרי מזון
            <br />
            ומזהה את מה שחשוב באמת
          </h1>

          <p className="reveal-up delay-200 mx-auto mt-7 max-w-2xl text-pretty text-lg leading-relaxed text-[#4E5663] md:text-xl md:leading-relaxed">
            Bari מנתח מוצרים דרך עשרות אותות תזונתיים ורכיביים — ולא לפי נתון בודד.
          </p>

          <div className="reveal-up delay-300 mt-11 flex flex-col items-center justify-center gap-3 sm:flex-row sm:gap-4">
            <Button
              size="lg"
              className="group h-12 w-full rounded-2xl border border-[#1F8F6A]/10 bg-[#1F8F6A] px-8 text-base font-semibold text-[#F7F7F2] shadow-lg shadow-slate-900/10 transition-[box-shadow,transform,background-color] duration-500 ease-out hover:-translate-y-px hover:bg-[#1F8F6A] hover:shadow-xl hover:shadow-slate-900/10 sm:w-auto"
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
              className="h-12 w-full rounded-2xl border-black/[0.08] bg-[#FFFFFF]/68 px-8 text-base font-semibold text-[#111318] shadow-sm shadow-slate-900/10 backdrop-blur-sm transition-[background-color,box-shadow,transform] duration-500 ease-out hover:-translate-y-px hover:bg-[#FFFFFF]/82 hover:shadow-md hover:shadow-slate-900/10 sm:w-auto"
              asChild
            >
              <Link href="/blog/milk-analysis">ניתוח מדף החלב</Link>
            </Button>
          </div>

          <div className="reveal-up delay-300 mx-auto mt-16 flex max-w-3xl flex-wrap items-center justify-center gap-x-9 gap-y-4 text-sm text-[#4E5663]">
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
