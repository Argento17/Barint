"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useMemo, useState } from "react";

import type { CheckStatus, DossierIndexRow } from "@/lib/dossier/types";

type QuickFilter = "all" | "bad_barcode" | "calc_fail" | "low_evidence" | "any_fail";
type SortKey = "name" | "shelfId" | "evidenceCompleteness" | "publishedScore";
const BAD_BARCODE_STATUSES = new Set(["malformed", "pending_manual_review", "found_but_conflicting", "not_found"]);
const QUICK_FILTERS: { id: QuickFilter; label: string }[] = [
  { id: "all", label: "All" }, { id: "bad_barcode", label: "Barcode review" }, { id: "calc_fail", label: "Score mismatch" }, { id: "low_evidence", label: "Low evidence (<50%)" }, { id: "any_fail", label: "Any failed check" },
];

function quality(row: DossierIndexRow) {
  if (row.evidenceCompleteness === null) return "Low";
  if (row.evidenceCompleteness >= 0.8) return `Good (${Math.round(row.evidenceCompleteness * 100)}%)`;
  if (row.evidenceCompleteness >= 0.5) return `Partial (${Math.round(row.evidenceCompleteness * 100)}%)`;
  return `Low (${Math.round(row.evidenceCompleteness * 100)}%)`;
}
function issueAndAction(row: DossierIndexRow) {
  if (BAD_BARCODE_STATUSES.has(row.barcodeStatus)) return { issue: "Barcode identity needs review", action: "Review barcode identity" };
  if (row.checks.calculation === "fail") return { issue: "Published score does not reproduce", action: "Review score reproducibility" };
  if (row.checks.calculation === "warn") return { issue: "Score is only partially verified", action: "Verify score evidence" };
  if (row.checks.source_traceability !== "pass") return { issue: "Source evidence needs review", action: "Review source traceability" };
  if (row.checks.publishability !== "pass") return { issue: "Publication record needs review", action: "Review publication record" };
  if (row.evidenceCompleteness !== null && row.evidenceCompleteness < 0.5) return { issue: "Limited source evidence", action: "Find missing source information" };
  return { issue: "No material issue", action: "—" };
}

