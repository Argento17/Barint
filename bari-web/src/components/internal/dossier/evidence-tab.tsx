import { LAYER2_FIELD_META } from "@/lib/dossier/overview-labels";
import type { Layer2Evidence } from "@/lib/dossier/types";

/**
 * Evidence tab (TASK-620 / PD-3.1). Readable provenance from layer_2, English
 * labels — never the internal field key verbatim (e.g. "Energy (kcal)", not
 * "energy"). This is a NEW, human-legible sibling to the Technical-audit
 * tab's raw EvidenceCellsTable (which stays exactly as-is, Hebrew labels and
 * all — moved verbatim per spec, not rebuilt).
 *
 * "Source type" is a fixed constant, not a per-row invented fact: the compiler
 * schema (`layer2_evidence.py`) carries only a retailer-name `source` string —
 * there is no separate per-cell source-type field. Per the project's
 * OFF-ban policy, the only allowed evidence pathway for nutrition/ingredients
 * is the direct retailer product-page scrape, so every populated cell has the
 * same true source type; this is documented here rather than fabricated
 * per-row.
 * "Confidence" is likewise not a field the schema carries per cell — it is a
 * deterministic translation of status + flags (never a new number).
 */
export function EvidenceTab({ layer2 }: { layer2: Layer2Evidence }) {
  const fields = Object.keys(layer2).sort();

  return (
    <div dir="ltr" lang="en">
      <p className="mb-3 text-xs text-neutral-500">
        One row per retrieved-or-not nutrition field, exactly as the compiler captured it. &ldquo;Not retrieved&rdquo; means the
        field was never found on the source page — never imputed, never substituted from another source (OFF is banned
        project-wide).
      </p>
      <div className="overflow-x-auto rounded-md border border-neutral-200">
        <table className="w-full min-w-[820px] text-left text-sm">
          <thead className="bg-neutral-50 text-xs text-neutral-500">
            <tr>
              <th className="px-3 py-2">Field</th>
              <th className="px-3 py-2">Value</th>
              <th className="px-3 py-2">Unit</th>
              <th className="px-3 py-2">Source</th>
              <th className="px-3 py-2">Source type</th>
              <th className="px-3 py-2">Status</th>
              <th className="px-3 py-2">Confidence</th>
              <th className="px-3 py-2">Notes / conflicts</th>
            </tr>
          </thead>
          <tbody>
            {fields.map((field) => {
              const cell = layer2[field];
              const meta = LAYER2_FIELD_META[field] ?? { label: field, unit: "" };
              const missing = cell.status !== "retrieved" || cell.value === null;
              const confidenceLabel = missing ? "Not available" : cell.flags.length > 0 ? "Flagged" : "Confirmed";
              const statusLabel = missing ? "Missing" : "Retrieved";
              return (
                <tr key={field} className="border-t border-neutral-100 odd:bg-white even:bg-neutral-50/50">
                  <td className="px-3 py-2 font-medium">{meta.label}</td>
                  <td className={`px-3 py-2 tabular-nums ${missing ? "text-neutral-400" : ""}`} dir="auto">
                    {cell.value === null ? "Not retrieved" : String(cell.value)}
                  </td>
                  <td className="px-3 py-2 text-xs text-neutral-400">{cell.value === null ? "—" : meta.unit || "—"}</td>
                  <td className="px-3 py-2 text-xs text-neutral-500">{cell.source ?? "—"}</td>
                  <td className="px-3 py-2 text-xs text-neutral-400">
                    {cell.source ? "Retailer product page (direct scrape)" : "—"}
                  </td>
                  <td className="px-3 py-2 text-xs">
                    <span className={missing ? "text-neutral-400" : "text-emerald-700"}>
                      {statusLabel}
                    </span>
                  </td>
                  <td className="px-3 py-2 text-xs text-neutral-500">{confidenceLabel}</td>
                  <td className="px-3 py-2 text-xs text-amber-700">{cell.flags.length > 0 ? cell.flags.join(", ") : "—"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
