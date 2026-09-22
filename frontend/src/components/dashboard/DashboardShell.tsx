"use client";

import Link from "next/link";
import type { ReactNode } from "react";
import { useState } from "react";
import theme from "@/components/ui/workspace-theme.module.css";

/* ── Inline SVG icons ─────────────────────────────────────────── */
function IGrid() {
	return (
		<svg
			width="15"
			height="15"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2"
			aria-hidden="true"
		>
			<rect x="3" y="3" width="7" height="7" rx="1.2" />
			<rect x="14" y="3" width="7" height="7" rx="1.2" />
			<rect x="3" y="14" width="7" height="7" rx="1.2" />
			<rect x="14" y="14" width="7" height="7" rx="1.2" />
		</svg>
	);
}
function IScroll() {
	return (
		<svg
			width="15"
			height="15"
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
function IUsers() {
	return (
		<svg
			width="15"
			height="15"
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
function ILayout() {
	return (
		<svg
			width="15"
			height="15"
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
function IGear() {
	return (
		<svg
			width="15"
			height="15"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2"
			aria-hidden="true"
		>
			<circle cx="12" cy="12" r="3" />
			<path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z" />
		</svg>
	);
}
function ICheck() {
	return (
		<svg
			width="15"
			height="15"
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
function IStar() {
	return (
		<svg
			width="15"
			height="15"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2"
			aria-hidden="true"
		>
			<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
		</svg>
	);
}
function IMsg() {
	return (
		<svg
			width="15"
			height="15"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2"
			aria-hidden="true"
		>
			<path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
		</svg>
	);
}
function IPhone() {
	return (
		<svg
			width="15"
			height="15"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2"
			aria-hidden="true"
		>
			<path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.63A2 2 0 012 1h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.91 8.09a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z" />
		</svg>
	);
}
function ILogout() {
	return (
		<svg
			width="14"
			height="14"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2"
			aria-hidden="true"
		>
			<path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4" />
			<polyline points="16 17 21 12 16 7" />
			<line x1="21" y1="12" x2="9" y2="12" />
		</svg>
	);
}
function ISearch() {
	return (
		<svg
			width="13"
			height="13"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
			strokeWidth="2.5"
			aria-hidden="true"
		>
			<circle cx="11" cy="11" r="8" />
			<path d="m21 21-4.35-4.35" />
		</svg>
	);
}
/* ── Navigation config ────────────────────────────────────────── */
type NavItem = { key: string; label: string; href: string; icon: ReactNode };

const mainNav: NavItem[] = [
	{ key: "overview", label: "Dashboard", href: "/dashboard", icon: <IGrid /> },
	{
		key: "invitations",
		label: "Undangan",
		href: "/dashboard/invitations",
		icon: <IScroll />,
	},
	{ key: "guests", label: "Tamu", href: "/dashboard/guests", icon: <IUsers /> },
	{
		key: "templates",
		label: "Template",
		href: "/dashboard/templates",
		icon: <ILayout />,
	},
];

const manageNav: NavItem[] = [
	{
		key: "settings",
		label: "Pengaturan",
		href: "/dashboard/settings",
		icon: <IGear />,
	},
];

const adminNav: NavItem[] = [
	{ key: "overview", label: "Dashboard", href: "/admin", icon: <IGrid /> },
	{ key: "hero", label: "Hero", href: "/admin/hero", icon: <IStar /> },
	{
		key: "features",
		label: "Fitur",
		href: "/admin/features",
		icon: <ILayout />,
	},
	{
		key: "testimonials",
		label: "Testimoni",
		href: "/admin/testimonials",
		icon: <IMsg />,
	},
	{ key: "kontak", label: "Kontak", href: "/admin/kontak", icon: <IPhone /> },
	{ key: "footer", label: "Footer", href: "/admin/footer", icon: <IGear /> },
];

function invitationNav(id: string): NavItem[] {
	return [
		{
			key: "summary",
			label: "Overview",
			href: `/dashboard/invitations/${id}`,
			icon: <IGrid />,
		},
		{
			key: "couple",
			label: "Pasangan",
			href: `/dashboard/invitations/${id}/couple`,
			icon: <IUsers />,
		},
		{
			key: "events",
			label: "Acara",
			href: `/dashboard/invitations/${id}/events`,
			icon: <ICheck />,
		},
		{
			key: "gallery",
			label: "Galeri",
			href: `/dashboard/invitations/${id}/gallery`,
			icon: <ILayout />,
		},
		{
			key: "guests",
			label: "Tamu",
			href: `/dashboard/invitations/${id}/guests`,
			icon: <IUsers />,
		},
		{
			key: "rsvp",
			label: "RSVP",
			href: `/dashboard/invitations/${id}/rsvp`,
			icon: <IStar />,
		},
		{
			key: "wishes",
			label: "Ucapan",
			href: `/dashboard/invitations/${id}/wishes`,
			icon: <IMsg />,
		},
		{
			key: "gift",
			label: "Hadiah",
			href: `/dashboard/invitations/${id}/gift`,
			icon: <IStar />,
		},
		{
			key: "checkin",
			label: "Check-in",
			href: `/dashboard/invitations/${id}/checkin`,
			icon: <ICheck />,
		},
		{
			key: "settings",
			label: "Pengaturan",
			href: `/dashboard/invitations/${id}/settings`,
			icon: <IGear />,
		},
		{
			key: "preview",
			label: "Preview",
			href: `/dashboard/invitations/${id}/preview`,
			icon: <ILayout />,
		},
	];
}

/* ── Component ────────────────────────────────────────────────── */
export function DashboardShell({
	active,
	invitationId,
	variant = "user",
	children,
}: {
	active: string;
	invitationId?: string;
	variant?: "user" | "admin";
	children: ReactNode;
}) {
	const [userName] = useState(() =>
		typeof window === "undefined"
			? "Pengguna"
			: window.localStorage.getItem("yukakad_name") ?? "Pengguna",
	);
	const [userEmail] = useState(() =>
		typeof window === "undefined"
			? ""
			: window.localStorage.getItem("yukakad_email") ?? "",
	);

	const navGroups =
		variant === "admin"
			? [{ label: "Admin CMS", items: adminNav }]
			: invitationId
				? [{ label: "Undangan ini", items: invitationNav(invitationId) }]
				: [
						{ label: "Menu Utama", items: mainNav },
						{ label: "Kelola", items: manageNav },
					];

	const initials = userName
		.split(" ")
		.slice(0, 2)
		.map((n) => n[0]?.toUpperCase() ?? "")
		.join("");

	function handleLogout() {
		if (typeof window === "undefined") return;
		window.localStorage.clear();
		window.location.href = "/auth/login";
	}

	return (
		<main className={`dashboard-shell ${theme.workspace}`}>
			{/* ── Dark sidebar ───────────────────────────────────────── */}
			<aside className="dashboard-rail">
				{/* Logo */}
				<Link href="/dashboard" className="dashboard-logo">
					<span className="dashboard-logo-icon">
						y
					</span>
					yukakad<span>.</span>
				</Link>

				{/* Search */}
				<div className="db-search" role="search" aria-label="Cari">
					<ISearch />
					<span style={{ flex: 1 }}>Cari...</span>
					<kbd>⌘F</kbd>
				</div>

				{/* Back link when inside an invitation */}
				{invitationId && (
					<div style={{ paddingTop: "1rem" }}>
						<Link
							href="/dashboard/invitations"
							style={{
								display: "flex",
								alignItems: "center",
								gap: ".4rem",
								padding: ".45rem .75rem",
								fontSize: ".78rem",
								color: "#5A8476",
								textDecoration: "none",
								borderRadius: ".35rem",
							}}
						>
							← Semua Undangan
						</Link>
					</div>
				)}

				{/* Nav groups */}
				{navGroups.map((group) => (
					<div key={group.label} className="db-nav-section">
						<p className="db-nav-label">{group.label}</p>
						<nav aria-label={group.label}>
							{group.items.map((item) => (
								<Link
									key={item.key}
									href={item.href}
									aria-current={active === item.key ? "page" : undefined}
									className={active === item.key ? "active" : undefined}
								>
									{item.icon}
									{item.label}
								</Link>
							))}
						</nav>
					</div>
				))}

				{/* User section */}
				<div className="rail-user">
					<div className="rail-user-inner">
						<div className="rail-user-avatar" aria-hidden="true">
							{initials || "YK"}
						</div>
						<div style={{ minWidth: 0, flex: 1 }}>
							<strong>{userName}</strong>
							<span>{userEmail}</span>
						</div>
						<button
							onClick={handleLogout}
							aria-label="Keluar"
							style={{
								background: "none",
								border: "none",
								cursor: "pointer",
								color: "#3A6058",
								flexShrink: 0,
								padding: ".25rem",
								display: "flex",
								alignItems: "center",
							}}
						>
							<ILogout />
						</button>
					</div>
				</div>
			</aside>

			{/* ── Content area ───────────────────────────────────────── */}
			<section className="dashboard-content">{children}</section>
		</main>
	);
}
