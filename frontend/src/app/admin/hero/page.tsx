"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { FormField, FormTextarea } from "@/components/dashboard/FormField";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { useAdminAuth } from "@/lib/useAuthToken";

type Hero = {
  heading?: string;
  subheading?: string;
  cta_label?: string;
  cta_href?: string;
};

export default function AdminHeroPage() {
  const { token, ready } = useAdminAuth();
  const [hero, setHero] = useState<Hero>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready || !token) return;
    apiFetch("/api/admin/site-content/hero", token)
      .then((r) => r.json())
      .then(setHero)
      .catch(() => setError("Could not load hero content"))
      .finally(() => setLoading(false));
  }, [ready, token]);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!token) return;
    setSaving(true);
    setSaved(false);
    setError("");
    try {
      const response = await apiFetch("/api/admin/site-content/hero", token, { method: "PUT", body: JSON.stringify(hero) });
      if (!response.ok) throw new Error();
      setSaved(true);
    } catch {
      setError("Could not save hero content");
    } finally {
      setSaving(false);
    }
  }

  if (!ready || !token) return null;

  return (
    <DashboardShell active="hero" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Landing page</p>
          <h1>Hero</h1>
          <p className="dashboard-subtitle">The first thing visitors see on the home page.</p>
        </div>
      </header>

      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      {!loading && (
        <form className="dashboard-form" onSubmit={handleSubmit}>
          <FormField label="Heading" value={hero.heading ?? ""} onChange={(e) => setHero({ ...hero, heading: e.target.value })} placeholder="Bikin undangan digital dalam hitungan menit" />
          <FormTextarea label="Subheading" rows={3} value={hero.subheading ?? ""} onChange={(e) => setHero({ ...hero, subheading: e.target.value })} placeholder="Platform undangan digital modern untuk pernikahan dan acara spesialmu." />
          <div className="form-row">
            <FormField label="CTA label" value={hero.cta_label ?? ""} onChange={(e) => setHero({ ...hero, cta_label: e.target.value })} placeholder="Buat undangan gratis" />
            <FormField label="CTA link" value={hero.cta_href ?? ""} onChange={(e) => setHero({ ...hero, cta_href: e.target.value })} placeholder="/auth/register" />
          </div>
          <div className="form-actions">
            <Button type="submit" disabled={saving} className="bg-[#173c3a] text-white">
              {saving ? "Saving..." : "Save changes"}
            </Button>
            {saved && <span className="form-hint">Saved.</span>}
          </div>
        </form>
      )}
    </DashboardShell>
  );
}
