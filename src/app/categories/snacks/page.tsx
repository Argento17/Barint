import type { Metadata } from "next";
import Link from "next/link";
import {
  BarChart3,
  ChevronLeft,
  Cookie,
  Layers3,
  Scale,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import { HomeContainer } from "@/components/home/section-frame";
import { cn } from "@/lib/utils";
import { siteHeaderOffsetClass } from "@/lib/site-layout";

export const metadata: Metadata = {
  title: "השוואות חטיפים | Bari",
  description:
    "ניתוח חטיפים לפי רכיבים, סוכר, עיבוד, תוספים, חלבון ושובע ביחס לקטגוריה.",
};

const categorySignals = [
  { label: "שונות בין מותגים", value: 78 },
  { label: "עומס עיבוד", value: 82 },
  { label: "פערי סוכר", value: 69 },
  { label: "תוספים נפוצים", value: 74 },
] as const;

const products = [
  {
    label: "מוצר A",
    name: "חטיף עדשים אפוי",
    position: "פרופיל חזק יותר בקטגוריה",
    summary:
      "לא בגלל שהוא “בריא” באופן מוחלט, אלא כי הוא מציג יחס טוב יותר בין רכיבים מזוהים, חלבון ושובע מול עומס עיבוד מתון.",
    score: "82",
    facts: ["סוכר נמוך יחסית", "מקור חלבון ברור", "רשימת רכיבים קצרה יותר"],
    signals: [
      { label: "סוכר", value: 72, note: "נמוך יותר ביחס לחטיפים דומים" },
      { label: "עיבוד", value: 63, note: "עדיין מעובד, אך פחות מורכב" },
      { label: "תוספים", value: 70, note: "פחות רכיבי עזר ומייצבים" },
      { label: "חלבון", value: 66, note: "תורם לשובע ולפרופיל תזונתי" },
      { label: "פשטות רכיבים", value: 78, note: "רכיבים מזוהים יותר" },
      { label: "שובע", value: 61, note: "חלבון וסיבים משפרים הקשר" },
    ],
  },
  {
    label: "מוצר B",
    name: "חטיף תירס בטעם גבינה",
    position: "פרופיל חלש יותר בקטגוריה",
    summary:
      "הפער נוצר בעיקר ממורכבות רכיבים, תיבול ותוספים. הוא לא “נפסל”, אבל דורש קריאה ביקורתית יותר מול חלופות.",
    score: "58",
    facts: ["יותר רכיבי טעם", "פחות חלבון", "עיבוד מורגש יותר"],
    signals: [
      { label: "סוכר", value: 44, note: "לא בהכרח גבוה, אך אינו היתרון המרכזי" },
      { label: "עיבוד", value: 38, note: "יותר סימני עיבוד ותיבול" },
      { label: "תוספים", value: 35, note: "רשימה מורכבת יותר" },
      { label: "חלבון", value: 28, note: "תרומה נמוכה לשובע" },
      { label: "פשטות רכיבים", value: 41, note: "פחות שקיפות רכיבית" },
      { label: "שובע", value: 34, note: "קל לצריכה עודפת ביחס לערך" },
    ],
  },
] as const;

const rationale = [
  {
    icon: Scale,
    title: "ההשוואה קטגורית",
    text: "Bari לא משווה חטיף ליוגורט או לארוחה מלאה. הסרגל הוא חטיפים דומים במדף.",
  },
  {
    icon: Layers3,
    title: "הפער אינו נתון אחד",
    text: "הדירוג משתנה בגלל שילוב של סוכר, חלבון, תוספים, עיבוד ושובע, לא בגלל קלוריה בודדת.",
  },
  {
    icon: ShieldCheck,
    title: "הסבר לפני מסקנה",
    text: "המטרה היא להבין למה מוצר מתנהג אחרת, ולא להדביק לו תווית ירוקה או אדומה.",
  },
] as const;

function SignalBar({ label, value, note }: { label: string; value: number; note?: string }) {
  return (
    <div>
      <div className="mb-2 flex items-center justify-between gap-4 text-sm">
        <span className="font-bold text-zinc-900">{label}</span>
        <span className="font-semibold text-zinc-500">{value}</span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-stone-200/80 shadow-inner shadow-zinc-950/[0.03]">
        <div className="h-full rounded-full bg-zinc-900" style={{ width: `${value}%` }} />
      </div>
      {note ? <p className="mt-2 text-xs leading-relaxed text-zinc-500">{note}</p> : null}
    </div>
  );
}

function ProductPanel({ product, highlighted = false }: { product: (typeof products)[number]; highlighted?: boolean }) {
  return (
    <article
      className={cn(
        "flex min-h-full flex-col rounded-[1.6rem] border bg-white p-5 shadow-sm shadow-zinc-950/[0.03] md:p-6",
        highlighted ? "border-emerald-900/18" : "border-stone-200/80"
      )}
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.18em] text-zinc-500">{product.label}</p>
          <h2 className="mt-2 text-2xl font-extrabold tracking-[-0.04em] text-zinc-950">{product.name}</h2>
          <p className="mt-2 text-sm font-bold text-emerald-900">{product.position}</p>
        </div>
        <div className="rounded-2xl border border-stone-200/80 bg-stone-50 px-4 py-3 text-center">
          <div className="text-2xl font-extrabold tracking-[-0.05em] text-zinc-950">{product.score}</div>
          <div className="text-[0.65rem] font-bold uppercase tracking-[0.16em] text-zinc-400">יחסי</div>
        </div>
      </div>

      <p className="mt-5 text-sm leading-relaxed text-zinc-600">{product.summary}</p>

      <div className="mt-5 flex flex-wrap gap-2">
        {product.facts.map((fact) => (
          <span
            key={fact}
            className="rounded-full border border-stone-200/80 bg-stone-50 px-3 py-1 text-xs font-semibold text-zinc-600"
          >
            {fact}
          </span>
        ))}
      </div>

      <div className="mt-7 space-y-5">
        {product.signals.map((signal) => (
          <SignalBar key={signal.label} label={signal.label} value={signal.value} note={signal.note} />
        ))}
      </div>
    </article>
  );
}

