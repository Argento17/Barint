import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Bari — Product Dossier (internal)",
  robots: { index: false, follow: false },
};

export default function InternalLayout({ children }: { children: ReactNode }) {
  return (
    <div dir="ltr" lang="en" className="min-h-screen bg-white text-neutral-900">
      <header className="border-b border-neutral-200 bg-neutral-50 px-4 py-3">
        <div className="mx-auto max-w-6xl text-sm font-semibold">Bari — Product Dossier (internal)</div>
      </header>
      {children}
    </div>
  );
}
