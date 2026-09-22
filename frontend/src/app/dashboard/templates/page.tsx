"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { API_URL } from "@/lib/api";
import { useAuthToken } from "@/lib/useAuthToken";

type Template = {
  id: string;
  name: string;
  slug: string;
  category: string;
  preview_image?: string;
  preview_url?: string;
  is_premium: boolean;
};

export default function DashboardTemplatesPage() {
  const { ready } = useAuthToken();
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [category, setCategory] = useState("all");

  useEffect(() => {
    if (!ready) return;
    fetch(`${API_URL}/api/templates`)
      .then(async (response) => {
        if (!response.ok) throw new Error("Template gagal dimuat");
        return response.json();
      })
      .then((body: { items?: Template[] }) => setTemplates(body.items ?? []))
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [ready]);

  if (!ready) return null;

  const categories = ["all", ...Array.from(new Set(templates.map((t) => t.category).filter(Boolean)))];
  const visible = category === "all" ? templates : templates.filter((t) => t.category === category);

  return (
    <DashboardShell active="templates">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Workspace</p>
          <h1>Template</h1>
          <p className="dashboard-subtitle">Lihat demo, lalu pakai template saat membuat undangan baru.</p>
        </div>
        <Link className="dashboard-action" href="/dashboard/invitations/create">
          + Buat undangan
        </Link>
      </header>

      {loading && <p className="dashboard-state">Memuat template...</p>}
      {error && <p className="dashboard-state dashboard-state-error" role="alert">{error}</p>}

      {!loading && !error && (
        <>
          <div className="form-row" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(5.5rem, auto))", gap: ".4rem", marginBottom: "1.25rem" }}>
            {categories.map((cat) => (
              <button
                key={cat}
                type="button"
                className="table-action"
                style={{ textTransform: "capitalize", fontWeight: category === cat ? 700 : 500 }}
                onClick={() => setCategory(cat)}
              >
                {cat}
              </button>
            ))}
          </div>

          {visible.length === 0 ? (
            <p className="dashboard-state">Belum ada template di kategori ini.</p>
          ) : (
            <div className="card-grid">
              {visible.map((template) => {
                const demoHref = template.preview_url || `/invitation/demo?template=${encodeURIComponent(template.id)}`;
                return (
                  <div className="dashboard-card" key={template.id}>
                    {template.preview_image && (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img src={template.preview_image} alt={template.name} />
                    )}
                    <div className="dashboard-card-meta">
                      <h3>{template.name}</h3>
                      {template.is_premium && <span className="badge badge-premium">Premium</span>}
                    </div>
                    <span className="badge" style={{ width: "fit-content", textTransform: "capitalize" }}>{template.category || "general"}</span>
                    <div style={{ display: "flex", flexWrap: "wrap", gap: ".4rem" }}>
                      <a className="table-action" href={demoHref} target="_blank" rel="noreferrer">Demo ↗</a>
                      <Link className="table-action" href={`/dashboard/invitations/create?template=${encodeURIComponent(template.id)}`}>
                        Pakai template
                      </Link>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </>
      )}
    </DashboardShell>
  );
}
