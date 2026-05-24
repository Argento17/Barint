"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useId, useMemo, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { ChevronLeft } from "lucide-react";

import { milkComparisonPage, milkProducts, PRIMARY_DIMENSION_KEYS } from "@/lib/comparisons/milk-page-data";
import { cn } from "@/lib/utils";
const INSIGHT_LINES = [
  "משקאות שיבולת שועל נוטים להכיל יותר מייצבים",
  "חלק ממוצרי הסויה מובילים בכמות החלבון",
  "מוצרים עתירי חלבון מגיעים לעיתים עם יותר עיבוד",
  "שקדים דל קלוריות אך גם דל יחסית בחלבון",
  "חלב פרה בסיסי לרוב עם פחות רכיבים תפקודיים מאשר תחליפים",
  "חלק מהמועשרים מציגים סידן או ויטמין D בתווית — ההשוואה מציגה את הפרטים",
] as const;

function MilkIntelligenceBackdrop() {
  const uid = useId().replace(/:/g, "");

  return (
    <svg
      className="pointer-events-none absolute inset-0 h-full w-full text-[#1F8F6A]"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden
    >
      <defs>
        <linearGradient id={`milk-wave-a-${uid}`} x1="0%" y1="50%" x2="100%" y2="50%">
          <stop offset="0%" stopColor="currentColor" stopOpacity="0" />
          <stop offset="38%" stopColor="currentColor" stopOpacity="0.09" />
          <stop offset="100%" stopColor="currentColor" stopOpacity="0" />
        </linearGradient>
        <linearGradient id={`milk-wave-b-${uid}`} x1="50%" x2="50%" y1="0%" y2="100%">
          <stop offset="0%" stopColor="#FAFAF6" />
          <stop offset="50%" stopColor="#F7F7F2" stopOpacity={0} />
          <stop offset="100%" stopColor="#E4EEE7" stopOpacity={0.32} />
        </linearGradient>
        <radialGradient id={`spot-${uid}`} cx="28%" cy="20%" r="58%">
          <stop offset="0%" stopColor="#FFFFFF" stopOpacity={0.95} />
          <stop offset="42%" stopColor="#F7F7F2" stopOpacity={0.3} />
          <stop offset="100%" stopColor="#F7F7F2" stopOpacity={0} />
        </radialGradient>
        <pattern id={`milk-grid-${uid}`} width={32} height={32} patternUnits="userSpaceOnUse">
          <path d="M 32 0 L 0 0 0 32" fill="none" stroke="currentColor" strokeOpacity="0.065" strokeWidth="0.45" />
        </pattern>
        <pattern id={`milk-grid-fine-${uid}`} width={8} height={8} patternUnits="userSpaceOnUse">
          <path d="M 8 0 L 0 0 0 8" fill="none" stroke="#9AA699" strokeOpacity="0.035" strokeWidth="0.35" />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill={`url(#milk-grid-${uid})`} />
      <rect width="100%" height="100%" fill={`url(#milk-grid-fine-${uid})`} opacity={0.7} />
      <rect width="100%" height="100%" fill={`url(#spot-${uid})`} />

      <g opacity={0.5} stroke="#8A968F" strokeOpacity={0.14} strokeWidth="0.6">
        <line x1="4%" y1="22%" x2="96%" y2="22%" strokeDasharray="4 14" />
        <line x1="8%" y1="52%" x2="94%" y2="50%" strokeDasharray="3 12" />
        <line x1="12%" y1="78%" x2="88%" y2="76%" strokeDasharray="5 16" />
      </g>

      <path
        d="M -8 42 C 85 88 160 14 276 52 S 442 118 514 74 S 688 -12 792 62"
        fill="none"
        stroke="currentColor"
        strokeOpacity={0.14}
        strokeWidth={1.45}
      />
      <path
        d="M -4 118 C 120 154 212 92 348 134 S 512 218 596 174 S 760 126 836 148"
        fill="none"
        stroke="#B5CFC3"
        strokeOpacity={0.48}
        strokeWidth={15}
      />
      <path
        d="M 12 218 C 98 276 218 206 362 258 S 562 348 744 294"
        fill="none"
        stroke="#DCE8E0"
        strokeOpacity={0.62}
        strokeWidth={40}
      />
      <path
        d="M 48 296 C 180 348 294 274 446 332 S 618 394 764 356"
        fill="none"
        stroke="#F8FAF8"
        strokeOpacity={0.95}
        strokeWidth={56}
      />
      <path
        d="M 120 88 C 240 120 320 36 440 72 S 600 108 720 56"
        fill="none"
        stroke="currentColor"
        strokeOpacity={0.1}
        strokeWidth={1.8}
      />

      <ellipse cx="86%" cy="78%" rx="38%" ry="22%" fill={`url(#milk-wave-b-${uid})`} opacity={0.28} />

      <path
        d="M -20 268 Q 420 348 940 236"
        fill="none"
        stroke={`url(#milk-wave-a-${uid})`}
        strokeWidth={102}
        opacity={0.55}
      />

      <g stroke="currentColor" strokeOpacity={0.16} strokeWidth={0.9} fill="none">
        <circle cx="18%" cy="24%" r="4" opacity={0.55} />
        <circle cx="78%" cy="36%" r="3.8" opacity={0.5} />
        <circle cx="52%" cy="14%" r="3.2" opacity={0.5} />
        <circle cx="34%" cy="42%" r="2.4" opacity={0.35} />
        <path d="M 18 24 Q 50 86 78 36" opacity={0.42} strokeDasharray="3 10" />
        <path d="M 52 14 L 78 36 M 52 14 L 18 24" opacity={0.32} strokeDasharray="2 9" />
        <path d="M 34 42 L 52 14" opacity={0.22} strokeDasharray="2 8" />
      </g>
    </svg>
  );
}

