"use client";

import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

import { HomeFooter } from "@/components/home/home-footer";
import { SiteHeader } from "@/components/site-header";
import { ConsentManager } from "@/components/shared/consent-manager";
import { GA4Script } from "@/components/shared/ga4-script";
import { VercelAnalytics } from "@/components/shared/vercel-analytics";
import { SiteStructuredData } from "@/components/seo/site-structured-data";

/** Keeps internal tools outside consumer chrome without changing public routes. */
export function InternalRouteFrame({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  if (pathname.startsWith("/internal/")) return <>{children}</>;

  return (
    <>
      <SiteHeader />
      <main id="main-content" className="flex-1">{children}</main>
      <HomeFooter />
      <ConsentManager />
      <GA4Script />
      <VercelAnalytics />
      <SiteStructuredData />
    </>
  );
}
