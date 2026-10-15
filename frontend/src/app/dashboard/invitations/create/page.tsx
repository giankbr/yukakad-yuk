"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { FormField } from "@/components/dashboard/FormField";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { useAuthToken } from "@/lib/useAuthToken";

function slugify(value: string) {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

export default function CreateInvitationPage() {
  const { token, ready } = useAuthToken();
  const router = useRouter();
  // Prefilled from the landing page "Nama acaramu" field (forwarded through registration).
  const [title, setTitle] = useState(() => typeof window === "undefined" ? "" : new URLSearchParams(window.location.search).get("title") ?? "");
  const [slug, setSlug] = useState("");
  const [slugTouched, setSlugTouched] = useState(false);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (!ready) return null;
  // Set by "Pakai template" on /dashboard/templates. Safe to read: `ready` is only true client-side.
  const templateId = new URLSearchParams(window.location.search).get("template");

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!token) return;
    setSubmitting(true);
    setError("");
    try {
      const response = await apiFetch("/api/invitations", token, {
        method: "POST",
        body: JSON.stringify({ title, slug: slug || slugify(title) }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error ?? "Gagal membuat undangan");
      if (templateId) {
        // Non-blocking: the template can still be picked later from the invitation settings.
        await apiFetch(`/api/invitations/${body.id}/template`, token, { method: "PUT", body: JSON.stringify({ template_id: templateId }) }).catch(() => undefined);
      }
      router.push(`/dashboard/invitations/${body.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Terjadi kesalahan");
      setSubmitting(false);
    }
  }

  return (
    <DashboardShell active="invitations">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Akun</p>
          <h1>Buat undangan</h1>
          <p className="dashboard-subtitle">Kasih judul dulu. Detail lainnya bisa dilengkapi nanti.</p>
        </div>
      </header>

      <form className="dashboard-form" onSubmit={handleSubmit}>
        <FormField
          label="Nama acara"
          required
          value={title}
          onChange={(event) => {
            setTitle(event.target.value);
            if (!slugTouched) setSlug(slugify(event.target.value));
          }}
          placeholder="Alya & Rizky"
        />
        <FormField
          label="Alamat URL (slug)"
          required
          value={slug}
          onChange={(event) => {
            setSlug(slugify(event.target.value));
            setSlugTouched(true);
          }}
          placeholder="alya-rizky"
        />
        <p className="form-hint">rawuh.id/invitation/{slug || "nama-undangan"}</p>
        {templateId && <p className="form-hint">Template: <strong>{templateId}</strong></p>}
        {error && <p className="dashboard-state dashboard-state-error">{error}</p>}
        <div className="form-actions">
          <Button type="submit" disabled={submitting || !title || !slug} className="bg-[#173c3a] text-white">
            {submitting ? "Membuat..." : "Buat undangan"}
          </Button>
        </div>
      </form>
    </DashboardShell>
  );
}
