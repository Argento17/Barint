import { useState } from "react";
import {
  Stack,
  Row,
  Grid,
  Card,
  CardHeader,
  CardBody,
  H1,
  H2,
  H3,
  Text,
  Pill,
  Callout,
  Divider,
  Table,
  Stat,
  useHostTheme,
} from "cursor/canvas";

type BundleId = "A" | "B" | "C";

const BUNDLES: Record<BundleId, {
  label: string;
  summary: string;
  adopts: string[];
  rejects: string[];
  riskLevel: "low" | "medium" | "high";
}> = {
  A: {
    label: "Bundle A — Fresh Energy",
    summary: "Fresh greens/oranges, gradients, circular score chips, card grids, micro-interactions, dark mode toggle, mobile-first.",
    adopts: [
      "Stronger product photography presence in collapsed rows",
      "Mobile-first layout rhythm (already Bari target)",
      "Micro-interactions on row expand (--ease-out-soft already present)",
    ],
    rejects: [
      "Gradient hero sections — bari-frontend-ui forbidden pattern",
      "Circular score chips — breaks frozen ScoreChip geometry (left-border accent lost)",
      "Card grid as default layout — explicitly banned pattern",
      "Dark mode toggle — forbidden without explicit product decision",
      "Orange second brand accent — creates a third color axis alongside --bari-green and grade palette",
    ],
    riskLevel: "medium",
  },
  B: {
    label: "Bundle B — Dark Dashboard",
    summary: "Dark mode primary, neon warning flags, barcode scanner FAB, Digital Cart health score.",
    adopts: [
      "Barcode scanner: user intent valid as a future product feature — log for roadmap, not Phase 1",
      "Warning flags for claim shortfalls — already present as claimShortfallFlag pill in ComparisonRow",
    ],
    rejects: [
      "Dark mode as primary — irreversible consumer-facing brand change; trips tripwire #2; owner escalation required",
      "Neon warning palette — contrast ratio untested; neon on dark fails WCAG 1.4.3 at small text",
      "Digital Cart health score — second score axis, triggers tripwire #1 (scoring philosophy change)",
      "Barcode scanner FAB as Phase 1 — adds a fourth filter dimension; out of comparison page scope",
    ],
    riskLevel: "high",
  },
  C: {
    label: "Bundle C — Social + Personal",
    summary: "Premium product cards, marketing-vs-reality visuals, share cards for Stories/WhatsApp, guess-the-score UI, personal filter chips.",
    adopts: [
      "Marketing-vs-reality insight framing — fits existing rowReason +/- pattern",
      "Share card: OG image per category achievable without gamification UI",
      "Personal filter chips up to 3 dimensions — already in spec; the 'personal' framing is copy",
    ],
    rejects: [
      "Guess-the-score UI — hard drift: user must make a choice before seeing a product (Drift Detection #2)",
      "WhatsApp/Stories share sheet as Phase 1 UI — marketing feature, not comparison UI",
      "Premium per-row hero imagery — breaks 72px collapsed-row height constraint (frozen)",
    ],
    riskLevel: "medium",
  },
};

const DIRECTION_STATEMENT =
  "Evolve the existing cream-and-green system with sharper product photography, a refreshed hashvaot hub card, and a hero that leads with product imagery rather than abstract plant illustration — while keeping the 4-section page spine, frozen row geometry, and grade-palette intact. No dark mode, no gamification, no new score axes.";

const PALETTE_ROWS = [
  ["--canvas", "#F7F7F2", "Warm off-white — unchanged"],
  ["--bari-green", "#1F8F6A", "Primary brand — unchanged"],
  ["--bari-green-bright", "#2FAE82", "Signal green — unchanged"],
  ["--fg1 / --fg2 / --fg3", "#111318 / #4E5663 / #5E6560", "Ink hierarchy — unchanged"],
  ["--grade-a through --grade-e", "existing", "Full A-E ramp — frozen by owner directive 2026-06-03"],
  ["--surface-hero-img (NEW)", "#FFFFFF", "White card frame for product photography in hero area"],
  ["--chip-accent-lift (NEW)", "color-mix(in oklab, var(--bari-green) 12%, white)", "Subtle tint for ScoreChip lg variant in hero/card (not row)"],
];

