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
  CardFooter,
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
    accent: "teal" as const,
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
    accent: "sky" as const,
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
    stroke: "text-amber-400",
    glow: "shadow-amber-500/20",
    icon: "bg-amber-400/12 text-amber-800 ring-amber-400/25",
  },
  emerald: {
    stroke: "text-emerald-400",
    glow: "shadow-emerald-500/20",
    icon: "bg-emerald-500/12 text-emerald-900 ring-emerald-400/25",
  },
  teal: {
    stroke: "text-teal-400",
    glow: "shadow-teal-500/15",
    icon: "bg-teal-500/12 text-teal-900 ring-teal-400/25",
  },
  sky: {
    stroke: "text-sky-400",
    glow: "shadow-sky-500/15",
    icon: "bg-sky-500/12 text-sky-900 ring-sky-400/25",
  },
  rose: {
    stroke: "text-rose-400",
    glow: "shadow-rose-500/15",
    icon: "bg-rose-500/12 text-rose-900 ring-rose-400/25",
  },
};

const signalStyles = {
  green: {
    dot: "bg-emerald-400",
    glow: "shadow-[0_0_20px_rgba(52,211,153,0.45)]",
    chip: "bg-emerald-500/12 text-emerald-950 ring-emerald-400/20",
  },
  yellow: {
    dot: "bg-amber-400",
    glow: "shadow-[0_0_20px_rgba(251,191,36,0.4)]",
    chip: "bg-amber-400/15 text-amber-950 ring-amber-400/25",
  },
  red: {
    dot: "bg-rose-400",
    glow: "shadow-[0_0_20px_rgba(251,113,133,0.45)]",
    chip: "bg-rose-500/12 text-rose-950 ring-rose-400/25",
  },
};

function MeshBackdrop() {
  return (
    <>
      <div
        className="pointer-events-none fixed inset-0 -z-20 bg-[#f4f9f7]"
        aria-hidden
      />
      <div
        className="pointer-events-none fixed inset-0 -z-10 opacity-90"
        aria-hidden
        style={{
          background: `
            radial-gradient(900px 520px at 85% -8%, rgba(167, 243, 208, 0.55), transparent 55%),
            radial-gradient(700px 480px at 0% 40%, rgba(224, 242, 254, 0.35), transparent 50%),
            radial-gradient(600px 500px at 100% 85%, rgba(209, 250, 229, 0.5), transparent 50%)
          `,
        }}
      />
      <div
        className="pointer-events-none fixed inset-0 -z-10 bg-gradient-to-b from-white/50 via-transparent to-emerald-50/30"
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
        className="absolute inset-0 -z-10 rounded-full bg-emerald-400/25 blur-3xl"
        aria-hidden
      />
      <div
        className="absolute inset-2 -z-10 rounded-full bg-gradient-to-br from-white/80 via-emerald-50/40 to-transparent opacity-90"
        aria-hidden
      />
      <div className="relative rounded-full p-1 shadow-[0_1px_0_rgba(255,255,255,0.9)_inset,0_24px_48px_-28px_rgba(16,185,129,0.35)] ring-1 ring-white/70">
        <svg
          className="size-[9.5rem] -rotate-90 sm:size-[10.5rem]"
          viewBox="0 0 124 124"
          aria-hidden
        >
          <defs>
            <linearGradient id={gid} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#34d399" />
              <stop offset="55%" stopColor="#10b981" />
              <stop offset="100%" stopColor="#059669" />
            </linearGradient>
          </defs>
          <circle
            cx="62"
            cy="62"
            r={RING_R}
            className="text-emerald-100/80"
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
            className="drop-shadow-[0_0_12px_rgba(16,185,129,0.35)] transition-[stroke-dashoffset] duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-[10px] font-semibold uppercase tracking-[0.2em] text-emerald-700/70">
            Bari
          </span>
          <span className="mt-0.5 text-4xl font-semibold tabular-nums tracking-tight text-zinc-900 sm:text-5xl">
            {SCORE}
          </span>
          <span className="mt-1 text-xs font-medium text-zinc-400">מתוך 100</span>
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
        <span className="flex size-12 items-center justify-center rounded-2xl bg-white/70 text-emerald-700 shadow-[0_12px_32px_-16px_rgba(16,185,129,0.35)] ring-1 ring-white/80 backdrop-blur-md transition duration-500 ease-out hover:scale-[1.03] hover:shadow-[0_16px_40px_-12px_rgba(16,185,129,0.4)]">
          <Icon className="size-5" strokeWidth={1.65} />
        </span>
        <div>
          <h2 className="text-2xl font-semibold tracking-tight text-zinc-900 md:text-[1.65rem]">
            {title}
          </h2>
          {subtitle ? (
            <p className="mt-1 max-w-xl text-sm leading-relaxed text-zinc-500 md:text-[0.9375rem]">
              {subtitle}
            </p>
          ) : null}
        </div>
      </div>
      <div className="ms-16 h-px max-w-md bg-gradient-to-l from-transparent via-emerald-200/60 to-emerald-400/30" />
    </div>
  );
}

