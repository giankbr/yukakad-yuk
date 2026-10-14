"use client";

import { use, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { API_URL } from "@/lib/api";
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
      const body = await response.json();
      if (!response.ok) throw new Error(body.error ?? "Konfirmasi pembayaran gagal.");
      router.replace("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Konfirmasi pembayaran gagal.");
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
