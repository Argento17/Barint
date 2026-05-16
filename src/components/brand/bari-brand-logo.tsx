import { cn } from "@/lib/utils";

type BariBrandLogoProps = {
  className?: string;
  surface?: "light" | "dark";
  mark?: boolean;
};

export function BariSignalMark({
  className,
  surface = "light",
}: {
  className?: string;
  surface?: "light" | "dark";
}) {
  const isDark = surface === "dark";

  return (
    <svg
      viewBox="0 0 48 48"
      className={cn(
        "size-8 shrink-0 transition-[opacity,transform] duration-500 ease-out group-hover:scale-[1.03] group-hover:opacity-90",
        isDark ? "text-white" : "text-zinc-950",
        className
      )}
      fill="none"
      aria-hidden
    >
      <g stroke="currentColor" strokeLinecap="round" strokeWidth="3.2">
        <path d="M16 16h16" />
        <path d="M12 24h24" />
        <path d="M16 32h16" />
      </g>
      <g fill="currentColor">
        <circle cx="24" cy="8" r="2.7" />
        <circle cx="16" cy="16" r="2.35" />
        <circle cx="32" cy="16" r="2.35" />
        <circle cx="12" cy="24" r="2.35" />
        <circle cx="36" cy="24" r="2.35" />
        <circle cx="16" cy="32" r="2.35" />
        <circle cx="32" cy="32" r="2.35" />
        <circle cx="24" cy="40" r="2.7" />
      </g>
      <g className={isDark ? "fill-emerald-300" : "fill-emerald-700"}>
        <circle cx="24" cy="16" r="2.45" />
        <circle cx="24" cy="24" r="2.65" />
        <circle cx="24" cy="32" r="2.45" />
      </g>
      <path
        d="M24 16v16"
        className={isDark ? "stroke-emerald-300" : "stroke-emerald-700"}
        strokeLinecap="round"
        strokeWidth="3.2"
      />
    </svg>
  );
}

export function BariBrandLogo({ className, surface = "light", mark = true }: BariBrandLogoProps) {
  const isDark = surface === "dark";

  return (
    <span
      className={cn(
        "inline-flex max-w-full shrink-0 items-center gap-2.5 rounded-full",
        isDark ? "text-white" : "text-zinc-950",
        className
      )}
      aria-label="Bari"
    >
      {mark ? <BariSignalMark surface={surface} /> : null}
      <span
        className="text-[1.76rem] font-extrabold leading-none tracking-[-0.065em] transition-opacity duration-500 ease-out group-hover:opacity-85"
        aria-hidden
      >
        Bari
      </span>
    </span>
  );
}
