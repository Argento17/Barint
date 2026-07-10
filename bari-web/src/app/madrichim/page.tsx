// Madrichim (מדריכים) hub — TASK-504 Wave 0 skeleton.
// Mirrors /hashvaot/page.tsx structure (HomeContainer shell, HashvaotCategoryBox grid,
// back links) — see 01_framework/frontend/component_build_sequence_v1.md pattern-reuse
// convention. Kept as a SEPARATE hub from /hashvaot per the concrete plan (§5): this is
// not a new tab on the food/supplements index, it is the new home for supplement guides.
//
// ────────────────────────────────────────────────────────────────────────────────────
// MIGRATION TODO (Wave 3, plan §5 — single PR, zero overlap window). Do NOT do any of
// this in the Wave 0/1/2 spikes. This block exists so the migration PR has an exact
// file list instead of re-deriving it from scratch:
//
//   1. next.config.ts
//      - Add `redirects()` (none exist yet — this repo currently has no redirects
//        config block at all):
//          /hashvaot/magnesium   -> /madrichim/magnesium   (permanent)
//          /hashvaot/creatine    -> /madrichim/creatine    (permanent)
//          /hashvaot/supplements -> /madrichim             (permanent)
//
//   2. src/lib/seo/sitemap-paths.ts
//      - Remove "/hashvaot/magnesium" (line ~19).
//      - Add "/madrichim", "/madrichim/magnesium", "/madrichim/creatine".
//      - NOTE (found during this spike, not caused by it): "/hashvaot/creatine" and
//        "/hashvaot/supplements" are NOT in this file today even though both routes are
//        live — a pre-existing sitemap gap. The migration PR should add the /madrichim
//        equivalents rather than assume it is "swapping" existing creatine/supplements
//        entries that don't exist.
//
//   3. src/app/hashvaot/supplements/page.tsx — DELETE (superseded by this hub).
//   4. src/app/hashvaot/magnesium/page.tsx — DELETE (content moves to
//      src/app/madrichim/magnesium/page.tsx once the real magnesium guide ships).
//   5. src/app/hashvaot/creatine/ — DELETE (content moves to
//      src/app/madrichim/creatine/page.tsx once the real creatine guide ships).
//   6. src/lib/hashvaot/hashvaot-categories.ts — remove the "supplements" entry
//      (id: "supplements", lines ~40-48) from HASHVAOT_CATEGORIES.
//   7. src/lib/guides/madrichim-categories.ts — replace the placeholder
//      "supplement-guides" building-card entry with real "live" entries for
//      magnesium + creatine (href, description, heroStat).
//   8. Any internal links to /hashvaot/magnesium, /hashvaot/creatine, or
//      /hashvaot/supplements (e.g. TASK-492B functional-dairy blog per the plan §7 note)
//      — repoint to /madrichim/... directly rather than relying solely on the redirect.
//
//   Both live pages (/hashvaot/magnesium, /hashvaot/creatine) stay untouched until the
//   guide replacements are built and gated (plan §6) — this migration only runs once,
//   together with the hub, per plan §5 "no one-guide hub, no half-state."
// ────────────────────────────────────────────────────────────────────────────────────

import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

import { HomeContainer } from "@/components/home/section-frame";
import { HashvaotCategoryBox } from "@/components/hashvaot/hashvaot-category-box";
import { MADRICHIM_CATEGORIES } from "@/lib/guides/madrichim-categories";
import { cn } from "@/lib/utils";
import { siteHeaderOffsetClass } from "@/lib/site-layout";

// TASK-504B residual fix (coordinator verification pass): the prior description used
// the banned ranking word "דירוג" plus antithesis phrasing ("...לעבור, לא דירוג") and
// an em-dash. Rewritten as a positive declarative naming the guide's actual mechanism
// (fixed bars a product must clear), brand-anchored, no negation construct.
export const metadata: Metadata = {
  title: "מדריכים | Bari",
  description: "מדריכי הקנייה של בארי בודקים אילו ספים תוסף תזונה צריך לעבור כדי להיחשב בחירה טובה.",
};

export default function MadrichimIndexPage() {
  return (
    <main
      className={cn(
        "relative min-h-screen bg-[#F7F7F2] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <HomeContainer className="relative py-14 md:py-20">
        {/* OLI as explorer, top-left of the hub (RTL: opposite the title block).
            Decorative — same idiom as the homepage LUMO (home-guides.tsx). */}
        <Image
          src="/mascots/mascot-oli-madrichim-explorer.webp"
          alt=""
          width={800}
          height={640}
          aria-hidden
          className="pointer-events-none absolute left-0 top-14 hidden w-44 lg:block xl:w-52"
        />
        {/* TASK-504B: color-only AA-contrast fix (was #1F8F6A/80 ≈2.8:1; #0F5C42 solid
            ≈7.4:1) — see GUIDE_SECTION_EYEBROW_CLASS note in bari-comparison-tokens.ts
            for the shared sectionEyebrow debt this mirrors. */}
        <p className="text-xs font-bold uppercase tracking-[0.22em] text-[#0F5C42]">
          Bari · מדריכים
        </p>
        <h1 className="mt-3 max-w-3xl text-balance text-4xl font-extrabold tracking-[-0.05em] md:text-5xl">
          מדריכים
        </h1>
        {/* TASK-504B residual fix: removed the "מדורג" ranking word + "לא...מול" antithesis
            clause. Positive framing: fixed, uniform bars replace a ranking mechanism, without
            naming or negating the ranking concept. */}
        <p className="mt-5 max-w-2xl text-pretty text-lg leading-relaxed text-[#4E5663]">
          מדריך קנייה בודק אם מוצר עומד בספים קבועים שקובעים אם הוא שווה קנייה, אותם
          ספים בדיוק לכל המוצרים בקטגוריה.
        </p>

        <div className="mt-12 grid gap-5 sm:grid-cols-2">
          {MADRICHIM_CATEGORIES.map((cat) => (
            <HashvaotCategoryBox key={cat.id} category={cat} />
          ))}
        </div>

        <div className="mt-10 flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-6">
          <Link
            href="/hashvaot"
            className="inline-flex items-center gap-2 text-sm font-semibold text-[#4E5663] transition-colors hover:text-[#111318]"
          >
            <ArrowLeft className="size-4" aria-hidden />
            להשוואות מהמדף
          </Link>
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-sm font-semibold text-[#4E5663] transition-colors hover:text-[#111318]"
          >
            <ArrowLeft className="size-4" aria-hidden />
            חזרה לדף הבית
          </Link>
        </div>
      </HomeContainer>
    </main>
  );
}
