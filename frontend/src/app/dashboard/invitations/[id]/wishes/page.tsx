"use client";

import { useCallback, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type Wish = { id: string; name: string; message: string; status: string; created_at: string };

export default function WishesPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [wishes, setWishes] = useState<Wish[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const invitationId = routeParams?.id;

  const load = useCallback(() => {
    if (!token || !invitationId) return;
    apiFetch(`/api/invitations/${invitationId}/wishes`, token)
      .then((response) => response.json())
      .then((body: { items?: Wish[] }) => setWishes(body.items ?? []))
      .catch(() => setError("Could not load wishes"))
      .finally(() => setLoading(false));
  }, [token, invitationId]);

  useEffect(() => {
    if (!ready) return;
    load();
  }, [ready, load]);

  async function setStatus(wishId: string, status: string) {
    if (!token || !invitationId) return;
    await apiFetch(`/api/invitations/${invitationId}/wishes/${wishId}`, token, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    });
    load();
  }

  if (!ready || !invitationId) return null;

  return (
    <DashboardShell active="wishes" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Invitation</p>
          <h1>Wishes</h1>
          <p className="dashboard-subtitle">Moderate messages before they appear on the public page.</p>
        </div>
      </header>

      {loading && <p className="dashboard-state">Loading wishes...</p>}
      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}
      {!loading && !error && wishes.length === 0 && <p className="dashboard-state">No wishes yet.</p>}
      {!loading && wishes.length > 0 && (
        <div className="dashboard-table-wrap">
          <table className="dashboard-table">
            <thead>
              <tr>
                <th>Guest</th>
                <th>Message</th>
                <th>Status</th>
                <th><span className="sr-only">Actions</span></th>
              </tr>
            </thead>
            <tbody>
              {wishes.map((wish) => (
                <tr key={wish.id}>
                  <td><strong>{wish.name}</strong></td>
                  <td>{wish.message}</td>
                  <td><span className={`status ${wish.status === "published" ? "status-published" : "status-draft"}`}>{wish.status}</span></td>
                  <td style={{ display: "flex", gap: ".5rem" }}>
                    {wish.status !== "published" && (
                      <button className="table-action" onClick={() => setStatus(wish.id, "published")}>Publish</button>
                    )}
                    {wish.status !== "rejected" && (
                      <button className="table-action" onClick={() => setStatus(wish.id, "rejected")}>Hide</button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </DashboardShell>
  );
}
