"use client";
// Theme "Khitanan Massal" — undangan khitanan massal dari panitia sosial, bergaya gouache ceria: tenda bergaris hijau-putih
// berumbai kuning, spanduk acara yang tergantung di bawahnya, tiga anak bersarung dan berpeci yang melambai (ilustrasi
// bergaya, tanpa citra medis), tumpukan bingkisan, balon dan bendera untai. Penyelenggara adalah panitia (bride = yayasan,
// groom = mitra), kisah berisi susunan program, konfirmasi berupa pendaftaran anak, dan amplop menjadi donasi.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Baloo 2:wght@600;700;800", "Plus Jakarta Sans:wght@400;500;600;700;800", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/khitanan-massal.py (bunting is also a CSS background)
const Art = makeArt("khitanan-massal", { tent: [780, 314], kids: [702, 351], balloons: [200, 351], gift: [120, 124], bunting: [400, 41] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Khitan Bersama, Bahagia Bersama",
    intro: "Dengan mengharap rida Allah, kami mengundang Bapak/Ibu untuk mendaftarkan putranya dalam program khitanan massal gratis, sekaligus mengajak para dermawan untuk ikut menyukseskan dan mendoakan anak-anak kita.",
  },
  roles: ["Penyelenggara", "Bekerja Sama dengan"],
  couple: ["Dari Kami", "Panitia Pelaksana"],
  count: ["Acara dimulai dalam", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat Tanggalnya", "Jadwal Kegiatan"],
  story: ["Alur Acara", "Susunan Program"],
  gallery: ["Dokumentasi", "Kegiatan Sebelumnya"],
  wishes: ["Daftar Sekarang", "Pendaftaran Anak"],
  gifts: ["Ikut Berbagi", "Salurkan Donasi"],
  closing: {
    thanks: "Jazakumullahu Khairan",
    text: "Terima kasih kepada para orang tua, relawan, dan donatur. Semoga Allah memberkahi anak-anak kita, menjadikan mereka saleh, sehat, dan berbakti.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Terima kasih! Pendaftaran dan pesan Anda sudah diterima panitia.",
  attend: { yes: "Daftar", maybe: "Insyaallah", no: "Tidak Ikut" },
  wishLabel: "Pesan untuk Panitia",
  wishPlaceholder: "Tulis pertanyaan, doa, atau pesan untuk panitia…",
  closedNote: "Pendaftaran peserta sudah ditutup. Terima kasih, doa dan pesan masih bisa dikirim lewat form ini.",
  giftIntro: "Donasi digunakan untuk biaya tindakan khitan, bingkisan, sarung, peci, dan uang saku anak-anak. Berapa pun nilainya, semoga menjadi amal jariyah:",
  guestsLabel: "Jumlah anak",
  giftAddressTitle: "Donasi Barang",
  familyLabel: null,
};

const WISHES = [
  { id: "w1", name: "Ibu Sumiati (orang tua Raka)", attendance: "yes" as Attendance, message: "Alhamdulillah, Raka sudah lama ingin dikhitan. Terima kasih panitia, semoga menjadi amal jariyah untuk semuanya." },
  { id: "w2", name: "Bapak H. Rahmat, donatur", attendance: "yes" as Attendance, message: "Semoga lancar dan anak-anak cepat pulih. Insyaallah kami bantu konsumsi untuk relawan." },
  { id: "w3", name: "Remaja Masjid Al-Ikhlas", attendance: "maybe" as Attendance, message: "Tim marawis siap tampil! Kami juga bisa bantu mendampingi adik-adik di ruang tunggu." },
];

export default function KhitananMassalTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const host = data.couple.bride?.trim() || "Panitia";
  const title = data.eventLabel?.trim() || "Khitanan Massal";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#cfeef5"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="tent" eager className={s.tent} />
          <div className={s.spanduk}>
            <p className={s.org}>{host} mengundang</p>
            <h1 className={s.title}>{title}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <Art name="balloons" eager className={s.balloonL} />
          <Art name="balloons" eager className={s.balloonR} />
          <Art name="kids" eager className={s.kids} />
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        celebrant
        noPhotos
        demoWishes={WISHES}
        light="#fff1bf"
        dark="#1f7a50"
        hero={(
          <header className={s.hero}>
            <Art name="bunting" className={s.heroBunting} />
            <p className={s.heroOrg}>{host}</p>
            <h1 className={s.heroTitle}>{title}</h1>
            <Art name="kids" className={s.heroKids} />
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.chips} aria-label="Yang didapat peserta">
              <span>Gratis</span><span>Sarung &amp; Peci</span><span>Bingkisan</span><span>Uang Saku</span>
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="bunting" className={s.divider} />,
          node: <Art name="gift" />,
          portrait: <Art name="gift" className={s.portraitGift} />,
          countDecor: <><span className={s.countBunting} aria-hidden /><Art name="balloons" className={s.countBalloon} /></>,
          closingDecor: <span className={s.closingBunting} aria-hidden />,
          closingEmblem: <Art name="balloons" className={s.emblem} />,
          sentArt: <Art name="gift" />,
        }}
      />
    </ThemeShell>
  );
}
