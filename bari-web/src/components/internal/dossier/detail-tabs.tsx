"use client";

import { useState, type ReactNode } from "react";

type TabId = "overview" | "evidence" | "technical";

const TABS: { id: TabId; label: string }[] = [
  { id: "overview", label: "Overview" },
  { id: "evidence", label: "Evidence" },
  { id: "technical", label: "Technical audit" },
];

/**
 * Client-side tab switch for the dossier detail page (TASK-620 / PD-3.1).
 * The page itself stays a Server Component that reads the dossier + resolves
 * the verdict; each tab's content is built server-side and passed in as a
 * ReactNode prop, so this wrapper only owns which one is visible. Overview is
 * the default per spec.
 */
export function DetailTabs({
  overview,
  evidence,
  technical,
}: {
  overview: ReactNode;
  evidence: ReactNode;
  technical: ReactNode;
}) {
  const [active, setActive] = useState<TabId>("overview");

  const content: Record<TabId, ReactNode> = { overview, evidence, technical };

  return (
    <div>
      <div dir="ltr" lang="en" className="mb-4 flex gap-1 border-b border-neutral-200">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            type="button"
            role="tab"
            aria-selected={active === tab.id}
            onClick={() => setActive(tab.id)}
            className={`-mb-px border-b-2 px-3 py-2 text-sm font-medium transition-colors ${
              active === tab.id
                ? "border-emerald-700 text-emerald-800"
                : "border-transparent text-neutral-400 hover:text-neutral-600"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div role="tabpanel">{content[active]}</div>
    </div>
  );
}
