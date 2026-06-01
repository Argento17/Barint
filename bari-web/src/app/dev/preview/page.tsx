"use client";

import { useEffect, useState } from "react";

import { MaadanimComparisonPage } from "@/components/comparisons/maadanim-comparison-page";
import {
  maadanimHero,
  maadanimMethodologyLines,
  maadanimPrologueSentences,
  formatMaadanimMetadataLine,
} from "@/lib/comparisons/maadanim-page-data";
import type { BariProductVM } from "@/lib/view-models";

interface MaadanimCorpusPayload {
  _meta: {
    product_count: number;
    generated: string;
  };
  products: BariProductVM[];
}

export default function PreviewPage() {
  const [corpus, setCorpus] = useState<MaadanimCorpusPayload | null>(null);
  const [loadingError, setLoadingError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    fetch("/api/dev/maadanim", { cache: "no-store" })
      .then(async (response) => {
        if (!response.ok) {
          const body = await response.json().catch(() => ({}));
          throw new Error(body?.details ?? "Failed to fetch corpus");
        }
        return response.json() as Promise<MaadanimCorpusPayload>;
      })
      .then((data) => {
        if (!mounted) return;
        setCorpus(data);
        setLoadingError(null);
      })
      .catch((error) => {
        if (!mounted) return;
        setLoadingError(error instanceof Error ? error.message : "Failed to load data");
      });

    return () => {
      mounted = false;
    };
  }, []);

  if (loadingError) {
    return (
      <div className="min-h-screen bg-[#EFEFEB] flex justify-center py-10" dir="rtl">
        <p className="px-4 py-4 text-sm text-[#8B2E2E]">טעינת המוצרים נכשלה: {loadingError}</p>
      </div>
    );
  }

  if (!corpus) {
    return (
      <div className="min-h-screen bg-[#EFEFEB] flex justify-center py-10" dir="rtl">
        <p className="px-4 py-4 text-sm text-[#6E756F]">טוען מוצרים…</p>
      </div>
    );
  }

  return (
    <MaadanimComparisonPage
      products={corpus.products}
      metadataLine={formatMaadanimMetadataLine(
        corpus._meta.product_count,
        corpus._meta.generated
      )}
      hero={maadanimHero}
      prologueSentences={maadanimPrologueSentences}
      methodologyLines={maadanimMethodologyLines}
    />
  );
}
