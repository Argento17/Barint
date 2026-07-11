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
            <span className="text-sm font-medium text-neutral-800">{label}</span>
            <CheckStatusBadge status={check.status} label={check.status.toUpperCase()} />
          </div>
          {check.reason ? <p className="text-xs text-neutral-500">{check.reason}</p> : null}
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
