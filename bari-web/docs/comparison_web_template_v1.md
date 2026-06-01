# Comparison Web Template v1

**Status:** Superseded for Snacks desktop (2026-05-29)

Snacks desktop (`lg+`) now follows the **`/hashvaot/milk-comparison`** shelf pattern via `SnacksComparisonDesktopPage`. Mobile Snacks remains Comparison Shelf v1 (375px phone frame).

See:

- `src/components/comparisons/snacks-comparison-desktop-page.tsx` — milk-aligned desktop
- `src/components/comparisons/milk-comparison-page.tsx` — reference implementation

The `layout="web"` table grid on `ComparisonShelfPage` is **not used** by Snacks. Maadanim and Bread remain `layout="shelf"` (default).

---

## Historical note

Earlier passes widened a 4-column CSS table (`webTable` tokens). That approach is retired for Snacks in favor of the milk comparison row model: rank + thumbnail + title + grade, `בקצרה` insight line, expandable score explanation panel, `HomeContainer` / `max-w-7xl`, zebra rows.

---

## Mobile (Snacks)

Unchanged: `ComparisonShelfPage` without `layout="web"`.

---

## QA

- [ ] Snacks `lg+` visually aligned with milk comparison
- [ ] Snacks `< lg` unchanged phone shelf
- [ ] Maadanim / Bread unchanged
