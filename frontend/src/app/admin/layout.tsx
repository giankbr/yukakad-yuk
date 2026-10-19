import type { Metadata } from "next";
import type { ReactNode } from "react";

// Admin area: keep it out of search results.
export const metadata: Metadata = { robots: { index: false, follow: false } };

export default function AdminLayout({ children }: { children: ReactNode }) {
  return children;
}
