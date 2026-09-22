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
  const [title, setTitle] = useState("");
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
      if (!response.ok) throw new Error(body.error ?? "Could not create invitation");
      if (templateId) {
        // Non-blocking: the template can still be picked later from the invitation settings.
        await apiFetch(`/api/invitations/${body.id}/template`, token, { method: "PUT", body: JSON.stringify({ template_id: templateId }) }).catch(() => undefined);
      }
      router.push(`/dashboard/invitations/${body.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setSubmitting(false);
    }
  }

  return (
    <DashboardShell active="invitations">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Workspace</p>
          <h1>Create an invitation</h1>
          <p className="dashboard-subtitle">Give it a title. Everything else can be filled in later.</p>
        </div>
      </header>

      <form className="dashboard-form" onSubmit={handleSubmit}>
        <FormField
          label="Event title"
          required
          value={title}
          onChange={(event) => {
            setTitle(event.target.value);
            if (!slugTouched) setSlug(slugify(event.target.value));
          }}
          placeholder="Alya & Rizky"
        />
        <FormField
          label="URL slug"
          required
          value={slug}
          onChange={(event) => {
            setSlug(slugify(event.target.value));
            setSlugTouched(true);
          }}
          placeholder="alya-rizky"
        />
        <p className="form-hint">yukakad.com/invitation/{slug || "your-slug"}</p>
        {templateId && <p className="form-hint">Template: <strong>{templateId}</strong></p>}
        {error && <p className="dashboard-state dashboard-state-error">{error}</p>}
        <div className="form-actions">
          <Button type="submit" disabled={submitting || !title || !slug} className="bg-[#173c3a] text-white">
            {submitting ? "Creating..." : "Create invitation"}
          </Button>
        </div>
      </form>
    </DashboardShell>
  );
}
