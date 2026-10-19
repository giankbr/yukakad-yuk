"use client";

import { useState } from "react";
import Link from "next/link";
import { AuthHeading, AuthLayout } from "@/components/auth/AuthLayout";
import { IconMail } from "@/components/brand/icons";
import { API_URL } from "@/lib/api";
import { friendlyError } from "@/lib/errors";

type Result = { kind: "sent" } | { kind: "unavailable"; waLink: string | null };

/** Same contact the marketing pages use: the admin-managed WhatsApp number from site content "kontak". */
async function whatsappLink(): Promise<string | null> {
  try {
    const response = await fetch(`${API_URL}/api/public/site-content/kontak`);
    if (!response.ok) return null;
    const kontak = (await response.json()) as { whatsapp?: string };
    const digits = kontak.whatsapp?.replace(/[^0-9]/g, "");
    if (!digits) return null;
    return `https://wa.me/${digits}?text=${encodeURIComponent("Halo admin Rawuh, saya lupa kata sandi akun saya.")}`;
  } catch {
    return null;
  }
}

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<Result | null>(null);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/auth/forgot-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim() }),
      });
      const data = (await response.json().catch(() => ({}))) as { error?: string; code?: string };
      if (response.ok) {
        setResult({ kind: "sent" });
      } else if (response.status === 503 && data.code === "reset_unavailable") {
        setResult({ kind: "unavailable", waLink: await whatsappLink() });
      } else {
        throw new Error(friendlyError(data.error, "Permintaan reset belum terkirim. Coba lagi."));
      }
    } catch (err) {
      setError(friendlyError(err instanceof Error ? err.message : ""));
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthLayout topRight={<>Ingat kata sandinya? <Link href="/auth/login">Masuk</Link></>}>
      <AuthHeading lead="Lupa kata" mono="sandi?">Masukkan email akunmu. Kami kirim link untuk membuat kata sandi baru.</AuthHeading>

      <form onSubmit={handleSubmit} className="auth-form">
        <div>
          <label htmlFor="forgot-email">Email</label>
          <div className="auth-input">
            <input id="forgot-email" autoComplete="email" type="email" value={email}
              onChange={(e) => setEmail(e.target.value)} required placeholder="nama@email.com" />
            <IconMail size={18} />
          </div>
        </div>

        {error && <div className="auth-error" role="alert">{error}</div>}
        {result?.kind === "sent" && (
          <p className="auth-status" role="status">Kalau emailnya terdaftar, link reset sudah kami kirim. Cek juga folder spam.</p>
        )}
        {result?.kind === "unavailable" && (
          <div className="auth-error" role="alert">
            Reset lewat email belum aktif. Hubungi admin Rawuh lewat{" "}
            {result.waLink
              ? <a href={result.waLink} target="_blank" rel="noreferrer" style={{ color: "inherit", textDecoration: "underline" }}>WhatsApp</a>
              : <Link href="/tentang#kontak" style={{ color: "inherit", textDecoration: "underline" }}>WhatsApp</Link>}.
          </div>
        )}

        <button type="submit" disabled={loading} className="auth-submit">
          {loading ? "Mengirim..." : "Kirim link reset"}
        </button>
        <p className="auth-note"><Link href="/auth/login">Kembali ke halaman masuk</Link></p>
      </form>
    </AuthLayout>
  );
}
