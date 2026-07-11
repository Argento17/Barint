import { ASSESSMENT_HEADLINE_LABEL, DATA_QUALITY_LABEL, PUBLICATION_RECORD_LABEL } from "@/lib/dossier/overview-labels";
import type { Layer3 } from "@/lib/dossier/types";

// Overview §C — three SEPARATE cards (TASK-620 / PD-3.1 hard rule): assessment,
// data_quality, and publication_record are disjoint namespaces the compiler keeps
// apart on purpose (memo R-C) — this component never averages or blends them into
// one overall number, and never renders them in a single shared card. Dimension
// breakdown lives in §D (the profile visual) so it is not duplicated here — this
// card shows only the assessment namespace's headline (non-dimension) fields.
// `nova_proxy` is intentionally never read/rendered here (banned framework term).

function fmtPct(value: unknown): string {
  return typeof value === "number" ? `${Math.round(value * 100)}%` : "—";
}

function fmtRaw(value: unknown): string {
  if (value === null || value === undefined) return "—";
  return String(value);
}

function fmtHash(value: unknown): string {
  if (typeof value !== "string" || value.length === 0) return "—";
  return `${value.slice(0, 12)}…`;
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-baseline justify-between gap-2 border-b border-neutral-100 py-1.5 last:border-0">
      <span className="text-xs text-neutral-400">{label}</span>
      <span className="font-medium text-neutral-800" title={value}>
        {value}
      </span>
    </div>
  );
}

function Card({ title, subtitle, children }: { title: string; subtitle: string; children: React.ReactNode }) {
  return (
    <div className="rounded-md border border-neutral-200 p-4">
      <h3 className="text-sm font-semibold text-neutral-800">{title}</h3>
      <p className="mb-2 text-[11px] text-neutral-400">{subtitle}</p>
      {children}
    </div>
  );
}

export function AssessmentCard({ assessment }: { assessment: Layer3["assessment"] }) {
  return (
    <Card title="Product assessment" subtitle="What Bari's engine estimates about this product">
      {(Object.keys(ASSESSMENT_HEADLINE_LABEL) as Array<keyof typeof ASSESSMENT_HEADLINE_LABEL>).map((key) => (
        <Row key={key} label={ASSESSMENT_HEADLINE_LABEL[key]} value={fmtRaw(assessment[key]?.value)} />
      ))}
    </Card>
  );
}

export function DataQualityCard({ dataQuality }: { dataQuality: Layer3["data_quality"] }) {
  return (
    <Card title="Data quality" subtitle="How complete and trustworthy the underlying record is">
      {(Object.keys(DATA_QUALITY_LABEL) as Array<keyof typeof DATA_QUALITY_LABEL>).map((key) => (
        <Row key={key} label={DATA_QUALITY_LABEL[key]} value={fmtPct(dataQuality[key]?.value)} />
      ))}
    </Card>
  );
}

export function PublicationIntegrityCard({ publicationRecord }: { publicationRecord: Layer3["publication_record"] }) {
  return (
    <Card title="Publication integrity" subtitle="Exactly what is live on the site today, verbatim">
      <Row label={PUBLICATION_RECORD_LABEL.score} value={fmtRaw(publicationRecord.score?.value)} />
      <Row label={PUBLICATION_RECORD_LABEL.grade} value={fmtRaw(publicationRecord.grade?.value)} />
      <Row label={PUBLICATION_RECORD_LABEL.run_id} value={fmtRaw(publicationRecord.run_id?.value)} />
      <Row label={PUBLICATION_RECORD_LABEL.trace_hash} value={fmtHash(publicationRecord.trace_hash?.value)} />
    </Card>
  );
}
