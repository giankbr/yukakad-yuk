"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { FormField } from "@/components/dashboard/FormField";
import { Button } from "@/components/ui/button";
import { themeList } from "@/components/invitation/themes/list";
import { apiFetch } from "@/lib/api";
import { friendlyError } from "@/lib/errors";
import { useAuthToken } from "@/lib/useAuthToken";

function slugify(value: string) {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function themeName(id: string) {
  return themeList.find((theme) => theme.id === id)?.name ?? id;
}

/** Shown instead of redirecting when the invitation was created but the chosen theme could not be applied. */
type TemplateNotice = { invitationId: string; templateName: string; premium: boolean };

function CreateInvitationForm({ token }: { token: string }) {
  const router = useRouter();
  const search = useSearchParams();
  // Prefilled from the landing page "Nama acaramu" field (?event=, forwarded through registration as ?title=).
  const initialTitle = (search.get("title") ?? search.get("event") ?? "").trim();
  // Set by "Pakai tema" on /dashboard/templates or the landing page.
  const templateId = search.get("template")?.trim() || null;
  const [title, setTitle] = useState(initialTitle);
  const [slug, setSlug] = useState(() => slugify(initialTitle));
  const [slugTouched, setSlugTouched] = useState(false);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [notice, setNotice] = useState<TemplateNotice | null>(null);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      const base = slug || slugify(title);
      const create = (value: string) => apiFetch("/api/invitations", token, {
        method: "POST",
        body: JSON.stringify({ title: title.trim(), slug: value }),
      });
      let response = await create(base);
      let body = await response.json().catch(() => ({}));
      // A slug we derived from the title is already taken: try a short random suffix instead of bothering the user.
      if (response.status === 409 && body.code === "slug_taken" && !slugTouched) {
        const next = `${base.slice(0, 70)}-${randomSuffix()}`;
        response = await create(next);
        body = await response.json().catch(() => ({}));
        if (response.ok) setSlug(next);
      }
      if (!response.ok) throw new Error(friendlyError(body.error, "Gagal membuat undangan"));
      if (templateId) {
        // The invitation exists already; a theme that can't be applied must not fail creation, but the user must know.
        const applied = await apiFetch(`/api/invitations/${body.id}/template`, token, {
          method: "PUT",
          body: JSON.stringify({ template_id: templateId }),
        }).catch(() => null);
        if (!applied?.ok) {
          setNotice({ invitationId: body.id, templateName: themeName(templateId), premium: applied?.status === 403 });
          return;
        }
      }
      router.push(`/dashboard/invitations/${body.id}`);
    } catch (err) {
      setError(friendlyError(err instanceof Error ? err.message : ""));
      setSubmitting(false);
    }
  }

  if (notice) {
    return (
      <div className="dashboard-form" role="status">
        <p className="dashboard-state" style={{ margin: 0 }}>
          {notice.premium
            ? <>Tema <strong>{notice.templateName}</strong> butuh paket berbayar — undanganmu dibuat dengan tema Linen Putih. Upgrade paket untuk memakainya.</>
            : <>Tema <strong>{notice.templateName}</strong> belum bisa dipasang — undanganmu dibuat dengan tema Linen Putih. Kamu bisa memilih tema lagi di menu Tema &amp; Musik.</>}
        </p>
        <div className="form-actions">
          <Link className="secondary-action" href={`/dashboard/invitations/${notice.invitationId}`}>Lanjut ke undangan</Link>
          {notice.premium && <Link className="secondary-action" href="/dashboard/paket">Upgrade paket</Link>}
        </div>
      </div>
    );
  }

  return (
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
      {templateId && <p className="form-hint">Tema: <strong>{themeName(templateId)}</strong></p>}
      {error && <p className="dashboard-state dashboard-state-error" role="alert">{error}</p>}
      <div className="form-actions">
        <Button type="submit" disabled={submitting || !title.trim() || !slug}>
          {submitting ? "Membuat..." : "Buat undangan"}
        </Button>
      </div>
    </form>
  );
}

/** Short random suffix for a taken slug (module scope: only called from the submit handler). */
function randomSuffix() {
  return Math.random().toString(36).slice(2, 6);
}

export default function CreateInvitationPage() {
  const { token, ready } = useAuthToken();
  if (!ready || !token) return null;

  return (
    <DashboardShell active="invitations">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Akun</p>
          <h1>Buat undangan</h1>
          <p className="dashboard-subtitle">Kasih judul dulu. Detail lainnya bisa dilengkapi nanti.</p>
        </div>
      </header>
      {/* useSearchParams needs a Suspense boundary so the route can still be prerendered. */}
      <Suspense fallback={<p className="dashboard-state">Memuat...</p>}>
        <CreateInvitationForm token={token} />
      </Suspense>
    </DashboardShell>
  );
}