function AnalysisParticles({ reduceMotion }: { reduceMotion: boolean | null }) {
  const seeds = [12, 28, 44, 58, 72, 88, 22, 66, 38, 91];
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden>
      {seeds.map((left, i) => (
        <motion.span
          key={i}
          className="absolute top-[18%] size-[2.5px] rounded-full bg-[#1F8F6A]"
          style={{ left: `${left}%`, top: `${22 + (i % 4) * 14}%` }}
          animate={
            reduceMotion
              ? { opacity: 0.12 }
              : { opacity: [0.08, 0.22, 0.1, 0.18, 0.08] }
          }
          transition={
            reduceMotion
              ? undefined
              : { duration: 8 + i * 0.55, repeat: Infinity, ease: "easeInOut" }
          }
        />
      ))}
    </div>
  );
}

function formatUpdatedLine(generatedAt: string): string {
  const parsed = /^(\d{4})-(\d{2})-(\d{2})/.exec(generatedAt);
  if (!parsed) return "עודכן לאחרונה";
  const [, y, mo, d] = parsed;
  const gen = new Date(Number(y), Number(mo) - 1, Number(d));
  const now = new Date();
  const diffDays = Math.floor((now.getTime() - gen.getTime()) / (1000 * 60 * 60 * 24));
  if (diffDays >= 0 && diffDays <= 7) return "עודכן השבוע";
  const dateHe = `${d}.${mo}.${y}`;
  return `עודכן ב-${dateHe}`;
}

type Props = {
  href: string;
  description: string;
};

/** ~12% larger than previous flagship sizes */
const PACK_CONFIG = [
  { w: 140, h: 148, rot: -9, y: 2, z: 50 },
  { w: 118, h: 126, rot: 6, y: 22, z: 40 },
  { w: 104, h: 112, rot: -4, y: 38, z: 30 },
  { w: 92, h: 102, rot: 11, y: 16, z: 20 },
  { w: 84, h: 92, rot: -7, y: 44, z: 10 },
] as const;

