"use client";

import { useCallback, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { friendlyError } from "@/lib/errors";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type Invitation = { id: string; slug: string; title: string; published: boolean };
/** Short-lived, read-only token for this one invitation (never the session token: it ends up in a URL). */
type PreviewToken = { token: string; expiresAt: number };

// Renew this long before the server-side expiry (tokens live 6 hours).
const REFRESH_MARGIN_MS = 10 * 60 * 1000;

export default function PreviewPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [invitation, setInvitation] = useState<Invitation | null>(null);
  const [viewport, setViewport] = useState<"desktop" | "mobile">("mobile");
  const [preview, setPreview] = useState<PreviewToken | null>(null);
  const [previewError, setPreviewError] = useState("");

  const invitationId = routeParams?.id;

  useEffect(() => {
    if (!ready || !token || !invitationId) return;
    apiFetch(`/api/invitations/${invitationId}`, token)
      .then((response) => (response.ok ? response.json() : null))
      .then((body: Invitation | null) => { if (body?.slug) setInvitation(body); })
      .catch(() => {});
  }, [ready, token, invitationId]);

  const loadPreviewToken = useCallback(async () => {
    if (!token || !invitationId) return;
    try {
      const response = await apiFetch(`/api/invitations/${invitationId}/preview-token`, token, { method: "POST" });
      const body = (await response.json().catch(() => ({}))) as { token?: string; expires_at?: string; error?: string };
      if (!response.ok || !body.token) throw new Error(friendlyError(body.error, "Pratinjau draf belum bisa dimuat."));
      const parsed = body.expires_at ? Date.parse(body.expires_at) : NaN;
      setPreview({ token: body.token, expiresAt: Number.isFinite(parsed) ? parsed : Date.now() + 60 * 60 * 1000 });
      setPreviewError("");
    } catch (err) {
      setPreviewError(err instanceof Error && err.message ? err.message : "Pratinjau draf belum bisa dimuat.");
    }
  }, [token, invitationId]);

  const needsPreviewToken = Boolean(invitation && !invitation.published);

  // Drafts need a preview token; fetch one as soon as we know the invitation is unpublished.
  useEffect(() => {
    if (!needsPreviewToken) return;
    const timer = setTimeout(loadPreviewToken, 0);
    return () => clearTimeout(timer);
  }, [needsPreviewToken, loadPreviewToken]);

  // Renew shortly before expiry, and when the tab comes back after a long sleep.
  useEffect(() => {
    if (!needsPreviewToken || !preview) return;
    const timer = setTimeout(loadPreviewToken, Math.max(preview.expiresAt - Date.now() - REFRESH_MARGIN_MS, 30_000));
    const onVisible = () => {
      if (document.visibilityState === "visible" && preview.expiresAt - Date.now() < REFRESH_MARGIN_MS) loadPreviewToken();
    };
    document.addEventListener("visibilitychange", onVisible);
    return () => {
      clearTimeout(timer);
      document.removeEventListener("visibilitychange", onVisible);
    };
  }, [needsPreviewToken, preview, loadPreviewToken]);

  if (!ready || !invitationId) return null;

  const base = invitation ? `/invitation/${encodeURIComponent(invitation.slug)}` : null;
  const previewUrl = !base
    ? null
    : invitation?.published
      ? base
      : preview
        ? `${base}?preview=${encodeURIComponent(preview.token)}`
        : null;

  return (
    <DashboardShell active="preview" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>Pratinjau</h1>
          <p className="dashboard-subtitle">
            {invitation?.published ? "Ini halaman publik yang sudah terbit." : "Pratinjau draf — belum bisa dilihat tamu."}
          </p>
        </div>
        <div className="form-actions">
          <button type="button" className="table-action" onClick={() => setViewport("mobile")} aria-pressed={viewport === "mobile"} style={{ fontWeight: viewport === "mobile" ? 700 : 500 }}>Ponsel</button>
          <button type="button" className="table-action" onClick={() => setViewport("desktop")} aria-pressed={viewport === "desktop"} style={{ fontWeight: viewport === "desktop" ? 700 : 500 }}>Desktop</button>
          {previewUrl && (
            <a className="secondary-action" href={previewUrl} target="_blank" rel="noreferrer">
              Buka di tab baru ↗
            </a>
          )}
        </div>
      </header>

      {previewError && (
        <div className="dashboard-state dashboard-state-error" role="alert" style={{ display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}>
          <span>{previewError}</span>
          <button type="button" className="table-action" onClick={loadPreviewToken}>Coba lagi</button>
        </div>
      )}
      {invitation && !previewUrl && !previewError && <p className="dashboard-state">Menyiapkan pratinjau...</p>}

      {previewUrl && (
        <div style={{ paddingTop: "2rem", display: "flex", justifyContent: "center" }}>
          <iframe
            src={previewUrl}
            title="Pratinjau undangan"
            referrerPolicy="no-referrer"
            style={{
              width: viewport === "mobile" ? "390px" : "100%",
              maxWidth: "100%",
              height: "80vh",
              border: "1px solid var(--rw-border-warm)",
              borderRadius: ".5rem",
              background: "#fff",
            }}
          />
        </div>
      )}
    </DashboardShell>
  );
}
