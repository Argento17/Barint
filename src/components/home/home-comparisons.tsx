"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import AutoScroll from "embla-carousel-auto-scroll";
import useEmblaCarousel from "embla-carousel-react";
import { ChevronLeft, ChevronRight, ShieldCheck } from "lucide-react";

import { Button } from "@/components/ui/button";

import { HomeContainer } from "./section-frame";

const comparisonReports = [
  {
    category: "משקאות צמחיים",
    title: "חלב שיבולת שועל A מול חלב שיבולת שועל B",
    products: ["Oat A", "Oat B"],
    sticker: "השוואה לדוגמה",
    summary: "פער קטן בסוכר, פער גדול יותר ברשימת הרכיבים ובכמות המייצבים.",
    scoreA: "84",
    scoreB: "67",
    signals: ["סוכר נמוך יותר", "רשימת רכיבים קצרה", "חלבון אינו יתרון מרכזי"],
  },
  {
    category: "חטיפים",
    title: "חטיף דגנים A מול חטיף דגנים B",
    products: ["Grain A", "Grain B"],
    sticker: "השוואת חטיפים",
    summary: "הדירוג משתנה בגלל שילוב של סוכר, שובע, תוספים ופשטות רכיבים.",
    scoreA: "79",
    scoreB: "58",
    signals: ["פערי סוכר", "ריבוי תוספים", "שובע משתנה"],
  },
  {
    category: "מוצרי חלב",
    title: "יוגורט חלבון A מול יוגורט חלבון B",
    products: ["Protein A", "Protein B"],
    sticker: "פרופיל חלבון",
    summary: "חלבון גבוה עוזר רק כשהסוכר והתוספים נשארים בפרופורציה קטגורית.",
    scoreA: "86",
    scoreB: "73",
    signals: ["חלבון גבוה", "סוכר בינוני", "מרקם ותוספים"],
  },
  {
    category: "דגני בוקר",
    title: "דגני בוקר A מול דגני בוקר B",
    products: ["Cereal A", "Cereal B"],
    sticker: "בדיקת מדף",
    summary: "ההשוואה נשענת על מקור הדגן, כמות סוכר, סיבים ותוספי טעם.",
    scoreA: "76",
    scoreB: "61",
    signals: ["מקור פחמימה", "סיבים", "טעמי עזר"],
  },
] as const;

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

