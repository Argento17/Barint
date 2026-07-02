import { readFileSync, writeFileSync } from "fs";
const p = "src/components/shared/comparison-table.tsx";
let s = readFileSync(p, "utf8");
if (!s.includes("scrollIntoView")) {
  s = s.replace(
    "import { Fragment, useCallback, useMemo, useRef, useState }",
    "import { Fragment, useCallback, useEffect, useMemo, useRef, useState }"
  );
  const insert = `  useEffect(() => {
    if (!initialExpandedProductId) return;
    const el = rowRefs.current.get(initialExpandedProductId);
    if (el) {
      requestAnimationFrame(() => {
        el.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    }
  }, [initialExpandedProductId]);

`;
  s = s.replace("  const onToggle = useCallback((id: string) => {", insert + "  const onToggle = useCallback((id: string) => {");
  writeFileSync(p, s, "utf8");
  console.log("patched");
} else console.log("skip");
