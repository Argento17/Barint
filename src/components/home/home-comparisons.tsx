import { ArrowUpRight, Award, BookOpen, ChevronLeft, ShieldCheck } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

import { comparisons } from "./content";
import { HomeContainer } from "./section-frame";

const criteriaTone = {
  positive: {
    dot: "bg-emerald-500",
    bar: "bg-emerald-600",
    text: "text-emerald-700",
  },
  neutral: {
    dot: "bg-zinc-400",
    bar: "bg-zinc-500",
    text: "text-zinc-600",
  },
  caution: {
    dot: "bg-amber-500",
    bar: "bg-amber-600",
    text: "text-amber-700",
  },
} as const;

const revealDelays = ["delay-100", "delay-200", "delay-300"] as const;

export function HomeComparisons() {
  return (
    <section className="relative py-16 md:py-20" id="comparisons">
      <HomeContainer>
        <div className="reveal-up mb-10 flex flex-col items-start justify-between gap-6 md:mb-12 md:flex-row md:items-end">
          <div className="max-w-2xl space-y-3 text-right">
            <h2 className="text-balance text-3xl font-bold tracking-tight text-zinc-900 md:text-4xl lg:text-5xl">
              השוואות מובילות
            </h2>
            <p className="text-pretty text-base text-zinc-600 md:text-lg">
              השוואות שמראות למה מוצר מדורג גבוה יותר — ביחס לקטגוריה, עם ביטחון, מקורות
              וסיגנלים ברורים.
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

        <div className="grid gap-5 md:grid-cols-3 md:gap-6">
          {comparisons.map((comparison, index) => (
            <Card
              key={comparison.title}
              className={`reveal-up group cursor-pointer gap-0 overflow-hidden border-zinc-200/65 bg-white/85 py-0 shadow-[0_18px_60px_-42px_rgba(24,24,27,0.32)] backdrop-blur-sm transition-[border-color,box-shadow,transform] duration-700 ease-out hover:-translate-y-0.5 hover:border-zinc-300/80 hover:shadow-[0_26px_76px_-48px_rgba(24,24,27,0.38)] ${revealDelays[index]}`}
            >
              <div className={`relative bg-gradient-to-br ${comparison.gradient} p-5 md:p-6`}>
                <div className="rounded-3xl border border-white/75 bg-white/70 p-4 shadow-sm shadow-zinc-950/[0.03] backdrop-blur-sm">
                  <div className="flex items-start justify-between gap-4">
                    <div className="space-y-1 text-right">
                      <div className="text-xs font-semibold text-emerald-900">
                        {comparison.category}
                      </div>
                      <div className="text-[0.72rem] font-medium text-zinc-500">
                        {comparison.benchmark}
                      </div>
                    </div>
                    <div className="text-left">
                      <div className="text-4xl font-extrabold leading-none tracking-tight text-zinc-950">
                        {comparison.score}
                      </div>
                      <div className="mt-1 text-[0.68rem] font-semibold uppercase tracking-[0.18em] text-zinc-500">
                        Bari score
                      </div>
                    </div>
                  </div>
                  <div className="mt-4 h-1.5 overflow-hidden rounded-full bg-zinc-200/70">
                    <div
                      className="h-full rounded-full bg-zinc-950"
                      style={{ width: `${comparison.score}%` }}
                    />
                  </div>
                </div>
                <div className="absolute end-4 top-4">
                  <span className="inline-flex items-center gap-1.5 rounded-full bg-white/90 px-3 py-1.5 text-xs font-medium text-zinc-700 shadow-sm backdrop-blur-sm">
                    <BookOpen className="size-3.5" aria-hidden />
                    {comparison.readTime}
                  </span>
                </div>
              </div>
              <CardContent className="space-y-5 p-6">
                <div className="flex items-center gap-2 text-xs font-semibold text-emerald-600">
                  <Award className="size-3.5 text-emerald-800" aria-hidden />
                  ניתוח קטגוריאלי
                </div>
                <h3 className="text-lg font-semibold text-zinc-900 transition-colors group-hover:text-emerald-700 md:text-xl">
                  {comparison.title}
                </h3>
                <p className="text-sm text-zinc-600">{comparison.products}</p>
                <div className="rounded-2xl border border-zinc-200/70 bg-zinc-50/70 p-3">
                  <div className="flex items-center justify-between gap-3 text-xs">
                    <span className="font-semibold text-zinc-800">רמת ביטחון</span>
                    <span className="font-bold text-zinc-950">{comparison.confidence}%</span>
                  </div>
                  <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-zinc-200">
                    <div
                      className="h-full rounded-full bg-emerald-600"
                      style={{ width: `${comparison.confidence}%` }}
                    />
                  </div>
                  <div className="mt-2 flex items-center justify-between gap-3 text-[0.72rem] font-medium text-zinc-500">
                    <span>{comparison.sources} מקורות</span>
                    <span>{comparison.updated}</span>
                  </div>
                </div>
                <div className="space-y-2.5">
                  {comparison.criteria.map((criterion) => {
                    const tone = criteriaTone[criterion.impact];

                    return (
                      <div
                        key={criterion.label}
                        className="rounded-2xl border border-zinc-200/65 bg-white/85 px-3 py-3"
                      >
                        <div className="flex items-center justify-between gap-3">
                          <div className="flex items-center gap-2">
                            <span className={`size-1.5 rounded-full ${tone.dot}`} aria-hidden />
                            <span className="text-sm font-semibold text-zinc-900">
                              {criterion.label}
                            </span>
                          </div>
                          <span className={`text-xs font-bold ${tone.text}`}>
                            {criterion.value}
                          </span>
                        </div>
                        <div className="mt-2 h-1 overflow-hidden rounded-full bg-zinc-100">
                          <div className={`h-full w-2/3 rounded-full ${tone.bar}`} />
                        </div>
                        <p className="mt-2 text-xs leading-relaxed text-zinc-500">
                          {criterion.context}
                        </p>
                      </div>
                    );
                  })}
                </div>
                <div className="flex flex-wrap gap-2">
                  {comparison.signals.map((signal) => (
                    <span
                      key={signal}
                      className="inline-flex items-center gap-1.5 rounded-full border border-zinc-200/75 bg-white/80 px-2.5 py-1 text-xs font-medium text-zinc-600 transition-colors duration-500 group-hover:border-zinc-300"
                    >
                      <span className="size-1.5 rounded-full bg-emerald-800" aria-hidden />
                      {signal}
                    </span>
                  ))}
                </div>
                <div className="rounded-2xl bg-zinc-950/95 px-4 py-3 text-white shadow-sm shadow-zinc-950/10">
                  <div className="text-xs font-semibold text-emerald-200">
                    למה הדירוג גבוה יותר?
                  </div>
                  <p className="mt-1.5 text-xs leading-relaxed text-zinc-300">
                    {comparison.rankingReason}
                  </p>
                </div>
                <div className="flex items-center justify-between pt-1">
                  <span className="inline-flex items-center gap-1.5 text-xs font-medium text-zinc-500">
                    <ShieldCheck className="size-3.5 text-emerald-600" aria-hidden />
                    שקיפות מקורות
                  </span>
                  <span className="inline-flex items-center gap-2 text-sm font-semibold text-emerald-600 transition-all group-hover:gap-3">
                    קראו
                    <ArrowUpRight className="size-4" aria-hidden />
                  </span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </HomeContainer>
    </section>
  );
}