function ComparisonReportCard({ report }: { report: (typeof comparisonReports)[number] }) {
  return (
    <article
      dir="rtl"
      className="relative flex h-full min-h-[23rem] w-[84vw] max-w-[34rem] shrink-0 snap-center flex-col overflow-hidden rounded-[2rem] border border-stone-200/80 bg-white/92 p-5 shadow-[0_28px_80px_-58px_rgba(24,24,27,0.6)] backdrop-blur-sm sm:w-[31rem] md:min-h-[25rem] md:w-[34rem] md:p-6"
    >
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_82%_12%,rgba(4,120,87,0.08),transparent_34%),linear-gradient(135deg,rgba(250,250,249,0.9),rgba(236,253,245,0.28))]"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-x-6 top-0 h-px bg-gradient-to-l from-transparent via-emerald-900/20 to-transparent"
        aria-hidden
      />

      <div className="relative z-10 flex h-full flex-col">
        <div className="mb-5 flex items-start justify-between gap-4">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.18em] text-emerald-900">
              Signal Review · {report.category}
            </p>
            <h3 className="mt-3 text-2xl font-extrabold leading-tight tracking-[-0.04em] text-zinc-950 md:text-3xl">
              {report.title}
            </h3>
          </div>
          <span className="shrink-0 rounded-full border border-emerald-900/10 bg-emerald-50/80 px-3 py-1 text-xs font-bold text-emerald-950">
            {report.sticker}
          </span>
        </div>

        <div className="grid gap-3 sm:grid-cols-[1fr_auto_1fr] sm:items-stretch">
          <div className="rounded-2xl border border-stone-200/80 bg-white/75 p-4 shadow-sm shadow-zinc-950/[0.02]">
            <div className="text-xs font-bold text-zinc-500">מוצר A</div>
            <div className="mt-2 text-lg font-extrabold text-zinc-950">{report.products[0]}</div>
            <div className="mt-4 inline-flex rounded-2xl border border-stone-200/80 bg-stone-50 px-4 py-3 text-center">
              <div>
                <div className="text-2xl font-extrabold tracking-[-0.05em] text-zinc-950">{report.scoreA}</div>
                <div className="text-[0.62rem] font-bold uppercase tracking-[0.16em] text-zinc-400">יחסי</div>
              </div>
            </div>
          </div>

          <div className="hidden w-px bg-stone-200/80 sm:block" aria-hidden />

          <div className="rounded-2xl border border-stone-200/80 bg-white/60 p-4 shadow-sm shadow-zinc-950/[0.02]">
            <div className="text-xs font-bold text-zinc-500">מוצר B</div>
            <div className="mt-2 text-lg font-extrabold text-zinc-950">{report.products[1]}</div>
            <div className="mt-4 inline-flex rounded-2xl border border-stone-200/80 bg-stone-50 px-4 py-3 text-center">
              <div>
                <div className="text-2xl font-extrabold tracking-[-0.05em] text-zinc-950">{report.scoreB}</div>
                <div className="text-[0.62rem] font-bold uppercase tracking-[0.16em] text-zinc-400">יחסי</div>
              </div>
            </div>
          </div>
        </div>

        <p className="mt-5 text-sm leading-relaxed text-zinc-600">{report.summary}</p>

        <div className="mt-auto pt-5">
          <div className="flex flex-wrap gap-2">
            {report.signals.map((signal) => (
              <span
                key={signal}
                className="rounded-full border border-stone-200/80 bg-white/75 px-3 py-1 text-xs font-semibold text-zinc-600"
              >
                {signal}
              </span>
            ))}
          </div>
        </div>
      </div>
    </article>
  );
}

