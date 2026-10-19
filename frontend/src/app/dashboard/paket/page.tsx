"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { API_URL, apiFetch } from "@/lib/api";
import { useAuthToken } from "@/lib/useAuthToken";
import { friendlyError } from "@/lib/errors";

type Plan = { id: string; name: string; price: number; max_guests: number; max_team_members?: number; duration_days?: number | null; has_watermark: boolean; custom_domain_allowed: boolean; payment_gateway_allowed: boolean; premium_templates_allowed?: boolean };
type Subscription = { id: string; plan_id: string; status: string; provider: string; started_at: string; ends_at?: string };
type Invoice = { id: string; invoice_number: string; amount: number; status: string; issued_at?: string; paid_at?: string };

const rupiah = (value: number) => (value > 0 ? `Rp${Math.round(value).toLocaleString("id-ID")}` : "Gratis");
const date = (value?: string) => (value ? new Date(value).toLocaleDateString("id-ID", { day: "numeric", month: "long", year: "numeric" }) : "—");
const SUB_STATUS: Record<string, string> = { active: "Aktif", pending: "Menunggu pembayaran", cancelled: "Berakhir", expired: "Kedaluwarsa" };

function perks(plan: Plan) {
  return [
    `Hingga ${plan.max_guests.toLocaleString("id-ID")} tamu`,
    typeof plan.max_team_members === "number"
      ? plan.max_team_members === 0 ? "Tim tanpa batas" : `Tim hingga ${plan.max_team_members.toLocaleString("id-ID")} anggota`
      : "",
    plan.duration_days ? `Aktif ${plan.duration_days} hari` : "Aktif selamanya",
    plan.premium_templates_allowed ? "Semua tema Premium" : "Tema gratis",
    plan.payment_gateway_allowed ? "Amplop online lewat Rawuh" : "",
    plan.custom_domain_allowed ? "Domain pribadi" : "",
    plan.has_watermark ? "Ada watermark Rawuh" : "Tanpa watermark",
  ].filter(Boolean);
}

