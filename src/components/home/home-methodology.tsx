"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { motion } from "framer-motion";
import { Activity, BarChart3, CheckCircle2, Layers3, Sparkles } from "lucide-react";

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
          "absolute inset-6 rounded-full border border-emerald-900/5 bg-emerald-900/[0.025] transition-opacity duration-700",
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
        <g className="text-zinc-200">
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
            fill="rgba(24,24,27,0.035)"
            stroke="rgba(113,113,122,0.54)"
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
            stroke="#047857"
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
          stroke="#047857"
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
                fill={isActive ? "#059669" : "#047857"}
                stroke="white"
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
                  isActive && "fill-zinc-950"
                )}
              >
                {signal.axis}
              </text>
            </g>
          );
        })}
      </svg>

      <div className="pointer-events-none absolute inset-0 z-20 grid place-items-center">
        <div className="w-36 rounded-[1.4rem] border border-zinc-200/80 bg-white/88 px-4 py-3 text-center shadow-sm shadow-zinc-950/[0.05] backdrop-blur-md">
          <div className="text-[0.62rem] font-bold uppercase tracking-[0.18em] text-emerald-800">
            Signal Focus
          </div>
          <div className="mt-1 text-sm font-extrabold tracking-[-0.02em] text-zinc-950">
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

  return (
    <motion.div
      className="group rounded-2xl border border-zinc-200/70 bg-white px-4 py-3 shadow-sm shadow-zinc-950/[0.02] transition-[border-color,box-shadow] duration-500 ease-out hover:border-emerald-900/15 hover:shadow-md hover:shadow-zinc-950/[0.04]"
      whileHover={reduceMotion ? undefined : { y: -2 }}
      transition={{ duration: 0.45, ease: "easeOut" }}
    >
      <div className="mb-2 flex items-center justify-between gap-4">
        <div>
          <div className="text-sm font-bold text-zinc-950 transition-colors duration-300 group-hover:text-emerald-950">
            {row.label}
          </div>
          <div className="mt-0.5 text-xs text-zinc-500 transition-colors duration-300 group-hover:text-zinc-600">
            {row.note}
          </div>
        </div>
        <div className="text-left">
          <div className="text-sm font-extrabold text-emerald-800">{row.value}</div>
          <div className="text-[0.62rem] font-bold uppercase tracking-[0.14em] text-zinc-400">Bari</div>
        </div>
      </div>

      <div className="relative h-3 overflow-visible rounded-full bg-zinc-100 shadow-inner shadow-zinc-950/[0.035]">
        <div className="absolute inset-y-0 end-0 w-full overflow-hidden rounded-full">
          <motion.div
            className="h-full rounded-full bg-zinc-950 transition-[width,background-color,box-shadow] ease-out group-hover:bg-emerald-800 group-hover:shadow-[0_0_0_1px_rgba(4,120,87,0.08)]"
            initial={false}
            animate={{ width: inView ? `${row.value}%` : "0%" }}
            transition={{
              delay: reduceMotion ? 0 : delay / 1000,
              duration: reduceMotion ? 0 : 1.5,
              ease: [0.22, 1, 0.36, 1],
            }}
          />
        </div>

        <motion.div
          className="absolute z-10 size-3 rounded-full border-2 border-white bg-emerald-700 shadow-sm shadow-emerald-950/20 transition-colors duration-300 group-hover:bg-emerald-600"
          initial={false}
          animate={
            inView
              ? {
                  opacity: 1,
                  x: reduceMotion ? 0 : [-2, 2, -2],
                }
              : { opacity: 0, x: 0 }
          }
          transition={
            inView && !reduceMotion
              ? {
                  opacity: { delay: (delay + 420) / 1000, duration: 0.7, ease: "easeOut" },
                  x: {
                    delay: (delay + 900) / 1000,
                    duration: 3.8,
                    ease: "easeInOut",
                    repeat: Infinity,
                  },
                }
              : { duration: 0 }
          }
          style={{
            right: `${row.category}%`,
            top: "50%",
            marginTop: "-0.375rem",
          }}
          aria-hidden
        />
      </div>

      <div className="mt-2 flex justify-between text-[0.68rem] font-medium text-zinc-400">
        <span>חלש</span>
        <span className="transition-colors duration-300 group-hover:text-emerald-800">קו קטגוריה</span>
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
    <section ref={ref} className="relative overflow-hidden bg-white py-20 md:py-28" id="methodology">
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-40 bg-gradient-to-b from-[#f7f8f6] to-white"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-x-6 top-24 h-px bg-gradient-to-l from-transparent via-emerald-900/10 to-transparent"
        aria-hidden
      />

      <HomeContainer>
        <div
          className={cn(
            "mx-auto mb-12 max-w-3xl text-center transition-all duration-1000 ease-out",
            inView ? "translate-y-0 opacity-100" : "translate-y-4 opacity-0"
          )}
        >
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-emerald-800">
            Multidimensional food intelligence
          </p>
          <h2 className="mt-3 text-balance text-3xl font-extrabold tracking-[-0.045em] text-zinc-950 md:text-5xl">
            לא ציון אחד. מערכת אותות.
          </h2>
          <p className="mx-auto mt-5 max-w-2xl text-pretty text-base leading-relaxed text-zinc-600 md:text-lg">
            Bari מנתחת את המציאות הנראית של המוצר: רכיבים, עיבוד, ערכים תזונתיים והקשר קטגורי
            נקראים יחד כדי לייצר תמונה עמוקה אבל קריאה.
          </p>
        </div>

        <div
          className={cn(
            "grid gap-6 rounded-[2rem] border border-zinc-200/70 bg-white/90 p-4 shadow-[0_28px_90px_-62px_rgba(24,24,27,0.5)] backdrop-blur-sm transition-all duration-1000 ease-out md:p-6 lg:grid-cols-[minmax(0,1.08fr)_minmax(320px,0.92fr)] lg:items-stretch",
            inView ? "translate-y-0 opacity-100" : "translate-y-6 opacity-0"
          )}
        >
          <div className="relative overflow-hidden rounded-[1.65rem] border border-zinc-200/70 bg-[#fbfbf8] p-4 md:p-6">
            <div className="mb-4 flex items-center justify-between gap-3">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.18em] text-zinc-500">Live product profile</p>
                <h3 className="mt-1 text-xl font-extrabold tracking-[-0.035em] text-zinc-950">
                  ניתוח מוצר רב־ממדי
                </h3>
              </div>
              <div className="rounded-full border border-emerald-900/10 bg-emerald-50 px-3 py-1 text-xs font-bold text-emerald-900">
                8 אותות
              </div>
            </div>

            <SignalRadar
              activeSignal={activeSignal}
              inView={inView}
              onSignalChange={setActiveSignal}
              reduceMotion={reduceMotion}
            />

            <div className="mt-5 rounded-2xl border border-zinc-200/70 bg-white/85 p-4 shadow-sm shadow-zinc-950/[0.02]">
              <div className="mb-2 flex items-center gap-2 text-sm font-extrabold text-zinc-950">
                <Sparkles className="size-4 text-emerald-700" aria-hidden />
                {activeSignalData.axis}
              </div>
              <p className="text-sm leading-relaxed text-zinc-600">{activeSignalData.detail}</p>
            </div>
          </div>

          <div className="flex flex-col justify-between gap-7 p-1 md:p-2">
            <div className="space-y-3">
              <p className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-500">
                Category-adjusted benchmarks
              </p>
              <h3 className="text-2xl font-extrabold tracking-[-0.04em] text-zinc-950 md:text-3xl">
                ההשוואה מתרחשת בתוך ההקשר של המזון.
              </h3>
              <p className="text-pretty text-sm leading-relaxed text-zinc-600 md:text-base">
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
                      "rounded-2xl border border-zinc-200/70 bg-zinc-50/70 p-4 transition-all duration-700 ease-out",
                      inView ? "translate-y-0 opacity-100" : "translate-y-3 opacity-0"
                    )}
                    style={{
                      transitionDelay: reduceMotion ? "0ms" : `${520 + index * 110}ms`,
                      transitionDuration: reduceMotion ? "0ms" : undefined,
                    }}
                  >
                    <Icon className="mb-3 size-5 text-emerald-700" aria-hidden />
                    <h4 className="text-sm font-extrabold text-zinc-950">{card.title}</h4>
                    <p className="mt-2 text-xs leading-relaxed text-zinc-500">{card.text}</p>
                  </div>
                );
              })}
            </div>

            <div className="flex items-start gap-3 rounded-2xl border border-emerald-900/10 bg-emerald-50/70 px-4 py-3 text-sm leading-relaxed text-emerald-950">
              <BarChart3 className="mt-0.5 size-5 shrink-0 text-emerald-700" aria-hidden />
              <p>
                פחמימות אינן בעיה בפני עצמן. Bari בודקת מה המקור שלהן, איך הן משתלבות במוצר,
                ומה מצופה מהקטגוריה.
              </p>
            </div>
          </div>
        </div>
      </HomeContainer>
    </section>
  );
}
