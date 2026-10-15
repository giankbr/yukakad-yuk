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
  event: { title: string; venue: string; date: string; maps_url?: string };
};

export default function EventsPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [invitation, setInvitation] = useState<Invitation | null>(null);
  const [eventTitle, setEventTitle] = useState("");
  const [venue, setVenue] = useState("");
  const [date, setDate] = useState("");
  const [mapsUrl, setMapsUrl] = useState("");
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
        setEventTitle(body.event?.title ?? "");
        setVenue(body.event?.venue ?? "");
        setDate(body.event?.date ?? "");
        setMapsUrl(body.event?.maps_url ?? "");
      })
      .catch(() => setError("Gagal memuat detail acara"))
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
          event: { title: eventTitle, venue, date, maps_url: mapsUrl },
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
    <DashboardShell active="events" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>Acara</h1>
          <p className="dashboard-subtitle">Kapan dan di mana tamu perlu hadir.</p>
        </div>
      </header>

      {loading && <p className="dashboard-state">Memuat...</p>}
      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      {!loading && (
        <form className="dashboard-form" onSubmit={handleSubmit}>
          <FormField label="Nama acara" value={eventTitle} onChange={(e) => setEventTitle(e.target.value)} placeholder="Akad Nikah" required />
          <div className="form-row">
            <FormField label="Tempat" value={venue} onChange={(e) => setVenue(e.target.value)} placeholder="Gedung Serbaguna" required />
            <FormField label="Tanggal" type="date" value={date} onChange={(e) => setDate(e.target.value)} />
          </div>
          <FormField label="Link Google Maps" value={mapsUrl} onChange={(e) => setMapsUrl(e.target.value)} placeholder="https://maps.google.com/..." />
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
