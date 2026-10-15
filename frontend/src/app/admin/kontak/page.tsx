"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { FormField, FormTextarea } from "@/components/dashboard/FormField";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { useAdminAuth } from "@/lib/useAuthToken";

type Kontak = {
  heading?: string;
  subheading?: string;
  whatsapp?: string;
};

export default function AdminKontakPage() {
  const { token, ready } = useAdminAuth();
  const [kontak, setKontak] = useState<Kontak>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready || !token) return;
    apiFetch("/api/admin/site-content/kontak", token)
      .then((r) => r.json())
      .then(setKontak)
      .catch(() => setError("Gagal memuat konten kontak"))
      .finally(() => setLoading(false));
  }, [ready, token]);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!token) return;
    setSaving(true);
    setSaved(false);
    setError("");
    try {
      const response = await apiFetch("/api/admin/site-content/kontak", token, { method: "PUT", body: JSON.stringify(kontak) });
      if (!response.ok) throw new Error();
      setSaved(true);
    } catch {
      setError("Gagal menyimpan konten kontak");
    } finally {
      setSaving(false);
    }
  }

  if (!ready || !token) return null;

  return (
    <DashboardShell active="kontak" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Landing page</p>
          <h1>Kontak</h1>
          <p className="dashboard-subtitle">Banner kontak yang tampil di dekat bagian bawah home page.</p>
        </div>
      </header>

      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      {!loading && (
        <form className="dashboard-form" onSubmit={handleSubmit}>
          <FormField label="Judul" value={kontak.heading ?? ""} onChange={(e) => setKontak({ ...kontak, heading: e.target.value })} placeholder="Siap bikin undangan digitalmu?" />
          <FormTextarea label="Subjudul" rows={2} value={kontak.subheading ?? ""} onChange={(e) => setKontak({ ...kontak, subheading: e.target.value })} placeholder="Tim kami siap bantu kapan saja." />
          <FormField label="Nomor WhatsApp" value={kontak.whatsapp ?? ""} onChange={(e) => setKontak({ ...kontak, whatsapp: e.target.value })} placeholder="628123456789" />
          <div className="form-actions">
            <Button type="submit" disabled={saving} className="bg-[#173c3a] text-white">
              {saving ? "Menyimpan..." : "Simpan perubahan"}
            </Button>
            {saved && <span className="form-hint">Tersimpan.</span>}
          </div>
        </form>
      )}
    </DashboardShell>
  );
}
