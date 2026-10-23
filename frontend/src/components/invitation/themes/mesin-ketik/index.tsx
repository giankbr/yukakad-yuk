"use client";
// Theme "Mesin Ketik" — surat cinta yang diketik: sampul berupa lembar kertas yang keluar dari mesin ketik tua berenamel
// hijau sage (lukisan gouache orisinal, tanpa merek), nama yang terketik huruf demi huruf, tinta pita merah-hitam tak
// rata, salinan karbon untuk hitung mundur, kartu indeks bergaris, klip kertas dan cap karet.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Special Elite", "Courier Prime:ital,wght@0,400;0,700;1,400", "Mrs Saint Delafield"];
// Painted by /tmp/pen/art/themes/mesin-ketik.py.
const Art = makeArt("mesin-ketik", { machine: [760, 513], spool: [120, 119], ribbon: [400, 40], clip: [40, 178] } as const);

const WISHES = [
  { id: "w1", name: "Ibu Dra. Sri Rahayu", attendance: "yes" as const, message: "Selamat untuk Lintang dan Bayu. Dari seratus dua belas amplop menjadi satu rumah, semoga surat-surat kalian tak pernah berhenti." },
  { id: "w2", name: "Komunitas Sahabat Pena Malang", attendance: "yes" as const, message: "Kami bawa kartu pos paling bagus. Selamat menempuh hidup baru, semoga selalu saling menulis dan saling membaca." },
  { id: "w3", name: "Dimas & Ayu", attendance: "maybe" as const, message: "Mungkin terlambat karena kereta dari Surabaya, tapi doa kami sudah sampai lebih dulu. Bahagia selalu!" },
];

export default function MesinKetikTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const city = data.address?.match(/Kota\s+([A-Za-z]+)/)?.[1] ?? "";
  const hero = data.gallery[0];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#232b2a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.sheet}>
            <p className={s.sheetTop}><span>{city ? `${city}, ` : ""}{formatDate(data.date)}</span><span>No. 01</span></p>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>
              <span className={s.typeLine}>{data.couple.bride}</span>
              <span className={s.typeLine}>&amp;</span>
              <span className={s.typeLine}>{data.couple.groom}</span>
            </h1>
            <p className={s.typedNote}>Dengan hormat, kami mengundang Anda untuk hadir di hari bahagia kami.</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#b3261e" />Buka Surat</button>
          </div>
          <div className={s.machineWrap} aria-hidden>
            <Art name="machine" eager className={s.machine} />
            <Art name="spool" eager className={s.spoolL} />
            <Art name="spool" eager className={s.spoolR} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbf7ec"
        dark="#232126"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Halaman pertama",
            title: "Kepada yang kami sayangi,",
            intro: "Dengan segala kerendahan hati dan rasa syukur, kami bermaksud menyatukan dua cerita menjadi satu. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Lampiran I", "Kedua Mempelai"],
          count: ["Salinan karbon", "Menuju Hari Bahagia"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Lampiran II", "Waktu & Tempat"],
          story: ["Arsip surat", "Cerita Kami"],
          gallery: ["Lampiran III", "Potret & Kenangan"],
          wishes: ["Surat balasan", "Ucapan & Kehadiran"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: { thanks: "Hormat kami,", text: "Terima kasih telah membaca surat ini sampai halaman terakhir. Kehadiran dan doa Anda adalah balasan terindah bagi kami." },
          sent: "Surat balasan Anda sudah kami terima. Terima kasih!",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Ketik ucapan dan doa untuk kedua mempelai…",
          closedNote: "Terima kasih atas doa dan perhatiannya. Surat balasan masih bisa dikirim lewat form ini.",
          giftIntro: "Doa restu Anda adalah hadiah terindah. Bila ingin memberi tanda kasih, dapat melalui:",
          giftAddressTitle: "Kirim Kado via Pos",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.heroPhotoWrap}>
                <Art name="clip" className={s.heroClip} />
                <div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} dan ${data.couple.groom}`} /></div>
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
            <p className={s.heroSign} aria-hidden>{data.couple.bride} &amp; {data.couple.groom}</p>
          </header>
        )}
        slots={{
          divider: <Art name="ribbon" className={s.divider} />,
          node: <Art name="spool" />,
          amp: <Art name="spool" />,
          portrait: <Art name="clip" />,
          closingEmblem: <Art name="machine" className={s.closingEmblem} />,
          sentArt: <Art name="clip" />,
        }}
      />
    </ThemeShell>
  );
}
