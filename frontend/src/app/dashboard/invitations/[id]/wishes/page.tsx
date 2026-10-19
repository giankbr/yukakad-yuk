"use client";

import { useCallback, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";
import { GateNotice, getJson, lostAccess, usePageGate } from "../_lib";

type Wish = { id: string; name: string; message: string; status: string; created_at: string };

const wishStatusLabels: Record<string, string> = { published: "Tampil", rejected: "Disembunyikan", pending: "Menunggu" };

export default function WishesPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [wishes, setWishes] = useState<Wish[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const invitationId = routeParams?.id;

  const gate = usePageGate(invitationId, token, "wishes");
  const { lose } = gate;
  const allowed = gate.status === "ok";

  const load = useCallback(() => {
    if (!token || !invitationId) return;
    getJson<{ items?: Wish[] }>(`/api/invitations/${invitationId}/wishes`, token)
      .then((result) => {
        if (lostAccess(result.status)) { lose(); return; }
        if (!result.ok) { setError(result.error || "Gagal memuat ucapan."); return; }
        setError("");
        setWishes(result.data?.items ?? []);
      })
      .finally(() => setLoading(false));
  }, [token, invitationId, lose]);

  useEffect(() => {
    if (!ready || !allowed) return;
    load();
  }, [ready, allowed, load]);

  async function setStatus(wishId: string, status: string) {
    if (!token || !invitationId) return;
    const response = await apiFetch(`/api/invitations/${invitationId}/wishes/${wishId}`, token, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    }).catch(() => null);
    if (!response?.ok) { setError("Status ucapan belum tersimpan. Coba lagi."); return; }
    load();
  }

  if (!ready || !invitationId) return null;

  if (!allowed) {
    return (
      <DashboardShell active="wishes" invitationId={invitationId}>
        <GateNotice gate={gate} invitationId={invitationId} />
      </DashboardShell>
    );
  }

  return (
    <DashboardShell active="wishes" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>Ucapan</h1>
          <p className="dashboard-subtitle">Moderasi ucapan sebelum tampil di halaman publik.</p>
        </div>
      </header>

      {loading && <p className="dashboard-state">Memuat ucapan...</p>}
      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}
      {!loading && !error && wishes.length === 0 && <p className="dashboard-state">Belum ada ucapan.</p>}
      {!loading && wishes.length > 0 && (
        <div className="dashboard-table-wrap">
          <table className="dashboard-table">
            <thead>
              <tr>
                <th>Tamu</th>
                <th>Ucapan</th>
                <th>Status</th>
                <th><span className="sr-only">Aksi</span></th>
              </tr>
            </thead>
            <tbody>
              {wishes.map((wish) => (
                <tr key={wish.id}>
                  <td><strong>{wish.name}</strong></td>
                  <td>{wish.message}</td>
                  <td><span className={`status ${wish.status === "published" ? "status-published" : "status-draft"}`}>{wishStatusLabels[wish.status] ?? wish.status}</span></td>
                  <td style={{ display: "flex", gap: ".5rem" }}>
                    {wish.status !== "published" && (
                      <button className="table-action" onClick={() => setStatus(wish.id, "published")}>Tampilkan</button>
                    )}
                    {wish.status !== "rejected" && (
                      <button className="table-action" onClick={() => setStatus(wish.id, "rejected")}>Sembunyikan</button>
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
