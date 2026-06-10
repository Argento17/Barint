import Image from "next/image";

import { cn } from "@/lib/utils";

type BariBrandLogoProps = {
  className?: string;
  surface?: "light" | "dark";
  mark?: boolean;
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
export function BariBrandLogo({ className, surface = "light", mark = true }: BariBrandLogoProps) {
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
        className="h-[44px] w-auto transition-opacity duration-500 ease-out group-hover:opacity-85"
      />
    </span>
  );
}
