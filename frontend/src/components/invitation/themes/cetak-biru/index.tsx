"use client";
// Theme "Cetak Biru" — modern: undangan sebagai gambar kerja rumah impian. Garis putih hasil cetak diazo (tampak depan,
// denah, garis ukur, huruf tangan arsitek) di atas kertas biru sian bergrid; kop gambar berisi tanggal dan tamu,
// potret sebagai "detail A/B" bertanda pojok potong, alat gambar dilukis gouache.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Architects Daughter", "Barlow Condensed:wght@400;500;600", "Barlow:ital,wght@0,400;0,500;1,400"];
// Painted by /tmp/pen/art/themes/cetak-biru.py (the blueprint paper is a CSS background tile)
const Art = makeArt("cetak-biru", { elevation: [700, 408], plan: [640, 547], tools: [380, 239] } as const);

function Dim({ label }: { label: string }) {
  return <span className={s.divider} aria-hidden><i /><em>{label}</em><b /></span>;
}

export default function CetakBiruTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const heroSrc = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;
  const note = data.couple.note?.trim();
  const label = data.eventLabel ?? "Pernikahan";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1f5fa6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.sheetHead}><span>Rencana Rumah Impian</span><span>Lbr. 01</span></div>
          <div className={s.elevationWrap}>
            <Art name="elevation" eager className={s.elevation} />
            <span className={s.note} aria-hidden>rumah kita, kelak</span>
          </div>
          <div className={s.coverText}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{bride}</span><i>&amp;</i><span>{groom}</span></h1>
          </div>
          <Art name="tools" eager className={s.coverTools} />
          <dl className={s.titleBlock}>
            <dt>Proyek</dt><dd>{label} {bride} &amp; {groom}</dd>
            <dt>Tanggal</dt><dd>{formatDate(data.date)}</dd>
            <dt>Kepada</dt>
            <dd className={s.tbGuest}>
              <small>Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </dd>
            <dt className={s.tbLast}>Skala</dt><dd className={s.tbLast}>1 : 100 · dengan cinta</dd>
          </dl>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#10335f" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ffffff"
        dark="#10335f"
        demoWishes={[
          { id: "w1", name: "Studio 7 Arsitektur", attendance: "yes", message: "Selamat, Nadia dan Arga! Akhirnya proyek paling penting di-ACC juga. Semoga fondasinya kuat dan atapnya selalu teduh." },
          { id: "w2", name: "Tante Maya & Om Rudi", attendance: "yes", message: "Bahagia sekali melihat kalian. Semoga rumah tangga kalian hangat, penuh tawa, dan selalu ada tempat untuk keluarga." },
          { id: "w3", name: "Dimas, teman asistensi", attendance: "maybe", message: "Masih di proyek luar kota, semoga bisa menyusul. Selamat menempuh hidup baru, jangan lupa undang ke rumah barunya." },
        ]}
        copy={{
          opening: {
            kicker: "Catatan Perancang",
            title: "Merancang Babak Baru",
            sub: "Gambar kerja untuk rumah tangga kami",
            intro: "Dengan penuh syukur, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan menjadi saksi hari pernikahan kami. Kehadiran dan doa Anda adalah fondasi terbaik bagi rumah yang akan kami bangun bersama.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua Perancang", "Kedua Mempelai"],
          count: ["Jadwal Pelaksanaan", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Lokasi Proyek", "Rangkaian Acara"],
          story: ["Riwayat Revisi", "Kisah Kami"],
          gallery: ["Lampiran", "Galeri"],
          wishes: ["Lembar Komentar", "Ucapan & Kehadiran"],
          gifts: ["Dukungan Proyek", "Amplop Digital"],
          closing: {
            thanks: "Terima Kasih",
            text: "Kehadiran dan doa Bapak/Ibu/Saudara/i merupakan kehormatan dan kebahagiaan bagi kami sekeluarga.",
            salam: "Disetujui dengan bahagia",
          },
          sent: "Terima kasih, ucapan Anda sudah masuk ke lembar komentar.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan ucapan dan doa untuk Nadia & Arga…",
          giftIntro: "Kehadiran Anda sudah lebih dari cukup. Jika ingin turut menambah bata di rumah baru kami, dapat melalui:",
          familyLabel: "Keluarga Besar",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Lbr. 02 · Kami akan menikah</p>
            <div className={s.heroFigure}>
              <div className={s.heroPhoto}>{heroSrc ? <Photo src={heroSrc} alt={`${bride} & ${groom}`} /> : <div />}</div>
              <span className={s.heroTag} aria-hidden>Foto · skala 1:1</span>
            </div>
            <h1 className={s.heroNames}>{bride} <i>&amp;</i> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="plan" className={s.plan} />
            <p className={s.planCaption} aria-hidden><span>Denah Lt. 1</span><span>Skala 1:100</span></p>
          </header>
        )}
        slots={{
          divider: <Dim label="1:100" />,
          portrait: <span className={s.callout} aria-hidden />,
          countDecor: <Art name="tools" className={s.countTools} />,
          closingEmblem: <Art name="elevation" className={s.closingEmblem} />,
          sentArt: <Art name="tools" />,
        }}
      />
    </ThemeShell>
  );
}
