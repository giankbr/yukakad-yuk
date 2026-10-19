"use client";

// Shared helpers for the per-invitation dashboard pages: JSON fetching that
// checks the status code, an access gate that waits for the caller's role
// before firing role-restricted calls, and the friendly "no access" states.

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";
import { friendlyError } from "@/lib/errors";
import { can, landingPath, ROLE_LABELS, type Access } from "@/lib/invitation-access";

/* ── Errors ─────────────────────────────────────────────────────────── */

const ENGLISH_ERRORS: Array<[RegExp, string]> = [
  [/invalid credentials/i, "Email atau kata sandi salah"],
  [/guest limit reached/i, "Kuota tamu paketmu sudah habis. Upgrade paket untuk menambah tamu."],
  [/media storage is not configured/i, "Penyimpanan foto belum disiapkan. Hubungi admin Rawuh."],
  [/invalid token|missing authorization token|unauthori[sz]ed/i, "Sesi kamu sudah berakhir. Silakan masuk lagi."],
  [/forbidden|permission/i, "Peranmu tidak bisa melakukan ini."],
  [/invitation not found|not found/i, "Data tidak ditemukan atau kamu sudah tidak punya akses."],
  [/name is required/i, "Nama wajib diisi."],
  [/invalid csv/i, "File CSV tidak bisa dibaca. Pastikan kolomnya: nama, no. HP, kategori, meja."],
  [/slug already (exists|taken)/i, "Alamat undangan itu sudah dipakai. Coba alamat lain."],
  [/already a member/i, "Orang ini sudah menjadi anggota tim."],
  [/invalid (json|payload|request)/i, "Data yang dikirim belum lengkap atau tidak valid."],
  [/too many requests|rate limit/i, "Terlalu banyak percobaan. Tunggu sebentar lalu coba lagi."],
  [/plan .*unavailable|plan not found/i, "Paket belum tersedia. Coba lagi nanti."],
  [/method not allowed|internal server error/i, "Terjadi kesalahan di server. Coba lagi sebentar lagi."],
  [/failed to fetch|networkerror|load failed/i, "Tidak bisa terhubung ke server. Periksa koneksi internetmu."],
];

/**
 * Maps known raw (English) API errors to Indonesian; Indonesian messages pass through.
 * Exact matches come from the shared table in lib/errors, then these page-level patterns.
 */
export function friendly(message: unknown, fallback = "Terjadi kesalahan. Coba lagi."): string {
  const text = typeof message === "string" ? message.trim() : message instanceof Error ? message.message.trim() : "";
  if (!text) return fallback;
  const shared = friendlyError(text, fallback);
  if (shared.toLowerCase() !== text.toLowerCase()) return shared;
  for (const [pattern, replacement] of ENGLISH_ERRORS) if (pattern.test(text)) return replacement;
  return shared;
}

/* ── Fetch ──────────────────────────────────────────────────────────── */

export type ApiBody = { error?: string; code?: string; [key: string]: unknown };
export type ApiResult<T> = { ok: boolean; status: number; data: T | null; body: ApiBody; error: string };

/** apiFetch + JSON parse that never throws on HTTP errors; `data` is only set for 2xx. */
export async function getJson<T>(path: string, token: string, init: RequestInit = {}): Promise<ApiResult<T>> {
  let response: Response;
  try {
    response = await apiFetch(path, token, init);
  } catch (err) {
    return { ok: false, status: 0, data: null, body: {}, error: friendly(err, "Tidak bisa terhubung ke server. Periksa koneksi internetmu.") };
  }
  const parsed: unknown = await response.json().catch(() => null);
  const body: ApiBody = parsed && typeof parsed === "object" && !Array.isArray(parsed) ? (parsed as ApiBody) : {};
  if (!response.ok) return { ok: false, status: response.status, data: null, body, error: friendly(body.error) };
  return { ok: true, status: response.status, data: parsed as T, body, error: "" };
}

/** True when a status means the caller lost (or never had) access to this invitation. */
export const lostAccess = (status: number) => status === 403 || status === 404;

