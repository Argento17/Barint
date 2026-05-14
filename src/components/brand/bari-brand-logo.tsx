import { cn } from "@/lib/utils";

type BariBrandLogoProps = {
  className?: string;
  surface?: "light" | "dark";
};

export function BariBrandLogo({ className, surface = "light" }: BariBrandLogoProps) {
  const logo = <img src="/logo-bari.png" alt="Bari" className="h-10 w-auto" />;

  if (surface === "dark") {
    return (
      <div
        className={cn(
          "inline-flex w-fit max-w-full shrink-0 items-center rounded-xl bg-white/95 px-3 py-2 shadow-sm ring-1 ring-white/10",
          className
        )}
      >
        {logo}
      </div>
    );
  }

  return <div className={cn("inline-flex max-w-full shrink-0 items-center", className)}>{logo}</div>;
}
