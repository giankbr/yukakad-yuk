"use client";
// Theme "Sidomukti Solo" — adat Jawa Surakarta: seluruh undangan adalah kain batik Sidomukti (kisi belah ketupat berisi
// kupu dan bunga dalam sogan-krem dengan isen-isen cecek, dilukis ulang), label krem bersudut takik di atas kain,
// untaian roncean melati yang berayun, wiru di tepi bawah, potret dalam bingkai belah ketupat, dan pendapa bertinta
// sepia. Motif orisinal terinspirasi Sidomukti, tanpa gurdha.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,500;1,400;1,500", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Imperial Script", "Amiri"];
// Painted by /tmp/pen/art/themes/sidomukti-solo.py (batik is a CSS background tile).
const Art = makeArt("sidomukti-solo", { kupu: [200, 163], ronce: [82, 616], pendopo: [640, 371], divider: [340, 45] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Mukti Wibawa",
    sub: "Dadi mukti, tansah mulya",
    intro: "Kanthi nyenyuwun rahmat saha ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan rawuh dan paring donga pangestu.",
  },
  roles: ["Mempelai Putri", "Mempelai Putra"],
  couple: ["Kekalih mempelai", "Putra-Putri Kami"],
  count: ["Wekdal ingkang dipun entosi", "Menghitung Hari"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Titi wanci lan papan", "Rangkaian Acara"],
  story: ["Lampahing tresna", "Kisah Kami"],
  gallery: ["Pepethan", "Galeri"],
  wishes: ["Donga pangestu", "Ucapan & Kehadiran"],
  gifts: ["Tandha asih", "Amplop Digital"],
  closing: {
    thanks: "Matur Sembah Nuwun",
    text: "Rawuh saha donga pangestu Bapak/Ibu/Saudara/i minangka kabingahan ingkang tanpa upami tumrap kulawarga kami.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Matur sembah nuwun, donga lan ucapan panjenengan sampun katampi.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
  closedNote: "Konfirmasi kehadiran sudah ditutup. Donga pangestu masih bisa dikirim lewat form ini.",
  giftIntro: "Donga pangestu panjenengan sampun dados peparing ingkang utami. Bila berkenan memberi tanda kasih, dapat melalui:",
  familyLabel: "Ingkang mangayubagya",
};

const WISHES = [
  { id: "w1", name: "Bude Murni & Pakde Joko, Laweyan", attendance: "yes" as const, message: "Mugi dados kulawarga ingkang sakinah, mawaddah, warahmah. Rukun, ayem tentrem, lan tansah pinaringan berkah." },
  { id: "w2", name: "Rekan Sanggar Batik Kauman", attendance: "yes" as const, message: "Selamat, Mbak Kinasih lan Mas Bagas! Sekarang kain Sidomukti-nya sudah benar-benar dipakai. Bahagia selalu." },
  { id: "w3", name: "Keluarga Om Pram, Semarang", attendance: "maybe" as const, message: "Mohon maaf bila belum bisa rawuh. Doa kami menyertai sampai hari H." },
];

function Names({ bride, groom, className }: { bride: string; groom?: string; className: string }) {
  return <h1 className={className}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>;
}

export default function SidomuktiSoloTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const kicker = label === "Pernikahan" ? "Pahargyan Pawiwahan" : label;
  const groom = data.couple.groom?.trim();
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const initials = [data.couple.bride, groom].filter(Boolean).map(name => name!.slice(0, 1)).join("");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3a2416"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="ronce" eager className={`${s.ronce} ${s.ronceL}`} />
          <Art name="ronce" eager className={`${s.ronce} ${s.ronceR}`} />
          <div className={s.label}>
            <Art name="kupu" eager className={s.coverKupu} />
            <p className={s.kicker}>{kicker}</p>
            <Names bride={data.couple.bride} groom={groom} className={s.coverNames} />
            <Art name="divider" eager className={s.coverRule} />
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f3e2bc" />Buka Undangan</button>
          <span className={s.wiru} aria-hidden />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#f3e2bc"
        dark="#3a2010"
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{kicker} · Surakarta</p>
            <Names bride={data.couple.bride} groom={groom} className={s.heroNames} />
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="pendopo" className={s.heroPendopo} />
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride}${groom ? ` dan ${groom}` : ""}`} /> : <span className={s.heroMono} aria-hidden>{initials}</span>}</div>
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="kupu" />,
          amp: <Art name="kupu" />,
          portrait: <Art name="kupu" className={s.portraitArt} />,
          countDecor: <span className={s.countDecor} aria-hidden />,
          closingDecor: <div className={s.closingStage} aria-hidden><Art name="pendopo" /></div>,
          closingEmblem: <Art name="kupu" className={s.closingEmblem} />,
          sentArt: <Art name="kupu" />,
        }}
      />
    </ThemeShell>
  );
}
