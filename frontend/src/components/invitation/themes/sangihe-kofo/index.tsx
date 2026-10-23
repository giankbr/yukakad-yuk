"use client";
// Theme "Sangihe Kofo" — tenun kofo dari serat pisang abaka Sangihe: garis lungsin halus berwarna alam, karat dan nila
// membingkai lukisan pulau gunung api yang menjulang dari laut biru, lengkap dengan perahu bercadik. Kartu berpinggir
// tenun, potret berselendang kofo, laut dalam di pita hitung mundur. Gerak tenang: perahu terayun, asap gunung mengepul.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Marcellus SC", "Della Respira", "Cormorant Upright:wght@500;600"];
// Painted by /tmp/pen/art/themes/sangihe-kofo.py.
const Art = makeArt("sangihe-kofo", { scene: [780, 1500], boat: [300, 144], smoke: [300, 195], divider: [360, 36], node: [96, 104] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Hendro Pandensolang", attendance: "yes" as const, message: "Selamat menempuh hidup baru, Febiola dan Rivaldo. Tuhan Yesus memberkati rumah tangga kalian, kuat seperti kofo yang ditenun rapat." },
  { id: "w2", name: "Pemuda GMIST Imanuel", attendance: "yes" as const, message: "Selamat ya, Kakak berdua! Sampai jumpa di Tahuna, kami siap bermasamper sampai malam." },
  { id: "w3", name: "Tante Meiske di Bitung", attendance: "maybe" as const, message: "Belum pasti bisa menyeberang, tapi doa kami menyertai. Kasih Tuhan selalu menaungi kalian." },
];

export default function SangiheKofoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const photo = data.gallery[0] ?? data.couple.bridePhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f5ecd8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.sceneWrap} aria-hidden>
            <Art name="scene" eager className={s.scene} />
            <Art name="smoke" eager className={s.smoke} />
            <Art name="boat" eager className={s.boat} />
          </div>
          <p className={s.syalom}>Syalom</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#12304f" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f1e3bf"
        dark="#12304f"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Syalom",
            title: "Dalam Kasih Tuhan",
            sub: "“Demikianlah mereka bukan lagi dua, melainkan satu.” (Matius 19:6)",
            intro: "Dengan penuh syukur atas kasih karunia Tuhan Yesus Kristus, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam pemberkatan nikah dan resepsi kami, dan turut mendoakan langkah kami sebagai satu keluarga.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua helai, satu tenun", "Kedua Mempelai"],
          count: ["Menanti hari", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & tempat", "Rangkaian Acara"],
          story: ["Benang demi benang", "Kisah Kami"],
          gallery: ["Album", "Galeri Kami"],
          wishes: ["Doa & kehadiran", "Ucapan & Konfirmasi"],
          gifts: ["Tanda kasih", "Hadiah Pernikahan"],
          closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat yang sangat berarti bagi kami sekeluarga. Tuhan memberkati.", salam: "Kasih Tuhan menyertai kita semua" },
          sent: "Terima kasih, doa dan ucapan Anda sudah terkirim. Tuhan memberkati.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
          closedNote: "Terima kasih atas doa dan kasihnya. Ucapan masih bisa dikirim lewat form ini.",
          giftIntro: "Doa Anda adalah hadiah terindah bagi kami. Bila ingin memberi tanda kasih, dapat melalui:",
        }}
        hero={(
          <header className={s.hero}>
            <div className={s.runner}>
              <div className={s.heroPhotoBox}>
                {photo ? <Photo src={photo} alt={`${data.couple.bride} dan ${data.couple.groom}`} /> : <span className={s.heroMono} aria-hidden>{data.couple.bride.slice(0, 1)}{data.couple.groom.slice(0, 1)}</span>}
              </div>
            </div>
            <p className={s.heroKicker}>Pernikahan Kudus</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="node" />,
          amp: <Art name="node" />,
          portrait: <Art name="node" />,
          countDecor: <span className={s.countDecor} aria-hidden><Art name="boat" /></span>,
          closingEmblem: <Art name="node" className={s.closingEmblem} />,
          sentArt: <Art name="boat" />,
        }}
      />
    </ThemeShell>
  );
}