const COMPONENTS = [
  {
    id: "C1", phase: 1 as const, action: "extend" as const,
    name: "HomeHero — product photography strip",
    file: "src/components/home/home-hero.tsx",
    description: "Replace PlantHeroBackground with 3-4 real product hero images (56×80px white-card thumbnails, --shadow-card, --radius-lg) rendered behind copy. Images aria-hidden; no score shown. Single copyline stays.",
    constraint: "Max hero height 280px mobile. No aggregate stats beside images. PlantHeroBackground removed, not overlaid.",
  },
  {
    id: "C2", phase: 1 as const, action: "restyle" as const,
    name: "HomeHero — grade-chip trust bar",
    file: "src/components/home/home-hero.tsx + content.ts",
    description: "Replace icon+text trust row with 3 grade chips (A/B/D, 28px, using ScoreChip lg) + label 'כל מוצר מקבל ציון'. Anchors the grade system before the user reaches a category page.",
    constraint: "ScoreChip uses existing gradePalette — no new chip geometry. 3 chips max. No stat labels ('מתוך X מוצרים' is drift).",
  },
  {
    id: "C3", phase: 1 as const, action: "restyle" as const,
    name: "HashvaotCategoryBox LiveCard — thumbnail strip",
    file: "src/components/hashvaot/hashvaot-category-box.tsx",
    description: "Add 2×2 mini product-thumbnail strip (40×40px, --radius-sm, object-fit: cover) in card lower-left, behind CTA button. Thumbnails aria-hidden. Remove heroStat aggregate numeric.",
    constraint: "No second accent color. category.accent drives CTA only. heroStat replaced with category product-count in --fg3.",
  },
  {
    id: "C4", phase: 1 as const, action: "extend" as const,
    name: "CategoryHero — optional insightLine",
    file: "src/components/shared/category-hero.tsx",
    description: "Add optional insightLine prop: one Hebrew sentence from category's top finding. Renders between eyebrow and title at bari-meta size, --fg3 color. Replaces 12px metadata string where a finding exists.",
    constraint: "One line only (truncate). No aggregate percentages. Content Agent + QA gate sign-off required.",
  },
  {
    id: "C5", phase: 1 as const, action: "extend" as const,
    name: "ComparisonRow — claimShortfall prominence",
    file: "src/components/shared/comparison-row.tsx",
    description: "Increase claimShortfallFlag pill padding-inline from 6px to 10px, font-size 10px to 11px. Move above rowVerdict so it appears directly under product name. No color change.",
    constraint: "Do not change amber color to neon. FBF8EE/6B5A1E passes AA — layout position change only.",
  },
  {
    id: "C6", phase: 1 as const, action: "extend" as const,
    name: "ScoreChip — lg variant",
    file: "src/components/shared/score-chip.tsx + bari-comparison-tokens.ts",
    description: "Add size='lg' variant: 48px tall, score numeral 20px, grade letter 13px, left-border 5px. Same gradePalette tokens. For HomeHero trust bar and hashvaot featured cards only.",
    constraint: "Frozen: do not change sm (row) geometry. lg is additive. Circular geometry rejected — keep left-accent-border.",
  },
  {
    id: "C7", phase: 1 as const, action: "extend" as const,
    name: "MicroComparisonSnapshotCard — photography mode",
    file: "src/components/home/micro-comparison-snapshot-card.tsx",
    description: "Add optional showImages prop: when true, product image 44×44px (--radius-sm, object-fit: contain on white). ScoreChip scales to lg variant (C6). Max 3 products per card. No card height increase beyond image height.",
    constraint: "Max 3 products. No extra copy lines.",
  },
  {
    id: "C8", phase: 1 as const, action: "restyle" as const,
    name: "home-comparisons — carousel section header",
    file: "src/components/home/home-comparisons.tsx",
    description: "Replace section heading with bari-eyebrow kicker + bari-h2 title naming a category finding. E.g. 'בדקנו 81 מוצרים בלחם — הנה מה שמצאנו'. No stat aggregate in subhead.",
    constraint: "Copy: Content Agent + QA gate. No stat-aggregate subheads ('X% of products...').",
  },
  {
    id: "C9", phase: 2 as const, action: "extend" as const,
    name: "ComparisonIntelligenceHero — product strip",
    file: "src/components/comparisons/comparison-intelligence-hero.tsx",
    description: "Add horizontal product strip (top-3-ranked, 56×72px white cards, --shadow-sm, --radius-md) below hero copy. No scores in strip — scores live in rows. Stays inside Hero section (section 1 of 4).",
    constraint: "Max 3 images. Degrades gracefully if no images available. No score shown in strip.",
  },
  {
    id: "C10", phase: 2 as const, action: "extend" as const,
    name: "CategoryPrologue — marketing-vs-reality callout",
    file: "src/components/shared/category-prologue.tsx",
    description: "Add optional marketingVsReality prop: one sentence surfacing the gap between front-of-pack claims and Bari's finding. Renders as borderless blockquote-style line in --fg2 with --bari-green left border (3px). Content Agent authored.",
    constraint: "One sentence. No icons, no chart, no percentage. Must be sourced from a real scoring finding. Content gate required.",
  },
  {
    id: "C11", phase: 2 as const, action: "new" as const,
    name: "OGImageTemplate — category share card",
    file: "src/app/og/[category]/route.tsx (new)",
    description: "Static OG image via @vercel/og: 1200×630 with category name, top-3 product images, grade chips A-E ramp, Bari wordmark. Server route only. No interactive share UI on comparison pages.",
    constraint: "Server-only. OG image shows grade letters only, not numerics (scores can be stale).",
  },
  {
    id: "C12", phase: 2 as const, action: "restyle" as const,
    name: "FilterFAB — label refresh",
    file: "src/components/comparisons/comparison-page.tsx (filter trigger)",
    description: "Rename filter FAB from icon to label pill: 'סינון' + count badge ('3' when all 3 dimensions active). --bari-green active-state background. Collapsed at 0px scroll, sticky after 300px — frozen timing unchanged.",
    constraint: "Frozen: 3-dimension max. Timing unchanged. No barcode scanner added.",
  },
];

