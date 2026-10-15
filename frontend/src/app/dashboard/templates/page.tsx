"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { ThemeGrid, ThemeLink, type DashboardTemplate } from "@/components/dashboard/ThemeGrid";
import { API_URL } from "@/lib/api";
import { useAuthToken } from "@/lib/useAuthToken";

export default function DashboardTemplatesPage() {
  const { ready } = useAuthToken();
  const [templates, setTemplates] = useState<DashboardTemplate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready) return;
    fetch(`${API_URL}/api/templates`)
      .then(async (response) => {
        if (!response.ok) throw new Error("Tema gagal dimuat");
        return response.json();
      })
      .then((body: { items?: DashboardTemplate[] }) => setTemplates(body.items ?? []))
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [ready]);

  if (!ready) return null;

  return (
    <DashboardShell active="templates">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Workspace</p>
          <h1>Tema</h1>
          <p className="dashboard-subtitle">{templates.length ? `${templates.length} tema siap pakai. ` : ""}Lihat demo, lalu pakai saat membuat undangan baru.</p>
        </div>
        <Link className="dashboard-action" href="/dashboard/invitations/create">
          + Buat undangan
        </Link>
      </header>

      {loading && <p className="dashboard-state">Memuat tema...</p>}
      {error && <p className="dashboard-state dashboard-state-error" role="alert">{error}</p>}

      {!loading && !error && (
        <ThemeGrid
          templates={templates}
          action={(template) => (
            <ThemeLink href={`/dashboard/invitations/create?template=${encodeURIComponent(template.id)}`}>Pakai tema</ThemeLink>
          )}
        />
      )}
    </DashboardShell>
  );
}
