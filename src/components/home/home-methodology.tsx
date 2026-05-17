"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { motion } from "framer-motion";
import { Activity, CheckCircle2, Layers3, Sparkles } from "lucide-react";

import { HomeContainer } from "./section-frame";
import { cn } from "@/lib/utils";

const radarSignals = [
  {
    axis: "איכות רכיבים",
    value: 84,
    benchmark: 56,
    detail: "זיהוי רכיבים מוכרים, מקורות מלאים וסדר הופעה ברשימה.",
  },
  {
    axis: "עומס עיבוד",
    value: 38,
    benchmark: 63,
    detail: "אות נמוך עדיף כאן: פחות סימני עיבוד, מייצבים ומניפולציות טקסטורה.",
  },
  {
    axis: "איכות פחמימה",
    value: 76,
    benchmark: 51,
    detail: "פחמימות נבחנות לפי מקור, סיבים והקשר קטגורי, לא נענשות אוטומטית.",
  },
  {
    axis: "צפיפות חלבון",
    value: 68,
    benchmark: 47,
    detail: "יחס חלבון למשקל, לאנרגיה ולציפייה ממוצרים באותה קטגוריה.",
  },
  {
    axis: "מורכבות תוספים",
    value: 35,
    benchmark: 59,
    detail: "אות נמוך עדיף: פחות תוספים, ממתיקים ורכיבי עזר לא הכרחיים.",
  },
  {
    axis: "צפיפות תזונתית",
    value: 79,
    benchmark: 54,
    detail: "כמה ערך תזונתי ממשי מתקבל ביחס לנפח, אנרגיה וקטגוריה.",
  },
  {
    axis: "איכות שומנים",
    value: 64,
    benchmark: 49,
    detail: "מקור השומן, איזון יחסי וסימנים לרכיבים עתירי שומן בעייתי.",
  },
  {
    axis: "ביטחון ניתוח",
    value: 82,
    benchmark: 58,
    detail: "רמת בהירות הנתונים, התאמה לקטגוריה ויכולת להסביר את המסקנה.",
  },
] as const;

const benchmarkRows = [
  {
    label: "מקור פחמימה",
    value: 76,
    category: 51,
    note: "מקור וסיבים לפני ספירת גרמים",
  },
  {
    label: "רכיבים מזוהים",
    value: 84,
    category: 56,
    note: "רשימה קצרה וברורה יותר",
  },
  {
    label: "עיבוד ותוספים",
    value: 65,
    category: 41,
    note: "פחות סימני עיבוד ביחס למדף",
  },
  {
    label: "צפיפות תזונתית",
    value: 79,
    category: 54,
    note: "יותר ערך תזונתי לכל החלטה",
  },
] as const;

const interpretationCards = [
  {
    icon: Layers3,
    title: "נרמול לפי קטגוריה",
    text: "לחם, יוגורט וחטיף לא נמדדים באותו סרגל. Bari משווה מוצר למציאות התחרותית שלו.",
  },
  {
    icon: Activity,
    title: "אותות במקביל",
    text: "רכיבים, עיבוד, צפיפות, פחמימה, חלבון וביטחון נקראים יחד במקום להפוך הכול למספר בודד.",
  },
  {
    icon: CheckCircle2,
    title: "הסבר שניתן להבין",
    text: "הפלט נשאר קריא: מה חזק, מה חלש, ואיזה פרט בתווית באמת משנה.",
  },
] as const;

function useInView<T extends HTMLElement>() {
  const ref = useRef<T | null>(null);
  const [inView, setInView] = useState(false);

  useEffect(() => {
    const element = ref.current;

    if (!element) {
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setInView(true);
          observer.disconnect();
        }
      },
      { rootMargin: "0px 0px -14% 0px", threshold: 0.22 }
    );

    observer.observe(element);

    return () => observer.disconnect();
  }, []);

  return { ref, inView };
}

function usePrefersReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(() => {
    if (typeof window === "undefined") {
      return false;
    }

    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  });

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    const handleChange = () => setPrefersReducedMotion(mediaQuery.matches);

    mediaQuery.addEventListener("change", handleChange);

    return () => mediaQuery.removeEventListener("change", handleChange);
  }, []);

  return prefersReducedMotion;
}

