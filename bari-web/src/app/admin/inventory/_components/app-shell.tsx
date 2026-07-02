/**
 * Re-export shim — AppShell has been lifted to the shared components tree.
 * src/app/admin/inventory/page.tsx still imports from this path for backward
 * compatibility; redirect to the canonical location.
 */
export { AppShell } from "@/components/inventory/app-shell";
export type { AppShellProps } from "@/components/inventory/app-shell";
