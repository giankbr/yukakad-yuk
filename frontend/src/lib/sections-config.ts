import { apiFetch } from "@/lib/api";
import type { InvitationExtras } from "@/components/invitation/types";

/** Merge one key into settings.sections_config without clobbering the other sections. */
export async function patchSectionsConfig<K extends keyof InvitationExtras>(invitationId: string, token: string, key: K, value: InvitationExtras[K]) {
  const current = await apiFetch(`/api/invitations/${invitationId}/settings`, token).then((r) => r.json());
  const config = current.sections_config && typeof current.sections_config === "object" && !Array.isArray(current.sections_config) ? current.sections_config : {};
  const response = await apiFetch(`/api/invitations/${invitationId}/settings`, token, { method: "PATCH", body: JSON.stringify({ sections_config: { ...config, [key]: value } }) });
  if (!response.ok) throw new Error("Belum tersimpan.");
  return { ...config, [key]: value } as InvitationExtras;
}

export async function getSectionsConfig(invitationId: string, token: string): Promise<InvitationExtras> {
  const current = await apiFetch(`/api/invitations/${invitationId}/settings`, token).then((r) => r.json());
  return current.sections_config && typeof current.sections_config === "object" && !Array.isArray(current.sections_config) ? current.sections_config : {};
}