function getPoint(value: number, index: number, total: number, radius = 128) {
  const center = 180;
  const angle = (Math.PI * 2 * index) / total - Math.PI / 2;
  const scaledRadius = radius * (value / 100);

  return {
    x: center + Math.cos(angle) * scaledRadius,
    y: center + Math.sin(angle) * scaledRadius,
  };
}

function pointsToString(points: { x: number; y: number }[]) {
  return points.map((point) => `${point.x},${point.y}`).join(" ");
}

function clampPercent(value: number) {
  return Math.min(96, Math.max(4, value));
}

function SignalRadar({
  activeSignal,
  inView,
  onSignalChange,
  reduceMotion,
}: {
  activeSignal: number;
  inView: boolean;
  onSignalChange: (index: number) => void;
  reduceMotion: boolean;
}) {
  const total = radarSignals.length;
  const productPoints = useMemo(
    () => radarSignals.map((signal, index) => getPoint(signal.value, index, total)),
    [total]
  );
  const benchmarkPoints = useMemo(
    () => radarSignals.map((signal, index) => getPoint(signal.benchmark, index, total)),
    [total]
  );
  const activePoint = productPoints[activeSignal];
  const activeSignalData = radarSignals[activeSignal];
  const transform = inView ? "scale(1)" : "scale(0.08)";
  const transition = reduceMotion
    ? "none"
    : "transform 1100ms cubic-bezier(0.22, 1, 0.36, 1), opacity 700ms ease-out";

  return (
    <div className="relative mx-auto w-full max-w-[32rem]">
      <div
        className={cn(
          "absolute inset-6 rounded-full border border-emerald-300/10 bg-emerald-300/[0.03] transition-opacity duration-700",
          inView ? "opacity-100" : "opacity-0"
        )}
        aria-hidden
      />
      <svg
        viewBox="0 0 360 360"
        className="relative z-10 aspect-square w-full overflow-visible"
        role="img"
        aria-label="פרופיל רדאר של אותות תזונתיים ורכיביים"
      >
        <g className="text-white/10">
          {[0.25, 0.5, 0.75, 1].map((level) => (
            <polygon
              key={level}
              points={pointsToString(radarSignals.map((_, index) => getPoint(level * 100, index, total)))}
              fill="none"
              stroke="currentColor"
              strokeWidth="1"
            />
          ))}
          {radarSignals.map((_, index) => {
            const end = getPoint(100, index, total);

            return <line key={index} x1="180" y1="180" x2={end.x} y2={end.y} stroke="currentColor" strokeWidth="1" />;
          })}
        </g>

        <g
          style={{
            opacity: inView ? 1 : 0,
            transform,
            transformOrigin: "180px 180px",
            transition,
            transitionDelay: reduceMotion ? "0ms" : "140ms",
          }}
        >
          <polygon
            points={pointsToString(benchmarkPoints)}
            fill="rgba(255,255,255,0.035)"
            stroke="rgba(161,161,170,0.42)"
            strokeDasharray="4 6"
            strokeWidth="1.5"
          />
        </g>

        <g
          style={{
            opacity: inView ? 1 : 0,
            transform,
            transformOrigin: "180px 180px",
            transition,
            transitionDelay: reduceMotion ? "0ms" : "260ms",
          }}
        >
          <polygon
            points={pointsToString(productPoints)}
            fill="rgba(4,120,87,0.13)"
            stroke="#34d399"
            strokeLinejoin="round"
            strokeWidth="2.5"
          />
          <polyline
            points={`${pointsToString(productPoints)} ${productPoints[0].x},${productPoints[0].y}`}
            fill="none"
            stroke="rgba(5,150,105,0.28)"
            strokeWidth="8"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </g>

        <line
          x1="180"
          y1="180"
          x2={activePoint.x}
          y2={activePoint.y}
          stroke="#34d399"
          strokeWidth="1.5"
          strokeDasharray="3 5"
          className="transition-all duration-500 ease-out"
        />

        {radarSignals.map((signal, index) => {
          const point = productPoints[index];
          const labelPoint = getPoint(113, index, total);
          const isActive = activeSignal === index;

          return (
            <g
              key={signal.axis}
              onMouseEnter={() => onSignalChange(index)}
              onFocus={() => onSignalChange(index)}
              tabIndex={0}
              className="cursor-default outline-none"
              style={{
                opacity: inView ? 1 : 0,
                transition: reduceMotion ? "none" : "opacity 600ms ease-out",
                transitionDelay: `${360 + index * 70}ms`,
              }}
            >
              <circle
                cx={point.x}
                cy={point.y}
                r={isActive ? 6 : 4}
                fill={isActive ? "#34d399" : "#10b981"}
                stroke="#07110c"
                strokeWidth="2"
                className="transition-all duration-300"
                style={{
                  animation:
                    inView && !reduceMotion
                      ? `bari-signal-point-pulse 900ms ease-out ${520 + index * 80}ms 1 both`
                      : "none",
                  transformOrigin: `${point.x}px ${point.y}px`,
                }}
              />
              <text
                x={labelPoint.x}
                y={labelPoint.y}
                textAnchor={labelPoint.x > 194 ? "start" : labelPoint.x < 166 ? "end" : "middle"}
                dominantBaseline="middle"
                className={cn(
                  "fill-zinc-500 text-[0.62rem] font-bold transition-colors duration-300",
                  isActive && "fill-emerald-100"
                )}
              >
                {signal.axis}
              </text>
            </g>
          );
        })}
      </svg>

      <div className="pointer-events-none absolute inset-0 z-20 grid place-items-center">
        <div className="w-36 rounded-[1.4rem] border border-emerald-300/12 bg-zinc-950/75 px-4 py-3 text-center shadow-sm shadow-black/30 backdrop-blur-md">
          <div className="text-[0.62rem] font-bold uppercase tracking-[0.18em] text-emerald-200/80">
            Signal Focus
          </div>
          <div className="mt-1 text-sm font-extrabold tracking-[-0.02em] text-white">
            {activeSignalData.axis}
          </div>
          <div className="mt-1 text-xs font-semibold text-zinc-500">{activeSignalData.value}/100</div>
        </div>
      </div>
    </div>
  );
}

