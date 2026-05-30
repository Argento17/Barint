"use client";

import { memo, useEffect, useRef, useState, type KeyboardEvent } from "react";
import Image from "next/image";
import { ChevronDown } from "lucide-react";

import {
  BARI_COMPARISON_TOKENS,
  comparisonRowStripeClass,
  comparisonWebTableGridClass,
} from "@/lib/design/bari-comparison-tokens";
import { useComparisonLayout } from "@/lib/comparisons/comparison-layout-context";
import { cn } from "@/lib/utils";
import type { BariProductVM } from "@/lib/view-models";
import { ExpansionSection } from "./expansion-section";
import { ScoreChip } from "./score-chip";

const ROW_IMAGE_SCALE = 1.18;
const WEB = BARI_COMPARISON_TOKENS.webTable;

const SHELF_IMAGE_PX = Math.round(
  parseInt(BARI_COMPARISON_TOKENS.layout.rowImageSize, 10) * ROW_IMAGE_SCALE
);
const WEB_IMAGE_PX = Math.round(
  parseInt(BARI_COMPARISON_TOKENS.layout.rowImageSizeWeb, 10) * ROW_IMAGE_SCALE
);

function ProductImage({
  product,
  priority = false,
  layout,
}: {
  product: BariProductVM;
  priority?: boolean;
  layout: "shelf" | "web";
}) {
  const size = layout === "web" ? WEB_IMAGE_PX : SHELF_IMAGE_PX;
  const frameClass =
    layout === "web"
      ? "h-[var(--bari-row-img-shelf)] w-[var(--bari-row-img-shelf)] lg:h-[var(--bari-row-img-web)] lg:w-[var(--bari-row-img-web)]"
      : undefined;
  const [failed, setFailed] = useState(false);

  const frameStyle = {
    width: layout === "web" ? undefined : size,
    height: layout === "web" ? undefined : size,
    ["--bari-row-img-shelf" as string]: `${SHELF_IMAGE_PX}px`,
    ["--bari-row-img-web" as string]: `${WEB_IMAGE_PX}px`,
    backgroundColor: "#F8F7F3",
    boxShadow: "inset 0 0 0 1px rgba(17,19,24,0.04)",
  } as const;

  if (!product.imageUrl || failed) {
    return (
      <div
        className={cn("shrink-0 rounded-md", frameClass)}
        style={{
          ...frameStyle,
          backgroundColor: "#F3F3EE",
        }}
        aria-hidden
      />
    );
  }

  return (
    <div
      className={cn("relative shrink-0 overflow-hidden rounded-md", frameClass)}
      style={frameStyle}
    >
      <Image
        src={product.imageUrl}
        alt=""
        width={size}
        height={size}
        sizes={`${size}px`}
        className="h-full w-full object-contain"
        loading={priority ? "eager" : "lazy"}
        priority={priority}
        decoding="async"
        onError={() => setFailed(true)}
        aria-hidden
      />
    </div>
  );
}

function ScoreCell({
  isExpanded,
  product,
}: {
  isExpanded: boolean;
  product: BariProductVM;
}) {
  return (
    <div className="flex shrink-0 items-center justify-center gap-2">
      <ChevronDown
        strokeWidth={1.75}
        aria-hidden
        className={cn(
          "size-3.5 shrink-0 text-[#B5BBB6] transition-transform duration-200 ease-[cubic-bezier(0.22,1,0.36,1)] motion-reduce:transition-none",
          isExpanded && "rotate-180 text-[#9A9FA6]"
        )}
      />
      <ScoreChip score={product.score} grade={product.grade} />
    </div>
  );
}

function ProductTextBlock({
  product,
  variant,
}: {
  product: BariProductVM;
  variant: "mobile" | "desktop";
}) {
  return (
    <div className={cn("min-w-0", variant === "mobile" ? "flex-1 py-3" : "py-0.5")}>
      <p
        className={cn(
          "font-semibold leading-snug tracking-[-0.012em] text-[#111318]",
          variant === "mobile"
            ? "line-clamp-1 text-[15px]"
            : "text-[16px] leading-snug"
        )}
      >
        {product.name}
      </p>
      <p
        className={cn(
          "mt-1.5 text-[#353D39]",
          product.insightLine ? "" : "invisible",
          variant === "mobile"
            ? "line-clamp-2 text-[13px] leading-[1.5]"
            : "line-clamp-3 text-[14px] leading-[1.55]"
        )}
        style={
          variant === "mobile"
            ? {
                fontSize: "13px",
                lineHeight: "1.5",
                minHeight: "2.9375rem",
              }
            : undefined
        }
        aria-hidden={!product.insightLine}
      >
        {product.insightLine || "\u00a0"}
      </p>
    </div>
  );
}

