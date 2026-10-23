"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { MusicNotes as PhMusicNotes } from "@phosphor-icons/react/ssr";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { MusicLibrary } from "@/components/dashboard/MusicLibrary";
import { TemplatePicker } from "@/components/dashboard/TemplatePicker";
import { themeMood } from "@/components/invitation/themes/mood";
import { libraryTrack } from "@/lib/music-library";
import { apiFetch } from "@/lib/api";
import { getSectionsConfig, patchSectionsConfig } from "@/lib/sections-config";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";
import styles from "./settings.module.css";
import { friendly, GateNotice, getJson, lostAccess, usePageGate } from "../_lib";

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
  const builtIn = libraryTrack(url);
  if (builtIn) return `${builtIn.title} · lagu bawaan Rawuh`;
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
  const [easyRead, setEasyRead] = useState(true);
  const fileInput = useRef<HTMLInputElement>(null);

  const invitationId = routeParams?.id;

  const gate = usePageGate(invitationId, token, "settings");
  const { lose } = gate;
  const allowed = gate.status === "ok";

  useEffect(() => {
    if (!ready || !token || !invitationId || !allowed) return;
    Promise.all([
      getJson<{ template_id?: string }>(`/api/invitations/${invitationId}`, token),
      getJson<Settings>(`/api/invitations/${invitationId}/settings`, token),
    ])
      .then(([invitationBody, settingsBody]) => {
        if (lostAccess(invitationBody.status) || lostAccess(settingsBody.status)) { lose(); return; }
        if (!invitationBody.ok || !settingsBody.ok) { setError("Pengaturan gagal dimuat. Coba muat ulang halaman."); return; }
        setTemplateId(invitationBody.data?.template_id ?? "");
        setSettings(settingsBody.data ?? {});
      })
      .finally(() => setLoading(false));
    getSectionsConfig(invitationId, token).then((config) => setEasyRead(config.easyRead?.enabled !== false)).catch(() => undefined);
  }, [ready, token, invitationId, allowed, lose]);

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
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(body.error ?? "Upload gagal");
      setBusy("");
      await saveSettings({ music_url: body.path }, "Musik tersimpan dan akan diputar di undangan.");
    } catch (err) {
      const message = friendly(err, "");
      setError(message ? `Upload musik gagal: ${message}` : "Upload musik gagal.");
      setBusy("");
    }
  }

  if (!ready || !invitationId || !token) return null;

  if (!allowed) {
    return (
      <DashboardShell active="settings" invitationId={invitationId}>
        <GateNotice gate={gate} invitationId={invitationId} />
      </DashboardShell>
    );
  }

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
                <p>Pilih lagu bawaan Rawuh atau unggah MP3 sendiri (maks. 10 MB). Tamu bisa menjeda musik kapan saja lewat tombol di pojok layar.</p>
              </div>
            </div>

            {music ? (
              <div className={styles.track}>
                <span className={styles.trackIcon} aria-hidden="true">
                  <PhMusicNotes size={20} weight="fill" />
                </span>
                <div className={styles.trackMain}>
                  <strong title={trackName(music)}>{trackName(music)}</strong>
                  <audio controls preload="none" src={music} />
                </div>
                <div className={styles.trackActions}>
                  <button type="button" className={styles.ghost} disabled={busy !== ""} onClick={() => fileInput.current?.click()}>Unggah lain</button>
                  <button type="button" className={styles.danger} disabled={busy !== ""} onClick={() => saveSettings({ music_url: "", autoplay_music: false }, "Musik dihapus dari undangan.")}>Hapus</button>
                </div>
              </div>
            ) : null}

            <div className={styles.subhead}>
              <h3>Lagu bawaan Rawuh</h3>
              <p>Bebas royalti, siap dipakai. Dengarkan dulu, lalu tekan Pakai.</p>
            </div>
            <MusicLibrary current={music} recommended={templateId ? themeMood(templateId).mood : undefined} disabled={busy !== ""}
              onPick={(track) => saveSettings(
                // First music for this invitation: start it when the cover opens, like an upload would be expected to.
                { music_url: track.file, autoplay_music: music ? settings.autoplay_music : true },
                `${track.title} dipakai sebagai musik undangan.`,
              )} />

            {!music && (
              <button type="button" className={styles.drop} disabled={busy !== ""} onClick={() => fileInput.current?.click()}>
                <strong>{busy === "upload" ? "Mengunggah musik..." : "Atau unggah MP3 sendiri"}</strong>
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

          <section className={styles.panel} aria-labelledby="easy-heading">
            <label className={styles.toggle}>
              <input
                type="checkbox"
                role="switch"
                checked={easyRead}
                onChange={async (e) => {
                  const enabled = e.target.checked;
                  setEasyRead(enabled);
                  try {
                    await patchSectionsConfig(invitationId, token!, "easyRead", { enabled });
                    setNotice(enabled ? "Tombol perbesar tulisan & dengarkan tampil di undangan." : "Tombol bantuan membaca disembunyikan.");
                  } catch { setEasyRead(!enabled); setError("Belum tersimpan."); }
                }}
              />
              <span className={styles.switch} aria-hidden="true" />
              <span>
                <strong id="easy-heading">Mode mudah dibaca untuk orang tua</strong>
                <small>Tombol “Besar” memperbesar tulisan, “Dengarkan” membacakan nama, tanggal, dan lokasi acara.</small>
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
