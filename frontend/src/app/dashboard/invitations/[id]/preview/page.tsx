"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type Invitation = { id: string; slug: string; title: string; published: boolean };

export default function PreviewPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [invitation, setInvitation] = useState<Invitation | null>(null);
  const [viewport, setViewport] = useState<"desktop" | "mobile">("mobile");

  const invitationId = routeParams?.id;

  useEffect(() => {
    if (!ready || !token || !invitationId) return;
    apiFetch(`/api/invitations/${invitationId}`, token)
      .then((response) => response.json())
      .then(setInvitation)
      .catch(() => {});
  }, [ready, token, invitationId]);

  if (!ready || !invitationId) return null;

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
          <button className="table-action" onClick={() => setViewport("mobile")} style={{ fontWeight: viewport === "mobile" ? 700 : 500 }}>Ponsel</button>
          <button className="table-action" onClick={() => setViewport("desktop")} style={{ fontWeight: viewport === "desktop" ? 700 : 500 }}>Desktop</button>
          {invitation && (
            <a
              className="secondary-action"
              href={`/invitation/${invitation.slug}${invitation.published ? "" : `?preview_token=${token}`}`}
              target="_blank"
              rel="noreferrer"
            >
              Buka di tab baru ↗
            </a>
          )}
        </div>
      </header>

      {invitation && (
        <div style={{ paddingTop: "2rem", display: "flex", justifyContent: "center" }}>
          <iframe
            src={`/invitation/${invitation.slug}${invitation.published ? "" : `?preview_token=${token}`}`}
            title="Pratinjau undangan"
            style={{
              width: viewport === "mobile" ? "390px" : "100%",
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
