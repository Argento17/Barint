const fs=require("fs");
for (const f of ["protein-bars-comparison-page-data.ts","chocolate-bars-comparison-page-data.ts","snacks-comparison-page-data.ts"]) {
  const t=fs.readFileSync("src/lib/comparisons/"+f,"utf8");
  const m=t.match(/@\/data\/comparisons\/([^\s"]+)/);
  console.log(f, m&&m[1]);
}
