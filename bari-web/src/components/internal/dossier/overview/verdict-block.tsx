"use client";

import { useCallback, useState } from "react";

import { ComparisonRow } from "@/components/shared/comparison-row";
import {
  deriveVerificationState,
  VERIFICATION_STATE_DESCRIPTION,
  VERIFICATION_STATE_LABEL,
  type VerificationState,
} from "@/lib/dossier/overview-derive";
import type { Layer4Check } from "@/lib/dossier/types";
import type { VerdictResolution } from "@/lib/dossier/verdict";
import { cn } from "@/lib/utils";

// Overview §B — Bari verdict (TASK-620 / PD-3.1). Renders the REAL, canonical
// <ComparisonRow> (the "VerdictRow") against the real BariProductVM resolved by
// resolveVerdict() (owner decision, Option A thin adapter) — never an invented
// verdict, never a new verdict system. When there is no live-shelf match, this
// shows an honest fallback instead. The verification badge is styled distinctly
// per state so "estimated" can never be mistaken for "verified" (spec hard rule).
const BADGE_STYLE: Record<VerificationState, string> = {
  verified: "border-emerald-200 bg-emerald-50 text-emerald-800",
  estimated: "border-amber-200 bg-amber-50 text-amber-800",
  mismatched: "border-red-200 bg-red-50 text-red-800",
  untraceable: "border-neutral-200 bg-neutral-100 text-neutral-500",
};

export function VerdictBlock({
  verdict,
  calculationCheck,
}: {
  verdict: VerdictResolution;
  calculationCheck: Layer4Check;
}) {
  const [open, setOpen] = useState(false);
  const registerRow = useCallback(() => {}, []);
  const onToggle = useCallback(() => setOpen((v) => !v), []);

  const confidence = verdict.status === "matched" ? verdict.product.confidence : null;
  const state = deriveVerificationState(calculationCheck, confidence);

  return (
    <div className="rounded-md border border-neutral-200 p-4">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <h2 className="text-sm font-semibold text-neutral-700">Bari verdict</h2>
        <span
          className={cn(
            "inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-semibold",
            BADGE_STYLE[state],
          )}
          title={VERIFICATION_STATE_DESCRIPTION[state]}
        >
          {VERIFICATION_STATE_LABEL[state]}
        </span>
      </div>

      {verdict.status === "matched" ? (
        // ComparisonRow assumes an RTL ancestor (logical start/end props, Hebrew
        // content) — the Overview tab around this block is dir="ltr" (English UI),
        // so this subtree restores dir="rtl" locally rather than letting a
        // mismatched ancestor direction mirror the row's geometry (see
        // visual_bugs_image_read_not_geometry lesson: dir must match physically).
        <div className="bari-cmp-workspace" dir="rtl" lang="he">
          <div className="bari-cmp-scroll bari-cmp-scroll--nometric overflow-hidden rounded-md border border-neutral-100">
            <ComparisonRow
              product={verdict.product}
              rank={0}
              open={open}
              onToggle={onToggle}
              metricSpecs={[]}
              registerRow={registerRow}
              category={verdict.categorySlug}
            />
          </div>
        </div>
      ) : (
        <div className="rounded-md bg-amber-50 px-3 py-2.5 text-sm text-amber-800">
          <p className="font-medium">No published verdict — not on a live comparison shelf.</p>
          <p className="mt-1 text-xs text-amber-700">{verdict.reason}</p>
        </div>
      )}

      <p className="mt-2 text-xs text-neutral-400">{VERIFICATION_STATE_DESCRIPTION[state]}</p>
    </div>
  );
}
