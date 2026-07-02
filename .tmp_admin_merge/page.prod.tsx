"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

export const dynamic = "force-dynamic";

// ---- Shared types (mirror the API responses) ----
type FieldKind = "text" | "list";

interface EditableField {
  path: string;
  label: string;
  kind: FieldKind;
  value: string | string[];
}

interface EditableProduct {
  id: string;
  name: string;
  score: number | null;
  grade: string | null;
  fields: EditableField[];
}

type DocKind = "comparison" | "blog";

interface CategorySummary {
  kind: DocKind;
  slug: string;
  nameHe: string;
  productCount?: number;
  unavailable?: boolean;
}

interface LoadedCategory {
  kind: DocKind;
  slug: string;
  sha: string;
  nameHe: string;
  products: EditableProduct[];
}

type Draft = Record<string, Record<string, string | string[]>>;

// ---- Helpers ----
function sameValue(a: string | string[], b: string | string[]): boolean {
  return JSON.stringify(a) === JSON.stringify(b);
}

export default function AdminPage() {
  const [status, setStatus] = useState<"loading" | "login" | "ready">("loading");
  const [githubReady, setGithubReady] = useState(true);

  // login
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");

  // data
  const [comparisons, setComparisons] = useState<CategorySummary[]>([]);
  const [blogDocs, setBlogDocs] = useState<CategorySummary[]>([]);
  const [loaded, setLoaded] = useState<LoadedCategory | null>(null);
  const [draft, setDraft] = useState<Draft>({});
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<{ kind: "ok" | "err"; text: string } | null>(null);

  const loadCategories = useCallback(async () => {
    const res = await fetch("/api/admin/categories");
    if (!res.ok) return;
    const data = await res.json();
    setComparisons(data.comparisons ?? []);
    setBlogDocs(data.blog ?? []);
  }, []);

  // ---- session bootstrap ----
  useEffect(() => {
    void (async () => {
      try {
        const res = await fetch("/api/admin/session");
        const data = await res.json();
        setGithubReady(Boolean(data.githubConfigured));
        if (data.authed) {
          setStatus("ready");
          await loadCategories();
        } else {
          setStatus("login");
        }
      } catch {
        setStatus("login");
      }
    })();
  }, [loadCategories]);

  // ---- actions ----
  async function doLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoginError("");
    const res = await fetch("/api/admin/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });
    if (res.ok) {
      setPassword("");
      setStatus("ready");
      const session = await (await fetch("/api/admin/session")).json();
      setGithubReady(Boolean(session.githubConfigured));
      await loadCategories();
    } else if (res.status === 503) {
      setLoginError("ÎöÎóÎòÎ¿ÎÜ Î£ÎÉ Î×ÎòÎÆÎôÎ¿ ÎóÎôÎÖÎÖÎƒ (ÎùÎíÎ¿ÎÖÎØ ÎíÎòÎôÎòÎ¬ ÎæÎ®Î¿Î¬).");
    } else {
      setLoginError("ÎíÎÖÎíÎ×Îö Î®ÎÆÎòÎÖÎö.");
    }
  }

  async function doLogout() {
    await fetch("/api/admin/logout", { method: "POST" });
    setLoaded(null);
    setDraft({});
    setStatus("login");
  }

  async function openCategory(slug: string, kind: DocKind) {
    setNotice(null);
    setBusy(true);
    setLoaded(null);
    setDraft({});
    try {
      const res = await fetch(`/api/admin/load?kind=${kind}&slug=${encodeURIComponent(slug)}`);
      const data = await res.json();
      if (data.ok) setLoaded(data as LoadedCategory);
      else setNotice({ kind: "err", text: "ÎöÎÿÎóÎÖÎáÎö ÎáÎøÎ®Î£Îö." });
    } finally {
      setBusy(false);
    }
  }

  function setField(productId: string, path: string, value: string | string[]) {
    setDraft((prev) => ({
      ...prev,
      [productId]: { ...(prev[productId] ?? {}), [path]: value },
    }));
  }

  // dirty edits = draft values that differ from the loaded originals
  const dirtyEdits = useMemo<Draft>(() => {
    if (!loaded) return {};
    const originals = new Map<string, Map<string, string | string[]>>();
    for (const p of loaded.products) {
      const m = new Map<string, string | string[]>();
      for (const f of p.fields) m.set(f.path, f.value);
      originals.set(p.id, m);
    }
    const out: Draft = {};
    for (const [pid, fields] of Object.entries(draft)) {
      for (const [path, value] of Object.entries(fields)) {
        const orig = originals.get(pid)?.get(path);
        if (orig === undefined || !sameValue(orig, value)) {
          (out[pid] ??= {})[path] = value;
        }
      }
    }
    return out;
  }, [draft, loaded]);

  const dirtyCount = useMemo(
    () => Object.values(dirtyEdits).reduce((n, f) => n + Object.keys(f).length, 0),
    [dirtyEdits],
  );

  async function save() {
    if (!loaded || dirtyCount === 0) return;
    setBusy(true);
    setNotice(null);
    try {
      const res = await fetch("/api/admin/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ kind: loaded.kind, slug: loaded.slug, edits: dirtyEdits }),
      });
      const data = await res.json();
      if (data.ok) {
        setNotice({
          kind: "ok",
          text: `ÎáÎ®Î×Î¿ ÎòÎñÎòÎ¿ÎíÎØ ÔÇö ${data.applied} Î®ÎÖÎáÎòÎÖ(ÎÖÎØ). ÎöÎóÎôÎøÎòÎƒ ÎÖÎóÎ£Îö Î£ÎÉÎ¬Î¿ Î¬ÎòÎÜ Îø-2 ÎôÎºÎòÎ¬.`,
        });
        // refresh so the editor reflects the committed values as the new baseline
        await openCategory(loaded.slug, loaded.kind);
      } else if (data.error === "github_not_configured") {
        setNotice({ kind: "err", text: "ÎöÎñÎ¿ÎíÎòÎØ Î£-GitHub Î£ÎÉ Î×ÎòÎÆÎôÎ¿ ÎæÎ®Î¿Î¬." });
      } else {
        setNotice({ kind: "err", text: "ÎöÎ®Î×ÎÖÎ¿Îö ÎáÎøÎ®Î£Îö. ÎáÎíÎö Î®ÎòÎæ." });
      }
    } catch {
      setNotice({ kind: "err", text: "Î®ÎÆÎÖÎÉÎ¬ Î¿Î®Î¬ ÎæÎ®Î×ÎÖÎ¿Îö." });
    } finally {
      setBusy(false);
    }
  }

  // ---- render ----
  if (status === "loading") {
    return <Shell><p className="text-neutral-500">ÎÿÎòÎóÎƒÔÇª</p></Shell>;
  }

  if (status === "login") {
    return (
      <Shell>
        <form onSubmit={doLogin} className="mx-auto mt-16 max-w-sm space-y-4">
          <h1 className="text-xl font-semibold">ÎóÎòÎ¿ÎÜ ÎöÎ¬ÎòÎøÎƒ Î®Î£ Bari</h1>
          <p className="text-sm text-neutral-500">ÎöÎûÎƒ ÎíÎÖÎíÎ×Îö ÎøÎôÎÖ Î£ÎóÎ¿ÎòÎÜ Î×Î®ÎñÎÿÎÖÎØ ÎòÎøÎÖÎ¬ÎòÎæÎÖÎØ.</p>
          <input
            type="password"
            autoFocus
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="ÎíÎÖÎíÎ×Îö"
            className="w-full rounded-md border border-neutral-300 px-3 py-2"
          />
          {loginError && <p className="text-sm text-red-600">{loginError}</p>}
          <button type="submit" className="w-full rounded-md bg-neutral-900 px-4 py-2 text-white">
            ÎøÎáÎÖÎíÎö
          </button>
        </form>
      </Shell>
    );
  }

  return (
    <Shell>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-xl font-semibold">ÎóÎòÎ¿ÎÜ ÎöÎ¬ÎòÎøÎƒ Î®Î£ Bari</h1>
        <button onClick={doLogout} className="text-sm text-neutral-500 underline">ÎÖÎªÎÖÎÉÎö</button>
      </div>

      {!githubReady && (
        <Banner kind="err">
          ÎöÎñÎ¿ÎíÎòÎØ Î£-GitHub Î£ÎÉ Î×ÎòÎÆÎôÎ¿ ÎæÎ®Î¿Î¬ ÔÇö ÎÉÎñÎ®Î¿ Î£ÎóÎ¿ÎòÎÜ ÎòÎ£ÎªÎñÎòÎ¬, ÎÉÎÜ Î®Î×ÎÖÎ¿Îö Î£ÎÉ Î¬ÎóÎ£Îö Î£ÎÉÎ¬Î¿ ÎóÎô Î®ÎÖÎòÎÆÎôÎ¿Îò ÎöÎíÎòÎôÎòÎ¬.
        </Banner>
      )}

      <div className="grid grid-cols-1 gap-6 md:grid-cols-[220px_1fr]">
        {/* category list */}
        <aside className="space-y-4">
          <CategoryGroup
            title="ÎöÎ®ÎòÎòÎÉÎòÎ¬"
            items={comparisons}
            loadedKey={loaded ? `${loaded.kind}:${loaded.slug}` : undefined}
            onOpen={openCategory}
          />
          <CategoryGroup
            title="ÎæÎ£ÎòÎÆ"
            items={blogDocs}
            loadedKey={loaded ? `${loaded.kind}:${loaded.slug}` : undefined}
            onOpen={openCategory}
          />
        </aside>

        {/* editor */}
        <div>
          {notice && <Banner kind={notice.kind}>{notice.text}</Banner>}

          {!loaded && <p className="text-neutral-400">ÎæÎùÎ¿ ÎºÎÿÎÆÎòÎ¿ÎÖÎö ÎøÎôÎÖ Î£ÎóÎ¿ÎòÎÜ.</p>}

          {loaded && (
            <>
              <div className="sticky top-0 z-10 mb-4 flex items-center justify-between border-b border-neutral-200 bg-white/90 py-3 backdrop-blur">
                <div>
                  <h2 className="text-lg font-medium">{loaded.nameHe}</h2>
                  <p className="text-xs text-neutral-400">{loaded.slug}</p>
                </div>
                <button
                  onClick={save}
                  disabled={busy || dirtyCount === 0}
                  className="rounded-md bg-emerald-600 px-4 py-2 text-sm text-white disabled:opacity-40"
                >
                  {busy ? "Î®ÎòÎ×Î¿ÔÇª" : dirtyCount > 0 ? `ÎñÎ¿ÎíÎØ ${dirtyCount} Î®ÎÖÎáÎòÎÖ(ÎÖÎØ)` : "ÎÉÎÖÎƒ Î®ÎÖÎáÎòÎÖÎÖÎØ"}
                </button>
              </div>

              <div className="space-y-8">
                {loaded.products.map((p) => (
                  <ProductBlock
                    key={p.id}
                    product={p}
                    draft={draft[p.id] ?? {}}
                    onChange={(path, value) => setField(p.id, path, value)}
                  />
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </Shell>
  );
}

function CategoryGroup({
  title,
  items,
  loadedKey,
  onOpen,
}: {
  title: string;
  items: CategorySummary[];
  loadedKey?: string;
  onOpen: (slug: string, kind: DocKind) => void;
}) {
  if (items.length === 0) return null;
  return (
    <div>
      <h2 className="mb-1 px-3 text-xs font-semibold tracking-wide text-neutral-400">{title}</h2>
      <div className="space-y-1">
        {items.map((c) => (
          <button
            key={`${c.kind}:${c.slug}`}
            onClick={() => onOpen(c.slug, c.kind)}
            disabled={c.unavailable}
            className={`block w-full rounded-md px-3 py-2 text-right text-sm ${
              loadedKey === `${c.kind}:${c.slug}` ? "bg-neutral-900 text-white" : "hover:bg-neutral-100"
            } ${c.unavailable ? "opacity-40" : ""}`}
          >
            {c.nameHe}
            {typeof c.productCount === "number" && (
              <span className="mr-1 text-xs opacity-60">({c.productCount})</span>
            )}
          </button>
        ))}
      </div>
    </div>
  );
}

function ProductBlock({
  product,
  draft,
  onChange,
}: {
  product: EditableProduct;
  draft: Record<string, string | string[]>;
  onChange: (path: string, value: string | string[]) => void;
}) {
  return (
    <section className="rounded-lg border border-neutral-200 p-4">
      <header className="mb-3 flex items-baseline justify-between">
        <h3 className="font-medium">{product.name || product.id}</h3>
        {product.score !== null && (
          <span className="text-xs text-neutral-400">
            {product.score} ┬À {product.grade ?? "ÔÇö"} <span className="opacity-60">(Î£ÎÉ ÎáÎÖÎ¬Îƒ Î£ÎóÎ¿ÎÖÎøÎö)</span>
          </span>
        )}
      </header>

      {product.fields.length === 0 && (
        <p className="text-xs text-neutral-400">ÎÉÎÖÎƒ Î®ÎôÎòÎ¬ ÎÿÎºÎíÎÿ ÎöÎáÎÖÎ¬ÎáÎÖÎØ Î£ÎóÎ¿ÎÖÎøÎö ÎæÎ×ÎòÎªÎ¿ ÎûÎö.</p>
      )}

      <div className="space-y-4">
        {product.fields.map((f) => {
          const current = draft[f.path] ?? f.value;
          return (
            <label key={f.path} className="block">
              <span className="mb-1 block text-xs font-medium text-neutral-500">{f.label}</span>
              {f.kind === "list" ? (
                <textarea
                  dir="rtl"
                  rows={Math.max(2, (current as string[]).length)}
                  value={(current as string[]).join("\n")}
                  onChange={(e) =>
                    onChange(f.path, e.target.value.split("\n").map((s) => s).filter((s, i, arr) => !(s === "" && i === arr.length - 1)))
                  }
                  className="w-full rounded-md border border-neutral-300 px-3 py-2 text-sm leading-relaxed"
                />
              ) : (
                <textarea
                  dir="rtl"
                  rows={2}
                  value={current as string}
                  onChange={(e) => onChange(f.path, e.target.value)}
                  className="w-full rounded-md border border-neutral-300 px-3 py-2 text-sm leading-relaxed"
                />
              )}
            </label>
          );
        })}
      </div>
    </section>
  );
}

function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div dir="rtl" lang="he" className="min-h-screen bg-white px-4 py-8 text-neutral-900">
      <div className="mx-auto max-w-4xl">{children}</div>
    </div>
  );
}

function Banner({ kind, children }: { kind: "ok" | "err"; children: React.ReactNode }) {
  return (
    <div
      className={`mb-4 rounded-md px-4 py-3 text-sm ${
        kind === "ok" ? "bg-emerald-50 text-emerald-800" : "bg-red-50 text-red-800"
      }`}
    >
      {children}
    </div>
  );
}
