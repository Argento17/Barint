import { ArrowUpRight, Award, BookOpen, ChevronLeft } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

import { comparisons } from "./content";
import { HomeContainer } from "./section-frame";

export function HomeComparisons() {
  return (
    <section className="relative py-16 md:py-20" id="comparisons">
      <HomeContainer>
        <div className="mb-10 flex flex-col items-start justify-between gap-6 md:mb-12 md:flex-row md:items-end">
          <div className="max-w-2xl space-y-3 text-right">
            <h2 className="text-balance text-3xl font-bold tracking-tight text-zinc-900 md:text-4xl lg:text-5xl">
              השוואות מובילות
            </h2>
            <p className="text-pretty text-base text-zinc-600 md:text-lg">
              ניתוחים מקיפים שעוזרים לכם לבחור טוב יותר — עם מקורות, זמן קריאה ותאריך עדכון.
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
          {comparisons.map((comparison) => (
            <Card
              key={comparison.title}
              className="group cursor-pointer gap-0 overflow-hidden border-zinc-200/70 bg-white py-0 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl"
            >
              <div
                className={`relative flex h-44 items-center justify-center bg-gradient-to-br ${comparison.gradient} p-8 md:h-48`}
              >
                <div className="text-center text-4xl font-bold text-black/10">VS</div>
                <div className="absolute end-4 top-4">
                  <span className="inline-flex items-center gap-1.5 rounded-full bg-white/90 px-3 py-1.5 text-xs font-medium text-zinc-700 shadow-sm backdrop-blur-sm">
                    <BookOpen className="size-3.5" aria-hidden />
                    {comparison.readTime}
                  </span>
                </div>
              </div>
              <CardContent className="space-y-3 p-6">
                <div className="flex items-center gap-2 text-xs font-semibold text-emerald-600">
                  <Award className="size-3.5" aria-hidden />
                  {comparison.category}
                </div>
                <h3 className="text-lg font-semibold text-zinc-900 transition-colors group-hover:text-emerald-700 md:text-xl">
                  {comparison.title}
                </h3>
                <p className="text-sm text-zinc-600">{comparison.products}</p>
                <div className="flex items-center justify-between pt-1">
                  <span className="text-xs font-medium text-zinc-500">{comparison.updated}</span>
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
