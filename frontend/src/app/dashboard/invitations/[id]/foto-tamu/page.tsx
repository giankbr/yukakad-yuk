"use client";

import { useCallback, useEffect, useState } from "react";
import QRCode from "qrcode";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { getSectionsConfig, patchSectionsConfig } from "@/lib/sections-config";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type Photo = { id: string; url: string; uploader_name?: string; status: "approved" | "pending" | "hidden"; created_at: string };
type Filter = "" | "pending" | "approved" | "hidden";
const STATUS: Record<string, string> = { approved: "Tampil", pending: "Menunggu", hidden: "Disembunyikan" };

export default function GuestPhotosPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const invitationId = routeParams?.id;
  const [photos, setPhotos] = useState<Photo[]>([]);
  const [config, setConfig] = useState<{ enabled?: boolean; moderate?: boolean }>({});
  const [storageReady, setStorageReady] = useState(true);
  const [slug, setSlug] = useState("");
  const [qr, setQr] = useState("");
  const [filter, setFilter] = useState<Filter>("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<string | null>(null);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    if (!token || !invitationId) return;
    const [list, sections, invitation] = await Promise.all([
      apiFetch(`/api/invitations/${invitationId}/guest-photos`, token).then((r) => r.json()),
      getSectionsConfig(invitationId, token),
      apiFetch(`/api/invitations/${invitationId}`, token).then((r) => r.json()),
    ]);
    setPhotos(list.items ?? []);
    setStorageReady(list.storage_ready !== false);
    setConfig(sections.guestPhotos ?? {});
    setSlug(invitation.slug ?? "");
  }, [token, invitationId]);

  useEffect(() => {
    if (!ready || !token || !invitationId) return;
    const timer = setTimeout(() => { load().catch(() => setError("Gagal memuat foto")).finally(() => setLoading(false)); }, 0);
    return () => clearTimeout(timer);
  }, [ready, token, invitationId, load]);

  const link = slug && typeof window !== "undefined" ? `${window.location.origin}/invitation/${slug}#extra-foto-tamu` : "";
  useEffect(() => {
    if (!link) return;
    QRCode.toDataURL(link, { width: 480, margin: 1 }).then(setQr).catch(() => undefined);
  }, [link]);

  async function saveConfig(next: { enabled?: boolean; moderate?: boolean }) {
    if (!token || !invitationId) return;
    setBusy("config");
    setError("");
    setNotice("");
    try {
      await patchSectionsConfig(invitationId, token, "guestPhotos", next);
      setConfig(next);
      setNotice(next.enabled ? "Tamu sekarang bisa mengirim foto dari undangan." : "Upload foto tamu dimatikan.");
    } catch {
      setError("Belum tersimpan.");
    } finally {
      setBusy(null);
    }
  }

  async function setStatus(photo: Photo, status: Photo["status"]) {
    if (!token || !invitationId) return;
    setBusy(photo.id);
    const response = await apiFetch(`/api/invitations/${invitationId}/guest-photos/${photo.id}`, token, { method: "PATCH", body: JSON.stringify({ status }) });
    if (response.ok) setPhotos((current) => current.map((p) => (p.id === photo.id ? { ...p, status } : p)));
    setBusy(null);
  }

  function printCard() {
    const win = window.open("", "_blank", "width=600,height=800");
    if (!win || !qr) return;
    win.document.write(`<!doctype html><title>QR foto tamu</title><style>body{margin:0;font-family:system-ui,sans-serif}.card{width:10cm;margin:1cm auto;padding:1cm;border:1px dashed #999;text-align:center}img{width:6cm;height:6cm}h1{margin:.2cm 0;font-size:20pt}p{margin:.2cm 0;color:#444;font-size:11pt}</style><div class="card"><p>Bagikan momen hari ini</p><h1>Kirim fotomu 📸</h1><img src="${qr}"><p>Scan, lalu ketuk <b>Kirim foto</b>.<br>Fotomu tampil di layar &amp; undangan.</p></div><script>onload=()=>print()</script>`);
    win.document.close();
  }

  if (!ready || !invitationId) return null;
  const visible = photos.filter((p) => !filter || p.status === filter);
  const pending = photos.filter((p) => p.status === "pending").length;

  return (
    <DashboardShell active="photos" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Hari-H</p>
          <h1>Foto dari tamu</h1>
          <p className="dashboard-subtitle">Tamu scan QR di meja, lalu kirim foto dari HP tanpa install aplikasi. Foto tampil di undangan dan jadi latar Layar sapa.</p>
        </div>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {notice && <p role="status" className={styles.ok} style={{ margin: "0 0 12px" }}>{notice}</p>}

      {loading ? <p className="dashboard-state">Memuat…</p> : (
        <div className={styles.form} style={{ maxWidth: "none" }}>
          <div className={styles.twoCol}>
            <section className={styles.panel} aria-label="Pengaturan" style={{ alignContent: "start" }}>
              <h2>Pengaturan</h2>
              <label className={styles.check}><input type="checkbox" checked={Boolean(config.enabled)} disabled={busy === "config"} onChange={(e) => saveConfig({ ...config, enabled: e.target.checked })} /> Tamu boleh mengirim foto</label>
              <label className={styles.check}><input type="checkbox" checked={Boolean(config.moderate)} disabled={busy === "config" || !config.enabled} onChange={(e) => saveConfig({ ...config, moderate: e.target.checked })} /> Setujui dulu sebelum tampil</label>
              {!storageReady && <p className={styles.hint} style={{ color: "#b42318" }}>Penyimpanan foto di server belum dikonfigurasi, jadi tamu belum bisa mengunggah. Hubungi admin Rawuh.</p>}
            </section>
            <section className={styles.panel} aria-label="QR meja">
              <div className={styles.panelHead}><div><h2>QR untuk meja</h2><p>Cetak dan taruh di setiap meja atau dekat photo booth.</p></div></div>
              <div style={{ display: "flex", alignItems: "center", gap: 16, flexWrap: "wrap" }}>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                {qr && <img src={qr} alt="QR menuju formulir foto tamu" width={120} height={120} style={{ borderRadius: 8, border: "1px solid var(--rw-border-warm)" }} />}
                <div style={{ display: "grid", gap: 8 }}>
                  <button type="button" className="dashboard-action" onClick={printCard} disabled={!qr}>Cetak kartu QR</button>
                  {link && <a className={styles.link} href={link} target="_blank" rel="noreferrer">Coba dari undangan ↗</a>}
                </div>
              </div>
            </section>
          </div>

          <section className={styles.panel} aria-label="Foto masuk">
            <div className={styles.panelHead}>
              <div><h2>Foto masuk</h2><p>{photos.length} foto{pending ? ` · ${pending} menunggu persetujuan` : ""}</p></div>
              <div className={styles.tabs} role="group" aria-label="Filter">
                {([["", "Semua"], ["pending", "Menunggu"], ["approved", "Tampil"], ["hidden", "Disembunyikan"]] as [Filter, string][]).map(([key, label]) => (
                  <button key={key || "all"} type="button" aria-pressed={filter === key} onClick={() => setFilter(key)}>{label}</button>
                ))}
              </div>
            </div>
            {visible.length === 0 ? <p className={styles.empty}>{config.enabled ? "Belum ada foto." : "Aktifkan upload foto tamu untuk mulai menerima foto."}</p> : (
              <ul style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))", gap: 12, margin: 0, padding: 0, listStyle: "none" }}>
                {visible.map((photo) => (
                  <li key={photo.id} className={styles.item} style={{ display: "grid", gap: 8, padding: 8, opacity: photo.status === "hidden" ? 0.55 : 1 }}>
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <a href={photo.url} target="_blank" rel="noreferrer"><img src={photo.url} alt={`Foto dari ${photo.uploader_name || "tamu"}`} style={{ width: "100%", aspectRatio: "1", objectFit: "cover", borderRadius: 8 }} /></a>
                    <small className={styles.hint}>{photo.uploader_name || "Tamu"} · {STATUS[photo.status]}</small>
                    <div style={{ display: "flex", gap: 6 }}>
                      {photo.status !== "approved" && <button type="button" className="table-action" disabled={busy === photo.id} onClick={() => setStatus(photo, "approved")}>Tampilkan</button>}
                      {photo.status !== "hidden" && <button type="button" className="table-action table-action-danger" disabled={busy === photo.id} onClick={() => setStatus(photo, "hidden")}>Sembunyikan</button>}
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </div>
      )}
    </DashboardShell>
  );
}
