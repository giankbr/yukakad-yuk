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
          <p className="dashboard-kicker">Invitation</p>
          <h1>Preview</h1>
          <p className="dashboard-subtitle">
            {invitation?.published ? "This is the live public page." : "Draft preview — not visible to guests yet."}
          </p>
        </div>
        <div className="form-actions">
          <button className="table-action" onClick={() => setViewport("mobile")} style={{ fontWeight: viewport === "mobile" ? 700 : 500 }}>Mobile</button>
          <button className="table-action" onClick={() => setViewport("desktop")} style={{ fontWeight: viewport === "desktop" ? 700 : 500 }}>Desktop</button>
          {invitation && (
            <a
              className="secondary-action"
              href={`/invitation/${invitation.slug}${invitation.published ? "" : `?preview_token=${token}`}`}
              target="_blank"
              rel="noreferrer"
            >
              Open in new tab ↗
            </a>
          )}
        </div>
      </header>

      {invitation && (
        <div style={{ paddingTop: "2rem", display: "flex", justifyContent: "center" }}>
          <iframe
            src={`/invitation/${invitation.slug}${invitation.published ? "" : `?preview_token=${token}`}`}
            title="Invitation preview"
            style={{
              width: viewport === "mobile" ? "390px" : "100%",
              height: "80vh",
              border: "1px solid #d9e1d8",
              borderRadius: ".5rem",
              background: "#fff",
            }}
          />
        </div>
      )}
    </DashboardShell>
  );
}
