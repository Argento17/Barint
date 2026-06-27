import type { ReactNode } from "react";
import { Clock } from "lucide-react";

import { cn } from "@/lib/utils";

export function HashvaotCategoryGroupHeader({
  title,
  countLabel,
}: {
  title: string;
  countLabel?: string;
}) {
  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
        <h2 className="text-sm font-bold uppercase tracking-[0.18em] text-[#7A817C]">
          {title}
        </h2>
        {countLabel ? (
          <span className="rounded-full border border-[#7A817C]/25 bg-white/60 px-2.5 py-0.5 text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-[#7A817C]">
            {countLabel}
          </span>
        ) : null}
      </div>
      <hr className="border-0 border-t border-[#E8E6DF]" />
    </div>
  );
}

export function HashvaotComingSoonTray({
  title,
  subtext,
  ariaLabel,
}: {
  title: string;
  subtext: string;
  ariaLabel: string;
}) {
  return (
    <div
      role="status"
      aria-label={ariaLabel}
      className="flex min-h-[5rem] cursor-default items-center gap-4 rounded-[1.35rem] border border-dashed border-[#7A817C]/30 bg-white/40 px-5 py-4 opacity-[0.62]"
    >
      <Clock className="size-5 shrink-0 text-[#7A817C]" aria-hidden />
      <div className="min-w-0">
        <div className="flex flex-wrap items-center gap-2">
          <p className="text-sm font-semibold text-[#4E5663]">{title}</p>
          <span className="rounded-full border border-[#7A817C]/30 px-3 py-1 text-[0.7rem] font-semibold text-[#7A817C]">
            בבנייה
          </span>
        </div>
        <p className="mt-1 text-pretty text-sm leading-relaxed text-[#7A817C]">{subtext}</p>
      </div>
    </div>
  );
}

export function HashvaotGroupSection({
  title,
  countLabel,
  intro,
  status,
  comingSoon,
  children,
  className,
  sectionId,
}: {
  title: string;
  countLabel?: string;
  intro?: ReactNode;
  status: "live" | "building";
  comingSoon?: { subtext: string; ariaLabel: string };
  children?: ReactNode;
  className?: string;
  sectionId: string;
}) {
  return (
    <section className={cn("mt-12 space-y-6", className)} aria-labelledby={sectionId}>
      <div id={sectionId}>
        <HashvaotCategoryGroupHeader title={title} countLabel={countLabel} />
      </div>
      {intro}
      {status === "building" && comingSoon ? (
        <HashvaotComingSoonTray
          title={title}
          subtext={comingSoon.subtext}
          ariaLabel={comingSoon.ariaLabel}
        />
      ) : (
        children
      )}
    </section>
  );
}

export function HashvaotComparisonCardGrid({
  lead,
  children,
}: {
  lead?: ReactNode;
  children: ReactNode;
}) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      {lead ? <div className="space-y-6 lg:col-span-2">{lead}</div> : null}
      {children}
    </div>
  );
}
