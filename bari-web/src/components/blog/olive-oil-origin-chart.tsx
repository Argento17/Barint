import { oliveOilArticle } from "@/lib/blog/olive-oil-article-content";

const COUNTRY_COLORS: Record<string, string> = {
  ספרד: "#C8B978",
  איטליה: "#7A9450",
  ישראל: "#4A8FA0",
};

export function OliveOilOriginChart() {
  const { originData } = oliveOilArticle;

  return (
    <section className="rounded-[1.2rem] border border-black/[0.07] bg-[#FFFFFF] px-6 py-7 md:px-8 md:py-9">
      <header className="mb-6 text-right">
        <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/85">
          מקור מוצהר
        </p>
        <h2 className="mt-1 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
          {originData.title}
        </h2>
        <p className="mt-2 max-w-2xl text-sm leading-relaxed text-[#4E5663] md:text-base">
          {originData.subtitle}
        </p>
      </header>

      <div className="space-y-4">
        {originData.items.map((item) => {
          const color = COUNTRY_COLORS[item.country] ?? "#7A817C";
          return (
            <div key={item.country} className="space-y-2">
              <div className="flex items-center justify-between text-right">
                <span className="text-xs text-[#7A817C]">
                  {item.count} מוצרים · {item.percent}%
                </span>
                <span className="text-sm font-bold text-[#111318]">{item.country}</span>
              </div>
              <div className="h-2.5 overflow-hidden rounded-full bg-[#F7F7F2]">
                <div
                  className="h-full rounded-full transition-all"
                  style={{ width: `${item.percent}%`, backgroundColor: color }}
                />
              </div>
              <p className="text-right text-[0.65rem] text-[#7A817C]">
                {item.products.join(" · ")}
              </p>
            </div>
          );
        })}
      </div>

      <p className="mt-6 rounded-[0.75rem] border border-amber-200/60 bg-amber-50/60 px-4 py-3 text-right text-xs leading-relaxed text-[#7A6A00]">
        <span className="font-bold">שימו לב · </span>
        {originData.caveat}
      </p>
    </section>
  );
}
