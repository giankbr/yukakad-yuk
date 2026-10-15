"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken } from "@/lib/useAuthToken";
import { landingPath, ROLE_LABELS, type AccessRole } from "@/lib/invitation-access";

type Invitation = {
  id: string;
  slug: string;
  title: string;
  published: boolean;
};
type Shared = Invitation & { role: Exclude<AccessRole, "owner">; owner_name?: string };

export default function InvitationsListPage() {
  const { token, ready } = useAuthToken();
  const [invitations, setInvitations] = useState<Invitation[]>([]);
  const [shared, setShared] = useState<Shared[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready || !token) return;
    apiFetch("/api/invitations", token)
      .then(async (response) => {
        if (!response.ok) throw new Error("Gagal memuat daftar undangan");
        return response.json();
      })
      .then((body: { items?: Invitation[]; shared?: Shared[] }) => { setInvitations(body.items ?? []); setShared(body.shared ?? []); })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [ready, token]);

  if (!ready) return null;

  return (
    <DashboardShell active="invitations">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Akun</p>
          <h1>Undangan</h1>
          <p className="dashboard-subtitle">Semua undangan yang sudah kamu buat atau terbitkan.</p>
        </div>
        <Link className="dashboard-action" href="/dashboard/invitations/create">
          + Buat undangan
        </Link>
      </header>

      {loading && <p className="dashboard-state">Memuat undangan...</p>}
      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}
      {!loading && !error && invitations.length === 0 && shared.length === 0 && (
        <div className="dashboard-empty">
          <span className="dashboard-empty-icon" aria-hidden>
            <svg width="26" height="26" viewBox="0 0 256 256" fill="currentColor"><path d="M224,48H32a8,8,0,0,0-8,8V192a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A8,8,0,0,0,224,48Zm-96,85.15L52.57,64H203.43ZM98.71,128,40,181.81V74.19Zm11.84,10.85,12,11.05a8,8,0,0,0,10.82,0l12-11.05,58,53.15H52.57ZM157.29,128,216,74.18V181.82Z" /></svg>
          </span>
          <h2>Belum ada undangan</h2>
          <p>Pilih tema, isi nama dan tanggal acara, lalu bagikan link-nya ke tamu. Cuma butuh sekitar 10 menit.</p>
          <div className="dashboard-empty-actions">
            <Link className="dashboard-action" href="/dashboard/invitations/create">+ Buat undangan pertama</Link>
            <Link className="secondary-action" href="/dashboard/templates">Lihat tema</Link>
          </div>
        </div>
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
                    <span>rawuh.id/{invitation.slug}</span>
                  </td>
                  <td>
                    <span className={`status status-${invitation.published ? "published" : "draft"}`}>
                      {invitation.published ? "Terbit" : "Draf"}
                    </span>
                  </td>
                  <td>
                    <a className="table-action" href={`/dashboard/invitations/${invitation.id}`}>
                      Buka →
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {!loading && shared.length > 0 && (
        <section aria-label="Dibagikan ke kamu" style={{ marginTop: 28 }}>
          <h2 style={{ margin: "0 0 12px", color: "var(--rw-ink)", fontSize: 18 }}>Dibagikan ke kamu</h2>
          <div className="dashboard-table-wrap">
            <table className="dashboard-table">
              <thead><tr><th>Undangan</th><th>Peranmu</th><th><span className="sr-only">Aksi</span></th></tr></thead>
              <tbody>
                {shared.map((invitation) => (
                  <tr key={invitation.id}>
                    <td><strong>{invitation.title}</strong><span>{invitation.owner_name ? `Milik ${invitation.owner_name}` : `rawuh.id/${invitation.slug}`}</span></td>
                    <td><span className="status status-draft">{ROLE_LABELS[invitation.role]}</span></td>
                    <td><a className="table-action" href={landingPath(invitation.id, invitation.role)}>Buka →</a></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </DashboardShell>
  );
}
