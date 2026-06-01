"use client";

import { createContext, useContext, type ReactNode } from "react";

/** `shelf` = frozen mobile phone-frame (Maadanim, Bread). `web` = responsive web template (Snacks+). */
export type ComparisonLayoutMode = "shelf" | "web";

const ComparisonLayoutContext = createContext<ComparisonLayoutMode>("shelf");

export function ComparisonLayoutProvider({
  mode,
  children,
}: {
  mode: ComparisonLayoutMode;
  children: ReactNode;
}) {
  return (
    <ComparisonLayoutContext.Provider value={mode}>{children}</ComparisonLayoutContext.Provider>
  );
}

export function useComparisonLayout(): ComparisonLayoutMode {
  return useContext(ComparisonLayoutContext);
}
