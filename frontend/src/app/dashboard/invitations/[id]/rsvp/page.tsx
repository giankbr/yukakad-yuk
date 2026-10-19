"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";
import { GateNotice, getJson, lostAccess, usePageGate } from "../_lib";

type RSVP = {
  id: string;
  guest_id?: string;
  attendance: string;
  attendees_count: number;
  message?: string;
  submitted_at: string;
};

const attendanceLabels: Record<string, string> = { yes: "Hadir", no: "Tidak hadir", maybe: "Mungkin" };

/**
 * The public RSVP form stores one string: "Nama: pesan [Catatan makanan: ...]"
 * (see useRsvp in components/invitation/themes/kit.tsx). Split it back up.
 */
function parseRsvpMessage(raw?: string): { name: string; message: string; diet: string } {
  let text = (raw ?? "").trim();
  let diet = "";
  const dietMatch = text.match(/\s*\[Catatan makanan:\s*([\s\S]*?)\]\s*$/);
  if (dietMatch) {
    diet = dietMatch[1].trim();
    text = text.slice(0, dietMatch.index).trim();
  }
  const nameMatch = text.match(/^([^:\n]{1,120}):(?:\s+([\s\S]*)|$)/);
  if (nameMatch) return { name: nameMatch[1].trim(), message: (nameMatch[2] ?? "").trim(), diet };
  return { name: "", message: text, diet };
}

type Summary = { yes: number; no: number; maybe: number; attendees: number };

export default function RSVPPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [rsvps, setRsvps] = useState<RSVP[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const invitationId = routeParams?.id;

  const gate = usePageGate(invitationId, token, "rsvp");
  const { lose } = gate;
  const allowed = gate.status === "ok";

  useEffect(() => {
    if (!ready || !token || !invitationId || !allowed) return;
    Promise.all([
      getJson<{ items?: RSVP[] }>(`/api/invitations/${invitationId}/rsvps`, token),
      getJson<Summary>(`/api/invitations/${invitationId}/rsvps/summary`, token),
    ])
      .then(([rsvpBody, summaryBody]) => {
        if (lostAccess(rsvpBody.status)) { lose(); return; }
        if (!rsvpBody.ok) { setError(rsvpBody.error || "Gagal memuat RSVP."); return; }
        setRsvps(rsvpBody.data?.items ?? []);
        setSummary(summaryBody.ok && typeof summaryBody.data?.yes === "number" ? summaryBody.data : null);
      })
      .finally(() => setLoading(false));
  }, [ready, token, invitationId, allowed, lose]);

  if (!ready || !invitationId) return null;

  if (!allowed) {
    return (
      <DashboardShell active="rsvp" invitationId={invitationId}>
        <GateNotice gate={gate} invitationId={invitationId} />
      </DashboardShell>
    );
  }

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
                <th>Nama</th>
                <th>Kehadiran</th>
                <th>Jumlah tamu</th>
                <th>Pesan</th>
                <th>Catatan makanan</th>
                <th>Dikirim</th>
              </tr>
            </thead>
            <tbody>
              {rsvps.map((rsvp) => {
                const parsed = parseRsvpMessage(rsvp.message);
                return (
                <tr key={rsvp.id}>
                  <td><strong>{parsed.name || "—"}</strong></td>
                  <td><span className={`status ${rsvp.attendance === "yes" ? "status-published" : "status-draft"}`}>{attendanceLabels[rsvp.attendance] ?? rsvp.attendance}</span></td>
                  <td>{rsvp.attendees_count}</td>
                  <td style={{ minWidth: 200 }}>{parsed.message || "—"}</td>
                  <td>{parsed.diet || "—"}</td>
                  <td>{new Date(rsvp.submitted_at).toLocaleString("id-ID")}</td>
                </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </DashboardShell>
  );
}