export function HomeComparisons() {
  const prefersReducedMotion = usePrefersReducedMotion();
  const resumeTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const autoScrollPlugins = useMemo(
    () =>
      prefersReducedMotion
        ? []
        : [
            AutoScroll({
              playOnInit: true,
              speed: 0.18,
              startDelay: 1000,
              stopOnInteraction: false,
              stopOnMouseEnter: true,
            }),
          ],
    [prefersReducedMotion]
  );
  const [emblaRef, emblaApi] = useEmblaCarousel(
    {
      align: "start",
      direction: "rtl",
      dragFree: true,
      loop: true,
    },
    autoScrollPlugins
  );

  useEffect(() => {
    return () => {
      if (resumeTimeoutRef.current) {
        clearTimeout(resumeTimeoutRef.current);
      }
    };
  }, []);

  useEffect(() => {
    if (prefersReducedMotion) {
      return;
    }

    emblaApi?.plugins().autoScroll?.play(1000);
  }, [emblaApi, prefersReducedMotion]);

  const stopAutoScroll = () => {
    emblaApi?.plugins().autoScroll?.stop();
  };

  const resumeAutoScroll = (delay = 1000) => {
    if (prefersReducedMotion) {
      return;
    }

    if (resumeTimeoutRef.current) {
      clearTimeout(resumeTimeoutRef.current);
    }

    resumeTimeoutRef.current = setTimeout(() => {
      emblaApi?.plugins().autoScroll?.play();
    }, delay);
  };

  const moveCarousel = (direction: "right" | "left") => {
    if (!emblaApi) {
      return;
    }

    stopAutoScroll();

    if (direction === "right") {
      emblaApi.scrollNext();
    } else {
      emblaApi.scrollPrev();
    }

    resumeAutoScroll(4500);
  };

  return (
    <section className="relative overflow-hidden py-16 md:py-24" id="comparisons">
      <HomeContainer>
        <div className="reveal-up mb-10 flex flex-col items-start justify-between gap-6 md:mb-12 md:flex-row md:items-end">
          <div className="max-w-2xl space-y-3 text-right">
            <p className="text-xs font-bold uppercase tracking-[0.2em] text-emerald-800">Moving comparison reports</p>
            <h2 className="text-balance text-3xl font-extrabold tracking-[-0.045em] text-zinc-950 md:text-5xl">
              השוואות שמרגישות כמו מוצר חי
            </h2>
            <p className="text-pretty text-base leading-relaxed text-zinc-600 md:text-lg">
              דוגמאות קצרות שמראות איך Bari מפרק מוצרי מזון לאותות, הקשר קטגורי ורציונל השוואתי.
            </p>
          </div>
          <Button
            variant="ghost"
            className="hidden shrink-0 gap-2 text-emerald-700 hover:text-emerald-800 md:inline-flex"
            asChild
          >
            <a href="#methodology" className="font-semibold">
              <span>איך הניתוח עובד</span>
              <ChevronLeft className="size-5" aria-hidden />
            </a>
          </Button>
        </div>
        <div className="relative z-20 mb-6 flex items-center justify-start gap-2">
          <button
            type="button"
            onClick={() => moveCarousel("right")}
            className="inline-flex size-10 items-center justify-center rounded-full border border-stone-200/80 bg-white/80 text-zinc-700 shadow-sm shadow-zinc-950/[0.03] backdrop-blur-sm transition-[background-color,color,border-color,transform,box-shadow] duration-300 hover:-translate-y-px hover:border-emerald-900/15 hover:bg-zinc-950 hover:text-white hover:shadow-md hover:shadow-emerald-950/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-800/20"
            aria-label="הזזת הקרוסלה ימינה"
          >
            <ChevronRight className="pointer-events-none size-5" aria-hidden />
          </button>
          <button
            type="button"
            onClick={() => moveCarousel("left")}
            className="inline-flex size-10 items-center justify-center rounded-full border border-emerald-900/15 bg-zinc-950 text-white shadow-md shadow-emerald-950/10 ring-1 ring-emerald-300/20 transition-[background-color,color,border-color,transform,box-shadow] duration-300 hover:-translate-y-px hover:bg-zinc-900 hover:shadow-lg hover:shadow-emerald-950/15 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-800/25"
            aria-label="הזזת הקרוסלה שמאלה"
          >
            <ChevronLeft className="pointer-events-none size-5" aria-hidden />
          </button>
        </div>
      </HomeContainer>

      <div className="relative">
        <div
          className="pointer-events-none absolute inset-y-0 start-0 z-10 w-24 bg-gradient-to-e from-[#f7f8f6] to-transparent md:w-40"
          aria-hidden
        />
        <div
          className="pointer-events-none absolute inset-y-0 end-0 z-10 w-24 bg-gradient-to-s from-[#f7f8f6] to-transparent md:w-40"
          aria-hidden
        />

        <div
          ref={emblaRef}
          className="overflow-hidden pb-3"
          dir="rtl"
        >
          <div className="flex items-stretch gap-4 px-5 sm:px-6">
            {comparisonReports.map((report) => (
              <div key={report.title} className="flex flex-[0_0_auto] min-w-0" data-comparison-card>
                <ComparisonReportCard report={report} />
              </div>
            ))}
          </div>
        </div>
      </div>

      <HomeContainer className="mt-6">
        <div className="flex items-center gap-2 rounded-2xl border border-stone-200/80 bg-white/72 px-4 py-3 text-xs font-medium text-zinc-500 shadow-sm shadow-zinc-950/[0.02] backdrop-blur-sm">
          <ShieldCheck className="size-4 text-emerald-700" aria-hidden />
          הדוגמאות ממחישות את חוויית ההשוואה. נתוני מוצר אמיתיים יחוברו בהמשך למאגר Bari.
        </div>
      </HomeContainer>
    </section>
  );
}
