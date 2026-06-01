export const BARI_COMPARISON_TOKENS = {
  gradePalette: {
    A: { bg: "#E8F5EF", text: "#176F53", border: "#1F8F6A33" },
    B: { bg: "#E8F5EF", text: "#176F53", border: "#1F8F6A33" },
    C: { bg: "#FBF4DE", text: "#8F6600", border: "#C98A0033" },
    D: { bg: "#FDECE8", text: "#A63F2A", border: "#D1583D33" },
    E: { bg: "#F3E8E6", text: "#8B2E2E", border: "#B4231833" },
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
    rowImageSizeWeb: "64px",
    scoreChipSize: "22px",
    heroMaxHeight: "280px",
    heroImageHeight: "160px",
    webShellMaxWidth: "1600px",
  },
  /** Comparison Web Template v1 — desktop workspace (lg+ only). */
  webTable: {
    /** Fills viewport; caps at 1600px; mx-auto centers within the grey canvas padding. */
    shellMaxWidthClass: "lg:w-full lg:max-w-[1600px] lg:mx-auto",
    /** Modest horizontal inset on the grey canvas only. */
    shellViewportPaddingClass: "lg:px-8 xl:px-10 2xl:px-12",
    shellSurfaceClass:
      "lg:rounded-none lg:border-0 lg:bg-white lg:shadow-none",
    sectionPaddingClass: "lg:px-8 xl:px-10 2xl:px-12",
    tableInsetClass: "lg:px-8 xl:px-10 2xl:px-12",
    /** RTL: rank | image | product+insight | score */
    gridColsClass: "lg:grid-cols-[2.25rem_4.5rem_minmax(0,1fr)_5.25rem]",
    gridGapClass: "lg:gap-x-5",
    headerBgClass: "lg:bg-[#FAFAF8]",
  },
  insightLine: {
    fontSize: "13px",
    color: "#444444",
    lineHeight: "1.4",
    maxWords: 12,
  },
  methodology: {
    fontSize: "12px",
    color: "#AAAAAA",
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
      size: {
        sm: "min-w-[3.25rem] px-2 py-1.5",
        md: "min-w-[4rem] px-2.5 py-2",
        lg: "min-w-[4.5rem] px-3 py-2.5",
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
      labelClass: "mt-0.5 font-bold text-[#5E6672]",
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

/** Shared desktop table grid classes for header, rows, and expansion alignment. */
export function comparisonWebTableGridClass(): string {
  const { gridColsClass, gridGapClass } = BARI_COMPARISON_TOKENS.webTable;
  return `${gridColsClass} ${gridGapClass}`;
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
