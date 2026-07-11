import {
  deriveConcerns,
  deriveMissingInformation,
  deriveRecommendedActions,
  deriveStrengths,
} from "@/lib/dossier/overview-derive";
import type { Layer2Evidence, Layer3, Layer4Checks } from "@/lib/dossier/types";

// Overview §E — Human insights (TASK-620 / PD-3.1). Every bullet is a
// DETERMINISTIC projection of an existing PD field (see
// lib/dossier/overview-derive.ts) — no authored prose, no new claims. An empty
// bucket renders nothing at all (never padded with placeholder text).
export function InsightsPanel({
  layer2,
  layer3,
  layer4,
}: {
  layer2: Layer2Evidence;
  layer3: Layer3;
  layer4: Layer4Checks;
}) {
  const strengths = deriveStrengths(layer3);
  const concerns = deriveConcerns(layer3);
  const missing = deriveMissingInformation(layer2);
  const actions = deriveRecommendedActions(layer4);

  if (strengths.length === 0 && concerns.length === 0 && missing.length === 0 && actions.length === 0) {
    return null;
  }

  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
      {strengths.length > 0 && (
        <Bucket title="Strengths" tone="good">
          {strengths.map((d) => (
            <li key={d.key}>
              {d.label} — {Math.round(d.value)}/100
            </li>
          ))}
        </Bucket>
      )}
      {concerns.length > 0 && (
        <Bucket title="Concerns" tone="warn">
          {concerns.map((d) => (
            <li key={d.key}>
              {d.label} — {Math.round(d.value)}/100
            </li>
          ))}
        </Bucket>
      )}
      {missing.length > 0 && (
        <Bucket title="Missing information" tone="neutral">
          {missing.map((label) => (
            <li key={label}>{label} — not retrieved</li>
          ))}
        </Bucket>
      )}
      {actions.length > 0 && (
        <Bucket title="Recommended action" tone="warn">
          {actions.map((a) => (
            <li key={a.checkId}>
              {a.label} ({a.status}){a.detail ? ` — ${a.detail}` : ""}
            </li>
          ))}
        </Bucket>
      )}
    </div>
  );
}

const TONE_STYLE: Record<"good" | "warn" | "neutral", string> = {
  good: "border-emerald-200 bg-emerald-50/60",
  warn: "border-amber-200 bg-amber-50/60",
  neutral: "border-neutral-200 bg-neutral-50",
};

function Bucket({ title, tone, children }: { title: string; tone: "good" | "warn" | "neutral"; children: React.ReactNode }) {
  return (
    <div className={`rounded-md border p-3 ${TONE_STYLE[tone]}`}>
      <h4 className="mb-1.5 text-xs font-semibold uppercase tracking-wide text-neutral-600">{title}</h4>
      <ul className="list-disc space-y-0.5 ps-4 text-sm text-neutral-700">{children}</ul>
    </div>
  );
}
