import { foodDyesArticle } from "@/lib/blog/food-dyes-article-content";

// Designed color-contrast visual — the section's argument IS the colour gap
// (US synthetic vs EU reformulated), so we show it rather than risk hotlinking
// brand photos. Keyed by the example brand string from the content file.
type Swatch = { fill: string; label: string; caption: string };

const FORMULA_PALETTES: Record<string, { us: Swatch; eu: Swatch }> = {
  Fanta: {
    us: { fill: "linear-gradient(135deg,#FF8A1E,#FF5300)", label: "ארה״ב", caption: "Yellow 6 + Red 40" },
    eu: { fill: "linear-gradient(135deg,#F6C892,#EEB877)", label: "אירופה", caption: "תרכיזי גזר ודלעת" },
  },
  Skittles: {
    us: {
      fill: "linear-gradient(90deg,#E2231A,#F58220,#FFD200,#3AA935,#6A2C91)",
      label: "ארה״ב",
      caption: "צבעים סינתטיים",
    },
    eu: {
      fill: "linear-gradient(90deg,#C98882,#D6B083,#DBD09A,#A6BE98,#A294B4)",
      label: "אירופה",
      caption: "חלופות טבעיות",
    },
  },
};

function FormulaSwatch({ swatch }: { swatch: Swatch }) {
  return (
    <div className="flex-1 text-center">
      <div
        className="h-14 w-full rounded-[0.6rem] border border-black/10 shadow-sm md:h-16"
        style={{ background: swatch.fill }}
        aria-hidden
      />
      <p className="mt-2 text-xs font-bold text-[#111318]">{swatch.label}</p>
      <p className="mt-0.5 text-[0.65rem] leading-tight text-[#7A817C]">{swatch.caption}</p>
    </div>
  );
}

export function FoodDyesDualFormula() {
  const { dualFormula } = foodDyesArticle;

  return (
    <section className="space-y-6">
      <header className="text-right">
        <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/85">
          אותו מותג, שתי נוסחאות
        </p>
        <h2 className="mt-1 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
          {dualFormula.title}
        </h2>
        <p className="mt-2 text-sm leading-relaxed text-[#4E5663] md:text-base">
          {dualFormula.subtitle}
        </p>
      </header>

      <div className="rounded-[1.2rem] border border-black/[0.07] bg-[#FFFFFF] px-6 py-7 md:px-8 md:py-8">
        <div className="flex flex-col gap-6 md:flex-row md:items-start md:gap-10">
          <div className="shrink-0 text-center md:text-right">
            <p className="text-[3.5rem] font-extrabold leading-none tracking-[-0.06em] text-[#C0392B] md:text-[4.5rem]">
              {dualFormula.headline}
            </p>
            <p className="mt-1 max-w-[11rem] text-center text-xs font-bold uppercase tracking-[0.1em] text-[#4E5663] md:text-right">
              {dualFormula.headlineLabel}
            </p>
          </div>

          <div className="flex-1 text-right">
            <p className="text-base leading-relaxed text-[#111318] md:text-lg">
              {dualFormula.description}
            </p>

            <ul className="mt-5 space-y-4">
              {dualFormula.examples.map((ex) => {
                const palette = FORMULA_PALETTES[ex.brand];
                return (
                  <li
                    key={ex.brand}
                    className="rounded-[0.9rem] border border-black/6 bg-[#F7F7F2]/60 px-4 py-4"
                  >
                    <p className="text-xs font-bold uppercase tracking-[0.12em] text-[#167A58]">
                      {ex.brand}
                    </p>

                    {palette && (
                      <div
                        className="mt-3 flex items-stretch gap-3"
                        role="img"
                        aria-label={`${ex.brand}: גרסת ארה״ב צבעונית מול גרסת אירופה חיוורת`}
                      >
                        <FormulaSwatch swatch={palette.us} />
                        <FormulaSwatch swatch={palette.eu} />
                      </div>
                    )}

                    <p className="mt-3 text-sm leading-relaxed text-[#111318]">
                      {ex.text}
                    </p>
                  </li>
                );
              })}
            </ul>
          </div>
        </div>

        <p className="mt-5 rounded-[0.75rem] border border-amber-200/60 bg-amber-50/60 px-4 py-3 text-right text-xs leading-relaxed text-[#7A6A00]">
          <span className="font-bold">להבהרה · </span>
          {dualFormula.caveat}
        </p>
      </div>
    </section>
  );
}
