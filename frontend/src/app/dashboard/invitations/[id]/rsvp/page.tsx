"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type RSVP = {
  id: string;
  guest_id?: string;
  attendance: string;
  attendees_count: number;
  message?: string;
  submitted_at: string;
};

const attendanceLabels: Record<string, string> = { yes: "Hadir", no: "Tidak hadir", maybe: "Mungkin" };

type Summary = { yes: number; no: number; maybe: number; attendees: number };

export default function RSVPPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [rsvps, setRsvps] = useState<RSVP[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const invitationId = routeParams?.id;

  useEffect(() => {
    if (!ready || !token || !invitationId) return;
    Promise.all([
      apiFetch(`/api/invitations/${invitationId}/rsvps`, token).then((r) => r.json()),
      apiFetch(`/api/invitations/${invitationId}/rsvps/summary`, token).then((r) => r.json()),
    ])
      .then(([rsvpBody, summaryBody]) => {
        setRsvps(rsvpBody.items ?? []);
        setSummary(summaryBody);
      })
      .catch(() => setError("Gagal memuat RSVP"))
      .finally(() => setLoading(false));
  }, [ready, token, invitationId]);

  if (!ready || !invitationId) return null;

  return (
    <DashboardShell active="rsvp" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>RSVP</h1>
          <p className="dashboard-subtitle">Konfirmasi kehadiran dari tamu kamu.</p>
        </div>
      </header>

      {summary && (
        <section className="dashboard-summary">
          <div className="dashboard-stat"><span>Hadir</span><strong>{summary.yes}</strong></div>
          <div className="dashboard-stat"><span>Tidak hadir</span><strong>{summary.no}</strong></div>
          <div className="dashboard-stat"><span>Mungkin</span><strong>{summary.maybe}</strong></div>
          <div className="dashboard-stat"><span>Total hadir</span><strong>{summary.attendees}</strong></div>
        </section>
      )}

      {loading && <p className="dashboard-state">Memuat RSVP...</p>}
      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}
      {!loading && !error && rsvps.length === 0 && <p className="dashboard-state">Belum ada RSVP.</p>}
      {!loading && rsvps.length > 0 && (
        <div className="dashboard-table-wrap">
          <table className="dashboard-table">
            <thead>
              <tr>
                <th>Kehadiran</th>
                <th>Jumlah tamu</th>
                <th>Pesan</th>
                <th>Dikirim</th>
              </tr>
            </thead>
            <tbody>
              {rsvps.map((rsvp) => (
                <tr key={rsvp.id}>
                  <td><span className={`status ${rsvp.attendance === "yes" ? "status-published" : "status-draft"}`}>{attendanceLabels[rsvp.attendance] ?? rsvp.attendance}</span></td>
                  <td>{rsvp.attendees_count}</td>
                  <td>{rsvp.message || "—"}</td>
                  <td>{new Date(rsvp.submitted_at).toLocaleString("id-ID")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </DashboardShell>
  );
}
