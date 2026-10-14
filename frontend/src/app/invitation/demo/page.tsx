import type { InvitationData } from "@/components/invitation/types";
import { FALLBACK_THEME, isTheme, loadTheme } from "@/components/invitation/themes/registry";

// "?names=Nina & Dimas" lets marketing pages preview a theme with the visitor's own names.
function withNames(names: string | undefined, base: InvitationData): InvitationData {
  const [bride, groom] = (names ?? "").split(/\s*(?:&|dan)\s*/i).map(part => part.trim().slice(0, 40));
  if (!bride || !groom) return base;
  return { ...base, couple: { ...base.couple, bride, groom, brideFull: bride, groomFull: groom } };
}

export default async function InvitationDemoPage({ searchParams }: { searchParams: Promise<{ template?: string; names?: string; to?: string; open?: string }> }) {
  const { template, names, to, open } = await searchParams;
  const id = isTheme(template) ? template : FALLBACK_THEME;
  const { Theme, demo } = await loadTheme(id);
  const data = withNames(names, demo);
  return <Theme data={{ ...data, guestName: to ? to.replace(/-/g, " ").slice(0, 80) : data.guestName }} slug={`demo-${id}`} demo skipCover={open === "1"} />;
}
