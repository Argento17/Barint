import type { ReactNode } from "react";

/**
 * UpfInfographicFrame — shared card shell for the 4 TASK-502 UPF infographics
 * (conditions grid, confidence ladder, schematic split, emulsifier spectrum).
 *
 * Colors here are deliberately NOT the site's existing blog eyebrow/meta pair
 * (#7A9450 / #7A817C) -- those are known to fail WCAG-AA (TASK-494, ~3.2-4.0:1
 * on white). This frame uses #167A58 (eyebrow) / #5E6672 (caption), both
 * verified >=4.9:1 against both the white and #F7F7F2 section backgrounds
 * this article alternates between, so the debt is not inherited into new
 * components.
 */
export function UpfInfographicFrame({
  eyebrow,
  title,
  caption,
  children,
}: {
  eyebrow: string;
  title: string;
  caption?: string;
  children: ReactNode;
}) {
  return (
    <figure className="rounded-[1.2rem] border border-black/[0.07] bg-[#FFFFFF] p-5 md:p-6" dir="rtl">
      <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.14em] text-[#167A58]">
        {eyebrow}
      </p>
      <p className="mt-1.5 text-base font-extrabold leading-snug tracking-[-0.01em] text-[#111318] md:text-lg">
        {title}
      </p>
      <div className="mt-4">{children}</div>
      {caption ? (
        <figcaption className="mt-4 border-t border-black/[0.06] pt-3 text-[12px] leading-[1.55] text-[#5E6672]">
          {caption}
        </figcaption>
      ) : null}
    </figure>
  );
}
