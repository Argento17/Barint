import { DossierTable } from "@/components/internal/dossier/dossier-table";
import { Shell } from "@/components/internal/dossier/shell";
import { dossierDataAvailable, loadDossierIndex } from "@/lib/dossier/data";

export const dynamic = "force-dynamic";

export default function DossierListPage() {
  if (!dossierDataAvailable()) {
    return <Shell wide><h1 className="mb-2 text-xl font-semibold">Product dossier</h1><p className="rounded-md bg-amber-50 px-4 py-3 text-sm text-amber-800">No dossier data found. Run <code className="font-mono">npm run sync:dossiers</code> after the compiler has produced its output.</p></Shell>;
  }
  const index = loadDossierIndex();
  return <Shell wide><div className="mb-6"><h1 className="text-xl font-semibold">Product dossier</h1><p className="mt-1 text-sm text-neutral-500">{index.products.length} products · read-only internal inspection tool. This view renders compiled dossier output without recomputing scores.</p></div><DossierTable rows={index.products} generatedAt={index.generatedAt} /></Shell>;
}
