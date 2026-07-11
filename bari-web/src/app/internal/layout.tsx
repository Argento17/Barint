import type { Metadata } from "next";
import type { ReactNode } from "react";

// Internal diagnostic tools only (TASK-611 / PD-3 and any future additions
// under /internal). Never indexed, never linked from consumer nav/sitemap —
// same noindex pattern as src/app/admin/layout.tsx.
export const metadata: Metadata = {
  title: "Bari — כלים פנימיים",
  robots: { index: false, follow: false },
};

export default function InternalLayout({ children }: { children: ReactNode }) {
  return children;
}
