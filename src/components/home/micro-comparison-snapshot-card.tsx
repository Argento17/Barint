"use client";

import Image from "next/image";
import Link from "next/link";
import { ChevronLeft } from "lucide-react";

import type {
  ComparisonCard,
  EditorialArchetype,
  EditorialCard,
  HomepageCard,
} from "@/lib/home/micro-comparison-snapshots";
import { cn } from "@/lib/utils";

const CARD_SHELL =
  "group block h-full min-h-[17rem] w-[84vw] max-w-[32rem] shrink-0 snap-center rounded-[1.5rem] border border-black/[0.08] bg-[#FFFFFF] p-4 shadow-[0_20px_60px_-48px_rgba(17,19,24,0.2)] transition-[border-color,box-shadow,transform] duration-300 hover:-translate-y-0.5 hover:border-[#1F8F6A]/22 hover:shadow-[0_24px_64px_-40px_rgba(31,143,106,0.2)] sm:w-[30rem] md:min-h-[18rem] md:p-5 flex flex-col";

const ARCHETYPE_BADGE: Record<
  EditorialArchetype | "comparison",
  string
> = {
  comparison: "bg-[#E8F5EF] text-[#1F8F6A]",
  investigation: "bg-[#FEF9EC] text-[#92400E]",
  "category-report": "bg-[#F1F5F9] text-[#475569]",
  ingredient: "bg-[#F0FAFA] text-[#0E7490]",
  methodology: "bg-[#F1F5F9] text-[#475569]",
  "what-surprised-us": "bg-[#FFF1F2] text-[#9F1239]",
};

function CardHeader({
  category,
  badgeLabel,
  title,
  archetype,
}: {
  category: string;
  badgeLabel: string;
  title: string;
  archetype: EditorialArchetype | "comparison";
}) {
  return (
    <div className="flex items-start justify-between gap-3 border-b border-black/[0.05] pb-3">
      <div className="min-w-0 flex-1 text-right">
        <p className="text-xs font-bold text-[#4E5663]">{category}</p>
        <h3 className="mt-1 line-clamp-2 text-lg font-extrabold leading-tight tracking-[-0.03em] text-[#111318] md:text-xl">
          {title}
        </h3>
      </div>
      <span
        className={cn(
          "shrink-0 rounded-full px-2.5 py-1 text-[0.65rem] font-bold",
          ARCHETYPE_BADGE[archetype]
        )}
      >
        {badgeLabel}
      </span>
    </div>
  );
}

function ProductMiniColumn({
  product,
  side,
}: {
  product: ComparisonCard["leftProduct"];
  side: "left" | "right";
}) {
  return (
    <div
      className={cn(
        "flex flex-1 flex-col gap-2 rounded-xl border border-black/[0.06] bg-[#F7F7F2]/50 p-3",
        side === "right" && "bg-[#FFFFFF]"
      )}
    >
      <div className="flex items-start gap-2.5">
        <div className="relative h-14 w-10 shrink-0">
          {product.imageUrl ? (
            <Image
              src={product.imageUrl}
              alt=""
              fill
              className="object-contain"
              sizes="40px"
            />
          ) : null}
        </div>
        <div className="min-w-0 flex-1 text-right">
          <p className="text-[0.6rem] font-bold text-[#1F8F6A]">{product.brand}</p>
          <p className="line-clamp-2 text-xs font-extrabold leading-snug text-[#111318]">
            {product.name}
          </p>
        </div>
      </div>
      <div className="flex items-baseline gap-2">
        <span className="text-2xl font-extrabold tabular-nums tracking-[-0.04em] text-[#111318]">
          {product.score}
        </span>
        <span className="text-[0.65rem] font-semibold text-[#7A817C]">ציון Bari</span>
      </div>
      <ul className="space-y-1">
        {product.strengths.map((s) => (
          <li
            key={s}
            className="text-[0.65rem] font-semibold leading-snug text-[#4E5663] before:ml-1 before:text-[#1F8F6A] before:content-['·']"
          >
            {s}
          </li>
        ))}
      </ul>
    </div>
  );
}

function ComparisonCardLayout({ card }: { card: ComparisonCard }) {
  return (
    <Link href={card.href} className={CARD_SHELL}>
      <CardHeader
        category={card.category}
        badgeLabel="השוואה"
        title={card.title}
        archetype="comparison"
      />

      <div className="mt-4 flex flex-1 flex-col gap-3">
        <div className="flex items-center gap-2">
          <ProductMiniColumn product={card.leftProduct} side="left" />
          <span className="shrink-0 text-xs font-extrabold text-[#7A817C]" aria-hidden>
            מול
          </span>
          <ProductMiniColumn product={card.rightProduct} side="right" />
        </div>

        <div className="rounded-lg border-r-[3px] border-[#1F8F6A] bg-[#F7F7F2]/80 px-3 py-2.5">
          <p className="text-[0.65rem] font-bold text-[#1F8F6A]">פער מרכזי</p>
          <p className="mt-1 text-sm font-medium leading-relaxed text-[#111318]">
            {card.tradeoff}
          </p>
        </div>
      </div>

      <p className="mt-3 flex items-center justify-end gap-1 text-xs font-bold text-[#1F8F6A] opacity-80 transition-opacity group-hover:opacity-100">
        לפרטים
        <ChevronLeft className="size-3.5" aria-hidden />
      </p>
    </Link>
  );
}

function EditorialCardLayout({ card }: { card: EditorialCard }) {
  return (
    <Link href={card.href} className={CARD_SHELL}>
      <CardHeader
        category={card.category}
        badgeLabel={card.eyebrow}
        title={card.title}
        archetype={card.archetype}
      />

      <div className="mt-4 flex flex-1 flex-col gap-3">
        {card.stat ? (
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-extrabold tabular-nums tracking-[-0.04em] text-[#111318]">
              {card.stat.value}
            </span>
            <span className="text-xs font-semibold text-[#7A817C]">{card.stat.label}</span>
          </div>
        ) : null}

        <div className="rounded-lg border-r-[3px] border-[#1F8F6A] bg-[#F7F7F2]/80 px-3 py-2.5">
          <p className="text-sm font-semibold leading-relaxed text-[#111318]">
            {card.finding}
          </p>
        </div>

        {card.context ? (
          <p className="text-xs text-[#7A817C]">{card.context}</p>
        ) : null}
      </div>

      <p className="mt-3 flex items-center justify-end gap-1 text-xs font-bold text-[#1F8F6A] opacity-80 transition-opacity group-hover:opacity-100">
        לפרטים
        <ChevronLeft className="size-3.5" aria-hidden />
      </p>
    </Link>
  );
}

export function HomepageCardItem({ card }: { card: HomepageCard }) {
  if (card.archetype === "comparison") {
    return <ComparisonCardLayout card={card} />;
  }
  return <EditorialCardLayout card={card} />;
}
