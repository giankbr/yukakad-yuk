"use client";

import { use, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { API_URL } from "@/lib/api";
import { friendlyError } from "@/lib/errors";
import { AuthHeading, AuthLayout } from "@/components/auth/AuthLayout";

export default function DummyPaymentPage({ params }: PageProps<"/payments/dummy/[reference]">) {
  const { reference } = use(params);
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function confirmPayment() {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_URL}/api/billing/dummy/${encodeURIComponent(reference)}`, { method: "POST" });
      if (response.ok) {
        // The paket page re-fetches the plan and confirms which one is now active.
        router.replace("/dashboard/paket?bayar=selesai");
        return;
      }
      // Not a plan purchase: try an online envelope, then return the guest to the invitation.
      const gift = await fetch(`${API_URL}/api/payments/dummy/${encodeURIComponent(reference)}`, { method: "POST" });
      const body = await gift.json().catch(() => ({}));
      if (!gift.ok) throw new Error(friendlyError(body.error, "Konfirmasi pembayaran gagal."));
      if (document.referrer.includes("/invitation/")) {
        const back = new URL(document.referrer);
        back.searchParams.set("amplop", "selesai");
        window.location.assign(back.href);
      } else {
        router.back();
      }
    } catch (err) {
      setError(friendlyError(err instanceof Error ? err.message : "", "Konfirmasi pembayaran gagal."));
      setLoading(false);
    }
  }

  return (
    <AuthLayout topRight={<Link href="/#harga">Lihat paket</Link>}>
      <AuthHeading lead="Checkout" mono="demo.">Ini pembayaran simulasi. Tidak ada uang yang ditagihkan.</AuthHeading>
      {error && <div className="auth-error" role="alert">{error}</div>}
      <button className="auth-submit" type="button" disabled={loading} onClick={confirmPayment}>{loading ? "Memproses…" : "Konfirmasi pembayaran demo"}</button>
      <p className="auth-switch"><Link href="/#harga">Kembali ke pilihan paket</Link></p>
    </AuthLayout>
  );
}
