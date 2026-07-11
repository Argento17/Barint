import type { ReactNode } from "react";

/** Utilitarian internal-tool shell — same neutral house style as /admin
 * (src/app/admin/page.tsx's Shell), not the consumer design system. RTL Hebrew.
 */
export function Shell({ children, wide }: { children: ReactNode; wide?: boolean }) {
  return (
    <div dir="rtl" lang="he" className="min-h-screen bg-white px-4 py-8 text-neutral-900">
      <div className={wide ? "mx-auto max-w-6xl" : "mx-auto max-w-4xl"}>{children}</div>
    </div>
  );
}
