import { AttentionChecks } from "./overview/attention-checks";
import { InsightsPanel } from "./overview/insights-panel";
import { AssessmentCard, DataQualityCard, PublicationIntegrityCard } from "./overview/metric-cards";
import { ProductHeader } from "./overview/product-header";
import { ProductProfileBars } from "./overview/profile-bars";
import { VerdictBlock } from "./overview/verdict-block";
import type { ProductDossier } from "@/lib/dossier/types";
import type { VerdictResolution } from "@/lib/dossier/verdict";

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
