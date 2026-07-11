"use client";

import Link from "next/link";
import { useMemo, useState } from "react";

import type { CheckStatus, DossierIndexRow } from "@/lib/dossier/types";
import { BarcodeStatusBadge, CheckStatusBadge } from "./status-badge";

type QuickFilter = "all" | "bad_barcode" | "calc_fail" | "low_evidence" | "any_fail";

const QUICK_FILTERS: { id: QuickFilter; label: string }[] = [
  { id: "all", label: "הכל" },
  { id: "bad_barcode", label: "ברקוד פגום/ממתין" },
  { id: "calc_fail", label: "חישוב נכשל" },
  { id: "low_evidence", label: "ראיות חסרות (<50%)" },
  { id: "any_fail", label: "כל בדיקה שנכשלה" },
];

const BAD_BARCODE_STATUSES = new Set(["malformed", "pending_manual_review", "found_but_conflicting", "not_found"]);

type SortKey = "name" | "shelfId" | "evidenceCompleteness" | "publishedScore";

function evidencePct(row: DossierIndexRow): string {
  return row.evidenceCompleteness === null ? "—" : `${Math.round(row.evidenceCompleteness * 100)}%`;
}

function checkSummary(row: DossierIndexRow): { worst: CheckStatus; failCount: number; warnCount: number } {
  const statuses = Object.values(row.checks);
  const failCount = statuses.filter((s) => s === "fail").length;
  const warnCount = statuses.filter((s) => s === "warn").length;
  const worst: CheckStatus = failCount > 0 ? "fail" : warnCount > 0 ? "warn" : statuses.every((s) => s === "unknown") ? "unknown" : "pass";
  return { worst, failCount, warnCount };
}

