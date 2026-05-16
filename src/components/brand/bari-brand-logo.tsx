import { cn } from "@/lib/utils";

type BariBrandLogoProps = {
  className?: string;
  surface?: "light" | "dark";
};

export function BariBrandLogo({ className, surface = "light" }: BariBrandLogoProps) {
  const isDark = surface === "dark";

  return (
    <span
      className={cn(
        "inline-flex max-w-full shrink-0 items-center gap-2 rounded-full tracking-tight",
        isDark ? "text-white" : "text-zinc-950",
        className
      )}
      aria-label="Bari"
    >
      <span
        className={cn(
          "grid size-7 place-items-center rounded-full text-sm font-black leading-none",
          isDark ? "bg-white text-emerald-700" : "bg-emerald-600 text-white"
        )}
        aria-hidden
      >
        B
      </span>
      <span className="text-[1.35rem] font-extrabold leading-none">Bari</span>
      <span className={cn("mt-1 size-1.5 rounded-full", isDark ? "bg-emerald-300" : "bg-emerald-500")} aria-hidden />
    </span>
  );
}