export const ProductRow = memo(function ProductRow({
  product,
  rank,
  expanded,
  onToggleProduct,
  imagePriority = false,
}: {
  product: BariProductVM;
  rank?: number;
  expanded?: boolean;
  onToggleProduct?: (productId: string) => void;
  imagePriority?: boolean;
}) {
  const layout = useComparisonLayout();
  const isWeb = layout === "web";
  const [internalExpanded, setInternalExpanded] = useState(false);
  const rowRef = useRef<HTMLElement>(null);
  const userExpandedRef = useRef(false);
  const isControlled = expanded != null;
  const isExpanded = isControlled ? expanded : internalExpanded;

  const handleToggle = () => {
    const nextExpanded = !isExpanded;
    if (nextExpanded) {
      userExpandedRef.current = true;
    }

    if (onToggleProduct) {
      onToggleProduct(product.id);
      return;
    }
    setInternalExpanded(nextExpanded);
  };

  const handleCollapse = () => {
    if (isControlled) {
      onToggleProduct?.(product.id);
      return;
    }
    setInternalExpanded(false);
  };

  useEffect(() => {
    if (!isExpanded || !userExpandedRef.current || !rowRef.current) return;

    const frame = requestAnimationFrame(() => {
      rowRef.current?.scrollIntoView({
        block: "nearest",
        behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
          ? "instant"
          : "smooth",
      });
    });

    return () => cancelAnimationFrame(frame);
  }, [isExpanded]);

  const stripeClass = rank != null ? comparisonRowStripeClass(rank) : undefined;

  const onRowKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      handleToggle();
    }
  };

  const expansionPanel = isExpanded ? (
    <ExpansionSection
      expansion={product.expansion}
      confidence={product.confidence}
      onCollapse={handleCollapse}
      wide={isWeb}
    />
  ) : null;

  return (
    <article
      ref={rowRef}
      className={cn(
        "bari-shelf-row",
        stripeClass,
        isExpanded ? "" : "bari-shelf-row--idle",
        isWeb && "max-lg:py-1 lg:grid lg:items-start",
        isWeb && comparisonWebTableGridClass(),
        isWeb && WEB.tableInsetClass
      )}
      style={{ scrollMarginBlock: "8px" }}
    >
      {/* Mobile + tablet: frozen shelf row */}
      <div
        role="button"
        tabIndex={0}
        aria-expanded={isExpanded}
        aria-label={product.name}
        onClick={handleToggle}
        onKeyDown={onRowKeyDown}
        className={cn(
          "flex cursor-pointer touch-manipulation items-center gap-2.5 px-4",
          isWeb ? "max-lg:flex lg:hidden" : "flex"
        )}
        style={
          isWeb
            ? undefined
            : { minHeight: BARI_COMPARISON_TOKENS.layout.rowHeightMobile }
        }
      >
        <ProductImage
          key={product.imageUrl ?? product.id}
          product={product}
          priority={imagePriority}
          layout={layout}
        />
        <div className="flex min-w-0 flex-1 items-center gap-2">
          <ProductTextBlock product={product} variant="mobile" />
          <ScoreCell isExpanded={isExpanded} product={product} />
        </div>
      </div>

      <div
        className={cn(
          "grid overflow-hidden transition-[grid-template-rows] duration-200 ease-[cubic-bezier(0.22,1,0.36,1)] motion-reduce:transition-none",
          isWeb && "lg:hidden"
        )}
        style={{ gridTemplateRows: isExpanded ? "1fr" : "0fr" }}
        aria-hidden={!isExpanded}
      >
        <div className="min-h-0">{expansionPanel}</div>
      </div>

      {/* Desktop web: aligned table columns */}
      {isWeb ? (
        <>
          <div
            role="button"
            tabIndex={0}
            aria-expanded={isExpanded}
            aria-label={product.name}
            onClick={handleToggle}
            onKeyDown={onRowKeyDown}
            className={cn(
              "hidden cursor-pointer touch-manipulation lg:contents",
              !isExpanded && "lg:py-2.5",
              isExpanded && "lg:pt-2.5 lg:pb-1"
            )}
          >
            <span
              className="hidden text-center text-[12px] font-semibold tabular-nums text-[#9A9FA6] lg:block lg:self-center"
              aria-hidden
            >
              {rank}
            </span>
            <div className="hidden lg:flex lg:items-center lg:justify-center lg:self-center">
              <ProductImage
                key={`${product.id}-web`}
                product={product}
                priority={imagePriority}
                layout={layout}
              />
            </div>
            <div className="hidden min-w-0 lg:block lg:self-center">
              <ProductTextBlock product={product} variant="desktop" />
            </div>
            <div className="hidden lg:flex lg:items-center lg:justify-center lg:self-center">
              <ScoreCell isExpanded={isExpanded} product={product} />
            </div>
          </div>

          {isExpanded ? (
            <div className="hidden min-w-0 border-t border-[rgba(17,19,24,0.06)] lg:col-start-3 lg:col-end-4 lg:block lg:pb-3 lg:pt-2">
              {expansionPanel}
            </div>
          ) : null}
        </>
      ) : null}
    </article>
  );
});
