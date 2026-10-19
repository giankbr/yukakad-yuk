"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { AuthHeading, AuthLayout } from "@/components/auth/AuthLayout";
import { safeNext } from "@/lib/next-path";
import { API_URL, saveSession } from "@/lib/api";
import { friendlyError } from "@/lib/errors";
import { IconEye, IconEyeOff } from "@/components/brand/icons";

export default function RegisterPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await response.json().catch(() => ({}));
      if (!response.ok || !data.token) throw new Error(friendlyError(data.error, "Pendaftaran gagal. Coba lagi."));

      saveSession(data.token, data.user);
      const search = new URLSearchParams(window.location.search);
      const planId = search.get("plan");
      const templateId = search.get("template");
      const eventName = search.get("event")?.trim();
      const next = safeNext(search.get("next"));
      router.push(next ?? (planId
        ? `/checkout?plan=${encodeURIComponent(planId)}`
        : templateId
          ? `/dashboard/invitations/create?template=${encodeURIComponent(templateId)}${eventName ? `&title=${encodeURIComponent(eventName)}` : ""}`
          : eventName
            ? `/dashboard/invitations/create?title=${encodeURIComponent(eventName)}`
            : "/dashboard"));
    } catch (err) {
      setError(friendlyError(err instanceof Error ? err.message : ""));
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout topRight={<>Sudah punya akun? <Link href="/auth/login" onClick={(event) => {
      const next = safeNext(new URLSearchParams(window.location.search).get("next"));
      if (!next) return;
      event.preventDefault();
      router.push(`/auth/login?next=${encodeURIComponent(next)}`);
    }}>Masuk</Link></>}>
      <AuthHeading lead="Buat undangan" mono="pertamamu.">Gratis untuk mencoba — bayar hanya saat undangan siap dikirim.</AuthHeading>

      <form onSubmit={handleSubmit} className="auth-form">
        <div>
          <label htmlFor="register-name">Nama lengkap</label>
          <input id="register-name" autoComplete="name" type="text" value={name}
            onChange={(e) => setName(e.target.value)} required placeholder="Nama kamu" />
        </div>

        <div>
          <label htmlFor="register-email">Email</label>
          <input id="register-email" autoComplete="email" type="email" value={email}
            onChange={(e) => setEmail(e.target.value)} required placeholder="nama@email.com" />
        </div>

        <div>
          <label htmlFor="register-password">Kata sandi</label>
          <div className="auth-input">
            <input id="register-password" autoComplete="new-password" minLength={8} type={showPassword ? "text" : "password"} value={password}
              onChange={(e) => setPassword(e.target.value)} required placeholder="Minimal 8 karakter" />
            <button type="button" onClick={() => setShowPassword(value => !value)} aria-label={showPassword ? "Sembunyikan kata sandi" : "Tampilkan kata sandi"} aria-pressed={showPassword}>
              {showPassword ? <IconEyeOff size={18} /> : <IconEye size={18} />}
            </button>
          </div>
        </div>

        {error && <div className="auth-error" role="alert">{error}</div>}

        <button type="submit" disabled={loading} className="auth-submit">
          {loading ? "Membuat akun..." : "Buat akun gratis"}
        </button>
        <p className="auth-note">Dengan mendaftar, kamu menyetujui <Link href="/syarat-ketentuan">Syarat &amp; Ketentuan</Link> dan <Link href="/kebijakan-privasi">Kebijakan Privasi</Link> Rawuh.</p>
      </form>
    </AuthLayout>
  );
}
