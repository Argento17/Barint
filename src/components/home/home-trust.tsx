import { trustPillars } from "./content";
import { HomeContainer, SectionHeading } from "./section-frame";

export function HomeTrust() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-zinc-900 via-zinc-800 to-zinc-900 py-20 md:py-24">
      <div
        className="pointer-events-none absolute inset-0 opacity-25"
        style={{
          backgroundImage:
            "radial-gradient(circle at 30% 40%, rgba(16,185,129,0.35) 0%, transparent 45%), radial-gradient(circle at 75% 60%, rgba(5,150,105,0.25) 0%, transparent 42%)",
        }}
      />

      <HomeContainer className="relative">
        <SectionHeading
          tone="inverted"
          title="בנויים על אמון ושקיפות"
          description="אנחנו לא מקבלים תשלומים מיצרנים. המתודולוגיה שלנו פתוחה. המטרה: לעזור לכם לבחור טוב יותר — עם הקשר ולא עם סלוגן."
        />

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 lg:gap-6">
          {trustPillars.map((item) => {
            const Icon = item.icon;
            return (
              <div
                key={item.label}
                className="rounded-2xl border border-white/15 bg-white/10 p-6 text-center shadow-sm backdrop-blur-md transition duration-300 hover:-translate-y-0.5 hover:bg-white/15"
              >
                <div className="mx-auto mb-4 flex size-14 items-center justify-center rounded-xl bg-white/15">
                  <Icon className="size-7 text-white" aria-hidden />
                </div>
                <h3 className="text-lg font-semibold text-white">{item.label}</h3>
                <p className="mt-1 text-sm text-zinc-300">{item.desc}</p>
              </div>
            );
          })}
        </div>
      </HomeContainer>
    </section>
  );
}
