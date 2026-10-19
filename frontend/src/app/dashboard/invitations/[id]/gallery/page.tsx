"use client";

import { useCallback, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";
import { friendly, GateNotice, getJson, lostAccess, usePageGate } from "../_lib";

type GalleryItem = { id: string; image_url: string; caption?: string };

export default function GalleryPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [items, setItems] = useState<GalleryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const invitationId = routeParams?.id;

  const gate = usePageGate(invitationId, token, "gallery");
  const { lose } = gate;
  const allowed = gate.status === "ok";

  const load = useCallback(() => {
    if (!token || !invitationId) return;
    getJson<{ items?: GalleryItem[] }>(`/api/invitations/${invitationId}/gallery`, token)
      .then((result) => {
        if (lostAccess(result.status)) { lose(); return; }
        if (!result.ok) { setError(result.error || "Gagal memuat galeri."); return; }
        setItems(result.data?.items ?? []);
      })
      .finally(() => setLoading(false));
  }, [token, invitationId, lose]);

  useEffect(() => {
    if (!ready || !allowed) return;
    load();
  }, [ready, allowed, load]);

  async function handleUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file || !token || !invitationId) return;
    setUploading(true);
    setError("");
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("type", "gallery");
      const uploadResponse = await apiFetch(`/api/invitations/${invitationId}/media`, token, {
        method: "POST",
        body: formData,
      });
      const uploaded = await uploadResponse.json().catch(() => ({}));
      if (!uploadResponse.ok) throw new Error(uploaded.error ?? "Gagal mengunggah");

      const galleryResponse = await apiFetch(`/api/invitations/${invitationId}/gallery`, token, {
        method: "POST",
        body: JSON.stringify({ image_url: uploaded.path }),
      });
      if (!galleryResponse.ok) throw new Error("Gagal menambahkan foto ke galeri.");
      load();
    } catch (err) {
      setError(friendly(err, "Gagal mengunggah."));
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  }

  if (!ready || !invitationId) return null;

  if (!allowed) {
    return (
      <DashboardShell active="gallery" invitationId={invitationId}>
        <GateNotice gate={gate} invitationId={invitationId} />
      </DashboardShell>
    );
  }

  return (
    <DashboardShell active="gallery" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>Galeri</h1>
          <p className="dashboard-subtitle">{items.length} foto terunggah</p>
        </div>
      </header>

      <label className="upload-drop">
        <span>{uploading ? "Mengunggah..." : "Klik untuk mengunggah foto (JPEG, PNG, atau WebP, maks. 10 MB)"}</span>
        <input type="file" accept="image/jpeg,image/png,image/webp" onChange={handleUpload} disabled={uploading} hidden />
      </label>

      {loading && <p className="dashboard-state">Memuat galeri...</p>}
      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}
      {!loading && !error && items.length === 0 && <p className="dashboard-state">Belum ada foto.</p>}
      {!loading && items.length > 0 && (
        <div className="card-grid">
          {items.map((item) => (
            <div className="dashboard-card" key={item.id}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={item.image_url} alt={item.caption ?? "Foto galeri"} />
            </div>
          ))}
        </div>
      )}
    </DashboardShell>
  );
}
