import Link from "next/link";
import { notFound } from "next/navigation";

import { ChecksPanel } from "@/components/internal/dossier/checks-panel";
import { EvidenceCellsTable } from "@/components/internal/dossier/evidence-cells-table";
import { IdentityHeader } from "@/components/internal/dossier/identity-header";
import { NamespaceBars } from "@/components/internal/dossier/namespace-bars";
import { PublicationRecordBlock } from "@/components/internal/dossier/publication-record-block";
import { Shell } from "@/components/internal/dossier/shell";
import { dossierDataAvailable, loadDossier, loadDossierIndex } from "@/lib/dossier/data";

export const dynamic = "force-dynamic";

// Internal-only Page-1 inspection view (TASK-611 / PD-3, memo §5). Read-only:
// renders exactly what build_dossiers.py produced, never recomputes anything.
export default async function DossierDetailPage({ params }: { params: Promise<{ pid: string }> }) {
  const { pid } = await params;

  if (!dossierDataAvailable()) {
    return (
      <Shell wide>
        <p className="rounded-md bg-amber-50 px-4 py-3 text-sm text-amber-800">
          לא נמצאו נתוני dossier. הרץ <code className="font-mono">npm run sync:dossiers</code>.
        </p>
      </Shell>
    );
  }

  const dossier = loadDossier(pid);
  if (!dossier) notFound();

  const index = loadDossierIndex();

  return (
    <Shell wide>
      <div className="mb-4 flex items-center justify-between">
        <Link href="/internal/dossier" className="text-xs font-medium text-neutral-500 underline">
          ← חזרה לרשימה
        </Link>
        <span className="text-xs text-neutral-400">
          מדף: {dossier.generation.shelf_id} · נוצר: {new Date(dossier.generation.generated_at).toLocaleString("he-IL")} ·
          compiler {dossier.generation.compiler_version}
        </span>
      </div>

      <div className="space-y-6">
        <IdentityHeader layer1={dossier.layer_1} />
        <ChecksPanel layer4={dossier.layer_4} />
        <PublicationRecordBlock publicationRecord={dossier.layer_3.publication_record} calculationCheck={dossier.layer_4.calculation} />
        <NamespaceBars layer3={dossier.layer_3} />
        <EvidenceCellsTable layer2={dossier.layer_2} />
      </div>

      <p className="mt-6 text-[0.65rem] text-neutral-300">
        {index.totalProducts} מוצרים בקובץ אינדקס זה · מקור: {index.sourceDir}
      </p>
    </Shell>
  );
}
