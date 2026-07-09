import type { Metadata } from "next";
import { Geist, Geist_Mono, Inter } from "next/font/google";
import "./globals.css";
import { SiteHeader } from "@/components/site-header";
import { HomeFooter } from "@/components/home/home-footer";
import { ConsentManager } from "@/components/shared/consent-manager";
import { GA4Script } from "@/components/shared/ga4-script";
import { VercelAnalytics } from "@/components/shared/vercel-analytics";
import { SiteStructuredData } from "@/components/seo/site-structured-data";
import { SITE_URL } from "@/lib/site-url";
import { cn } from "@/lib/utils";

const inter = Inter({subsets:['latin'],variable:'--font-sans'});

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: "Bari — אינטליגנציית מזון ישראלית",
  description:
    "אינטליגנציית מזון ישראלית: אלגוריתמים, דירוגים והשוואות שקופות שמבוססות על נתונים.",
  // Self-referential canonical, resolved per-route against metadataBase
  // (e.g. /hashvaot/hummus → https://bari.digital/hashvaot/hummus). Inherited
  // by every page that does not set its own `alternates`.
  alternates: { canonical: "./" },
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true },
  },
  openGraph: {
    title: "Bari — אינטליגנציית מזון ישראלית",
    description:
      "אינטליגנציית מזון ישראלית: אלגוריתמים, דירוגים והשוואות שקופות שמבוססות על נתונים.",
    locale: "he_IL",
    type: "website",
    images: [{ url: "/bari-logo-optimized.png", width: 512, height: 512 }],
  },
  twitter: {
    card: "summary",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="he"
      dir="rtl"
      className={cn("h-full scroll-smooth", "antialiased", geistSans.variable, geistMono.variable, "font-sans", inter.variable)}
    >
      <body className="min-h-full flex flex-col">
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:absolute focus:right-4 focus:top-4 focus:z-[100] focus:rounded-lg focus:bg-[#167A58] focus:px-4 focus:py-2 focus:text-[13px] focus:font-semibold focus:text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          דלג לתוכן ראשי
        </a>
        <SiteHeader />
        <main id="main-content" className="flex-1">
          {children}
        </main>
        <HomeFooter />
        <ConsentManager />
        <GA4Script />
        <VercelAnalytics />
        <SiteStructuredData />
      </body>
    </html>
  );
}
