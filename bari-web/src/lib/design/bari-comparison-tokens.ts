export const BARI_COMPARISON_TOKENS = {
  gradePalette: {
    A: { accent: "#1E7A4F", bg: "#E7F4EC", text: "#155C3C", border: "#1E7A4F33", dot: "top" },
    B: { accent: "#5F7D17", bg: "#F0F3DF", text: "#4C6314", border: "#5F7D1733", dot: "upper" },
    C: { accent: "#A87A0C", bg: "#FBF3D8", text: "#7E5800", border: "#A87A0C33", dot: "middle" },
    D: { accent: "#D85C1C", bg: "#FCEAD9", text: "#9A4012", border: "#D85C1C33", dot: "lower" },
    E: { accent: "#A52121", bg: "#F7E3E1", text: "#7A1A1A", border: "#A5212133", dot: "bottom" },
  },
  rows: {
    oddBg: "#FFFFFF",
    evenBg: "#F9F9F9",
    /** Tailwind classes for `<tr>` / motion rows where odd/even sibling index is reliable. */
    zebraRowClass: "odd:bg-[#FFFFFF] even:bg-[#F9F9F9]",
    zebraContainerClass: "bari-zebra-rows overflow-hidden",
    stripeOddClass: "bg-[#FFFFFF]",
    stripeEvenClass: "bg-[#F9F9F9]",
  },
  typography: {
    sectionEyebrow: "font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/80",
    sectionTitle: "mt-2 text-2xl font-extrabold tracking-[-0.04em] md:text-3xl",
    sectionMeta: "mt-2 max-w-xl text-sm leading-relaxed text-[#4E5663]",
  },
  layout: {
    rowHeightMobile: "72px",
    rowHeightMobileMax: "80px",
    rowImageSize: "56px",
    scoreChipSize: "22px",
    heroMaxHeight: "280px",
    heroImageHeight: "160px",
  },
  /** Horizontal section inset shared by the `wide` category chrome (hero/prologue/lenses/methodology). */
  webTable: {
    sectionPaddingClass: "lg:px-8 xl:px-10 2xl:px-12",
  },
  insightLine: {
    fontSize: "13px",
    color: "#444444",
    lineHeight: "1.4",
    maxWords: 12,
  },
  methodology: {
    fontSize: "12px",
    color: "#666C67",
    maxSentences: 4,
  },
  score: {
    hero: {
      container: "text-right",
      scoreSize: {
        sm: "text-4xl",
        md: "text-5xl",
        lg: "text-6xl",
      },
      labelSize: {
        sm: "text-sm",
        md: "text-base",
        lg: "text-lg",
      },
      scoreClass: "font-extrabold tabular-nums leading-none tracking-[-0.04em]",
      labelClass: "mt-1 font-bold",
    },
    rowChip: {
      container:
        "inline-flex flex-col items-center justify-center rounded-xl border text-center",
      // Fixed widths (not min-width) so every grade chip is identical regardless
      // of the tier word's length (טוב=3 chars vs בינוני=6). Sized to fit the
      // longest label without wrapping; paired with whitespace-nowrap on the label.
      size: {
        sm: "w-[4.25rem] px-2 py-1.5",
        md: "w-[5rem] px-2.5 py-2",
        lg: "w-[5.5rem] px-3 py-2.5",
      },
      scoreSize: {
        sm: "text-base",
        md: "text-lg",
        lg: "text-xl",
      },
      labelSize: {
        sm: "text-[0.6rem]",
        md: "text-[0.65rem]",
        lg: "text-xs",
      },
      scoreClass: "font-extrabold tabular-nums leading-none text-[#111318]",
      labelClass: "mt-0.5 whitespace-nowrap font-bold text-[#5E6672]",
      backgroundColor: "#F7F7F2",
      borderColor: "rgba(17,19,24,0.10)",
    },
    comparisonChip: {
      container:
        "inline-flex flex-col items-center justify-center rounded-xl border text-center",
      size: "min-w-[5.5rem] px-4 py-3",
      gradeClass: "font-extrabold leading-none text-[2rem] md:text-[2.25rem]",
      scoreClass: "mt-1 font-bold tabular-nums leading-none text-lg opacity-90",
    },
  },
} as const;

/** Maps a grade's `dot` keyword to its vertical position (% from top) along the accent bar. */
const GRADE_DOT_POSITION = {
  top: "10%",
  upper: "30%",
  middle: "50%",
  lower: "70%",
  bottom: "90%",
} as const;

export type GradeDotPosition = keyof typeof GRADE_DOT_POSITION;

/** Returns the vertical offset (e.g. "10%") for a grade's colorblind-safe position dot. */
export function gradeDotOffset(dot: GradeDotPosition): string {
  return GRADE_DOT_POSITION[dot];
}

/** Horizontal padding for hero, prologue, lenses, methodology in web layout. */
export function comparisonWebSectionPaddingClass(): string {
  return BARI_COMPARISON_TOKENS.webTable.sectionPaddingClass;
}

/** Rank 1 = white, 2 = grey — stable when a non-row node (e.g. table header) precedes products. */
export function comparisonRowStripeClass(rank: number): string {
  return rank % 2 === 1
    ? BARI_COMPARISON_TOKENS.rows.stripeOddClass
    : BARI_COMPARISON_TOKENS.rows.stripeEvenClass;
}

export function warnComparisonImplementationDeviation(
  component: string,
  reason: string
) {
  if (process.env.NODE_ENV !== "production") {
    console.warn(
      `[Bari Comparison Token Warning] ${component}: ${reason}. Use shared comparison tokens only.`
    );
  }
}
