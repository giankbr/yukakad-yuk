"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { FormField } from "@/components/dashboard/FormField";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { useAdminAuth } from "@/lib/useAuthToken";

type Footer = {
  heading?: string;
  copyright?: string;
  instagram?: string;
};

export default function AdminFooterPage() {
  const { token, ready } = useAdminAuth();
  const [footer, setFooter] = useState<Footer>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready || !token) return;
    apiFetch("/api/admin/site-content/footer", token)
      .then((r) => r.json())
      .then(setFooter)
      .catch(() => setError("Could not load footer content"))
      .finally(() => setLoading(false));
  }, [ready, token]);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!token) return;
    setSaving(true);
    setSaved(false);
    setError("");
    try {
      const response = await apiFetch("/api/admin/site-content/footer", token, { method: "PUT", body: JSON.stringify(footer) });
      if (!response.ok) throw new Error();
      setSaved(true);
    } catch {
      setError("Could not save footer content");
    } finally {
      setSaving(false);
    }
  }

  if (!ready || !token) return null;

  return (
    <DashboardShell active="footer" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Landing page</p>
          <h1>Footer</h1>
          <p className="dashboard-subtitle">Shown at the very bottom of the home page.</p>
        </div>
      </header>

      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      {!loading && (
        <form className="dashboard-form" onSubmit={handleSubmit}>
          <FormField label="Heading" value={footer.heading ?? ""} onChange={(e) => setFooter({ ...footer, heading: e.target.value })} placeholder="yukakad" />
          <FormField label="Copyright" value={footer.copyright ?? ""} onChange={(e) => setFooter({ ...footer, copyright: e.target.value })} placeholder="© 2026 Yukakad. All rights reserved." />
          <FormField label="Instagram handle" value={footer.instagram ?? ""} onChange={(e) => setFooter({ ...footer, instagram: e.target.value })} placeholder="@yukakad" />
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
