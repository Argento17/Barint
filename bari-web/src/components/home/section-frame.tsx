import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

export function HomeContainer({
  className,
  children,
}: {
  className?: string;
  children: ReactNode;
}) {
  return <div className={cn("mx-auto max-w-7xl px-5 sm:px-6", className)}>{children}</div>;
}

export function SectionHeading({
  eyebrow,
  title,
  description,
  align = "center",
  tone = "default",
}: {
  eyebrow?: string;
  title: string;
  description?: string;
  align?: "center" | "start";
  tone?: "default" | "inverted";
}) {
  const isInverted = tone === "inverted";
  return (
    <div
      className={cn(
        "mb-10 space-y-3 md:mb-12",
        align === "center" ? "mx-auto max-w-3xl text-center" : "text-right"
      )}
    >
      {eyebrow ? (
        <p
          className={cn(
            "text-xs font-semibold tracking-wide",
            isInverted ? "text-[#1F8F6A]" : "text-[#2FAE82]"
          )}
        >
          {eyebrow}
        </p>
      ) : null}
      <h2
        className={cn(
          "text-balance text-3xl font-bold tracking-tight md:text-4xl lg:text-5xl",
          isInverted ? "text-[#111318]" : "text-[#111318]"
        )}
      >
        {title}
      </h2>
      {description ? (
        <p
          className={cn(
            "text-pretty text-base md:text-lg",
            isInverted ? "text-[#4E5663]" : "text-[#4E5663]"
          )}
        >
          {description}
        </p>
      ) : null}
    </div>
  );
}
