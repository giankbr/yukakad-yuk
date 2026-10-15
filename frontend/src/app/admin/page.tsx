"use client";

import Link from "next/link";
import { useEffect, useState, type ReactNode } from "react";
import {
  ArrowRight as PhArrowRight, ArrowSquareOut as PhArrowSquareOut, Article as PhArticle, Browser as PhBrowser,
  ChatCircleText as PhChatCircleText, Megaphone as PhMegaphone, Palette as PhPalette, Phone as PhPhone, Star as PhStar, Tag as PhTag, Users as PhUsers,
} from "@phosphor-icons/react/ssr";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAdminAuth } from "@/lib/useAuthToken";
import styles from "./admin.module.css";

type Status = "filled" | "empty" | "unknown";
type Section = { key: string; href: string; label: string; description: string; icon: ReactNode };

const sections: Section[] = [
  { key: "hero", href: "/admin/hero", label: "Hero", description: "Judul, subjudul, dan tombol utama di bagian atas home page.", icon: <PhBrowser size={20} /> },
  { key: "features", href: "/admin/features", label: "Fitur", description: "Kartu fitur tambahan di bawah bento fitur.", icon: <PhStar size={20} /> },
  { key: "testimonials", href: "/admin/testimonials", label: "Testimoni", description: "Ulasan pengguna di bagian “Kata mereka”.", icon: <PhChatCircleText size={20} /> },
  { key: "kontak", href: "/admin/kontak", label: "Kontak", description: "Nomor WhatsApp untuk tombol chat admin.", icon: <PhPhone size={20} /> },
  { key: "footer", href: "/admin/footer", label: "Footer", description: "Hak cipta serta akun Instagram & TikTok.", icon: <PhArticle size={20} /> },
  { key: "landing", href: "/admin/landing", label: "Statistik, FAQ & pengumuman", description: "Angka di bawah hero, daftar FAQ, dan bar pengumuman.", icon: <PhMegaphone size={20} /> },
];

const business: Section[] = [
  { key: "plans", href: "/admin/plans", label: "Paket & harga", description: "Harga, kuota tamu, masa aktif, dan fitur tiap paket.", icon: <PhTag size={20} /> },
  { key: "templates", href: "/admin/templates", label: "Tema", description: "Aktif/nonaktif, kategori, dan akses Premium tiap tema.", icon: <PhPalette size={20} /> },
  { key: "users", href: "/admin/users", label: "Pengguna", description: "Ubah paket atau peran akun secara manual.", icon: <PhUsers size={20} /> },
];

type Platform = { total_users?: number; total_invitations?: number; published_invitations?: number; total_guests?: number; total_rsvps?: number };

const hasValue = (value: unknown) => Boolean(value) && typeof value === "object" && Object.values(value as Record<string, unknown>).some(v => typeof v === "string" ? v.trim() : v);