export default function ProductPage() {
  return (
    <div
      className={cn(
        hebrew.className,
        "relative min-h-screen overflow-x-hidden text-zinc-900 antialiased",
        "selection:bg-emerald-500/20 selection:text-emerald-950"
      )}
    >
      <MeshBackdrop />

      <main
        dir="rtl"
        lang="he"
        className="relative mx-auto max-w-6xl px-5 pb-24 pt-14 sm:px-8 sm:pb-28 sm:pt-16 md:px-10 md:pt-20"
      >
        {/* —— Hero —— */}
        <section className="relative overflow-hidden rounded-[2rem] border border-white/60 bg-white/55 p-8 shadow-[0_32px_64px_-28px_rgba(15,23,42,0.12),0_0_0_1px_rgba(255,255,255,0.8)_inset] backdrop-blur-2xl backdrop-saturate-150 sm:p-10 md:rounded-[2.25rem] md:p-12 lg:p-14">
          <div
            className="pointer-events-none absolute -start-24 -top-24 size-72 rounded-full bg-emerald-300/25 blur-3xl"
            aria-hidden
          />
          <div
            className="pointer-events-none absolute -bottom-20 -end-16 size-80 rounded-full bg-sky-200/20 blur-3xl"
            aria-hidden
          />

          <div className="relative grid gap-12 lg:grid-cols-[minmax(0,1.15fr)_minmax(240px,0.85fr)] lg:items-center lg:gap-16">
            <div className="flex min-w-0 flex-col gap-8">
              <div className="flex flex-wrap items-center gap-2">
                <Badge className="h-7 rounded-full border-0 bg-emerald-600/90 px-3 text-[11px] font-semibold text-white shadow-lg shadow-emerald-600/25 transition duration-300 hover:bg-emerald-600 hover:shadow-emerald-600/35">
                  חטיף · קטגוריה
                </Badge>
                <Badge
                  variant="outline"
                  className="h-7 rounded-full border-white/80 bg-white/50 px-3 text-[11px] font-medium text-zinc-600 shadow-sm backdrop-blur-sm"
                >
                  מאומת תווית
                </Badge>
                <span className="rounded-full bg-zinc-900/[0.03] px-3 py-1 font-mono text-[11px] tabular-nums text-zinc-500">
                  GTIN 7290001234567
                </span>
              </div>

              <div className="space-y-4">
                <p className="text-[11px] font-semibold tracking-[0.18em] text-emerald-700/80">
                  BARI · מודיעין מזון
                </p>
                <h1 className="text-balance text-[2rem] font-semibold leading-[1.08] tracking-tight text-zinc-950 sm:text-[2.35rem] md:text-[2.65rem]">
                  מוצר הדגמה
                </h1>
                <p className="max-w-xl text-base leading-relaxed text-zinc-600 md:text-[1.05rem]">
                  תצוגת נתונים מבוססת תווית ומקורות רשמיים. הציון משקלל רכיבים,
                  פרופיל תזונתי ושקיפות מידע — ללא המלצות רפואיות.
                </p>
              </div>

              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-4">
                <Sheet>
                  <SheetTrigger asChild>
                    <Button
                      size="lg"
                      className="group h-12 rounded-2xl bg-gradient-to-l from-emerald-600 to-emerald-500 px-8 text-sm font-semibold text-white shadow-[0_16px_40px_-12px_rgba(16,185,129,0.45)] transition-all duration-500 ease-out hover:-translate-y-0.5 hover:from-emerald-500 hover:to-emerald-400 hover:shadow-[0_22px_48px_-10px_rgba(16,185,129,0.5)] active:translate-y-0"
                    >
                      <GitCompareArrows className="size-4 transition-transform duration-500 group-hover:-rotate-6" />
                      השוואת מוצרים
                    </Button>
                  </SheetTrigger>
                  <SheetContent
                    side="right"
                    showCloseButton={false}
                    className="flex w-full flex-col gap-0 border-white/40 bg-white/75 p-0 shadow-2xl shadow-emerald-950/10 backdrop-blur-2xl sm:max-w-md"
                  >
                    <div className="relative px-6 pb-6 pt-16 sm:px-8">
                      <div className="pointer-events-none absolute inset-0 bg-gradient-to-bl from-emerald-100/40 via-transparent to-sky-50/30" />
                      <SheetClose asChild>
                        <Button
                          variant="ghost"
                          size="icon-sm"
                          className="absolute top-5 right-5 rounded-xl text-zinc-500 transition-colors hover:bg-white/80 hover:text-zinc-900"
                          aria-label="סגור"
                        >
                          <X className="size-4" />
                        </Button>
                      </SheetClose>
                      <SheetHeader className="relative space-y-2 p-0 text-right">
                        <SheetTitle className="text-xl font-semibold text-zinc-950">
                          השוואת מוצרים
                        </SheetTitle>
                        <SheetDescription className="text-sm text-zinc-500">
                          נתונים ל־100 גרם · ציון Bari לפי מודל המערכת
                        </SheetDescription>
                      </SheetHeader>
                    </div>

                    <div className="relative flex-1 overflow-auto px-6 py-2 sm:px-8">
                      <div className="overflow-hidden rounded-2xl bg-white/60 shadow-[0_1px_0_rgba(255,255,255,0.9)_inset,0_12px_40px_-24px_rgba(15,23,42,0.08)] ring-1 ring-emerald-950/[0.04] backdrop-blur-sm">
                        <table className="w-full min-w-[300px] text-right text-sm">
                          <thead>
                            <tr className="text-xs font-semibold text-zinc-400">
                              <th className="px-4 py-3.5 font-medium">מוצר</th>
                              <th className="px-4 py-3.5 font-medium">ציון</th>
                              <th className="px-4 py-3.5 font-medium">קק״ל</th>
                              <th className="px-4 py-3.5 font-medium">חלבון</th>
                              <th className="px-4 py-3.5 font-medium">נתרן</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-emerald-950/[0.04]">
                            {comparisonRows.map((row) => (
                              <tr
                                key={row.name}
                                className={cn(
                                  "transition-colors duration-300 hover:bg-emerald-500/[0.06]",
                                  row.highlight &&
                                    "bg-gradient-to-l from-emerald-500/[0.08] to-transparent"
                                )}
                              >
                                <td className="px-4 py-3.5 font-medium text-zinc-800">
                                  {row.name}
                                </td>
                                <td className="px-4 py-3.5 tabular-nums font-semibold text-emerald-700">
                                  {row.score}
                                </td>
                                <td className="px-4 py-3.5 tabular-nums text-zinc-600">
                                  {row.kcal}
                                </td>
                                <td className="px-4 py-3.5 tabular-nums text-zinc-600">
                                  {row.protein}
                                </td>
                                <td className="px-4 py-3.5 tabular-nums text-zinc-600">
                                  {row.sodium}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>

                    <SheetFooter className="border-t border-white/50 bg-white/30 px-6 py-5 backdrop-blur-md sm:px-8">
                      <p className="text-xs leading-relaxed text-zinc-500">
                        ההשוואה מבוססת על ערכים שדווחו לרשות המזון או על תווית
                        היצרן. ייתכנו פערים בין אצווה לאצווה.
                      </p>
                    </SheetFooter>
                  </SheetContent>
                </Sheet>

                <Button
                  variant="ghost"
                  size="lg"
                  className="h-12 rounded-2xl text-zinc-500 transition-all duration-300 hover:bg-white/60 hover:text-zinc-800"
                  disabled
                >
                  <Package className="size-4 opacity-70" />
                  ייצוא נתונים
                </Button>
              </div>
            </div>

            <div className="relative mx-auto w-full max-w-[280px] lg:mx-0 lg:max-w-none">
              <div className="aspect-[4/5] overflow-hidden rounded-[1.75rem] bg-gradient-to-br from-white via-emerald-50/50 to-teal-100/40 shadow-[0_28px_56px_-24px_rgba(16,185,129,0.35)] ring-1 ring-white/80 transition duration-700 ease-out hover:-translate-y-1 hover:shadow-[0_36px_64px_-20px_rgba(16,185,129,0.4)]">
                <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_30%_20%,rgba(255,255,255,0.95),transparent_50%),radial-gradient(ellipse_at_80%_80%,rgba(167,243,208,0.45),transparent_55%)]" />
                <div className="relative flex h-full flex-col items-center justify-center gap-5 p-8">
                  <div className="flex size-20 items-center justify-center rounded-3xl bg-white/75 text-emerald-600 shadow-[0_20px_40px_-16px_rgba(16,185,129,0.35)] ring-1 ring-white/90 backdrop-blur-md transition duration-500 hover:rotate-6 hover:scale-105">
                    <Sparkles className="size-10" strokeWidth={1.15} />
                  </div>
                  <div className="text-center">
                    <p className="text-sm font-medium text-zinc-700">תצוגת מוצר</p>
                    <p className="mt-1 text-xs text-zinc-400">ממתין לנכס ויזואלי</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* —— Bento: score + compliance —— */}
        <section className="mt-16 grid gap-6 md:mt-20 md:gap-8 lg:grid-cols-12">
          <Card className="group relative overflow-hidden border-0 bg-white/50 shadow-[0_28px_56px_-32px_rgba(15,23,42,0.18)] ring-1 ring-white/80 backdrop-blur-xl transition duration-500 ease-out hover:-translate-y-1 hover:shadow-[0_36px_64px_-28px_rgba(15,23,42,0.2)] lg:col-span-8 lg:rounded-[2rem]">
            <div className="pointer-events-none absolute inset-0 bg-gradient-to-bl from-emerald-100/35 via-transparent to-sky-50/20 opacity-80 transition duration-700 group-hover:opacity-100" />
            <CardHeader className="relative flex flex-col gap-10 border-0 pb-2 pt-10 sm:flex-row sm:items-center sm:justify-between sm:px-10 sm:pt-12">
              <div className="max-w-md space-y-4 text-center sm:text-right">
                <div className="flex flex-wrap justify-center gap-2 sm:justify-end">
                  <span className="inline-flex items-center gap-1.5 rounded-full bg-amber-400/15 px-3 py-1 text-[11px] font-semibold text-amber-950 ring-1 ring-amber-400/25">
                    <span className="size-1.5 rounded-full bg-amber-400 shadow-[0_0_10px_rgba(251,191,36,0.6)]" />
                    מודל פעיל
                  </span>
                  <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-500/12 px-3 py-1 text-[11px] font-semibold text-emerald-950 ring-1 ring-emerald-400/25">
                    <span className="size-1.5 rounded-full bg-emerald-400 shadow-[0_0_10px_rgba(52,211,153,0.55)]" />
                    נתונים סטטיים
                  </span>
                </div>
                <div>
                  <CardDescription className="text-xs font-semibold tracking-wide text-zinc-400">
                    ציון Bari
                  </CardDescription>
                  <CardTitle className="mt-2 text-2xl font-semibold leading-tight text-zinc-950 md:text-3xl">
                    פרופיל תזונתי־רכיבי
                  </CardTitle>
                  <p className="mt-3 text-sm leading-relaxed text-zinc-500">
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
                  className="rounded-2xl bg-white/55 px-5 py-5 shadow-[0_1px_0_rgba(255,255,255,0.9)_inset] ring-1 ring-emerald-950/[0.04] transition duration-500 ease-out hover:bg-white/80 hover:shadow-lg hover:shadow-emerald-500/10"
                >
                  <p className="text-[11px] font-semibold text-zinc-400">
                    {m.label}
                  </p>
                  <p className="mt-2 text-lg font-semibold tabular-nums text-zinc-900">
                    {m.value}
                  </p>
                  <p className="mt-1 text-xs text-zinc-500">{m.sub}</p>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card className="group flex flex-col border-0 bg-white/45 shadow-[0_24px_48px_-28px_rgba(15,23,42,0.14)] ring-1 ring-white/80 backdrop-blur-xl transition duration-500 ease-out hover:-translate-y-1 hover:shadow-[0_32px_56px_-24px_rgba(15,23,42,0.16)] lg:col-span-4 lg:rounded-[2rem]">
            <CardHeader className="border-0 pb-2 pt-8 sm:px-8 sm:pt-10">
              <div className="flex items-start gap-4">
                <span className="flex size-11 shrink-0 items-center justify-center rounded-2xl bg-emerald-500/12 text-emerald-800 ring-1 ring-emerald-400/20 shadow-inner shadow-white/60">
                  <ShieldCheck className="size-5" strokeWidth={1.6} />
                </span>
                <div>
                  <CardTitle className="text-lg font-semibold text-zinc-950">
                    רגולציה ותווית
                  </CardTitle>
                  <CardDescription className="mt-2 text-sm leading-relaxed text-zinc-500">
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
                    <Separator className="my-1 bg-gradient-to-l from-transparent via-emerald-100/80 to-transparent" />
                  ) : null}
                  <div className="flex justify-between gap-4 py-4 text-sm transition-colors duration-300 hover:bg-white/40">
                    <span className="text-zinc-400">{k}</span>
                    <span className="max-w-[58%] text-end font-medium text-zinc-800">
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
                    "group relative overflow-hidden rounded-2xl border border-white/70 bg-white/50 p-6 shadow-[0_20px_44px_-28px_rgba(15,23,42,0.12)] backdrop-blur-xl transition duration-500 ease-out",
                    "hover:-translate-y-1 hover:bg-white/70 hover:shadow-[0_28px_52px_-22px_rgba(15,23,42,0.14)]",
                    a.glow
                  )}
                >
                  <div
                    className={cn(
                      "absolute start-0 top-0 h-full w-1 rounded-full bg-gradient-to-b opacity-80",
                      n.accent === "amber" && "from-amber-300 to-amber-500",
                      n.accent === "emerald" && "from-emerald-300 to-emerald-600",
                      n.accent === "teal" && "from-teal-300 to-teal-600",
                      n.accent === "sky" && "from-sky-300 to-sky-500",
                      n.accent === "rose" && "from-rose-300 to-rose-500"
                    )}
                  />
                  <div className="relative flex items-start justify-between gap-4 ps-3">
                    <div>
                      <p className="text-[11px] font-semibold tracking-wide text-zinc-400">
                        {n.label}
                      </p>
                      <p className="mt-3 text-3xl font-semibold tabular-nums tracking-tight text-zinc-950 transition duration-300 group-hover:text-zinc-900">
                        {n.value}
                        <span className="ms-1.5 text-base font-medium text-zinc-400">
                          {n.unit}
                        </span>
                      </p>
                      <p className="mt-2 text-xs font-medium text-zinc-400">
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
              className="h-8 w-fit shrink-0 self-start rounded-full border-emerald-400/30 bg-emerald-500/10 px-4 text-xs font-semibold text-emerald-950 shadow-sm sm:self-auto"
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
                  className="group flex flex-col gap-4 rounded-2xl border border-white/60 bg-white/45 px-5 py-5 shadow-[0_16px_40px_-28px_rgba(15,23,42,0.1)] backdrop-blur-xl transition duration-500 ease-out hover:border-emerald-200/40 hover:bg-white/65 hover:shadow-[0_24px_48px_-24px_rgba(16,185,129,0.12)] sm:flex-row sm:items-center sm:justify-between sm:gap-6 sm:px-8 sm:py-5"
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
                      <p className="text-lg font-semibold text-zinc-950">
                        {ing.name}
                      </p>
                      <p className="mt-0.5 text-sm text-zinc-500">{ing.role}</p>
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
                    <span className="rounded-xl bg-zinc-900/[0.04] px-3 py-1.5 font-mono text-sm font-semibold tabular-nums text-zinc-700">
                      {ing.pct}%
                    </span>
                    <span className="text-sm text-zinc-500">{ing.note}</span>
                  </div>
                </div>
              );
            })}
          </div>
          <p className="mt-6 text-center text-xs leading-relaxed text-zinc-400 md:text-start">
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

          <div className="overflow-hidden rounded-[1.75rem] border border-white/60 bg-white/45 p-2 shadow-[0_28px_56px_-32px_rgba(15,23,42,0.12)] ring-1 ring-white/70 backdrop-blur-xl sm:p-3 md:rounded-[2rem]">
            <Accordion type="single" collapsible className="space-y-2">
              <AccordionItem
                value="processing"
                className="overflow-hidden rounded-2xl border-0 bg-white/40 shadow-sm ring-1 ring-emerald-950/[0.03] transition duration-300 hover:bg-white/70"
              >
                <AccordionTrigger className="px-5 py-5 text-start text-base font-semibold text-zinc-900 transition-colors hover:text-emerald-800 hover:no-underline sm:px-6 [&_[data-slot=accordion-trigger-icon]]:ms-auto [&_[data-slot=accordion-trigger-icon]]:ml-0">
                  עיבוד ומבנה מוצר
                </AccordionTrigger>
                <AccordionContent className="px-5 pb-6 sm:px-6">
                  <ul className="space-y-3 text-sm leading-relaxed text-zinc-600">
                    <li className="flex gap-3">
                      <span className="mt-2 size-1.5 shrink-0 rounded-full bg-emerald-400 shadow-[0_0_12px_rgba(52,211,153,0.5)]" />
                      שלב אפייה בטמפרטורה גבוהה — השפעה על ויטמינים מסיסי מים כפי
                      שמופיע בתווית.
                    </li>
                    <li className="flex gap-3">
                      <span className="mt-2 size-1.5 shrink-0 rounded-full bg-emerald-400 shadow-[0_0_12px_rgba(52,211,153,0.5)]" />
                      שומן צמחי לשיפור מרקם; ללא טענת &quot;מזון מינימלי&quot;.
                    </li>
                    <li className="flex gap-3">
                      <span className="mt-2 size-1.5 shrink-0 rounded-full bg-emerald-400 shadow-[0_0_12px_rgba(52,211,153,0.5)]" />
                      NOVA (אם קיים במאגר): 4 — מעובד במידה גבוהה.
                    </li>
                  </ul>
                </AccordionContent>
              </AccordionItem>

              <AccordionItem
                value="sugar"
                className="overflow-hidden rounded-2xl border-0 bg-white/40 shadow-sm ring-1 ring-emerald-950/[0.03] transition duration-300 hover:bg-white/70"
              >
                <AccordionTrigger className="px-5 py-5 text-start text-base font-semibold text-zinc-900 transition-colors hover:text-emerald-800 hover:no-underline sm:px-6 [&_[data-slot=accordion-trigger-icon]]:ms-auto [&_[data-slot=accordion-trigger-icon]]:ml-0">
                  פרופיל סוכרים
                </AccordionTrigger>
                <AccordionContent className="px-5 pb-6 sm:px-6">
                  <div className="grid gap-4 sm:grid-cols-2">
                    <div className="rounded-2xl bg-amber-50/50 p-5 ring-1 ring-amber-200/30 transition duration-300 hover:bg-amber-50/80">
                      <p className="text-xs font-semibold text-amber-800/80">
                        סוכרים מוספים
                      </p>
                      <p className="mt-2 text-2xl font-semibold tabular-nums text-zinc-900">
                        12 גרם
                      </p>
                      <p className="mt-1 text-xs text-zinc-500">ל־100 גרם</p>
                    </div>
                    <div className="rounded-2xl bg-amber-50/50 p-5 ring-1 ring-amber-200/30 transition duration-300 hover:bg-amber-50/80">
                      <p className="text-xs font-semibold text-amber-800/80">
                        סוכר כולל
                      </p>
                      <p className="mt-2 text-2xl font-semibold tabular-nums text-zinc-900">
                        12 גרם
                      </p>
                      <p className="mt-1 text-xs text-zinc-500">ל־100 גרם</p>
                    </div>
                    <p className="text-sm leading-relaxed text-zinc-600 sm:col-span-2">
                      אין פירוט לפי סוג סוכר בתווית המקורית; Bari משתמש בערך
                      הכולל בלבד לצורך דירוג.
                    </p>
                  </div>
                </AccordionContent>
              </AccordionItem>

              <AccordionItem
                value="additives"
                className="overflow-hidden rounded-2xl border-0 bg-white/40 shadow-sm ring-1 ring-emerald-950/[0.03] transition duration-300 hover:bg-white/70"
              >
                <AccordionTrigger className="px-5 py-5 text-start text-base font-semibold text-zinc-900 transition-colors hover:text-emerald-800 hover:no-underline sm:px-6 [&_[data-slot=accordion-trigger-icon]]:ms-auto [&_[data-slot=accordion-trigger-icon]]:ml-0">
                  תוספים ורשויות מאשרות
                </AccordionTrigger>
                <AccordionContent className="px-5 pb-6 sm:px-6">
                  <div className="overflow-hidden rounded-2xl bg-white/60 ring-1 ring-emerald-950/[0.04]">
                    <table className="w-full text-right text-sm">
                      <thead>
                        <tr className="text-xs font-semibold text-zinc-400">
                          <th className="px-4 py-3 font-medium">קוד</th>
                          <th className="px-4 py-3 font-medium">שם</th>
                          <th className="px-4 py-3 font-medium">מגבלה</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-emerald-950/[0.04]">
                        <tr className="transition-colors hover:bg-emerald-500/[0.04]">
                          <td className="px-4 py-3 tabular-nums font-medium text-zinc-800">
                            E322
                          </td>
                          <td className="px-4 py-3 text-zinc-700">לציטין סויה</td>
                          <td className="px-4 py-3 text-zinc-500">ADI קיים</td>
                        </tr>
                        <tr className="transition-colors hover:bg-emerald-500/[0.04]">
                          <td className="px-4 py-3 tabular-nums font-medium text-zinc-800">
                            E500
                          </td>
                          <td className="px-4 py-3 text-zinc-700">פחמת סודיום</td>
                          <td className="px-4 py-3 text-zinc-500">QS</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <p className="mt-4 text-xs leading-relaxed text-zinc-500">
                    קישור לרגולציה מוצג כאשר קיים במאגר; אין המלצה לצריכה או
                    הימנעות.
                  </p>
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </div>
        </section>

        <footer className="mt-24 text-center md:mt-32">
          <div className="inline-flex flex-col items-center gap-3 rounded-2xl border border-white/50 bg-white/40 px-8 py-6 shadow-[0_16px_40px_-24px_rgba(15,23,42,0.1)] backdrop-blur-md">
            <BariBrandLogo />
            <p className="text-xs font-medium text-zinc-500">ידע ומדע במזון שאתם צורכים</p>
            <p className="text-[11px] text-zinc-400">נתונים לצורכי השוואה ומחקר צרכן</p>
          </div>
        </footer>
      </main>
    </div>
  );
}
