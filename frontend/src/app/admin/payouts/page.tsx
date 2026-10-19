"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { useAdminAuth } from "@/lib/useAuthToken";

type Payout = { id: string; amount: number; status: string; bank_name: string; account_number: string; account_name: string; note?: string; created_at: string; processed_at?: string };
type Row = {
  payout: Payout;
  invitation?: { id: string; slug: string; title: string };
  user?: { name: string; email: string };
  wallet?: { received: number; fee: number; paid_out: number; requested: number; available: number };
};
type Settings = { online_enabled?: boolean; fee_percent: number; min_payout: number };
type Filter = "requested" | "paid" | "rejected" | "";

const rupiah = (value: number) => `Rp${Math.round(value).toLocaleString("id-ID")}`;
const date = (value?: string) => (value ? new Date(value).toLocaleString("id-ID", { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" }) : "");
const FILTERS: [Filter, string][] = [["requested", "Perlu diproses"], ["paid", "Sudah ditransfer"], ["rejected", "Ditolak"], ["", "Semua"]];
const STATUS: Record<string, string> = { requested: "Diproses", paid: "Ditransfer", rejected: "Ditolak" };

export default function AdminPayoutsPage() {
  const { token, ready } = useAdminAuth();
  const [filter, setFilter] = useState<Filter>("requested");
  const [rows, setRows] = useState<Row[]>([]);
  const [settings, setSettings] = useState<Settings>({ fee_percent: 0, min_payout: 50000 });
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<string | null>(null);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [reload, setReload] = useState(0);

  useEffect(() => {
    if (!ready || !token) return;
    apiFetch(`/api/admin/gift-payouts${filter ? `?status=${filter}` : ""}`, token)
      .then((r) => r.json())
      .then((body: { items?: Row[]; settings?: Settings }) => { setRows(body.items ?? []); if (body.settings) setSettings(body.settings); })
      .catch(() => setError("Gagal memuat pencairan"))
      .finally(() => setLoading(false));
  }, [ready, token, filter, reload]);

  async function process(row: Row, status: "paid" | "rejected") {
    if (!token) return;
    const label = `${rupiah(row.payout.amount)} ke ${row.payout.bank_name} ${row.payout.account_number} a.n. ${row.payout.account_name}`;
    const note = window.prompt(status === "paid" ? `Sudah transfer ${label}?\nIsi nomor referensi transfer (opsional):` : `Tolak pencairan ${label}?\nAlasan (akan terlihat oleh pengguna):`, "");
    if (note === null) return;
    setBusy(row.payout.id);
    setError("");
    setNotice("");
    try {
      const response = await apiFetch(`/api/admin/gift-payouts/${row.payout.id}`, token, { method: "PATCH", body: JSON.stringify({ status, note }) });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error);
      setNotice(status === "paid" ? "Ditandai sudah ditransfer." : "Pencairan ditolak; saldo kembali ke pengguna.");
      setReload((n) => n + 1);
    } catch (err) {
      setError(err instanceof Error && err.message ? err.message : "Belum tersimpan.");
    } finally {
      setBusy(null);
    }
  }

  async function saveSettings(event: React.FormEvent) {
    event.preventDefault();
    if (!token) return;
    setBusy("settings");
    setError("");
    setNotice("");
    try {
      const response = await apiFetch("/api/admin/site-content/gift_settings", token, { method: "PUT", body: JSON.stringify(settings) });
      if (!response.ok) throw new Error();
      setNotice("Pengaturan amplop online tersimpan.");
    } catch {
      setError("Pengaturan belum tersimpan.");
    } finally {
      setBusy(null);
    }
  }

  if (!ready || !token) return null;

  return (
    <DashboardShell active="payouts" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Bisnis</p>
          <h1>Pencairan amplop</h1>
          <p className="dashboard-subtitle">Amplop online dibayar tamu ke rekening Mayar Rawuh. Transfer manual ke rekening pengantin, lalu tandai di sini.</p>
        </div>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {notice && <p role="status" className={styles.ok} style={{ margin: "0 0 12px" }}>{notice}</p>}

      <div className={styles.form} style={{ maxWidth: "none" }}>
        <form className={styles.panel} onSubmit={saveSettings} aria-label="Pengaturan">
          <div className={styles.panelHead}>
            <div><h2>Pengaturan</h2><p>Berlaku untuk semua undangan. Biaya dipotong dari saldo sebelum dicairkan.</p></div>
            <label className={styles.check}><input type="checkbox" checked={Boolean(settings.online_enabled)} onChange={(e) => setSettings({ ...settings, online_enabled: e.target.checked })} /> {settings.online_enabled ? "Amplop online dibuka" : "Amplop online ditutup"}</label>
          </div>
          <p className={styles.hint} style={{ margin: 0 }}>Selama ditutup, pengantin tidak bisa mengaktifkan amplop online dan tamu hanya melihat transfer langsung ke rekening pengantin. Buka setelah tinjauan legal &amp; izin penampungan dana selesai.</p>
          <div className={styles.row3} style={{ alignItems: "end" }}>
            <label className={styles.field}><span>Biaya layanan (%)</span>
              <input type="number" min={0} max={50} step={0.1} value={settings.fee_percent} onChange={(e) => setSettings({ ...settings, fee_percent: Number(e.target.value) })} />
            </label>
            <label className={styles.field}><span>Minimal pencairan (Rp)</span>
              <input type="number" min={0} step={1000} value={settings.min_payout} onChange={(e) => setSettings({ ...settings, min_payout: Number(e.target.value) })} />
            </label>
            <div><button type="submit" className="dashboard-action" disabled={busy === "settings"}>{busy === "settings" ? "Menyimpan…" : "Simpan"}</button></div>
          </div>
        </form>

        <div className={styles.tabs} role="group" aria-label="Status">
          {FILTERS.map(([key, label]) => (
            <button key={key || "all"} type="button" aria-pressed={filter === key} onClick={() => { setLoading(true); setFilter(key); }}>{label}</button>
          ))}
        </div>

        {loading ? <p className="dashboard-state">Memuat…</p> : rows.length === 0 ? (
          <p className={styles.empty}>{filter === "requested" ? "Tidak ada pencairan yang menunggu." : "Belum ada data."}</p>
        ) : (
          <div className="dashboard-table-wrap">
            <table className="dashboard-table" style={{ minWidth: 860 }}>
              <thead><tr><th>Diajukan</th><th>Pengguna</th><th>Nominal</th><th>Rekening tujuan</th><th>Status</th><th><span className="sr-only">Aksi</span></th></tr></thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.payout.id}>
                    <td>{date(row.payout.created_at)}</td>
                    <td><strong>{row.user?.name ?? "—"}</strong><span>{row.user?.email}</span>{row.invitation && <span><a href={`/invitation/${row.invitation.slug}`} target="_blank" rel="noreferrer">{row.invitation.title} ↗</a></span>}</td>
                    <td><strong>{rupiah(row.payout.amount)}</strong>{row.wallet && <span>Saldo diterima {rupiah(row.wallet.received - row.wallet.fee)}</span>}</td>
                    <td><strong>{row.payout.bank_name} · {row.payout.account_number}</strong><span>a.n. {row.payout.account_name}</span></td>
                    <td><span className={`status ${row.payout.status === "paid" ? "status-published" : "status-draft"}`}>{STATUS[row.payout.status] ?? row.payout.status}</span>{row.payout.note && <span>{row.payout.note}</span>}{row.payout.processed_at && <span>{date(row.payout.processed_at)}</span>}</td>
                    <td>
                      {row.payout.status === "requested" && (
                        <div style={{ display: "flex", gap: 6 }}>
                          <button type="button" className="table-action" disabled={busy === row.payout.id} onClick={() => process(row, "paid")}>Tandai ditransfer</button>
                          <button type="button" className="table-action table-action-danger" disabled={busy === row.payout.id} onClick={() => process(row, "rejected")}>Tolak</button>
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </DashboardShell>
  );
}
