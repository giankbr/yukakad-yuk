"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { apiFetch, getToken } from "@/lib/api";
import { AuthHeading, AuthLayout } from "@/components/auth/AuthLayout";

// Payment pages may live on our own origin (simulated checkout) or on Mayar's hosted checkout.
const PAYMENT_HOSTS = [/\.myr\.id$/, /(^|\.)mayar\.id$/, /(^|\.)mayar\.io$/];
function isTrustedPaymentUrl(url: URL) {
  if (url.origin === window.location.origin) return true;
  return url.protocol === "https:" && PAYMENT_HOSTS.some(pattern => pattern.test(url.hostname));
}

export default function CheckoutPage() {
  const router = useRouter();
  const started = useRef(false);
  const [attempt, setAttempt] = useState(0);
  const [error, setError] = useState("");

  useEffect(() => {
    const planId = new URLSearchParams(window.location.search).get("plan");
    if (!planId) {
      router.replace("/#harga");
      return;
    }
    const token = getToken();
    if (!token) {
      router.replace(`/auth/login?plan=${encodeURIComponent(planId)}`);
      return;
    }
    if (started.current) return;
    started.current = true;
    setError("");

    apiFetch("/api/billing/checkout", token, {
      method: "POST",
      body: JSON.stringify({ plan_id: planId }),
    }).then(async response => {
      const body = await response.json();
      if (!response.ok) throw new Error(body.error ?? "Checkout gagal dimulai.");
      const paymentUrl = new URL(body.payment_url, window.location.origin);
      if (!isTrustedPaymentUrl(paymentUrl)) throw new Error("Alamat pembayaran tidak valid.");
      window.location.assign(paymentUrl.href);
    }).catch(err => {
      setError(err instanceof Error ? err.message : "Checkout gagal dimulai.");
      started.current = false;
    });
  }, [attempt, router]);

  return (
    <AuthLayout topRight={<Link href="/#harga">Lihat paket</Link>}>
      <AuthHeading lead="Menyiapkan" mono="pembayaran.">Kami sedang menyiapkan checkout paket Rawuh pilihanmu. Kamu akan diarahkan ke halaman pembayaran Mayar.</AuthHeading>
      {error ? <div className="auth-error" role="alert">{error}</div> : <p className="auth-status" role="status">Mohon tunggu sebentar…</p>}
      {error && <button className="auth-submit" type="button" onClick={() => setAttempt(value => value + 1)}>Coba lagi</button>}
      <p className="auth-switch"><Link href="/#harga">Kembali ke pilihan paket</Link></p>
    </AuthLayout>
  );
}
