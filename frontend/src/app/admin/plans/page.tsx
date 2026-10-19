"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { useAdminAuth } from "@/lib/useAuthToken";

type Plan = {
  id: string; name: string; price: number; max_guests: number; max_team_members?: number; duration_days?: number | null;
  has_watermark: boolean; custom_domain_allowed: boolean; payment_gateway_allowed: boolean; premium_templates_allowed: boolean;
};
type Draft = Plan & { isNew?: boolean };

type Flag = "has_watermark" | "custom_domain_allowed" | "payment_gateway_allowed" | "premium_templates_allowed";
const FLAGS: [Flag, string][] = [
  ["premium_templates_allowed", "Akses tema Premium"],
  ["custom_domain_allowed", "Domain pribadi"],
  ["payment_gateway_allowed", "Amplop digital (payment gateway)"],
  ["has_watermark", "Tampilkan watermark Rawuh"],
];

const rupiah = (value: number) => (value > 0 ? `Rp${value.toLocaleString("id-ID")}` : "Gratis");

export default function AdminPlansPage() {
  const { token, ready } = useAdminAuth();
  const [plans, setPlans] = useState<Plan[]>([]);
  const [draft, setDraft] = useState<Draft | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready || !token) return;
    apiFetch("/api/admin/plans", token)
      .then((r) => r.json())
      .then((body: { items?: Plan[] }) => setPlans(body.items ?? []))
      .catch(() => setError("Gagal memuat paket"))
      .finally(() => setLoading(false));
  }, [ready, token]);

  async function save(event: React.FormEvent) {
    event.preventDefault();
    if (!token || !draft) return;
    setSaving(true);
    setError("");
    setNotice("");
    try {
      const { isNew, ...plan } = draft;
      const payload = { ...plan, duration_days: plan.duration_days ? Number(plan.duration_days) : null };
      const response = await apiFetch(isNew ? "/api/admin/plans" : `/api/admin/plans/${plan.id}`, token, { method: isNew ? "POST" : "PUT", body: JSON.stringify(payload) });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error);
      setPlans((current) => (isNew ? [...current, body] : current.map((item) => (item.id === body.id ? body : item))).sort((a, b) => a.price - b.price));
      setDraft(null);
      setNotice(`Paket ${body.name} tersimpan. Halaman harga ikut berubah.`);
    } catch (err) {
      setError(err instanceof Error && err.message ? `Paket belum tersimpan: ${err.message}` : "Paket belum tersimpan.");
    } finally {
      setSaving(false);
    }
  }

  if (!ready || !token) return null;

  const set = <K extends keyof Draft>(key: K, value: Draft[K]) => setDraft((d) => (d ? { ...d, [key]: value } : d));

  return (
    <DashboardShell active="plans" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Bisnis</p>
          <h1>Paket &amp; harga</h1>
          <p className="dashboard-subtitle">Harga, kuota tamu, dan fitur tiap paket. Tampil di halaman Harga dan dipakai untuk membatasi akun.</p>
        </div>
        {!draft && (
          <button type="button" className="dashboard-action" onClick={() => setDraft({ id: "", name: "", price: 0, max_guests: 100, max_team_members: 5, duration_days: 30, has_watermark: false, custom_domain_allowed: false, payment_gateway_allowed: false, premium_templates_allowed: false, isNew: true })}>
            + Paket baru
          </button>
        )}
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {notice && <p role="status" className={styles.ok} style={{ margin: "0 0 12px" }}>{notice}</p>}

      {loading ? <p className="dashboard-state">Memuat paket…</p> : (
        <div className={styles.form}>
          {draft && (
            <form className={styles.editor} onSubmit={save} aria-label={draft.isNew ? "Paket baru" : `Ubah ${draft.name}`}>
              <div className={styles.row3}>
                <label className={styles.field}><span>ID paket</span>
                  <input value={draft.id} disabled={!draft.isNew} required pattern="[a-z0-9][a-z0-9-]{1,30}" title="huruf kecil, angka, tanda minus" onChange={(e) => set("id", e.target.value.toLowerCase())} placeholder="rayakan" />
                </label>
                <label className={styles.field}><span>Nama</span><input value={draft.name} required onChange={(e) => set("name", e.target.value)} placeholder="Rayakan" /></label>
                <label className={styles.field}><span>Harga (Rp)</span><input type="number" min={0} step={1000} value={draft.price} onChange={(e) => set("price", Number(e.target.value))} /></label>
              </div>
              <div className={styles.row}>
                <label className={styles.field}><span>Maksimal tamu</span><input type="number" min={0} value={draft.max_guests} onChange={(e) => set("max_guests", Number(e.target.value))} /></label>
                <label className={styles.field}><span>Maksimal anggota tim per undangan (0 = tanpa batas)</span><input type="number" min={0} max={100} value={draft.max_team_members ?? 15} onChange={(e) => set("max_team_members", Number(e.target.value))} /></label>
              </div>
              <div className={styles.row}>
                <label className={styles.field}><span>Masa aktif (hari, kosongkan = selamanya)</span><input type="number" min={0} value={draft.duration_days ?? ""} onChange={(e) => set("duration_days", e.target.value ? Number(e.target.value) : null)} /></label>
              </div>
              <div className={styles.row}>
                {FLAGS.map(([key, label]) => (
                  <label key={key} className={styles.check}>
                    <input type="checkbox" checked={Boolean(draft[key])} onChange={(e) => set(key, e.target.checked)} /> {label}
                  </label>
                ))}
              </div>
              {!draft.isNew && <p className={styles.hint}>Perubahan berlaku untuk semua pengguna paket ini, termasuk yang sudah membayar.</p>}
              <div className={styles.actions}>
                <button type="submit" className="dashboard-action" disabled={saving}>{saving ? "Menyimpan…" : "Simpan paket"}</button>
                <button type="button" className={styles.ghost} onClick={() => setDraft(null)}>Batal</button>
              </div>
            </form>
          )}

          <div className="dashboard-table-wrap">
            <table className="dashboard-table" style={{ minWidth: 640 }}>
              <thead><tr><th>Paket</th><th>Harga</th><th>Tamu</th><th>Tim</th><th>Masa aktif</th><th>Fitur</th><th><span className="sr-only">Aksi</span></th></tr></thead>
              <tbody>
                {plans.map((plan) => (
                  <tr key={plan.id}>
                    <td><strong>{plan.name}</strong><span>{plan.id}</span></td>
                    <td>{rupiah(plan.price)}</td>
                    <td>{plan.max_guests.toLocaleString("id-ID")}</td>
                    <td>{plan.max_team_members === 0 ? "Bebas" : `${plan.max_team_members ?? 15} orang`}</td>
                    <td>{plan.duration_days ? `${plan.duration_days} hari` : "Selamanya"}</td>
                    <td>{FLAGS.filter(([key]) => (key === "has_watermark" ? !plan[key] : plan[key])).map(([key, label]) => (key === "has_watermark" ? "Tanpa watermark" : label.replace(" (payment gateway)", ""))).join(" · ") || "—"}</td>
                    <td><button type="button" className="table-action" onClick={() => setDraft({ ...plan })}>Ubah</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </DashboardShell>
  );
}
