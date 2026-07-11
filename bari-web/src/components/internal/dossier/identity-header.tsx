import type { IdentityFact, Layer1Identity } from "@/lib/dossier/types";
import { BarcodeStatusBadge } from "./status-badge";

const FACT_LABEL_HE: Record<string, string> = {
  name: "שם",
  brand: "מותג",
  manufacturer: "יצרן",
  package_size: "גודל אריזה",
  retailer: "קמעונאי",
  source_urls: "כתובות מקור",
  last_scrape: "סריקה אחרונה",
};

function FactRow({ label, fact }: { label: string; fact: IdentityFact }) {
  const value = fact.value;
  const display =
    value === null || value === undefined
      ? "—"
      : Array.isArray(value)
        ? value.length
          ? value.join(", ")
          : "—"
        : String(value);
  return (
    <div className="flex flex-col gap-0.5 border-b border-neutral-100 py-1.5 last:border-0">
      <div className="flex items-baseline justify-between gap-2">
        <span className="text-xs text-neutral-400">{label}</span>
        <span className="max-w-[60%] truncate text-sm font-medium" title={display}>
          {display}
        </span>
      </div>
      <span className="text-[0.65rem] text-neutral-400">
        {fact.derivation}
        {fact.source ? ` · ${fact.source}` : ""}
      </span>
    </div>
  );
}

/** Layer-1 identity + barcode-status header (memo §5 Page-1 shape).
 * `identity_facts` are R-B provenance-pointed projections, never registry
 * copies — the derivation/source line under each fact is what makes that
 * visible rather than implicit.
 */
export function IdentityHeader({ layer1 }: { layer1: Layer1Identity }) {
  const facts = layer1.identity_facts;
  return (
    <div className="rounded-md border border-neutral-200 p-4">
      <div className="mb-3 flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="text-lg font-semibold">{facts.name.value ?? "(ללא שם)"}</h1>
          <p className="mt-0.5 font-mono text-xs text-neutral-400">
            pid: {layer1.pid ?? "—"} ({layer1.pid_status}) · key: {layer1.provisional_key}
          </p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <BarcodeStatusBadge status={layer1.barcode_state.status} />
          {layer1.barcode_state.reason && <span className="text-[0.65rem] text-neutral-400">{layer1.barcode_state.reason}</span>}
        </div>
      </div>

      <div className="mb-3 grid grid-cols-2 gap-x-6 gap-y-1 text-xs text-neutral-500 sm:grid-cols-3">
        <span>
          ברקוד כפי שהוגש: <span className="font-mono text-neutral-700">{layer1.barcode_state.served_barcode_unadjudicated ?? "—"}</span>
        </span>
        <span>
          GTIN משוחזר: <span className="font-mono text-neutral-700">{layer1.recovered_gtin ?? "—"}</span>
        </span>
        <span>כינויים: {layer1.aliases.length}</span>
      </div>

      {layer1.aliases.length > 0 && (
        <details className="mb-3 text-xs text-neutral-400">
          <summary className="cursor-pointer select-none">כל הכינויים ({layer1.aliases.length})</summary>
          <ul className="mt-1 space-y-0.5 font-mono">
            {layer1.aliases.map((a) => (
              <li key={a}>{a}</li>
            ))}
          </ul>
        </details>
      )}

      <div className="grid grid-cols-1 gap-x-6 sm:grid-cols-2">
        {Object.entries(facts).map(([key, fact]) => (
          <FactRow key={key} label={FACT_LABEL_HE[key] ?? key} fact={fact} />
        ))}
      </div>
    </div>
  );
}
