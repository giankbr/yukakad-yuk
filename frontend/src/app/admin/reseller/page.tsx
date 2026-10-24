"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { defaultReseller, mergeReseller, type ResellerContent } from "@/lib/site-content";
import { useAdminAuth } from "@/lib/useAuthToken";

type TitledKey = "audiences" | "benefits" | "steps";
type ListKey = TitledKey | "faq";

const TITLED: { key: TitledKey; title: string; hint: string; add: string }[] = [
  { key: "audiences", title: "Untuk siapa", hint: "Kartu bernomor jenis usaha yang cocok jadi mitra. Paling rapi 4 kartu.", add: "+ Tambah jenis usaha" },
  { key: "benefits", title: "Keuntungan", hint: "Kenapa jadi mitra Rawuh. Paling rapi 4 kartu.", add: "+ Tambah keuntungan" },
  { key: "steps", title: "Cara kerja", hint: "Langkah dari daftar sampai undangan terkirim, urut.", add: "+ Tambah langkah" },
];

export default function AdminResellerPage() {
  const { token, ready } = useAdminAuth();
  const [form, setForm] = useState<ResellerContent>(defaultReseller);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready || !token) return;
    apiFetch("/api/admin/site-content/reseller", token)
      .then((r) => (r.ok ? r.json() : {}))
      .then((saved: Partial<ResellerContent>) => setForm(mergeReseller(saved)))
      .catch(() => setError("Gagal memuat konten"))
      .finally(() => setLoading(false));
  }, [ready, token]);

  const set = <K extends keyof ResellerContent>(key: K, value: ResellerContent[K]) => { setForm((f) => ({ ...f, [key]: value })); setNotice(""); };
  function setItem<K extends ListKey>(key: K, index: number, patch: Partial<ResellerContent[K][number]>) {
    set(key, (form[key] as ResellerContent[K][number][]).map((item, i) => (i === index ? { ...item, ...patch } : item)) as ResellerContent[K]);
  }
  const remove = (key: ListKey, index: number) => set(key, (form[key] as unknown[]).filter((_, i) => i !== index) as never);
  const add = <K extends ListKey>(key: K, item: ResellerContent[K][number]) => set(key, [...form[key], item] as ResellerContent[K]);
  const move = (key: ListKey, index: number, delta: number) => {
    const next = (form[key] as unknown[]).slice();
    [next[index], next[index + delta]] = [next[index + delta], next[index]];
    set(key, next as never);
  };

  async function save() {
    if (!token) return;
    setSaving(true);
    setError("");
    setNotice("");
    try {
      const response = await apiFetch("/api/admin/site-content/reseller", token, { method: "PUT", body: JSON.stringify(form) });
      if (!response.ok) throw new Error();
      setNotice("Tersimpan. Halaman Reseller diperbarui dalam ±1 menit.");
    } catch {
      setError("Belum tersimpan. Coba lagi.");
    } finally {
      setSaving(false);
    }
  }

  if (!ready || !token) return null;

  const order = (key: ListKey, index: number, length: number) => (
    <div className={styles.itemActions}>
      <button type="button" className="table-action" aria-label="Naikkan" disabled={index === 0} onClick={() => move(key, index, -1)}>↑</button>
      <button type="button" className="table-action" aria-label="Turunkan" disabled={index === length - 1} onClick={() => move(key, index, 1)}>↓</button>
      <button type="button" className="table-action table-action-danger" onClick={() => remove(key, index)}>Hapus</button>
    </div>
  );

  return (
    <DashboardShell active="reseller" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Halaman</p>
          <h1>Program Reseller</h1>
          <p className="dashboard-subtitle">Isi halaman /reseller. Tombol daftar membuka WhatsApp admin (nomornya diatur di menu Kontak).</p>
        </div>
        <a className="secondary-action" href="/reseller" target="_blank" rel="noreferrer">Lihat halaman ↗</a>
      </header>

      {loading ? <p className="dashboard-state">Memuat…</p> : (
        <div className={styles.form}>
          <section className={styles.panel} aria-label="Pembuka">
            <h2>Pembuka</h2>
            <div className={styles.row}>
              <label className={styles.field}><span>Judul (bagian biasa)</span><input value={form.title_lead} onChange={(e) => set("title_lead", e.target.value)} /></label>
              <label className={styles.field}><span>Judul (bagian aksen)</span><input value={form.title_mono} onChange={(e) => set("title_mono", e.target.value)} /></label>
            </div>
            <label className={styles.field}><span>Paragraf pembuka</span><textarea rows={3} value={form.lead} onChange={(e) => set("lead", e.target.value)} /></label>
          </section>

          {TITLED.map(({ key, title, hint, add: addLabel }) => (
            <section key={key} className={styles.panel} aria-label={title}>
              <div className={styles.panelHead}><div><h2>{title}</h2><p>{hint}</p></div></div>
              <ul className={styles.list}>
                {form[key].map((item, index) => (
                  <li key={index} className={styles.item}>
                    <span className={styles.badge}>{String(index + 1).padStart(2, "0")}</span>
                    <div className={styles.cells}>
                      <label className={styles.field}><span>Judul</span><input value={item.title} maxLength={60} onChange={(e) => setItem(key, index, { title: e.target.value })} /></label>
                      <label className={styles.field}><span>Penjelasan</span><input value={item.text} maxLength={160} onChange={(e) => setItem(key, index, { text: e.target.value })} /></label>
                    </div>
                    {order(key, index, form[key].length)}
                  </li>
                ))}
              </ul>
              {form[key].length < 8 && <button type="button" className={styles.ghost} style={{ justifySelf: "start" }} onClick={() => add(key, { title: "", text: "" })}>{addLabel}</button>}
            </section>
          ))}

          <section className={styles.panel} aria-label="Ketentuan dan komisi">
            <div className={styles.panelHead}><div><h2>Ketentuan & komisi</h2><p>Besaran komisi atau harga mitra, cara bayar, syarat. Kosongkan untuk menyembunyikan kotaknya.</p></div></div>
            <label className={styles.field}><span>Isi (pisahkan paragraf dengan baris kosong)</span><textarea rows={5} value={form.terms} onChange={(e) => set("terms", e.target.value)} placeholder="Contoh: Komisi …% dari setiap paket yang terjual, dibayarkan setiap tanggal …" /></label>
          </section>

          <section className={styles.panel} aria-label="FAQ">
            <div className={styles.panelHead}><div><h2>FAQ</h2><p>Pertanyaan yang sering ditanyakan calon mitra.</p></div></div>
            <ul className={styles.list}>
              {form.faq.map((item, index) => (
                <li key={index} className={styles.item}>
                  <div className={styles.cells}>
                    <label className={styles.field}><span>Pertanyaan</span><input value={item.q} maxLength={120} onChange={(e) => setItem("faq", index, { q: e.target.value })} /></label>
                    <label className={styles.field}><span>Jawaban</span><textarea rows={2} value={item.a} maxLength={400} onChange={(e) => setItem("faq", index, { a: e.target.value })} /></label>
                  </div>
                  {order("faq", index, form.faq.length)}
                </li>
              ))}
            </ul>
            <button type="button" className={styles.ghost} style={{ justifySelf: "start" }} onClick={() => add("faq", { q: "", a: "" })}>+ Tambah pertanyaan</button>
          </section>

          <section className={styles.panel} aria-label="Ajakan bergabung">
            <h2>Ajakan bergabung</h2>
            <div className={styles.row}>
              <label className={styles.field}><span>Judul</span><input value={form.cta_heading} onChange={(e) => set("cta_heading", e.target.value)} /></label>
              <label className={styles.field}><span>Pesan WhatsApp otomatis</span><input value={form.wa_message} onChange={(e) => set("wa_message", e.target.value)} /></label>
            </div>
          </section>

          <div className={styles.saveBar}>
            <button type="button" className="dashboard-action" disabled={saving} onClick={save}>{saving ? "Menyimpan…" : "Simpan halaman Reseller"}</button>
            {notice && <span role="status" className={styles.ok}>{notice}</span>}
            {error && <span role="alert" className={styles.error}>{error}</span>}
          </div>
        </div>
      )}
    </DashboardShell>
  );
}
