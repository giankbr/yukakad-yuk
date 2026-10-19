"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { apiFetch, getToken } from "@/lib/api";
import { AuthHeading, AuthLayout } from "@/components/auth/AuthLayout";
import { friendlyError } from "@/lib/errors";

type VerifyResult = { plan?: { id: string; name: string; price: number }; activated?: unknown[]; pending?: number; latest_status?: string };
type State = "checking" | "paid" | "pending" | "error";

const ATTEMPTS = 10;
const INTERVAL = 3000;

/** Mayar sends the payer here after paying; we ask the backend to confirm with Mayar and activate the plan. */
export default function PaymentDonePage() {
  const router = useRouter();
  const [state, setState] = useState<State>("checking");
  const [planName, setPlanName] = useState("");
  const [error, setError] = useState("");
  const [run, setRun] = useState(0);

  useEffect(() => {
    let cancelled = false;
    const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));
    (async () => {
      const token = getToken();
      if (!token) {
        router.replace(`/auth/login?next=${encodeURIComponent("/payments/selesai")}`);
        return;
      }
      try {
        for (let attempt = 0; attempt < ATTEMPTS && !cancelled; attempt++) {
          if (attempt > 0) await sleep(INTERVAL);
          const response = await apiFetch("/api/billing/verify", token, { method: "POST" });
          const body: VerifyResult & { error?: string } = await response.json().catch(() => ({}));
          if (response.status === 401) { router.replace(`/auth/login?next=${encodeURIComponent("/payments/selesai")}`); return; }
          if (!response.ok) throw new Error(friendlyError(body.error, "Gagal memeriksa pembayaran."));
          if ((body.activated?.length ?? 0) > 0 || body.latest_status === "active") {
            if (!cancelled) { setPlanName(body.plan?.name ?? ""); setState("paid"); }
            return;
          }
        }
        if (!cancelled) setState("pending");
      } catch (err) {
        if (!cancelled) { setError(friendlyError(err instanceof Error ? err.message : "", "Gagal memeriksa pembayaran.")); setState("error"); }
      }
    })();
    return () => { cancelled = true; };
  }, [run, router]);

  const retry = () => { setState("checking"); setError(""); setRun(value => value + 1); };

  return (
    <AuthLayout topRight={<Link href="/dashboard">Dashboard</Link>}>
      {state === "paid" ? (
        <>
          <AuthHeading lead="Pembayaran" mono="berhasil.">{planName ? `Paket ${planName} sudah aktif di akunmu.` : "Paketmu sudah aktif."} Terima kasih sudah memakai Rawuh.</AuthHeading>
          <Link className="auth-submit" href="/dashboard/paket?bayar=selesai" style={{ display: "grid", placeItems: "center", textDecoration: "none" }}>Lihat paketku</Link>
          <p className="auth-switch"><Link href="/dashboard">Ke dashboard</Link></p>
        </>
      ) : state === "pending" ? (
        <>
          <AuthHeading lead="Menunggu" mono="pembayaran.">Pembayaranmu belum terkonfirmasi. Kalau sudah membayar, biasanya butuh beberapa menit — paket aktif otomatis tanpa perlu apa-apa lagi.</AuthHeading>
          <button className="auth-submit" type="button" onClick={retry}>Cek lagi</button>
          <p className="auth-switch"><Link href="/dashboard">Kembali ke dashboard</Link></p>
        </>
      ) : state === "error" ? (
        <>
          <AuthHeading lead="Belum bisa" mono="memeriksa.">Kami belum bisa memeriksa status pembayaranmu.</AuthHeading>
          <div className="auth-error" role="alert">{error}</div>
          <button className="auth-submit" type="button" onClick={retry}>Coba lagi</button>
        </>
      ) : (
        <>
          <AuthHeading lead="Memeriksa" mono="pembayaran.">Sebentar, kami sedang memastikan pembayaranmu ke Mayar…</AuthHeading>
          <p className="auth-status" role="status">Jangan tutup halaman ini.</p>
        </>
      )}
    </AuthLayout>
  );
}
