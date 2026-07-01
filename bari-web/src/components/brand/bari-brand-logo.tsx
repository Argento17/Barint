import Image from "next/image";

import { cn } from "@/lib/utils";

type BariBrandLogoProps = {
  className?: string;
  surface?: "light" | "dark";
  mark?: boolean;
  /** Override the default logo height (e.g. "h-[56px]"). Defaults to h-[44px]. */
  imgClassName?: string;
};

/** Icon-only mark — used in small badge contexts (e.g. hero badge). */
export function BariSignalMark({
  className,
  surface = "light",
}: {
  className?: string;
  surface?: "light" | "dark";
}) {
  // surface kept in signature for API compatibility; icon PNG is always the same asset
  void surface;
  return (
    <Image
      src="/bari-icon-optimized.webp"
      alt="Bari icon"
      width={62}
      height={64}
      className={cn(
        "shrink-0 transition-[opacity,transform] duration-500 ease-out group-hover:scale-[1.03] group-hover:opacity-90",
        className
      )}
      aria-hidden
    />
  );
}

/** Full wordmark + icon logo — used in navbar, footer, and mobile sheet. */
export function BariBrandLogo({ className, surface = "light", mark = true, imgClassName }: BariBrandLogoProps) {
  // surface and mark kept for API compatibility; full logo PNG already contains both
  void surface;
  void mark;
  return (
    <span
      className={cn("inline-flex shrink-0 items-center rounded-full", className)}
      aria-label="Bari"
    >
      <Image
        src="/bari-logo-optimized.webp"
        alt="Bari"
        width={180}
        height={88}
        priority
        className={cn(
          "w-auto transition-opacity duration-500 ease-out group-hover:opacity-85",
          imgClassName ?? "h-[44px]"
        )}
      />
    </span>
  );
}