const ANTIPATTERNS = [
  { pattern: "Dark-only primary theme", why: "Consumer-facing irreversible brand change (tripwire #2). Requires owner-level decision. Also breaks the warm-paper-canvas identity that anchors the 'paper investigation' feel." },
  { pattern: "Circular / pill score chips", why: "Destroys left-border grade accent encoding three simultaneous signals (color, position, border width). Frozen by gradePalette spec." },
  { pattern: "Radar chart above product rows", why: "Hard dashboard drift: visualization before the first row. Users must interpret a chart before seeing a product. Also requires a stable axis set that doesn't exist across all 12 categories." },
  { pattern: "Guess-the-score gamification", why: "Hard drift: user must make a choice before seeing a product (Drift Detection #2). Score is evidence, not a quiz answer. Contradicts 'clarity over cleverness'." },
  { pattern: "Aggregate statistics in hero", why: "'67% are NOVA 4' before rows = Drift Detection #4. Creates anxiety without context. Findings are explained by the rows themselves." },
  { pattern: "Neon warning flags", why: "Untested against WCAG 1.4.3. Neon on dark at 10-11px fails at 3:1. The existing amber claimShortfallFlag palette already passes AA — do not replace it." },
  { pattern: "Digital Cart health score", why: "New scoring philosophy — triggers tripwire #1. Requires BSIP governance decision and category methodology rewrite. Not a design decision." },
  { pattern: "Generic card-grid default layout", why: "Listed explicitly in bari-frontend-ui forbidden patterns. Not every section needs the same card style. Mix open sections with cards." },
];

