"use client";
// Per-theme code splitting. Each theme is its own `next/dynamic` chunk, so a guest only downloads the
// theme their invitation uses (plus the shared kit). Rendered on the server too (ssr default), and Next
// preloads the chunk that was used during SSR, so there's no flash on hydration.
// Generated from the ids in registry.ts — keep both lists in sync when adding a theme.
import dynamic from "next/dynamic";
import type { ComponentType } from "react";
import type { ThemeProps } from "./kit";

const themes: Record<string, ComponentType<ThemeProps>> = {
  "marketplace": dynamic(() => import("./marketplace")),
  "oranye": dynamic(() => import("./oranye")),
  "streaming": dynamic(() => import("./streaming")),
  "jawa": dynamic(() => import("./jawa")),
  "rumah-gadang": dynamic(() => import("./rumah-gadang")),
  "bali-kuning": dynamic(() => import("./bali-kuning")),
  "syari-zamrud": dynamic(() => import("./syari-zamrud")),
  "lavender-air": dynamic(() => import("./lavender-air")),
  "linen-putih": dynamic(() => import("./linen-putih")),
  "sketsa-tangan": dynamic(() => import("./sketsa-tangan")),
  "malam-rimba": dynamic(() => import("./malam-rimba")),
  "pastel-flat": dynamic(() => import("./pastel-flat")),
  "hijau-ojek": dynamic(() => import("./hijau-ojek")),
  "pesan-antar": dynamic(() => import("./pesan-antar")),
  "arena-legenda": dynamic(() => import("./arena-legenda")),
  "kanal-video": dynamic(() => import("./kanal-video")),
  "repositori": dynamic(() => import("./repositori")),
  "pemutar-musik": dynamic(() => import("./pemutar-musik")),
  "playlist": dynamic(() => import("./playlist")),
  "chat-hijau": dynamic(() => import("./chat-hijau")),
  "feed-foto": dynamic(() => import("./feed-foto")),
  "video-vertikal": dynamic(() => import("./video-vertikal")),
  "kencan": dynamic(() => import("./kencan")),
  "peta-rute": dynamic(() => import("./peta-rute")),
  "surel": dynamic(() => import("./surel")),
  "dokumen": dynamic(() => import("./dokumen")),
  "rapat-video": dynamic(() => import("./rapat-video")),
  "boarding-pass": dynamic(() => import("./boarding-pass")),
  "tiket-kereta": dynamic(() => import("./tiket-kereta")),
  "game-retro": dynamic(() => import("./game-retro")),
  "koran": dynamic(() => import("./koran")),
  "dompet-digital": dynamic(() => import("./dompet-digital")),
  "saku-biru": dynamic(() => import("./saku-biru")),
  "poin-ungu": dynamic(() => import("./poin-ungu")),
  "kantong-oranye": dynamic(() => import("./kantong-oranye")),
  "kursi-kereta": dynamic(() => import("./kursi-kereta")),
  "paket-liburan": dynamic(() => import("./paket-liburan")),
  "rencana-perjalanan": dynamic(() => import("./rencana-perjalanan")),
};

/** Renders the theme `themeId` (falls back to Linen Putih for unknown ids). */
export default function ThemeSwitch({ themeId, ...props }: ThemeProps & { themeId: string }) {
  const Theme = themes[themeId] ?? themes["linen-putih"];
  return <Theme {...props} />;
}
