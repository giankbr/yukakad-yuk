"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight as PhArrowRight, Bell as PhBell, CheckSquare as PhCheckSquare, EnvelopeSimple as PhEnvelopeSimple, Globe as PhGlobe, Palette as PhPalette, Plus as PhPlus, Users as PhUsers } from "@phosphor-icons/react/ssr";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken } from "@/lib/useAuthToken";

/* ── Types ──────────────────────────────────────────────────────── */
type Invitation = {
	id: string;
	title: string;
	slug: string;
	published: boolean;
	created_at: string;
	couple?: { groom_name: string; bride_name: string };
};

/* ── Components ─────────────────────────────────────────────────── */
function StatCard({
	label,
	value,
	icon,
	badge,
	delta,
}: {
	label: string;
	value: number | string;
	icon: React.ReactNode;
	badge?: { text: string; positive: boolean };
	delta?: string;
}) {
	return (
		<div className="db-stat-card">
			<div className="db-stat-header">
				<div>
					<p className="db-stat-label">{label}</p>
					<div className="db-stat-num-row">
						<h2 className="db-stat-value">{value}</h2>
						{badge && (
							<span
								className={badge.positive ? "db-badge-pos" : "db-badge-neg"}
							>
								{badge.positive ? "↑" : "↓"} {badge.text}
							</span>
						)}
					</div>
				</div>
				<div className="db-stat-icon-box">{icon}</div>
			</div>
			{delta && (
				<p className="db-stat-delta">
					{delta}&nbsp;
					<PhArrowRight size={12} />
				</p>
			)}
		</div>
	);
}

