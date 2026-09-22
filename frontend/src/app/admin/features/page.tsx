"use client";

import { useCallback, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { FormField, FormTextarea } from "@/components/dashboard/FormField";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { useAdminAuth } from "@/lib/useAuthToken";

type Feature = { id: string; title: string; description: string; icon?: string };

export default function AdminFeaturesPage() {
  const { token, ready } = useAdminAuth();
  const [items, setItems] = useState<Feature[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({ title: "", description: "", icon: "" });

  const load = useCallback(() => {
    if (!token) return;
    apiFetch("/api/admin/features", token)
      .then((r) => r.json())
      .then((body: { items?: Feature[] }) => setItems(body.items ?? []))
      .catch(() => setError("Could not load features"))
      .finally(() => setLoading(false));
  }, [token]);

  useEffect(() => {
    if (!ready) return;
    load();
  }, [ready, load]);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!token) return;
    setSaving(true);
    setError("");
    try {
      const response = await apiFetch("/api/admin/features", token, { method: "POST", body: JSON.stringify(form) });
      if (!response.ok) throw new Error();
      setForm({ title: "", description: "", icon: "" });
      load();
    } catch {
      setError("Could not add feature");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id: string) {
    if (!token) return;
    await apiFetch(`/api/admin/features/${id}`, token, { method: "DELETE" });
    load();
  }

  if (!ready || !token) return null;

  return (
    <DashboardShell active="features" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Landing page</p>
          <h1>Fitur</h1>
          <p className="dashboard-subtitle">{items.length} fitur ditampilkan di home page</p>
        </div>
      </header>

      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      <form className="dashboard-form" onSubmit={handleSubmit}>
        <div className="form-row">
          <FormField label="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} placeholder="RSVP real-time" required />
          <FormField label="Icon (emoji, optional)" value={form.icon} onChange={(e) => setForm({ ...form, icon: e.target.value })} placeholder="✅" />
        </div>
        <FormTextarea label="Description" rows={2} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} placeholder="Pantau kehadiran tamu langsung dari dashboard." required />
        <div className="form-actions">
          <Button type="submit" disabled={saving} className="bg-[#173c3a] text-white">
            {saving ? "Adding..." : "Add feature"}
          </Button>
        </div>
      </form>

      {loading && <p className="dashboard-state">Loading...</p>}
      {!loading && items.length > 0 && (
        <div className="card-grid">
          {items.map((item) => (
            <div className="dashboard-card" key={item.id}>
              <h3>{item.icon ? `${item.icon} ` : ""}{item.title}</h3>
              <p style={{ margin: 0, color: "#6e786f", fontSize: ".85rem" }}>{item.description}</p>
              <button type="button" className="table-action" onClick={() => handleDelete(item.id)}>
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </DashboardShell>
  );
}
