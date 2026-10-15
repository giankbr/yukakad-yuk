"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { privacy, terms } from "@/lib/legal";
import { legalToContent, type LegalContent } from "@/lib/site-content";
import { useAdminAuth } from "@/lib/useAuthToken";

type Doc = "terms" | "privacy";
type Form = Required<LegalContent>;
const DOCS: Record<Doc, { label: string; href: string; defaults: Form }> = {
  terms: { label: "Syarat & Ketentuan", href: "/syarat-ketentuan", defaults: legalToContent(terms) },
  privacy: { label: "Kebijakan Privasi", href: "/kebijakan-privasi", defaults: legalToContent(privacy) },
};

const pick = (saved: LegalContent, defaults: Form): Form => ({
  updated: saved.updated?.trim() ? saved.updated : defaults.updated,
  intro: saved.intro?.trim() ? saved.intro : defaults.intro,
  summary: saved.summary?.length ? saved.summary : defaults.summary,
  sections: saved.sections?.length ? saved.sections : defaults.sections,
});

const today = () => new Date().toLocaleDateString("id-ID", { day: "numeric", month: "long", year: "numeric" });

export default function AdminLegalPage() {
  const { token, ready } = useAdminAuth();
  const [doc, setDoc] = useState<Doc>("terms");
  const [forms, setForms] = useState<Record<Doc, Form>>({ terms: DOCS.terms.defaults, privacy: DOCS.privacy.defaults });
  const [dirty, setDirty] = useState<Record<Doc, boolean>>({ terms: false, privacy: false });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready || !token) return;
    const get = (key: Doc) => apiFetch(`/api/admin/site-content/${key}`, token).then((r) => (r.ok ? r.json() : {})).catch(() => ({}));
    Promise.all([get("terms"), get("privacy")])
      .then(([t, p]: [LegalContent, LegalContent]) => setForms({ terms: pick(t, DOCS.terms.defaults), privacy: pick(p, DOCS.privacy.defaults) }))
      .finally(() => setLoading(false));
  }, [ready, token]);

  const form = forms[doc];
  const update = (patch: Partial<Form>) => {
    setForms((current) => ({ ...current, [doc]: { ...current[doc], ...patch } }));
    setDirty((current) => ({ ...current, [doc]: true }));
    setNotice("");
  };
  const setSection = (index: number, patch: Partial<Form["sections"][number]>) => update({ sections: form.sections.map((s, i) => (i === index ? { ...s, ...patch } : s)) });
  const move = (index: number, delta: number) => {
    const next = form.sections.slice();
    [next[index], next[index + delta]] = [next[index + delta], next[index]];
    update({ sections: next });
  };

  async function save() {
    if (!token) return;
    setSaving(true);
    setError("");
    setNotice("");
    const body: Form = {
      ...form,
      summary: form.summary.filter((s) => s.title.trim() && s.text.trim()),
      sections: form.sections.filter((s) => s.title.trim() && s.body.trim()),
    };
    try {
      const response = await apiFetch(`/api/admin/site-content/${doc}`, token, { method: "PUT", body: JSON.stringify(body) });
      if (!response.ok) throw new Error();
      setDirty((current) => ({ ...current, [doc]: false }));
      setNotice(`${DOCS[doc].label} tersimpan. Halaman publik diperbarui dalam ±1 menit.`);
    } catch {
      setError("Belum tersimpan. Coba lagi.");
    } finally {
      setSaving(false);
    }
  }

  if (!ready || !token) return null;

  return (
    <DashboardShell active="legal" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Halaman</p>
          <h1>Legal</h1>
          <p className="dashboard-subtitle">Isi Syarat &amp; Ketentuan dan Kebijakan Privasi. Pastikan perubahan sudah ditinjau sebelum disimpan.</p>
        </div>
        <a className="secondary-action" href={DOCS[doc].href} target="_blank" rel="noreferrer">Lihat halaman ↗</a>
      </header>

      <div className={styles.tabs} role="group" aria-label="Dokumen" style={{ marginBottom: 16 }}>
        {(Object.keys(DOCS) as Doc[]).map((key) => (
          <button key={key} type="button" aria-pressed={doc === key} onClick={() => { setDoc(key); setNotice(""); setError(""); }}>
            {DOCS[key].label}{dirty[key] ? " •" : ""}
          </button>
        ))}
      </div>

      {loading ? <p className="dashboard-state">Memuat…</p> : (
        <div className={styles.form}>
          <section className={styles.panel} aria-label="Pembuka">
            <h2>Pembuka</h2>
            <div className={styles.row}>
              <label className={styles.field}><span>Terakhir diperbarui</span><input value={form.updated} onChange={(e) => update({ updated: e.target.value })} /></label>
              <div className={styles.field} style={{ alignContent: "end" }}><button type="button" className={styles.ghost} style={{ justifySelf: "start" }} onClick={() => update({ updated: today() })}>Pakai tanggal hari ini</button></div>
            </div>
            <label className={styles.field}><span>Paragraf pembuka</span><textarea rows={3} value={form.intro} onChange={(e) => update({ intro: e.target.value })} /></label>
          </section>

          <section className={styles.panel} aria-label="Ringkasan">
            <div className={styles.panelHead}><div><h2>Ringkasan</h2><p>Tiga poin singkat di atas dokumen.</p></div></div>
            <ul className={styles.list}>
              {form.summary.map((item, index) => (
                <li key={index} className={styles.item}>
                  <div className={styles.cells}>
                    <label className={styles.field}><span>Judul poin {index + 1}</span><input value={item.title} maxLength={60} onChange={(e) => update({ summary: form.summary.map((s, i) => (i === index ? { ...s, title: e.target.value } : s)) })} /></label>
                    <label className={styles.field}><span>Penjelasan</span><input value={item.text} maxLength={200} onChange={(e) => update({ summary: form.summary.map((s, i) => (i === index ? { ...s, text: e.target.value } : s)) })} /></label>
                  </div>
                  <div className={styles.itemActions}><button type="button" className="table-action table-action-danger" onClick={() => update({ summary: form.summary.filter((_, i) => i !== index) })}>Hapus</button></div>
                </li>
              ))}
            </ul>
            {form.summary.length < 4 && <button type="button" className={styles.ghost} style={{ justifySelf: "start" }} onClick={() => update({ summary: [...form.summary, { title: "", text: "" }] })}>+ Tambah poin</button>}
          </section>

          <section className={styles.panel} aria-label="Isi dokumen">
            <div className={styles.panelHead}>
              <div><h2>Isi dokumen</h2><p>Pisahkan paragraf dengan satu baris kosong. Baris yang diawali “- ” jadi daftar berpoin.</p></div>
            </div>
            <ol className={styles.list}>
              {form.sections.map((section, index) => (
                <li key={index} className={styles.item}>
                  <span className={styles.badge}>{String(index + 1).padStart(2, "0")}</span>
                  <div className={styles.cells}>
                    <label className={styles.field}><span>Judul bagian</span><input value={section.title} onChange={(e) => setSection(index, { title: e.target.value })} /></label>
                    <label className={styles.field}><span>Isi</span><textarea rows={Math.min(14, Math.max(4, section.body.split("\n").length + 1))} value={section.body} onChange={(e) => setSection(index, { body: e.target.value })} /></label>
                  </div>
                  <div className={styles.itemActions}>
                    <button type="button" className="table-action" aria-label="Naikkan" disabled={index === 0} onClick={() => move(index, -1)}>↑</button>
                    <button type="button" className="table-action" aria-label="Turunkan" disabled={index === form.sections.length - 1} onClick={() => move(index, 1)}>↓</button>
                    <button type="button" className="table-action table-action-danger" onClick={() => { if (window.confirm(`Hapus bagian “${section.title || "tanpa judul"}”?`)) update({ sections: form.sections.filter((_, i) => i !== index) }); }}>Hapus</button>
                  </div>
                </li>
              ))}
            </ol>
            <button type="button" className={styles.ghost} style={{ justifySelf: "start" }} onClick={() => update({ sections: [...form.sections, { title: "", body: "" }] })}>+ Tambah bagian</button>
          </section>

          <div className={styles.saveBar}>
            <button type="button" className="dashboard-action" disabled={saving} onClick={save}>{saving ? "Menyimpan…" : `Simpan ${DOCS[doc].label}`}</button>
            <button type="button" className={styles.ghost} disabled={saving} onClick={() => { if (window.confirm("Kembalikan ke teks bawaan? Perubahan yang belum disimpan hilang.")) update(DOCS[doc].defaults); }}>Kembalikan teks bawaan</button>
            {notice && <span role="status" className={styles.ok}>{notice}</span>}
            {error && <span role="alert" className={styles.error}>{error}</span>}
          </div>
        </div>
      )}
    </DashboardShell>
  );
}
