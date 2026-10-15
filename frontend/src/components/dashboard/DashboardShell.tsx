"use client";

import Link from "next/link";
import type { ReactNode } from "react";
import { useState } from "react";
import theme from "@/components/ui/workspace-theme.module.css";
import { IconHeart } from "@/components/brand/icons";
import { Article as PhArticle, Browser as PhBrowser, CalendarBlank as PhCalendarBlank, ChatCircleText as PhChatCircleText, CheckSquare as PhCheckSquare, EnvelopeSimple as PhEnvelopeSimple, Eye as PhEye, Gear as PhGear, Gift as PhGift, Heart as PhHeart, Images as PhImages, MagnifyingGlass as PhMagnifyingGlass, MusicNotes as PhMusicNotes, Stack as PhStack, Palette as PhPalette, Phone as PhPhone, QrCode as PhQrCode, SignOut as PhSignOut, SquaresFour as PhSquaresFour, Star as PhStar, Users as PhUsers } from "@phosphor-icons/react/ssr";

type NavItem = { key: string; label: string; href: string; icon: ReactNode };

const mainNav: NavItem[] = [
	{ key: "overview", label: "Dashboard", href: "/dashboard", icon: <PhSquaresFour size={16} /> },
	{
		key: "invitations",
		label: "Undangan",
		href: "/dashboard/invitations",
		icon: <PhEnvelopeSimple size={16} />,
	},
	{ key: "guests", label: "Tamu", href: "/dashboard/guests", icon: <PhUsers size={16} /> },
	{
		key: "templates",
		label: "Tema",
		href: "/dashboard/templates",
		icon: <PhPalette size={16} />,
	},
];

const manageNav: NavItem[] = [
	{
		key: "settings",
		label: "Pengaturan",
		href: "/dashboard/settings",
		icon: <PhGear size={16} />,
	},
];

const adminNav: NavItem[] = [
	{ key: "overview", label: "Dashboard", href: "/admin", icon: <PhSquaresFour size={16} /> },
	{ key: "hero", label: "Hero", href: "/admin/hero", icon: <PhBrowser size={16} /> },
	{
		key: "features",
		label: "Fitur",
		href: "/admin/features",
		icon: <PhStar size={16} />,
	},
	{
		key: "testimonials",
		label: "Testimoni",
		href: "/admin/testimonials",
		icon: <PhChatCircleText size={16} />,
	},
	{ key: "kontak", label: "Kontak", href: "/admin/kontak", icon: <PhPhone size={16} /> },
	{ key: "footer", label: "Footer", href: "/admin/footer", icon: <PhArticle size={16} /> },
];

function invitationNav(id: string): NavItem[] {
	return [
		{
			key: "summary",
			label: "Ringkasan",
			href: `/dashboard/invitations/${id}`,
			icon: <PhSquaresFour size={16} />,
		},
		{
			key: "couple",
			label: "Mempelai",
			href: `/dashboard/invitations/${id}/couple`,
			icon: <PhHeart size={16} />,
		},
		{
			key: "events",
			label: "Acara",
			href: `/dashboard/invitations/${id}/events`,
			icon: <PhCalendarBlank size={16} />,
		},
		{
			key: "gallery",
			label: "Galeri",
			href: `/dashboard/invitations/${id}/gallery`,
			icon: <PhImages size={16} />,
		},
		{
			key: "guests",
			label: "Tamu",
			href: `/dashboard/invitations/${id}/guests`,
			icon: <PhUsers size={16} />,
		},
		{
			key: "rsvp",
			label: "RSVP",
			href: `/dashboard/invitations/${id}/rsvp`,
			icon: <PhCheckSquare size={16} />,
		},
		{
			key: "wishes",
			label: "Ucapan",
			href: `/dashboard/invitations/${id}/wishes`,
			icon: <PhChatCircleText size={16} />,
		},
		{
			key: "gift",
			label: "Hadiah",
			href: `/dashboard/invitations/${id}/gift`,
			icon: <PhGift size={16} />,
		},
		{
			key: "checkin",
			label: "Check-in",
			href: `/dashboard/invitations/${id}/checkin`,
			icon: <PhQrCode size={16} />,
		},
		{
			key: "settings",
			label: "Tema & Musik",
			href: `/dashboard/invitations/${id}/settings`,
			icon: <PhMusicNotes size={16} />,
		},
		{
			key: "sections",
			label: "Section Tambahan",
			href: `/dashboard/invitations/${id}/sections`,
			icon: <PhStack size={16} />,
		},
		{
			key: "preview",
			label: "Pratinjau",
			href: `/dashboard/invitations/${id}/preview`,
			icon: <PhEye size={16} />,
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
			: window.localStorage.getItem("yukakad_name") ?? (variant === "admin" ? "Admin" : "Pengguna"),
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
					<span className="dashboard-logo-icon" aria-hidden="true">
						<IconHeart size={16} strokeWidth={2.2} />
					</span>
					RAWUH
				</Link>

				{/* Search */}
				<div className="db-search" role="search" aria-label="Cari">
					<PhMagnifyingGlass size={15} />
					<span style={{ flex: 1 }}>Cari...</span>
					<kbd>⌘F</kbd>
				</div>

				{/* Back link when inside an invitation */}
				{invitationId && (
					<div style={{ paddingTop: "1rem" }}>
						<Link
							href="/dashboard/invitations"
							className="rail-back"
							style={{
								display: "flex",
								alignItems: "center",
								gap: ".4rem",
								padding: ".45rem .75rem",
								fontSize: ".78rem",
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
							{initials || "RW"}
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
								flexShrink: 0,
								padding: ".25rem",
								display: "flex",
								alignItems: "center",
							}}
						>
							<PhSignOut size={16} />
						</button>
					</div>
				</div>
			</aside>

			{/* ── Content area ───────────────────────────────────────── */}
			<section className="dashboard-content">{children}</section>
		</main>
	);
}
