import { chart1 } from "@/lib/blog/sugar-alcohols-article-content";

export function SugarAlcoholsChart1() {
  return (
    <section
      id="chart1"
      className="rounded-[1.2rem] border border-black/[0.07] bg-[#FFFFFF] px-6 py-7 md:px-8 md:py-9"
    >
      <header className="mb-6 text-right">
        <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/85">
          רכיבים · כוהלי סוכר
        </p>
        <h2 className="mt-1 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
          {chart1.title}
        </h2>
        <p className="mt-2 max-w-2xl text-sm leading-relaxed text-[#4E5663] md:text-base">
          {chart1.subtitle}
        </p>
      </header>

      {/* Column headers */}
      <div className="mb-3 hidden grid-cols-[2fr_1fr_1.5fr_2fr] gap-3 border-b border-black/[0.06] pb-2 text-right sm:grid">
        <p className="text-[0.6rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
          {chart1.cols.name}
        </p>
        <p className="text-[0.6rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
          {chart1.cols.kcal}
        </p>
        <p className="text-[0.6rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
          {chart1.cols.gi}
        </p>
        <p className="text-[0.6rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
          {chart1.cols.tolerance}
        </p>
      </div>

      <div className="space-y-3">
        {chart1.rows.map((row) => (
          <div
            key={row.id}
            className={
              row.highlight
                ? "rounded-[0.9rem] border border-[#1F8F6A]/30 bg-[#F0FAF6] px-4 py-4"
                : "rounded-[0.9rem] border border-black/[0.05] bg-[#F7F7F2] px-4 py-4"
            }
          >
            {/* Mobile: stacked layout */}
            <div className="text-right sm:hidden">
              <div className="flex items-center justify-between">
                <span className="text-[0.6rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                  {chart1.cols.kcal}: {row.kcal}
                </span>
                <p
                  className={
                    row.highlight
                      ? "text-sm font-extrabold text-[#111318]"
                      : "text-sm font-bold text-[#111318]"
                  }
                >
                  {row.name}
                  {row.highlight && (
                    <span className="mr-2 inline-block rounded-full bg-[#1F8F6A] px-2 py-0.5 text-[0.55rem] font-bold uppercase tracking-[0.1em] text-white">
                      הנפוץ ביותר
                    </span>
                  )}
                </p>
              </div>
              <p className="mt-2 text-xs text-[#4E5663]">
                <span className="font-bold text-[#7A817C]">{chart1.cols.gi}: </span>
                {row.gi}
              </p>
              <p className="mt-1.5 text-xs leading-relaxed text-[#4E5663]">
                <span className="font-bold text-[#7A817C]">{chart1.cols.tolerance}: </span>
                {row.tolerance}
              </p>
            </div>

            {/* Desktop: grid layout */}
            <div className="hidden grid-cols-[2fr_1fr_1.5fr_2fr] gap-3 text-right sm:grid">
              <div>
                <p
                  className={
                    row.highlight
                      ? "text-sm font-extrabold text-[#111318]"
                      : "text-sm font-bold text-[#111318]"
                  }
                >
                  {row.name}
                </p>
                {row.highlight && (
                  <span className="mt-1 inline-block rounded-full bg-[#1F8F6A] px-2 py-0.5 text-[0.55rem] font-bold uppercase tracking-[0.1em] text-white">
                    הנפוץ ביותר
                  </span>
                )}
              </div>
              <p className="text-sm font-semibold text-[#111318]">{row.kcal}</p>
              <p className="text-xs leading-relaxed text-[#4E5663]">{row.gi}</p>
              <p className="text-xs leading-relaxed text-[#4E5663]">{row.tolerance}</p>
            </div>
          </div>
        ))}
      </div>

      <p className="mt-5 rounded-[0.75rem] border border-amber-200/60 bg-amber-50/60 px-4 py-3 text-right text-xs leading-relaxed text-[#7A6A00]">
        <span className="font-bold">שימו לב · </span>
        {chart1.caveat}
      </p>
    </section>
  );
}