export function FeaturedMilkIntelligenceCard({ href, description }: Props) {
  const reduceMotion = useReducedMotion();
  const [insightIndex, setInsightIndex] = useState(0);

  const heroProducts = useMemo(() => {
    const sorted = [...milkProducts].filter((p) => p.image_url).sort((a, b) => b.score - a.score);
    return sorted.slice(0, 5);
  }, []);

  const metadata = useMemo(() => {
    const productCount = milkProducts.length;
    const categoryKeys = new Set(milkProducts.map((p) => p.productType));
    const pillarCount =
      milkProducts.find((p) => p.bariInterpretation?.length)?.bariInterpretation?.length ?? 6;
    const paramSlots = PRIMARY_DIMENSION_KEYS.length * pillarCount;
    return {
      productCount,
      categoryCount: categoryKeys.size,
      paramCount: paramSlots >= 42 ? paramSlots : 42,
    };
  }, []);

  const updatedLabel = formatUpdatedLine(milkComparisonPage.generated_at);

  useEffect(() => {
    if (reduceMotion) return;
    const id = window.setInterval(
      () => setInsightIndex((i) => (i + 1) % INSIGHT_LINES.length),
      7000
    );
    return () => window.clearInterval(id);
  }, [reduceMotion]);

  return (
    <Link
      href={href}
      className={cn(
        "group/card relative block overflow-hidden rounded-[1.35rem]",
        "border border-[#1A1D24]/[0.08] shadow-[0_32px_100px_-60px_rgba(17,19,24,0.35)] ring-1 ring-[#FFFFFF]/80",
        "transition-[transform,box-shadow,border-color] duration-500 ease-out",
        "hover:-translate-y-1 hover:border-[#1F8F6A]/30",
        "hover:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      <div
        className="pointer-events-none absolute inset-0 bg-[linear-gradient(135deg,#FDFDF8_0%,#F4F6F3_42%,#EEF5F1_100%)]"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom_left,rgba(31,143,106,0.045),transparent_48%,transparent_72%,rgba(31,143,106,0.028))]"
        aria-hidden
      />

      <MilkIntelligenceBackdrop />
      <AnalysisParticles reduceMotion={reduceMotion} />

      <div className="relative z-[1] flex flex-col md:grid md:grid-cols-[minmax(0,2fr)_minmax(0,0.95fr)] md:items-stretch">
        <div className="order-2 flex flex-col justify-center px-6 pb-10 pt-8 sm:px-8 md:order-none lg:px-11 lg:py-11">
          <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
            <span className="rounded-md border border-[#1F8F6A]/14 bg-[#1F8F6A]/[0.06] px-2 py-0.5 text-[0.58rem] font-extrabold tracking-wide text-[#1F8F6A]">
              דוח ראשון
            </span>
            <span className="text-[0.62rem] font-bold uppercase tracking-[0.22em] text-[#8A928A]">
              Bari Intel
            </span>
            <span className="h-px w-5 bg-[#1F8F6A]/15" aria-hidden />
            <span className="text-[0.65rem] font-semibold tracking-wide text-[#4E5663]">
              חלב · תחליפי חלב · משקאות חלבון
            </span>
          </div>

          <h3 className="mt-5 text-balance text-2xl font-extrabold leading-[1.12] tracking-[-0.045em] text-[#12151A] sm:text-[1.75rem] lg:text-[2rem] lg:tracking-[-0.05em]">
            {milkComparisonPage.comparison_title}
          </h3>

          <p className="mt-3 max-w-2xl text-pretty text-sm leading-[1.7] text-[#4E5663] sm:text-[0.95rem] lg:mt-4">
            {description}
          </p>

          <div className="mt-6 lg:mt-8">
            <div className="mb-3 flex items-center gap-3">
              <span
                className="h-[2px] w-8 rounded-full bg-gradient-to-l from-[#1F8F6A]/40 to-transparent shadow-[0_0_12px_-2px_rgba(31,143,106,0.25)]"
                aria-hidden
              />
              <h4 className="font-heading text-[0.8125rem] font-semibold leading-none tracking-[-0.02em] text-[#3A413D] antialiased">
                תובנות מרכזיות
              </h4>
            </div>
            <div
              aria-live={reduceMotion ? undefined : "polite"}
              className="relative mt-0 min-h-[3.65rem] overflow-hidden rounded-xl border border-[#1F8F6A]/12 bg-[#FFFFFF]/75 px-4 py-3 shadow-[inset_0_1px_0_rgba(255,255,255,0.65)] backdrop-blur-[3px]"
            >
              {!reduceMotion ? (
                <motion.div
                  className="pointer-events-none absolute inset-y-0 w-2/5 bg-gradient-to-r from-transparent via-[#1F8F6A]/[0.038] to-transparent"
                  initial={{ x: "-100%" }}
                  animate={{ x: "320%" }}
                  transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                  aria-hidden
                />
              ) : null}
              <AnimatePresence mode="wait">
                <motion.p
                  key={INSIGHT_LINES[insightIndex]}
                  initial={
                    reduceMotion ? { opacity: 1, y: 0 } : { opacity: 0, y: 5 }
                  }
                  animate={{ opacity: 1, y: 0 }}
                  exit={
                    reduceMotion ? { opacity: 1, y: 0 } : { opacity: 0, y: -5 }
                  }
                  transition={{ duration: 1.05, ease: [0.25, 0.1, 0.25, 1] }}
                  className="relative z-[1] text-sm font-medium leading-snug text-[#2C322E]"
                >
                  {INSIGHT_LINES[insightIndex]}
                </motion.p>
              </AnimatePresence>
            </div>
          </div>

          <div className="mt-5 flex flex-wrap gap-x-3 gap-y-1.5 border-t border-black/[0.05] pt-5 text-[0.62rem] font-medium tabular-nums leading-relaxed text-[#8A918B]">
            <span>
              <strong className="font-bold text-[#5C645E]">{metadata.productCount}</strong> מוצרים נותחו
            </span>
            <span className="text-[#D5DAD6]" aria-hidden>
              ·
            </span>
            <span>
              <strong className="font-bold text-[#5C645E]">{metadata.paramCount}</strong> פרמטרים הושוו
            </span>
            <span className="text-[#D5DAD6]" aria-hidden>
              ·
            </span>
            <span>
              <strong className="font-bold text-[#5C645E]">{metadata.categoryCount}</strong> קטגוריות
            </span>
            <span className="text-[#D5DAD6]" aria-hidden>
              ·
            </span>
            <span>{updatedLabel}</span>
          </div>

          <div className="mt-7">
            <span
              className={cn(
                "relative isolate inline-flex items-center gap-2 overflow-hidden rounded-2xl border border-[#1F8F6A]/38",
                "bg-[#1F8F6A] px-6 py-3.5 text-sm font-bold text-[#FAFAFA]",
                "shadow-[inset_0_1px_0_rgba(255,255,255,0.2),0_14px_40px_-16px_rgba(31,143,106,0.58)]",
                "transition-[transform,box-shadow] duration-500",
                "group-hover/card:-translate-x-px group-hover/card:shadow-[inset_0_1px_0_rgba(255,255,255,0.24),0_18px_48px_-12px_rgba(31,143,106,0.48)]"
              )}
            >
              <span className="pointer-events-none absolute inset-x-0 top-0 h-px bg-[#FFFFFF]/25" aria-hidden />
              <span className="relative">פתיחת דוח ההשוואה</span>
              <ChevronLeft className="relative size-[1.125rem] transition-transform duration-300 group-hover/card:-translate-x-0.5" />
            </span>
          </div>
        </div>

        <div className="relative isolate order-1 min-h-[280px] border-b border-black/[0.055] px-7 pb-2 pt-4 md:order-none md:border-b-0 md:border-s md:border-black/[0.06] md:pt-6 lg:min-h-[340px] lg:px-8 lg:pb-4 lg:pt-5">
          <div className="pointer-events-none absolute inset-[6%_6%_10%_6%] rounded-[3rem] bg-[radial-gradient(ellipse_at_38%_32%,rgba(255,255,255,0.97),transparent_62%)]" />

          <div className="relative mx-auto flex h-full min-h-[252px] w-full max-w-[348px] items-end justify-center pb-2 pt-2 lg:max-w-none lg:pb-0">
            <div
              className="pointer-events-none absolute bottom-[14%] left-1/2 h-[58%] w-[62%] max-w-[220px] -translate-x-1/2 rounded-[2.25rem] bg-[#C8D8D2]/28 blur-2xl"
              aria-hidden
            />

            <div className="relative -mt-1 mb-1 flex items-end justify-center ps-6 pe-8 md:-mt-2 md:ps-9 md:pe-11">
              {heroProducts.map((p, i) => {
                const cfg = PACK_CONFIG[i];
                if (!cfg) return null;
                return (
                  <div
                    key={p.barcode}
                    className={cn("relative shrink-0", i > 0 && "-ms-[3rem] sm:-ms-[3.15rem]")}
                    style={{
                      zIndex: cfg.z,
                      marginBottom: cfg.y,
                    }}
                  >
                    <motion.div
                      animate={
                        reduceMotion
                          ? undefined
                          : {
                              y: [0, -5, 0],
                            }
                      }
                      transition={{
                        repeat: Infinity,
                        duration: 6 + i * 0.4,
                        delay: i * 0.42,
                        ease: "easeInOut",
                      }}
                      className={cn(
                        "relative overflow-hidden rounded-[1.65rem]",
                        "bg-[linear-gradient(165deg,#FFFFFF_8%,#F3F8F6_100%)]",
                        "shadow-[0_28px_64px_-34px_rgba(17,19,24,0.52),0_16px_38px_-26px_rgba(31,143,106,0.07),inset_0_1px_0_rgba(255,255,255,1)]",
                        "ring-1 ring-black/[0.07]"
                      )}
                      style={{
                        width: cfg.w,
                        height: cfg.h,
                        rotate: `${cfg.rot}deg`,
                      }}
                    >
                      <Image
                        src={p.image_url!}
                        alt=""
                        fill
                        className="object-contain p-3"
                        sizes={cfg.w >= 132 ? "150px" : "110px"}
                      />
                    </motion.div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
}
