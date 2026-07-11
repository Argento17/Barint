import { DossierTable } from "@/components/internal/dossier/dossier-table";
import { Shell } from "@/components/internal/dossier/shell";
import { dossierDataAvailable, listDossierRows } from "@/lib/dossier/data";

export const dynamic = "force-dynamic";

// Internal-only route (TASK-611 / PD-3). Corpus-wide Product Dossier list —
// the queryable view over data health: barcode adjudication state, Layer-4
// check verdicts, and evidence completeness for every product the compiler
// (03_operations/product_dossier/build_dossiers.py) has produced a dossier
// for. Read-only: this page never recomputes a score or mutates anything.
export default function DossierListPage() {
  if (!dossierDataAvailable()) {
    return (
      <Shell wide>
        <h1 className="mb-2 text-xl font-semibold">Product Dossier — רשימת מוצרים</h1>
        <p className="rounded-md bg-amber-50 px-4 py-3 text-sm text-amber-800">
          לא נמצאו נתוני dossier. הרץ <code className="font-mono">npm run sync:dossiers</code> (לאחר הרצת{" "}
          <code className="font-mono">python 03_operations/product_dossier/build_dossiers.py</code> ב-C:\Bari).
        </p>
      </Shell>
    );
  }

  const rows = listDossierRows();

  return (
    <Shell wide>
      <div className="mb-6">
        <h1 className="text-xl font-semibold">Product Dossier — רשימת מוצרים</h1>
        <p className="mt-1 text-sm text-neutral-500">
          {rows.length} מוצרים · כלי אבחון פנימי (לא מיועד לצרכן, לא ניתן לאינדוקס). נתונים נגזרים מ-
          <code className="mx-1 font-mono text-xs">build_dossiers.py</code>
          — מציג בדיוק את מה שהמחשוב הפיק, ללא עיבוד נוסף.
        </p>
      </div>
      <DossierTable rows={rows} />
    </Shell>
  );
}
