import type { Layer3, Layer4Check } from "@/lib/dossier/types";
import { CheckStatusBadge } from "./status-badge";

/** `publication_record` — what Bari currently publishes, verbatim (memo R-C).
 * This is its OWN disjoint namespace: never labeled as "assessment", never
 * folded into product-quality. The calculation-check verdict is shown right
 * beside the served score so an unverifiable published value is visibly
 * flagged rather than silently trusted (memo §4, tripwire-1).
 */
export function PublicationRecordBlock({
  publicationRecord,
  calculationCheck,
}: {
  publicationRecord: Layer3["publication_record"];
  calculationCheck: Layer4Check;
}) {
  const { score, grade, run_id, trace_hash } = publicationRecord;
  return (
    <div className="rounded-md border border-neutral-200 p-4">
      <div className="mb-2 flex items-center justify-between">
        <h2 className="text-sm font-semibold">publication_record — הציון המפורסם, כפי שהוא</h2>
        <CheckStatusBadge status={calculationCheck.status} label="בדיקת חישוב" />
      </div>
      <p className="mb-3 text-xs text-neutral-400">
        זהו עותק מדויק של מה שמתפרסם באתר כיום — לא הערכה טרייה ולא ממוצע עם data_quality. ראה בדיקת &ldquo;חישוב&rdquo; למעלה
        לפני שסומכים על ערך זה.
      </p>
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <Field label="ציון" value={score?.value == null ? "—" : String(score.value)} />
        <Field label="ציון (אות)" value={grade?.value == null ? "—" : String(grade.value)} />
        <Field label="run_id" value={run_id?.value == null ? "—" : String(run_id.value)} mono />
        <Field label="trace_hash" value={trace_hash?.value ? String(trace_hash.value).slice(0, 16) + "…" : "—"} mono />
      </div>
      {calculationCheck.reason && <p className="mt-3 text-xs text-red-700">{calculationCheck.reason}</p>}
    </div>
  );
}

function Field({ label, value, mono }: { label: string; value: string | number; mono?: boolean }) {
  return (
    <div>
      <div className="text-xs text-neutral-400">{label}</div>
      <div className={`text-sm font-medium ${mono ? "font-mono text-xs" : ""}`}>{value}</div>
    </div>
  );
}
