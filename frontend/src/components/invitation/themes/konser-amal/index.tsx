"use client";
// Theme "Konser Amal" — undangan konser amal komunitas, bergaya poster gig cetak sablon dan gouache: panggung malam dengan
// truss lampu, lampu untai, drum, keyboard, gitar dan ampli; lampu sorot yang menyapu dan kerumunan yang mengangkat tangan;
// tiket robek berperforasi untuk tamu, stiker not, toples donasi. Penyelenggara adalah panitia, bagian "Line Up" memuat
// para penampil, kisah berisi tujuan amalnya, dan amplop menjadi donasi.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bowlby One:wght@400", "Bricolage Grotesque:wght@400;600;700;800", "Caveat Brush:wght@400"];
// Painted by /tmp/pen/art/themes/konser-amal.py (crowd and paper are CSS backgrounds)
const Art = makeArt("konser-amal", { stage: [780, 600], beam: [160, 427], mic: [130, 262], jar: [130, 185], note: [90, 87], wave: [360, 24] } as const);

export default function KonserAmalTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const title = data.eventLabel?.trim() || "Konser Amal";
  const lineUp = [bride, groom].map(name => name?.trim()).filter(Boolean).join(" · ");
  const note = data.couple.note?.trim();
  const venue = data.events[0]?.venue || data.place;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6efe2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.tape}>Undangan Konser Amal</p>
          <h1 className={s.title}>{title}</h1>
          <div className={s.stageBox}>
            <Art name="stage" eager />
            <span className={`${s.beam} ${s.beamL}`} aria-hidden><Art name="beam" eager /></span>
            <span className={`${s.beam} ${s.beamR}`} aria-hidden><Art name="beam" eager /></span>
            <span className={s.crowd} aria-hidden />
            {lineUp && <p className={s.performers}>{lineUp}</p>}
          </div>
          <div className={s.ticket}>
            <div className={s.ticketMain}>
              <small>Tiket undangan untuk</small>
              <strong>{guestLabel(data)}</strong>
              <span>{formatDate(data.date)}{venue ? ` · ${venue}` : ""}</span>
            </div>
            <div className={s.stub}>
              <small>{table ? "Area" : "Masuk"}</small>
              <b>{table ? table.replace(/^Meja\s+/i, "") : "1 Tiket"}</b>
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        light="#ffc94a"
        dark="#1b1433"
        demoWishes={[
          { id: "w1", name: "Dimas & anak-anak kos Kenari", attendance: "yes", message: "Kami datang berlima, bawa buku cerita bekas juga. Semoga atap taman bacanya cepat beres!" },
          { id: "w2", name: "Bu Ratri, guru SD Muja Muju", attendance: "yes", message: "Terima kasih sudah memikirkan anak-anak kami. Murid-murid sudah tidak sabar ikut sesi dongengnya." },
          { id: "w3", name: "Yoga (Komunitas Sepeda Jogja)", attendance: "maybe", message: "Belum pasti bisa datang, tapi donasi sudah saya kirim. Semangat untuk panitia dan semua penampil!" },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Halo, teman baik!",
            title: "Mari Bernyanyi untuk Berbagi",
            intro: "Kami mengundang Anda untuk hadir dalam konser amal ini: satu malam penuh musik, tawa, dan kepedulian. Datang, bernyanyi bersama, dan ikut menyalakan harapan bagi mereka yang kita dukung.",
          },
          roles: ["Penampil Utama", "Penampil Tamu"],
          couple: ["Line Up", "Yang Akan Tampil"],
          count: ["Panggung dibuka dalam", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat Jadwalnya", "Info Acara"],
          story: ["Kenapa Kita Berkumpul", "Tujuan Amal"],
          gallery: ["Dokumentasi", "Dari Panggung Sebelumnya"],
          wishes: ["Pesan Semangat", "Konfirmasi Kehadiran"],
          gifts: ["Ikut Berbagi", "Salurkan Donasi"],
          closing: {
            thanks: "Sampai Jumpa di Depan Panggung!",
            text: "Terima kasih sudah peduli. Setiap kehadiran, donasi, dan pesan semangat Anda berarti besar bagi kami dan mereka yang kita bantu.",
            salam: "Salam hangat dari seluruh panitia",
          },
          sent: "Terima kasih! Pesan semangatmu sudah sampai ke panitia.",
          attend: { yes: "Datang", maybe: "Mungkin", no: "Tidak Bisa" },
          wishPlaceholder: "Tulis pesan semangat untuk panitia dan para penampil…",
          closedNote: "Pendaftaran kehadiran sudah ditutup. Terima kasih atas dukungannya, pesan semangat masih bisa dikirim lewat form ini.",
          giftIntro: "Seluruh donasi yang terkumpul disalurkan sepenuhnya untuk program amal yang kami dukung. Berapa pun nilainya, terima kasih sudah ikut berbagi:",
          giftAddressTitle: "Kirim Donasi Barang",
          familyLabel: null,
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.tape}>Save the date</p>
            <h1 className={s.heroTitle}>{title}</h1>
            <div className={s.heroStage}><Art name="stage" /></div>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.meter} aria-hidden>
              <p>Ayo penuhi panggung kebaikan!</p>
              <div className={s.meterBar}><span /></div>
              <Art name="jar" className={s.meterJar} />
            </div>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="wave" /></span>,
          node: <Art name="note" />,
          portrait: <Art name="note" className={s.portraitNote} />,
          countDecor: <span className={s.countCrowd} aria-hidden />,
          closingEmblem: <Art name="mic" className={s.closingMic} />,
          sentArt: <Art name="note" />,
        }}
      />
    </ThemeShell>
  );
}