export default function AdminOverviewPage() {
  const { token, ready } = useAdminAuth();
  const [counts, setCounts] = useState<{ features: number; testimonials: number } | null>(null);
  const [status, setStatus] = useState<Record<string, Status>>({});
  const [platform, setPlatform] = useState<Platform | null>(null);

  useEffect(() => {
    if (!ready || !token) return;
    const json = (path: string) => apiFetch(path, token).then(r => (r.ok ? r.json() : null)).catch(() => null);
    Promise.all([
      json("/api/admin/features"), json("/api/admin/testimonials"),
      json("/api/admin/site-content/hero"), json("/api/admin/site-content/kontak"), json("/api/admin/site-content/footer"),
      json("/api/admin/site-content/stats"), json("/api/admin/site-content/faq"), json("/api/admin/stats"),
    ]).then(([features, testimonials, hero, kontak, footer, landingStats, faq, stats]) => {
      setPlatform(stats);
      const featureCount = features?.items?.length ?? 0;
      const testimonialCount = testimonials?.items?.length ?? 0;
      setCounts({ features: featureCount, testimonials: testimonialCount });
      const state = (value: unknown): Status => (value === null ? "unknown" : hasValue(value) ? "filled" : "empty");
      setStatus({
        hero: state(hero), kontak: state(kontak), footer: state(footer),
        landing: landingStats === null && faq === null ? "unknown" : landingStats?.items?.length || faq?.items?.length ? "filled" : "empty",
        features: features ? (featureCount ? "filled" : "empty") : "unknown",
        testimonials: testimonials ? (testimonialCount ? "filled" : "empty") : "unknown",
      });
    });
  }, [ready, token]);

  if (!ready || !token) return null;

  const filled = Object.values(status).filter(value => value === "filled").length;
  const detail: Record<string, string> = {
    features: counts ? `${counts.features} fitur` : "",
    testimonials: counts ? `${counts.testimonials} testimoni` : "",
  };

  return (
    <DashboardShell active="overview" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Admin</p>
          <h1>Ringkasan admin</h1>
          <p className="dashboard-subtitle">Konten landing page, paket, tema, dan pengguna Rawuh.</p>
        </div>
        <a className="dashboard-action" href="/" target="_blank" rel="noreferrer">Lihat landing page <PhArrowSquareOut size={16} /></a>
      </header>

      <div className={styles.stats}>
        <div className={styles.stat}>
          <span>Bagian terisi</span>
          <strong>{counts ? `${filled}/${sections.length}` : "—"}</strong>
          <div className={styles.meter} aria-hidden><i style={{ width: `${(filled / sections.length) * 100}%` }} /></div>
        </div>
        <Link href="/admin/features" className={styles.stat}>
          <span>Fitur tambahan</span>
          <strong>{counts?.features ?? "—"}</strong>
          <small>Kelola fitur <PhArrowRight size={12} /></small>
        </Link>
        <Link href="/admin/testimonials" className={styles.stat}>
          <span>Testimoni</span>
          <strong>{counts?.testimonials ?? "—"}</strong>
          <small>Kelola testimoni <PhArrowRight size={12} /></small>
        </Link>
      </div>

      {platform && (
        <>
          <h2 className={styles.heading}>Platform</h2>
          <div className={styles.stats}>
            <Link href="/admin/users" className={styles.stat}><span>Pengguna</span><strong>{(platform.total_users ?? 0).toLocaleString("id-ID")}</strong><small>Kelola pengguna <PhArrowRight size={12} /></small></Link>
            <div className={styles.stat}><span>Undangan</span><strong>{(platform.total_invitations ?? 0).toLocaleString("id-ID")}</strong><small>{(platform.published_invitations ?? 0).toLocaleString("id-ID")} sudah terbit</small></div>
            <div className={styles.stat}><span>Tamu</span><strong>{(platform.total_guests ?? 0).toLocaleString("id-ID")}</strong><small>{(platform.total_rsvps ?? 0).toLocaleString("id-ID")} RSVP masuk</small></div>
          </div>
        </>
      )}

      <h2 className={styles.heading}>Bagian home page</h2>
      <div className={styles.grid}>
        {sections.map(section => {
          const state = status[section.key] ?? "unknown";
          return (
            <Link key={section.href} href={section.href} className={styles.card}>
              <span className={styles.icon}>{section.icon}</span>
              <div className={styles.cardText}>
                <div className={styles.cardTop}>
                  <h3>{section.label}</h3>
                  {state !== "unknown" && (
                    <span className={styles.badge} data-state={state}>
                      {state === "filled" ? detail[section.key] || "Terisi" : "Belum diisi"}
                    </span>
                  )}
                </div>
                <p>{section.description}</p>
              </div>
              <PhArrowRight className={styles.arrow} size={16} />
            </Link>
          );
        })}
      </div>

      <h2 className={styles.heading}>Bisnis</h2>
      <div className={styles.grid}>
        {business.map(section => (
          <Link key={section.href} href={section.href} className={styles.card}>
            <span className={styles.icon}>{section.icon}</span>
            <div className={styles.cardText}>
              <div className={styles.cardTop}><h3>{section.label}</h3></div>
              <p>{section.description}</p>
            </div>
            <PhArrowRight className={styles.arrow} size={16} />
          </Link>
        ))}
      </div>
    </DashboardShell>
  );
}
