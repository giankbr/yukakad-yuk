"use client";

import { useCallback, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { FormField, FormTextarea } from "@/components/dashboard/FormField";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { useAdminAuth } from "@/lib/useAuthToken";

type Testimonial = { id: string; name: string; role?: string; quote: string; avatar_url?: string };

export default function AdminTestimonialsPage() {
  const { token, ready } = useAdminAuth();
  const [items, setItems] = useState<Testimonial[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({ name: "", role: "", quote: "", avatar_url: "" });

  const load = useCallback(() => {
    if (!token) return;
    apiFetch("/api/admin/testimonials", token)
      .then((r) => r.json())
      .then((body: { items?: Testimonial[] }) => setItems(body.items ?? []))
      .catch(() => setError("Could not load testimonials"))
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
      const response = await apiFetch("/api/admin/testimonials", token, { method: "POST", body: JSON.stringify(form) });
      if (!response.ok) throw new Error();
      setForm({ name: "", role: "", quote: "", avatar_url: "" });
      load();
    } catch {
      setError("Could not add testimonial");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id: string) {
    if (!token) return;
    await apiFetch(`/api/admin/testimonials/${id}`, token, { method: "DELETE" });
    load();
  }

  if (!ready || !token) return null;

  return (
    <DashboardShell active="testimonials" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Landing page</p>
          <h1>Testimonials</h1>
          <p className="dashboard-subtitle">{items.length} testimoni ditampilkan di home page</p>
        </div>
      </header>

      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      <form className="dashboard-form" onSubmit={handleSubmit}>
        <div className="form-row">
          <FormField label="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Dinda & Raka" required />
          <FormField label="Role (optional)" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })} placeholder="Pengantin, Jakarta" />
        </div>
        <FormTextarea label="Quote" rows={2} value={form.quote} onChange={(e) => setForm({ ...form, quote: e.target.value })} placeholder="Prosesnya cepat banget, tamu-tamu juga suka tampilannya." required />
        <FormField label="Avatar URL (optional)" value={form.avatar_url} onChange={(e) => setForm({ ...form, avatar_url: e.target.value })} placeholder="https://..." />
        <div className="form-actions">
          <Button type="submit" disabled={saving} className="bg-[#173c3a] text-white">
            {saving ? "Adding..." : "Add testimonial"}
          </Button>
        </div>
      </form>

      {loading && <p className="dashboard-state">Loading...</p>}
      {!loading && items.length > 0 && (
        <div className="card-grid">
          {items.map((item) => (
            <div className="dashboard-card" key={item.id}>
              <h3>{item.name}</h3>
              {item.role && <span className="dashboard-card-meta">{item.role}</span>}
              <p style={{ margin: 0, color: "#6e786f", fontSize: ".85rem" }}>&ldquo;{item.quote}&rdquo;</p>
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
