"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAdminAuth } from "@/lib/useAuthToken";

const sections = [
  { href: "/admin/hero", label: "Hero", description: "Judul dan CTA utama di home page" },
  { href: "/admin/features", label: "Fitur", description: "Daftar fitur yang ditampilkan" },
  { href: "/admin/testimonials", label: "Testimonials", description: "Ulasan dari pengguna" },
  { href: "/admin/kontak", label: "Kontak", description: "Banner kontak/WhatsApp" },
  { href: "/admin/footer", label: "Footer", description: "Bagian paling bawah home page" },
];

export default function AdminOverviewPage() {
  const { token, ready } = useAdminAuth();
  const [counts, setCounts] = useState<{ features: number; testimonials: number } | null>(null);

  useEffect(() => {
    if (!ready || !token) return;
    Promise.all([
      apiFetch("/api/admin/features", token).then((r) => r.json()),
      apiFetch("/api/admin/testimonials", token).then((r) => r.json()),
    ]).then(([features, testimonials]) => {
      setCounts({ features: features.items?.length ?? 0, testimonials: testimonials.items?.length ?? 0 });
    });
  }, [ready, token]);

  if (!ready || !token) return null;

  return (
    <DashboardShell active="overview" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Admin</p>
          <h1>Landing page content</h1>
          <p className="dashboard-subtitle">Kelola konten yang tampil di home page publik.</p>
        </div>
      </header>

      {counts && (
        <div className="dashboard-summary">
          <div className="dashboard-stat">
            <span>Fitur</span>
            <strong>{counts.features}</strong>
          </div>
          <div className="dashboard-stat">
            <span>Testimonials</span>
            <strong>{counts.testimonials}</strong>
          </div>
        </div>
      )}

      <div className="card-grid">
        {sections.map((section) => (
          <Link key={section.href} href={section.href} className="dashboard-card">
            <h3>{section.label}</h3>
            <p style={{ margin: 0, color: "#6e786f", fontSize: ".85rem" }}>{section.description}</p>
          </Link>
        ))}
      </div>
    </DashboardShell>
  );
}