export function DossierTable({ rows }: { rows: DossierIndexRow[] }) {
  const [quickFilter, setQuickFilter] = useState<QuickFilter>("all");
  const [shelfFilter, setShelfFilter] = useState<string>("all");
  const [query, setQuery] = useState("");
  const [sortKey, setSortKey] = useState<SortKey>("shelfId");
  const [sortDir, setSortDir] = useState<"asc" | "desc">("asc");

  const shelves = useMemo(() => Array.from(new Set(rows.map((r) => r.shelfId))).sort(), [rows]);

  const filtered = useMemo(() => {
    let out = rows;
    if (shelfFilter !== "all") out = out.filter((r) => r.shelfId === shelfFilter);
    if (query.trim()) {
      const q = query.trim().toLowerCase();
      out = out.filter((r) => (r.name ?? "").toLowerCase().includes(q) || r.key.toLowerCase().includes(q) || (r.pid ?? "").toLowerCase().includes(q));
    }
    switch (quickFilter) {
      case "bad_barcode":
        out = out.filter((r) => BAD_BARCODE_STATUSES.has(r.barcodeStatus));
        break;
      case "calc_fail":
        out = out.filter((r) => r.checks.calculation === "fail");
        break;
      case "low_evidence":
        out = out.filter((r) => r.evidenceCompleteness !== null && r.evidenceCompleteness < 0.5);
        break;
      case "any_fail":
        out = out.filter((r) => Object.values(r.checks).some((s) => s === "fail"));
        break;
      default:
        break;
    }
    return out;
  }, [rows, shelfFilter, query, quickFilter]);

  const sorted = useMemo(() => {
    const copy = [...filtered];
    copy.sort((a, b) => {
      let av: string | number = "";
      let bv: string | number = "";
      if (sortKey === "name") {
        av = a.name ?? "";
        bv = b.name ?? "";
      } else if (sortKey === "shelfId") {
        av = a.shelfId;
        bv = b.shelfId;
      } else if (sortKey === "evidenceCompleteness") {
        av = a.evidenceCompleteness ?? -1;
        bv = b.evidenceCompleteness ?? -1;
      } else if (sortKey === "publishedScore") {
        av = a.publishedScore ?? -1;
        bv = b.publishedScore ?? -1;
      }
      if (av < bv) return sortDir === "asc" ? -1 : 1;
      if (av > bv) return sortDir === "asc" ? 1 : -1;
      return 0;
    });
    return copy;
  }, [filtered, sortKey, sortDir]);

  function toggleSort(key: SortKey) {
    if (key === sortKey) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir("asc");
    }
  }

  return (
    <div>
      <div className="mb-4 flex flex-wrap items-center gap-2">
        {QUICK_FILTERS.map((f) => (
          <button
            key={f.id}
            onClick={() => setQuickFilter(f.id)}
            className={`rounded-md border px-3 py-1.5 text-xs font-medium ${
              quickFilter === f.id ? "border-neutral-900 bg-neutral-900 text-white" : "border-neutral-300 text-neutral-600 hover:bg-neutral-50"
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      <div className="mb-4 flex flex-wrap items-center gap-3">
        <input
          type="search"
          dir="rtl"
          placeholder="חיפוש לפי שם / מזהה"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-64 rounded-md border border-neutral-300 px-3 py-1.5 text-sm"
        />
        <select
          value={shelfFilter}
          onChange={(e) => setShelfFilter(e.target.value)}
          className="rounded-md border border-neutral-300 px-3 py-1.5 text-sm"
        >
          <option value="all">כל המדפים</option>
          {shelves.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <span className="text-xs text-neutral-400">
          {sorted.length}/{rows.length} מוצרים
        </span>
      </div>

      <div className="overflow-x-auto rounded-md border border-neutral-200">
        <table className="w-full min-w-[900px] text-right text-sm">
          <thead className="bg-neutral-50 text-xs text-neutral-500">
            <tr>
              <Th onClick={() => toggleSort("name")}>שם מוצר</Th>
              <Th onClick={() => toggleSort("shelfId")}>מדף</Th>
              <th className="px-3 py-2">מזהה (pid)</th>
              <th className="px-3 py-2">מצב ברקוד</th>
              <th className="px-3 py-2">בדיקות (שכבה 4)</th>
              <Th onClick={() => toggleSort("evidenceCompleteness")}>שלמות ראיות</Th>
              <Th onClick={() => toggleSort("publishedScore")}>ציון פורסם</Th>
              <th className="px-3 py-2" />
            </tr>
          </thead>
          <tbody>
            {sorted.map((row) => {
              const summary = checkSummary(row);
              return (
                <tr key={`${row.shelfId}:${row.key}`} className="border-t border-neutral-100 odd:bg-white even:bg-neutral-50/50">
                  <td className="px-3 py-2 font-medium">{row.name ?? <span className="text-neutral-400">—</span>}</td>
                  <td className="px-3 py-2 text-neutral-500">{row.shelfId}</td>
                  <td className="px-3 py-2 font-mono text-xs text-neutral-400">{row.pid ?? row.key}</td>
                  <td className="px-3 py-2">
                    <BarcodeStatusBadge status={row.barcodeStatus} />
                  </td>
                  <td className="px-3 py-2">
                    <div className="flex flex-wrap gap-1">
                      {summary.failCount > 0 && <CheckStatusBadge status="fail" label={`${summary.failCount} נכשל`} />}
                      {summary.warnCount > 0 && <CheckStatusBadge status="warn" label={`${summary.warnCount} אזהרה`} />}
                      {summary.failCount === 0 && summary.warnCount === 0 && <CheckStatusBadge status={summary.worst} label="4/4" />}
                    </div>
                  </td>
                  <td className="px-3 py-2 tabular-nums">{evidencePct(row)}</td>
                  <td className="px-3 py-2 tabular-nums">
                    {row.publishedScore ?? "—"} {row.publishedGrade ? `/ ${row.publishedGrade}` : ""}
                  </td>
                  <td className="px-3 py-2">
                    <Link href={`/internal/dossier/${row.key}`} className="text-xs font-medium text-emerald-700 underline">
                      פתח
                    </Link>
                  </td>
                </tr>
              );
            })}
            {sorted.length === 0 && (
              <tr>
                <td colSpan={8} className="px-3 py-8 text-center text-neutral-400">
                  אין תוצאות תואמות.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Th({ children, onClick }: { children: React.ReactNode; onClick?: () => void }) {
  return (
    <th className="px-3 py-2">
      <button onClick={onClick} className="flex items-center gap-1 font-medium hover:text-neutral-900">
        {children}
      </button>
    </th>
  );
}
