"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch, saveProfile, saveToken } from "@/lib/api";
import { friendlyError } from "@/lib/errors";
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
  const [pw, setPw] = useState({ current: "", next: "", confirm: "" });
  const [pwSaving, setPwSaving] = useState(false);
  const [pwStatus, setPwStatus] = useState<{ ok: boolean; text: string } | null>(null);
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
        saveProfile({ name: body.name ?? "", email: body.email ?? "" });
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
      if (!response.ok) throw new Error(friendlyError(body.error, "Profil gagal disimpan"));
      setProfile(body);
      setName(body.name ?? "");
      saveProfile({ name: body.name ?? "" });
      setSaved(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Profil gagal disimpan");
    } finally {
      setSaving(false);
    }
  }

  async function changePassword(event: React.FormEvent) {
    event.preventDefault();
    if (!token) return;
    setPwStatus(null);
    if (pw.next !== pw.confirm) { setPwStatus({ ok: false, text: "Konfirmasi password tidak sama." }); return; }
    setPwSaving(true);
    try {
      const response = await apiFetch("/api/auth/change-password", token, { method: "POST", body: JSON.stringify({ current_password: pw.current, new_password: pw.next }) });
      const body = (await response.json().catch(() => ({}))) as { error?: string; token?: string };
      if (!response.ok) throw new Error(friendlyError(body.error, "Password belum diganti."));
      // Changing the password revokes every earlier session, including this one: keep the fresh token.
      if (body.token) saveToken(body.token);
      setPw({ current: "", next: "", confirm: "" });
      setPwStatus({ ok: true, text: "Password berhasil diganti. Sesi di perangkat lain otomatis keluar." });
    } catch (err) {
      setPwStatus({ ok: false, text: err instanceof Error && err.message ? err.message : "Password belum diganti." });
    } finally {
      setPwSaving(false);
    }
  }

  if (!ready) return null;

  return (
    <DashboardShell active="settings">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Akun</p>
          <h1>Pengaturan</h1>
          <p className="dashboard-subtitle">Kelola profil dan keamanan akunmu.</p>
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

      {!loading && profile && (
        <form className="dashboard-form" onSubmit={changePassword} style={{ marginTop: 24 }} aria-labelledby="pw-heading">
          <h2 id="pw-heading" style={{ margin: 0, color: "var(--rw-ink)", fontSize: 18 }}>Ganti password</h2>
          <div className="form-field">
            <label htmlFor="pw-current">Password saat ini</label>
            <input id="pw-current" type="password" autoComplete="current-password" value={pw.current} onChange={(e) => setPw({ ...pw, current: e.target.value })} required />
          </div>
          <div className="form-field">
            <label htmlFor="pw-new">Password baru</label>
            <input id="pw-new" type="password" autoComplete="new-password" minLength={8} value={pw.next} onChange={(e) => setPw({ ...pw, next: e.target.value })} required />
            <p className="form-hint">Minimal 8 karakter.</p>
          </div>
          <div className="form-field">
            <label htmlFor="pw-confirm">Ulangi password baru</label>
            <input id="pw-confirm" type="password" autoComplete="new-password" minLength={8} value={pw.confirm} onChange={(e) => setPw({ ...pw, confirm: e.target.value })} required />
          </div>
          {pwStatus && <p className={`dashboard-state ${pwStatus.ok ? "" : "dashboard-state-error"}`} role={pwStatus.ok ? "status" : "alert"}>{pwStatus.text}</p>}
          <button type="submit" disabled={pwSaving}>{pwSaving ? "Menyimpan..." : "Ganti password"}</button>
        </form>
      )}
    </DashboardShell>
  );
}
