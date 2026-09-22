"use client";

import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { FormField } from "@/components/dashboard/FormField";
import { TemplatePicker } from "@/components/dashboard/TemplatePicker";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type Settings = {
  theme?: string;
  primary_color?: string;
  secondary_color?: string;
  font?: string;
  music_url?: string;
  autoplay_music?: boolean;
};

export default function SettingsPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [templateId, setTemplateId] = useState("");
  const [settings, setSettings] = useState<Settings>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [uploadingMusic, setUploadingMusic] = useState(false);
  const [error, setError] = useState("");

  const invitationId = routeParams?.id;

  useEffect(() => {
    if (!ready || !token || !invitationId) return;
    Promise.all([
      apiFetch(`/api/invitations/${invitationId}`, token).then((r) => r.json()),
      apiFetch(`/api/invitations/${invitationId}/settings`, token).then((r) => r.json()),
    ])
      .then(([invitationBody, settingsBody]) => {
        setTemplateId(invitationBody.template_id ?? "");
        setSettings(settingsBody);
      })
      .catch(() => setError("Could not load settings"))
      .finally(() => setLoading(false));
  }, [ready, token, invitationId]);

  async function handleUploadMusic(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file || !token || !invitationId) return;
    setUploadingMusic(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("type", "music");
      const response = await apiFetch(`/api/invitations/${invitationId}/media`, token, { method: "POST", body: formData });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error ?? "Upload failed");
      setSettings((prev) => ({ ...prev, music_url: body.path }));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Music upload failed");
    } finally {
      setUploadingMusic(false);
    }
  }

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!token || !invitationId) return;
    setSaving(true);
    setSaved(false);
    setError("");
    try {
      const response = await apiFetch(`/api/invitations/${invitationId}/settings`, token, {
        method: "PATCH",
        body: JSON.stringify(settings),
      });
      if (!response.ok) throw new Error();
      setSaved(true);
    } catch {
      setError("Could not save settings");
    } finally {
      setSaving(false);
    }
  }

  if (!ready || !invitationId || !token) return null;

  return (
    <DashboardShell active="settings" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Invitation</p>
          <h1>Settings</h1>
          <p className="dashboard-subtitle">Template, theme, and background music.</p>
        </div>
      </header>

      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      <section>
        <h2 style={{ color: "#173c3a" }}>Template</h2>
        {!loading && <TemplatePicker invitationId={invitationId} token={token} selectedTemplateId={templateId} />}
      </section>

      {!loading && (
        <form className="dashboard-form" onSubmit={handleSubmit} style={{ marginTop: "2rem" }}>
          <h2 style={{ margin: 0, color: "#173c3a" }}>Theme</h2>
          <div className="form-row">
            <FormField
              label="Primary color"
              type="color"
              value={settings.primary_color ?? "#d97706"}
              onChange={(e) => setSettings({ ...settings, primary_color: e.target.value })}
            />
            <FormField
              label="Secondary color"
              type="color"
              value={settings.secondary_color ?? "#f59e0b"}
              onChange={(e) => setSettings({ ...settings, secondary_color: e.target.value })}
            />
          </div>
          <FormField label="Font" value={settings.font ?? ""} onChange={(e) => setSettings({ ...settings, font: e.target.value })} placeholder="poppins" />

          <h2 style={{ margin: "1rem 0 0", color: "#173c3a" }}>Music</h2>
          <label className="upload-drop">
            <span>{uploadingMusic ? "Uploading..." : settings.music_url ? "Music uploaded — click to replace" : "Click to upload background music (MP3, max 10MB)"}</span>
            <input type="file" accept="audio/mpeg" onChange={handleUploadMusic} disabled={uploadingMusic} hidden />
          </label>
          <label style={{ display: "flex", alignItems: "center", gap: ".5rem", fontSize: ".85rem", color: "#536057" }}>
            <input
              type="checkbox"
              style={{ width: "auto" }}
              checked={settings.autoplay_music ?? false}
              onChange={(e) => setSettings({ ...settings, autoplay_music: e.target.checked })}
            />
            Autoplay music on open
          </label>

          <div className="form-actions">
            <Button type="submit" disabled={saving} className="bg-[#173c3a] text-white">
              {saving ? "Saving..." : "Save settings"}
            </Button>
            {saved && <span className="form-hint">Saved.</span>}
          </div>
        </form>
      )}
    </DashboardShell>
  );
}
