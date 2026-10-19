"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { FormField } from "@/components/dashboard/FormField";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { useAdminAuth } from "@/lib/useAuthToken";
import styles from "@/components/dashboard/editor.module.css";
import { defaultFooterColumns, defaultPaymentMethods, type FooterColumn } from "@/components/landing/SiteChrome";

type Footer = {
  heading?: string;
  tagline?: string;
  copyright?: string;
  instagram?: string;
  tiktok?: string;
  columns?: FooterColumn[];
  payment_methods?: string[];
};

export default function AdminFooterPage() {
  const { token, ready } = useAdminAuth();
  const [footer, setFooter] = useState<Footer>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready || !token) return;
    apiFetch("/api/admin/site-content/footer", token)
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
      .then((body: Footer) => setFooter({ ...body, columns: body.columns?.length ? body.columns : defaultFooterColumns, payment_methods: body.payment_methods?.length ? body.payment_methods : defaultPaymentMethods }))
      .catch(() => setError("Gagal memuat konten footer"))
      .finally(() => setLoading(false));
  }, [ready, token]);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!token) return;
    setSaving(true);
    setSaved(false);
    setError("");
    try {
      const response = await apiFetch("/api/admin/site-content/footer", token, { method: "PUT", body: JSON.stringify({ ...footer, payment_methods: (footer.payment_methods ?? []).map((m) => m.trim()).filter(Boolean) }) });
      if (!response.ok) throw new Error();
      setSaved(true);
    } catch {
      setError("Gagal menyimpan konten footer");
    } finally {
      setSaving(false);
    }
  }

  if (!ready || !token) return null;

  return (
    <DashboardShell active="footer" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Landing page</p>
          <h1>Footer</h1>
          <p className="dashboard-subtitle">Tampil di bagian paling bawah home page.</p>
        </div>
      </header>

      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      {!loading && (
        <form className="dashboard-form" onSubmit={handleSubmit}>
          <FormField label="Tagline (di bawah logo)" value={footer.tagline ?? ""} onChange={(e) => setFooter({ ...footer, tagline: e.target.value })} placeholder="Undangan digital untuk setiap momen berharga. Dibuat dengan sepenuh hati di Yogyakarta." maxLength={160} />
          <FormField label="Hak cipta" value={footer.copyright ?? ""} onChange={(e) => setFooter({ ...footer, copyright: e.target.value })} placeholder="© 2026 Rawuh.id" />
          <FormField label="Akun Instagram" value={footer.instagram ?? ""} onChange={(e) => setFooter({ ...footer, instagram: e.target.value })} placeholder="@rawuh.id" />
          <FormField label="Akun TikTok" value={footer.tiktok ?? ""} onChange={(e) => setFooter({ ...footer, tiktok: e.target.value })} placeholder="@rawuh.id" />
          <FormField label="Metode bayar (pisahkan dengan koma)" value={(footer.payment_methods ?? []).join(", ")} onChange={(e) => setFooter({ ...footer, payment_methods: e.target.value.split(",").map((m) => m.trimStart()) })} placeholder="QRIS, Virtual Account, GoPay" />

          <div style={{ display: "grid", gap: 12 }}>
            <strong style={{ color: "var(--rw-ink)" }}>Kolom tautan</strong>
            <p className="form-hint" style={{ margin: 0 }}>Kolom “Produk” otomatis dari menu Produk. Isi tautan dengan “contact” untuk membuka WhatsApp admin.</p>
            {(footer.columns ?? []).map((column, ci) => {
              const setColumn = (next: FooterColumn) => setFooter({ ...footer, columns: (footer.columns ?? []).map((c, i) => (i === ci ? next : c)) });
              return (
                <div key={ci} className={styles.item} style={{ display: "grid", gap: 10 }}>
                  <label className={styles.field}><span>Judul kolom</span><input value={column.title} onChange={(e) => setColumn({ ...column, title: e.target.value })} /></label>
                  {column.links.map((link, li) => (
                    <div key={li} style={{ display: "grid", gridTemplateColumns: "minmax(0,1fr) minmax(0,1fr) auto", gap: 8, alignItems: "end" }}>
                      <label className={styles.field}><span>Teks</span><input value={link.label} onChange={(e) => setColumn({ ...column, links: column.links.map((l, i) => (i === li ? { ...l, label: e.target.value } : l)) })} /></label>
                      <label className={styles.field}><span>Tautan</span><input value={link.href} onChange={(e) => setColumn({ ...column, links: column.links.map((l, i) => (i === li ? { ...l, href: e.target.value } : l)) })} /></label>
                      <button type="button" className="table-action table-action-danger" onClick={() => setColumn({ ...column, links: column.links.filter((_, i) => i !== li) })}>Hapus</button>
                    </div>
                  ))}
                  <div style={{ display: "flex", gap: 8 }}>
                    <button type="button" className={styles.ghost} onClick={() => setColumn({ ...column, links: [...column.links, { label: "", href: "/" }] })}>+ Tautan</button>
                    <button type="button" className={styles.ghost} onClick={() => setFooter({ ...footer, columns: (footer.columns ?? []).filter((_, i) => i !== ci) })}>Hapus kolom</button>
                  </div>
                </div>
              );
            })}
            {(footer.columns ?? []).length < 4 && <button type="button" className={styles.ghost} style={{ justifySelf: "start" }} onClick={() => setFooter({ ...footer, columns: [...(footer.columns ?? []), { title: "Kolom baru", links: [] }] })}>+ Tambah kolom</button>}
          </div>

          <div className="form-actions">
            <Button type="submit" disabled={saving}>
              {saving ? "Menyimpan..." : "Simpan perubahan"}
            </Button>
            {saved && <span className="form-hint">Tersimpan.</span>}
          </div>
        </form>
      )}
    </DashboardShell>
  );
}
