"use client";
// Theme "Lomba Layangan" — undangan festival layang-layang di pantai (komunitas rekaan), poster guas yang ceria: langit
// biru berawan, laut toska, pasir dengan umbul-umbul dan tenda panitia. Layangan wajik berekor pita, layangan ikan,
// delta pelangi, dan layangan kotak bergoyang di talinya masing-masing. Kartu tamu berupa nomor dada peserta, panitia
// di bingkai layangan wajik, hitung mundur di ubin wajik, jadwal ditarik benang dari kaleng, biaya pendaftaran sebagai
// amplop, penutup langit penuh layangan di atas pasir.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Titan One", "Lexend:wght@400;500;600;700;800", "Gochi Hand"];
// Painted by /tmp/pen/art/themes/lomba-layangan.py
const Art = makeArt("lomba-layangan", {
  wajik: [210, 1042], ikan: [260, 580], delta: [240, 667], kotak: [180, 1027], bunting: [380, 49], mini: [84, 132],
} as const);

const WISHES = [
  { id: "w1", name: "Tim Garuda Biru", attendance: "yes" as const, message: "Layangan ikan sepanjang tiga meter sudah siap terbang. Tahun ini piala bergilir harus pulang ke RT kami!" },
  { id: "w2", name: "Bu Ratna & cucu-cucu", attendance: "maybe" as const, message: "Kami datang menonton sambil ikut kelas membuat layangan. Semoga anginnya bersahabat dan cuacanya cerah." },
  { id: "w3", name: "Dika, peserta pemula", attendance: "yes" as const, message: "Pertama kali ikut lomba. Layangan wajik buatan sendiri, ekornya dari pita bekas hajatan. Doakan terbang tinggi ya!" },
];

export default function LombaLayanganTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const host = data.couple.bride?.trim() || "Panitia";
  const title = data.eventLabel?.trim() || "Lomba Layangan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3d9be0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.kites} aria-hidden>
            <Art name="wajik" eager className={s.kWajik} />
            <Art name="ikan" eager className={s.kIkan} />
            <Art name="delta" eager className={s.kDelta} />
            <Art name="kotak" eager className={s.kKotak} />
          </div>
          <p className={s.badge}>Undangan Festival</p>
          <p className={s.host}>{host} mengundang</p>
          <h1 className={s.title}>{title}</h1>
          <p className={s.when}>{formatDate(data.date)}</p>
          <span className={s.spacer} aria-hidden />
          <div className={s.bib}>
            <p className={s.bibHead}><span>Kartu Undangan</span>{table && <span>{table}</span>}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#ffffff"
        dark="#1d2b4f"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Halo, para pecinta langit!",
            title: "Ayo Warnai Langit Bersama",
            intro: "Kami mengundang warga, komunitas, dan keluarga untuk meramaikan festival layang-layang di pantai: daftar sebagai peserta lomba, ikut kelas membuat layangan, atau datang menonton sambil menikmati angin laut.",
          },
          roles: ["Penyelenggara", "Bekerja sama dengan"],
          couple: ["Di balik festival", "Panitia"],
          count: ["Angin sudah berembus", "Menuju Hari Festival"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat tanggalnya", "Hari Festival"],
          story: ["Dari pagi sampai sore", "Jadwal Acara"],
          gallery: ["Dokumentasi", "Festival Tahun Lalu"],
          wishes: ["Konfirmasi & pesan", "Daftar Hadir"],
          gifts: ["Pendaftaran & donasi", "Biaya Pendaftaran"],
          closing: {
            thanks: "Sampai Jumpa di Pantai!",
            text: "Terima kasih untuk setiap peserta, penonton, relawan, dan warga yang membantu. Siapa pun juaranya, langit hari itu milik kita bersama.",
            salam: "Salam angin laut, panitia",
          },
          sent: "Siap! Konfirmasi dan pesanmu sudah diterima panitia.",
          attend: { yes: "Peserta", maybe: "Penonton", no: "Berhalangan" },
          wishLabel: "Pesan untuk panitia",
          wishPlaceholder: "Tulis kategori lomba, nama tim, atau pesan untuk panitia…",
          closedNote: "Pendaftaran peserta sudah ditutup. Terima kasih atas antusiasmenya, pesan semangat masih bisa dikirim lewat form ini.",
          giftIntro: "Biaya pendaftaran Rp20.000 per layangan (pelajar Rp10.000), sudah termasuk nomor dada, air minum, dan sertifikat. Donasi untuk hadiah juga sangat kami hargai:",
          giftAddressTitle: "Donasi Bahan & Hadiah",
          familyLabel: null,
        }}
        hero={(
          <header className={s.hero}>
            <Art name="bunting" className={s.heroBunting} />
            <p className={s.heroKicker}>{host} mempersembahkan</p>
            <h1 className={s.heroTitle}>{title}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.chips} aria-hidden>
              <span>Layangan Tradisional</span>
              <span>Layangan Kreasi</span>
              <span>Kelas Membuat</span>
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.heroKites} aria-hidden>
              <Art name="wajik" className={s.h1} />
              <Art name="delta" className={s.h2} />
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="bunting" className={s.divider} />,
          node: <Art name="mini" />,
          countDecor: null,
          closingDecor: (
            <div className={s.closingSky} aria-hidden>
              <Art name="wajik" className={s.k1} />
              <Art name="ikan" className={s.k2} />
              <Art name="delta" className={s.k3} />
            </div>
          ),
          sentArt: <Art name="ikan" />,
        }}
      />
    </ThemeShell>
  );
}
