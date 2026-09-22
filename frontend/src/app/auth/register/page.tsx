"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function RegisterPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080"}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || "Registration failed");
      }

      const data = await response.json();
      localStorage.setItem("yukakad_token", data.token);
      localStorage.setItem("yukakad_role", data.user?.role ?? "user");
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <div className="auth-aside"><Link href="/" className="auth-brand"><span>y</span> yukakad.</Link><p>Undangan yang terasa seperti kalian.</p><small>Mulai dari template. Selesai dengan cerita.</small></div>
      <div className="auth-panel">
        <div className="auth-heading">
          <p className="auth-kicker">Mulai dalam beberapa menit</p>
          <h1>Buat undangan yang ingin dibagikan.</h1>
          <p>Akun gratis, tanpa kartu kredit.</p>
        </div>
        
        <form onSubmit={handleSubmit} className="auth-form">
          <div>
            <label>Nama lengkap</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              placeholder="Nama kamu"
            />
          </div>

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
              placeholder="Minimal 8 karakter"
            />
          </div>

          {error && <div className="auth-error">{error}</div>}

          <button
            type="submit"
            disabled={loading}
            className="auth-submit"
          >
            {loading ? "Membuat akun..." : "Buat akun gratis →"}
          </button>
        </form>

        <p className="auth-switch">
          Sudah punya akun? <a href="/auth/login">Masuk di sini</a>
        </p>
      </div>
    </main>
  );
}
