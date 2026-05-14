import { ChevronLeft, Info } from "lucide-react";

import { Button } from "@/components/ui/button";

import { ingredients } from "./content";
import { HomeContainer, SectionHeading } from "./section-frame";

export function HomeIngredients() {
  return (
    <section
      className="bg-gradient-to-b from-white via-white to-zinc-50 py-16 md:py-20"
      id="ingredients"
    >
      <HomeContainer>
        <SectionHeading
          title="זרקור רכיבים"
          description="הכירו רכיבים שמופיעים בתוויות — בהקשר רגולטורי ועדכני."
        />

        <div className="grid gap-5 md:grid-cols-2 md:gap-6">
          {ingredients.map((ingredient) => (
            <article
              key={ingredient.name}
              className={`group relative cursor-pointer overflow-hidden rounded-3xl border border-zinc-200/50 bg-gradient-to-br ${ingredient.bgColor} p-8 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl`}
            >
              <div className="absolute start-4 top-4 rounded-full bg-white/80 px-3 py-1.5 text-xs font-medium text-zinc-500 backdrop-blur-sm">
                {ingredient.badge}
              </div>
              <div className="mb-4 mt-8 flex items-start justify-between gap-3">
                <div
                  className={`inline-flex items-center gap-2 rounded-full bg-gradient-to-l ${ingredient.color} px-4 py-2 text-sm font-semibold text-white shadow-sm`}
                >
                  <Info className="size-4 shrink-0" aria-hidden />
                  {ingredient.status}
                </div>
                <ChevronLeft
                  className="size-5 shrink-0 text-zinc-400 transition group-hover:-translate-x-0.5 group-hover:text-zinc-600"
                  aria-hidden
                />
              </div>
              <h3 className="mb-3 text-2xl font-semibold text-zinc-900">{ingredient.name}</h3>
              <p className="leading-relaxed text-zinc-700">{ingredient.description}</p>
            </article>
          ))}
        </div>

        <div className="mt-10 text-center">
          <Button variant="link" className="gap-2 text-base font-semibold text-emerald-700" asChild>
            <a href="#guides">
              <span>ראו את כל מדריך הרכיבים</span>
              <ChevronLeft className="size-5" aria-hidden />
            </a>
          </Button>
        </div>
      </HomeContainer>
    </section>
  );
}
