import { UpfInfographicFrame } from "@/components/blog/upf-infographic-frame";
import { upfArticle } from "@/lib/blog/upf-article-content";

/**
 * Infographic #4 -- the emulsifier differentiation that IS live and
 * unconditional in the engine today (EV-003/EV-019, score_engine.py:3664 --
 * per the TASK-502 verification memo §4.1). Penalized vs. relief lists are
 * exactly the additives named in the article body copy; nothing added here.
 */
export function UpfEmulsifierSpectrum() {
  const data = (
    upfArticle.infographics as unknown as {
      spectrum: {
        eyebrow: string;
        title: string;
        penalizedLabel: string;
        reliefLabel: string;
        penalized: { id: string; label: string; code: string }[];
        relief: { id: string; label: string; code: string }[];
        caption: string;
      };
    }
  ).spectrum;

  return (
    <UpfInfographicFrame eyebrow={data.eyebrow} title={data.title} caption={data.caption}>
      <div className="mb-2 flex items-center justify-between text-[13px] font-bold">
        <span className="text-[#9A4012]">{data.penalizedLabel}</span>
        <span className="text-[#155C3C]">{data.reliefLabel}</span>
      </div>
      <div
        className="mb-4 h-2 w-full rounded-full opacity-90"
        style={{
          background: "linear-gradient(90deg, #9A4012 0%, #8A8F98 50%, #155C3C 100%)",
        }}
        aria-hidden
      />
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <div className="rounded-[0.7rem] bg-[#FCEAD9] p-3.5">
          <p className="mb-2 text-[13px] font-bold text-[#9A4012]">{data.penalizedLabel}</p>
          <div className="flex flex-wrap gap-1.5">
            {data.penalized.map((item) => (
              <span
                key={item.id}
                className="rounded-md border border-black/[0.07] bg-[#FFFFFF] px-2.5 py-1 text-xs font-semibold text-[#111318]"
              >
                {item.label}
                {item.code ? (
                  <code className="mr-1 font-mono text-[0.85em] text-[#5E6672]" dir="ltr">
                    {item.code}
                  </code>
                ) : null}
              </span>
            ))}
          </div>
        </div>
        <div className="rounded-[0.7rem] bg-[#E7F4EC] p-3.5">
          <p className="mb-2 text-[13px] font-bold text-[#155C3C]">{data.reliefLabel}</p>
          <div className="flex flex-wrap gap-1.5">
            {data.relief.map((item) => (
              <span
                key={item.id}
                className="rounded-md border border-black/[0.07] bg-[#FFFFFF] px-2.5 py-1 text-xs font-semibold text-[#111318]"
              >
                {item.label}
                {item.code ? (
                  <code className="mr-1 font-mono text-[0.85em] text-[#5E6672]" dir="ltr">
                    {item.code}
                  </code>
                ) : null}
              </span>
            ))}
          </div>
        </div>
      </div>
    </UpfInfographicFrame>
  );
}
