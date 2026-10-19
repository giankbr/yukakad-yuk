"use client";
import Link from "next/link";
import { StateCard, stateStyles } from "./StateCard";

// API busy (429/5xx) or unreachable: never claim the invitation is unpublished, just ask to retry.
export default function InvitationError({ retry }: { error: Error & { digest?: string }; retry: () => void }) {
  return (
    <StateCard
      title="Undangan sedang ramai dibuka, coba lagi sebentar"
      actions={
        <>
          <button type="button" className={stateStyles.primary} onClick={() => retry()}>Coba lagi</button>
          <Link href="/" className={stateStyles.secondary}>Ke beranda</Link>
        </>
      }
    >
      Banyak tamu membuka undangan ini bersamaan. Tunggu beberapa detik, lalu muat ulang.
    </StateCard>
  );
}
