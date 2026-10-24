"use client";
// Theme "Ukiran Botani" — lempeng ilustrasi botani bergaya ukiran tembaga di atas kertas tua: sampul berupa "Tab." dengan
// garis rangkap, gambar peoni dan pakis yang digores arsir sejajar dan silang di kiri, keterangan Latin rekaan dan nama
// di kanan; foto bernada sepia dalam bingkai oval kameo, kartu acara seperti label spesimen, hitung mundur di lempeng tinta.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["IM Fell English:ital@0;1", "Old Standard TT:ital,wght@0,400;0,700;1,400"];
// Engraved by /tmp/pen/art/themes/ukiran-botani.py (paper is a CSS background tile).
const Art = makeArt("ukiran-botani", { plate: [384, 789], fern: [139, 699], sprig: [474, 42], specimen: [170, 338] } as const);

const ROMAN: [number, string][] = [[1000, "M"], [900, "CM"], [500, "D"], [400, "CD"], [100, "C"], [90, "XC"], [50, "L"], [40, "XL"], [10, "X"], [9, "IX"], [5, "V"], [4, "IV"], [1, "I"]];
function roman(n: number) {
  let out = "";
  for (const [v, r] of ROMAN) while (n >= v) { out += r; n -= v; }
  return out;
}

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Hartono", attendance: "yes" as const, message: "Selamat menempuh hidup baru, Livia dan Bastian. Semoga rumah kalian selalu rimbun oleh tawa dan tanaman." },
  { id: "w2", name: "Sekar, teman herbarium", attendance: "yes" as const, message: "Akhirnya buku sketsa kalian punya halaman paling indah. Sampai jumpa di rumah kaca!" },
  { id: "w3", name: "Om Johan & Tante Mira", attendance: "maybe" as const, message: "Mohon maaf kalau belum bisa datang. Doa dan peluk hangat kami untuk kalian berdua." },
];

export default function UkiranBotaniTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const when = toDate(data.date);
  const plateNo = when ? roman(when.getDate()) : "I";
  const year = when ? roman(when.getFullYear()) : "";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe5cf"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.sheet}>
            <p className={s.plateHead}><span>Tab. {plateNo}</span><span>Flora Nuptialis</span><span>{year}</span></p>
            <div className={s.plateBody}>
              <div className={s.figure} aria-hidden>
                <Art name="plate" eager />
                <span className={`${s.figTag} ${s.figTag1}`}>Fig. 1</span>
                <span className={`${s.figTag} ${s.figTag2}`}>Fig. 2</span>
              </div>
              <div className={s.legend}>
                <p className={s.legendSmall}>Undangan {label}</p>
                <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
                <p className={s.coverDate}>{formatDate(data.date)}</p>
                <p className={s.latin}>Fig. 1 Paeonia amoris<br />Fig. 2 Filix fidelis</p>
              </div>
            </div>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f6efdd" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#efe5cf"
        dark="#1e1a16"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Dengan Penuh Sukacita",
            title: "Kami Mengundang Anda",
            sub: "untuk turut menyaksikan dua hal yang tumbuh menjadi satu",
            intro: "Dengan penuh rasa syukur, kami bermaksud melangsungkan pernikahan kami. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Fig. III & IV", "Kedua Mempelai"],
          count: ["Menuju Musim Mekar", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Catatan Lapangan", "Kisah Kami"],
          gallery: ["Lampiran", "Album Kami"],
          wishes: ["Buku Tamu", "Ucapan & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa restu Anda adalah lembar terindah dalam buku sketsa kehidupan kami." },
          sent: "Terima kasih, ucapan Anda sudah tercatat di buku tamu.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan ucapan dan doa untuk kami berdua…",
          familyLabel: "Kami yang berbahagia",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Plate II · {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.cameo}>
                <div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} dan ${data.couple.groom}`} /></div>
                <Art name="fern" className={`${s.fern} ${s.fernL}`} />
                <Art name="fern" className={`${s.fern} ${s.fernR}`} />
              </div>
            )}
            {hero && <p className={s.heroCaption}>Fig. 5 Sponsa et sponsus, in horto</p>}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="specimen" />,
          amp: <Art name="specimen" />,
          portrait: <Art name="fern" className={s.portraitArt} />,
          closingDecor: <><Art name="fern" className={`${s.closingDecor} ${s.closingFernL}`} /><Art name="fern" className={`${s.closingDecor} ${s.closingFernR}`} /></>,
          closingEmblem: <Art name="specimen" className={s.closingEmblem} />,
          sentArt: <Art name="specimen" />,
        }}
      />
    </ThemeShell>
  );
}
