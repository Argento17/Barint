import { ChevronLeft } from "lucide-react";

import { categories } from "./content";
import { HomeContainer, SectionHeading } from "./section-frame";

export function HomeCategories() {
  return (
    <section className="bg-white py-16 md:py-20" id="categories">
      <HomeContainer>
        <SectionHeading
          title="קטגוריות מובילות"
          description="עיינו בהשוואות ודירוגים לפי קטגוריה — נקודת כניסה נוחה לתוכן העומק."
        />

        <div className="grid grid-cols-2 gap-3 md:grid-cols-4 md:gap-4">
          {categories.map((category) => {
            const Icon = category.icon;
            return (
              <a
                key={category.name}
                href="#comparisons"
                className={`group relative overflow-hidden rounded-2xl border border-zinc-200/60 bg-gradient-to-br ${category.bg} p-5 shadow-sm transition duration-300 hover:-translate-y-1 hover:shadow-lg md:p-6`}
              >
                <div
                  className={`mb-3 flex size-12 items-center justify-center rounded-xl bg-gradient-to-br ${category.color} shadow-md transition-transform group-hover:scale-105 md:size-14`}
                >
                  <Icon className="size-6 text-white md:size-7" aria-hidden />
                </div>
                <h3 className="text-base font-semibold text-zinc-900 md:text-lg">{category.name}</h3>
                <div className="mt-2 flex items-center gap-1 text-sm text-zinc-500 transition-colors group-hover:text-zinc-700">
                  <span>עיינו</span>
                  <ChevronLeft className="size-4" aria-hidden />
                </div>
              </a>
            );
          })}
        </div>
      </HomeContainer>
    </section>
  );
}
