import type { Layer1Identity, Layer3 } from "@/lib/dossier/types";
import { BARCODE_STATUS_LABEL_EN } from "@/lib/dossier/overview-labels";
import type { VerdictResolution } from "@/lib/dossier/verdict";

/**
 * Overview §A — Product header (TASK-620 / PD-3.1). English, consumer-legible
 * identity facts only. Deliberately OMITS bari_pid, compiler/parser names, raw
 * paths, raw IDs, namespaces, and build timestamps — those move to the
 * Technical-audit tab. Image comes from the matched live VM when a verdict
 * match exists; otherwise falls back to an initial tile (never fabricates a
 * product photo).
 */
export function ProductHeader({
  layer1,
  publicationRecord,
  shelfId,
  verdict,
}: {
  layer1: Layer1Identity;
  publicationRecord: Layer3["publication_record"];
  shelfId: string;
  verdict: VerdictResolution;
}) {
  const facts = layer1.identity_facts;
  const name = facts.name.value ?? "(no name on file)";
  const imageUrl = verdict.status === "matched" ? verdict.product.imageUrl : null;
  const categoryLabel = verdict.status === "matched" ? verdict.categoryNameHe : shelfId;

  const score = publicationRecord.score?.value;
  const grade = publicationRecord.grade?.value;

  return (
    <div className="flex flex-wrap items-start gap-4 rounded-md border border-neutral-200 p-4">
      <ProductThumb imageUrl={imageUrl} name={name} />

      <div className="min-w-0 flex-1">
        <p className="text-[11px] font-bold uppercase tracking-[0.14em] text-neutral-400">
          {categoryLabel}
        </p>
        <h1 className="mt-0.5 text-lg font-semibold text-neutral-900" dir="auto">
          {name}
        </h1>
        {facts.brand.value ? (
          <p className="text-sm font-medium text-emerald-700" dir="auto">
            {facts.brand.value}
          </p>
        ) : null}

        <dl className="mt-3 grid grid-cols-1 gap-x-6 gap-y-1.5 text-xs text-neutral-500 sm:grid-cols-2">
          <Fact label="Manufacturer" value={facts.manufacturer.value} />
          <Fact label="Package size" value={facts.package_size.value} />
          <Fact label="Barcode status" value={BARCODE_STATUS_LABEL_EN[layer1.barcode_state.status] ?? layer1.barcode_state.status} />
          <Fact label="Retailer" value={facts.retailer.value} />
        </dl>
      </div>

      <div className="flex shrink-0 flex-col items-end gap-1">
        <span className="text-[11px] font-medium uppercase tracking-wide text-neutral-400">Published score</span>
        <span className="text-2xl font-bold tabular-nums text-neutral-900">
          {score != null ? String(score) : "—"}
          {grade != null ? <span className="ms-1.5 text-base font-semibold text-emerald-700">{String(grade)}</span> : null}
        </span>
      </div>
    </div>
  );
}

function Fact({ label, value }: { label: string; value: string | null }) {
  return (
    <div className="flex items-baseline justify-between gap-2 border-b border-neutral-100 py-1 last:border-0">
      <span className="text-neutral-400">{label}</span>
      <span className="max-w-[65%] truncate font-medium text-neutral-700" dir="auto" title={value ?? undefined}>
        {value ?? "—"}
      </span>
    </div>
  );
}

function ProductThumb({ imageUrl, name }: { imageUrl: string | null; name: string }) {
  if (imageUrl) {
    // eslint-disable-next-line @next/next/no-img-element
    return (
      <img
        src={imageUrl}
        alt=""
        className="size-16 shrink-0 rounded-lg border border-neutral-200 object-contain"
        style={{ background: "#F7F7F2" }}
      />
    );
  }
  const initial = name.trim()[0] ?? "?";
  return (
    <span
      className="inline-flex size-16 shrink-0 items-center justify-center rounded-lg border border-neutral-200 text-xl font-bold text-neutral-400"
      style={{ background: "#F7F7F2" }}
      aria-hidden
    >
      {initial}
    </span>
  );
}