export function DossierTable({ rows, generatedAt }: { rows: DossierIndexRow[]; generatedAt: string }) {
  const router = useRouter();
  const [quickFilter, setQuickFilter] = useState<QuickFilter>("all");
  const [shelfFilter, setShelfFilter] = useState("all");
  const [query, setQuery] = useState("");
  const [sortKey, setSortKey] = useState<SortKey>("shelfId");
  const [sortDir, setSortDir] = useState<"asc" | "desc">("asc");
  const shelves = useMemo(() => Array.from(new Set(rows.map((r) => r.shelfId))).sort(), [rows]);
  const updated = new Date(generatedAt).toLocaleDateString("en-GB");
  const filtered = useMemo(() => rows.filter((r) => {
    const q = query.trim().toLowerCase();
    if (shelfFilter !== "all" && r.shelfId !== shelfFilter) return false;
    if (q && !(r.name ?? "").toLowerCase().includes(q) && !(r.brand ?? "").toLowerCase().includes(q) && !r.key.toLowerCase().includes(q) && !(r.pid ?? "").toLowerCase().includes(q)) return false;
    if (quickFilter === "bad_barcode") return BAD_BARCODE_STATUSES.has(r.barcodeStatus);
    if (quickFilter === "calc_fail") return r.checks.calculation === "fail";
    if (quickFilter === "low_evidence") return r.evidenceCompleteness !== null && r.evidenceCompleteness < 0.5;
    return quickFilter !== "any_fail" || (Object.values(r.checks) as CheckStatus[]).some((s) => s === "fail");
  }), [rows, shelfFilter, query, quickFilter]);
  const sorted = useMemo(() => [...filtered].sort((a, b) => {
    const av = sortKey === "name" ? a.name ?? "" : sortKey === "shelfId" ? a.shelfId : sortKey === "publishedScore" ? a.publishedScore ?? -1 : a.evidenceCompleteness ?? -1;
    const bv = sortKey === "name" ? b.name ?? "" : sortKey === "shelfId" ? b.shelfId : sortKey === "publishedScore" ? b.publishedScore ?? -1 : b.evidenceCompleteness ?? -1;
    return av < bv ? (sortDir === "asc" ? -1 : 1) : av > bv ? (sortDir === "asc" ? 1 : -1) : 0;
  }), [filtered, sortKey, sortDir]);
  const toggle = (key: SortKey) => key === sortKey ? setSortDir((d) => d === "asc" ? "desc" : "asc") : (setSortKey(key), setSortDir("asc"));
  return <div><div className="mb-4 flex flex-wrap gap-2">{QUICK_FILTERS.map((f) => <button key={f.id} onClick={() => setQuickFilter(f.id)} className={`rounded-md border px-3 py-1.5 text-xs font-medium ${quickFilter === f.id ? "border-neutral-900 bg-neutral-900 text-white" : "border-neutral-300 text-neutral-600 hover:bg-neutral-50"}`}>{f.label}</button>)}</div><div className="mb-4 flex flex-wrap items-center gap-3"><input type="search" placeholder="Search product, brand, or ID" value={query} onChange={(e) => setQuery(e.target.value)} className="w-64 rounded-md border border-neutral-300 px-3 py-1.5 text-sm"/><select value={shelfFilter} onChange={(e) => setShelfFilter(e.target.value)} className="rounded-md border border-neutral-300 px-3 py-1.5 text-sm"><option value="all">All categories</option>{shelves.map((s) => <option key={s} value={s}>{s}</option>)}</select><span className="text-xs text-neutral-400">{sorted.length}/{rows.length} products</span></div><div className="overflow-x-auto rounded-md border border-neutral-200"><table className="w-full min-w-[1080px] text-left text-sm"><thead className="bg-neutral-50 text-xs text-neutral-500"><tr><Th onClick={() => toggle("name")}>Product</Th><Th onClick={() => toggle("shelfId")}>Category</Th><Th onClick={() => toggle("publishedScore")}>Score</Th><Th onClick={() => toggle("evidenceCompleteness")}>Data quality</Th><th className="px-3 py-2">Main issue</th><th className="px-3 py-2">Action needed</th><th className="px-3 py-2">Last updated</th></tr></thead><tbody>{sorted.map((row) => { const summary = issueAndAction(row); const href = `/internal/dossier/${row.key}`; return <tr key={`${row.shelfId}:${row.key}`} onClick={() => router.push(href)} className="cursor-pointer border-t border-neutral-100 odd:bg-white even:bg-neutral-50/50 hover:bg-emerald-50/40" title={`ID: ${row.pid ?? row.key}`}><td className="px-3 py-2"><Link href={href} onClick={(e) => e.stopPropagation()} className="font-medium text-neutral-900 hover:underline" dir="auto">{row.name ?? "—"}</Link>{row.brand && <div className="text-xs text-neutral-500" dir="auto">{row.brand}</div>}</td><td className="px-3 py-2 text-neutral-600">{row.shelfId}</td><td className="px-3 py-2 tabular-nums">{row.publishedScore ?? "—"}{row.publishedGrade ? ` / ${row.publishedGrade}` : ""}</td><td className="px-3 py-2">{quality(row)}</td><td className="px-3 py-2 text-neutral-600">{summary.issue}</td><td className="px-3 py-2 text-neutral-600">{summary.action}</td><td className="px-3 py-2 text-xs text-neutral-500">{updated}</td></tr>; })}{sorted.length === 0 && <tr><td colSpan={7} className="px-3 py-8 text-center text-neutral-400">No matching products.</td></tr>}</tbody></table></div></div>;
}
function Th({ children, onClick }: { children: React.ReactNode; onClick: () => void }) { return <th className="px-3 py-2"><button onClick={onClick} className="font-medium hover:text-neutral-900">{children}</button></th>; }