function SignalBenchmarkRow({
  index,
  inView,
  reduceMotion,
  row,
}: {
  index: number;
  inView: boolean;
  reduceMotion: boolean;
  row: (typeof benchmarkRows)[number];
}) {
  const delay = 180 + index * 130;
  const fillDrift = 3 + (index % 2);
  const markerDrift = 2 + (index % 3);
  const fillMotion = [
    `${clampPercent(row.value - fillDrift)}%`,
    `${clampPercent(row.value + fillDrift)}%`,
    `${clampPercent(row.value - fillDrift)}%`,
  ];
  const markerMotion = [
    `${clampPercent(row.category - markerDrift)}%`,
    `${clampPercent(row.category + markerDrift)}%`,
    `${clampPercent(row.category - markerDrift)}%`,
  ];
  const loopDuration = 4.8 + index * 0.35;

  return (
    <motion.div
      className="group rounded-2xl border border-emerald-300/10 bg-white/[0.045] px-4 py-3 shadow-sm shadow-black/20 backdrop-blur-sm transition-[border-color,box-shadow,background-color] duration-500 ease-out hover:border-emerald-300/20 hover:bg-white/[0.06] hover:shadow-md hover:shadow-emerald-950/15"
      whileHover={reduceMotion ? undefined : { y: -2 }}
      transition={{ duration: 0.45, ease: "easeOut" }}
    >
      <div className="mb-2 flex items-center justify-between gap-4">
        <div>
          <div className="text-sm font-bold text-white transition-colors duration-300 group-hover:text-emerald-100">
            {row.label}
          </div>
          <div className="mt-0.5 text-xs text-zinc-500 transition-colors duration-300 group-hover:text-zinc-400">
            {row.note}
          </div>
        </div>
        <div className="text-left">
          <div className="text-sm font-extrabold text-emerald-200">{row.value}</div>
          <div className="text-[0.62rem] font-bold uppercase tracking-[0.14em] text-zinc-400">Bari</div>
        </div>
      </div>

      <div className="relative h-3 overflow-visible rounded-full bg-zinc-950/70 shadow-inner shadow-black/30">
        <div className="absolute inset-y-0 end-0 w-full overflow-hidden rounded-full">
          <motion.div
            className="h-full rounded-full bg-emerald-300/70 transition-[width,background-color,box-shadow] ease-out group-hover:bg-emerald-300 group-hover:shadow-[0_0_18px_rgba(16,185,129,0.18)]"
            initial={false}
            animate={{ width: inView ? (reduceMotion ? `${row.value}%` : fillMotion) : "0%" }}
            transition={{
              delay: reduceMotion ? 0 : delay / 1000,
              duration: reduceMotion ? 0 : loopDuration,
              ease: "easeInOut",
              repeat: inView && !reduceMotion ? Infinity : 0,
            }}
          />
        </div>

        <motion.div
          className="absolute z-10 size-3 rounded-full border-2 border-zinc-950 bg-emerald-300 shadow-sm shadow-emerald-950/20 transition-colors duration-300 group-hover:bg-emerald-200"
          initial={false}
          animate={
            inView
              ? {
                  opacity: 1,
                  right: reduceMotion ? `${row.category}%` : markerMotion,
                }
              : { opacity: 0, right: `${row.category}%` }
          }
          transition={
            inView && !reduceMotion
              ? {
                  opacity: { delay: (delay + 420) / 1000, duration: 0.7, ease: "easeOut" },
                  right: {
                    delay: (delay + 900) / 1000,
                    duration: loopDuration,
                    ease: "easeInOut",
                    repeat: Infinity,
                  },
                }
              : { duration: 0 }
          }
          style={{
            top: "50%",
            marginTop: "-0.375rem",
          }}
          aria-hidden
        />
      </div>

      <div className="mt-2 flex justify-between text-[0.68rem] font-medium text-zinc-500">
        <span>חלש</span>
        <span className="transition-colors duration-300 group-hover:text-emerald-200">קו קטגוריה</span>
        <span>חזק</span>
      </div>
    </motion.div>
  );
}

