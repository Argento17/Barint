"use client";

import { useId } from "react";
import { Noto_Sans_Hebrew } from "next/font/google";
import {
  BarChart3,
  Beaker,
  Beef,
  Candy,
  Droplets,
  Flame,
  GitCompareArrows,
  Gauge,
  Package,
  Scale,
  ShieldCheck,
  Sparkles,
  Wheat,
  X,
  type LucideIcon,
} from "lucide-react";

import { BariBrandLogo } from "@/components/brand/bari-brand-logo";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { cn } from "@/lib/utils";

const hebrew = Noto_Sans_Hebrew({
  subsets: ["hebrew"],
  weight: ["400", "500", "600", "700"],
  display: "swap",
});

const nutrition = [
  {
    label: "אנרגיה",
    value: "412",
    unit: "קק״ל",
    per: "ל־100 גרם",
    icon: Flame,
    accent: "amber" as const,
  },
  {
    label: "חלבון",
    value: "8.2",
    unit: "גרם",
    per: "ל־100 גרם",
    icon: Beef,
    accent: "emerald" as const,
  },
  {
    label: "פחמימות",
    value: "54",
    unit: "גרם",
    per: "ל־100 גרם",
    icon: Wheat,
    accent: "emerald" as const,
  },
  {
    label: "מתוכם סוכרים",
    value: "12",
    unit: "גרם",
    per: "ל־100 גרם",
    icon: Candy,
    accent: "amber" as const,
  },
  {
    label: "שומן",
    value: "18",
    unit: "גרם",
    per: "ל־100 גרם",
    icon: Droplets,
    accent: "sage" as const,
  },
  {
    label: "נתרן",
    value: "0.38",
    unit: "גרם",
    per: "ל־100 גרם",
    icon: Gauge,
    accent: "rose" as const,
  },
] as const;

const ingredients = [
  {
    name: "קמח חיטה מלא",
    pct: "34",
    role: "בסיס",
    note: "מקור סיבים",
    signal: "green" as const,
    signalLabel: "מנוף חיובי",
  },
  {
    name: "סוכר",
    pct: "14",
    role: "מתיקה",
    note: "מזוהה בתווית",
    signal: "yellow" as const,
    signalLabel: "לתשומת לב",
  },
  {
    name: "שמן קנולה",
    pct: "11",
    role: "שומן",
    note: "רב־בלתי רווי",
    signal: "yellow" as const,
    signalLabel: "לתשומת לב",
  },
  {
    name: "אבקת חלב מיובש",
    pct: "6",
    role: "חלבון",
    note: "אלרגן: חלב",
    signal: "yellow" as const,
    signalLabel: "אלרגן",
  },
  {
    name: "מלח",
    pct: "0.9",
    role: "תיבול",
    note: "תרומה לנתרן",
    signal: "red" as const,
    signalLabel: "נתרן",
  },
] as const;

const comparisonRows = [
  {
    name: "מוצר הדגמה (Bari)",
    score: "82",
    kcal: "412",
    protein: "8.2",
    sodium: "0.38",
    highlight: true,
  },
  {
    name: "ממוצע קטגוריה",
    score: "71",
    kcal: "438",
    protein: "6.1",
    sodium: "0.42",
    highlight: false,
  },
  {
    name: "חלופה דומה #1",
    score: "76",
    kcal: "401",
    protein: "7.4",
    sodium: "0.35",
    highlight: false,
  },
] as const;

const SCORE = 82;
const RING_R = 54;
const RING_C = 2 * Math.PI * RING_R;

const nutritionAccent: Record<
  (typeof nutrition)[number]["accent"],
  { stroke: string; glow: string; icon: string }
> = {
  amber: {
    stroke: "text-[#1F8F6A]",
    glow: "shadow-slate-900/20",
    icon: "bg-[#1F8F6A]/10 text-[#1F8F6A] ring-black/[0.08]",
  },
  emerald: {
    stroke: "text-[#2FAE82]",
    glow: "shadow-slate-900/20",
    icon: "bg-[#2FAE82]/10 text-[#1F8F6A] ring-black/[0.08]",
  },
  sage: {
    stroke: "text-[#1F8F6A]",
    glow: "shadow-slate-900/10",
    icon: "bg-[#1F8F6A]/10 text-[#1F8F6A] ring-black/[0.08]",
  },
  rose: {
    stroke: "text-[#1F8F6A]",
    glow: "shadow-slate-900/20",
    icon: "bg-[#1F8F6A]/10 text-[#1F8F6A] ring-black/[0.08]",
  },
};

