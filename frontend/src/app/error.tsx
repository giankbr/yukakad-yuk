"use client";
import Link from "next/link";
import { StateCard, stateStyles } from "./invitation/[slug]/StateCard";

// Root error boundary (below the root layout, so fonts and globals.css are loaded).
export default function RootError({ retry }: { error: Error & { digest?: string }; retry: () => void }) {
  return (
    <StateCard
      title="Ada yang tidak beres"
      actions={
        <>
          <button type="button" className={stateStyles.primary} onClick={() => retry()}>Coba lagi</button>
          <Link href="/" className={stateStyles.secondary}>Ke beranda</Link>
        </>
      }
    >
      Halaman ini gagal dimuat. Coba lagi sebentar lagi, atau kembali ke beranda.
    </StateCard>
  );
}
