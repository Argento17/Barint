import type { ReactNode } from "react";
import Link from "next/link";
import { Noto_Sans_Hebrew } from "next/font/google";
import {
  Barcode,
  CheckCircle2,
  Database,
  FileSearch,
  GitCompareArrows,
  ScanLine,
  Search,
  Shield,
  Sparkles,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

const hebrew = Noto_Sans_Hebrew({
  subsets: ["hebrew"],
  weight: ["400", "500", "600", "700"],
  display: "swap",
});

const comparisonPreview = [
  { name: "מוצר א׳", score: "82", kcal: "412", sodium: "0.38" },
  { name: "מוצר ב׳", score: "71", kcal: "438", sodium: "0.42" },
  { name: "מוצר ג׳", score: "76", kcal: "401", sodium: "0.35" },
] as const;

const steps = [
  {
    step: "1",
    title: "סריקה או חיפוש",
    body: "מזינים ברקוד, שם מוצר או מותג — Bari מזהה את הרשומה במאגר.",
    icon: Barcode,
  },
  {
    step: "2",
    title: "ניתוח מבוסס תווית",
    body: "רכיבים, תזונה ל־100 גרם, תוספים ומטא־דאטה רגולטורית מסודרים במקום אחד.",
    icon: FileSearch,
  },
  {
    step: "3",
    title: "השוואה והקשר",
    body: "משווים למוצרים דומים ובודקים איך הנתון נראה מול קטגוריה ומקורות רשמיים.",
    icon: GitCompareArrows,
  },
] as const;

const trustPoints = [
  {
    title: "מקורות רשמיים",
    text: "שדות מסומנים כ־«לפי תווית» או «לפי רשות» כדי לשמור על עקביות בין מקורות.",
    icon: Shield,
  },
  {
    title: "שקיפות מודל",
    text: "ציון Bari מוצג עם רמת ביטחון ותאריך עדכון — בלי ניסוחים שיווקיים.",
    icon: Sparkles,
  },
  {
    title: "מאגר מובנה",
    text: "GTIN, קטגוריות ושדות אחידים מאפשרים השוואות עקביות בין מותגים.",
    icon: Database,
  },
] as const;

function SectionShell({
  id,
  className,
  children,
}: {
  id?: string;
  className?: string;
  children: ReactNode;
}) {
  return (
    <section
      id={id}
      className={cn("mx-auto max-w-6xl px-5 py-16 sm:px-8 sm:py-20 md:py-24", className)}
    >
      {children}
    </section>
  );
}

export default function HomePage() {
  return (
    <div
      className={cn(
        hebrew.className,
        "relative min-h-screen overflow-x-hidden bg-[#f4f9f7] text-zinc-900 antialiased selection:bg-emerald-500/20"
      )}
    >
      <div className="pointer-events-none fixed inset-0 -z-10 bg-[radial-gradient(900px_520px_at_80%_-10%,rgba(167,243,208,0.45),transparent_55%),radial-gradient(700px_420px_at_0%_40%,rgba(224,242,254,0.28),transparent_50%)]" />
      <div className="pointer-events-none fixed inset-0 -z-10 bg-gradient-to-b from-white/60 via-transparent to-emerald-50/35" />

      <main lang="he">
        {/* 1 — Hero */}
        <SectionShell className="pb-12 pt-14 sm:pb-16 sm:pt-16 md:pt-20">
          <div className="mx-auto max-w-3xl text-center">
            <Badge
              variant="outline"
              className="mb-6 rounded-full border-emerald-500/25 bg-emerald-500/10 px-4 py-1 text-xs font-semibold text-emerald-900 shadow-sm ring-1 ring-emerald-500/10"
            >
              מודיעין מזון למוצרים ארוזים בישראל
            </Badge>
            <h1 className="text-balance text-4xl font-semibold leading-[1.08] tracking-tight text-zinc-950 sm:text-5xl md:text-[3.15rem]">
              תווית ברורה.
              <span className="block text-emerald-800/95">החלטה מדויקת.</span>
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-zinc-600 md:text-xl">
              Bari הופכת נתונים מתווית ומהרגולציה לתמונה אחת מסודרת — כדי שתדעו
              מה באמת במוצר, בלי רעש.
            </p>
            <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row sm:gap-4">
              <Button
                size="lg"
                className="h-12 w-full rounded-2xl bg-gradient-to-l from-emerald-600 to-emerald-500 px-8 text-sm font-semibold text-white shadow-lg shadow-emerald-600/25 transition hover:-translate-y-0.5 hover:shadow-xl sm:w-auto"
                asChild
              >
                <Link href="/products/demo">למסך מוצר לדוגמה</Link>
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="h-12 w-full rounded-2xl border-white/80 bg-white/60 px-8 text-sm font-semibold shadow-sm backdrop-blur-sm transition hover:bg-white/90 sm:w-auto"
                asChild
              >
                <a href="#how">איך זה עובד</a>
              </Button>
            </div>
          </div>
        </SectionShell>

        {/* 2 — What Bari does */}
        <SectionShell className="py-12 sm:py-16">
          <Card className="border-white/70 bg-white/65 shadow-[0_24px_56px_-32px_rgba(15,23,42,0.12)] ring-1 ring-white/80 backdrop-blur-xl md:rounded-[1.75rem]">
            <CardHeader className="space-y-2 px-6 pt-8 text-center sm:px-10 sm:pt-10">
              <CardDescription className="text-xs font-semibold tracking-wide text-emerald-800/80">
                מה Bari עושה
              </CardDescription>
              <CardTitle className="text-2xl font-semibold text-zinc-950 md:text-3xl">
                אינטליגנציה על מזון ארוז — לא ייעוץ תזונתי ולא תוכן &quot;וולנס&quot;
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 px-6 pb-8 text-center text-base leading-relaxed text-zinc-600 sm:px-10 sm:pb-10 sm:text-[1.05rem]">
              <p>
                הפלטפורמה אוגדת רכיבים, ערכים תזונתיים, תוספים, אלרגנים ומידע
                רגולטורי מזוהה בתווית ובמקורות רשמיים, ומציגה אותם במבנה אחיד
                לצורך השוואה ומחקר צרכן.
              </p>
              <p className="text-sm text-zinc-500">
                כל הנתונים בעמוד זה לדוגמה סטטית; אין איסוף חיפושים או חיבור
                לשרת בגרסה הנוכחית.
              </p>
            </CardContent>
          </Card>
        </SectionShell>

        {/* 3 — Search / barcode mockup */}
        <SectionShell id="search" className="py-12 sm:py-16">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-2xl font-semibold tracking-tight text-zinc-950 md:text-3xl">
              חיפוש מוצר או ברקוד
            </h2>
            <p className="mt-3 text-sm text-zinc-500 md:text-base">
              תצוגת מוקאפ בלבד — השדות אינם שולחים בקשות רשת.
            </p>
          </div>
          <Card className="mx-auto mt-10 max-w-2xl border-white/70 bg-white/70 shadow-[0_20px_48px_-28px_rgba(15,23,42,0.1)] ring-1 ring-white/80 backdrop-blur-xl md:rounded-3xl">
            <CardContent className="space-y-4 p-6 sm:p-8">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-stretch">
                <div className="relative flex-1">
                  <Search className="pointer-events-none absolute top-1/2 right-3 size-4 -translate-y-1/2 text-zinc-400" />
                  <Input
                    readOnly
                    placeholder="שם מוצר, מותג או מילת מפתח…"
                    className="h-12 rounded-xl border-emerald-950/10 bg-white/80 pe-10 text-right shadow-inner"
                    aria-label="חיפוש מוצר (מוקאפ)"
                  />
                </div>
                <Button
                  type="button"
                  size="lg"
                  className="h-12 shrink-0 rounded-xl bg-zinc-900 text-white hover:bg-zinc-800"
                  disabled
                >
                  חיפוש
                </Button>
              </div>
              <div className="relative">
                <Barcode className="pointer-events-none absolute top-1/2 right-3 size-4 -translate-y-1/2 text-zinc-400" />
                <Input
                  readOnly
                  placeholder="7290001234567"
                  className="h-12 rounded-xl border-emerald-950/10 bg-white/80 pe-10 text-right font-mono text-sm shadow-inner"
                  aria-label="ברקוד (מוקאפ)"
                />
              </div>
              <p className="text-center text-xs text-zinc-400">
                סריקת מצלמה תתווסף בשלב מאוחר יותר.
              </p>
            </CardContent>
          </Card>
        </SectionShell>

        {/* 4 — How it works */}
        <SectionShell id="how" className="py-12 sm:py-16">
          <div className="text-center">
            <h2 className="text-2xl font-semibold tracking-tight text-zinc-950 md:text-3xl">
              איך זה עובד
            </h2>
            <p className="mx-auto mt-3 max-w-xl text-sm text-zinc-500 md:text-base">
              שלושה שלבים ממוקדים — מהזנה ועד הקשר קטגוריאלי.
            </p>
          </div>
          <div className="mt-12 grid gap-6 md:grid-cols-3 md:gap-8">
            {steps.map((s) => {
              const Icon = s.icon;
              return (
                <Card
                  key={s.step}
                  className="group border-white/70 bg-white/55 shadow-[0_16px_40px_-24px_rgba(15,23,42,0.1)] ring-1 ring-white/80 backdrop-blur-xl transition duration-300 hover:-translate-y-1 hover:bg-white/75 hover:shadow-lg md:rounded-2xl"
                >
                  <CardHeader className="space-y-4 pb-2">
                    <div className="flex items-center justify-between gap-3">
                      <span className="flex size-10 items-center justify-center rounded-2xl bg-emerald-500/12 text-sm font-bold text-emerald-800 ring-1 ring-emerald-400/25">
                        {s.step}
                      </span>
                      <span className="flex size-11 items-center justify-center rounded-2xl bg-emerald-500/10 text-emerald-700 ring-1 ring-emerald-500/15 transition group-hover:scale-105">
                        <Icon className="size-5" strokeWidth={1.65} />
                      </span>
                    </div>
                    <CardTitle className="text-lg font-semibold text-zinc-950">
                      {s.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm leading-relaxed text-zinc-600">
                    {s.body}
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </SectionShell>

        {/* 5 — Comparison preview */}
        <SectionShell id="compare" className="py-12 sm:py-16">
          <div className="text-center">
            <h2 className="text-2xl font-semibold tracking-tight text-zinc-950 md:text-3xl">
              תצוגת השוואה
            </h2>
            <p className="mx-auto mt-3 max-w-xl text-sm text-zinc-500 md:text-base">
              טבלת דמה — אותם שדות כמו במסך המוצר המלא.
            </p>
          </div>
          <Card className="mx-auto mt-10 max-w-4xl overflow-hidden border-white/70 bg-white/65 shadow-[0_24px_56px_-32px_rgba(15,23,42,0.12)] ring-1 ring-white/80 backdrop-blur-xl md:rounded-[1.75rem]">
            <CardContent className="p-0">
              <div className="overflow-x-auto">
                <table className="w-full min-w-[420px] text-right text-sm">
                  <thead>
                    <tr className="border-b border-emerald-950/[0.06] bg-emerald-50/40 text-xs font-semibold text-zinc-500">
                      <th className="px-5 py-4 font-medium">מוצר</th>
                      <th className="px-5 py-4 font-medium">ציון Bari</th>
                      <th className="px-5 py-4 font-medium">קק״ל / 100ג׳</th>
                      <th className="px-5 py-4 font-medium">נתרן</th>
                    </tr>
                  </thead>
                  <tbody>
                    {comparisonPreview.map((row, i) => (
                      <tr
                        key={row.name}
                        className={cn(
                          "border-b border-emerald-950/[0.04] transition-colors last:border-0 hover:bg-emerald-500/[0.04]",
                          i === 0 &&
                            "bg-gradient-to-l from-emerald-500/[0.08] to-transparent"
                        )}
                      >
                        <td className="px-5 py-4 font-medium text-zinc-900">
                          {row.name}
                        </td>
                        <td className="px-5 py-4 tabular-nums font-semibold text-emerald-800">
                          {row.score}
                        </td>
                        <td className="px-5 py-4 tabular-nums text-zinc-600">
                          {row.kcal}
                        </td>
                        <td className="px-5 py-4 tabular-nums text-zinc-600">
                          {row.sodium}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </SectionShell>

        {/* 6 — Methodology / trust */}
        <SectionShell className="py-12 sm:py-16">
          <div className="text-center">
            <h2 className="text-2xl font-semibold tracking-tight text-zinc-950 md:text-3xl">
              מתודולוגיה ואמון
            </h2>
            <p className="mx-auto mt-3 max-w-xl text-sm text-zinc-500 md:text-base">
              עקרונות עבודה שמניעים הצגה מטעה ושומרים על אופי אנליטי.
            </p>
          </div>
          <div className="mt-12 grid gap-6 md:grid-cols-3">
            {trustPoints.map((t) => {
              const Icon = t.icon;
              return (
                <div
                  key={t.title}
                  className="rounded-2xl border border-white/70 bg-white/50 p-6 shadow-sm ring-1 ring-emerald-950/[0.03] backdrop-blur-md transition hover:border-emerald-200/40 hover:bg-white/70 md:p-7"
                >
                  <div className="flex size-11 items-center justify-center rounded-2xl bg-emerald-500/10 text-emerald-800 ring-1 ring-emerald-400/20">
                    <Icon className="size-5" strokeWidth={1.6} />
                  </div>
                  <h3 className="mt-4 text-lg font-semibold text-zinc-950">
                    {t.title}
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-zinc-600">
                    {t.text}
                  </p>
                </div>
              );
            })}
          </div>
          <ul className="mx-auto mt-10 max-w-2xl space-y-3 text-sm text-zinc-600">
            <li className="flex gap-3 rounded-xl bg-white/40 px-4 py-3 ring-1 ring-white/60 backdrop-blur-sm">
              <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-emerald-600" />
              <span>
                Bari אינה מחליפה ייעוץ רפואי או דיאטני; היא כלי לקריאת תווית
                ולניתוח נתונים.
              </span>
            </li>
            <li className="flex gap-3 rounded-xl bg-white/40 px-4 py-3 ring-1 ring-white/60 backdrop-blur-sm">
              <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-emerald-600" />
              <span>
                ציונים ודירוגים מוצגים עם הקשר (מקור, תאריך, רמת ביטחון) כדי
                לשמור על שקיפות מול המשתמש.
              </span>
            </li>
          </ul>
        </SectionShell>

        {/* 7 — CTA */}
        <SectionShell className="pb-20 pt-4 sm:pb-28">
          <div className="relative overflow-hidden rounded-[1.75rem] border border-white/60 bg-gradient-to-bl from-emerald-600/90 via-emerald-600 to-teal-700 px-6 py-12 text-center shadow-[0_28px_56px_-24px_rgba(5,150,105,0.45)] sm:px-10 sm:py-14 md:rounded-[2rem]">
            <div className="pointer-events-none absolute -start-20 -top-20 size-64 rounded-full bg-white/15 blur-3xl" />
            <div className="pointer-events-none absolute -bottom-16 -end-16 size-56 rounded-full bg-teal-400/20 blur-3xl" />
            <div className="relative mx-auto max-w-xl space-y-4">
              <ScanLine className="mx-auto size-10 text-white/90" strokeWidth={1.5} />
              <h2 className="text-2xl font-semibold text-white md:text-3xl">
                מוכנים לבדוק מוצר?
              </h2>
              <p className="text-sm leading-relaxed text-emerald-50/95 md:text-base">
                עברו למסך הדגמה לראות פרופיל מלא: ציון, תזונה, רכיבים והשוואה —
                כולו בנתונים סטטיים לצורך עיצוב.
              </p>
              <div className="flex flex-col items-stretch justify-center gap-3 pt-4 sm:flex-row sm:justify-center">
                <Button
                  size="lg"
                  className="h-12 rounded-2xl border-0 bg-white px-8 text-sm font-semibold text-emerald-900 shadow-lg transition hover:bg-emerald-50"
                  asChild
                >
                  <Link href="/products/demo">פתיחת מוצר לדוגמה</Link>
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="h-12 rounded-2xl border-white/40 bg-white/10 px-8 text-sm font-semibold text-white backdrop-blur-sm transition hover:bg-white/20"
                  asChild
                >
                  <a href="#compare">חזרה להשוואה</a>
                </Button>
              </div>
            </div>
          </div>
        </SectionShell>

        <footer className="border-t border-emerald-950/[0.06] bg-white/30 py-8 text-center text-xs text-zinc-500 backdrop-blur-sm">
          <p>Bari — מודיעין מזון למוצרים ארוזים בישראל</p>
        </footer>
      </main>
    </div>
  );
}
