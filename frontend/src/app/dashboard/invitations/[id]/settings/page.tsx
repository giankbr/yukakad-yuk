"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { TemplatePicker } from "@/components/dashboard/TemplatePicker";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";
import styles from "./settings.module.css";

type Settings = {
  theme?: string;
  primary_color?: string;
  secondary_color?: string;
  font?: string;
  music_url?: string;
  autoplay_music?: boolean;
};

const MAX_MUSIC_BYTES = 10 << 20;

function trackName(url: string) {
  try {
    const name = decodeURIComponent(new URL(url).pathname.split("/").pop() ?? "");
    return name.replace(/^[0-9a-f]{8,}(?:-[0-9a-f]{4,})*[-_]/i, "") || "Musik latar";
  } catch {
    return "Musik latar";
  }
}

export default function SettingsPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [templateId, setTemplateId] = useState("");
  const [settings, setSettings] = useState<Settings>({});
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<"" | "upload" | "save">("");
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const fileInput = useRef<HTMLInputElement>(null);

  const invitationId = routeParams?.id;

  useEffect(() => {
    if (!ready || !token || !invitationId) return;
    Promise.all([
      apiFetch(`/api/invitations/${invitationId}`, token).then((r) => r.json()),
      apiFetch(`/api/invitations/${invitationId}/settings`, token).then((r) => r.json()),
    ])
      .then(([invitationBody, settingsBody]) => {
        setTemplateId(invitationBody.template_id ?? "");
        setSettings(settingsBody ?? {});
      })
      .catch(() => setError("Pengaturan gagal dimuat. Coba muat ulang halaman."))
      .finally(() => setLoading(false));
  }, [ready, token, invitationId]);

  async function saveSettings(patch: Partial<Settings>, message: string) {
    if (!token || !invitationId) return false;
    const next = { ...settings, ...patch };
    setBusy("save");
    setError("");
    setNotice("");
    try {
      const response = await apiFetch(`/api/invitations/${invitationId}/settings`, token, {
        method: "PATCH",
        body: JSON.stringify(next),
      });
      if (!response.ok) throw new Error();
      setSettings(next);
      setNotice(message);
      return true;
    } catch {
      setError("Pengaturan belum tersimpan. Periksa koneksi lalu coba lagi.");
      return false;
    } finally {
      setBusy("");
    }
  }

  async function handleUploadMusic(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file || !token || !invitationId) return;
    if (file.type !== "audio/mpeg") return setError("Format musik harus MP3.");
    if (file.size > MAX_MUSIC_BYTES) return setError("Ukuran musik maksimal 10 MB.");
    setBusy("upload");
    setError("");
    setNotice("");
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("type", "music");
      const response = await apiFetch(`/api/invitations/${invitationId}/media`, token, { method: "POST", body: formData });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error ?? "Upload gagal");
      setBusy("");
      await saveSettings({ music_url: body.path }, "Musik tersimpan dan akan diputar di undangan.");
    } catch (err) {
      setError(err instanceof Error && err.message ? `Upload musik gagal: ${err.message}` : "Upload musik gagal.");
      setBusy("");
    }
  }

  if (!ready || !invitationId || !token) return null;

  const music = settings.music_url;

  return (
    <DashboardShell active="settings" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>Tema & Musik</h1>
          <p className="dashboard-subtitle">Pilih tampilan undangan dan musik latar yang diputar saat tamu membukanya.</p>
        </div>
        <Link className="dashboard-action" href={`/dashboard/invitations/${invitationId}/preview`}>
          Pratinjau undangan
        </Link>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {notice && <p role="status" className={styles.notice}>{notice}</p>}

      {loading ? (
        <p className="dashboard-state">Memuat pengaturan...</p>
      ) : (
        <>
          <section className={styles.panel} aria-labelledby="music-heading">
            <div className={styles.panelHead}>
              <div>
                <h2 id="music-heading">Musik latar</h2>
                <p>MP3, maksimal 10 MB. Tamu bisa menjeda musik kapan saja lewat tombol di pojok layar.</p>
              </div>
            </div>

            {music ? (
              <div className={styles.track}>
                <span className={styles.trackIcon} aria-hidden="true">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 18V5l12-2v13" /><circle cx="6" cy="18" r="3" /><circle cx="18" cy="16" r="3" /></svg>
                </span>
                <div className={styles.trackMain}>
                  <strong title={trackName(music)}>{trackName(music)}</strong>
                  <audio controls preload="none" src={music} />
                </div>
                <div className={styles.trackActions}>
                  <button type="button" className={styles.ghost} disabled={busy !== ""} onClick={() => fileInput.current?.click()}>Ganti</button>
                  <button type="button" className={styles.danger} disabled={busy !== ""} onClick={() => saveSettings({ music_url: "", autoplay_music: false }, "Musik dihapus dari undangan.")}>Hapus</button>
                </div>
              </div>
            ) : (
              <button type="button" className={styles.drop} disabled={busy !== ""} onClick={() => fileInput.current?.click()}>
                <strong>{busy === "upload" ? "Mengunggah musik..." : "Unggah musik"}</strong>
                <span>Klik untuk memilih file MP3 dari perangkatmu</span>
              </button>
            )}
            {music && busy === "upload" && <p className={styles.hint}>Mengunggah musik baru...</p>}
            <input ref={fileInput} type="file" accept="audio/mpeg,.mp3" onChange={handleUploadMusic} hidden />

            <label className={styles.toggle} data-disabled={!music || undefined}>
              <input
                type="checkbox"
                role="switch"
                disabled={!music || busy !== ""}
                checked={Boolean(music && settings.autoplay_music)}
                onChange={(e) => saveSettings({ autoplay_music: e.target.checked }, e.target.checked ? "Musik akan langsung diputar saat undangan dibuka." : "Musik tidak diputar otomatis.")}
              />
              <span className={styles.switch} aria-hidden="true" />
              <span>
                <strong>Putar otomatis saat undangan dibuka</strong>
                <small>Musik mulai setelah tamu menekan tombol buka undangan.</small>
              </span>
            </label>
          </section>

          <section className={styles.panel} aria-labelledby="theme-heading">
            <div className={styles.panelHead}>
              <div>
                <h2 id="theme-heading">Tema undangan</h2>
                <p>Ganti tema kapan saja — semua data undangan tetap sama.</p>
              </div>
            </div>
            <TemplatePicker invitationId={invitationId} token={token} selectedTemplateId={templateId} onChange={setTemplateId} />
          </section>
        </>
      )}
    </DashboardShell>
  );
}
