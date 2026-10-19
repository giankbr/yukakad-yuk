"use client";

import { useEffect, useState } from "react";
import { apiFetch, AUTH_EVENT, getToken } from "@/lib/api";

export type AccessRole = "owner" | "editor" | "organizer" | "receptionist";
export type Access = { role: AccessRole; permissions: string[] };

export const ROLE_LABELS: Record<AccessRole, string> = {
  owner: "Pemilik",
  editor: "Keluarga / editor",
  organizer: "WO / vendor",
  receptionist: "Penerima tamu",
};

export const ROLE_DESCRIPTIONS: Record<Exclude<AccessRole, "owner">, string> = {
  editor: "Mengubah isi undangan, mengelola tamu, RSVP & ucapan. Tidak bisa melihat amplop atau saldo.",
  organizer: "Semua yang bisa dilakukan keluarga, plus hari-H: check-in, buku buwuh, doorprize, foto tamu.",
  receptionist: "Khusus hari-H: scan check-in, mencatat amplop/kado, dan membuka layar sapa.",
};

/** Permission each dashboard page needs (mirrors the backend gate; "owner" = owner only). */
export const PAGE_PERMISSION: Record<string, string> = {
  summary: "guests", preview: "view", // the summary shows RSVP and wishes counts
  couple: "content", events: "content", stories: "content", gallery: "content", settings: "content", sections: "content",
  guests: "guests", rsvp: "guests", wishes: "guests",
  gift: "owner", team: "owner", domain: "owner",
  ledger: "ledger_read",
  checkin: "checkin", screen: "live", doorprize: "hari_h", photos: "hari_h",
};

export function can(access: Access | null | undefined, page: string) {
  if (!access) return true; // unknown yet: show everything, the API still enforces
  if (access.role === "owner") return true;
  const need = PAGE_PERMISSION[page];
  return Boolean(need) && need !== "owner" && access.permissions.includes(need);
}

/** Where a member lands when opening a shared invitation. */
export function landingPath(id: string, role: AccessRole) {
  return role === "receptionist" ? `/dashboard/invitations/${id}/checkin` : `/dashboard/invitations/${id}`;
}

const cache = new Map<string, Access>();

/** Forgets every cached role, e.g. on logout so the next account doesn't inherit the previous one's access. */
export function clearAccessCache() {
  cache.clear();
}

// Any login/logout/token swap in this tab invalidates the cached roles.
if (typeof window !== "undefined") window.addEventListener(AUTH_EVENT, clearAccessCache);

export function useInvitationAccess(invitationId?: string) {
  const [access, setAccess] = useState<Access | null>(() => (invitationId ? cache.get(invitationId) ?? null : null));
  useEffect(() => {
    if (!invitationId) return;
    const token = getToken();
    if (!token) return;
    let cancelled = false;
    apiFetch(`/api/invitations/${invitationId}`, token)
      .then((r) => (r.ok ? r.json() : null))
      .then((body: { access?: Access } | null) => {
        if (cancelled || !body?.access?.role) return;
        cache.set(invitationId, body.access);
        setAccess(body.access);
      })
      .catch(() => undefined);
    return () => { cancelled = true; };
  }, [invitationId]);
  return access;
}
