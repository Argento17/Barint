"use client";

import Link from "next/link";

import { GLASSBOX_W5_ON } from "@/lib/feature-flags";
import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";

// TASK-181Q: `glassBoxMethodologyLink` prop — when provided AND NEXT_PUBLIC_GLASSBOX_W5=on,
// appends an inline "פירוט המתודולוגיה" link to the last paragraph. When the flag is OFF
// the footer is byte-identical to HEAD regardless of the prop value.

export function MethodologyFooter({
  lines,
  wide = false,
  glassBoxMethodologyLink = false,
}: {
  lines: string[];
  wide?: boolean;
  /** When true + GLASSBOX_W5_ON, appends an inline link to /research/glass-box on the last line. */
  glassBoxMethodologyLink?: boolean;
}) {
  const showMethodologyLink = glassBoxMethodologyLink && GLASSBOX_W5_ON;

  return (
    <footer
      className={cn("px-4 pt-4 pb-6", wide && cn(comparisonWebSectionPaddingClass(), "lg:pb-8 lg:pt-3"))}
    >
      <div className="space-y-1.5">
        {lines.map((line, index) => {
          const isLast = index === lines.length - 1;
          return (
            <p key={`${index}-${line.slice(0, 14)}`} className="text-[11px] leading-relaxed text-[#8A908B]">
              {line}
              {isLast && showMethodologyLink && (
                <>
                  {" "}
                  <Link
                    href="/research/glass-box"
                    className="text-[#1F8F6A] underline underline-offset-2"
                  >
                    פירוט המתודולוגיה
                  </Link>
                </>
              )}
            </p>
          );
        })}
      </div>
    </footer>
  );
}
