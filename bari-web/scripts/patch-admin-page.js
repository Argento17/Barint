const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const file = path.join(ROOT, "src/app/admin/page.tsx");
let t = fs.readFileSync(file, "utf8");
if (t.includes("AdminTab")) {
  console.log("skip");
  process.exit(0);
}

const insertAfter = 'type Draft = Record<string, Record<string, string | string[]>>;\n';
const extraTypes = `
type AdminTab = "products" | "page_chrome" | "site";

interface SiteEntry {
  id: string;
  file: string;
  labelHe: string;
}

interface PageChromeEntry {
  slug: string;
  nameHe: string;
}

interface LoadedSite {
  type: "site" | "page_chrome";
  id?: string;
  slug?: string;
  file: string;
  sha: string;
  labelHe?: string;
  fields: EditableField[];
}
`;

t = t.replace(insertAfter, insertAfter + extraTypes);

t = t.replace(
  "const [categories, setCategories] = useState<CategorySummary[]>([]);",
  `const [tab, setTab] = useState<AdminTab>("products");
  const [categories, setCategories] = useState<CategorySummary[]>([]);
  const [siteEntries, setSiteEntries] = useState<SiteEntry[]>([]);
  const [chromeEntries, setChromeEntries] = useState<PageChromeEntry[]>([]);
  const [loadedSite, setLoadedSite] = useState<LoadedSite | null>(null);
  const [siteDraft, setSiteDraft] = useState<Record<string, string | string[]>>({});`,
);

t = t.replace(
  `const data = await res.json();\n    setCategories(data.categories ?? []);`,
  `const data = await res.json();\n    setCategories(data.sections?.products ?? data.categories ?? []);\n    setSiteEntries(data.sections?.site ?? []);\n    setChromeEntries(data.sections?.pageChrome ?? []);`,
);

// Add openSite and openChrome before openCategory
const openCategoryFn = "async function openCategory(slug: string) {";
const siteFns = `
  async function openSite(id: string) {
    setNotice(null);
    setBusy(true);
    setLoaded(null);
    setLoadedSite(null);
    setDraft({});
    setSiteDraft({});
    try {
      const res = await fetch(\`/api/admin/load?type=site&id=\${encodeURIComponent(id)}\`);
      const data = await res.json();
      if (data.ok) setLoadedSite(data as LoadedSite);
      else setNotice({ kind: "err", text: "טעינה נכשלה." });
    } finally {
      setBusy(false);
    }
  }

  async function openChrome(slug: string) {
    setNotice(null);
    setBusy(true);
    setLoaded(null);
    setLoadedSite(null);
    setDraft({});
    setSiteDraft({});
    try {
      const res = await fetch(\`/api/admin/load?type=page_chrome&slug=\${encodeURIComponent(slug)}\`);
      const data = await res.json();
      if (data.ok) setLoadedSite(data as LoadedSite);
      else setNotice({ kind: "err", text: "טעינה נכשלה." });
    } finally {
      setBusy(false);
    }
  }

  `;
t = t.replace(openCategoryFn, siteFns + openCategoryFn);

t = t.replace(
  "setLoaded(null);\n    setDraft({});",
  "setLoaded(null);\n    setLoadedSite(null);\n    setDraft({});\n    setSiteDraft({});",
);

// tabs UI before grid
t = t.replace(
  '<div className="grid grid-cols-1 gap-6 md:grid-cols-[220px_1fr]">',
  `<div className="mb-4 flex flex-wrap gap-2">
        {(["products", "page_chrome", "site"] as AdminTab[]).map((key) => (
          <button
            key={key}
            type="button"
            onClick={() => { setTab(key); setLoaded(null); setLoadedSite(null); setDraft({}); setSiteDraft({}); }}
            className={\`rounded-md px-3 py-2 text-sm \${tab === key ? "bg-neutral-900 text-white" : "bg-neutral-100"}\`}
          >
            {key === "products" ? "טקסט מוצרים" : key === "page_chrome" ? "כרום דפים" : "דפי אתר"}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-[220px_1fr]">`,
);

// sidebar lists
t = t.replace(
  "{categories.map((c) => (",
  `{tab === "products" && categories.map((c) => (`,
);
t = t.replace(
  "          ))}\n        </aside>",
  `          ))}
          {tab === "page_chrome" && chromeEntries.map((c) => (
            <button
              key={c.slug}
              onClick={() => openChrome(c.slug)}
              className={\`block w-full rounded-md px-3 py-2 text-right text-sm \${loadedSite?.slug === c.slug ? "bg-neutral-900 text-white" : "hover:bg-neutral-100"}\`}
            >
              {c.nameHe}
            </button>
          ))}
          {tab === "site" && siteEntries.map((s) => (
            <button
              key={s.id}
              onClick={() => openSite(s.id)}
              className={\`block w-full rounded-md px-3 py-2 text-right text-sm \${loadedSite?.id === s.id ? "bg-neutral-900 text-white" : "hover:bg-neutral-100"}\`}
            >
              {s.labelHe}
            </button>
          ))}
        </aside>`,
);