/* ── Access gate ────────────────────────────────────────────────────── */

export type GateStatus = "loading" | "ok" | "denied" | "gone" | "expired" | "error";
export type Gate<I> = { status: GateStatus; access: Access | null; invitation: I | null; lose: () => void };

const accessCache = new Map<string, Access>();

/**
 * Loads the invitation once to learn the caller's role, then reports whether
 * `page` (a key of PAGE_PERMISSION) is allowed. Pages should only fire their
 * own calls when `status === "ok"`.
 */
export function usePageGate<I extends object = { access?: Access }>(invitationId: string | undefined, token: string | null, page: string): Gate<I> {
  const cached = invitationId ? accessCache.get(invitationId) : undefined;
  const [state, setState] = useState<{ status: GateStatus; access: Access | null; invitation: I | null }>(() => ({
    status: cached ? (can(cached, page) ? "ok" : "denied") : "loading",
    access: cached ?? null,
    invitation: null,
  }));

  useEffect(() => {
    if (!invitationId || !token) return;
    let cancelled = false;
    getJson<I>(`/api/invitations/${invitationId}`, token).then((result) => {
      if (cancelled) return;
      if (!result.ok) {
        if (lostAccess(result.status)) accessCache.delete(invitationId);
        const status: GateStatus = lostAccess(result.status) ? "gone" : result.status === 401 ? "expired" : "error";
        setState({ status, access: null, invitation: null });
        return;
      }
      // Older payloads carry no access block: only the owner could load it then.
      const given = (result.data as { access?: Access } | null)?.access;
      const access: Access = given?.role ? given : { role: "owner", permissions: [] };
      accessCache.set(invitationId, access);
      setState({ status: can(access, page) ? "ok" : "denied", access, invitation: result.data });
    });
    return () => { cancelled = true; };
  }, [invitationId, token, page]);

  const lose = useCallback(() => {
    if (invitationId) accessCache.delete(invitationId);
    setState({ status: "gone", access: null, invitation: null });
  }, [invitationId]);

  return { ...state, lose };
}

/** Full-page notice for every non-"ok" gate state. `deniedText` customises the role message. */
export function GateNotice({ gate, invitationId, deniedText }: { gate: Pick<Gate<unknown>, "status" | "access">; invitationId: string; deniedText?: string }) {
  if (gate.status === "ok") return null;
  if (gate.status === "loading") return <p className="dashboard-state" role="status">Memuat…</p>;

  let title = "";
  let text = "";
  let href = "/dashboard";
  let cta = "Kembali ke dashboard";
  if (gate.status === "gone") {
    title = "Kamu tidak punya akses ke undangan ini lagi";
    text = "Undangan ini mungkin sudah dihapus, atau pemiliknya mengeluarkanmu dari tim.";
  } else if (gate.status === "expired") {
    title = "Sesi kamu sudah berakhir";
    text = "Silakan masuk lagi untuk melanjutkan.";
    href = `/auth/login?next=${encodeURIComponent(`/dashboard/invitations/${invitationId}`)}`;
    cta = "Masuk lagi";
  } else if (gate.status === "denied") {
    const role = gate.access?.role;
    title = deniedText ?? "Peranmu tidak bisa membuka halaman ini";
    text = role && role !== "owner" ? `Kamu bergabung sebagai ${ROLE_LABELS[role]}. Minta pemilik undangan bila perlu akses lebih.` : "Minta pemilik undangan bila perlu akses lebih.";
    if (role) {
      href = landingPath(invitationId, role);
      cta = role === "receptionist" ? "Buka scan check-in" : "Ke ringkasan undangan";
    }
  } else {
    title = "Undangan belum bisa dimuat";
    text = "Periksa koneksi internetmu, lalu muat ulang halaman ini.";
  }

  return (
    <section className="dashboard-note" role="alert" style={{ marginTop: "1rem" }}>
      <div>
        <p className="dashboard-kicker">Akses</p>
        <h2>{title}</h2>
      </div>
      <p>{text}</p>
      <Link className="secondary-action" href={href}>{cta} →</Link>
    </section>
  );
}
