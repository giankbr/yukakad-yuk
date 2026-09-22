"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken } from "@/lib/useAuthToken";

type Profile = {
  id: string;
  name: string;
  email: string;
  role: string;
  avatar?: string;
};

export default function DashboardSettingsPage() {
  const { token, ready } = useAuthToken();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (!ready || !token) return;
    apiFetch("/api/profile", token)
      .then(async (response) => {
        if (!response.ok) throw new Error("Profil gagal dimuat");
        return response.json();
      })
      .then((body: Profile) => {
        setProfile(body);
        setName(body.name ?? "");
        if (typeof window !== "undefined") {
          window.localStorage.setItem("yukakad_name", body.name ?? "");
          window.localStorage.setItem("yukakad_email", body.email ?? "");
        }
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [ready, token]);

  async function handleSave(event: React.FormEvent) {
    event.preventDefault();
    if (!token) return;
    setSaving(true);
    setError("");
    setSaved(false);
    try {
      const response = await apiFetch("/api/profile", token, {
        method: "PATCH",
        body: JSON.stringify({ name: name.trim() }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error ?? "Profil gagal disimpan");
      setProfile(body);
      setName(body.name ?? "");
      if (typeof window !== "undefined") {
        window.localStorage.setItem("yukakad_name", body.name ?? "");
      }
      setSaved(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Profil gagal disimpan");
    } finally {
      setSaving(false);
    }
  }

  if (!ready) return null;

  return (
    <DashboardShell active="settings">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Workspace</p>
          <h1>Pengaturan</h1>
          <p className="dashboard-subtitle">Kelola profil akun yang dipakai di workspace kamu.</p>
        </div>
      </header>

      {loading && <p className="dashboard-state">Memuat profil...</p>}
      {error && <p className="dashboard-state dashboard-state-error" role="alert">{error}</p>}
      {saved && <p className="dashboard-state" role="status">Profil tersimpan.</p>}

      {!loading && profile && (
        <form className="dashboard-form" onSubmit={handleSave}>
          <div className="form-field">
            <label htmlFor="settings-name">Nama</label>
            <input
              id="settings-name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              maxLength={100}
              autoComplete="name"
            />
          </div>
          <div className="form-field">
            <label htmlFor="settings-email">Email</label>
            <input id="settings-email" value={profile.email} disabled readOnly />
            <p className="form-hint">Email tidak bisa diubah dari halaman ini.</p>
          </div>
          <div className="form-field">
            <label>Peran</label>
            <input value={profile.role} disabled readOnly style={{ textTransform: "capitalize" }} />
          </div>
          <button type="submit" disabled={saving || !name.trim()}>
            {saving ? "Menyimpan..." : "Simpan perubahan"}
          </button>
        </form>
      )}
    </DashboardShell>
  );
}
