"use client";

import { use, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AuthHeading, AuthLayout } from "@/components/auth/AuthLayout";
import { API_URL, apiFetch, getToken } from "@/lib/api";
import { landingPath, ROLE_DESCRIPTIONS, ROLE_LABELS, type AccessRole } from "@/lib/invitation-access";

type Preview = {
  invitation: { id: string; title: string; couple?: { bride_name?: string; groom_name?: string; bride_nickname?: string; groom_nickname?: string } };
  role: Exclude<AccessRole, "owner">;
  inviter?: string;
  email?: string;
};

export default function JoinTeamPage({ params }: { params: Promise<{ token: string }> }) {
  const { token } = use(params);
  const router = useRouter();
  const [preview, setPreview] = useState<Preview | null>(null);
  const [error, setError] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);
  const [joining, setJoining] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setLoggedIn(Boolean(getToken())), 0);
    fetch(`${API_URL}/api/team-invites/${encodeURIComponent(token)}`)
      .then(async (r) => { const body = await r.json(); if (!r.ok) throw new Error(body.error); setPreview(body); })
      .catch((err) => setError(err instanceof Error && err.message ? err.message : "Link tidak bisa dibuka."));
    return () => clearTimeout(timer);
  }, [token]);

  async function join() {
    const auth = getToken();
    if (!auth) return;
    setJoining(true);
    setError("");
    try {
      const response = await apiFetch(`/api/team-invites/${encodeURIComponent(token)}/accept`, auth, { method: "POST" });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error);
      router.replace(landingPath(body.invitation_id, body.role));
    } catch (err) {
      setError(err instanceof Error && err.message ? err.message : "Belum bisa bergabung.");
      setJoining(false);
    }
  }

  const couple = preview?.invitation.couple;
  const names = couple?.bride_name && couple?.groom_name ? `${couple.bride_nickname || couple.bride_name} & ${couple.groom_nickname || couple.groom_name}` : preview?.invitation.title;
  const next = encodeURIComponent(`/gabung/${token}`);

  return (
    <AuthLayout topRight={<Link href="/dashboard">Dashboard</Link>}>
      {preview ? (
        <>
          <AuthHeading lead="Bantu undangan" mono={`${names}.`}>
            {preview.inviter ? `${preview.inviter} mengajakmu` : "Kamu diajak"} bergabung sebagai <b>{ROLE_LABELS[preview.role]}</b>. {ROLE_DESCRIPTIONS[preview.role]}
          </AuthHeading>
          {error && <div className="auth-error" role="alert">{error}</div>}
          {loggedIn ? (
            <button className="auth-submit" type="button" disabled={joining} onClick={join}>{joining ? "Bergabung…" : "Gabung ke tim"}</button>
          ) : (
            <>
              <Link className="auth-submit" href={`/auth/login?next=${next}`} style={{ display: "grid", placeItems: "center", textDecoration: "none" }}>Masuk untuk bergabung</Link>
              <p className="auth-switch">Belum punya akun? <Link href={`/auth/register?next=${next}`}>Daftar gratis</Link></p>
            </>
          )}
          {preview.email && <p className="auth-note">Undangan ini dibuat untuk {preview.email}.</p>}
        </>
      ) : error ? (
        <>
          <AuthHeading lead="Link tidak" mono="berlaku.">{error}</AuthHeading>
          <p className="auth-switch"><Link href="/dashboard">Ke dashboard</Link></p>
        </>
      ) : (
        <p className="auth-status" role="status">Memuat undangan tim…</p>
      )}
    </AuthLayout>
  );
}
