import { Button } from "@/components/ui/button";

import { HomeContainer } from "./section-frame";

export function HomeFinalCta() {
  return (
    <section className="relative overflow-hidden bg-[#F7F7F2] py-20 md:py-24">
      <div
        className="pointer-events-none absolute inset-0 bg-transparent"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-0 opacity-0"
        style={{
          backgroundImage:
            "radial-gradient(circle at 20% 30%, rgba(47,174,130,0.06) 1px, transparent 1px), radial-gradient(circle at 80% 70%, rgba(255,255,255,0.06) 1px, transparent 1px)",
          backgroundSize: "48px 48px",
        }}
      />

      <HomeContainer className="relative text-center">
        <p className="mb-4 text-xs font-bold uppercase tracking-[0.22em] text-[#1F8F6A]/80">Food intelligence system</p>
        <h2 className="text-balance text-3xl font-extrabold leading-tight tracking-[-0.045em] text-[#111318] md:text-5xl lg:text-6xl">
          התחילו לקבל החלטות
          <br />
          מזון מושכלות
        </h2>
        <p className="mx-auto mt-6 max-w-2xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-xl">
          השוואות, דירוגים והסברים קצרים שמחזירים את ההקשר לבחירת המזון.
        </p>
        <div className="mt-10 flex flex-col items-stretch justify-center gap-4 sm:flex-row sm:items-center sm:justify-center sm:gap-5">
          <Button
            size="lg"
            className="h-12 rounded-2xl border border-[#1F8F6A]/10 bg-[#1F8F6A] px-10 text-base font-bold text-[#F7F7F2] shadow-xl shadow-slate-900/10 hover:bg-[#1F8F6A] sm:min-w-44"
            asChild
          >
            <a href="#comparisons" className="inline-flex items-center justify-center">
              עיינו בהשוואות
            </a>
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="h-12 rounded-2xl border border-black/[0.08] bg-[#FFFFFF]/68 px-10 text-base font-semibold text-[#111318] backdrop-blur-sm hover:bg-[#FFFFFF]/82 sm:min-w-44"
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
