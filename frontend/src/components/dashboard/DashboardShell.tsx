"use client";

import Link from "next/link";
import { useCallback, useEffect, useState, type ReactNode } from "react";
import { usePathname } from "next/navigation";
import { can, landingPath, ROLE_LABELS, useInvitationAccess } from "@/lib/invitation-access";
import shell from "./shell.module.css";
import theme from "@/components/ui/workspace-theme.module.css";
import { IconHeart } from "@/components/brand/icons";
import { Article as PhArticle, Megaphone as PhMegaphone, Tag as PhTag, Info as PhInfo, UsersThree as PhUsersThree, LockSimple as PhLockSimple, CreditCard as PhCreditCard, Receipt as PhReceipt, Notebook as PhNotebook, Monitor as PhMonitor, Confetti as PhConfetti, Camera as PhCamera, HandCoins as PhHandCoins, Package as PhPackage, Scales as PhScales, BookOpenText as PhBookOpenText, Browser as PhBrowser, CalendarBlank as PhCalendarBlank, ChatCircleText as PhChatCircleText, CheckSquare as PhCheckSquare, EnvelopeSimple as PhEnvelopeSimple, Eye as PhEye, Gear as PhGear, Gift as PhGift, Heart as PhHeart, Images as PhImages, MagnifyingGlass as PhMagnifyingGlass, MusicNotes as PhMusicNotes, Stack as PhStack, Palette as PhPalette, Phone as PhPhone, QrCode as PhQrCode, SignOut as PhSignOut, SidebarSimple as PhSidebarSimple, List as PhList, X as PhX, ArrowLeft as PhArrowLeft, SquaresFour as PhSquaresFour, Star as PhStar, Users as PhUsers } from "@phosphor-icons/react/ssr";

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
	{ key: "billing", label: "Paket & tagihan", href: "/dashboard/paket", icon: <PhCreditCard size={16} /> },
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
	{ key: "landing", label: "Statistik & FAQ", href: "/admin/landing", icon: <PhMegaphone size={16} /> },
];

const pagesNav: NavItem[] = [
	{ key: "about", label: "Tentang kami", href: "/admin/about", icon: <PhInfo size={16} /> },
	{ key: "products", label: "Produk", href: "/admin/products", icon: <PhPackage size={16} /> },
	{ key: "legal", label: "Legal", href: "/admin/legal", icon: <PhScales size={16} /> },
];

const businessNav: NavItem[] = [
	{ key: "plans", label: "Paket & harga", href: "/admin/plans", icon: <PhTag size={16} /> },
	{ key: "templates", label: "Tema", href: "/admin/templates", icon: <PhPalette size={16} /> },
	{ key: "users", label: "Pengguna", href: "/admin/users", icon: <PhUsers size={16} /> },
	{ key: "payouts", label: "Pencairan amplop", href: "/admin/payouts", icon: <PhHandCoins size={16} /> },
	{ key: "payments", label: "Pembayaran", href: "/admin/payments", icon: <PhReceipt size={16} /> },
];

