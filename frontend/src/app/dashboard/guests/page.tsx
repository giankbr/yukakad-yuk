"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken } from "@/lib/useAuthToken";

type Invitation = {
  id: string;
  slug: string;
  title: string;
  published: boolean;
};

export default function DashboardGuestsPage() {
  const { token, ready } = useAuthToken();
  const [invitations, setInvitations] = useState<Invitation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready || !token) return;
    apiFetch("/api/invitations", token)
      .then(async (response) => {
        if (!response.ok) throw new Error("Daftar undangan gagal dimuat");
        return response.json();
      })
      .then((body: { items?: Invitation[] }) => setInvitations(body.items ?? []))
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [ready, token]);

  if (!ready) return null;

  return (
    <DashboardShell active="guests">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Workspace</p>
          <h1>Tamu</h1>
          <p className="dashboard-subtitle">Kelola tamu per undangan. Pilih undangan untuk membuka daftar tamu.</p>
        </div>
        <Link className="dashboard-action" href="/dashboard/invitations/create">
          + Buat undangan
        </Link>
      </header>

      {loading && <p className="dashboard-state">Memuat undangan...</p>}
      {error && <p className="dashboard-state dashboard-state-error" role="alert">{error}</p>}
      {!loading && !error && invitations.length === 0 && (
        <p className="dashboard-state">Belum ada undangan. Buat undangan dulu untuk menambah tamu.</p>
      )}
      {!loading && !error && invitations.length > 0 && (
        <div className="dashboard-table-wrap">
          <table className="dashboard-table">
            <thead>
              <tr>
                <th>Undangan</th>
                <th>Status</th>
                <th><span className="sr-only">Aksi</span></th>
              </tr>
            </thead>
            <tbody>
              {invitations.map((invitation) => (
                <tr key={invitation.id}>
                  <td>
                    <strong>{invitation.title}</strong>
                    <span>yukakad.com/{invitation.slug}</span>
                  </td>
                  <td>
                    <span className={`status status-${invitation.published ? "published" : "draft"}`}>
                      {invitation.published ? "Published" : "Draft"}
                    </span>
                  </td>
                  <td>
                    <Link className="table-action" href={`/dashboard/invitations/${invitation.id}/guests`}>
                      Kelola tamu →
                    </Link>
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
