// Built-in background music the couple can pick in Dashboard → Tema & Musik (and that theme demos play).
// Files live in /public/music; the invitation stores the path as settings.music_url like an uploaded track.
// Every track must be ours to ship: synthesized in tools/audio, or a recording whose licence allows commercial,
// in-product use (record it in `credit` / `license` and keep the proof link in `source`).
import type { Mood } from "@/components/invitation/themes/mood";

export type LibraryTrack = {
  id: string;
  mood: Mood;
  title: string;
  /** Short description shown under the title in the dashboard. */
  note: string;
  file: string;
  bpm?: number;
  /** Performer / author, when the licence asks for (or we want to show) credit. */
  credit?: string;
  license?: string;
  source?: string;
};

export const MUSIC_LIBRARY: LibraryTrack[] = [
  { id: "romantis", mood: "romantis", title: "Piano Romantis", note: "Piano lembut untuk pernikahan modern & klasik", file: "/music/demo/romantis.mp3", bpm: 70 },
  { id: "gamelan", mood: "gamelan", title: "Gamelan Keraton", note: "Gamelan tenang untuk adat Jawa, Bali, Sunda", file: "/music/demo/gamelan.mp3", bpm: 60 },
  { id: "nusantara", mood: "nusantara", title: "Kecapi Nusantara", note: "Petikan pentatonik untuk adat Nusantara", file: "/music/demo/nusantara.mp3", bpm: 72 },
  { id: "religi", mood: "religi", title: "Doa & Harapan", note: "Tanpa perkusi, tenang untuk undangan islami", file: "/music/demo/religi.mp3", bpm: 60 },
  { id: "akustik", mood: "akustik", title: "Petikan Akustik", note: "Gitar hangat untuk garden, rustic, pantai", file: "/music/demo/akustik.mp3", bpm: 84 },
  { id: "ceria", mood: "ceria", title: "Ceria", note: "Marimba riang untuk ulang tahun & acara anak", file: "/music/demo/ceria.mp3", bpm: 112 },
  { id: "khidmat", mood: "khidmat", title: "Khidmat", note: "Piano & gesek untuk wisuda, pelantikan, ibadah", file: "/music/demo/khidmat.mp3", bpm: 76 },
  // Licensed recordings (sources and proof in tools/audio/LICENSES.md).
  { id: "chopin-nocturne", mood: "romantis", title: "Nocturne Op. 9 No. 2", note: "Chopin, piano klasik yang lembut", file: "/music/library/chopin-nocturne.mp3", credit: "Frank Levy", license: "Domain publik", source: "https://commons.wikimedia.org/wiki/File:Nocturne_in_E_flat_major,_Op._9_no._2.mp3" },
  { id: "satie-gymnopedie", mood: "romantis", title: "Gymnopédie No. 1", note: "Satie, piano pelan dan tenang", file: "/music/library/satie-gymnopedie.mp3", license: "CC0", source: "https://commons.wikimedia.org/wiki/File:Gymnopedie_No._1..ogg" },
  { id: "canon-pachelbel", mood: "khidmat", title: "Canon in D", note: "Pachelbel, gesek untuk prosesi & akad", file: "/music/library/canon-pachelbel.mp3", credit: "USAF Strolling Strings", license: "Domain publik", source: "https://commons.wikimedia.org/wiki/File:Canon_(2004)_-_Strolling_Strings_-_United_States_Air_Force_Band.mp3" },
  { id: "pomp-circumstance", mood: "khidmat", title: "Pomp and Circumstance", note: "Elgar, mars wisuda", file: "/music/library/pomp-circumstance.mp3", credit: "US Marine Band", license: "Domain publik", source: "https://commons.wikimedia.org/wiki/File:ELGAR_Pomp_and_Circumstance_in_D,_Opus_39,_No._1_-_United_States_Marine_Band.mp3" },
  { id: "gamelan-bali", mood: "gamelan", title: "Gamelan Bali", note: "Rekaman gamelan Bali yang tenang", file: "/music/library/gamelan-bali.mp3", license: "CC0", source: "https://commons.wikimedia.org/wiki/File:Bali_xylophone.ogg" },
  { id: "gender-wayang", mood: "gamelan", title: "Gendér Wayang (1928)", note: "Rekaman piringan hitam Bali, nuansa antik", file: "/music/library/gender-wayang.mp3", credit: "Gendér Wajang of Kuta", license: "Domain publik", source: "https://commons.wikimedia.org/wiki/File:Gend%C3%A9r_Wayang_(1928).ogg" },
  { id: "hujan-alam", mood: "religi", title: "Hujan & Kicau Burung", note: "Suara alam tanpa alat musik", file: "/music/library/hujan-alam.mp3", license: "CC0", source: "https://freesound.org/people/thinkingfish/sounds/693699/" },
  { id: "senandung", mood: "religi", title: "Senandung", note: "Senandung suara tanpa alat musik", file: "/music/library/senandung.mp3", credit: "Andrewfai", license: "Pixabay", source: "https://pixabay.com/music/vocal-vocal-mmms-213611/" },
  { id: "morning-garden", mood: "akustik", title: "Morning Garden", note: "Petikan gitar akustik yang hangat", file: "/music/library/morning-garden.mp3", credit: "folk_acoustic", license: "Pixabay", source: "https://pixabay.com/music/acoustic-group-morning-garden-acoustic-chill-15013/" },
  { id: "ukulele-ceria", mood: "ceria", title: "Happy Ukulele", note: "Ukulele & siulan, riang untuk anak", file: "/music/library/ukulele-ceria.mp3", credit: "virtuosound", license: "Pixabay", source: "https://pixabay.com/music/upbeat-happy-ukulele-song-8347/" },
];

/** The library track stored in an invitation's music_url, if it is one. */
export function libraryTrack(url?: string) {
  if (!url) return undefined;
  return MUSIC_LIBRARY.find(track => track.file === url);
}

/** The default track for a mood (first library entry with that mood). */
export function trackForMood(mood: Mood) {
  return MUSIC_LIBRARY.find(track => track.mood === mood) ?? MUSIC_LIBRARY[0];
}