const signalStyles = {
  green: {
    dot: "bg-[#2FAE82]",
    glow: "shadow-[0_0_20px_rgba(47,174,130,0.06)]",
    chip: "bg-[#2FAE82]/10 text-[#1F8F6A] ring-black/[0.08]",
  },
  yellow: {
    dot: "bg-[#1F8F6A]",
    glow: "shadow-[0_0_20px_rgba(47,174,130,0.06)]",
    chip: "bg-[#1F8F6A]/10 text-[#1F8F6A] ring-black/[0.08]",
  },
  red: {
    dot: "bg-[#1F8F6A]",
    glow: "shadow-[0_0_20px_rgba(47,174,130,0.06)]",
    chip: "bg-[#1F8F6A]/10 text-[#1F8F6A] ring-black/[0.08]",
  },
};

function MeshBackdrop() {
  return (
    <>
      <div
        className="pointer-events-none fixed inset-0 -z-20 bg-[#F7F7F2]"
        aria-hidden
      />
      <div
        className="pointer-events-none fixed inset-0 -z-10 opacity-0"
        aria-hidden
        style={{
          background: "transparent",
        }}
      />
      <div
        className="pointer-events-none fixed inset-0 -z-10 bg-transparent"
        aria-hidden
      />
    </>
  );
}

function ScoreRing({ className }: { className?: string }) {
  const uid = useId().replace(/:/g, "");
  const gid = `bari-ring-${uid}`;
  const offset = RING_C - (SCORE / 100) * RING_C;

  return (
    <div
      className={cn(
        "relative isolate flex flex-col items-center justify-center",
        className
      )}
    >
      <div
        className="absolute inset-0 -z-10 rounded-full bg-[#2FAE82]/[0.025] blur-3xl"
        aria-hidden
      />
      <div
        className="absolute inset-2 -z-10 rounded-full bg-gradient-to-br from-[#FFFFFF]/80 via-[#FFFFFF]/40 to-transparent opacity-90"
        aria-hidden
      />
      <div className="relative rounded-full p-1 shadow-[0_1px_0_rgba(255,255,255,0.08)_inset,0_24px_48px_-28px_rgba(47,174,130,0.06)] ring-1 ring-black/[0.08]">
        <svg
          className="size-[9.5rem] -rotate-90 sm:size-[10.5rem]"
          viewBox="0 0 124 124"
          aria-hidden
        >
          <defs>
            <linearGradient id={gid} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#1F8F6A" />
              <stop offset="55%" stopColor="#2FAE82" />
              <stop offset="100%" stopColor="#2FAE82" />
            </linearGradient>
          </defs>
          <circle
            cx="62"
            cy="62"
            r={RING_R}
            className="text-[#1F8F6A]/60"
            stroke="currentColor"
            strokeWidth="8"
            fill="none"
          />
          <circle
            cx="62"
            cy="62"
            r={RING_R}
            stroke={`url(#${gid})`}
            strokeWidth="8"
            fill="none"
            strokeLinecap="round"
            strokeDasharray={RING_C}
            strokeDashoffset={offset}
            className="drop-shadow-[0_0_12px_rgba(47,174,130,0.06)] transition-[stroke-dashoffset] duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-[10px] font-semibold uppercase tracking-[0.2em] text-[#2FAE82]/70">
            Bari
          </span>
          <span className="mt-0.5 text-4xl font-semibold tabular-nums tracking-tight text-[#111318] sm:text-5xl">
            {SCORE}
          </span>
          <span className="mt-1 text-xs font-medium text-[#4E5663]">מתוך 100</span>
        </div>
      </div>
    </div>
  );
}

function SectionLabel({
  icon: Icon,
  title,
  subtitle,
  className,
}: {
  icon: LucideIcon;
  title: string;
  subtitle?: string;
  className?: string;
}) {
  return (
    <div
      className={cn("mb-10 flex flex-col gap-2 sm:mb-12", className)}
    >
      <div className="flex items-center gap-4">
        <span className="flex size-12 items-center justify-center rounded-2xl bg-[#FFFFFF]/70 text-[#2FAE82] shadow-[0_12px_32px_-16px_rgba(47,174,130,0.06)] ring-1 ring-black/[0.08] backdrop-blur-md transition duration-500 ease-out hover:scale-[1.03] hover:shadow-[0_16px_40px_-12px_rgba(47,174,130,0.06)]">
          <Icon className="size-5" strokeWidth={1.65} />
        </span>
        <div>
          <h2 className="text-2xl font-semibold tracking-tight text-[#111318] md:text-[1.65rem]">
            {title}
          </h2>
          {subtitle ? (
            <p className="mt-1 max-w-xl text-sm leading-relaxed text-[#4E5663] md:text-[0.9375rem]">
              {subtitle}
            </p>
          ) : null}
        </div>
      </div>
      <div className="ms-16 h-px max-w-md bg-gradient-to-l from-transparent via-[#1F8F6A]/12 to-transparent" />
    </div>
  );
}

