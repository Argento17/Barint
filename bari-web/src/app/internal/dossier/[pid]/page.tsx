import Link from "next/link";
import { notFound } from "next/navigation";

import { DetailTabs } from "@/components/internal/dossier/detail-tabs";
import { EvidenceTab } from "@/components/internal/dossier/evidence-tab";
import { OverviewTab } from "@/components/internal/dossier/overview-tab";
import { Shell } from "@/components/internal/dossier/shell";
import { TechnicalAuditTab } from "@/components/internal/dossier/technical-tab";
import { dossierDataAvailable, loadDossier, loadDossierIndex } from "@/lib/dossier/data";
import { resolveVerdict } from "@/lib/dossier/verdict";

export const dynamic = "force-dynamic";

export default async function DossierDetailPage({ params }: { params: Promise<{ pid: string }> }) {
  const { pid } = await params;
  if (!dossierDataAvailable()) return <Shell wide><p className="rounded-md bg-amber-50 px-4 py-3 text-sm text-amber-800">No dossier data found. Run <code className="font-mono">npm run sync:dossiers</code>.</p></Shell>;
  const dossier = loadDossier(pid);
  if (!dossier) notFound();
  const index = loadDossierIndex();
  const verdict = resolveVerdict(dossier);
  return <Shell wide><div className="mb-4 flex items-center justify-between"><Link href="/internal/dossier" className="text-xs font-medium text-neutral-500 underline">← Back to list</Link><span className="font-mono text-xs text-neutral-400">{pid}</span></div><DetailTabs overview={<OverviewTab dossier={dossier} verdict={verdict} />} evidence={<EvidenceTab layer2={dossier.layer_2} />} technical={<TechnicalAuditTab dossier={dossier} />} /><p className="mt-6 text-[0.65rem] text-neutral-300">{index.totalProducts} products in this index · source: {index.sourceDir}</p></Shell>;
}
