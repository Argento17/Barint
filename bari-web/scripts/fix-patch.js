const fs = require("fs");
let t = fs.readFileSync("scripts/mk-expand.js", "utf8");
const neu = `function patchPageData(file, slug) {
  patch(path.join("src/lib/comparisons", file), (t) => {
    if (t.includes("getComparisonPageChrome")) return t;
    const heroM = t.match(/export const (\\w+)Hero\\b/);
    if (!heroM) return t;
    const pfx = heroM[1];
    const metaM = t.match(/export const (\\w+(?:Comparison)?Metadata)\\b/);
    const metaName = metaM ? metaM[1] : pfx + "ComparisonMetadata";
    t = t.replace(
      /import type \\{ Metadata \\} from "next";\\r?\\n/,
      'import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";\\nimport type { Metadata } from "next";\\n',
    );
    t = t.replace(/export const \\w+Hero = [\\s\\S]*?as const;\\r?\\n\\r?\\n/g, "");
    t = t.replace(/export const \\w+PrologueSentences = [\\s\\S]*?as const;\\r?\\n\\r?\\n/g, "");
    t = t.replace(/export const \\w+CategoryNote = [\\s\\S]*?;\\r?\\n\\r?\\n/g, "");
    t = t.replace(/export const \\w+MethodologyLines = [\\s\\S]*?;\\r?\\n\\r?\\n/g, "");
    t = t.replace(/export const \\w+(?:Comparison)?Metadata: Metadata = [\\s\\S]*?};\\r?\\n\\r?\\n/g, "");
    const chromeVar = pfx + "PageChrome";
    const block = [
      "",
      "const " + chromeVar + ' = getComparisonPageChrome("' + slug + '");',
      "export const " + pfx + "Hero = " + chromeVar + ".hero;",
      "export const " + pfx + "PrologueSentences = " + chromeVar + ".prologue;",
      "export const " + pfx + "CategoryNote = " + chromeVar + ".categoryNote;",
      "export const " + pfx + "MethodologyLines = " + chromeVar + ".methodology;",
      "export const " + metaName + ": Metadata = " + chromeVar + ".metadata;",
      "",
    ].join("\\n");
    const fnM = t.match(/export function get\\w+PageData/);
    if (fnM) t = t.replace(fnM[0], block + fnM[0]);
    else t += block;
    return t;
  });
}`;
const start = t.indexOf("function patchPageData");
const end = t.indexOf("for (const [file, slug] of PAGE_DATA_FILES)");
t = t.slice(0, start) + neu + "\n\n" + t.slice(end);
fs.writeFileSync("scripts/mk-expand.js", t);
console.log("fixed");
