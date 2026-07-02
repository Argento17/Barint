const fs = require("fs");
const p = "src/lib/admin/github.ts";
let s = fs.readFileSync(p, "utf8");
if (!s.includes("SITE_CONTENT_REPO_DIR")) {
  s = s.replace(
    'const DIR = "bari-web/src/data/comparisons";',
    'const DIR = "bari-web/src/data/comparisons";\nexport const SITE_CONTENT_REPO_DIR = "bari-web/src/data/site-content";',
  );
  const append = `

export function getSiteContentFile(file: string): Promise<FetchedFile> {
  return getRepoJson<FetchedFile["data"]>(\`\${SITE_CONTENT_REPO_DIR}/\${file}\`);
}

export function putSiteContentFile(
  file: string,
  data: unknown,
  sha: string,
  message: string,
): Promise<{ commitSha: string }> {
  return putRepoJson(\`\${SITE_CONTENT_REPO_DIR}/\${file}\`, data, sha, message);
}
`;
  s = s.trimEnd() + append;
  fs.writeFileSync(p, s, "utf8");
  console.log("patched github.ts");
} else {
  console.log("already patched");
}
