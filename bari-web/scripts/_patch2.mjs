import { readFileSync, writeFileSync } from "fs";
let d = readFileSync("src/lib/home/homepage-carousel-data.ts", "utf8");
d = d.replace(
  /evidence: "67[^"]+"/,
  'evidence: Math.round(SNACKS_GRADE_DIST.high) + " \u05e2\u05d3 " + Math.round(SNACKS_GRADE_DIST.low) + " \u2014 \u05d0\u05d5\u05ea\u05d4 \u05e7\u05d8\u05d2\u05d5\u05e8\u05d9\u05d4, \u05e2\u05d5\u05dc\u05de\u05d5\u05ea \u05e9\u05d5\u05e0\u05d9\u05dd. \u05d4\u05de\u05d5\u05d1\u05d9\u05dc: \u05ea\u05de\u05e8\u05d9\u05dd \u05d5\u05e7\u05d9\u05e0\u05de\u05d5\u05df \u05d1\u05dc\u05d1\u05d3."'
);
writeFileSync("src/lib/home/homepage-carousel-data.ts", d);

// scroll into view for deep links
let t = readFileSync("src/components/shared/comparison-table.tsx", "utf8");
if (!t.includes("scrollIntoView")) {
  t = t.replace(
    'import { Fragment, useCallback, useMemo, useRef, useState } from "react";',
    'import { Fragment, useCallback, useEffect, useMemo, useRef, useState } from "react";'
  );
  t = t.replace(
    "  const onToggle = useCallback((id: string) => {",
    `  useEffect(() => {
    if (!initialExpandedProductId) return;
    const el = rowRefs.current.get(initialExpandedProductId);
    if (el) {
      requestAnimationFrame(() => {
        el.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    }
  }, [initialExpandedProductId]);

  const onToggle = useCallback((id: string) => {`
  );
  writeFileSync("src/components/shared/comparison-table.tsx", t);
}
console.log("patched");
