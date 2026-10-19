import type { Metadata } from "next";
import Link from "next/link";
import { StateCard, stateStyles } from "./StateCard";

export const metadata: Metadata = { title: "Undangan tidak ditemukan — Rawuh", robots: { index: false, follow: false } };

// Unknown or unpublished slugs (notFound() in page/generateMetadata) → HTTP 404 with this card.
export default function InvitationNotFound() {
  return (
    <StateCard
      code="404"
      title="Undangan tidak ditemukan"
      actions={<Link href="/" className={stateStyles.primary}>Ke beranda Rawuh</Link>}
    >
      Link ini belum aktif atau sudah tidak tersedia. Coba cek lagi link dari pengirim undangan.
    </StateCard>
  );
}