export default function ProductPage() {
  return (
    <div
      className={cn(
        hebrew.className,
        "bari-product-demo relative min-h-screen overflow-x-hidden text-[#111318] antialiased",
        "selection:bg-[#2FAE82]/20 selection:text-[#1F8F6A]"
      )}
    >
      <MeshBackdrop />

      <main
        dir="rtl"
        lang="he"
        className="relative mx-auto max-w-6xl px-5 pb-24 pt-14 sm:px-8 sm:pb-28 sm:pt-16 md:px-10 md:pt-20"
      >
        {/* —— Hero —— */}
        <section className="relative overflow-hidden rounded-[2rem] border border-black/[0.08] bg-[#FFFFFF]/60 p-8 shadow-[0_32px_64px_-28px_rgba(17,19,24,0.58),0_0_0_1px_rgba(255,255,255,0.04)_inset] backdrop-blur-2xl backdrop-saturate-150 sm:p-10 md:rounded-[2.25rem] md:p-12 lg:p-14">
          <div
            className="pointer-events-none absolute -start-24 -top-24 size-72 rounded-full bg-[#1F8F6A]/[0.025] blur-3xl"
            aria-hidden
          />
          <div
            className="pointer-events-none absolute -bottom-20 -end-16 size-80 rounded-full bg-[#1F8F6A]/[0.02] blur-3xl"
            aria-hidden
          />

          <div className="relative grid gap-12 lg:grid-cols-[minmax(0,1.15fr)_minmax(240px,0.85fr)] lg:items-center lg:gap-16">
            <div className="flex min-w-0 flex-col gap-8">
              <div className="flex flex-wrap items-center gap-2">
                <Badge className="h-7 rounded-full border-0 bg-[#1F8F6A] px-3 text-[11px] font-semibold text-[#F7F7F2] shadow-lg shadow-slate-900/25 transition duration-300 hover:bg-[#1F8F6A] hover:shadow-slate-900/35">
                  חטיף · קטגוריה
                </Badge>
                <Badge
                  variant="outline"
                  className="h-7 rounded-full border-black/[0.08] bg-[#FFFFFF]/60 px-3 text-[11px] font-medium text-[#4E5663] shadow-sm backdrop-blur-sm"
                >
                  מאומת תווית
                </Badge>
                <span className="rounded-full bg-[#F7F7F2]/50 px-3 py-1 font-mono text-[11px] tabular-nums text-[#7A817C]">
                  GTIN 7290001234567
                </span>
              </div>

              <div className="space-y-4">
                <p className="text-[11px] font-semibold tracking-[0.18em] text-[#2FAE82]/80">
                  BARI · מודיעין מזון
                </p>
                <h1 className="text-balance text-[2rem] font-semibold leading-[1.08] tracking-tight text-[#111318] sm:text-[2.35rem] md:text-[2.65rem]">
                  מוצר הדגמה
                </h1>
                <p className="max-w-xl text-base leading-relaxed text-[#4E5663] md:text-[1.05rem]">
                  תצוגת נתונים מבוססת תווית ומקורות רשמיים. הציון משקלל רכיבים,
                  פרופיל תזונתי ושקיפות מידע — ללא המלצות רפואיות.
                </p>
              </div>

              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-4">
                <Sheet>
                  <SheetTrigger asChild>
                    <Button
                      size="lg"
                      className="group h-12 rounded-2xl bg-[#1F8F6A] px-8 text-sm font-semibold text-[#F7F7F2] shadow-[0_16px_40px_-12px_rgba(47,174,130,0.06)] transition-all duration-500 ease-out hover:-translate-y-0.5 hover:bg-[#1F8F6A] hover:shadow-[0_22px_48px_-10px_rgba(47,174,130,0.06)] active:translate-y-0"
                    >
                      <GitCompareArrows className="size-4 transition-transform duration-500 group-hover:-rotate-6" />
                      השוואת מוצרים
                    </Button>
                  </SheetTrigger>
                  <SheetContent
                    side="right"
                    showCloseButton={false}
                    className="flex w-full flex-col gap-0 border-black/[0.08] bg-[#FFFFFF]/92 p-0 shadow-2xl shadow-slate-900/10 backdrop-blur-2xl sm:max-w-md"
                  >
                    <div className="relative px-6 pb-6 pt-16 sm:px-8">
                      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_80%_0%,rgba(47,174,130,0.04),transparent_42%)]" />
                      <SheetClose asChild>
                        <Button
                          variant="ghost"
                          size="icon-sm"
                          className="absolute top-5 right-5 rounded-xl text-[#7A817C] transition-colors hover:bg-[#FFFFFF]/78 hover:text-[#111318]"
                          aria-label="סגור"
                        >
                          <X className="size-4" />
                        </Button>
                      </SheetClose>
                      <SheetHeader className="relative space-y-2 p-0 text-right">
                        <SheetTitle className="text-xl font-semibold text-[#111318]">
                          השוואת מוצרים
                        </SheetTitle>
                        <SheetDescription className="text-sm text-[#4E5663]">
                          נתונים ל־100 גרם · ציון Bari לפי מודל המערכת
                        </SheetDescription>
                      </SheetHeader>
                    </div>

                    <div className="relative flex-1 overflow-auto px-6 py-2 sm:px-8">
                      <div className="overflow-hidden rounded-2xl bg-[#FFFFFF]/68 shadow-[0_1px_0_rgba(255,255,255,0.05)_inset,0_12px_40px_-24px_rgba(17,19,24,0.5)] ring-1 ring-black/[0.08] backdrop-blur-sm">
                        <table className="w-full min-w-[300px] text-right text-sm">
                          <thead>
                            <tr className="text-xs font-semibold text-[#4E5663]">
                              <th className="px-4 py-3.5 font-medium">מוצר</th>
                              <th className="px-4 py-3.5 font-medium">ציון</th>
                              <th className="px-4 py-3.5 font-medium">קק״ל</th>
                              <th className="px-4 py-3.5 font-medium">חלבון</th>
                              <th className="px-4 py-3.5 font-medium">נתרן</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-white/[0.08]">
                            {comparisonRows.map((row) => (
                              <tr
                                key={row.name}
                                className={cn(
                                  "transition-colors duration-300 hover:bg-[#1F8F6A]/[0.04]",
                                  row.highlight &&
                                    "bg-gradient-to-l from-[#2FAE82]/[0.04] to-transparent"
                                )}
                              >
                                <td className="px-4 py-3.5 font-medium text-[#111318]">
                                  {row.name}
                                </td>
                                <td className="px-4 py-3.5 tabular-nums font-semibold text-[#2FAE82]">
                                  {row.score}
                                </td>
                                <td className="px-4 py-3.5 tabular-nums text-[#4E5663]">
                                  {row.kcal}
                                </td>
                                <td className="px-4 py-3.5 tabular-nums text-[#4E5663]">
                                  {row.protein}
                                </td>
                                <td className="px-4 py-3.5 tabular-nums text-[#4E5663]">
                                  {row.sodium}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>

                    <SheetFooter className="border-t border-black/[0.08] bg-[#F7F7F2]/30 px-6 py-5 backdrop-blur-md sm:px-8">
                      <p className="text-xs leading-relaxed text-[#7A817C]">
                        ההשוואה מבוססת על ערכים שדווחו לרשות המזון או על תווית
                        היצרן. ייתכנו פערים בין אצווה לאצווה.
                      </p>
                    </SheetFooter>
                  </SheetContent>
                </Sheet>

                <Button
                  variant="ghost"
                  size="lg"
                  className="h-12 rounded-2xl text-[#7A817C] transition-all duration-300 hover:bg-[#FFFFFF]/68 hover:text-[#111318]"
                  disabled
                >
                  <Package className="size-4 opacity-70" />
                  ייצוא נתונים
                </Button>
              </div>
            </div>

            <div className="relative mx-auto w-full max-w-[280px] lg:mx-0 lg:max-w-none">
              <div className="aspect-[4/5] overflow-hidden rounded-[1.75rem] bg-gradient-to-br from-[#F7F7F2] via-[#FFFFFF]/60 to-[#1F8F6A]/[0.04] shadow-[0_28px_56px_-24px_rgba(47,174,130,0.06)] ring-1 ring-black/[0.08] transition duration-700 ease-out hover:-translate-y-1 hover:shadow-[0_36px_64px_-20px_rgba(47,174,130,0.06)]">
                <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_30%_20%,rgba(255,255,255,0.08),transparent_50%),radial-gradient(ellipse_at_80%_80%,rgba(47,174,130,0.06),transparent_55%)]" />
                <div className="relative flex h-full flex-col items-center justify-center gap-5 p-8">
                  <div className="flex size-20 items-center justify-center rounded-3xl bg-[#FFFFFF]/82 text-[#2FAE82] shadow-[0_20px_40px_-16px_rgba(47,174,130,0.06)] ring-1 ring-black/[0.08] backdrop-blur-md transition duration-500 hover:rotate-6 hover:scale-105">
                    <Sparkles className="size-10" strokeWidth={1.15} />
                  </div>
                  <div className="text-center">
                    <p className="text-sm font-medium text-[#4E5663]">תצוגת מוצר</p>
                    <p className="mt-1 text-xs text-[#7A817C]">ממתין לנכס ויזואלי</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* —— Bento: score + compliance —— */}
        <section className="mt-16 grid gap-6 md:mt-20 md:gap-8 lg:grid-cols-12">
          <Card className="group relative overflow-hidden border-0 bg-[#FFFFFF]/60 shadow-[0_28px_56px_-32px_rgba(17,19,24,0.58)] ring-1 ring-black/[0.08] backdrop-blur-xl transition duration-500 ease-out hover:-translate-y-1 hover:shadow-[0_36px_64px_-28px_rgba(17,19,24,0.62)] lg:col-span-8 lg:rounded-[2rem]">
            <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_80%_0%,rgba(47,174,130,0.04),transparent_42%)] opacity-80 transition duration-700 group-hover:opacity-100" />
            <CardHeader className="relative flex flex-col gap-10 border-0 pb-2 pt-10 sm:flex-row sm:items-center sm:justify-between sm:px-10 sm:pt-12">
              <div className="max-w-md space-y-4 text-center sm:text-right">
                <div className="flex flex-wrap justify-center gap-2 sm:justify-end">
                  <span className="inline-flex items-center gap-1.5 rounded-full bg-[#1F8F6A]/10 px-3 py-1 text-[11px] font-semibold text-[#1F8F6A] ring-1 ring-black/[0.08]">
                    <span className="size-1.5 rounded-full bg-[#1F8F6A] shadow-[0_0_10px_rgba(47,174,130,0.06)]" />
                    מודל פעיל
                  </span>
                  <span className="inline-flex items-center gap-1.5 rounded-full bg-[#2FAE82]/10 px-3 py-1 text-[11px] font-semibold text-[#1F8F6A] ring-1 ring-black/[0.08]">
                    <span className="size-1.5 rounded-full bg-[#2FAE82] shadow-[0_0_10px_rgba(47,174,130,0.06)]" />
                    נתונים סטטיים
                  </span>
                </div>
                <div>
                  <CardDescription className="text-xs font-semibold tracking-wide text-[#4E5663]">
                    ציון Bari
                  </CardDescription>
                  <CardTitle className="mt-2 text-2xl font-semibold leading-tight text-[#111318] md:text-3xl">
                    פרופיל תזונתי־רכיבי
                  </CardTitle>
                  <p className="mt-3 text-sm leading-relaxed text-[#4E5663]">
                    משקלל רכיבים, תזונה ושקיפות מתוך התווית והמאגר הפנימי.
                  </p>
                </div>
              </div>
              <ScoreRing className="shrink-0 scale-95 sm:scale-100" />
            </CardHeader>
            <CardContent className="relative grid gap-4 px-6 pb-10 pt-4 sm:grid-cols-3 sm:gap-5 sm:px-10">
              {[
                {
                  label: "רמת ביטחון במודל",
                  value: "גבוהה",
                  sub: "92% הצלבה",
                },
                {
                  label: "עדכון אחרון",
                  value: "2026-05-02",
                  sub: "מקור: תווית",
                },
                {
                  label: "כיסוי רכיבים",
                  value: "94%",
                  sub: "כולל תוספים מזוהים",
                },
              ].map((m) => (
                <div
                  key={m.label}
                  className="rounded-2xl bg-[#FFFFFF]/60 px-5 py-5 shadow-[0_1px_0_rgba(255,255,255,0.05)_inset] ring-1 ring-black/[0.08] transition duration-500 ease-out hover:bg-[#FFFFFF]/78 hover:shadow-lg hover:shadow-slate-900/10"
                >
                  <p className="text-[11px] font-semibold text-[#4E5663]">
                    {m.label}
                  </p>
                  <p className="mt-2 text-lg font-semibold tabular-nums text-[#111318]">
                    {m.value}
                  </p>
                  <p className="mt-1 text-xs text-[#7A817C]">{m.sub}</p>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card className="group flex flex-col border-0 bg-[#FFFFFF]/58 shadow-[0_24px_48px_-28px_rgba(17,19,24,0.58)] ring-1 ring-black/[0.08] backdrop-blur-xl transition duration-500 ease-out hover:-translate-y-1 hover:shadow-[0_32px_56px_-24px_rgba(17,19,24,0.62)] lg:col-span-4 lg:rounded-[2rem]">
            <CardHeader className="border-0 pb-2 pt-8 sm:px-8 sm:pt-10">
              <div className="flex items-start gap-4">
                <span className="flex size-11 shrink-0 items-center justify-center rounded-2xl bg-[#2FAE82]/10 text-[#1F8F6A] ring-1 ring-black/[0.08] shadow-inner shadow-slate-900/20">
                  <ShieldCheck className="size-5" strokeWidth={1.6} />
                </span>
                <div>
                  <CardTitle className="text-lg font-semibold text-[#111318]">
                    רגולציה ותווית
                  </CardTitle>
                  <CardDescription className="mt-2 text-sm leading-relaxed text-[#4E5663]">
                    נקודות שזוהו בתווית — לא אימות משפטי.
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="flex flex-1 flex-col justify-center space-y-0 px-6 pb-8 sm:px-8">
              {[
                ["תקן ייצור", "מפעל ISO 22000"],
                ["אלרגנים", "חיטה, חלב, סויה"],
                ["כשרות", "לפי אצווה"],
              ].map(([k, v], i) => (
                <div key={k}>
                  {i > 0 ? (
                    <Separator className="my-1 bg-gradient-to-l from-transparent via-black/[0.08] to-transparent" />
                  ) : null}
                  <div className="flex justify-between gap-4 py-4 text-sm transition-colors duration-300 hover:bg-[#FFFFFF]/70">
                    <span className="text-[#4E5663]">{k}</span>
                    <span className="max-w-[58%] text-end font-medium text-[#111318]">
                      {v}
                    </span>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </section>

        {/* —— Nutrition —— */}
        <section className="mt-20 md:mt-28">
          <SectionLabel
            icon={Scale}
            title="סקירת תזונה"
            subtitle="ל־100 גרם · ערכים לפי תווית היצרן"
          />
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 lg:gap-6">
            {nutrition.map((n) => {
              const Icon = n.icon;
              const a = nutritionAccent[n.accent];
              return (
                <div
                  key={n.label}
                  className={cn(
                    "group relative overflow-hidden rounded-2xl border border-black/[0.08] bg-[#FFFFFF]/60 p-6 shadow-[0_20px_44px_-28px_rgba(17,19,24,0.58)] backdrop-blur-xl transition duration-500 ease-out",
                    "hover:-translate-y-1 hover:bg-[#FFFFFF]/78 hover:shadow-[0_28px_52px_-22px_rgba(17,19,24,0.62)]",
                    a.glow
                  )}
                >
                  <div
                    className={cn(
                      "absolute start-0 top-0 h-full w-1 rounded-full bg-gradient-to-b opacity-80",
                      "from-[#1F8F6A] to-[#2FAE82]"
                    )}
                  />
                  <div className="relative flex items-start justify-between gap-4 ps-3">
                    <div>
                      <p className="text-[11px] font-semibold tracking-wide text-[#4E5663]">
                        {n.label}
                      </p>
                      <p className="mt-3 text-3xl font-semibold tabular-nums tracking-tight text-[#111318] transition duration-300 group-hover:text-[#111318]">
                        {n.value}
                        <span className="ms-1.5 text-base font-medium text-[#4E5663]">
                          {n.unit}
                        </span>
                      </p>
                      <p className="mt-2 text-xs font-medium text-[#4E5663]">
                        {n.per}
                      </p>
                    </div>
                    <span
                      className={cn(
                        "flex size-12 shrink-0 items-center justify-center rounded-2xl ring-1 backdrop-blur-sm transition duration-500 group-hover:scale-110",
                        a.icon
                      )}
                    >
                      <Icon className="size-5" strokeWidth={1.65} />
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* —— Ingredients —— */}
        <section className="mt-20 md:mt-28">
          <div className="mb-10 flex flex-col gap-4 sm:mb-12 sm:flex-row sm:items-end sm:justify-between">
            <SectionLabel
              className="mb-0 sm:mb-0"
              icon={Beaker}
              title="שקיפות רכיבים"
              subtitle="פירוט לפי סדר יורד של משקל בתווית"
            />
            <Badge
              variant="outline"
              className="h-8 w-fit shrink-0 self-start rounded-full border-black/[0.08] bg-[#2FAE82]/10 px-4 text-xs font-semibold text-[#1F8F6A] shadow-sm sm:self-auto"
            >
              סדר יורד לפי משקל
            </Badge>
          </div>

          <div className="flex flex-col gap-3">
            {ingredients.map((ing) => {
              const s = signalStyles[ing.signal];
              return (
                <div
                  key={ing.name}
                  className="group flex flex-col gap-4 rounded-2xl border border-black/[0.08] bg-[#FFFFFF]/58 px-5 py-5 shadow-[0_16px_40px_-28px_rgba(17,19,24,0.58)] backdrop-blur-xl transition duration-500 ease-out hover:border-[#1F8F6A]/18 hover:bg-[#FFFFFF]/70 hover:shadow-[0_24px_48px_-24px_rgba(47,174,130,0.06)] sm:flex-row sm:items-center sm:justify-between sm:gap-6 sm:px-8 sm:py-5"
                >
                  <div className="flex items-center gap-4">
                    <span
                      className={cn(
                        "relative flex size-3 shrink-0 rounded-full",
                        s.dot,
                        s.glow
                      )}
                    />
                    <div>
                      <p className="text-lg font-semibold text-[#111318]">
                        {ing.name}
                      </p>
                      <p className="mt-0.5 text-sm text-[#4E5663]">{ing.role}</p>
                    </div>
                  </div>
                  <div className="flex flex-wrap items-center gap-3 sm:justify-end">
                    <span
                      className={cn(
                        "rounded-full px-3 py-1 text-[11px] font-semibold ring-1 backdrop-blur-sm",
                        s.chip
                      )}
                    >
                      {ing.signalLabel}
                    </span>
                    <span className="rounded-xl bg-[#F7F7F2]/50 px-3 py-1.5 font-mono text-sm font-semibold tabular-nums text-[#4E5663]">
                      {ing.pct}%
                    </span>
                    <span className="text-sm text-[#7A817C]">{ing.note}</span>
                  </div>
                </div>
              );
            })}
          </div>
          <p className="mt-6 text-center text-xs leading-relaxed text-[#4E5663] md:text-start">
            אחוזים מחושבים מהתווית ומ־NutriScore כאשר קיים. צבעי הסטטוס הם סיווג
            תוויתי סטטי לדוגמה בלבד.
          </p>
        </section>

        {/* —— Analysis —— */}
        <section className="mt-20 md:mt-28">
          <SectionLabel
            icon={BarChart3}
            title="ניתוח מורחב"
            subtitle="הרחבה לפי נושא — נתונים סטטיים לדוגמה"
          />

          <div className="overflow-hidden rounded-[1.75rem] border border-black/[0.08] bg-[#FFFFFF]/58 p-2 shadow-[0_28px_56px_-32px_rgba(17,19,24,0.58)] ring-1 ring-black/[0.08] backdrop-blur-xl sm:p-3 md:rounded-[2rem]">
            <Accordion type="single" collapsible className="space-y-2">
              <AccordionItem
                value="processing"
                className="overflow-hidden rounded-2xl border-0 bg-[#FFFFFF]/60 shadow-sm ring-1 ring-black/[0.08] transition duration-300 hover:bg-[#FFFFFF]/78"
              >
                <AccordionTrigger className="px-5 py-5 text-start text-base font-semibold text-[#111318] transition-colors hover:text-[#1F8F6A] hover:no-underline sm:px-6 [&_[data-slot=accordion-trigger-icon]]:ms-auto [&_[data-slot=accordion-trigger-icon]]:ml-0">
                  עיבוד ומבנה מוצר
                </AccordionTrigger>
                <AccordionContent className="px-5 pb-6 sm:px-6">
                  <ul className="space-y-3 text-sm leading-relaxed text-[#4E5663]">
                    <li className="flex gap-3">
                      <span className="mt-2 size-1.5 shrink-0 rounded-full bg-[#2FAE82] shadow-[0_0_12px_rgba(47,174,130,0.06)]" />
                      שלב אפייה בטמפרטורה גבוהה — השפעה על ויטמינים מסיסי מים כפי
                      שמופיע בתווית.
                    </li>
                    <li className="flex gap-3">
                      <span className="mt-2 size-1.5 shrink-0 rounded-full bg-[#2FAE82] shadow-[0_0_12px_rgba(47,174,130,0.06)]" />
                      שומן צמחי לשיפור מרקם; ללא טענת &quot;מזון מינימלי&quot;.
                    </li>
                    <li className="flex gap-3">
                      <span className="mt-2 size-1.5 shrink-0 rounded-full bg-[#2FAE82] shadow-[0_0_12px_rgba(47,174,130,0.06)]" />
                      NOVA (אם קיים במאגר): 4 — מעובד במידה גבוהה.
                    </li>
                  </ul>
                </AccordionContent>
              </AccordionItem>

              <AccordionItem
                value="sugar"
                className="overflow-hidden rounded-2xl border-0 bg-[#FFFFFF]/60 shadow-sm ring-1 ring-black/[0.08] transition duration-300 hover:bg-[#FFFFFF]/78"
              >
                <AccordionTrigger className="px-5 py-5 text-start text-base font-semibold text-[#111318] transition-colors hover:text-[#1F8F6A] hover:no-underline sm:px-6 [&_[data-slot=accordion-trigger-icon]]:ms-auto [&_[data-slot=accordion-trigger-icon]]:ml-0">
                  פרופיל סוכרים
                </AccordionTrigger>
                <AccordionContent className="px-5 pb-6 sm:px-6">
                  <div className="grid gap-4 sm:grid-cols-2">
                    <div className="rounded-2xl bg-[#FFFFFF]/70 p-5 ring-1 ring-black/[0.08] transition duration-300 hover:bg-[#FFFFFF]/82">
                      <p className="text-xs font-semibold text-[#1F8F6A]/80">
                        סוכרים מוספים
                      </p>
                      <p className="mt-2 text-2xl font-semibold tabular-nums text-[#111318]">
                        12 גרם
                      </p>
                      <p className="mt-1 text-xs text-[#7A817C]">ל־100 גרם</p>
                    </div>
                    <div className="rounded-2xl bg-[#FFFFFF]/70 p-5 ring-1 ring-black/[0.08] transition duration-300 hover:bg-[#FFFFFF]/82">
                      <p className="text-xs font-semibold text-[#1F8F6A]/80">
                        סוכר כולל
                      </p>
                      <p className="mt-2 text-2xl font-semibold tabular-nums text-[#111318]">
                        12 גרם
                      </p>
                      <p className="mt-1 text-xs text-[#7A817C]">ל־100 גרם</p>
                    </div>
                    <p className="text-sm leading-relaxed text-[#4E5663] sm:col-span-2">
                      אין פירוט לפי סוג סוכר בתווית המקורית; Bari משתמש בערך
                      הכולל בלבד לצורך דירוג.
                    </p>
                  </div>
                </AccordionContent>
              </AccordionItem>

              <AccordionItem
                value="additives"
                className="overflow-hidden rounded-2xl border-0 bg-[#FFFFFF]/60 shadow-sm ring-1 ring-black/[0.08] transition duration-300 hover:bg-[#FFFFFF]/78"
              >
                <AccordionTrigger className="px-5 py-5 text-start text-base font-semibold text-[#111318] transition-colors hover:text-[#1F8F6A] hover:no-underline sm:px-6 [&_[data-slot=accordion-trigger-icon]]:ms-auto [&_[data-slot=accordion-trigger-icon]]:ml-0">
                  תוספים ורשויות מאשרות
                </AccordionTrigger>
                <AccordionContent className="px-5 pb-6 sm:px-6">
                  <div className="overflow-hidden rounded-2xl bg-[#FFFFFF]/68 ring-1 ring-black/[0.08]">
                    <table className="w-full text-right text-sm">
                      <thead>
                        <tr className="text-xs font-semibold text-[#4E5663]">
                          <th className="px-4 py-3 font-medium">קוד</th>
                          <th className="px-4 py-3 font-medium">שם</th>
                          <th className="px-4 py-3 font-medium">מגבלה</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-white/[0.08]">
                        <tr className="transition-colors hover:bg-[#1F8F6A]/[0.04]">
                          <td className="px-4 py-3 tabular-nums font-medium text-[#111318]">
                            E322
                          </td>
                          <td className="px-4 py-3 text-[#4E5663]">לציטין סויה</td>
                          <td className="px-4 py-3 text-[#7A817C]">ADI קיים</td>
                        </tr>
                        <tr className="transition-colors hover:bg-[#1F8F6A]/[0.04]">
                          <td className="px-4 py-3 tabular-nums font-medium text-[#111318]">
                            E500
                          </td>
                          <td className="px-4 py-3 text-[#4E5663]">פחמת סודיום</td>
                          <td className="px-4 py-3 text-[#7A817C]">QS</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <p className="mt-4 text-xs leading-relaxed text-[#7A817C]">
                    קישור לרגולציה מוצג כאשר קיים במאגר; אין המלצה לצריכה או
                    הימנעות.
                  </p>
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </div>
        </section>

        <footer className="mt-24 text-center md:mt-32">
          <div className="inline-flex flex-col items-center gap-3 rounded-2xl border border-black/[0.08] bg-[#FFFFFF]/60 px-8 py-6 shadow-[0_16px_40px_-24px_rgba(17,19,24,0.58)] backdrop-blur-md">
            <BariBrandLogo />
            <p className="text-xs font-medium text-[#7A817C]">ידע ומדע במזון שאתם צורכים</p>
            <p className="text-[11px] text-[#4E5663]">נתונים לצורכי השוואה ומחקר צרכן</p>
          </div>
        </footer>
      </main>
    </div>
  );
}
