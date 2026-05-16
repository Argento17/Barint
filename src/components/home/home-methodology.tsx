import { methodology } from "./content";
import { HomeContainer, SectionHeading } from "./section-frame";
import { cn } from "@/lib/utils";

const revealDelays = ["delay-100", "delay-200", "delay-300"] as const;

export function HomeMethodology() {
  return (
    <section className="relative overflow-hidden bg-white py-20 md:py-24" id="methodology">
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-40 bg-gradient-to-b from-[#f7f8f6] to-white"
        aria-hidden
      />
      <HomeContainer>
        <div className="reveal-up">
          <SectionHeading
            eyebrow="מסגרת דירוג Bari · Signal Review"
            title="איך ברי מנתחת מזון"
            description="מודל הערכה רב־פרמטרי שמתרגם תוויות מוצר לאותות תזונתיים, משווה אותם ביחס לקטגוריה, ומציג דירוג עם מקור, ביטחון ונימוק."
          />
        </div>

        <div className="grid items-stretch gap-6 md:grid-cols-3 md:gap-8">
          {methodology.map((step, index) => {
            const Icon = step.icon;
            return (
              <div
                key={step.title}
                className={cn(
                  "reveal-up group flex h-full min-h-[34rem] flex-col rounded-[2rem] border border-zinc-200/65 bg-white/80 p-7 shadow-[0_18px_60px_-42px_rgba(24,24,27,0.28)] backdrop-blur-sm transition-[border-color,box-shadow,transform,background-color] duration-700 ease-out hover:-translate-y-0.5 hover:border-zinc-300/75 hover:bg-white hover:shadow-[0_24px_70px_-44px_rgba(24,24,27,0.34)]",
                  revealDelays[index]
                )}
              >
                <div className="mb-7 flex h-11 items-center justify-between gap-4">
                  <div className="text-xs font-semibold tracking-[0.24em] text-emerald-700">
                    {step.step}
                  </div>
                  <div className="flex size-11 items-center justify-center rounded-2xl border border-zinc-200 bg-white/80 text-zinc-800 shadow-sm shadow-zinc-950/[0.03] transition-colors duration-500 group-hover:border-emerald-200 group-hover:text-emerald-700">
                    <Icon className="size-5" aria-hidden />
                  </div>
                </div>
                <h3 className="mb-3 text-2xl font-semibold tracking-[-0.02em] text-zinc-950">
                  {step.title}
                </h3>
                <p className="min-h-[5.25rem] text-pretty leading-relaxed text-zinc-600">
                  {step.description}
                </p>

                <div className="mt-7 rounded-2xl border border-zinc-200/65 bg-white/70 p-4 shadow-sm shadow-zinc-950/[0.02]">
                  <div className="mb-4 flex h-5 items-center justify-between gap-3">
                    <span className="text-xs font-semibold text-zinc-500">מדדי בדיקה</span>
                    <span className="text-xs font-bold text-zinc-900">{step.metric}</span>
                  </div>
                  <div className="space-y-2.5">
                    <div className="h-1.5 overflow-hidden rounded-full bg-zinc-100">
                      <div className="h-full w-4/5 rounded-full bg-zinc-950 transition-all duration-500 group-hover:w-11/12" />
                    </div>
                    <div className="h-1.5 overflow-hidden rounded-full bg-zinc-100">
                      <div className="h-full w-2/3 rounded-full bg-emerald-600 transition-all duration-500 group-hover:w-3/4" />
                    </div>
                    <div className="h-1.5 overflow-hidden rounded-full bg-zinc-100">
                      <div className="h-full w-1/2 rounded-full bg-zinc-300 transition-all duration-500 group-hover:w-3/5" />
                    </div>
                  </div>
                </div>

                <div className="mt-auto flex min-h-8 flex-wrap content-end gap-2 pt-5">
                  {step.signals.map((signal) => (
                    <span
                      key={signal}
                      className="rounded-full border border-zinc-200 bg-white px-2.5 py-1 text-xs font-medium text-zinc-600 transition-colors group-hover:border-emerald-100 group-hover:text-zinc-900"
                    >
                      {signal}
                    </span>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </HomeContainer>
    </section>
  );
}
