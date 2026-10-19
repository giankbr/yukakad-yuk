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
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
      .then(setHero)
      .catch(() => setError("Gagal memuat konten hero"))
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
      setError("Gagal menyimpan konten hero");
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
          <p className="dashboard-subtitle">Bagian pertama yang dilihat pengunjung di home page.</p>
        </div>
      </header>

      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      {!loading && (
        <form className="dashboard-form" onSubmit={handleSubmit}>
          <FormField label="Judul" value={hero.heading ?? ""} onChange={(e) => setHero({ ...hero, heading: e.target.value })} placeholder="Bikin undangan digital dalam hitungan menit" />
          <FormTextarea label="Subjudul" rows={3} value={hero.subheading ?? ""} onChange={(e) => setHero({ ...hero, subheading: e.target.value })} placeholder="Platform undangan digital modern untuk pernikahan dan acara spesialmu." />
          <div className="form-row">
            <FormField label="Teks tombol CTA" value={hero.cta_label ?? ""} onChange={(e) => setHero({ ...hero, cta_label: e.target.value })} placeholder="Buat undangan gratis" />
            <FormField label="Link tombol CTA" value={hero.cta_href ?? ""} onChange={(e) => setHero({ ...hero, cta_href: e.target.value })} placeholder="/auth/register" />
          </div>
          <div className="form-actions">
            <Button type="submit" disabled={saving}>
              {saving ? "Menyimpan..." : "Simpan perubahan"}
            </Button>
            {saved && <span className="form-hint">Tersimpan.</span>}
          </div>
        </form>
      )}
    </DashboardShell>
  );
}
