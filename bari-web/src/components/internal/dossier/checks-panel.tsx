import type { Layer4Check, Layer4Checks } from "@/lib/dossier/types";
import { CheckStatusBadge } from "./status-badge";

const CHECK_LABEL_HE: Record<keyof Layer4Checks, string> = {
  barcode: "ברקוד",
  source_traceability: "מעקב מקור",
  calculation: "חישוב",
  publishability: "פרסום (אבחוני בלבד)",
};

function CheckCard({ id, check }: { id: keyof Layer4Checks; check: Layer4Check }) {
  return (
    <div className="rounded-md border border-neutral-200 p-3">
      <div className="mb-1.5 flex items-center justify-between">
        <span className="text-sm font-medium">{CHECK_LABEL_HE[id]}</span>
        <CheckStatusBadge status={check.status} label={check.status.toUpperCase()} />
      </div>
      {check.reason && <p className="mb-1.5 text-xs text-neutral-500">{check.reason}</p>}
      {check.evidence.length > 0 && (
        <ul className="space-y-0.5 text-[0.7rem] text-neutral-400">
          {check.evidence.map((line, i) => (
            <li key={i} className="font-mono">
              {line}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

/** Layer-4 check panel — the four pass/warn/fail/unknown checks (memo §4/§5).
 * `publishability` is explicitly diagnostic-only (tripwire-1: it never gates
 * or changes current publication) — labeled as such here, not just in data.
 */
export function ChecksPanel({ layer4 }: { layer4: Layer4Checks }) {
  return (
    <div>
      <h2 className="mb-2 text-sm font-semibold">שכבה 4 — בדיקות</h2>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <CheckCard id="barcode" check={layer4.barcode} />
        <CheckCard id="source_traceability" check={layer4.source_traceability} />
        <CheckCard id="calculation" check={layer4.calculation} />
        <CheckCard id="publishability" check={layer4.publishability} />
      </div>
    </div>
  );
}
