import type { Metadata } from "next";
import Link from "next/link";
import { StateCard, stateStyles } from "./invitation/[slug]/StateCard";

export const metadata: Metadata = { title: "Halaman tidak ditemukan — Rawuh", robots: { index: false, follow: false } };

export default function NotFound() {
  return (
    <StateCard
      code="404"
      title="Halaman tidak ditemukan"
      actions={
        <>
          <Link href="/" className={stateStyles.primary}>Ke beranda</Link>
          <Link href="/templates" className={stateStyles.secondary}>Lihat tema</Link>
        </>
      }
    >
      Halaman yang kamu cari tidak ada atau sudah dipindahkan.
    </StateCard>
  );
}
