import { Button } from "@/components/ui/button";

import { HomeContainer } from "./section-frame";

export function HomeFinalCta() {
  return (
    <section className="relative overflow-hidden py-20 md:py-24">
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_18%,rgba(16,185,129,0.14),transparent_34%),linear-gradient(180deg,rgba(255,255,255,0.035),transparent_58%)]"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.08]"
        style={{
          backgroundImage:
            "radial-gradient(circle at 20% 30%, rgba(52,211,153,0.9) 1px, transparent 1px), radial-gradient(circle at 80% 70%, rgba(255,255,255,0.7) 1px, transparent 1px)",
          backgroundSize: "48px 48px",
        }}
      />

      <HomeContainer className="relative text-center">
        <p className="mb-4 text-xs font-bold uppercase tracking-[0.22em] text-emerald-200/80">Food intelligence system</p>
        <h2 className="text-balance text-3xl font-extrabold leading-tight tracking-[-0.045em] text-white md:text-5xl lg:text-6xl">
          התחילו לקבל החלטות
          <br />
          מזון מושכלות
        </h2>
        <p className="mx-auto mt-6 max-w-2xl text-pretty text-base leading-relaxed text-zinc-400 md:text-xl">
          השוואות, דירוגים והסברים קצרים שמחזירים את ההקשר לבחירת המזון.
        </p>
        <div className="mt-10 flex flex-col items-stretch justify-center gap-4 sm:flex-row sm:items-center sm:justify-center sm:gap-5">
          <Button
            size="lg"
            className="h-12 rounded-2xl border border-emerald-300/10 bg-white px-10 text-base font-bold text-zinc-950 shadow-xl shadow-emerald-950/20 hover:bg-emerald-50 sm:min-w-44"
            asChild
          >
            <a href="#comparisons" className="inline-flex items-center justify-center">
              עיינו בהשוואות
            </a>
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="h-12 rounded-2xl border border-emerald-300/12 bg-white/[0.045] px-10 text-base font-semibold text-white backdrop-blur-sm hover:bg-white/[0.075] sm:min-w-44"
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
