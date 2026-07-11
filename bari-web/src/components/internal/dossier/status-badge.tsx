import type { CheckStatus } from "@/lib/dossier/types";

const CHECK_STATUS_STYLE: Record<CheckStatus, string> = {
  pass: "bg-emerald-50 text-emerald-800 border-emerald-200",
  warn: "bg-amber-50 text-amber-800 border-amber-200",
  fail: "bg-red-50 text-red-800 border-red-200",
  unknown: "bg-neutral-100 text-neutral-500 border-neutral-200",
};

const CHECK_STATUS_LABEL_HE: Record<CheckStatus, string> = {
  pass: "עבר",
  warn: "אזהרה",
  fail: "נכשל",
  unknown: "לא ידוע",
};

/** Layer-4 check status badge — pass/warn/fail/unknown. Internal-tool only;
 * intentionally NOT the consumer gradePalette (that is a product-grade axis,
 * this is a record-check axis — never mix the two visual languages).
 */
export function CheckStatusBadge({ status, label }: { status: CheckStatus; label: string }) {
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-md border px-2 py-0.5 text-xs font-medium ${CHECK_STATUS_STYLE[status]}`}
    >
      <span>{label}</span>
      <span className="opacity-60">·</span>
      <span>{CHECK_STATUS_LABEL_HE[status]}</span>
    </span>
  );
}

const BARCODE_STATUS_STYLE: Record<string, string> = {
  verified: "bg-emerald-50 text-emerald-800 border-emerald-200",
  malformed: "bg-amber-50 text-amber-800 border-amber-200",
  pending_manual_review: "bg-amber-50 text-amber-800 border-amber-200",
  found_but_conflicting: "bg-red-50 text-red-800 border-red-200",
  not_found: "bg-red-50 text-red-800 border-red-200",
  unknown: "bg-neutral-100 text-neutral-500 border-neutral-200",
};

const BARCODE_STATUS_LABEL_HE: Record<string, string> = {
  verified: "מאומת",
  malformed: "פגום",
  pending_manual_review: "ממתין לבדיקה",
  found_but_conflicting: "סתירה",
  not_found: "לא נמצא",
  unknown: "לא ידוע",
};

export function BarcodeStatusBadge({ status }: { status: string }) {
  const cls = BARCODE_STATUS_STYLE[status] ?? BARCODE_STATUS_STYLE.unknown;
  const label = BARCODE_STATUS_LABEL_HE[status] ?? status;
  return (
    <span className={`inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium ${cls}`}>
      {label}
    </span>
  );
}
