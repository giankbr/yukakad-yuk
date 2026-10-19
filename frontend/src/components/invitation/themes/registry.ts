// Generated from the Rawuh design file. Theme ids are stable: they are stored as invitations.template_id.
import { createElement, type ComponentType } from "react";
import type { InvitationData } from "../types";
import type { ThemeProps } from "./kit";
import { freshDemo } from "./demo-base";
import ThemeSwitch from "./ThemeSwitch";

export { themeList, type ThemeMeta } from "./list";

type DemoModule = { demo: InvitationData };

// Demo data only (server-side). Theme components are NOT imported here: they live behind per-theme
// `next/dynamic` chunks in ThemeSwitch.tsx, so guests download only the theme they need. Importing the
// theme modules from this server file would register all 38 as client references of the page and
// ship them in one big client chunk.
const loaders: Record<string, () => Promise<DemoModule>> = {
  "marketplace": () => import("./marketplace/demo"),
  "oranye": () => import("./oranye/demo"),
  "streaming": () => import("./streaming/demo"),
  "jawa": () => import("./jawa/demo"),
  "rumah-gadang": () => import("./rumah-gadang/demo"),
  "bali-kuning": () => import("./bali-kuning/demo"),
  "syari-zamrud": () => import("./syari-zamrud/demo"),
  "lavender-air": () => import("./lavender-air/demo"),
  "linen-putih": () => import("./linen-putih/demo"),
  "sketsa-tangan": () => import("./sketsa-tangan/demo"),
  "malam-rimba": () => import("./malam-rimba/demo"),
  "pastel-flat": () => import("./pastel-flat/demo"),
  "hijau-ojek": () => import("./hijau-ojek/demo"),
  "pesan-antar": () => import("./pesan-antar/demo"),
  "arena-legenda": () => import("./arena-legenda/demo"),
  "kanal-video": () => import("./kanal-video/demo"),
  "repositori": () => import("./repositori/demo"),
  "pemutar-musik": () => import("./pemutar-musik/demo"),
  "playlist": () => import("./playlist/demo"),
  "chat-hijau": () => import("./chat-hijau/demo"),
  "feed-foto": () => import("./feed-foto/demo"),
  "video-vertikal": () => import("./video-vertikal/demo"),
  "kencan": () => import("./kencan/demo"),
  "peta-rute": () => import("./peta-rute/demo"),
  "surel": () => import("./surel/demo"),
  "dokumen": () => import("./dokumen/demo"),
  "rapat-video": () => import("./rapat-video/demo"),
  "boarding-pass": () => import("./boarding-pass/demo"),
  "tiket-kereta": () => import("./tiket-kereta/demo"),
  "game-retro": () => import("./game-retro/demo"),
  "koran": () => import("./koran/demo"),
  "dompet-digital": () => import("./dompet-digital/demo"),
  "saku-biru": () => import("./saku-biru/demo"),
  "poin-ungu": () => import("./poin-ungu/demo"),
  "kantong-oranye": () => import("./kantong-oranye/demo"),
  "kursi-kereta": () => import("./kursi-kereta/demo"),
  "paket-liburan": () => import("./paket-liburan/demo"),
  "rencana-perjalanan": () => import("./rencana-perjalanan/demo"),
};

/** Themes that render their own music button (the page then skips the generic <MusicPlayer>). */
export const themesWithOwnMusic = new Set(["jawa"]);

/** Theme used for invitations whose template is missing or retired. */
export const FALLBACK_THEME = "linen-putih";

export function isTheme(id?: string): id is string {
  return Boolean(id && Object.hasOwn(loaders, id));
}

const themeComponents = new Map<string, ComponentType<ThemeProps>>();

/** A stable component for theme `id` that renders the client-side, per-theme chunk via <ThemeSwitch>. */
function themeComponent(id: string): ComponentType<ThemeProps> {
  let component = themeComponents.get(id);
  if (!component) {
    const Theme = (props: ThemeProps) => createElement(ThemeSwitch, { ...props, themeId: id });
    Theme.displayName = `Theme(${id})`;
    component = Theme;
    themeComponents.set(id, component);
  }
  return component;
}

/** `{ Theme, demo }` for a theme id; `demo` is a fresh copy of the theme's demo data (server-side). */
export async function loadTheme(id: string) {
  const themeId = isTheme(id) ? id : FALLBACK_THEME;
  const demo = await loaders[themeId]();
  return { Theme: themeComponent(themeId), demo: freshDemo(demo.demo) };
}
