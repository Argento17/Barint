"use client";

import Image from "next/image";
import Link from "next/link";
import { Search } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";

import { Button } from "@/components/ui/button";
import { HERO_COPY } from "@/lib/home/hero-copy";

// ── Motion variants ──────────────────────────────────────────────────────────
const EASE: [number, number, number, number] = [0.22, 1, 0.36, 1];

function makeReveal(delay: number) {
  return {
    hidden: { opacity: 0, y: 16 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.76, delay, ease: EASE },
    },
  };
}

const photoVariant = {
  hidden: { opacity: 0, y: 22 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 1.0, delay: 0.2, ease: EASE },
  },
};

// ── Edge-dissolve mask (feather right ~11%, top ~14%, bottom ~11%; left bleeds) ──
const MASK_STYLE = {
  WebkitMaskImage: [
    "linear-gradient(to right, #000 89%, transparent 100%)",
    "linear-gradient(to bottom, transparent 0%, #000 14%, #000 89%, transparent 100%)",
  ].join(", "),
  WebkitMaskComposite: "source-in" as const,
  maskImage: [
    "linear-gradient(to right, #000 89%, transparent 100%)",
    "linear-gradient(to bottom, transparent 0%, #000 14%, #000 89%, transparent 100%)",
  ].join(", "),
  maskComposite: "intersect" as const,
};