export default function SnacksCategoryPage() {
  return (
    <main className={cn("relative overflow-hidden bg-[#f7f8f6] text-zinc-900", siteHeaderOffsetClass)}>
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-[34rem] bg-[radial-gradient(circle_at_80%_5%,rgba(4,120,87,0.11),transparent_34%),linear-gradient(to_bottom,rgba(255,255,255,0.92),rgba(247,248,246,0))]"
        aria-hidden
      />

      <HomeContainer className="relative py-16 md:py-24">
        <section className="grid gap-10 lg:grid-cols-[minmax(0,1fr)_22rem] lg:items-end">
          <div className="max-w-4xl">
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-emerald-900/10 bg-white/70 px-4 py-2 text-sm font-bold text-emerald-950 shadow-sm shadow-zinc-950/[0.03] backdrop-blur-sm">
              <Cookie className="size-4" aria-hidden />
              השוואות חטיפים
            </div>
            <h1 className="text-balance text-4xl font-extrabold leading-[1.05] tracking-[-0.055em] text-zinc-950 md:text-6xl">
              חטיפים נמדדים לפי דפוס, לא לפי רושם.
            </h1>
            <p className="mt-6 max-w-2xl text-pretty text-lg leading-relaxed text-zinc-600">
              Bari מנתח חטיפים דרך רכיבים, סוכר, עיבוד, תוספים, חלבון ושובע, ואז משווה אותם
              לציפיות של קטגוריית החטיפים עצמה.
            </p>
          </div>

          <div className="rounded-[1.5rem] border border-stone-200/80 bg-white/75 p-5 shadow-sm shadow-zinc-950/[0.03] backdrop-blur-sm">
            <div className="mb-5 flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-[0.18em] text-zinc-500">Category profile</span>
              <Sparkles className="size-4 text-emerald-800" aria-hidden />
            </div>
            <div className="space-y-4">
              {categorySignals.map((signal) => (
                <SignalBar key={signal.label} label={signal.label} value={signal.value} />
              ))}
            </div>
          </div>
        </section>

        <section className="mt-14 rounded-[2rem] border border-stone-200/80 bg-white/82 p-4 shadow-[0_28px_90px_-64px_rgba(24,24,27,0.55)] backdrop-blur-sm md:p-6">
          <div className="mb-6 flex flex-col justify-between gap-4 md:flex-row md:items-end">
            <div className="max-w-2xl">
              <p className="text-xs font-bold uppercase tracking-[0.2em] text-emerald-900">Side-by-side analysis</p>
              <h2 className="mt-2 text-3xl font-extrabold tracking-[-0.045em] text-zinc-950 md:text-4xl">
                למה שני חטיפים דומים מקבלים פרופיל שונה?
              </h2>
              <p className="mt-3 text-sm leading-relaxed text-zinc-600 md:text-base">
                הדוגמה מדגימה דירוג יחסי. מוצר A אינו “אידיאלי”, ומוצר B אינו “אסור”, אבל האותות
                מראים הבדל ברור באיכות ההרכב וביכולת השובע.
              </p>
            </div>
            <div className="flex items-center gap-2 rounded-full border border-stone-200/80 bg-stone-50 px-4 py-2 text-sm font-bold text-zinc-600">
              <BarChart3 className="size-4 text-emerald-800" aria-hidden />
              מבוסס אותות קטגוריים
            </div>
          </div>

          <div className="grid gap-4 lg:grid-cols-2">
            <ProductPanel product={products[0]} highlighted />
            <ProductPanel product={products[1]} />
          </div>
        </section>

        <section className="mt-8 grid gap-4 md:grid-cols-3">
          {rationale.map((item) => {
            const Icon = item.icon;

            return (
              <div key={item.title} className="rounded-[1.5rem] border border-stone-200/80 bg-white/78 p-5 shadow-sm shadow-zinc-950/[0.025]">
                <Icon className="mb-4 size-5 text-emerald-900" aria-hidden />
                <h3 className="text-lg font-extrabold tracking-[-0.035em] text-zinc-950">{item.title}</h3>
                <p className="mt-3 text-sm leading-relaxed text-zinc-600">{item.text}</p>
              </div>
            );
          })}
        </section>

        <section className="mt-8 rounded-[1.5rem] border border-emerald-900/10 bg-emerald-50/45 p-5 text-sm leading-relaxed text-emerald-950 md:p-6">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <p>
              בדף אמיתי, הערכים יוזנו ממסד נתוני מוצרים ותוויות. כרגע זו דוגמת UX שמראה איך Bari
              מסביר הבדלים בתוך קטגוריה בלי להפוך אותם לפסק דין פשטני.
            </p>
            <Link href="/#categories" className="inline-flex shrink-0 items-center gap-1 font-bold text-emerald-900">
              חזרה לתחומי הניתוח
              <ChevronLeft className="size-4" aria-hidden />
            </Link>
          </div>
        </section>
      </HomeContainer>
    </main>
  );
}
