# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(r"c:\Bari\bari-web\src")

# Fix radar label
radar = ROOT / "components/home/hero-decorative-radar.tsx"
t = radar.read_text(encoding="utf-8")
t = t.replace("\\u05e0\\u05d9\\u05ea\\u05d5\\u05d7 \\u05de\\u05d5\\u05e6\\u05e8", "\u05e0\u05d9\u05ea\u05d5\u05d7 \u05de\u05d5\u05e6\u05e8")
radar.write_text(t, encoding="utf-8")

(ROOT / "components/home/hero-still-life.tsx").write_text(r'''"use client";

import { useState } from "react";
import { CAROUSEL_PRODUCT_FALLBACK } from "@/lib/home/homepage-carousel-schema";
import { HERO_STILL_LIFE_PRODUCTS } from "@/lib/home/hero-still-life-products";
import { HeroDecorativeRadar } from "@/components/home/hero-decorative-radar";
import { HeroDecorativeScoreRing } from "@/components/home/hero-decorative-score-ring";

function FloatingPack({
  imageUrl,
  imageAlt,
  layout,
}: {
  imageUrl: string;
  imageAlt: string;
  layout: (typeof HERO_STILL_LIFE_PRODUCTS)[number]["layout"];
}) {
  const [loaded, setLoaded] = useState(false);
  const [errored, setErrored] = useState(false);
  const src = errored ? CAROUSEL_PRODUCT_FALLBACK : imageUrl;

  return (
    <div
      className="pointer-events-none absolute transition-transform duration-500"
      style={{
        top: layout.top,
        left: layout.left,
        width: layout.width,
        zIndex: layout.zIndex,
        transform: `rotate(${layout.rotate})`,
      }}
    >
      <div
        className="relative drop-shadow-[0_18px_28px_rgba(17,19,24,0.14)]"
        style={{ filter: loaded ? undefined : "blur(2px)" }}
      >
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={src}
          alt={imageAlt}
          className={`h-auto w-full object-contain mix-blend-multiply transition-opacity duration-500 ${
            loaded ? "opacity-100" : "opacity-0"
          }`}
          onLoad={() => setLoaded(true)}
          onError={() => {
            setErrored(true);
            setLoaded(true);
          }}
        />
      </div>
    </div>
  );
}

export function HeroStillLife() {
  return (
    <div
      className="relative mx-auto w-full max-w-[30rem] sm:max-w-[32rem]"
      aria-hidden
    >
      {/* Stage */}
      <div className="relative aspect-[4/5] min-h-[22rem] sm:min-h-[26rem]">
        {/* Soft pedestal */}
        <div
          className="absolute inset-x-[8%] bottom-[6%] h-[38%] rounded-[50%] bg-gradient-to-b from-[#EEF3EF]/80 to-[#E4EBE6]/40 blur-[1px]"
          style={{ zIndex: 0 }}
        />
        <div
          className="absolute inset-x-[12%] bottom-[8%] h-[32%] rounded-[50%] border border-[#1F8F6A]/10 bg-[radial-gradient(ellipse_at_center,rgba(255,255,255,0.9),rgba(247,247,242,0.2))] shadow-[inset_0_1px_0_rgba(255,255,255,0.8)]"
          style={{ zIndex: 0 }}
        />

        {HERO_STILL_LIFE_PRODUCTS.map((product) => (
          <FloatingPack
            key={product.id}
            imageUrl={product.imageUrl}
            imageAlt={product.imageAlt}
            layout={product.layout}
          />
        ))}

        {/* Score ring on Vitabix anchor */}
        <div
          className="absolute"
          style={{ top: "42%", left: "68%", zIndex: 10 }}
        >
          <HeroDecorativeScoreRing score={75} grade="B" />
        </div>

        {/* Mini radar card */}
        <HeroDecorativeRadar
          className="absolute end-0 top-2 z-20 sm:top-4"
        />

        {/* Quality chip */}
        <div
          className="absolute bottom-[14%] start-[6%] z-20 rounded-full border border-[#1F8F6A]/20 bg-white/90 px-3 py-1.5 text-[11px] font-bold text-[#167A58] shadow-[0_8px_24px_-12px_rgba(17,19,24,0.18)] backdrop-blur-sm"
        >
          \u05e2\u05d9\u05d1\u05d5\u05d3 \u05de\u05d9\u05e0\u05d9\u05de\u05dc\u05d9
        </div>
      </div>
    </div>
  );
}
''', encoding="utf-8")

# Fix Hebrew in still-life chip
still = ROOT / "components/home/hero-still-life.tsx"
st = still.read_text(encoding="utf-8")
st = st.replace("\\u05e2\\u05d9\\u05d1\\u05d5\\u05d3 \\u05de\\u05d9\\u05e0\\u05d9\\u05de\\u05dc\\u05d9", "\u05e2\u05d9\u05d1\u05d5\u05d3 \u05de\u05d9\u05e0\u05d9\u05de\u05dc\u05d9")
still.write_text(st, encoding="utf-8")

print("wrote hero-still-life")
