"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { ImageField } from "@/components/dashboard/ImageField";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { defaultProducts, mergeProducts, PRODUCT_PERK_ICONS, type ProductContent } from "@/lib/products";
import { useAdminAuth } from "@/lib/useAuthToken";

type PairKey = "stats" | "steps" | "perks";
const ICON_LABELS: Record<string, string> = {
  user: "Orang", users: "Grup", calendar: "Kalender", pin: "Lokasi", images: "Galeri", music: "Musik", gift: "Hadiah", sparkle: "Kilau",
  refresh: "Ulangi", link: "Tautan", wifi: "Offline", download: "Unduh", file: "Kertas", mail: "Amplop", truck: "Kirim", qr: "QR", globe: "Web", video: "Video", printer: "Cetak",
};
const LINK_HINT = "Isi “contact” untuk membuka WhatsApp admin.";

export default function AdminProductsPage() {
  const { token, ready } = useAdminAuth();
  const [items, setItems] = useState<ProductContent[]>(defaultProducts);
  const [slug, setSlug] = useState(defaultProducts[0].slug);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready || !token) return;
    apiFetch("/api/admin/site-content/products", token)
      .then((r) => (r.ok ? r.json() : {}))
      .then((saved: { items?: unknown }) => setItems(mergeProducts(saved.items)))
      .catch(() => setError("Gagal memuat produk"))
      .finally(() => setLoading(false));
  }, [ready, token]);

  const product = items.find((item) => item.slug === slug) ?? items[0];
  const update = (patch: Partial<ProductContent>) => {
    setItems((current) => current.map((item) => (item.slug === product.slug ? { ...item, ...patch } : item)));
    setNotice("");
  };
  const setPair = (key: PairKey, index: number, side: 0 | 1, value: string) =>
    update({ [key]: product[key].map((pair, i) => (i === index ? (side === 0 ? [value, pair[1]] : [pair[0], value]) : pair)) });

  async function save() {
    if (!token) return;
    setSaving(true);
    setError("");
    setNotice("");
    try {
      const response = await apiFetch("/api/admin/site-content/products", token, { method: "PUT", body: JSON.stringify({ items }) });
      if (!response.ok) throw new Error();
      setNotice("Semua produk tersimpan. Halaman produk diperbarui dalam ±1 menit.");
    } catch {
      setError("Belum tersimpan. Coba lagi.");
    } finally {
      setSaving(false);
    }
  }

  if (!ready || !token) return null;

  const pairs = (key: PairKey, title: string, hint: string, labels: [string, string], max: number) => (
    <section className={styles.panel} aria-label={title}>
      <div className={styles.panelHead}><div><h2>{title}</h2><p>{hint}</p></div></div>
      <ul className={styles.list}>
        {product[key].map((pair, index) => (
          <li key={index} className={styles.item}>
            <div className={`${styles.cells} ${styles.row}`}>
              {key === "perks" ? (
                <label className={styles.field}><span>Ikon</span>
                  <select value={pair[0]} onChange={(e) => setPair(key, index, 0, e.target.value)}>
                    {PRODUCT_PERK_ICONS.map((name) => <option key={name} value={name}>{ICON_LABELS[name] ?? name}</option>)}
                  </select>
                </label>
              ) : (
                <label className={styles.field}><span>{labels[0]}</span><input value={pair[0]} maxLength={40} onChange={(e) => setPair(key, index, 0, e.target.value)} /></label>
              )}
              <label className={styles.field}><span>{labels[1]}</span><input value={pair[1]} maxLength={120} onChange={(e) => setPair(key, index, 1, e.target.value)} /></label>
            </div>
            <div className={styles.itemActions}>
              <button type="button" className="table-action table-action-danger" onClick={() => update({ [key]: product[key].filter((_, i) => i !== index) })}>Hapus</button>
            </div>
          </li>
        ))}
      </ul>
      {product[key].length < max && (
        <button type="button" className={styles.ghost} style={{ justifySelf: "start" }} onClick={() => update({ [key]: [...product[key], [key === "perks" ? "sparkle" : "", ""]] })}>+ Tambah</button>
      )}
    </section>
  );

  return (
    <DashboardShell active="products" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Halaman</p>
          <h1>Produk</h1>
          <p className="dashboard-subtitle">Isi halaman tiap produk: judul, harga, gambar, angka, cara kerja, dan daftar keunggulan.</p>
        </div>
        <a className="secondary-action" href={`/produk/${product.slug}`} target="_blank" rel="noreferrer">Lihat halaman ↗</a>
      </header>

      <div className={styles.tabs} role="group" aria-label="Produk" style={{ marginBottom: 16 }}>
        {items.map((item) => (
          <button key={item.slug} type="button" aria-pressed={item.slug === product.slug} onClick={() => setSlug(item.slug)}>{item.name}</button>
        ))}
      </div>

      {loading ? <p className="dashboard-state">Memuat…</p> : (
        <div className={styles.form}>
          <section className={styles.panel} aria-label="Hero">
            <h2>Bagian atas</h2>
            <div className={styles.row}>
              <label className={styles.field}><span>Nama produk</span><input value={product.name} maxLength={40} onChange={(e) => update({ name: e.target.value })} /></label>
              <label className={styles.field}><span>Harga</span><input value={product.price} maxLength={40} onChange={(e) => update({ price: e.target.value })} placeholder="Mulai Rp3.500 / lembar" /></label>
            </div>
            <div className={styles.row}>
              <label className={styles.field}><span>Judul (bagian biasa)</span><input value={product.headline[0]} onChange={(e) => update({ headline: [e.target.value, product.headline[1]] })} /></label>
              <label className={styles.field}><span>Judul (bagian aksen)</span><input value={product.headline[1]} onChange={(e) => update({ headline: [product.headline[0], e.target.value] })} /></label>
            </div>
            <label className={styles.field}><span>Deskripsi</span><textarea rows={3} value={product.lead} onChange={(e) => update({ lead: e.target.value })} /></label>
            <div className={styles.row}>
              <label className={styles.field}><span>Tombol utama</span><input value={product.primary.label} onChange={(e) => update({ primary: { ...product.primary, label: e.target.value } })} /></label>
              <label className={styles.field}><span>Tautan tombol utama</span><input className={styles.mono} value={product.primary.href} onChange={(e) => update({ primary: { ...product.primary, href: e.target.value } })} /></label>
              <label className={styles.field}><span>Tombol kedua</span><input value={product.secondary.label} onChange={(e) => update({ secondary: { ...product.secondary, label: e.target.value } })} /></label>
              <label className={styles.field}><span>Tautan tombol kedua</span><input className={styles.mono} value={product.secondary.href} onChange={(e) => update({ secondary: { ...product.secondary, href: e.target.value } })} /></label>
            </div>
            <p className={styles.hint}>{LINK_HINT}</p>
            <ImageField label="Gambar produk" value={product.image} onChange={(v) => update({ image: v })} token={token} folder="products" hint="Rasio ±4:5, dipakai juga di kartu produk lain." />
          </section>

          {pairs("stats", "Angka", "Tiga angka di bawah bagian atas.", ["Angka", "Keterangan"], 3)}
          {pairs("steps", "Cara kerja", "“Tiga langkah, selesai.” Paling rapi 3 langkah.", ["Langkah", "Penjelasan"], 4)}
          {pairs("perks", "Yang kamu dapat", "Daftar keunggulan dengan ikon. Paling rapi 6 item.", ["Ikon", "Teks"], 9)}

          <div className={styles.saveBar}>
            <button type="button" className="dashboard-action" disabled={saving} onClick={save}>{saving ? "Menyimpan…" : "Simpan semua produk"}</button>
            <button type="button" className={styles.ghost} disabled={saving} onClick={() => { const base = defaultProducts.find((p) => p.slug === product.slug); if (base && window.confirm(`Kembalikan ${product.name} ke isi bawaan?`)) update(base); }}>Kembalikan isi bawaan</button>
            {notice && <span role="status" className={styles.ok}>{notice}</span>}
            {error && <span role="alert" className={styles.error}>{error}</span>}
          </div>
        </div>
      )}
    </DashboardShell>
  );
}