/* ── Page ────────────────────────────────────────────────────────── */
export default function DashboardPage() {
	const { token, ready } = useAuthToken();
	const [invitations, setInvitations] = useState<Invitation[]>([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState("");
	const [userName] = useState(() =>
		typeof window === "undefined"
			? "Pengguna"
			: window.localStorage.getItem("yukakad_name") ?? "Pengguna",
	);

	useEffect(() => {
		if (!ready || !token) return;
		apiFetch("/api/invitations", token)
			.then((r) => (r.ok ? r.json() : Promise.reject("Gagal memuat data.")))
			.then((body: { items?: Invitation[] }) =>
				setInvitations(body.items ?? []),
			)
			.catch((e: unknown) => setError(String(e)))
			.finally(() => setLoading(false));
	}, [ready, token]);

	if (!ready) return null;

	const published = invitations.filter((i) => i.published);
	const draft = invitations.filter((i) => !i.published);
	const publishRate =
		invitations.length > 0
			? Math.round((published.length / invitations.length) * 100)
			: 0;

	/* greeting based on time of day */
	const hour = new Date().getHours();
	const greeting =
		hour < 12 ? "Selamat pagi" : hour < 17 ? "Selamat siang" : "Selamat malam";

	return (
		<DashboardShell active="overview">
			{/* ── Topbar ──────────────────────────────────────────────── */}
			<div className="db-topbar">
				<div className="db-topbar-left">
					<h1>Dashboard</h1>
					<p>
						{greeting}, {userName} 👋
					</p>
				</div>
				<div className="db-topbar-actions">
					<button className="db-icon-btn" aria-label="Notifikasi">
						<PhBell size={17} />
					</button>
					<Link href="/dashboard/invitations/create" className="db-primary-btn">
						<PhPlus size={14} /> Buat Undangan
					</Link>
				</div>
			</div>

			{/* ── Inner content ───────────────────────────────────────── */}
			<div className="db-inner">
				{/* Stats row */}
				<div className="db-stat-grid">
					<StatCard
						label="Total Undangan"
						value={invitations.length}
						icon={<PhEnvelopeSimple size={18} />}
						delta="Semua undangan Anda"
					/>
					<StatCard
						label="Terpublikasi"
						value={published.length}
						icon={<PhGlobe size={18} />}
						badge={
							invitations.length > 0
								? { text: `${publishRate}%`, positive: true }
								: undefined
						}
						delta="Sudah dibagikan ke tamu"
					/>
					<StatCard
						label="Dalam Proses"
						value={draft.length}
						icon={<PhUsers size={18} />}
						badge={
							draft.length > 0 ? { text: "Draf", positive: false } : undefined
						}
						delta="Belum dipublikasikan"
					/>
					<StatCard
						label="Acara Aktif"
						value={published.length}
						icon={<PhCheckSquare size={18} />}
						delta="Sedang berlangsung"
					/>
				</div>

				{/* Content grid: table + side panel */}
				<div className="db-content-grid">
					{/* ── Invitation table ──────────────────────────────── */}
					<div className="db-card">
						<div className="db-card-header">
							<h2 className="db-card-title">Undangan Terbaru</h2>
							<Link href="/dashboard/invitations" className="db-card-action">
								Lihat semua →
							</Link>
						</div>

						{loading && (
							<div className="db-empty">
								<span style={{ opacity: 0.6 }}>Memuat undangan...</span>
							</div>
						)}

						{error && (
							<div className="db-empty" style={{ color: "#D63244" }}>
								{error}
							</div>
						)}

						{!loading && !error && invitations.length === 0 && (
							<div className="db-empty">
								<p style={{ margin: 0 }}>
									Belum ada undangan. Buat undangan pertama Anda sekarang.
								</p>
								<Link
									href="/dashboard/invitations/create"
									className="db-primary-btn"
									style={{ width: "fit-content" }}
								>
									<PhPlus size={14} /> Buat Undangan
								</Link>
							</div>
						)}

						{!loading && !error && invitations.length > 0 && (
							<table className="db-table">
								<thead>
									<tr>
										<th>Undangan</th>
										<th>Status</th>
										<th>Mempelai</th>
										<th>
											<span className="sr-only">Aksi</span>
										</th>
									</tr>
								</thead>
								<tbody>
									{invitations.slice(0, 7).map((inv) => (
										<tr key={inv.id}>
											<td>
												{inv.title}
												<small
													style={{
														display: "block",
														fontWeight: 400,
														color: "#8CAEA8",
														fontSize: ".72rem",
														marginTop: ".12rem",
													}}
												>
													rawuh.id/{inv.slug}
												</small>
											</td>
											<td>
												<span
													className={
														inv.published ? "db-status-pub" : "db-status-draft"
													}
												>
													{inv.published ? "● Publik" : "○ Draf"}
												</span>
											</td>
											<td style={{ color: "#8CAEA8", fontSize: ".81rem" }}>
												{inv.couple?.groom_name && inv.couple?.bride_name ? (
													`${inv.couple.groom_name} & ${inv.couple.bride_name}`
												) : (
													<span style={{ opacity: 0.45 }}>—</span>
												)}
											</td>
											<td>
												<Link
													href={`/dashboard/invitations/${inv.id}`}
													className="db-table-action"
												>
													Kelola →
												</Link>
											</td>
										</tr>
									))}
								</tbody>
							</table>
						)}
					</div>

					{/* ── Side panel ────────────────────────────────────── */}
					<div className="db-side-panel">
						{/* Upgrade card */}
						<div className="db-upgrade-card">
							<span className="db-upgrade-tag">✦ Pro</span>
							<h3>Tingkatkan ke Pro</h3>
							<p>
								Hapus watermark, custom domain, hingga 1.000 tamu, dan tema
								Premium seperti Jawa Keraton & Marketplace.
							</p>
							<Link className="db-upgrade-btn" href="/harga">Upgrade Sekarang →</Link>
						</div>

						{/* Quick links */}
						<div className="db-card">
							<div className="db-card-header">
								<h2 className="db-card-title">Aksi Cepat</h2>
							</div>

							<Link
								href="/dashboard/invitations/create"
								className="db-quick-link"
							>
								<div className="db-quick-link-icon">
									<PhPlus size={14} />
								</div>
								<div className="db-quick-link-text">
									<span>Buat Undangan Baru</span>
									<small>Mulai dari template</small>
								</div>
							</Link>

							<Link href="/dashboard/invitations" className="db-quick-link">
								<div className="db-quick-link-icon">
									<PhEnvelopeSimple size={16} />
								</div>
								<div className="db-quick-link-text">
									<span>Kelola Undangan</span>
									<small>Ubah, terbitkan, atau hapus</small>
								</div>
							</Link>

							<Link href="/dashboard/templates" className="db-quick-link">
								<div className="db-quick-link-icon">
									<PhPalette size={16} />
								</div>
								<div className="db-quick-link-text">
									<span>Jelajahi Template</span>
									<small>Modern, adat, dan eksklusif</small>
								</div>
							</Link>
						</div>
					</div>
				</div>
			</div>
		</DashboardShell>
	);
}
