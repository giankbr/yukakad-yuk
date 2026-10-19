"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { useAdminAuth } from "@/lib/useAuthToken";

type Row = { subscription: { id: string; plan_id: string; status: string; provider: string; provider_reference?: string; started_at: string; ends_at?: string }; user: { name: string; email: string }; plan_name: string; amount: number };
type Data = { items: Row[]; totals: { revenue_total: number; revenue_month: number; paid_count: number; pending_count: number }; envelopes: { paid_out: number; requested: number }; gateway: string };

const rupiah = (value: number) => `Rp${Math.round(value).toLocaleString("id-ID")}`;
const when = (value: string) => new Date(value).toLocaleString("id-ID", { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });
const STATUS: Record<string, string> = { active: "Lunas · aktif", pending: "Menunggu bayar", cancelled: "Lunas · berakhir", expired: "Kedaluwarsa" };
const GATEWAY: Record<string, string> = { mayar: "Mayar", dummy: "Simulasi (development)", "": "Belum dikonfigurasi" };

export default function AdminPaymentsPage() {
  const { token, ready } = useAdminAuth();
  const [data, setData] = useState<Data | null>(null);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready || !token) return;
    apiFetch("/api/admin/payments", token).then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status))))).then(setData).catch(() => setError("Gagal memuat pembayaran"));
  }, [ready, token]);

  const rows = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return (data?.items ?? []).filter((row) => (!status || row.subscription.status === status) && (!needle || `${row.user.name} ${row.user.email} ${row.plan_name} ${row.subscription.provider_reference ?? ""}`.toLowerCase().includes(needle)));
  }, [data, query, status]);

  if (!ready || !token) return null;
  const t = data?.totals;

  return (
    <DashboardShell active="payments" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Bisnis</p>
          <h1>Pembayaran</h1>
          <p className="dashboard-subtitle">Pembelian paket lewat {GATEWAY[data?.gateway ?? ""] ?? data?.gateway}. Paket aktif otomatis setelah Mayar mengonfirmasi pembayaran.</p>
        </div>
        <Link className="secondary-action" href="/admin/payouts">Pencairan amplop →</Link>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {data?.gateway === "" && <p role="alert" className="dashboard-state dashboard-state-error">MAYAR_API_KEY belum diisi di server — pengguna belum bisa membeli paket.</p>}

      {!data ? <p className="dashboard-state">Memuat…</p> : (
        <div className={styles.form} style={{ maxWidth: "none" }}>
          <div className={styles.row3} style={{ gridTemplateColumns: "repeat(auto-fit, minmax(170px, 1fr))" }}>
            {[["Pendapatan bulan ini", rupiah(t!.revenue_month)], ["Total pendapatan", rupiah(t!.revenue_total)], ["Transaksi lunas", String(t!.paid_count)], ["Menunggu bayar", String(t!.pending_count)], ["Amplop dicairkan", rupiah(data.envelopes.paid_out)], ["Amplop perlu ditransfer", rupiah(data.envelopes.requested)]].map(([label, value]) => (
              <div key={label} className={styles.item} style={{ display: "grid", gap: 2 }}><small className={styles.hint}>{label}</small><strong style={{ fontSize: 20 }}>{value}</strong></div>
            ))}
          </div>

          <section className={styles.panel} aria-label="Transaksi paket">
            <div className={styles.panelHead}>
              <div><h2>Transaksi paket</h2><p>{rows.length} transaksi</p></div>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                <label className={styles.field} style={{ width: 220 }}><span className="sr-only">Cari</span><input type="search" placeholder="Cari email, paket, ref…" value={query} onChange={(e) => setQuery(e.target.value)} /></label>
                <label className={styles.field} style={{ width: 170 }}><span className="sr-only">Status</span>
                  <select value={status} onChange={(e) => setStatus(e.target.value)}>
                    <option value="">Semua status</option><option value="active">Aktif</option><option value="pending">Menunggu bayar</option><option value="cancelled">Berakhir</option><option value="expired">Kedaluwarsa</option>
                  </select>
                </label>
              </div>
            </div>
            {rows.length === 0 ? <p className={styles.empty}>Belum ada transaksi.</p> : (
              <div className="dashboard-table-wrap">
                <table className="dashboard-table dashboard-table-stack" style={{ minWidth: 760 }}>
                  <thead><tr><th>Waktu</th><th>Pengguna</th><th>Paket</th><th>Status</th><th>Referensi</th></tr></thead>
                  <tbody>
                    {rows.map((row) => (
                      <tr key={row.subscription.id}>
                        <td data-label="Waktu">{when(row.subscription.started_at)}</td>
                        <td data-label="Pengguna"><strong>{row.user.name}</strong><span>{row.user.email}</span></td>
                        <td data-label="Paket"><strong>{row.plan_name}</strong><span>{rupiah(row.amount)}</span></td>
                        <td data-label="Status"><span className={`status ${row.subscription.status === "active" ? "status-published" : "status-draft"}`}>{STATUS[row.subscription.status] ?? row.subscription.status}</span></td>
                        <td data-label="Referensi"><span style={{ fontFamily: "var(--rw-font-mono)" }}>{row.subscription.provider} · {(row.subscription.provider_reference ?? "").slice(0, 18)}</span></td>
                      </tr>
                    ))}
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
