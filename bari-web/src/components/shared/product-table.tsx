"use client";

import { useCallback, useState } from "react";

import { useComparisonLayout } from "@/lib/comparisons/comparison-layout-context";
import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";
import type { BariProductVM } from "@/lib/view-models";
import { ProductRow } from "./product-row";
import { ProductTableHeader } from "./product-table-header";

export function ProductTable({
  products,
  initialExpandedProductId = null,
}: {
  products: BariProductVM[];
  initialExpandedProductId?: string | null;
}) {
  const layout = useComparisonLayout();
  const [expandedProductId, setExpandedProductId] = useState<string | null>(
    initialExpandedProductId
  );

  const handleToggleProduct = useCallback((productId: string) => {
    setExpandedProductId((current) => (current === productId ? null : productId));
  }, []);

  return (
    <div
      className={cn(
        BARI_COMPARISON_TOKENS.rows.zebraContainerClass,
        layout === "web" && "bari-zebra-rows--web"
      )}
    >
      <ProductTableHeader productCount={products.length} />
      {products.map((product, index) => (
        <ProductRow
          key={product.id}
          product={product}
          rank={index + 1}
          expanded={expandedProductId === product.id}
          onToggleProduct={handleToggleProduct}
          imagePriority={index < 2}
        />
      ))}
    </div>
  );
}