export default function BillingPage() {
  const { token, ready } = useAuthToken();
  const [current, setCurrent] = useState<Plan | null>(null);
  const [plans, setPlans] = useState<Plan[]>([]);
  const [subs, setSubs] = useState<Subscription[]>([]);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [checking, setChecking] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  const load = useCallback(async (): Promise<Plan | null> => {
    if (!token) return null;
    const ok = (r: Response) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status))));
    const [plan, list, s, i] = await Promise.all([
      apiFetch("/api/billing/plan", token).then(ok),
      fetch(`${API_URL}/api/public/plans`).then(ok).catch(() => ({ items: [] })),
      apiFetch("/api/billing/subscriptions", token).then(ok).catch(() => ({ items: [] })),
      apiFetch("/api/billing/invoices", token).then(ok).catch(() => ({ items: [] })),
    ]);
    const currentPlan: Plan | null = plan && typeof plan === "object" && "id" in plan ? plan : null;
    setCurrent(currentPlan);
    setPlans((list.items ?? []).slice().sort((a: Plan, b: Plan) => a.price - b.price));
    setSubs(s.items ?? []);
    setInvoices(i.items ?? []);
    return currentPlan;
  }, [token]);

  useEffect(() => {
    if (!ready || !token) return;
    // Back from checkout (/payments/dummy or /payments/selesai): confirm, re-fetch, and say which plan is now active.
    const returned = typeof window !== "undefined" && new URLSearchParams(window.location.search).get("bayar") === "selesai";
    const timer = setTimeout(() => {
      const confirm = returned ? apiFetch("/api/billing/verify", token, { method: "POST" }).catch(() => null) : Promise.resolve(null);
      confirm
        .then(() => load())
        .then((plan) => {
          if (!returned) return;
          window.history.replaceState(null, "", window.location.pathname);
          setNotice(plan && plan.price > 0
            ? `Paket ${plan.name} sudah aktif. Terima kasih sudah memakai Rawuh.`
            : "Pembayaranmu belum terkonfirmasi. Kalau sudah membayar, tunggu beberapa menit lalu tekan Cek pembayaran.");
        })
        .catch(() => setError("Gagal memuat paket. Coba muat ulang halaman."))
        .finally(() => setLoading(false));
    }, 0);
    return () => clearTimeout(timer);
  }, [ready, token, load]);

  async function verify() {
    if (!token) return;
    setChecking(true);
    setNotice("");
    setError("");
    try {
      const response = await apiFetch("/api/billing/verify", token, { method: "POST" });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(body.error);
      await load();
      setNotice(body.activated?.length ? `Pembayaran diterima. Paket ${body.plan?.name ?? ""} aktif.` : "Belum ada pembayaran baru yang masuk. Kalau baru saja membayar, tunggu beberapa menit.");
    } catch (err) {
      setError(friendlyError(err instanceof Error ? err.message : "", "Gagal memeriksa pembayaran. Coba lagi sebentar lagi."));
    } finally {
      setChecking(false);
    }
  }

  if (!ready) return null;
  const active = subs.find((s) => s.status === "active");
  const pending = subs.filter((s) => s.status === "pending");
  const planName = (id: string) => plans.find((p) => p.id === id)?.name ?? id;

  return (
    <DashboardShell active="billing">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Akun</p>
          <h1>Paket &amp; tagihan</h1>
          <p className="dashboard-subtitle">Paket aktif, upgrade, dan riwayat pembayaran akunmu. Sekali bayar, tanpa langganan otomatis.</p>
        </div>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {notice && <p role="status" className={styles.ok} style={{ margin: "0 0 12px" }}>{notice}</p>}

      {loading ? <p className="dashboard-state">Memuat…</p> : (
        <div className={styles.form} style={{ maxWidth: "none" }}>
          {current && (
            <section className={styles.panel} aria-label="Paket aktif" style={{ borderColor: "var(--rw-primary-border)" }}>
              <div className={styles.panelHead}>
                <div>
                  <h2>Paket {current.name}</h2>
                  <p>{active?.ends_at ? `Aktif sampai ${date(active.ends_at)}` : current.price > 0 ? "Aktif" : "Paket gratis — upgrade kapan saja."}</p>
                </div>
                <span className="status status-published">Paket kamu</span>
              </div>
              <ul className={styles.hint} style={{ margin: 0, paddingLeft: 18, display: "grid", gap: 4, fontSize: 14 }}>{perks(current).map((p) => <li key={p}>{p}</li>)}</ul>
            </section>
          )}

          {pending.length > 0 && (
            <section className={styles.panel} aria-label="Menunggu pembayaran">
              <div className={styles.panelHead}>
                <div><h2>Menunggu pembayaran</h2><p>{pending.map((s) => `Paket ${planName(s.plan_id)}`).join(", ")} — sudah bayar? Cek di sini.</p></div>
                <button type="button" className="dashboard-action" disabled={checking} onClick={verify}>{checking ? "Memeriksa…" : "Cek pembayaran"}</button>
              </div>
            </section>
          )}

          <section className={styles.panel} aria-label="Pilihan paket">
            <h2>Pilihan paket</h2>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 12 }}>
              {plans.map((plan) => {
                const isCurrent = plan.id === current?.id;
                return (
                  <div key={plan.id} className={styles.item} style={{ display: "grid", alignContent: "start", gap: 8, ...(isCurrent ? { borderColor: "var(--rw-primary-border)", background: "var(--rw-primary-soft)" } : {}) }}>
                    <strong style={{ fontSize: 16 }}>{plan.name}</strong>
                    <strong style={{ fontSize: 22 }}>{rupiah(plan.price)}</strong>
                    <ul className={styles.hint} style={{ margin: 0, paddingLeft: 16, display: "grid", gap: 2 }}>{perks(plan).map((p) => <li key={p}>{p}</li>)}</ul>
                    {isCurrent ? <span className={styles.hint}><b>Paket kamu saat ini</b></span>
                      : plan.price > 0 ? <Link className="dashboard-action" href={`/checkout?plan=${encodeURIComponent(plan.id)}`} style={{ justifySelf: "start" }}>Pilih {plan.name}</Link>
                      : null}
                  </div>
                );
              })}
            </div>
          </section>

          <section className={styles.panel} aria-label="Riwayat pembayaran">
            <h2>Riwayat pembayaran</h2>
            {invoices.length === 0 && subs.length === 0 ? <p className={styles.empty}>Belum ada pembayaran.</p> : (
              <div className="dashboard-table-wrap">
                <table className="dashboard-table" style={{ minWidth: 560 }}>
                  <thead><tr><th>Tanggal</th><th>Paket</th><th>Nominal</th><th>Status</th></tr></thead>
                  <tbody>
                    {subs.map((s) => {
                      const invoice = invoices.find((i) => i.invoice_number === `INV-${s.id}`);
                      return (
                        <tr key={s.id}>
                          <td>{date(s.started_at)}</td>
                          <td><strong>{planName(s.plan_id)}</strong>{invoice && <span>{invoice.invoice_number}</span>}</td>
                          <td>{invoice ? rupiah(invoice.amount) : rupiah(plans.find((p) => p.id === s.plan_id)?.price ?? 0)}</td>
                          <td><span className={`status ${s.status === "active" ? "status-published" : "status-draft"}`}>{SUB_STATUS[s.status] ?? s.status}</span>{s.ends_at && s.status === "active" && <span>s/d {date(s.ends_at)}</span>}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </div>
      )}
    </DashboardShell>
  );
}
