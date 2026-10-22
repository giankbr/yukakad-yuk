"use client";
// Theme "Kolase Kertas" — undangan pernikahan bergaya kolase potongan kertas: daun, pakis, matahari bergerigi,
// bintang dan coretan bergelombang dari kertas warna (merah bata, kobalt, mustar, merah jambu, hijau daun) dengan
// serat kertas, tepi sobek dan bayangan tipis. Foto ditempel selotip kertas, nama di atas potongan label. Ilustrasi
// asli, digunting tangan secara digital.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Shrikhand", "Manrope:wght@400;500;600;700;800", "Caveat Brush"];
// Painted by /tmp/pen/art/themes/kolase-kertas.py (tools/art/themes in the repo).
const Art = makeArt("kolase-kertas", { top: [540, 534], bottom: [560, 318], star: [96, 97], leaf: [150, 306], strip: [360, 46], blob: [300, 307], tape: [130, 37] } as const);

const WISHES = [
  { id: "w1", name: "Teman-teman Komunitas Zine", attendance: "yes" as const, message: "Selamat Clara & Yohan! Dari satu gunting pinjaman jadi satu rumah. Tuhan memberkati langkah kalian berdua." },
  { id: "w2", name: "Bu Retno (Tante Clara)", attendance: "yes" as const, message: "Selamat menempuh hidup baru, Nak. Kiranya kasih Kristus selalu menjadi lem yang merekatkan keluarga kalian." },
  { id: "w3", name: "Dimas & Sekar", attendance: "maybe" as const, message: "Semoga bisa menyusul ke Kaliurang. Bahagia selalu, jangan lupa bikin kolase pernikahan kalian sendiri!" },
];

function Divider() {
  return <span className={s.divider} aria-hidden><Art name="strip" /></span>;
}

export default function KolaseKertasTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const { bride, groom } = data.couple;
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Salam Kasih",
      title: "Dua Potong Jadi Satu",
      intro: "Dengan sukacita dan atas kasih karunia Tuhan, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan turut berbahagia dalam pemberkatan dan perayaan pernikahan kami.",
    },
    roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
    couple: ["yang berbahagia", "Kedua Mempelai"] as [string, string],
    count: ["tinggal sebentar lagi", "Menuju Hari Bahagia"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["catat tanggalnya", "Waktu & Tempat"] as [string, string],
    story: ["dari awal", "Cerita Kami"] as [string, string],
    gallery: ["tempelan kenangan", "Galeri"] as [string, string],
    wishes: ["tinggalkan pesan", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["tanda kasih", "Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih!", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah potongan terindah yang melengkapi kolase hari bahagia kami.", salam: "Tuhan Yesus memberkati." },
    sent: "Terima kasih! Pesanmu sudah tertempel di papan kami.",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: "Tulis ucapan dan doa untuk kedua mempelai…",
    giftIntro: "Doa dan kehadiran Anda sudah lebih dari cukup. Bila ingin memberi tanda kasih, dapat melalui:",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f3eadb"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="top" eager className={s.cTop} />
          <Art name="bottom" eager className={s.cBottom} />
          <p className={s.kicker}>Undangan {label}</p>
          <div className={s.snap}>
            {hero ? <div className={s.snapImg}><Photo src={hero} alt="" /></div> : <div className={s.snapArt}><Art name="blob" eager /></div>}
            <Art name="tape" eager className={s.snapTape} />
          </div>
          <p className={s.hand} aria-hidden>kami menikah!</p>
          <h1 className={s.coverNames}>
            <span className={s.chipA}>{bride}</span>
            <span className={s.ampChip}>&amp;</span>
            <span className={s.chipB}>{groom}</span>
          </h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.note}>
            <Art name="tape" eager className={s.noteTape} />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#f2b52e" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbf3e3"
        dark="#22202a"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroArt}>
              <Art name="blob" className={s.heroBlob} />
              {hero && <div className={s.heroPhoto}><Photo src={hero} alt={`${bride} & ${groom}`} /></div>}
              <span className={s.heroLeaf}><Art name="leaf" /></span>
              <span className={s.heroStar}><Art name="star" /></span>
            </div>
            <p className={s.heroKicker}>Kami menikah</p>
            <h1 className={s.heroNames}><span>{bride}</span><em>&amp;</em><span>{groom}</span></h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Divider />,
          node: <Art name="star" />,
          amp: <Art name="leaf" />,
          portrait: <Art name="tape" className={s.portraitTape} />,
          countDecor: <span className={s.countLeaf} aria-hidden><Art name="leaf" /></span>,
          closingDecor: <Art name="bottom" className={s.closingArt} />,
          closingEmblem: <span className={s.emblem} aria-hidden><Art name="star" /></span>,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
