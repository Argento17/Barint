"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import AutoScroll from "embla-carousel-auto-scroll";
import useEmblaCarousel from "embla-carousel-react";
import { ChevronLeft, ChevronRight } from "lucide-react";

import { MicroComparisonSnapshotCard } from "@/components/home/micro-comparison-snapshot-card";
import { Button } from "@/components/ui/button";
import { getMicroComparisonSnapshots } from "@/lib/home/micro-comparison-snapshots";

import { HomeContainer } from "./section-frame";

function usePrefersReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(() => {
    if (typeof window === "undefined") return false;
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

export function HomeComparisons() {
  const prefersReducedMotion = usePrefersReducedMotion();
  const snapshots = useMemo(() => getMicroComparisonSnapshots(), []);
  const resumeTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const carouselItems = useMemo(
    () => [...snapshots, ...snapshots],
    [snapshots]
  );

  const autoScrollPlugins = useMemo(
    () =>
      prefersReducedMotion
        ? []
        : [
            AutoScroll({
              playOnInit: true,
              speed: 0.22,
              startDelay: 800,
              direction: "forward",
              stopOnInteraction: false,
              stopOnMouseEnter: true,
            }),
          ],
    [prefersReducedMotion]
  );

  const [emblaRef, emblaApi] = useEmblaCarousel(
    { align: "start", direction: "rtl", loop: true, skipSnaps: false },
    autoScrollPlugins
  );

  useEffect(() => {
    return () => {
      if (resumeTimeoutRef.current) clearTimeout(resumeTimeoutRef.current);
    };
  }, []);

  useEffect(() => {
    if (prefersReducedMotion || !emblaApi) return;
    emblaApi.reInit();
    emblaApi.plugins().autoScroll?.play(800);
  }, [emblaApi, prefersReducedMotion]);

  const stopAutoScroll = () => emblaApi?.plugins().autoScroll?.stop();

  const resumeAutoScroll = (delay = 1000) => {
    if (prefersReducedMotion) return;
    if (resumeTimeoutRef.current) clearTimeout(resumeTimeoutRef.current);
    resumeTimeoutRef.current = setTimeout(() => {
      emblaApi?.plugins().autoScroll?.play();
    }, delay);
  };

  const moveCarousel = (direction: "right" | "left") => {
    if (!emblaApi) return;
    stopAutoScroll();
    if (direction === "right") emblaApi.scrollPrev();
    else emblaApi.scrollNext();
    resumeAutoScroll(4500);
  };

  return (
    <section className="relative overflow-hidden bg-[#F7F7F2] py-14 md:py-20" id="comparisons">
      <HomeContainer>
        <div className="reveal-up mb-8 flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
          <div className="max-w-2xl space-y-3 text-right">
            <p className="text-sm font-bold text-[#1F8F6A]">השוואות ממוצרים אמיתיים</p>
            <h2 className="text-balance text-3xl font-extrabold tracking-[-0.045em] text-[#111318] md:text-4xl">
              השוואות ברורות בין מוצרים דומים
            </h2>
            <p className="text-pretty text-base leading-relaxed text-[#4E5663]">
              לא דמו — מוצרים מהמדף הישראלי, ציון Bari, חוזקות ופער מרכזי בכל כרטיס.
            </p>
          </div>
          <div className="flex shrink-0 flex-wrap items-center gap-3">
            <Button variant="ghost" className="gap-2 text-[#1F8F6A]" asChild>
              <Link href="/hashvaot/milk-comparison" className="font-semibold">
                השוואת החלב המלאה
                <ChevronLeft className="size-5" aria-hidden />
              </Link>
            </Button>
            <Button variant="ghost" className="gap-2 text-[#4E5663]" asChild>
              <Link href="/blog/milk-analysis" className="font-semibold">
                הניתוח בבלוג
              </Link>
            </Button>
          </div>
        </div>

        <div className="relative z-20 mb-4 flex items-center gap-2">
          <button
            type="button"
            onClick={() => moveCarousel("right")}
            className="inline-flex size-10 items-center justify-center rounded-full border border-black/[0.08] bg-[#FFFFFF] text-[#4E5663] shadow-sm transition hover:border-[#1F8F6A]/20"
            aria-label="הזזת הקרוסלה ימינה"
          >
            <ChevronRight className="size-5" aria-hidden />
          </button>
          <button
            type="button"
            onClick={() => moveCarousel("left")}
            className="inline-flex size-10 items-center justify-center rounded-full border border-[#1F8F6A]/20 bg-[#1F8F6A] text-[#F7F7F2] shadow-sm"
            aria-label="הזזת הקרוסלה שמאלה"
          >
            <ChevronLeft className="size-5" aria-hidden />
          </button>
        </div>
      </HomeContainer>

      <div className="relative">
        <div
          className="pointer-events-none absolute inset-y-0 start-0 z-10 w-20 bg-gradient-to-e from-[#F7F7F2] to-transparent md:w-32"
          aria-hidden
        />
        <div
          className="pointer-events-none absolute inset-y-0 end-0 z-10 w-20 bg-gradient-to-s from-[#F7F7F2] to-transparent md:w-32"
          aria-hidden
        />

        <div ref={emblaRef} className="overflow-hidden" dir="rtl">
          <div className="flex gap-4 px-5 sm:px-6">
            {carouselItems.map((snapshot, index) => (
              <div key={`${snapshot.id}-${index}`} className="flex flex-[0_0_auto]">
                <MicroComparisonSnapshotCard snapshot={snapshot} />
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
