"use client";

import { useEffect, useMemo, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { friendlyError } from "@/lib/errors";
import { useAdminAuth } from "@/lib/useAuthToken";

type Template = { id: string; name: string; slug: string; category: string; is_premium: boolean; tier: string; status: string; preview_image?: string; sort_order: number };

export default function AdminTemplatesPage() {
  const { token, ready } = useAdminAuth();
  const [items, setItems] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready || !token) return;
    apiFetch("/api/admin/templates", token)
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
      .then((body: { items?: Template[] }) => setItems((body.items ?? []).slice().sort((a, b) => a.sort_order - b.sort_order)))
      .catch(() => setError("Gagal memuat tema"))
      .finally(() => setLoading(false));
  }, [ready, token]);

  async function update(item: Template, patch: Partial<Template>, path = "") {
    if (!token) return;
    setBusy(item.id);
    setError("");
    try {
      const response = path
        ? await apiFetch(`/api/admin/templates/${item.id}/${path}`, token, { method: "POST" })
        : await apiFetch(`/api/admin/templates/${item.id}`, token, { method: "PATCH", body: JSON.stringify(patch) });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(friendlyError(body.error, ""));
      setItems((current) => current.map((entry) => (entry.id === item.id ? { ...entry, ...body } : entry)));
    } catch (err) {
      setError(err instanceof Error && err.message ? `${item.name}: ${err.message}` : `${item.name} belum tersimpan.`);
    } finally {
      setBusy(null);
    }
  }

  const visible = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return items.filter((item) => !needle || `${item.name} ${item.category}`.toLowerCase().includes(needle));
  }, [items, query]);

  if (!ready || !token) return null;

  const active = items.filter((item) => item.status === "active").length;
  const premium = items.filter((item) => item.is_premium).length;

  return (
    <DashboardShell active="templates" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Bisnis</p>
          <h1>Tema</h1>
          <p className="dashboard-subtitle">{items.length} tema · {active} aktif · {premium} Premium. Tema nonaktif tidak tampil di galeri dan tidak bisa dipilih.</p>
        </div>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}

      <label className={styles.field} style={{ maxWidth: 360, marginBottom: 16 }}>
        <span className="sr-only">Cari tema</span>
        <input type="search" placeholder="Cari nama atau kategori…" value={query} onChange={(e) => setQuery(e.target.value)} />
      </label>

      {loading ? <p className="dashboard-state">Memuat tema…</p> : (
        <div className="dashboard-table-wrap">
          <table className="dashboard-table" style={{ minWidth: 640 }}>
            <thead><tr><th>Tema</th><th>Kategori</th><th>Akses</th><th>Status</th><th><span className="sr-only">Demo</span></th></tr></thead>
            <tbody>
              {visible.map((item) => (
                <tr key={item.id}>
                  <td>
                    <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      <img src={item.preview_image || `/themes/previews/${item.slug}.webp`} alt="" width={36} height={48} style={{ borderRadius: 6, objectFit: "cover", objectPosition: "top", background: "var(--rw-surface)" }} />
                      <strong>{item.name}</strong>
                    </div>
                  </td>
                  <td>
                    <input className="table-input" style={{ width: 140 }} defaultValue={item.category} key={item.category} aria-label={`Kategori ${item.name}`}
                      onBlur={(e) => { const value = e.target.value.trim(); if (value && value !== item.category) void update(item, { category: value }); }}
                      onKeyDown={(e) => { if (e.key === "Enter") e.currentTarget.blur(); }} />
                  </td>
                  <td>
                    <label className={styles.check}>
                      <input type="checkbox" checked={item.is_premium} disabled={busy === item.id}
                        onChange={(e) => update(item, { is_premium: e.target.checked, tier: e.target.checked ? "premium" : "free" })} />
                      Premium
                    </label>
                  </td>
                  <td>
                    <button type="button" className={`table-action${item.status === "active" ? "" : " table-action-danger"}`} disabled={busy === item.id}
                      onClick={() => update(item, {}, item.status === "active" ? "archive" : "publish")}>
                      {item.status === "active" ? "Aktif" : "Nonaktif"}
                    </button>
                  </td>
                  <td><a className="table-action" href={`/invitation/demo?template=${item.slug}`} target="_blank" rel="noreferrer">Demo ↗</a></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </DashboardShell>
  );
}
