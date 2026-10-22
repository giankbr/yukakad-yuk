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
  "mawar-blush": () => import("./mawar-blush/demo"),
  "emas-hitam": () => import("./emas-hitam/demo"),
  "rustic-kayu": () => import("./rustic-kayu/demo"),
  "taman-eukaliptus": () => import("./taman-eukaliptus/demo"),
  "surat-vintage": () => import("./surat-vintage/demo"),
  "marmer-rosegold": () => import("./marmer-rosegold/demo"),
  "langit-navy": () => import("./langit-navy/demo"),
  "boho-terakota": () => import("./boho-terakota/demo"),
  "pantai-senja": () => import("./pantai-senja/demo"),
  "editorial-monokrom": () => import("./editorial-monokrom/demo"),
  "kaligrafi-emas": () => import("./kaligrafi-emas/demo"),
  "masjid-biru": () => import("./masjid-biru/demo"),
  "sakinah-putih": () => import("./sakinah-putih/demo"),
  "arabesque-marun": () => import("./arabesque-marun/demo"),
  "lentera-malam": () => import("./lentera-malam/demo"),
  "mihrab-pastel": () => import("./mihrab-pastel/demo"),
  "sunda-siger": () => import("./sunda-siger/demo"),
  "batak-ulos": () => import("./batak-ulos/demo"),
  "bugis-bosara": () => import("./bugis-bosara/demo"),
  "betawi-ondel": () => import("./betawi-ondel/demo"),
  "melayu-songket": () => import("./melayu-songket/demo"),
  "toraja-tongkonan": () => import("./toraja-tongkonan/demo"),
  "dayak-borneo": () => import("./dayak-borneo/demo"),
  "palembang-aesan": () => import("./palembang-aesan/demo"),
  "joglo-marun": () => import("./joglo-marun/demo"),
  "kawung-biru": () => import("./kawung-biru/demo"),
  "gebyok-sogan": () => import("./gebyok-sogan/demo"),
  "busana-jawi": () => import("./busana-jawi/demo"),
  "wayang-mega": () => import("./wayang-mega/demo"),
  "kereta-kencana": () => import("./kereta-kencana/demo"),
  "madura-sakera": () => import("./madura-sakera/demo"),
  "lampung-tapis": () => import("./lampung-tapis/demo"),
  "aceh-pintu": () => import("./aceh-pintu/demo"),
  "papua-cendrawasih": () => import("./papua-cendrawasih/demo"),
  "ntt-tenun": () => import("./ntt-tenun/demo"),
  "banjar-sasirangan": () => import("./banjar-sasirangan/demo"),
  "zellige-hijau": () => import("./zellige-hijau/demo"),
  "andalusia-terakota": () => import("./andalusia-terakota/demo"),
  "tasbih-mutiara": () => import("./tasbih-mutiara/demo"),
  "hijrah-senja": () => import("./hijrah-senja/demo"),
  "iznik-tulip": () => import("./iznik-tulip/demo"),
  "taman-persia": () => import("./taman-persia/demo"),
  "deco-sampanye": () => import("./deco-sampanye/demo"),
  "terrazzo-modern": () => import("./terrazzo-modern/demo"),
  "sakura-sumi": () => import("./sakura-sumi/demo"),
  "kebun-tropis": () => import("./kebun-tropis/demo"),
  "herbarium-klasik": () => import("./herbarium-klasik/demo"),
  "telaga-kabut": () => import("./telaga-kabut/demo"),
  "perak-kenangan": () => import("./perak-kenangan/demo"),
  "ultah-dino": () => import("./ultah-dino/demo"),
  "baby-shower-awan": () => import("./baby-shower-awan/demo"),
  "walimatus-safar": () => import("./walimatus-safar/demo"),
  "reuni-sekolah": () => import("./reuni-sekolah/demo"),
  "sweet-seventeen": () => import("./sweet-seventeen/demo"),
  "minahasa-kawanua": () => import("./minahasa-kawanua/demo"),
  "gorontalo-karawo": () => import("./gorontalo-karawo/demo"),
  "nias-omo": () => import("./nias-omo/demo"),
  "sasak-lombok": () => import("./sasak-lombok/demo"),
  "mandar-sandeq": () => import("./mandar-sandeq/demo"),
  "jambi-angso": () => import("./jambi-angso/demo"),
  "mashrabiya-kayu": () => import("./mashrabiya-kayu/demo"),
  "mughal-marmer": () => import("./mughal-marmer/demo"),
  "oasis-kurma": () => import("./oasis-kurma/demo"),
  "masjid-tajug": () => import("./masjid-tajug/demo"),
  "anyelir-syari": () => import("./anyelir-syari/demo"),
  "samarkand-biru": () => import("./samarkand-biru/demo"),
  "boho-pampas": () => import("./boho-pampas/demo"),
  "hydrangea-biru": () => import("./hydrangea-biru/demo"),
  "riso-cetak": () => import("./riso-cetak/demo"),
  "kaca-patri": () => import("./kaca-patri/demo"),
  "delft-biru": () => import("./delft-biru/demo"),
  "origami-bangau": () => import("./origami-bangau/demo"),
  "ultah-antariksa": () => import("./ultah-antariksa/demo"),
  "aqiqah-domba": () => import("./aqiqah-domba/demo"),
  "khataman-quran": () => import("./khataman-quran/demo"),
  "tedak-siten": () => import("./tedak-siten/demo"),
  "halal-bihalal": () => import("./halal-bihalal/demo"),
  "purna-tugas": () => import("./purna-tugas/demo"),
  "bengkulu-rafflesia": () => import("./bengkulu-rafflesia/demo"),
  "maluku-tifa": () => import("./maluku-tifa/demo"),
  "sumbawa-samawa": () => import("./sumbawa-samawa/demo"),
  "peranakan-merah": () => import("./peranakan-merah/demo"),
  "osing-gajah-oling": () => import("./osing-gajah-oling/demo"),
  "buton-wolio": () => import("./buton-wolio/demo"),
  "lampu-mosaik": () => import("./lampu-mosaik/demo"),
  "hadramaut-tanah": () => import("./hadramaut-tanah/demo"),
  "melati-syari": () => import("./melati-syari/demo"),
  "kaftan-ottoman": () => import("./kaftan-ottoman/demo"),
  "istana-maimun": () => import("./istana-maimun/demo"),
  "langit-subuh": () => import("./langit-subuh/demo"),
  "zaitun-tuscan": () => import("./zaitun-tuscan/demo"),
  "santorini-putih": () => import("./santorini-putih/demo"),
  "neon-malam": () => import("./neon-malam/demo"),
  "marmer-ebru": () => import("./marmer-ebru/demo"),
  "padang-liar": () => import("./padang-liar/demo"),
  "batik-kontemporer": () => import("./batik-kontemporer/demo"),
  "ultah-unicorn": () => import("./ultah-unicorn/demo"),
  "ultah-bola": () => import("./ultah-bola/demo"),
  "wisuda-tk": () => import("./wisuda-tk/demo"),
  "syukuran-kelahiran": () => import("./syukuran-kelahiran/demo"),
  "ultah-sepuh": () => import("./ultah-sepuh/demo"),
  "natal-keluarga": () => import("./natal-keluarga/demo"),
  "khitan-ceria": () => import("./khitan-ceria/demo"),
  "aqiqah-bintang": () => import("./aqiqah-bintang/demo"),
  "ultah-balon": () => import("./ultah-balon/demo"),
  "ultah-gemerlap": () => import("./ultah-gemerlap/demo"),
  "syukuran-rumah": () => import("./syukuran-rumah/demo"),
  "lamaran-cincin": () => import("./lamaran-cincin/demo"),
  "wisuda-toga": () => import("./wisuda-toga/demo"),
  "tujuh-bulanan": () => import("./tujuh-bulanan/demo"),
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
