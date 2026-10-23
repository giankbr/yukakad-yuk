"use client";
// Theme "Gathering Kantor" — undangan family gathering dan outbound kantor (bukan pernikahan). Sampul: kartu peserta
// bertali lanyard yang berayun pelan di bawah untaian bendera segitiga, nama tamu tertulis seperti name tag, kelompok
// sebagai pita oranye, panorama perkemahan tepi danau pinus di bawahnya. Hero: panorama gouache Lembang (tenda panitia
// bergaris, tenda dome berpanji, tali tambang, kerucut estafet) dengan papan kayu berisi nama acara. Penyelenggara di
// atas tenda, hitung mundur papan skor, kegiatan per pos, ucapan seperti name tag, donasi doorprize seperti kupon.
// Lukisan dari /tmp/pen/art/themes/gathering-kantor.py.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Big Shoulders Display:wght@700;800", "Figtree:wght@400;600;700;800", "Patrick Hand"];
const Art = makeArt("gathering-kantor", {
  scene: [780, 620], flags: [800, 83], tent: [282, 214], rope: [397, 36], bbq: [237, 304], cone: [92, 96], pines: [219, 254],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Halo, keluarga besar kantor!",
    title: "Waktunya Gathering!",
    sub: "Satu hari, satu tim, satu keluarga besar",
    intro: "Terima kasih untuk kerja keras sepanjang tahun. Kali ini kami mengajak Bapak/Ibu/Saudara/i beserta keluarga untuk sehari penuh bermain, tertawa, dan saling mengenal di tepi danau: senam pagi, outbound keluarga, barbeku, dan doorprize.",
  },
  // The organiser is shown on its own; the second label only matters if a second organiser is filled in.
  roles: ["Penyelenggara", "Panitia"] as [string, string],
  couple: ["dari kami untuk keluarga besar", "Penyelenggara"] as [string, string],
  count: ["bus berangkat dalam", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["catat jadwalnya", "Rangkaian Kegiatan"] as [string, string],
  story: ["dari tahun ke tahun", "Jejak Gathering Kita"] as [string, string],
  gallery: ["kenangan", "Gathering Sebelumnya"] as [string, string],
  wishes: ["daftar ulang", "Konfirmasi Peserta"] as [string, string],
  gifts: ["sukarela", "Donasi Doorprize"] as [string, string],
  closing: {
    thanks: "Sampai Jumpa di Lokasi!",
    text: "Terima kasih sudah menjadi bagian dari tim. Kehadiran Bapak/Ibu/Saudara/i dan keluarga yang membuat hari ini meriah.",
    salam: "Salam satu tim!",
  },
  attend: { yes: "Ikut", maybe: "Masih dicek", no: "Tidak ikut" } as Partial<Record<Attendance, string>>,
  sent: "Data Anda sudah masuk ke panitia. Sampai jumpa di lokasi!",
  wishPlaceholder: "Tulis pesan untuk panitia, misalnya ukuran kaos anak atau kebutuhan khusus…",
  closedNote: "Pendaftaran peserta sudah ditutup. Pesan untuk panitia masih bisa dikirim lewat form ini.",
  giftIntro: "Sifatnya sukarela: bagi yang ingin ikut menyumbang hadiah doorprize atau donasi untuk anak panti di sekitar lokasi, dapat melalui:",
  giftAddressTitle: "Antar Doorprize",
  familyLabel: null,
};

const WISHES = [
  { id: "w1", name: "Rizky (Gudang Cimahi)", attendance: "yes" as Attendance, message: "Ikut berempat, Pak! Anak-anak sudah latihan tarik tambang di rumah. Tim Elang siap juara lagi." },
  { id: "w2", name: "Bu Lestari (Finance)", attendance: "maybe" as Attendance, message: "Masih menunggu jadwal suami, nanti saya kabari paling lambat Jumat. Ukuran kaos anak saya S ya." },
  { id: "w3", name: "Andre (Cabang Garut)", attendance: "yes" as Attendance, message: "Terima kasih panitia! Kami bertiga ikut, bawa kendaraan sendiri dari Garut. Sampai ketemu di Lembang." },
];

export default function GatheringKantorTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Family Gathering";
  const org = data.couple.brideFull?.trim() || data.couple.bride;
  const year = /\d{4}/.exec(data.date ?? "")?.[0];
  const title = year && !label.includes(year) ? `${label} ${year}` : label;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const venue = data.events[0]?.venue || data.place;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#cdebf2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverFlags} aria-hidden><Art name="flags" eager /></span>
          <div className={s.badgeSwing}>
            <span className={s.lanyard} aria-hidden />
            <div className={s.badge}>
              <div className={s.badgeHead}>
                <small>Kartu Peserta</small>
                <h1>{title}</h1>
                <p>{org}</p>
              </div>
              <div className={s.badgeBody}>
                <div className={s.guest}>
                  <small>Nama peserta</small>
                  <strong>{guestLabel(data)}</strong>
                  {table && <span className={s.table}>{table}</span>}
                </div>
                <div className={s.badgeMeta}>
                  <div><span>Tanggal</span><b>{formatDate(data.date)}</b></div>
                  <div><span>Lokasi</span><b>{venue}</b></div>
                </div>
              </div>
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#ffffff" />Buka Undangan</button>
          <Art name="scene" eager className={s.coverScene} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#f6c945"
        dark="#22312b"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroScene} aria-hidden>
              <Art name="scene" />
              <span className={s.heroFlags}><Art name="flags" /></span>
            </div>
            <div className={s.sign}>
              <p className={s.heroKicker}>Undangan untuk karyawan & keluarga</p>
              <h1 className={s.heroTitle}>{title}</h1>
              <p className={s.heroOrg}>{org}</p>
              <div className={s.heroMeta}><span>{formatDate(data.date)}</span>{venue && <span>{venue}</span>}</div>
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="rope" className={s.divider} />,
          node: <Art name="cone" />,
          portrait: <span className={s.orgArt} aria-hidden><Art name="tent" /></span>,
          countDecor: <><Art name="pines" className={s.countPines} /><Art name="pines" className={`${s.countPines} ${s.countPinesR}`} /></>,
          closingEmblem: <div className={s.closeSet} aria-hidden><Art name="tent" /><Art name="bbq" className={s.closeBbq} /></div>,
          sentArt: <Art name="tent" />,
        }}
      />
    </ThemeShell>
  );
}
