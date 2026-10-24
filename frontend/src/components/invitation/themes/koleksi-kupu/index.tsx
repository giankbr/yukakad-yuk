"use client";
// Theme "Koleksi Kupu" — kotak koleksi kupu-kupu ala museum: bingkai kenari, alas linen, enam spesimen karangan
// (gouache bertinta urat) tersemat jarum dengan label tulisan tangan, pantulan kaca, dan kaca pembesar kuningan.
// Nama mempelai tertulis di kartu katalog di tengah kotak; hero berupa pelat "holotipe". Netral (bukan Islami).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["IM Fell English:ital@0;1", "Libre Caslon Text:ital,wght@0,400;0,700;1,400", "Homemade Apple"];
// Painted by /tmp/pen/art/themes/koleksi-kupu.py (wood + linen are CSS background tiles).
const Art = makeArt("koleksi-kupu", {
  aurelia: [220, 138], nila: [220, 159], senja: [220, 161], ekor: [220, 168], mata: [220, 169], mawar: [220, 158], lens: [200, 201],
} as const);

// Invented species for the labels (fictional names, not real taxa).
const TOP = [["nila", "Lazulina nila"], ["senja", "Delias senjana"], ["mawar", "Rosalia kirana"]] as const;
const BOTTOM = [["ekor", "Graphium bogorense"], ["aurelia", "Troides aurelia"], ["mata", "Ocellata halimun"]] as const;

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Catatan Kurator",
    title: "Dengan Penuh Syukur",
    sub: "koleksi no. 1 · dua hati, satu kotak kaca",
    intro: "Setelah bertahun-tahun mengamati hal-hal kecil yang indah bersama, kami memutuskan untuk menyimpan satu hal untuk selamanya: satu sama lain. Dengan sukacita kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan memberikan doa restu di hari pernikahan kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Spesimen Utama", "Kedua Mempelai"],
  count: ["Laci dibuka dalam", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Kartu Indeks", "Waktu & Tempat"],
  story: ["Catatan Lapangan", "Perjalanan Kami"],
  gallery: ["Arsip Foto", "Galeri"],
  wishes: ["Buku Tamu", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Hadiah"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i akan menjadi bagian paling berharga dari koleksi kenangan kami." },
  sent: "Terima kasih, ucapan Anda sudah kami simpan di buku tamu.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk Renata & Gilang…",
  giftIntro: "Kehadiran Anda sudah lebih dari cukup. Bagi yang ingin memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Tim Survei Bantimurung 2019", attendance: "yes" as const, message: "Akhirnya dua pengamat paling sabar di tim kami menemukan satu sama lain. Selamat menempuh hidup baru!" },
  { id: "w2", name: "Ibu Dr. Wahyuni Sasmita", attendance: "yes" as const, message: "Semoga rumah tangga kalian selalu penuh rasa ingin tahu, kesabaran, dan kebahagiaan kecil setiap hari." },
  { id: "w3", name: "Keluarga Om Bram, Malang", attendance: "maybe" as const, message: "Kami usahakan datang. Kalau belum bisa, doa terbaik kami kirim dari jauh." },
];

export default function KoleksiKupuTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const photo = data.gallery[0];
  const year = (data.date ?? "").slice(0, 4) || "—";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1d2520"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.plaque}>Koleksi Pribadi · {label}</p>
          <div className={s.case}>
            <div className={s.caseIn}>
              {TOP.map(([name, latin]) => <div key={name} className={s.spec}><Art name={name} eager /><span>{latin}</span></div>)}
              <div className={s.card}>
                <p className={s.cardTop}><span>Spesimen Nuptiale</span><span>{year}</span></p>
                <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
                <p className={s.coverDate}>{formatDate(data.date)}</p>
              </div>
              {BOTTOM.map(([name, latin]) => <div key={name} className={s.spec}><Art name={name} eager /><span>{latin}</span></div>)}
            </div>
            <Art name="lens" eager className={s.lens} />
          </div>
          <div className={s.coverFoot}>
            <div className={s.tag}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#23180c" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#e6c98a"
        dark="#1f2a23"
        hero={(
          <header className={s.hero}>
            <div className={s.plate}>
              <Art name="aurelia" className={s.holo} />
              <span className={s.holoLabel}>Holotipe · {data.couple.bride} &amp; {data.couple.groom}</span>
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            {photo && <div className={s.heroPhoto}><Photo src={photo} alt="" /></div>}
          </header>
        )}
        slots={{
          divider: <Art name="nila" className={s.divider} />,
          node: <Art name="senja" />,
          amp: <Art name="mawar" />,
          portrait: <Art name="mawar" className={s.portraitArt} />,
          closingEmblem: <div className={s.miniCase} aria-hidden><Art name="ekor" /><Art name="aurelia" /><Art name="mata" /></div>,
          sentArt: <Art name="aurelia" />,
        }}
      />
    </ThemeShell>
  );
}
