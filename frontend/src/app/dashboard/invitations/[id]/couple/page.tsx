"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";
import styles from "@/components/dashboard/editor.module.css";
import { GREETINGS } from "@/lib/greetings";

type Couple = {
  groom_name: string; bride_name: string;
  groom_nickname?: string; bride_nickname?: string;
  groom_parents?: string; bride_parents?: string;
  groom_photo?: string; bride_photo?: string;
};
type Invitation = { id: string; slug: string; title: string; published: boolean; couple?: Couple };
type Side = "bride" | "groom";

const EMPTY: Couple = { groom_name: "", bride_name: "" };

export default function CouplePage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [invitation, setInvitation] = useState<Invitation | null>(null);
  const [couple, setCouple] = useState<Couple>(EMPTY);
  const [note, setNote] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [uploading, setUploading] = useState<Side | null>(null);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  const invitationId = routeParams?.id;

  useEffect(() => {
    if (!ready || !token || !invitationId) return;
    Promise.all([
      apiFetch(`/api/invitations/${invitationId}`, token).then((r) => r.json()),
      apiFetch(`/api/invitations/${invitationId}/settings`, token).then((r) => r.json()).catch(() => ({})),
    ])
      .then(([body, settings]: [Invitation, { opening_text?: string }]) => {
        setInvitation(body);
        setCouple({ ...EMPTY, ...body.couple });
        setNote(settings.opening_text ?? "");
      })
      .catch(() => setError("Gagal memuat data mempelai"))
      .finally(() => setLoading(false));
  }, [ready, token, invitationId]);

  const set = (key: keyof Couple, value: string) => { setCouple((c) => ({ ...c, [key]: value })); setNotice(""); };

  async function uploadPhoto(side: Side, file: File) {
    if (!token || !invitationId) return;
    setUploading(side);
    setError("");
    try {
      const form = new FormData();
      form.append("file", file);
      form.append("type", "cover");
      const response = await apiFetch(`/api/invitations/${invitationId}/media`, token, { method: "POST", body: form });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error);
      set(side === "bride" ? "bride_photo" : "groom_photo", body.path);
    } catch {
      setError("Foto belum terunggah. Gunakan JPG, PNG, atau WebP maksimal 10 MB.");
    } finally {
      setUploading(null);
    }
  }

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!token || !invitation) return;
    setSaving(true);
    setNotice("");
    setError("");
    try {
      const [response, settings] = await Promise.all([
        apiFetch(`/api/invitations/${invitation.id}`, token, {
          method: "PUT",
          body: JSON.stringify({ slug: invitation.slug, title: invitation.title, published: invitation.published, couple }),
        }),
        apiFetch(`/api/invitations/${invitation.id}/settings`, token, { method: "PATCH", body: JSON.stringify({ opening_text: note.trim() }) }),
      ]);
      if (!response.ok || !settings.ok) throw new Error();
      setNotice("Tersimpan.");
    } catch {
      setError("Gagal menyimpan perubahan");
    } finally {
      setSaving(false);
    }
  }

  if (!ready || !invitationId) return null;

  function person(side: Side, title: string, parentsHint: string) {
    const photo = side === "bride" ? couple.bride_photo : couple.groom_photo;
    return (
      <section className={styles.panel} aria-label={title}>
        <h2>{title}</h2>
        <div className={styles.person}>
          <label className={styles.photo}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            {photo ? <img src={photo} alt="" /> : <span>{uploading === side ? "…" : "+ Foto"}</span>}
            <input type="file" accept="image/jpeg,image/png,image/webp" hidden disabled={uploading !== null}
              onChange={(e) => { const file = e.target.files?.[0]; e.target.value = ""; if (file) void uploadPhoto(side, file); }} />
          </label>
          <div className={styles.fields}>
            <label className={styles.field}><span>Nama lengkap (dengan gelar)</span>
              <input value={couple[`${side}_name`] ?? ""} onChange={(e) => set(`${side}_name`, e.target.value)} required placeholder={side === "bride" ? "Rina Maharani, S.Ds." : "Bima Saputra, S.T."} />
            </label>
            <label className={styles.field}><span>Nama panggilan</span>
              <input value={couple[`${side}_nickname`] ?? ""} onChange={(e) => set(`${side}_nickname`, e.target.value)} placeholder={side === "bride" ? "Rina" : "Bima"} maxLength={40} />
            </label>
          </div>
        </div>
        <label className={styles.field}><span>Nama orang tua</span>
          <input value={couple[`${side}_parents`] ?? ""} onChange={(e) => set(`${side}_parents`, e.target.value)} placeholder={parentsHint} />
        </label>
        {photo && <button type="button" className={styles.link} onClick={() => set(side === "bride" ? "bride_photo" : "groom_photo", "")}>Hapus foto</button>}
      </section>
    );
  }

  return (
    <DashboardShell active="couple" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>Mempelai</h1>
          <p className="dashboard-subtitle">Nama, orang tua, dan foto yang tampil di seluruh undangan. Nama panggilan dipakai di judul dan sampul.</p>
        </div>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {loading ? <p className="dashboard-state">Memuat...</p> : (
        <form className={styles.form} onSubmit={handleSubmit}>
          <div className={styles.twoCol}>
            {person("bride", "Mempelai wanita", "Putri dari Bpk. Ahmad & Ibu Siti")}
            {person("groom", "Mempelai pria", "Putra dari Bpk. Hadi & Ibu Ratna")}
          </div>
          <section className={styles.panel} aria-label="Kata pengantar">
            <h2>Kata pengantar</h2>
            <label className={styles.field}><span>Pakai kalimat siap pakai (termasuk bahasa daerah)</span>
              <select value="" onChange={(e) => { const greeting = GREETINGS.find((g) => g.id === e.target.value); if (greeting && (!note.trim() || window.confirm("Ganti kata pengantar yang sudah ada?"))) { setNote(greeting.text); setNotice(""); } }}>
                <option value="">Pilih bahasa…</option>
                {GREETINGS.map((g) => <option key={g.id} value={g.id}>{g.label}</option>)}
              </select>
            </label>
            <label className={styles.field}><span>Kutipan singkat di bawah nama kalian (opsional)</span>
              <textarea rows={3} maxLength={240} value={note} onChange={(e) => { setNote(e.target.value); setNotice(""); }} placeholder="Dua cerita yang akhirnya menemukan rumah yang sama." />
            </label>
          </section>
          <div className={styles.actions}>
            <button type="submit" className="dashboard-action" disabled={saving || uploading !== null}>{saving ? "Menyimpan..." : "Simpan perubahan"}</button>
            {notice && <span role="status" className={styles.ok}>{notice}</span>}
          </div>
        </form>
      )}
    </DashboardShell>
  );
}
