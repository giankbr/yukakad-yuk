"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { ImageField } from "@/components/dashboard/ImageField";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { defaultAbout, mergeAbout, type AboutContent } from "@/lib/site-content";
import { useAdminAuth } from "@/lib/useAuthToken";

type ListKey = "stats" | "principles" | "milestones" | "team";

export default function AdminAboutPage() {
  const { token, ready } = useAdminAuth();
  const [form, setForm] = useState<AboutContent>(defaultAbout);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready || !token) return;
    apiFetch("/api/admin/site-content/about", token)
      .then((r) => (r.ok ? r.json() : {}))
      .then((saved: Partial<AboutContent>) => setForm(mergeAbout(saved)))
      .catch(() => setError("Gagal memuat konten"))
      .finally(() => setLoading(false));
  }, [ready, token]);

  const set = <K extends keyof AboutContent>(key: K, value: AboutContent[K]) => { setForm((f) => ({ ...f, [key]: value })); setNotice(""); };
  function setItem<K extends ListKey>(key: K, index: number, patch: Partial<AboutContent[K][number]>) {
    set(key, (form[key] as AboutContent[K][number][]).map((item, i) => (i === index ? { ...item, ...patch } : item)) as AboutContent[K]);
  }
  const remove = (key: ListKey, index: number) => set(key, (form[key] as unknown[]).filter((_, i) => i !== index) as never);
  const add = <K extends ListKey>(key: K, item: AboutContent[K][number]) => set(key, [...form[key], item] as AboutContent[K]);
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
      const response = await apiFetch("/api/admin/site-content/about", token, { method: "PUT", body: JSON.stringify(form) });
      if (!response.ok) throw new Error();
      setNotice("Tersimpan. Halaman Tentang diperbarui dalam ±1 menit.");
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
    <DashboardShell active="about" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Halaman</p>
          <h1>Tentang kami</h1>
          <p className="dashboard-subtitle">Cerita, angka, prinsip, perjalanan, tim, dan kontak kantor di halaman /tentang.</p>
        </div>
        <a className="secondary-action" href="/tentang" target="_blank" rel="noreferrer">Lihat halaman ↗</a>
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
            <ImageField label="Foto utama (lebar)" value={form.photo} onChange={(v) => set("photo", v)} token={token} folder="about" hint="Rasio ±16:7, minimal 1600px." />
          </section>

          <section className={styles.panel} aria-label="Angka">
            <div className={styles.panelHead}><div><h2>Angka</h2><p>Baris angka di bawah foto utama. Maksimal 4.</p></div></div>
            <ul className={styles.list}>
              {form.stats.map((item, index) => (
                <li key={index} className={styles.item}>
                  <div className={`${styles.cells} ${styles.row}`}>
                    <label className={styles.field}><span>Angka</span><input value={item.value} maxLength={12} onChange={(e) => setItem("stats", index, { value: e.target.value })} /></label>
                    <label className={styles.field}><span>Keterangan</span><input value={item.label} maxLength={60} onChange={(e) => setItem("stats", index, { label: e.target.value })} /></label>
                  </div>
                  {order("stats", index, form.stats.length)}
                </li>
              ))}
            </ul>
            {form.stats.length < 4 && <button type="button" className={styles.ghost} style={{ justifySelf: "start" }} onClick={() => add("stats", { value: "", label: "" })}>+ Tambah angka</button>}
          </section>

          <section className={styles.panel} aria-label="Cerita">
            <h2>Cerita kami</h2>
            <label className={styles.field}><span>Judul</span><input value={form.story_title} onChange={(e) => set("story_title", e.target.value)} /></label>
            <label className={styles.field}><span>Isi cerita (pisahkan paragraf dengan baris kosong)</span><textarea rows={7} value={form.story} onChange={(e) => set("story", e.target.value)} /></label>
            <div className={styles.row}>
              <label className={styles.field}><span>Kutipan (kosongkan untuk menyembunyikan)</span><textarea rows={2} value={form.quote} onChange={(e) => set("quote", e.target.value)} /></label>
              <label className={styles.field}><span>Oleh</span><input value={form.quote_by} onChange={(e) => set("quote_by", e.target.value)} placeholder="Nama, jabatan" /></label>
            </div>
          </section>

          <section className={styles.panel} aria-label="Prinsip">
            <div className={styles.panelHead}><div><h2>Prinsip</h2><p>Kartu bernomor “Yang kami pegang”. Paling rapi 4 kartu.</p></div></div>
            <ul className={styles.list}>
              {form.principles.map((item, index) => (
                <li key={index} className={styles.item}>
                  <span className={styles.badge}>{String(index + 1).padStart(2, "0")}</span>
                  <div className={styles.cells}>
                    <label className={styles.field}><span>Judul</span><input value={item.title} maxLength={60} onChange={(e) => setItem("principles", index, { title: e.target.value })} /></label>
                    <label className={styles.field}><span>Penjelasan</span><input value={item.text} maxLength={140} onChange={(e) => setItem("principles", index, { text: e.target.value })} /></label>
                  </div>
                  {order("principles", index, form.principles.length)}
                </li>
              ))}
            </ul>
            {form.principles.length < 8 && <button type="button" className={styles.ghost} style={{ justifySelf: "start" }} onClick={() => add("principles", { title: "", text: "" })}>+ Tambah prinsip</button>}
          </section>

          <section className={styles.panel} aria-label="Perjalanan">
            <div className={styles.panelHead}><div><h2>Perjalanan</h2><p>Linimasa dari awal sampai sekarang, urut dari yang paling lama.</p></div></div>
            <label className={styles.field}><span>Judul</span><input value={form.journey_title} onChange={(e) => set("journey_title", e.target.value)} /></label>
            <ul className={styles.list}>
              {form.milestones.map((item, index) => (
                <li key={index} className={styles.item}>
                  <div className={`${styles.cells} ${styles.row3}`}>
                    <label className={styles.field}><span>Tahun</span><input value={item.year} maxLength={10} onChange={(e) => setItem("milestones", index, { year: e.target.value })} /></label>
                    <label className={styles.field}><span>Judul</span><input value={item.title} maxLength={50} onChange={(e) => setItem("milestones", index, { title: e.target.value })} /></label>
                    <label className={styles.field}><span>Keterangan</span><input value={item.text} maxLength={120} onChange={(e) => setItem("milestones", index, { text: e.target.value })} /></label>
                  </div>
                  {order("milestones", index, form.milestones.length)}
                </li>
              ))}
            </ul>
            <button type="button" className={styles.ghost} style={{ justifySelf: "start" }} onClick={() => add("milestones", { year: String(new Date().getFullYear()), title: "", text: "" })}>+ Tambah momen</button>
          </section>

          <section className={styles.panel} aria-label="Tim">
            <div className={styles.panelHead}><div><h2>Tim</h2><p>Foto potret 3:4 terlihat paling rapi.</p></div></div>
            <div className={styles.row}>
              <label className={styles.field}><span>Judul</span><input value={form.team_title} onChange={(e) => set("team_title", e.target.value)} /></label>
              <label className={styles.field}><span>Info lowongan (kosongkan untuk menyembunyikan)</span><input value={form.open_roles} onChange={(e) => set("open_roles", e.target.value)} /></label>
            </div>
            <ul className={styles.list}>
              {form.team.map((member, index) => (
                <li key={index} className={styles.item}>
                  <div className={styles.cells}>
                    <div className={styles.row}>
                      <label className={styles.field}><span>Nama</span><input value={member.name} onChange={(e) => setItem("team", index, { name: e.target.value })} /></label>
                      <label className={styles.field}><span>Peran</span><input value={member.role} onChange={(e) => setItem("team", index, { role: e.target.value })} /></label>
                    </div>
                    <ImageField label="Foto" value={member.photo} onChange={(v) => setItem("team", index, { photo: v })} token={token} folder="team" />
                  </div>
                  {order("team", index, form.team.length)}
                </li>
              ))}
            </ul>
            <button type="button" className={styles.ghost} style={{ justifySelf: "start" }} onClick={() => add("team", { name: "", role: "", photo: "" })}>+ Tambah anggota</button>
          </section>

          <section className={styles.panel} aria-label="Kontak kantor">
            <div className={styles.panelHead}><div><h2>Kontak kantor</h2><p>Nomor WhatsApp diatur di menu Kontak.</p></div></div>
            <div className={styles.row}>
              <label className={styles.field}><span>Alamat</span><input value={form.address} onChange={(e) => set("address", e.target.value)} /></label>
              <label className={styles.field}><span>Email</span><input type="email" value={form.email} onChange={(e) => set("email", e.target.value)} /></label>
            </div>
          </section>

          <div className={styles.saveBar}>
            <button type="button" className="dashboard-action" disabled={saving} onClick={save}>{saving ? "Menyimpan…" : "Simpan halaman Tentang"}</button>
            {notice && <span role="status" className={styles.ok}>{notice}</span>}
            {error && <span role="alert" className={styles.error}>{error}</span>}
          </div>
        </div>
      )}
    </DashboardShell>
  );
}
