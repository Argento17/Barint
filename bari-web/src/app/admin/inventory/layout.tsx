/**
 * /admin/inventory layout — suppresses the root SiteHeader and HomeFooter so the
 * navy AppShell is the sole chrome for the inventory dashboard (mirrors the
 * /catalog layout). Other admin routes (login, copy editor) keep the normal
 * site header via the parent admin layout — only this dashboard route is full-bleed.
 *
 * The root layout.tsx renders <SiteHeader /> and <HomeFooter /> as direct children
 * of <body>; a scoped <style> hides those top-level elements only while this route
 * is mounted. `body > header` / `body > footer` never matches the AppShell's own
 * <header> (it is nested, not a direct child of body).
 */

import type { ReactNode } from "react";

export default function InventoryDashboardLayout({ children }: { children: ReactNode }) {
  return (
    <>
      <style>{`
        body > header,
        body > footer {
          display: none !important;
        }
      `}</style>
      {children}
    </>
  );
}