function invitationNav(id: string): { label: string; items: NavItem[] }[] {
	const base = `/dashboard/invitations/${id}`;
	return [
		{
			label: "Undangan ini",
			items: [
				{ key: "summary", label: "Ringkasan", href: base, icon: <PhSquaresFour size={16} /> },
				{ key: "couple", label: "Mempelai", href: `${base}/couple`, icon: <PhHeart size={16} /> },
				{ key: "events", label: "Acara", href: `${base}/events`, icon: <PhCalendarBlank size={16} /> },
				{ key: "stories", label: "Kisah cinta", href: `${base}/stories`, icon: <PhBookOpenText size={16} /> },
				{ key: "gallery", label: "Galeri", href: `${base}/gallery`, icon: <PhImages size={16} /> },
				{ key: "settings", label: "Tema & Musik", href: `${base}/settings`, icon: <PhMusicNotes size={16} /> },
				{ key: "sections", label: "Section Tambahan", href: `${base}/sections`, icon: <PhStack size={16} /> },
				{ key: "preview", label: "Pratinjau", href: `${base}/preview`, icon: <PhEye size={16} /> },
				{ key: "team", label: "Tim & akses", href: `${base}/tim`, icon: <PhUsersThree size={16} /> },
			],
		},
		{
			label: "Tamu & amplop",
			items: [
				{ key: "guests", label: "Tamu", href: `${base}/guests`, icon: <PhUsers size={16} /> },
				{ key: "rsvp", label: "RSVP", href: `${base}/rsvp`, icon: <PhCheckSquare size={16} /> },
				{ key: "wishes", label: "Ucapan", href: `${base}/wishes`, icon: <PhChatCircleText size={16} /> },
				{ key: "gift", label: "Amplop digital", href: `${base}/gift`, icon: <PhGift size={16} /> },
				{ key: "ledger", label: "Buku buwuh", href: `${base}/buwuh`, icon: <PhNotebook size={16} /> },
			],
		},
		{
			label: "Hari-H",
			items: [
				{ key: "checkin", label: "Check-in", href: `${base}/checkin`, icon: <PhQrCode size={16} /> },
				{ key: "screen", label: "Layar sapa", href: `${base}/layar`, icon: <PhMonitor size={16} /> },
				{ key: "doorprize", label: "Undian doorprize", href: `${base}/doorprize`, icon: <PhConfetti size={16} /> },
				{ key: "photos", label: "Foto dari tamu", href: `${base}/foto-tamu`, icon: <PhCamera size={16} /> },
			],
		},
	];
}

