// Motion personality per theme. ThemeShell sets `data-motion` on the invitation root and globals.css maps it to
// easing / duration / distance tokens (--m-*), so reveals, presses, sheets and celebrations feel like the theme:
//   elegant — classic & adat themes: slow, soft, blur-in, no overshoot
//   playful — app & social themes: springy overshoot, pop-in, confetti
//   crisp   — document / productivity themes: short, precise, no bounce
export type MotionStyle = "elegant" | "playful" | "crisp";

const ELEGANT = new Set([
  "mawar-blush", "emas-hitam", "rustic-kayu", "taman-eukaliptus", "surat-vintage", "marmer-rosegold", "langit-navy", "boho-terakota", "pantai-senja", "kaligrafi-emas", "masjid-biru", "sakinah-putih", "arabesque-marun", "lentera-malam", "mihrab-pastel", "sunda-siger", "batak-ulos", "bugis-bosara", "betawi-ondel", "melayu-songket", "toraja-tongkonan", "dayak-borneo", "palembang-aesan", "syukuran-rumah", "lamaran-cincin", "tujuh-bulanan",
  "madura-sakera", "lampung-tapis", "aceh-pintu", "papua-cendrawasih", "ntt-tenun", "banjar-sasirangan", "zellige-hijau", "andalusia-terakota", "tasbih-mutiara", "hijrah-senja", "iznik-tulip", "taman-persia", "deco-sampanye", "terrazzo-modern", "sakura-sumi", "kebun-tropis", "herbarium-klasik", "telaga-kabut", "perak-kenangan", "walimatus-safar", "minahasa-kawanua", "gorontalo-karawo", "nias-omo", "sasak-lombok", "mandar-sandeq", "jambi-angso", "mashrabiya-kayu", "mughal-marmer", "oasis-kurma", "masjid-tajug", "anyelir-syari", "samarkand-biru", "boho-pampas", "hydrangea-biru", "riso-cetak", "kaca-patri", "delft-biru", "origami-bangau", "khataman-quran", "tedak-siten", "purna-tugas", "bengkulu-rafflesia", "maluku-tifa", "sumbawa-samawa", "peranakan-merah", "osing-gajah-oling", "buton-wolio", "lampu-mosaik", "hadramaut-tanah", "melati-syari", "kaftan-ottoman", "istana-maimun", "langit-subuh", "zaitun-tuscan", "santorini-putih", "marmer-ebru", "padang-liar", "batik-kontemporer", "ultah-sepuh", "joglo-marun", "kawung-biru", "gebyok-sogan", "busana-jawi", "wayang-mega", "kereta-kencana", "jawa", "rumah-gadang", "bali-kuning", "syari-zamrud", "lavender-air", "linen-putih", "sketsa-tangan", "malam-rimba",
]);
const CRISP = new Set(["editorial-monokrom", "wisuda-toga", "dokumen", "surel", "koran", "repositori", "rapat-video", "peta-rute", "rencana-perjalanan"]);

export function motionOf(themeId?: string): MotionStyle {
  if (!themeId) return "elegant";
  if (ELEGANT.has(themeId)) return "elegant";
  if (CRISP.has(themeId)) return "crisp";
  return "playful";
}
