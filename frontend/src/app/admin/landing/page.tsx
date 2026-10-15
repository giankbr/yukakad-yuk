"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { defaultAnnouncement, defaultFaq, defaultStats, type Announcement, type FaqItem, type LandingStat } from "@/lib/marketing";
import { useAdminAuth } from "@/lib/useAuthToken";

type Section = "stats" | "faq" | "announcement";

export default function AdminLandingPage() {
  const { token, ready } = useAdminAuth();
  const [stats, setStats] = useState<LandingStat[]>(defaultStats);
  const [faq, setFaq] = useState<FaqItem[]>(defaultFaq);
  const [announcement, setAnnouncement] = useState<Announcement>(defaultAnnouncement);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState<Section | null>(null);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready || !token) return;
    const get = (key: Section) => apiFetch(`/api/admin/site-content/${key}`, token).then((r) => (r.ok ? r.json() : {})).catch(() => ({}));
    Promise.all([get("stats"), get("faq"), get("announcement")])
      .then(([s, f, a]: [{ items?: LandingStat[] }, { items?: FaqItem[] }, Announcement]) => {
        if (s.items?.length) setStats(s.items);
        if (f.items?.length) setFaq(f.items);
        if (typeof a.enabled === "boolean" || a.text) setAnnouncement({ ...defaultAnnouncement, ...a });
      })
      .finally(() => setLoading(false));
  }, [ready, token]);

  async function save(section: Section) {
    if (!token) return;
    setSaving(section);
    setError("");
    setNotice("");
    const body = section === "stats" ? { items: stats.filter((s) => s.value.trim() && s.label.trim()) }
      : section === "faq" ? { items: faq.filter((f) => f.q.trim() && f.a.trim()) }
      : announcement;
    try {
      const response = await apiFetch(`/api/admin/site-content/${section}`, token, { method: "PUT", body: JSON.stringify(body) });
      if (!response.ok) throw new Error();
      setNotice(section === "stats" ? "Statistik tersimpan." : section === "faq" ? "FAQ tersimpan." : "Pengumuman tersimpan.");
    } catch {
      setError("Belum tersimpan. Coba lagi.");
    } finally {
      setSaving(null);
    }
  }

  if (!ready || !token) return null;

  return (
    <DashboardShell active="landing" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Konten landing</p>
          <h1>Statistik, FAQ &amp; pengumuman</h1>
          <p className="dashboard-subtitle">Angka di bawah hero, daftar FAQ (home & Harga), dan bar pengumuman di atas semua halaman.</p>
        </div>
        <a className="secondary-action" href="/" target="_blank" rel="noreferrer">Lihat landing ↗</a>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {notice && <p role="status" className={styles.ok} style={{ margin: "0 0 12px" }}>{notice}</p>}

      {loading ? <p className="dashboard-state">Memuat…</p> : (
        <div className={styles.form}>
          <section className={styles.panel} aria-label="Pengumuman">
            <div className={styles.panelHead}>
              <div><h2>Bar pengumuman</h2><p>Strip hitam di paling atas setiap halaman marketing.</p></div>
              <label className={styles.check}><input type="checkbox" checked={announcement.enabled !== false} onChange={(e) => setAnnouncement({ ...announcement, enabled: e.target.checked })} /> Tampilkan</label>
            </div>
            <label className={styles.field}><span>Teks</span><input value={announcement.text ?? ""} maxLength={120} onChange={(e) => setAnnouncement({ ...announcement, text: e.target.value })} /></label>
            <div className={styles.row}>
              <label className={styles.field}><span>Teks tautan</span><input value={announcement.label ?? ""} maxLength={30} onChange={(e) => setAnnouncement({ ...announcement, label: e.target.value })} placeholder="Lihat sekarang" /></label>
              <label className={styles.field}><span>Tautan</span><input value={announcement.href ?? ""} onChange={(e) => setAnnouncement({ ...announcement, href: e.target.value })} placeholder="/harga atau https://…" /></label>
            </div>
            <div className={styles.actions}><button type="button" className="dashboard-action" disabled={saving !== null} onClick={() => save("announcement")}>{saving === "announcement" ? "Menyimpan…" : "Simpan pengumuman"}</button></div>
          </section>

          <section className={styles.panel} aria-label="Statistik">
            <div className={styles.panelHead}><div><h2>Statistik</h2><p>Empat angka di bawah hero. Gunakan angka yang benar dan bisa dipertanggungjawabkan.</p></div></div>
            <ul className={styles.list}>
              {stats.map((item, index) => (
                <li key={index} className={styles.item}>
                  <label className={styles.field} style={{ width: 120 }}><span>Angka</span><input value={item.value} maxLength={10} onChange={(e) => setStats(stats.map((s, i) => (i === index ? { ...s, value: e.target.value } : s)))} /></label>
                  <label className={styles.field} style={{ flex: 1 }}><span>Keterangan</span><input value={item.label} maxLength={120} onChange={(e) => setStats(stats.map((s, i) => (i === index ? { ...s, label: e.target.value } : s)))} /></label>
                  <button type="button" className="table-action table-action-danger" style={{ alignSelf: "end" }} onClick={() => setStats(stats.filter((_, i) => i !== index))}>Hapus</button>
                </li>
              ))}
            </ul>
            <div className={styles.actions}>
              {stats.length < 4 && <button type="button" className={styles.ghost} onClick={() => setStats([...stats, { value: "", label: "" }])}>+ Tambah angka</button>}
              <button type="button" className="dashboard-action" disabled={saving !== null} onClick={() => save("stats")}>{saving === "stats" ? "Menyimpan…" : "Simpan statistik"}</button>
            </div>
          </section>

          <section className={styles.panel} aria-label="FAQ">
            <div className={styles.panelHead}><div><h2>FAQ</h2><p>Tampil di home page dan halaman Harga.</p></div></div>
            <ul className={styles.list}>
              {faq.map((item, index) => (
                <li key={index} className={styles.item} style={{ display: "grid", gap: 10 }}>
                  <label className={styles.field}><span>Pertanyaan</span><input value={item.q} onChange={(e) => setFaq(faq.map((f, i) => (i === index ? { ...f, q: e.target.value } : f)))} /></label>
                  <label className={styles.field}><span>Jawaban</span><textarea rows={2} value={item.a} onChange={(e) => setFaq(faq.map((f, i) => (i === index ? { ...f, a: e.target.value } : f)))} /></label>
                  <div className={styles.itemActions}>
                    <button type="button" className="table-action" disabled={index === 0} onClick={() => { const next = faq.slice(); [next[index - 1], next[index]] = [next[index], next[index - 1]]; setFaq(next); }}>↑</button>
                    <button type="button" className="table-action table-action-danger" onClick={() => setFaq(faq.filter((_, i) => i !== index))}>Hapus</button>
                  </div>
                </li>
              ))}
            </ul>
            <div className={styles.actions}>
              <button type="button" className={styles.ghost} onClick={() => setFaq([...faq, { q: "", a: "" }])}>+ Tambah pertanyaan</button>
              <button type="button" className="dashboard-action" disabled={saving !== null} onClick={() => save("faq")}>{saving === "faq" ? "Menyimpan…" : "Simpan FAQ"}</button>
            </div>
          </section>
        </div>
      )}
    </DashboardShell>
  );
}
