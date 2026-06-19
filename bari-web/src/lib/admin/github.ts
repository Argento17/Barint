/**
 * Admin copy editor — GitHub read/write of the live comparison JSON files.
 *
 * The live site (bari.digital) deploys from Argento17/Barint, branch master,
 * root dir bari-web. We read the current JSON straight from that repo (so the
 * editor always reflects the deployed source) and write edits back as a commit,
 * which triggers a Vercel rebuild. The data file stays the single source of
 * truth — no separate database, no drift.
 *
 * Required env (Vercel secrets + .env.local):
 *   ADMIN_GITHUB_TOKEN    a fine-grained PAT with Contents: read/write on the repo
 *   ADMIN_GITHUB_REPO     "owner/name"   (default "Argento17/Barint")
 *   ADMIN_GITHUB_BRANCH   branch          (default "master")
 */
const API = "https://api.github.com";
const DIR = "bari-web/src/data/comparisons";

function cfg() {
  const token = process.env.ADMIN_GITHUB_TOKEN || "";
  const repo = process.env.ADMIN_GITHUB_REPO || "Argento17/Barint";
  const branch = process.env.ADMIN_GITHUB_BRANCH || "master";
  return { token, repo, branch };
}

export function githubConfigured(): boolean {
  return Boolean(process.env.ADMIN_GITHUB_TOKEN);
}

async function gh(path: string, init?: RequestInit): Promise<Response> {
  const { token } = cfg();
  return fetch(`${API}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "bari-admin-copy-editor",
      ...(init?.headers || {}),
    },
    cache: "no-store",
  });
}

export interface FetchedFile {
  data: { _meta?: Record<string, unknown>; products?: Record<string, unknown>[] };
  sha: string;
}

/** Fetch + parse one comparison file. Returns the parsed JSON and its blob sha. */
export async function getComparisonFile(file: string): Promise<FetchedFile> {
  const { repo, branch } = cfg();
  const res = await gh(
    `/repos/${repo}/contents/${DIR}/${encodeURIComponent(file)}?ref=${encodeURIComponent(branch)}`,
  );
  if (!res.ok) {
    throw new Error(`GitHub getFile ${file} failed: ${res.status} ${await res.text()}`);
  }
  const body = (await res.json()) as { content: string; sha: string; encoding: string };
  const raw = Buffer.from(body.content, body.encoding === "base64" ? "base64" : "utf8").toString("utf8");
  return { data: JSON.parse(raw), sha: body.sha };
}

/**
 * Commit new content for one comparison file. `sha` must be the current blob
 * sha (optimistic concurrency — GitHub rejects a stale sha, which protects
 * against overwriting a change made since load).
 */
export async function putComparisonFile(
  file: string,
  data: unknown,
  sha: string,
  message: string,
): Promise<{ commitSha: string }> {
  const { repo, branch } = cfg();
  const text = JSON.stringify(data, null, 2);
  const res = await gh(`/repos/${repo}/contents/${DIR}/${encodeURIComponent(file)}`, {
    method: "PUT",
    body: JSON.stringify({
      message,
      content: Buffer.from(text, "utf8").toString("base64"),
      sha,
      branch,
    }),
  });
  if (!res.ok) {
    throw new Error(`GitHub putFile ${file} failed: ${res.status} ${await res.text()}`);
  }
  const body = (await res.json()) as { commit: { sha: string } };
  return { commitSha: body.commit.sha };
}