// ── Component ────────────────────────────────────────────────────────────────
export function HomeHero() {
  const reduceMotion = useReducedMotion();

  // When reduced-motion is preferred, render all elements visible immediately.
  const initial = reduceMotion ? "visible" : "hidden";
  const animate = "visible";

  return (
    <section
      aria-label="hero"
      style={{
        background: "var(--canvas, #F7F7F2)",
        // The global SiteHeader is sticky at ~64px; hero fills remaining viewport.
        minHeight: "calc(100vh - var(--site-header-height, 4rem))",
        display: "grid",
        // RTL: col 1 (right in RTL) = headline, col 2 (left in RTL) = photo
        gridTemplateColumns: "0.92fr 1.12fr",
        alignItems: "center",
        gap: "clamp(16px, 2vw, 44px)",
        paddingBlock: "clamp(32px, 5vh, 64px)",
        overflow: "hidden",
      }}
      className="hero-handoff"
    >
      {/* ── Headline column (col 1 = right side in RTL) ────────────────── */}
      <div
        style={{
          paddingInline: "clamp(28px, 4.5vw, 80px) clamp(16px, 2vw, 40px)",
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
        }}
      >
        {/* H1 */}
        <motion.h1
          variants={makeReveal(0.08)}
          initial={initial}
          animate={animate}
          style={{
            fontFamily: "var(--font-heading, var(--font-sans))",
            fontWeight: 800,
            fontSize: "clamp(1.9rem, 3.25vw, 3.4rem)",
            lineHeight: 1.16,
            letterSpacing: "-0.045em",
            color: "var(--fg1, #111318)",
            margin: 0,
            textWrap: "balance",
          } as React.CSSProperties}
        >
          {/* Line 1: "אתם יודעים [באמת] מה יש במוצרים שאתם צורכים?" */}
          <span style={{ display: "block" }}>
            {HERO_COPY.headline1Part1}{" "}
            <span style={{ color: "var(--bari-green, #1F8F6A)" }}>
              {HERO_COPY.headline1Green}
            </span>{" "}
            {HERO_COPY.headline1Part2}
          </span>
          {/* Line 2: entire line in green */}
          <span
            style={{
              display: "block",
              color: "var(--bari-green, #1F8F6A)",
            }}
          >
            {HERO_COPY.headline2}
          </span>
        </motion.h1>

        {/* Lead */}
        <motion.p
          variants={makeReveal(0.18)}
          initial={initial}
          animate={animate}
          style={{
            fontFamily: "var(--font-sans)",
            fontWeight: 400,
            fontSize: "clamp(1.05rem, 1.25vw, 1.25rem)",
            lineHeight: 1.7,
            color: "var(--fg2, #4E5663)",
            maxWidth: "27em",
            marginTop: "24px",
            marginBottom: 0,
            textWrap: "pretty",
          } as React.CSSProperties}
        >
          {HERO_COPY.subline}
        </motion.p>

        {/* Primary CTA */}
        <motion.div
          variants={makeReveal(0.28)}
          initial={initial}
          animate={animate}
          style={{ marginTop: "30px" }}
          className="hero-cta-wrapper"
        >
          <Button
            asChild
            style={{
              display: "inline-flex",
              alignItems: "center",
              justifyContent: "center",
              gap: "11px",
              minWidth: "300px",
              background: "var(--bari-green, #1F8F6A)",
              color: "#fff",
              borderRadius: "14px",
              padding: "18px 32px",
              fontSize: "19px",
              fontWeight: 700,
              boxShadow: "var(--shadow-cta, inset 0 1px 0 rgba(255,255,255,0.20), 0 14px 40px -16px rgba(31,143,106,0.58))",
              border: "none",
              height: "auto",
              // Hover via CSS class below (framer-motion whileHover disabled when reduced-motion)
            }}
            className={
              reduceMotion
                ? "hero-cta-btn"
                : "hero-cta-btn hero-cta-btn--motion"
            }
          >
            <Link href="/hashvaot">
              <Search
                size={20}
                strokeWidth={2.2}
                aria-hidden="true"
              />
              {HERO_COPY.primaryCta}
            </Link>
          </Button>
        </motion.div>

        {/* Secondary coming-soon */}
        <motion.span
          variants={makeReveal(0.36)}
          initial={initial}
          animate={animate}
          aria-label="סריקת ברקוד — בקרוב"
          role="note"
          style={{
            display: "inline-block",
            marginTop: "18px",
            fontSize: "14px",
            fontWeight: 600,
            color: "var(--fg3, #5E6560)",
            borderBottom: "1px solid var(--green-ring, rgba(31,143,106,0.25))",
            paddingBottom: "2px",
            whiteSpace: "nowrap",
            cursor: "default",
            userSelect: "none",
          }}
        >
          {HERO_COPY.secondaryCta}
        </motion.span>
      </div>

      {/* ── Photo column (col 2 = left side in RTL, bleeds off left edge) ── */}
      <div style={{ position: "relative", alignSelf: "center" }}>
        <motion.div
          variants={photoVariant}
          initial={initial}
          animate={animate}
          style={{
            width: "100%",
            maxWidth: "780px",
            marginInlineStart: "auto",
            lineHeight: 0,
          }}
        >
          {/*
           * next/image with explicit intrinsic dimensions (780×560, matching the
           * handoff's max-width). CSS width:100%/height:auto scales it responsively.
           * The `sizes` hint ensures the optimizer picks the right breakpoint source.
           * The edge-dissolve mask is applied via MASK_STYLE; no border, no bg box.
           *
           * PERF NOTE: hero-products.png is ~2.2MB. next/image serves it optimised
           * (WebP/AVIF) at the requested breakpoints. If LCP is a concern on low-end
           * mobile, a pre-exported WebP at ≤800px wide would remove the server-side
           * conversion overhead and shave ~400-600KB. Flag to owner as an asset task.
           */}
          <Image
            src="/home/hero-products.png"
            alt="מבחר מוצרי מזון — שיבולת שועל, שמן זית, יוגורט ועוד"
            width={780}
            height={560}
            priority
            sizes="(max-width: 768px) 100vw, 52vw"
            style={{
              width: "100%",
              height: "auto",
              display: "block",
              maxWidth: "780px",
              ...MASK_STYLE,
            }}
          />
        </motion.div>
      </div>

      {/* ── Responsive + hover styles ────────────────────────────────────── */}
      <style>{`
        /* Mobile: single column, photo above headline */
        @media (max-width: 768px) {
          .hero-handoff {
            grid-template-columns: 1fr !important;
            grid-template-rows: auto auto;
            min-height: auto !important;
            padding-block: clamp(24px, 4vh, 48px) !important;
          }
          /* On mobile, photo is col 1 (renders first in source) → shows above headline */
          /* Headline col padding becomes symmetric */
          .hero-handoff > div:first-child {
            padding-inline: clamp(20px, 5vw, 40px) !important;
            align-items: stretch;
          }
          /* CTA full-width on mobile */
          .hero-cta-wrapper {
            width: 100%;
          }
          .hero-cta-btn {
            width: 100% !important;
            min-width: 0 !important;
          }
          /* Photo: drop left-bleed on mobile, center it */
          .hero-handoff > div:last-child {
            display: flex;
            justify-content: center;
            overflow: hidden;
          }
          .hero-handoff > div:last-child > div {
            margin-inline-start: 0 !important;
            max-width: 100% !important;
          }
        }

        /* CTA hover — only when motion is not reduced */
        .hero-cta-btn--motion {
          transition: transform 500ms cubic-bezier(0.22, 1, 0.36, 1),
                      box-shadow 500ms cubic-bezier(0.22, 1, 0.36, 1);
        }
        .hero-cta-btn--motion:hover {
          transform: translateY(-1px);
          box-shadow: inset 0 1px 0 rgba(255,255,255,0.20),
                      0 18px 50px -16px rgba(31,143,106,0.66) !important;
        }
      `}</style>
    </section>
  );
}