function SignalBenchmarkBars({ inView, reduceMotion }: { inView: boolean; reduceMotion: boolean }) {
  return (
    <div className="space-y-4">
      {benchmarkRows.map((row, index) => (
        <SignalBenchmarkRow
          key={row.label}
          index={index}
          inView={inView}
          reduceMotion={reduceMotion}
          row={row}
        />
      ))}
    </div>
  );
}

export function HomeMethodology() {
  const { ref, inView } = useInView<HTMLElement>();
  const reduceMotion = usePrefersReducedMotion();
  const [activeSignal, setActiveSignal] = useState(2);

  useEffect(() => {
    if (!inView || reduceMotion) {
      return;
    }

    const interval = window.setInterval(() => {
      setActiveSignal((current) => (current + 1) % radarSignals.length);
    }, 2800);

    return () => window.clearInterval(interval);
  }, [inView, reduceMotion]);

  const activeSignalData = radarSignals[activeSignal];

  return (
    <section ref={ref} className="relative overflow-hidden py-20 md:py-28" id="methodology">
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_22%_22%,rgba(16,185,129,0.08),transparent_32%),radial-gradient(circle_at_84%_72%,rgba(16,185,129,0.045),transparent_34%)]"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-x-6 top-24 h-px bg-gradient-to-l from-transparent via-emerald-300/12 to-transparent"
        aria-hidden
      />

      <HomeContainer>
        <div
          className={cn(
            "mx-auto mb-12 max-w-3xl text-center transition-all duration-1000 ease-out",
            inView ? "translate-y-0 opacity-100" : "translate-y-4 opacity-0"
          )}
        >
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-emerald-200/80">
            Multidimensional food intelligence
          </p>
          <h2 className="mt-3 text-balance text-3xl font-extrabold tracking-[-0.045em] text-white md:text-5xl">
            לא ציון אחד. מערכת אותות.
          </h2>
          <p className="mx-auto mt-5 max-w-2xl text-pretty text-base leading-relaxed text-zinc-400 md:text-lg">
            Bari מנתחת את המציאות הנראית של המוצר: רכיבים, עיבוד, ערכים תזונתיים והקשר קטגורי
            נקראים יחד כדי לייצר תמונה עמוקה אבל קריאה.
          </p>
        </div>

        <div
          className={cn(
            "grid gap-6 rounded-[2rem] border border-emerald-300/10 bg-white/[0.045] p-4 shadow-[0_36px_120px_-74px_rgba(0,0,0,0.95)] backdrop-blur-xl transition-all duration-1000 ease-out md:p-6 lg:grid-cols-[minmax(0,1.08fr)_minmax(320px,0.92fr)] lg:items-stretch",
            inView ? "translate-y-0 opacity-100" : "translate-y-6 opacity-0"
          )}
        >
          <div className="relative overflow-hidden rounded-[1.65rem] border border-emerald-300/10 bg-zinc-950/45 p-4 md:p-6">
            <div className="mb-4 flex items-center justify-between gap-3">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.18em] text-zinc-500">Live product profile</p>
                <h3 className="mt-1 text-xl font-extrabold tracking-[-0.035em] text-white">
                  ניתוח מוצר רב־ממדי
                </h3>
              </div>
              <div className="rounded-full border border-emerald-300/10 bg-emerald-300/[0.06] px-3 py-1 text-xs font-bold text-emerald-100">
                8 אותות
              </div>
            </div>

            <SignalRadar
              activeSignal={activeSignal}
              inView={inView}
              onSignalChange={setActiveSignal}
              reduceMotion={reduceMotion}
            />

            <div className="mt-5 rounded-2xl border border-emerald-300/10 bg-white/[0.045] p-4 shadow-sm shadow-black/20">
              <div className="mb-2 flex items-center gap-2 text-sm font-extrabold text-white">
                <Sparkles className="size-4 text-emerald-200" aria-hidden />
                {activeSignalData.axis}
              </div>
              <p className="text-sm leading-relaxed text-zinc-400">{activeSignalData.detail}</p>
            </div>
          </div>

          <div className="flex flex-col justify-between gap-7 p-1 md:p-2">
            <div className="space-y-3">
              <p className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-500">
                Category-adjusted benchmarks
              </p>
              <h3 className="text-2xl font-extrabold tracking-[-0.04em] text-white md:text-3xl">
                ההשוואה מתרחשת בתוך ההקשר של המזון.
              </h3>
              <p className="text-pretty text-sm leading-relaxed text-zinc-400 md:text-base">
                כל פס מציג אות אחד מול ציפייה קטגורית. כך Bari יכולה לזהות מוצר עם פחמימה איכותית,
                רשימת רכיבים טובה או עיבוד נמוך בלי להפוך את הניתוח לספירת קלוריות.
              </p>
            </div>

            <SignalBenchmarkBars inView={inView} reduceMotion={reduceMotion} />

            <div className="grid gap-3 sm:grid-cols-3">
              {interpretationCards.map((card, index) => {
                const Icon = card.icon;

                return (
                  <div
                    key={card.title}
                    className={cn(
                      "rounded-2xl border border-emerald-300/10 bg-white/[0.035] p-4 transition-all duration-700 ease-out",
                      inView ? "translate-y-0 opacity-100" : "translate-y-3 opacity-0"
                    )}
                    style={{
                      transitionDelay: reduceMotion ? "0ms" : `${520 + index * 110}ms`,
                      transitionDuration: reduceMotion ? "0ms" : undefined,
                    }}
                  >
                    <Icon className="mb-3 size-5 text-emerald-200" aria-hidden />
                    <h4 className="text-sm font-extrabold text-white">{card.title}</h4>
                    <p className="mt-2 text-xs leading-relaxed text-zinc-500">{card.text}</p>
                  </div>
                );
              })}
            </div>

          </div>
        </div>
      </HomeContainer>
    </section>
  );
}
