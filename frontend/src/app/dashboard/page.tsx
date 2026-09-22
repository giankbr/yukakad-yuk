"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
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

/* ── Tiny icon set ───────────────────────────────────────────────── */
function IDoc() {
	return (
		<svg
			width="18"
			height="18"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2"
			aria-hidden="true"
		>
			<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
			<polyline points="14 2 14 8 20 8" />
			<line x1="16" y1="13" x2="8" y2="13" />
			<line x1="16" y1="17" x2="8" y2="17" />
		</svg>
	);
}
function IGlobe() {
	return (
		<svg
			width="18"
			height="18"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2"
			aria-hidden="true"
		>
			<circle cx="12" cy="12" r="10" />
			<line x1="2" y1="12" x2="22" y2="12" />
			<path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z" />
		</svg>
	);
}
function IUsers() {
	return (
		<svg
			width="18"
			height="18"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2"
			aria-hidden="true"
		>
			<path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
			<circle cx="9" cy="7" r="4" />
			<path d="M23 21v-2a4 4 0 00-3-3.87" />
			<path d="M16 3.13a4 4 0 010 7.75" />
		</svg>
	);
}
function ICheck() {
	return (
		<svg
			width="18"
			height="18"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2"
			aria-hidden="true"
		>
			<polyline points="9 11 12 14 22 4" />
			<path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" />
		</svg>
	);
}
function IBell() {
	return (
		<svg
			width="17"
			height="17"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2"
			aria-hidden="true"
		>
			<path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9" />
			<path d="M13.73 21a2 2 0 01-3.46 0" />
		</svg>
	);
}
function IPlus() {
	return (
		<svg
			width="14"
			height="14"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2.5"
			aria-hidden="true"
		>
			<line x1="12" y1="5" x2="12" y2="19" />
			<line x1="5" y1="12" x2="19" y2="12" />
		</svg>
	);
}
function IArrow() {
	return (
		<svg
			width="12"
			height="12"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2.5"
			aria-hidden="true"
		>
			<line x1="5" y1="12" x2="19" y2="12" />
			<polyline points="12 5 19 12 12 19" />
		</svg>
	);
}
function ILayout() {
	return (
		<svg
			width="16"
			height="16"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2"
			aria-hidden="true"
		>
			<rect x="3" y="3" width="18" height="18" rx="2" />
			<line x1="3" y1="9" x2="21" y2="9" />
			<line x1="9" y1="21" x2="9" y2="9" />
		</svg>
	);
}
function IScroll() {
	return (
		<svg
			width="16"
			height="16"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2"
			aria-hidden="true"
		>
			<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
			<polyline points="14 2 14 8 20 8" />
		</svg>
	);
}

/* ── Stat card ───────────────────────────────────────────────────── */
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
					<IArrow />
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
						<IBell />
					</button>
					<Link href="/dashboard/invitations/create" className="db-primary-btn">
						<IPlus /> Buat Undangan
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
						icon={<IDoc />}
						delta="Semua undangan Anda"
					/>
					<StatCard
						label="Terpublikasi"
						value={published.length}
						icon={<IGlobe />}
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
						icon={<IUsers />}
						badge={
							draft.length > 0 ? { text: "Draft", positive: false } : undefined
						}
						delta="Belum dipublikasikan"
					/>
					<StatCard
						label="Acara Aktif"
						value={published.length}
						icon={<ICheck />}
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
									<IPlus /> Buat Undangan
								</Link>
							</div>
						)}

						{!loading && !error && invitations.length > 0 && (
							<table className="db-table">
								<thead>
									<tr>
										<th>Undangan</th>
										<th>Status</th>
										<th>Pasangan</th>
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
													yukakad.com/{inv.slug}
												</small>
											</td>
											<td>
												<span
													className={
														inv.published ? "db-status-pub" : "db-status-draft"
													}
												>
													{inv.published ? "● Publik" : "○ Draft"}
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
								Hapus watermark, custom domain, tamu tak terbatas, dan template
								eksklusif adat Nusantara.
							</p>
							<button className="db-upgrade-btn">Upgrade Sekarang →</button>
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
									<IPlus />
								</div>
								<div className="db-quick-link-text">
									<span>Buat Undangan Baru</span>
									<small>Mulai dari template</small>
								</div>
							</Link>

							<Link href="/dashboard/invitations" className="db-quick-link">
								<div className="db-quick-link-icon">
									<IScroll />
								</div>
								<div className="db-quick-link-text">
									<span>Kelola Undangan</span>
									<small>Edit, publish, atau hapus</small>
								</div>
							</Link>

							<Link href="/dashboard/templates" className="db-quick-link">
								<div className="db-quick-link-icon">
									<ILayout />
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
