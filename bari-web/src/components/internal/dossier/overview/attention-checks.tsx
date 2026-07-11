"use client";

import { useState } from "react";

import { deriveAttentionChecks } from "@/lib/dossier/overview-derive";
import { LAYER4_CHECK_LABEL } from "@/lib/dossier/overview-labels";
import type { Layer4Checks } from "@/lib/dossier/types";
import { CheckStatusBadge } from "@/components/internal/dossier/status-badge";

// Overview §F — Checks needing attention (TASK-620 / PD-3.1). Shows only
// layer_4 checks with status fail/warn/unknown; passed checks collapse behind
// a "X other checks passed" disclosure rather than being hidden entirely.
export function AttentionChecks({ layer4 }: { layer4: Layer4Checks }) {
  const { attention, passedCount } = deriveAttentionChecks(layer4);
  const [showPassed, setShowPassed] = useState(false);

  if (attention.length === 0) {
    return (
      <div className="rounded-md border border-emerald-200 bg-emerald-50/60 p-3 text-sm text-emerald-800">
        All {passedCount} checks passed.
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {attention.map(({ id, label, check }) => (
        <div key={id} className="rounded-md border border-neutral-200 p-3">
          <div className="mb-1 flex items-center justify-between">
            <span className="text-sm font-medium text-neutral-800">{humanAction(id, label)}</span>
            <CheckStatusBadge status={check.status} label={check.status.toUpperCase()} />
          </div>
          <p className="text-xs text-neutral-500">{humanExplanation(id, check.status)}</p>
        </div>
      ))}

      {passedCount > 0 && (
        <button
          type="button"
          onClick={() => setShowPassed((v) => !v)}
          className="text-xs font-medium text-neutral-400 underline"
        >
          {showPassed ? "Hide passed checks" : `${passedCount} other check${passedCount === 1 ? "" : "s"} passed`}
        </button>
      )}

      {showPassed && (
        <div className="space-y-1 text-xs text-neutral-500">
          {(Object.keys(layer4) as Array<keyof Layer4Checks>)
            .filter((id) => layer4[id].status === "pass")
            .map((id) => (
              <div key={id} className="flex items-center justify-between rounded-md border border-neutral-100 px-3 py-1.5">
                <span>{LAYER4_CHECK_LABEL[id] ?? id}</span>
                <CheckStatusBadge status="pass" label="PASS" />
              </div>
            ))}
        </div>
      )}
    </div>
  );
}

function humanAction(id: keyof Layer4Checks, fallback: string): string {
  return ({ barcode: "Review barcode identity", source_traceability: "Review source traceability", calculation: "Review score reproducibility", publishability: "Review publication record" } as const)[id] ?? fallback;
}

function humanExplanation(id: keyof Layer4Checks, status: string): string {
  const detail = ({ barcode: "This product may share or conflict with another barcode-derived record.", source_traceability: "The source evidence does not yet provide a complete traceable record.", calculation: "The published score is not fully reproduced by the available trace data.", publishability: "The diagnostic publication checks need review before relying on this record." } as const)[id];
  return status === "unknown" ? `${detail} The check outcome is currently unavailable.` : detail;
}
