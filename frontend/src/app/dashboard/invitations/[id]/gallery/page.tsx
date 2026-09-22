"use client";

import { useCallback, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type GalleryItem = { id: string; image_url: string; caption?: string };

export default function GalleryPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [items, setItems] = useState<GalleryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const invitationId = routeParams?.id;

  const load = useCallback(() => {
    if (!token || !invitationId) return;
    apiFetch(`/api/invitations/${invitationId}/gallery`, token)
      .then((response) => response.json())
      .then((body: { items?: GalleryItem[] }) => setItems(body.items ?? []))
      .catch(() => setError("Could not load gallery"))
      .finally(() => setLoading(false));
  }, [token, invitationId]);

  useEffect(() => {
    if (!ready) return;
    load();
  }, [ready, load]);

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
      const uploaded = await uploadResponse.json();
      if (!uploadResponse.ok) throw new Error(uploaded.error ?? "Upload failed");

      const galleryResponse = await apiFetch(`/api/invitations/${invitationId}/gallery`, token, {
        method: "POST",
        body: JSON.stringify({ image_url: uploaded.path }),
      });
      if (!galleryResponse.ok) throw new Error("Could not add photo to gallery");
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  }

  if (!ready || !invitationId) return null;

  return (
    <DashboardShell active="gallery" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Invitation</p>
          <h1>Gallery</h1>
          <p className="dashboard-subtitle">{items.length} photos uploaded</p>
        </div>
      </header>

      <label className="upload-drop">
        <span>{uploading ? "Uploading..." : "Click to upload a photo (JPEG, PNG, or WebP, max 10MB)"}</span>
        <input type="file" accept="image/jpeg,image/png,image/webp" onChange={handleUpload} disabled={uploading} hidden />
      </label>

      {loading && <p className="dashboard-state">Loading gallery...</p>}
      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}
      {!loading && !error && items.length === 0 && <p className="dashboard-state">No photos yet.</p>}
      {!loading && items.length > 0 && (
        <div className="card-grid">
          {items.map((item) => (
            <div className="dashboard-card" key={item.id}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={item.image_url} alt={item.caption ?? "Gallery photo"} />
            </div>
          ))}
        </div>
      )}
    </DashboardShell>
  );
}
