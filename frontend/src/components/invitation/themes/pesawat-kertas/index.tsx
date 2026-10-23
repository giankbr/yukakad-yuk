"use client";
// Theme "Pesawat Kertas" — undangan ceria bertema pesawat kertas di langit biru. Sampul berbingkai garis airmail merah-biru,
// pesawat kertas besar dari kertas airmail melayang naik-turun, jejak garis putus berputar dari bawah ke ekornya, awan
// gouache yang hanyut. Hero berupa "peta penerbangan": dua titik bernama mempelai dihubungkan garis putus dan pesawat
// kertas kecil (kertas bergaris) yang terbang di sepanjang jalurnya. Lukisan: /tmp/pen/art/themes/pesawat-kertas.py.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bricolage Grotesque:wght@400;600;800", "Lexend:wght@300;400;500;600", "Gochi Hand"];
const Art = makeArt("pesawat-kertas", { plane: [520, 266], plane2: [240, 136], "cloud-a": [460, 163], "cloud-b": [280, 110] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Halo, kamu!",
    title: "Kami Akhirnya Mendarat",
    intro: "Setelah bertahun-tahun saling mengirim kabar dari dua kota, kami memutuskan untuk berlabuh di satu rumah. Dengan senang hati kami mengundang Bapak/Ibu/Saudara/i untuk ikut merayakan hari bahagia kami.",
  },
  roles: ["Penumpang Pertama", "Penumpang Kedua"] as [string, string],
  couple: ["dua kota, satu tujuan", "Kami Berdua"] as [string, string],
  count: ["bersiap lepas landas", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["catat jadwalnya", "Rute Acara"] as [string, string],
  story: ["catatan perjalanan", "Kisah Kami"] as [string, string],
  gallery: ["oleh-oleh foto", "Galeri"] as [string, string],
  wishes: ["kirim pesan terbangmu", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["tanda kasih", "Kado Digital"] as [string, string],
  closing: { thanks: "Terima Kasih!", text: "Untuk setiap doa dan ucapan yang Anda terbangkan untuk kami. Sampai jumpa di hari bahagia!" },
  sent: "Pesanmu sudah terbang dan mendarat dengan selamat. Terima kasih!",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tulis pesan untuk kami, lalu terbangkan…",
  giftIntro: "Kehadiranmu adalah hadiah terbaik. Bila ingin mengirim tanda kasih, bisa lewat:",
};

const TRAIL = "M14 560 C 60 500, 20 440, 70 420 C 130 396, 160 450, 120 470 C 80 490, 70 410, 110 360 C 150 310, 60 250, 90 190 C 110 150, 130 130, 150 118";
const ROUTE = "M28 96 C 80 20, 160 20, 170 70 C 178 112, 120 112, 140 76 C 160 40, 230 30, 272 50";

export default function PesawatKertasTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const photo = data.gallery[0];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#bfe0f4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.sky}>
            <Art name="cloud-a" eager className={s.cloudA} />
            <Art name="cloud-b" eager className={s.cloudB} />
            <Art name="cloud-b" eager className={s.cloudC} />
            <svg className={s.trail} viewBox="0 0 200 580" aria-hidden>
              <path d={TRAIL} />
            </svg>
            <span className={s.trailPin} aria-hidden />
            <div className={s.coverPlane} aria-hidden><Art name="plane" eager /></div>
            <p className={s.coverKicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>
              <span className={s.nameA}>{data.couple.bride}</span>
              <em>&amp;</em>
              <span className={s.nameB}>{data.couple.groom}</span>
            </h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <p className={s.coverNote}>dua kota, satu tujuan</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ffffff"
        dark="#1f3354"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="cloud-a" className={s.heroCloud} />
            <div className={s.map}>
              <svg className={s.route} viewBox="0 0 300 120" aria-hidden>
                <path d={ROUTE} />
              </svg>
              <span className={s.flyer} aria-hidden><Art name="plane2" /></span>
              <span className={`${s.pin} ${s.pinA}`}><b aria-hidden />{data.couple.bride}</span>
              <span className={`${s.pin} ${s.pinB}`}><b aria-hidden />{data.couple.groom}</span>
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            {photo && <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} dan ${data.couple.groom}`} /></div>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="plane2" /></span>,
          node: <Art name="plane2" />,
          amp: <Art name="plane2" />,
          portrait: <span className={s.portraitPlane} aria-hidden><Art name="plane2" /></span>,
          countDecor: <><Art name="cloud-a" className={s.countCloudA} /><Art name="cloud-b" className={s.countCloudB} /></>,
          closingDecor: <><Art name="cloud-a" className={s.closeCloudA} /><Art name="cloud-b" className={s.closeCloudB} /></>,
          closingEmblem: <span className={s.closePlane} aria-hidden><Art name="plane" /></span>,
          sentArt: <Art name="plane2" />,
        }}
      />
    </ThemeShell>
  );
}
