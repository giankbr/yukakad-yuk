"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { AuthHeading, AuthLayout } from "@/components/auth/AuthLayout";
import { IconEye, IconEyeOff, IconMail } from "@/components/brand/icons";
import { safeNext } from "@/lib/next-path";

export default function LoginPage() {
  const router = useRouter();
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
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080"}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || "Login gagal");
      }

      const data = await response.json();
      // Storage keys keep the legacy prefix so existing sessions stay signed in.
      localStorage.setItem("yukakad_token", data.token);
      localStorage.setItem("yukakad_role", data.user?.role ?? "user");
      const search = new URLSearchParams(window.location.search);
      const planId = search.get("plan");
      const next = safeNext(search.get("next"));
      router.push(next ?? (data.user?.role === "admin" ? "/admin" : planId
        ? `/checkout?plan=${encodeURIComponent(planId)}`
        : "/dashboard"));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Terjadi kesalahan");
    } finally {
      setLoading(false);
    }
  };

  const registerLink = <Link href="/auth/register" onClick={(event) => {
    const search = new URLSearchParams(window.location.search);
    const planId = search.get("plan");
    const next = safeNext(search.get("next"));
    if (!planId && !next) return;
    event.preventDefault();
    router.push(next ? `/auth/register?next=${encodeURIComponent(next)}` : `/auth/register?plan=${encodeURIComponent(planId!)}`);
  }}>Daftar gratis</Link>;

  return (
    <AuthLayout topRight={<>Belum punya akun? {registerLink}</>}>
      <AuthHeading lead="Selamat datang" mono="kembali.">Lanjutkan undanganmu — draft tersimpan otomatis.</AuthHeading>

      <form onSubmit={handleSubmit} className="auth-form">
        <div>
          <label htmlFor="login-email">Email</label>
          <div className="auth-input">
            <input id="login-email" autoComplete="email" type="email" value={email}
              onChange={(e) => setEmail(e.target.value)} required placeholder="nama@email.com" />
            <IconMail size={18} />
          </div>
        </div>

        <div>
          <label htmlFor="login-password">Kata sandi</label>
          <div className="auth-input">
            <input id="login-password" autoComplete="current-password" type={showPassword ? "text" : "password"} value={password}
              onChange={(e) => setPassword(e.target.value)} required placeholder="Masukkan kata sandi" />
            <button type="button" onClick={() => setShowPassword(value => !value)} aria-label={showPassword ? "Sembunyikan kata sandi" : "Tampilkan kata sandi"} aria-pressed={showPassword}>
              {showPassword ? <IconEyeOff size={18} /> : <IconEye size={18} />}
            </button>
          </div>
        </div>

        {error && <div className="auth-error" role="alert">{error}</div>}

        <button type="submit" disabled={loading} className="auth-submit">
          {loading ? "Memproses..." : "Masuk"}
        </button>
      </form>
    </AuthLayout>
  );
}