const WIREFRAMES = [
  { id: "W1", route: "/", change: "HomeHero: product photography strip (C1) + grade-chip trust bar (C2). Carousel section header copy (C8).", size: "375px + 1280px" },
  { id: "W2", route: "/hashvaot", change: "HashvaotCategoryBox LiveCard: mini thumbnail strip (C3), remove heroStat aggregate.", size: "375px" },
  { id: "W3", route: "/hashvaot/[category]", change: "CategoryHero: optional insightLine prop (C4). claimShortfall prominence (C5).", size: "375px + 1280px" },
  { id: "W4", route: "ScoreChip lg variant", change: "Component spec: lg size tokens, left-border 5px, gradePalette unchanged. HomeHero + carousel use only.", size: "Component only" },
  { id: "W5", route: "home carousel", change: "MicroComparisonSnapshotCard: showImages=true, ScoreChip lg (C6, C7).", size: "375px" },
];

function RiskPill({ level }: { level: "low" | "medium" | "high" }) {
  const colors = { low: "#1F8F6A", medium: "#B8860B", high: "#B42318" };
  const labels = { low: "Low risk", medium: "Medium risk", high: "High risk" };
  return <span style={{ color: colors[level], fontSize: 11, fontWeight: 600 }}>{labels[level]}</span>;
}

function PhaseTag({ phase }: { phase: 1 | 2 }) {
  const theme = useHostTheme();
  return (
    <span style={{ fontSize: 10, fontWeight: 700, padding: "2px 7px", borderRadius: 99, background: phase === 1 ? theme.fill.secondary : theme.fill.tertiary, color: phase === 1 ? theme.text.primary : theme.text.tertiary }}>
      Phase {phase}
    </span>
  );
}

function ActionTag({ action }: { action: "extend" | "new" | "restyle" }) {
  const theme = useHostTheme();
  return (
    <span style={{ fontSize: 10, fontWeight: 600, color: action === "new" ? theme.accent.primary : theme.text.tertiary }}>
      {action === "new" ? "new file" : action}
    </span>
  );
}

function BundleCard({ id }: { id: BundleId }) {
  const b = BUNDLES[id];
  const theme = useHostTheme();
  return (
    <Card>
      <CardHeader trailing={<RiskPill level={b.riskLevel} />}>{b.label}</CardHeader>
      <CardBody>
        <Stack gap={12}>
          <Text tone="secondary" size="small">{b.summary}</Text>
          <div>
            <Text weight="semibold" size="small" style={{ marginBottom: 4 }}>Adopt</Text>
            {b.adopts.map((a, i) => (
              <Text key={i} size="small" tone="secondary" style={{ display: "flex", gap: 6, marginBottom: 3 }}>
                <span style={{ color: "#1F8F6A", flexShrink: 0 }}>+</span>{a}
              </Text>
            ))}
          </div>
          <Divider />
          <div>
            <Text weight="semibold" size="small" style={{ marginBottom: 4, color: "#B42318" }}>Reject</Text>
            {b.rejects.map((r, i) => (
              <Text key={i} size="small" tone="secondary" style={{ display: "flex", gap: 6, marginBottom: 3 }}>
                <span style={{ color: "#B42318", flexShrink: 0 }}>x</span>{r}
              </Text>
            ))}
          </div>
        </Stack>
      </CardBody>
    </Card>
  );
}

function ComponentCard({ c }: { c: typeof COMPONENTS[number] }) {
  const theme = useHostTheme();
  return (
    <Card collapsible defaultOpen={c.phase === 1}>
      <CardHeader trailing={<Row gap={6} align="center"><PhaseTag phase={c.phase} /><ActionTag action={c.action} /></Row>}>
        {c.id} · {c.name}
      </CardHeader>
      <CardBody>
        <Stack gap={8}>
          <Text size="small" tone="tertiary" style={{ fontFamily: "monospace" }}>{c.file}</Text>
          <Text size="small">{c.description}</Text>
          <div style={{ borderInlineStart: "3px solid", borderInlineStartColor: theme.stroke.secondary, paddingInlineStart: 8 }}>
            <Text size="small" tone="secondary">
              <Text as="span" weight="semibold" size="small">Constraint: </Text>{c.constraint}
            </Text>
          </div>
        </Stack>
      </CardBody>
    </Card>
  );
}

