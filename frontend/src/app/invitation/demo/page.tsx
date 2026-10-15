import type { InvitationData } from "@/components/invitation/types";
import { FALLBACK_THEME, isTheme, loadTheme } from "@/components/invitation/themes/registry";
import { InvitationProvider } from "@/components/invitation/themes/kit";

// "?names=Nina & Dimas" lets marketing pages preview a theme with the visitor's own names.
function withNames(names: string | undefined, base: InvitationData): InvitationData {
  const [bride, groom] = (names ?? "").split(/\s*(?:&|dan)\s*/i).map(part => part.trim().slice(0, 40));
  if (!bride || !groom) return base;
  return { ...base, couple: { ...base.couple, bride, groom, brideFull: bride, groomFull: groom } };
}

export default async function InvitationDemoPage({ searchParams }: { searchParams: Promise<{ template?: string; names?: string; to?: string; open?: string; selesai?: string }> }) {
  const { template, names, to, open, selesai } = await searchParams;
  const id = isTheme(template) ? template : FALLBACK_THEME;
  const { Theme, demo } = await loadTheme(id);
  const named = withNames(names, demo);
  const data = {
    ...named,
    guestName: to ? to.replace(/-/g, " ").slice(0, 80) : named.guestName,
    // "?selesai=1" previews the after-the-event thank-you mode.
    extras: selesai === "1" ? { ...named.extras, thankYou: { mode: "on" as const } } : named.extras,
  };
  const slug = `demo-${id}`;
  return (
    <InvitationProvider data={data} slug={slug} demo theme={id}>
      <Theme data={data} slug={slug} demo skipCover={open === "1"} />
    </InvitationProvider>
  );
}
