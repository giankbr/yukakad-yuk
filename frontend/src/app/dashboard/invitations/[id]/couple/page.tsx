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
      .catch(() => setError("Gagal memuat data mempelai"))
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
      setError("Gagal menyimpan perubahan");
    } finally {
      setSaving(false);
    }
  }

  if (!ready || !invitationId) return null;

  return (
    <DashboardShell active="couple" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>Mempelai</h1>
          <p className="dashboard-subtitle">Nama yang tampil di seluruh undangan.</p>
        </div>
      </header>

      {loading && <p className="dashboard-state">Memuat...</p>}
      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      {!loading && (
        <form className="dashboard-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <FormField label="Nama mempelai pria" value={groomName} onChange={(e) => setGroomName(e.target.value)} required />
            <FormField label="Nama mempelai wanita" value={brideName} onChange={(e) => setBrideName(e.target.value)} required />
          </div>
          <div className="form-actions">
            <Button type="submit" disabled={saving}>
              {saving ? "Menyimpan..." : "Simpan perubahan"}
            </Button>
            {saved && <span className="form-hint">Tersimpan.</span>}
          </div>
        </form>
      )}
    </DashboardShell>
  );
}
