"use client";

import { useCallback, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type Invitation = {
  id: string;
  slug: string;
  title: string;
  published: boolean;
  access?: { role: string };
};

type RSVPSummary = { yes: number; no: number; maybe: number; attendees: number };

export default function InvitationSummaryPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [invitation, setInvitation] = useState<Invitation | null>(null);
  const [rsvp, setRsvp] = useState<RSVPSummary | null>(null);
  const [guestCount, setGuestCount] = useState<number | null>(null);
  const [wishCount, setWishCount] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [publishing, setPublishing] = useState(false);

  const invitationId = routeParams?.id;

  const load = useCallback(() => {
    if (!token || !invitationId) return;
    Promise.all([
      apiFetch(`/api/invitations/${invitationId}`, token).then((r) => r.json()),
      apiFetch(`/api/invitations/${invitationId}/rsvps/summary`, token).then((r) => r.json()),
      apiFetch(`/api/invitations/${invitationId}/guests`, token).then((r) => r.json()),
      apiFetch(`/api/invitations/${invitationId}/wishes`, token).then((r) => r.json()),
    ])
      .then(([invitationBody, rsvpBody, guestsBody, wishesBody]) => {
        setInvitation(invitationBody);
        setRsvp(rsvpBody);
        setGuestCount((guestsBody.items ?? []).length);
        setWishCount((wishesBody.items ?? []).length);
      })
      .catch(() => setError("Gagal memuat undangan ini"));
  }, [token, invitationId]);

  useEffect(() => {
    if (!ready) return;
    load();
  }, [ready, load]);

  async function togglePublish() {
    if (!token || !invitation) return;
    setPublishing(true);
    try {
      const response = await apiFetch(`/api/invitations/${invitation.id}`, token, {
        method: "PUT",
        body: JSON.stringify({ slug: invitation.slug, title: invitation.title, published: !invitation.published }),
      });
      if (!response.ok) throw new Error();
      const body = await response.json();
      setInvitation(body);
    } catch {
      setError("Gagal mengubah status terbit");
    } finally {
      setPublishing(false);
    }
  }

  if (!ready || !invitationId) return null;

  return (
    <DashboardShell active="summary" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>{invitation?.title ?? "Memuat..."}</h1>
          <p className="dashboard-subtitle">rawuh.id/invitation/{invitation?.slug}</p>
        </div>
        {invitation && (!invitation.access || invitation.access.role === "owner") && (
          <button className="dashboard-action" onClick={togglePublish} disabled={publishing}>
            {invitation.published ? "Batalkan terbit" : "Terbitkan"}
          </button>
        )}
      </header>

      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      <section className="dashboard-summary">
        <div className="dashboard-stat">
          <span>Status</span>
          <strong>{invitation?.published ? "Terbit" : "Draf"}</strong>
          <small>{invitation?.published ? "Sudah bisa dilihat tamu" : "Belum diterbitkan"}</small>
        </div>
        <div className="dashboard-stat">
          <span>Tamu</span>
          <strong>{guestCount ?? "—"}</strong>
          <small>Sudah diundang</small>
        </div>
        <div className="dashboard-stat">
          <span>Total hadir</span>
          <strong>{rsvp?.attendees ?? "—"}</strong>
          <small>{rsvp ? `${rsvp.yes} hadir · ${rsvp.no} tidak · ${rsvp.maybe} mungkin` : "Belum ada RSVP"}</small>
        </div>
        <div className="dashboard-stat">
          <span>Ucapan</span>
          <strong>{wishCount ?? "—"}</strong>
          <small>Total ucapan diterima</small>
        </div>
      </section>

      <section className="dashboard-note">
        <div>
          <p className="dashboard-kicker">Langkah berikutnya</p>
          <h2>Lengkapi data mempelai, acara, dan galeri.</h2>
        </div>
        <p>Lihat pratinjau halaman publik kapan saja untuk melihat tampilannya di mata tamu.</p>
        {invitation && (
          <a className="secondary-action" href={`/dashboard/invitations/${invitation.id}/preview`}>
            Pratinjau →
          </a>
        )}
      </section>
    </DashboardShell>
  );
}
