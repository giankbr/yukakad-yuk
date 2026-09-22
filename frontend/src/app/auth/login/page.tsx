"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
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
        throw new Error(data.error || "Login failed");
      }

      const data = await response.json();
      localStorage.setItem("yukakad_token", data.token);
      localStorage.setItem("yukakad_role", data.user?.role ?? "user");
      router.push(data.user?.role === "admin" ? "/admin" : "/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <div className="auth-aside"><Link href="/" className="auth-brand"><span>y</span> yukakad.</Link><p>Undangan yang terasa seperti kalian.</p><small>Bagikan cerita. Rayakan bersama.</small></div>
      <div className="auth-panel">
        <div className="auth-heading">
          <p className="auth-kicker">Selamat datang kembali</p>
          <h1>Masuk ke workspace kamu.</h1>
          <p>Kelola undangan dan tamu dari satu tempat.</p>
        </div>
        
        <form onSubmit={handleSubmit} className="auth-form">
          <div>
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="nama@email.com"
            />
          </div>

          <div>
            <label>Kata sandi</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Masukkan kata sandi"
            />
          </div>

          {error && <div className="auth-error">{error}</div>}

          <button
            type="submit"
            disabled={loading}
            className="auth-submit"
          >
            {loading ? "Memproses..." : "Masuk"}
          </button>
        </form>

        <p className="auth-switch">
          Belum punya akun? <a href="/auth/register">Buat akun gratis</a>
        </p>
      </div>
    </main>
  );
}