/* ── Component ────────────────────────────────────────────────── */
const COLLAPSE_KEY = "rawuh_sidebar_collapsed";

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
	// Desktop: icon-only rail, remembered per browser. Mobile: off-canvas drawer.
	const [collapsed, setCollapsed] = useState(() => {
		if (typeof window === "undefined") return false;
		try {
			return window.localStorage.getItem(COLLAPSE_KEY) === "1";
		} catch {
			return false;
		}
	});
	const [drawerOpen, setDrawerOpen] = useState(false);
	const pathname = usePathname();
	const access = useInvitationAccess(variant === "user" ? invitationId : undefined);

	const toggleCollapsed = useCallback(() => {
		setCollapsed((value) => {
			try {
				window.localStorage.setItem(COLLAPSE_KEY, value ? "0" : "1");
			} catch {
				/* storage unavailable: keep in-memory state */
			}
			return !value;
		});
	}, []);

	// Close the drawer on navigation and with Escape; lock page scroll while it is open.
	useEffect(() => {
		const timer = setTimeout(() => setDrawerOpen(false), 0);
		return () => clearTimeout(timer);
	}, [pathname]);
	useEffect(() => {
		if (!drawerOpen) return;
		const onKey = (event: KeyboardEvent) => { if (event.key === "Escape") setDrawerOpen(false); };
		const previous = document.body.style.overflow;
		document.body.style.overflow = "hidden";
		window.addEventListener("keydown", onKey);
		return () => { document.body.style.overflow = previous; window.removeEventListener("keydown", onKey); };
	}, [drawerOpen]);
	// Keyboard shortcut: Ctrl/Cmd + B toggles the rail on desktop.
	useEffect(() => {
		const onKey = (event: KeyboardEvent) => {
			if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "b") {
				event.preventDefault();
				toggleCollapsed();
			}
		};
		window.addEventListener("keydown", onKey);
		return () => window.removeEventListener("keydown", onKey);
	}, [toggleCollapsed]);

	const navGroups =
		variant === "admin"
			? [{ label: "Konten landing", items: adminNav }, { label: "Halaman", items: pagesNav }, { label: "Bisnis", items: businessNav }]
			: invitationId
				? invitationNav(invitationId)
						.map((group) => ({ ...group, items: group.items.filter((item) => can(access, item.key)) }))
						.filter((group) => group.items.length > 0)
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

	const home = variant === "admin" ? "/admin" : "/dashboard";

	return (
		<main className={`${shell.shell} ${theme.workspace}`} data-collapsed={collapsed || undefined}>
			{/* ── Mobile top bar ─────────────────────────────────────── */}
			<header className={shell.topbar}>
				<button type="button" className={shell.iconButton} onClick={() => setDrawerOpen(true)} aria-label="Buka menu" aria-expanded={drawerOpen} aria-controls="dashboard-rail">
					<PhList size={20} />
				</button>
				<Link href={home} className={shell.logo}>
					<span className={shell.logoIcon} aria-hidden="true"><IconHeart size={16} strokeWidth={2.2} /></span>
					<span>RAWUH</span>
				</Link>
				<span className={shell.avatar} aria-hidden="true">{initials || "RW"}</span>
			</header>

			{drawerOpen && <button type="button" className={shell.scrim} aria-label="Tutup menu" onClick={() => setDrawerOpen(false)} />}

			{/* ── Sidebar ────────────────────────────────────────────── */}
			<aside id="dashboard-rail" className={shell.rail} data-open={drawerOpen || undefined} aria-label="Navigasi dashboard">
				<div className={shell.railHead}>
					<Link href={home} className={shell.logo} title="Rawuh">
						<span className={shell.logoIcon} aria-hidden="true"><IconHeart size={16} strokeWidth={2.2} /></span>
						<span className={shell.label}>RAWUH</span>
					</Link>
					<button type="button" className={`${shell.iconButton} ${shell.collapseButton}`} onClick={toggleCollapsed}
						aria-label={collapsed ? "Lebarkan sidebar" : "Ciutkan sidebar"} aria-pressed={collapsed} title={`${collapsed ? "Lebarkan" : "Ciutkan"} sidebar (Ctrl/⌘ B)`}>
						<PhSidebarSimple size={18} />
					</button>
					<button type="button" className={`${shell.iconButton} ${shell.closeButton}`} onClick={() => setDrawerOpen(false)} aria-label="Tutup menu">
						<PhX size={18} />
					</button>
				</div>

				<div className={shell.search} role="search" aria-label="Cari" data-tip="Cari">
					<PhMagnifyingGlass size={15} />
					<span className={shell.label}>Cari...</span>
					<kbd className={shell.label}>⌘F</kbd>
				</div>

				{invitationId && (
					<Link href="/dashboard/invitations" className={shell.back} data-tip="Semua undangan">
						<PhArrowLeft size={15} />
						<span className={shell.label}>Semua Undangan</span>
					</Link>
				)}

				<div className={shell.navScroll}>
					{navGroups.map((group) => (
						<div key={group.label} className={shell.group}>
							<p className={shell.groupLabel}>{group.label}</p>
							<nav aria-label={group.label} className={shell.nav}>
								{group.items.map((item) => (
									<Link
										key={item.key}
										href={item.href}
										aria-current={active === item.key ? "page" : undefined}
										className={shell.link}
										data-tip={item.label}
										onClick={() => setDrawerOpen(false)}
									>
										<span className={shell.linkIcon}>{item.icon}</span>
										<span className={shell.label}>{item.label}</span>
									</Link>
								))}
							</nav>
						</div>
					))}
				</div>

				<div className={shell.user}>
					<span className={shell.avatar} aria-hidden="true">{initials || "RW"}</span>
					<div className={`${shell.userText} ${shell.label}`}>
						<strong>{userName}</strong>
						{userEmail && <small>{userEmail}</small>}
					</div>
					<button type="button" onClick={handleLogout} aria-label="Keluar" className={shell.iconButton} data-tip="Keluar">
						<PhSignOut size={16} />
					</button>
				</div>
			</aside>

			{/* ── Content area ───────────────────────────────────────── */}
			<section className={`dashboard-content ${shell.content}`}>
				{access && access.role !== "owner" && (
					<p className="dashboard-role-note"><PhUsersThree size={14} /> Kamu membantu undangan ini sebagai <b>{ROLE_LABELS[access.role]}</b>.</p>
				)}
				{invitationId && variant === "user" && !can(access, active) ? (
					<div className="dashboard-state" role="alert" style={{ display: "grid", gap: 8, justifyItems: "start" }}>
						<strong><PhLockSimple size={14} /> Halaman ini tidak tersedia untuk peranmu.</strong>
						{access && <a className="table-action" href={landingPath(invitationId, access.role)}>Ke halaman yang bisa kamu buka</a>}
					</div>
				) : children}
			</section>
		</main>
	);
}
