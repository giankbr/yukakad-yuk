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
      .catch(() => setError("Could not load this invitation"));
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
      setError("Could not update publish status");
    } finally {
      setPublishing(false);
    }
  }

  if (!ready || !invitationId) return null;

  return (
    <DashboardShell active="summary" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Invitation</p>
          <h1>{invitation?.title ?? "Loading..."}</h1>
          <p className="dashboard-subtitle">yukakad.com/invitation/{invitation?.slug}</p>
        </div>
        {invitation && (
          <button className="dashboard-action" onClick={togglePublish} disabled={publishing}>
            {invitation.published ? "Unpublish" : "Publish"}
          </button>
        )}
      </header>

      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      <section className="dashboard-summary">
        <div className="dashboard-stat">
          <span>Status</span>
          <strong>{invitation?.published ? "Live" : "Draft"}</strong>
          <small>{invitation?.published ? "Visible to guests" : "Not published yet"}</small>
        </div>
        <div className="dashboard-stat">
          <span>Guests</span>
          <strong>{guestCount ?? "—"}</strong>
          <small>Invited so far</small>
        </div>
        <div className="dashboard-stat">
          <span>Attending</span>
          <strong>{rsvp?.attendees ?? "—"}</strong>
          <small>{rsvp ? `${rsvp.yes} yes · ${rsvp.no} no · ${rsvp.maybe} maybe` : "No RSVPs yet"}</small>
        </div>
        <div className="dashboard-stat">
          <span>Wishes</span>
          <strong>{wishCount ?? "—"}</strong>
          <small>Total messages received</small>
        </div>
      </section>

      <section className="dashboard-note">
        <div>
          <p className="dashboard-kicker">Next step</p>
          <h2>Fill in couple, event, and gallery details.</h2>
        </div>
        <p>Preview the public page any time to see how guests will experience it.</p>
        {invitation && (
          <a className="secondary-action" href={`/dashboard/invitations/${invitation.id}/preview`}>
            Preview →
          </a>
        )}
      </section>
    </DashboardShell>
  );
}
