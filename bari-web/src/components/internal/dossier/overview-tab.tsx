import { AttentionChecks } from "./overview/attention-checks";
import { InsightsPanel } from "./overview/insights-panel";
import { AssessmentCard, DataQualityCard, PublicationIntegrityCard } from "./overview/metric-cards";
import { ProductHeader } from "./overview/product-header";
import { ProductProfileBars } from "./overview/profile-bars";
import { VerdictBlock } from "./overview/verdict-block";
import type { ProductDossier } from "@/lib/dossier/types";
import type { VerdictResolution } from "@/lib/dossier/verdict";

function statusLine(dossier: ProductDossier, verdict: VerdictResolution): string {
  const barcode = dossier.layer_1.barcode_state.status;
  const verified = dossier.layer_4.calculation.status === "pass" && verdict.status === "matched" && verdict.product.confidence === "verified";
  const barcodeText = barcode === "verified" ? "Barcode identity is verified" : barcode === "pending_manual_review" ? "Needs manual barcode review" : barcode === "found_but_conflicting" ? "Barcode identity has a conflicting match" : barcode === "malformed" ? "Barcode appears malformed" : barcode === "not_found" ? "Barcode was not found" : "Barcode identity is unresolved";
  return `Status: ${barcodeText}. Score is ${verified ? "verified" : "not fully verified"}.`;
}

/**
 * Overview tab — the DEFAULT view on the dossier detail page (TASK-620 /
 * PD-3.1). English UI. Answers in <30s: what is this product, what does Bari
 * think, why, can we trust it, what needs action. Server Component — the only
 * client boundary inside is VerdictBlock (needs local open/toggle state for
 * the real ComparisonRow) and ProductProfileBars/AttentionChecks (recharts /
 * local disclosure state respectively).
 */
export function OverviewTab({ dossier, verdict }: { dossier: ProductDossier; verdict: VerdictResolution }) {
  return (
    <div dir="ltr" lang="en" className="space-y-4">
      <ProductHeader
        layer1={dossier.layer_1}
        publicationRecord={dossier.layer_3.publication_record}
        shelfId={dossier.generation.shelf_id}
        verdict={verdict}
      />

      <p className="rounded-md border border-neutral-200 bg-neutral-50 px-4 py-3 text-sm font-semibold text-neutral-800">{statusLine(dossier, verdict)}</p>

      <VerdictBlock verdict={verdict} calculationCheck={dossier.layer_4.calculation} />

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <AssessmentCard assessment={dossier.layer_3.assessment} />
        <DataQualityCard dataQuality={dossier.layer_3.data_quality} />
        <PublicationIntegrityCard publicationRecord={dossier.layer_3.publication_record} />
      </div>

      <ProductProfileBars assessment={dossier.layer_3.assessment} />

      <InsightsPanel layer2={dossier.layer_2} layer3={dossier.layer_3} layer4={dossier.layer_4} />

      <div>
        <h3 className="mb-2 text-sm font-semibold text-neutral-800">Checks needing attention</h3>
        <AttentionChecks layer4={dossier.layer_4} />
      </div>
    </div>
  );
}
