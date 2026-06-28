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
export const SITE_CONTENT_REPO_DIR = "bari-web/src/data/site-content";

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

export interface FetchedJson<T = Record<string, unknown>> {
  data: T;
  sha: string;
}

/** Fetch + parse a JSON file at an arbitrary repo path (relative to repo root). */
export async function getRepoJson<T = Record<string, unknown>>(
  repoPath: string,
): Promise<FetchedJson<T>> {
  const { repo, branch } = cfg();
  const encoded = repoPath.split("/").map(encodeURIComponent).join("/");
  const res = await gh(`/repos/${repo}/contents/${encoded}?ref=${encodeURIComponent(branch)}`);
  if (!res.ok) {
    throw new Error(`GitHub getFile ${repoPath} failed: ${res.status} ${await res.text()}`);
  }
  const body = (await res.json()) as { content: string; sha: string; encoding: string };
  const raw = Buffer.from(body.content, body.encoding === "base64" ? "base64" : "utf8").toString("utf8");
  return { data: JSON.parse(raw) as T, sha: body.sha };
}

/**
 * Commit new content for a JSON file at an arbitrary repo path. `sha` must be
 * the current blob sha (optimistic concurrency — GitHub rejects a stale sha,
 * protecting against overwriting a change made since load).
 */
export async function putRepoJson(
  repoPath: string,
  data: unknown,
  sha: string,
  message: string,
): Promise<{ commitSha: string }> {
  const { repo, branch } = cfg();
  const text = JSON.stringify(data, null, 2);
  const encoded = repoPath.split("/").map(encodeURIComponent).join("/");
  const res = await gh(`/repos/${repo}/contents/${encoded}`, {
    method: "PUT",
    body: JSON.stringify({
      message,
      content: Buffer.from(text, "utf8").toString("base64"),
      sha,
      branch,
    }),
  });
  if (!res.ok) {
    throw new Error(`GitHub putFile ${repoPath} failed: ${res.status} ${await res.text()}`);
  }
  const body = (await res.json()) as { commit: { sha: string } };
  return { commitSha: body.commit.sha };
}

export interface FetchedFile {
  data: { _meta?: Record<string, unknown>; products?: Record<string, unknown>[] };
  sha: string;
}

/** Fetch + parse one comparison file (thin wrapper over getRepoJson). */
export function getComparisonFile(file: string): Promise<FetchedFile> {
  return getRepoJson<FetchedFile["data"]>(`${DIR}/${file}`);
}

/** Commit new content for one comparison file (thin wrapper over putRepoJson). */
export function putComparisonFile(
  file: string,
  data: unknown,
  sha: string,
  message: string,
): Promise<{ commitSha: string }> {
  return putRepoJson(`${DIR}/${file}`, data, sha, message);
}

export function getSiteContentFile(file: string): Promise<FetchedFile> {
  return getRepoJson<FetchedFile["data"]>(`${SITE_CONTENT_REPO_DIR}/${file}`);
}

export function putSiteContentFile(
  file: string,
  data: unknown,
  sha: string,
  message: string,
): Promise<{ commitSha: string }> {
  return putRepoJson(`${SITE_CONTENT_REPO_DIR}/${file}`, data, sha, message);
}
