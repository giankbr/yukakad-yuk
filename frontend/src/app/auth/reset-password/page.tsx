"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { AuthHeading, AuthLayout } from "@/components/auth/AuthLayout";
import { IconEye, IconEyeOff } from "@/components/brand/icons";
import { API_URL } from "@/lib/api";
import { friendlyError } from "@/lib/errors";

function ResetPasswordForm() {
  const token = useSearchParams().get("token") ?? "";
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError("");
    if (password.length < 8) { setError("Kata sandi baru minimal 8 karakter."); return; }
    if (password !== confirm) { setError("Konfirmasi kata sandi tidak sama."); return; }
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/auth/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, password }),
      });
      const data = (await response.json().catch(() => ({}))) as { error?: string };
      if (!response.ok) throw new Error(friendlyError(data.error, "Kata sandi belum diganti. Coba lagi."));
      setDone(true);
    } catch (err) {
      setError(friendlyError(err instanceof Error ? err.message : ""));
    } finally {
      setLoading(false);
    }
  }

  if (!token) {
    return (
      <div className="auth-form">
        <div className="auth-error" role="alert">Link reset tidak lengkap atau sudah tidak berlaku.</div>
        <Link href="/auth/forgot-password" className="auth-submit" style={{ display: "grid", placeItems: "center", textDecoration: "none" }}>Minta link baru</Link>
      </div>
    );
  }

  if (done) {
    return (
      <div className="auth-form">
        <p className="auth-status" role="status">Kata sandi baru tersimpan. Silakan masuk dengan kata sandi barumu.</p>
        <Link href="/auth/login" className="auth-submit" style={{ display: "grid", placeItems: "center", textDecoration: "none" }}>Masuk</Link>
      </div>
    );
  }

  const toggle = (
    <button type="button" onClick={() => setShowPassword((value) => !value)} aria-label={showPassword ? "Sembunyikan kata sandi" : "Tampilkan kata sandi"} aria-pressed={showPassword}>
      {showPassword ? <IconEyeOff size={18} /> : <IconEye size={18} />}
    </button>
  );

  return (
    <form onSubmit={handleSubmit} className="auth-form">
      <div>
        <label htmlFor="reset-password">Kata sandi baru</label>
        <div className="auth-input">
          <input id="reset-password" autoComplete="new-password" minLength={8} type={showPassword ? "text" : "password"} value={password}
            onChange={(e) => setPassword(e.target.value)} required placeholder="Minimal 8 karakter" />
          {toggle}
        </div>
      </div>
      <div>
        <label htmlFor="reset-confirm">Ulangi kata sandi baru</label>
        <input id="reset-confirm" autoComplete="new-password" minLength={8} type={showPassword ? "text" : "password"} value={confirm}
          onChange={(e) => setConfirm(e.target.value)} required placeholder="Ketik ulang kata sandi baru" />
      </div>

      {error && (
        <div className="auth-error" role="alert">
          {error}
          {/kedaluwarsa|tidak berlaku/.test(error) && <> <Link href="/auth/forgot-password" style={{ color: "inherit", textDecoration: "underline" }}>Minta link baru</Link></>}
        </div>
      )}

      <button type="submit" disabled={loading} className="auth-submit">
        {loading ? "Menyimpan..." : "Simpan kata sandi baru"}
      </button>
    </form>
  );
}

export default function ResetPasswordPage() {
  return (
    <AuthLayout topRight={<>Ingat kata sandinya? <Link href="/auth/login">Masuk</Link></>}>
      <AuthHeading lead="Buat kata sandi" mono="baru.">Setelah tersimpan, semua sesi lama akan keluar otomatis.</AuthHeading>
      <Suspense fallback={<p className="auth-status">Memuat...</p>}>
        <ResetPasswordForm />
      </Suspense>
    </AuthLayout>
  );
}
