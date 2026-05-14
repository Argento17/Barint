import { methodology } from "./content";
import { HomeContainer, SectionHeading } from "./section-frame";

export function HomeMethodology() {
  return (
    <section className="bg-white py-20 md:py-24" id="methodology">
      <HomeContainer>
        <SectionHeading
          title="איך אנחנו עובדים"
          description="מתודולוגיה שקופה, מבוססת מקורות, ומכבדת את המשתמש — בלי הבטחות רפואיות."
        />

        <div className="grid gap-6 md:grid-cols-3 md:gap-8">
          {methodology.map((step) => {
            const Icon = step.icon;
            return (
              <div
                key={step.title}
                className="rounded-3xl border border-zinc-200/60 bg-gradient-to-br from-zinc-50 to-white p-8 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl"
              >
                <div className="mb-6 flex size-16 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-500 to-emerald-600 shadow-md">
                  <Icon className="size-8 text-white" aria-hidden />
                </div>
                <h3 className="mb-3 text-2xl font-semibold text-zinc-900">{step.title}</h3>
                <p className="leading-relaxed text-zinc-600">{step.description}</p>
              </div>
            );
          })}
        </div>
      </HomeContainer>
    </section>
  );
}
