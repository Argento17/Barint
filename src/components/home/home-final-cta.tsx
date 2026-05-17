import { Button } from "@/components/ui/button";

import { HomeContainer } from "./section-frame";

export function HomeFinalCta() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-emerald-600 via-emerald-700 to-green-700 py-20 md:py-24">
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.12]"
        style={{
          backgroundImage:
            "radial-gradient(circle at 20% 30%, white 1px, transparent 1px), radial-gradient(circle at 80% 70%, white 1px, transparent 1px)",
          backgroundSize: "48px 48px",
        }}
      />

      <HomeContainer className="relative text-center">
        <h2 className="text-balance text-3xl font-bold leading-tight text-white md:text-5xl lg:text-6xl">
          התחילו לקבל החלטות
          <br />
          מזון מושכלות
        </h2>
        <p className="mx-auto mt-6 max-w-2xl text-pretty text-base leading-relaxed text-emerald-50 md:text-xl">
          גלו השוואות, דירוגים ומדריכים שעוזרים לכם לבחור טוב יותר — בלי חיפוש מוצרים מזויף.
        </p>
        <div className="mt-10 flex flex-col items-stretch justify-center gap-4 sm:flex-row sm:items-center sm:justify-center sm:gap-5">
          <Button
            size="lg"
            className="h-12 rounded-2xl bg-white px-10 text-base font-bold text-emerald-700 shadow-xl hover:bg-emerald-50 sm:min-w-44"
            asChild
          >
            <a href="#comparisons" className="inline-flex items-center justify-center">
              עיינו בהשוואות
            </a>
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="h-12 rounded-2xl border-2 border-white/35 bg-emerald-800/40 px-10 text-base font-semibold text-white backdrop-blur-sm hover:bg-emerald-800/60 sm:min-w-44"
            asChild
          >
            <a href="#guides" className="inline-flex items-center justify-center">
              קראו את המדריכים
            </a>
          </Button>
        </div>
      </HomeContainer>
    </section>
  );
}
