"use client";

import { useCallback, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";
import styles from "@/components/dashboard/editor.module.css";
import { friendly, GateNotice, getJson, lostAccess, usePageGate } from "../_lib";

type Story = { id: string; title?: string; content: string; date?: string; image_url?: string };
type Draft = Omit<Story, "id"> & { id?: string };

const EMPTY: Draft = { title: "", content: "", date: "", image_url: "" };

export default function StoriesPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const invitationId = routeParams?.id;
  const [items, setItems] = useState<Story[]>([]);
  const [draft, setDraft] = useState<Draft | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const gate = usePageGate(invitationId, token, "stories");
  const { lose } = gate;
  const allowed = gate.status === "ok";

  const load = useCallback(async () => {
    if (!token || !invitationId) return;
    const result = await getJson<{ items?: Story[] }>(`/api/invitations/${invitationId}/stories`, token);
    if (lostAccess(result.status)) { lose(); return; }
    if (!result.ok) { setError(result.error || "Gagal memuat kisah."); return; }
    setItems(result.data?.items ?? []);
  }, [token, invitationId, lose]);

  useEffect(() => {
    if (!ready || !allowed) return;
    const timer = setTimeout(() => { load().finally(() => setLoading(false)); }, 0);
    return () => clearTimeout(timer);
  }, [ready, allowed, load]);

  async function upload(file: File) {
    if (!token || !invitationId) return;
    setUploading(true);
    setError("");
    try {
      const form = new FormData();
      form.append("file", file);
      form.append("type", "gallery");
      const response = await apiFetch(`/api/invitations/${invitationId}/media`, token, { method: "POST", body: form });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(body.error);
      setDraft((d) => (d ? { ...d, image_url: body.path } : d));
    } catch {
      setError("Foto belum terunggah. Gunakan JPG, PNG, atau WebP maksimal 10 MB.");
    } finally {
      setUploading(false);
    }
  }

  async function save(event: React.FormEvent) {
    event.preventDefault();
    if (!token || !invitationId || !draft) return;
    setSaving(true);
    setError("");
    try {
      const payload = { title: draft.title?.trim(), content: draft.content.trim(), date: draft.date?.trim(), image_url: draft.image_url };
      const response = draft.id
        ? await apiFetch(`/api/invitations/${invitationId}/stories/${draft.id}`, token, { method: "PUT", body: JSON.stringify(payload) })
        : await apiFetch(`/api/invitations/${invitationId}/stories`, token, { method: "POST", body: JSON.stringify(payload) });
      if (!response.ok) throw new Error(((await response.json().catch(() => ({}))) as { error?: string }).error ?? "");
      setDraft(null);
      await load();
    } catch (err) {
      const message = friendly(err, "");
      setError(message ? `Kisah belum tersimpan: ${message}` : "Kisah belum tersimpan.");
    } finally {
      setSaving(false);
    }
  }

  async function remove(item: Story) {
    if (!token || !invitationId || !window.confirm(`Hapus kisah "${item.title || item.content.slice(0, 30)}"?`)) return;
    const response = await apiFetch(`/api/invitations/${invitationId}/stories/${item.id}`, token, { method: "DELETE" });
    if (!response.ok) { setError("Kisah belum terhapus."); return; }
    await load();
  }

  if (!ready || !invitationId) return null;

  if (!allowed) {
    return (
      <DashboardShell active="stories" invitationId={invitationId}>
        <GateNotice gate={gate} invitationId={invitationId} />
      </DashboardShell>
    );
  }

  return (
    <DashboardShell active="stories" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>Kisah cinta</h1>
          <p className="dashboard-subtitle">Momen-momen perjalanan kalian, tampil sebagai linimasa di undangan.</p>
        </div>
        {!draft && <button type="button" className="dashboard-action" onClick={() => setDraft({ ...EMPTY })}>+ Tambah momen</button>}
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}

      {loading ? <p className="dashboard-state">Memuat...</p> : (
        <div className={styles.form}>
          {draft && (
            <form className={styles.editor} onSubmit={save} aria-label={draft.id ? "Ubah momen" : "Tambah momen"}>
              <div className={styles.person}>
                <label className={styles.photo}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  {draft.image_url ? <img src={draft.image_url} alt="" /> : <span>{uploading ? "…" : "+ Foto"}</span>}
                  <input type="file" accept="image/jpeg,image/png,image/webp" hidden disabled={uploading}
                    onChange={(e) => { const file = e.target.files?.[0]; e.target.value = ""; if (file) void upload(file); }} />
                </label>
                <div className={styles.fields}>
                  <div className={styles.row}>
                    <label className={styles.field}><span>Judul</span>
                      <input value={draft.title ?? ""} onChange={(e) => setDraft({ ...draft, title: e.target.value })} placeholder="Pertama bertemu" maxLength={80} />
                    </label>
                    <label className={styles.field}><span>Waktu</span>
                      <input value={draft.date ?? ""} onChange={(e) => setDraft({ ...draft, date: e.target.value })} placeholder="2019 atau Juni 2021" maxLength={40} />
                    </label>
                  </div>
                  <label className={styles.field}><span>Cerita</span>
                    <textarea rows={4} required maxLength={800} value={draft.content} onChange={(e) => setDraft({ ...draft, content: e.target.value })} placeholder="Ceritakan momen ini dalam beberapa kalimat." />
                  </label>
                </div>
              </div>
              <div className={styles.actions}>
                <button type="submit" className="dashboard-action" disabled={saving || uploading}>{saving ? "Menyimpan..." : draft.id ? "Simpan momen" : "Tambah momen"}</button>
                <button type="button" className={styles.ghost} onClick={() => setDraft(null)}>Batal</button>
                {draft.image_url && <button type="button" className={styles.link} onClick={() => setDraft({ ...draft, image_url: "" })}>Hapus foto</button>}
              </div>
            </form>
          )}

          {items.length === 0 && !draft ? (
            <div className="dashboard-empty">
              <h2>Belum ada kisah</h2>
              <p>Tambahkan 3–5 momen, misalnya pertama bertemu, jadian, lamaran, hingga hari H.</p>
              <div className="dashboard-empty-actions"><button type="button" className="dashboard-action" onClick={() => setDraft({ ...EMPTY })}>+ Tambah momen pertama</button></div>
            </div>
          ) : (
            <ul className={styles.list}>
              {items.map((item) => draft?.id === item.id ? null : (
                <li key={item.id} className={styles.item}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  {item.image_url ? <img className={styles.thumb} src={item.image_url} alt="" /> : <span className={styles.badge}>{item.date || "—"}</span>}
                  <div className={styles.itemBody}>
                    <strong>{item.title || "Tanpa judul"}{item.date && item.image_url ? ` · ${item.date}` : ""}</strong>
                    <small>{item.content}</small>
                  </div>
                  <div className={styles.itemActions}>
                    <button type="button" className="table-action" onClick={() => setDraft({ ...item })}>Ubah</button>
                    <button type="button" className="table-action table-action-danger" onClick={() => remove(item)}>Hapus</button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </DashboardShell>
  );
}
