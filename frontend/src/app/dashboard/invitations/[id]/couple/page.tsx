"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { FormField } from "@/components/dashboard/FormField";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type Invitation = {
  id: string;
  slug: string;
  title: string;
  published: boolean;
  couple: { groom_name: string; bride_name: string };
};

export default function CouplePage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [invitation, setInvitation] = useState<Invitation | null>(null);
  const [groomName, setGroomName] = useState("");
  const [brideName, setBrideName] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");

  const invitationId = routeParams?.id;

  useEffect(() => {
    if (!ready || !token || !invitationId) return;
    apiFetch(`/api/invitations/${invitationId}`, token)
      .then((response) => response.json())
      .then((body: Invitation) => {
        setInvitation(body);
        setGroomName(body.couple?.groom_name ?? "");
        setBrideName(body.couple?.bride_name ?? "");
      })
      .catch(() => setError("Could not load couple details"))
      .finally(() => setLoading(false));
  }, [ready, token, invitationId]);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!token || !invitation) return;
    setSaving(true);
    setSaved(false);
    setError("");
    try {
      const response = await apiFetch(`/api/invitations/${invitation.id}`, token, {
        method: "PUT",
        body: JSON.stringify({
          slug: invitation.slug,
          title: invitation.title,
          published: invitation.published,
          couple: { groom_name: groomName, bride_name: brideName },
        }),
      });
      if (!response.ok) throw new Error();
      setSaved(true);
    } catch {
      setError("Could not save changes");
    } finally {
      setSaving(false);
    }
  }

  if (!ready || !invitationId) return null;

  return (
    <DashboardShell active="couple" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Invitation</p>
          <h1>Couple</h1>
          <p className="dashboard-subtitle">Names shown across the invitation.</p>
        </div>
      </header>

      {loading && <p className="dashboard-state">Loading...</p>}
      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      {!loading && (
        <form className="dashboard-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <FormField label="Groom's name" value={groomName} onChange={(e) => setGroomName(e.target.value)} required />
            <FormField label="Bride's name" value={brideName} onChange={(e) => setBrideName(e.target.value)} required />
          </div>
          <div className="form-actions">
            <Button type="submit" disabled={saving} className="bg-[#173c3a] text-white">
              {saving ? "Saving..." : "Save changes"}
            </Button>
            {saved && <span className="form-hint">Saved.</span>}
          </div>
        </form>
      )}
    </DashboardShell>
  );
}
