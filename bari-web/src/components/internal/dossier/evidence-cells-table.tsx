import type { Layer2Evidence } from "@/lib/dossier/types";

const FIELD_LABEL_HE: Record<string, string> = {
  energy: "אנרגיה",
  protein: "חלבון",
  fat: "שומן",
  saturated_fat: "שומן רווי",
  trans_fat: "שומן טראנס",
  carbs: "פחמימות",
  sugar: "סוכר",
  fiber: "סיבים",
  sodium: "נתרן",
  cholesterol: "כולסטרול",
};

/** Layer-2 raw-evidence cells — one row per nutrition field, exactly the
 * compiler's own {value, raw_source_text, source, status, flags,
 * captured_at} shape. `raw_source_text` is the retailer's raw Hebrew/number
 * string (dir="auto" so mixed Hebrew/Latin/digit strings render correctly
 * regardless of which script leads).
 */
export function EvidenceCellsTable({ layer2 }: { layer2: Layer2Evidence }) {
  const fields = Object.keys(layer2).sort();
  return (
    <div>
      <h2 className="mb-2 text-sm font-semibold">שכבה 2 — תאי ראיה גולמיים</h2>
      <div className="overflow-x-auto rounded-md border border-neutral-200">
        <table className="w-full min-w-[720px] text-right text-sm">
          <thead className="bg-neutral-50 text-xs text-neutral-500">
            <tr>
              <th className="px-3 py-2">שדה</th>
              <th className="px-3 py-2">ערך מפוענח</th>
              <th className="px-3 py-2">טקסט מקור גולמי</th>
              <th className="px-3 py-2">מקור</th>
              <th className="px-3 py-2">סטטוס</th>
              <th className="px-3 py-2">דגלים</th>
              <th className="px-3 py-2">נלכד ב-</th>
            </tr>
          </thead>
          <tbody>
            {fields.map((field) => {
              const cell = layer2[field];
              const missing = cell.status !== "retrieved" || cell.value === null;
              return (
                <tr key={field} className="border-t border-neutral-100 odd:bg-white even:bg-neutral-50/50">
                  <td className="px-3 py-2 font-medium">{FIELD_LABEL_HE[field] ?? field}</td>
                  <td className={`px-3 py-2 tabular-nums ${missing ? "text-neutral-400" : ""}`}>
                    {cell.value === null ? "לא נמצא" : String(cell.value)}
                  </td>
                  <td dir="auto" className="px-3 py-2 font-mono text-xs text-neutral-500">
                    {cell.raw_source_text ?? "—"}
                  </td>
                  <td className="px-3 py-2 text-xs text-neutral-400">{cell.source}</td>
                  <td className="px-3 py-2 text-xs">
                    <span className={cell.status === "retrieved" ? "text-emerald-700" : "text-neutral-400"}>
                      {cell.status === "retrieved" ? "התקבל" : "לא התקבל"}
                    </span>
                  </td>
                  <td className="px-3 py-2 text-xs text-amber-700">{cell.flags.length > 0 ? cell.flags.join(", ") : "—"}</td>
                  <td className="px-3 py-2 text-xs text-neutral-400">{cell.captured_at ?? "—"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