// site editor block before closing main - after loaded products block
const siteEditor = `
          {loadedSite && (
            <>
              <div className="sticky top-0 z-10 mb-4 flex items-center justify-between border-b border-neutral-200 bg-white/90 py-3 backdrop-blur">
                <div>
                  <h2 className="text-lg font-medium">{loadedSite.labelHe ?? loadedSite.slug ?? loadedSite.id}</h2>
                  <p className="text-xs text-neutral-400">{loadedSite.file}</p>
                </div>
                <button
                  onClick={saveSite}
                  disabled={busy || siteDirtyCount === 0}
                  className="rounded-md bg-emerald-600 px-4 py-2 text-sm text-white disabled:opacity-40"
                >
                  {busy ? "שומר…" : siteDirtyCount > 0 ? \`שמור \${siteDirtyCount} שדות\` : "אין שינויים"}
                </button>
              </div>
              <div className="space-y-4">
                {loadedSite.fields.map((f) => {
                  const current = siteDraft[f.path] ?? f.value;
                  return (
                    <label key={f.path} className="block">
                      <span className="mb-1 block text-xs font-medium text-neutral-500">{f.label}</span>
                      {f.kind === "list" ? (
                        <textarea
                          dir="rtl"
                          rows={Math.max(2, (current as string[]).length)}
                          value={(current as string[]).join("\\n")}
                          onChange={(e) => setSiteDraft((prev) => ({ ...prev, [f.path]: e.target.value.split("\\n") }))}
                          className="w-full rounded-md border border-neutral-300 px-3 py-2 text-sm leading-relaxed"
                        />
                      ) : (
                        <textarea
                          dir="rtl"
                          rows={3}
                          value={current as string}
                          onChange={(e) => setSiteDraft((prev) => ({ ...prev, [f.path]: e.target.value }))}
                          className="w-full rounded-md border border-neutral-300 px-3 py-2 text-sm leading-relaxed"
                        />
                      )}
                    </label>
                  );
                })}
              </div>
            </>
          )}
`;

t = t.replace(
  "{!loaded && <p className=\"text-neutral-400\">",
  siteEditor + "\n          {!loaded && !loadedSite && <p className=\"text-neutral-400\">",
);

// add siteDirtyCount and saveSite before save function
const saveFn = "async function save() {";
const siteHelpers = `
  const siteDirtyEdits = useMemo(() => {
    if (!loadedSite) return {} as Record<string, string | string[]>;
    const orig = new Map(loadedSite.fields.map((f) => [f.path, f.value]));
    const out: Record<string, string | string[]> = {};
    for (const [path, value] of Object.entries(siteDraft)) {
      const o = orig.get(path);
      if (o === undefined || !sameValue(o, value)) out[path] = value;
    }
    for (const f of loadedSite.fields) {
      if (!(f.path in siteDraft) && f.value !== undefined) continue;
    }
    return out;
  }, [loadedSite, siteDraft]);

  const siteDirtyCount = Object.keys(siteDirtyEdits).length;

  async function saveSite() {
    if (!loadedSite || siteDirtyCount === 0) return;
    setBusy(true);
    setNotice(null);
    try {
      const body =
        loadedSite.type === "page_chrome"
          ? { type: "page_chrome", slug: loadedSite.slug, edits: siteDirtyEdits }
          : { type: "site", id: loadedSite.id, edits: siteDirtyEdits };
      const res = await fetch("/api/admin/save", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      const data = await res.json();
      if (data.ok) {
        setNotice({ kind: "ok", text: "נשמר ויפורסם תוך ~2 דקות." });
        if (loadedSite.type === "page_chrome" && loadedSite.slug) await openChrome(loadedSite.slug);
        else if (loadedSite.id) await openSite(loadedSite.id);
      } else setNotice({ kind: "err", text: "שמירה נכשלה." });
    } finally {
      setBusy(false);
    }
  }

  `;
t = t.replace(saveFn, siteHelpers + saveFn);

t = t.replace(
  'body: JSON.stringify({ slug: loaded.slug, edits: dirtyEdits }),',
  'body: JSON.stringify({ type: "products", slug: loaded.slug, edits: dirtyEdits }),',
);

fs.writeFileSync(file, t, "utf8");
console.log("patched admin page");
