"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

export const dynamic = "force-dynamic";

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

type DocKind = "comparison" | "blog" | "page_chrome" | "site";

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

function sameValue(a: string | string[], b: string | string[]): boolean {
  return JSON.stringify(a) === JSON.stringify(b);
}

export default function AdminPage() {
  const [status, setStatus] = useState<"loading" | "login" | "ready">("loading");
  const [githubReady, setGithubReady] = useState(true);
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");

  const [comparisons, setComparisons] = useState<CategorySummary[]>([]);
  const [blogDocs, setBlogDocs] = useState<CategorySummary[]>([]);
  const [pageChromeDocs, setPageChromeDocs] = useState<CategorySummary[]>([]);
  const [siteDocs, setSiteDocs] = useState<CategorySummary[]>([]);
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
    setPageChromeDocs(data.pageChrome ?? []);
    setSiteDocs(data.site ?? []);
  }, []);

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
      setLoginError("העורך לא מוגד עדיין (חסרים סודות בשרת).");
    } else {
      setLoginError("סיסמה שגויה.");
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
      else setNotice({ kind: "err", text: "הטעינה נכשלה." });
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
          text: `נשמר ופורסם — ${data.applied} שינוי(ים). העדכון יעלה לאתר תוך כידי 2 דקות.`,
        });
        await openCategory(loaded.slug, loaded.kind);
      } else if (data.error === "github_not_configured") {
        setNotice({ kind: "err", text: "הפרסום ל-GitHub לא מוגדר בשרת." });
      } else {
        setNotice({ kind: "err", text: "השמירה נכשלה. נסה שוב." });
      }
    } catch {
      setNotice({ kind: "err", text: "שגיאת רשת בשמירה." });
    } finally {
      setBusy(false);
    }
  }

  if (status === "loading") {
    return (
      <Shell wide>
        <p className="text-neutral-500">טוען…</p>
      </Shell>
    );
  }

  if (status === "login") {
    return (
      <Shell>
        <form onSubmit={doLogin} className="mx-auto mt-16 max-w-sm space-y-4">
          <h1 className="text-xl font-semibold">עורך התוכן של Bari</h1>
          <p className="text-sm text-neutral-500">הזן סיסמה כדי לערוך משפטים וכיתובים.</p>
          <input
            type="password"
            autoFocus
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="סיסמה"
            className="w-full rounded-md border border-neutral-300 px-3 py-2"
          />
          {loginError && <p className="text-sm text-red-600">{loginError}</p>}
          <button type="submit" className="w-full rounded-md bg-neutral-900 px-4 py-2 text-white">
            כניסה
          </button>
        </form>
      </Shell>
    );
  }

  return (
    <Shell wide>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-xl font-semibold">עורך התוכן של Bari</h1>
        <button onClick={doLogout} className="text-sm text-neutral-500 underline">יציאה</button>
      </div>

      {!githubReady && (
        <Banner kind="err">
          הפרסום ל-GitHub לא מוגדר בשרת — אפשר לערוך ולצפות, אך שמירה לא תעלה לאתר עד שיוגדרו הסודות.
        </Banner>
      )}

      <div className="grid grid-cols-1 gap-6 md:grid-cols-[240px_1fr]">
        <aside className="max-h-[calc(100vh-8rem)] space-y-4 overflow-y-auto">
          <CategoryGroup
            title="השוואות"
            items={comparisons}
            loadedKey={loaded ? `${loaded.kind}:${loaded.slug}` : undefined}
            onOpen={openCategory}
          />
          <CategoryGroup
            title="בלוג"
            items={blogDocs}
            loadedKey={loaded ? `${loaded.kind}:${loaded.slug}` : undefined}
            onOpen={openCategory}
          />
          <CategoryGroup
            title="כותרות עמודי השוואה"
            items={pageChromeDocs}
            loadedKey={loaded ? `${loaded.kind}:${loaded.slug}` : undefined}
            onOpen={openCategory}
          />
          <CategoryGroup
            title="דפי אתר"
            items={siteDocs}
            loadedKey={loaded ? `${loaded.kind}:${loaded.slug}` : undefined}
            onOpen={openCategory}
          />
        </aside>

        <div>
          {notice && <Banner kind={notice.kind}>{notice.text}</Banner>}
          {!loaded && <p className="text-neutral-400">בחר קטגוריה כדי לערוך.</p>}

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
                  {busy ? "שומר…" : dirtyCount > 0 ? `פרסם ${dirtyCount} שינוי(ים)` : "אין שינויים"}
                </button>
              </div>

              <div className="space-y-8">
                {loaded.products.map((p) => (
                  <ProductBlock
                    key={p.id}
                    product={p}
                    draft={draft[p.id] ?? {}}
                    onChange={(path, value) => setField(p.id, path, value)}
                    showScore={loaded.kind === "comparison"}
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
  showScore,
}: {
  product: EditableProduct;
  draft: Record<string, string | string[]>;
  onChange: (path: string, value: string | string[]) => void;
  showScore?: boolean;
}) {
  return (
    <section className="rounded-lg border border-neutral-200 p-4">
      <header className="mb-3 flex items-baseline justify-between">
        <h3 className="font-medium">{product.name || product.id}</h3>
        {showScore && product.score !== null && (
          <span className="text-xs text-neutral-400">
            {product.score} · {product.grade ?? "—"}{" "}
            <span className="opacity-60">(לא ניתן לעריכה)</span>
          </span>
        )}
      </header>

      {product.fields.length === 0 && (
        <p className="text-xs text-neutral-400">אין שדות טקסט הניתנים לעריכה במוצר זה.</p>
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
                    onChange(
                      f.path,
                      e.target.value
                        .split("\n")
                        .map((s) => s)
                        .filter((s, i, arr) => !(s === "" && i === arr.length - 1)),
                    )
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

function Shell({ children, wide }: { children: React.ReactNode; wide?: boolean }) {
  return (
    <div dir="rtl" lang="he" className="min-h-screen bg-white px-4 py-8 text-neutral-900">
      <div className={wide ? "mx-auto max-w-6xl" : "mx-auto max-w-4xl"}>{children}</div>
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
