import { ChecksPanel } from "@/components/internal/dossier/checks-panel";
import { EvidenceCellsTable } from "@/components/internal/dossier/evidence-cells-table";
import { IdentityHeader } from "@/components/internal/dossier/identity-header";
import { NamespaceBars } from "@/components/internal/dossier/namespace-bars";
import { PublicationRecordBlock } from "@/components/internal/dossier/publication-record-block";
import type { ProductDossier } from "@/lib/dossier/types";

/**
 * Technical-audit tab (TASK-620 / PD-3.1). Moves the pre-TASK-620 dense
 * diagnostic view here VERBATIM — same components, same Hebrew labels, no
 * rebuild — per spec ("move today's dense diagnostic view here verbatim").
 * This is the ONLY place bari_pid, compiler/parser identifiers, raw config
 * paths, and the full layer_2 provenance table are shown; the Overview and
 * Evidence tabs deliberately hide them.
 */
export function TechnicalAuditTab({ dossier }: { dossier: ProductDossier }) {
  return (
    <div dir="rtl" lang="he">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-2 rounded-md bg-neutral-50 px-3 py-2 text-xs text-neutral-500">
        <span>
          מדף: {dossier.generation.shelf_id} · נוצר: {new Date(dossier.generation.generated_at).toLocaleString("he-IL")} · compiler{" "}
          {dossier.generation.compiler_version} · parser {dossier.generation.parser_version}
        </span>
        <span className="font-mono text-[0.65rem] text-neutral-400" dir="ltr">
          {dossier.generation.shelf_config_path}
        </span>
      </div>

      <div className="space-y-6">
        <IdentityHeader layer1={dossier.layer_1} />
        <ChecksPanel layer4={dossier.layer_4} />
        <PublicationRecordBlock publicationRecord={dossier.layer_3.publication_record} calculationCheck={dossier.layer_4.calculation} />
        <NamespaceBars layer3={dossier.layer_3} />
        <EvidenceCellsTable layer2={dossier.layer_2} />

        <details className="rounded-md border border-neutral-200 p-3">
          <summary className="cursor-pointer select-none text-sm font-semibold text-neutral-700">
            Raw dossier JSON (compiler output, served-JSON excerpt)
          </summary>
          <pre dir="ltr" className="mt-3 max-h-[480px] overflow-auto rounded bg-neutral-900 p-3 text-[0.7rem] leading-relaxed text-neutral-100">
            {JSON.stringify(dossier, null, 2)}
          </pre>
        </details>
      </div>
    </div>
  );
}