export default function GenZDesignReview() {
  const [activeSection, setActiveSection] = useState<"bundles" | "components" | "tokens" | "wireframes" | "antipatterns">("bundles");
  const theme = useHostTheme();

  const sections = [
    { id: "bundles" as const, label: "Bundle Assessment" },
    { id: "components" as const, label: "Component Roadmap" },
    { id: "tokens" as const, label: "Token / Palette" },
    { id: "wireframes" as const, label: "Phase 1 Wireframes" },
    { id: "antipatterns" as const, label: "Anti-Patterns" },
  ];

  return (
    <Stack gap={24} style={{ padding: 24, maxWidth: 900, margin: "0 auto" }}>
      <Stack gap={4}>
        <Text tone="tertiary" size="small" weight="semibold" style={{ letterSpacing: "0.1em", textTransform: "uppercase" }}>
          Design Agent · Bari
        </Text>
        <H1>Project Gen Z — Direction & Component Roadmap</H1>
        <Text tone="secondary">
          Synthesis of Bundles A, B, C against the frozen Gen 1 spec. No rebrand. Selective evolution within the existing token system.
        </Text>
      </Stack>

      <div style={{ borderInlineStart: "4px solid #1F8F6A", paddingInlineStart: 16, paddingBlock: 4 }}>
        <Text weight="semibold" style={{ marginBottom: 6 }}>Direction Statement</Text>
        <Text tone="secondary">{DIRECTION_STATEMENT}</Text>
      </div>

      <Grid columns={4} gap={12}>
        <Stat value="3" label="Bundles reviewed" />
        <Stat value="12" label="Components scoped" />
        <Stat value="5" label="Phase 1 wireframes" />
        <Stat value="8" label="Anti-patterns flagged" />
      </Grid>

      <Row gap={8} wrap>
        {sections.map(s => (
          <Pill key={s.id} active={activeSection === s.id} onClick={() => setActiveSection(s.id)}>
            {s.label}
          </Pill>
        ))}
      </Row>

      <Divider />

      {activeSection === "bundles" && (
        <Stack gap={16}>
          <H2>Bundle Assessment</H2>
          <Callout tone="info" title="Synthesis, not wholesale adoption">
            No bundle is adopted in full. Each is audited against the frozen Gen 1 spec and the bari-frontend-ui skill. Items that pass are harvested; items that fail are rejected with a named rule citation.
          </Callout>
          <Grid columns={1} gap={12}>
            <BundleCard id="A" />
            <BundleCard id="B" />
            <BundleCard id="C" />
          </Grid>
          <Callout tone="warning" title="Bundle B — owner escalation required">
            Bundle B's dark-mode-primary proposal trips strategic tripwire #2 (irreversible AND consumer-facing brand change).
            This cannot be decided within the Design Agent lane. Escalate to the owner before any dark-mode implementation begins.
            The barcode scanner intent can be logged as a product backlog item without a design commitment now.
          </Callout>
        </Stack>
      )}

      {activeSection === "components" && (
        <Stack gap={16}>
          <H2>Component Roadmap</H2>
          <Text tone="secondary">
            12 concrete solutions tied to existing codebase files. Phase 1 (8 items) ships without touching the 12 category pages.
            Phase 2 (4 items) requires a category page deploy.
          </Text>
          <Grid columns={4} gap={12}>
            <Stat value="8" label="Phase 1 items" />
            <Stat value="4" label="Phase 2 items" />
            <Stat value="0" label="New score axes" />
            <Stat value="0" label="Dark mode changes" />
          </Grid>
          <H3>Phase 1 — No category page required</H3>
          <Stack gap={8}>
            {COMPONENTS.filter(c => c.phase === 1).map(c => <ComponentCard key={c.id} c={c} />)}
          </Stack>
          <H3>Phase 2 — Requires category page deploy</H3>
          <Stack gap={8}>
            {COMPONENTS.filter(c => c.phase === 2).map(c => <ComponentCard key={c.id} c={c} />)}
          </Stack>
        </Stack>
      )}

      {activeSection === "tokens" && (
        <Stack gap={16}>
          <H2>Token / Palette Proposal</H2>
          <Callout tone="success" title="Minimal delta — 2 additions only">
            The existing token system in colors_and_type.css requires only 2 new tokens.
            All other tokens remain frozen. No new color families, no orange, no neon.
          </Callout>
          <Table
            headers={["Token", "Value", "Role"]}
            striped
            rowTone={[undefined, undefined, undefined, undefined, undefined, "info", "info"]}
            rows={PALETTE_ROWS.map(([token, hex, role]) => [
              <Text key={token} size="small" style={{ fontFamily: "monospace" }}>{token}</Text>,
              <Text key={hex} size="small" tone="secondary">{hex}</Text>,
              <Text key={role} size="small">{role}</Text>,
            ])}
          />
          <H3>Grade Palette — Frozen</H3>
          <Text tone="secondary" size="small">
            The 5-grade A-E ramp (green to olive/gold to amber to orange to red) is frozen by owner directive 2026-06-03.
            No new grade colors. No circular chips. No second color axis per product.
            gradePalette in bari-comparison-tokens.ts is read-only for this phase.
          </Text>
          <H3>Typography — Frozen</H3>
          <Text tone="secondary" size="small">
            Inter/Heebo stack, 800-weight headings, negative tracking: unchanged.
            bari-eyebrow (mono uppercase, 0.65rem, 0.24em tracking) is the recommended Gen Z addition — it already exists in the system.
          </Text>
        </Stack>
      )}

      {activeSection === "wireframes" && (
        <Stack gap={16}>
          <H2>Phase 1 Wireframe List</H2>
          <Text tone="secondary">
            5 wireframes cover all Phase 1 component changes. Each requires review at 375px mobile first, then 1280px desktop (Design Agent hard rule #1: see it before you judge it).
          </Text>
          <Callout tone="neutral" title="Vision-in requirement">
            These are spec wireframes. No design verdict can be issued until the actual render is reviewed via Playwright screenshot + getBoundingClientRect geometry at 375px.
            The Vision-in loop is currently PROPOSED (to build). Until it exists, these are implementation specs pending visual sign-off.
          </Callout>
          <Table
            headers={["ID", "Route", "Change scope", "Viewport"]}
            striped
            rows={WIREFRAMES.map(w => [
              <Text key={w.id} size="small" weight="semibold">{w.id}</Text>,
              <Text key={w.route} size="small" style={{ fontFamily: "monospace" }}>{w.route}</Text>,
              <Text key={w.change} size="small">{w.change}</Text>,
              <Text key={w.size} size="small" tone="tertiary">{w.size}</Text>,
            ])}
          />
          <H3>Content Sign-off Gate</H3>
          <Text tone="secondary" size="small">
            Wireframes carrying consumer-facing copy (C4 insightLine, C8 section header, C10 marketing-vs-reality) require Content Agent authoring + Adversarial QA gate sign-off before implementation.
            Structural wireframes with no copy (C1, C3, C6) can be implemented and reviewed visually without the content gate.
          </Text>
        </Stack>
      )}

      {activeSection === "antipatterns" && (
        <Stack gap={16}>
          <H2>What Not To Do</H2>
          <Text tone="secondary">
            8 named anti-patterns across the three bundles. Each cited to a specific rule. These are design stops — not preferences — and must not appear in any implementation PR.
          </Text>
          <Stack gap={8}>
            {ANTIPATTERNS.map((ap, i) => (
              <Card key={i}>
                <CardHeader trailing={<Text size="small" tone="tertiary" as="span">Stop</Text>}>{ap.pattern}</CardHeader>
                <CardBody><Text size="small" tone="secondary">{ap.why}</Text></CardBody>
              </Card>
            ))}
          </Stack>
        </Stack>
      )}
    </Stack>
  );
}
