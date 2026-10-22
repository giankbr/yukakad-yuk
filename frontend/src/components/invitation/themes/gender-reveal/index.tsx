"use client";
// Theme "Gender Reveal" — pesta tebak jenis kelamin bayi (gouache ceria): sampul terbelah biru/merah muda dengan
// balon biru dan pink yang melayang, konfeti tanda tanya, tanda tanya dua warna, perlengkapan bayi. Hero berisi kartu
// tebakan "Tim Biru atau Tim Pink" (pilihan lokal saja, hanya hiburan), kartu bulat tebal berbayang navy.
import { useState } from "react";
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import { toast } from "@/lib/celebrate";
import s from "./styles.module.css";

const FONTS = ["Bowlby One", "Baloo 2:wght@400;500;600;700;800"];
// Painted by /tmp/pen/art/themes/gender-reveal.py
const Art = makeArt("gender-reveal", {
  "balon-biru": [220, 443], "balon-pink": [220, 442], tanya: [220, 364], konfeti: [360, 357], bayi: [380, 200],
} as const);

type Team = "boy" | "girl";

function Vote({ date }: { date: string }) {
  const [team, setTeam] = useState<Team | null>(null);
  const pick = (value: Team) => {
    setTeam(value);
    toast(value === "boy" ? "Kamu masuk Tim Biru" : "Kamu masuk Tim Pink");
  };
  return (
    <div className={s.vote}>
      <h2>Tebak dulu, yuk!</h2>
      <p>Menurutmu si kecil cowok atau cewek?</p>
      <div className={s.voteBtns} role="radiogroup" aria-label="Tebakan">
        <button type="button" role="radio" aria-checked={team === "boy"} className={`${s.voteBtn} ${s.voteBoy} ${team === "boy" ? s.voteOn : ""}`} onClick={() => pick("boy")}>
          <Art name="balon-biru" /><span>Tim Biru</span><small>cowok</small>
        </button>
        <button type="button" role="radio" aria-checked={team === "girl"} className={`${s.voteBtn} ${s.voteGirl} ${team === "girl" ? s.voteOn : ""}`} onClick={() => pick("girl")}>
          <Art name="balon-pink" /><span>Tim Pink</span><small>cewek</small>
        </button>
      </div>
      {team && (
        <p key={team} className={s.voteResult} role="status">
          {team === "boy" ? "Tim Biru, catat!" : "Tim Pink, catat!"} Jawabannya terungkap saat kotak balon dibuka{date ? ` pada ${date}` : ""}. Pakai warna tebakanmu, ya.
        </p>
      )}
    </div>
  );
}

export default function GenderRevealTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Gender Reveal";
  const bride = data.couple.bride;
  const groom = data.couple.groom?.trim();
  const names = [bride, groom].filter(Boolean).join(" & ");
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const date = formatDate(data.date);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fff7ee"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="konfeti" eager className={s.coverKonfeti} />
          <Art name="balon-biru" eager className={s.coverBalloonL} />
          <Art name="balon-pink" eager className={s.coverBalloonR} />
          <p className={s.coverKicker}>Undangan {label}</p>
          <h1 className={s.coverTitle}>
            <span className={s.boy}>Boy</span>
            <span className={s.or}>atau</span>
            <span className={s.girl}>Girl<span className={s.q}>?</span></span>
          </h1>
          <p className={s.coverSub}>bersama calon orang tua <b>{names}</b></p>
          <p className={s.coverDate}>{date}</p>
          <div className={s.guestCard}>
            <div className={s.guest}>
              <small>Halo, Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#2c3459" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!data.couple.bridePhoto && !data.couple.groomPhoto}
        light="#fff7ee"
        dark="#2c3459"
        demoWishes={[
          { id: "w1", name: "Tante Rina", attendance: "yes", message: "Aku yang pegang amplop rahasianya dan sumpah belum ngintip! Semoga Dinda dan si kecil sehat sampai hari lahir." },
          { id: "w2", name: "Gilang & Sasa", attendance: "yes", message: "Tim Biru hadir! Apa pun jawabannya, selamat ya calon ayah dan bunda. Nggak sabar main sama ponakan baru." },
          { id: "w3", name: "Mbak Yuni", attendance: "maybe", message: "Feeling-ku cewek! Maaf kalau telat datang, semoga lancar dan sehat selalu untuk kalian bertiga." },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Halo, keluarga & sahabat",
            title: "Ada kabar gembira!",
            sub: label,
            intro: `Si kecil sedang tumbuh di perut dan sebentar lagi rahasianya akan terungkap. Kami mengundangmu untuk ikut menebak, menghitung mundur, dan membuka kotak balon bersama ${names}.`,
          },
          roles: ["Calon Bunda", "Calon Ayah"],
          couple: ["Calon orang tua", "Kenalan dulu"],
          count: ["Hitung mundur", "Rahasia terungkap dalam"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat tanggalnya", "Waktu & tempat"],
          story: ["Cerita kecil", "Kabar si kecil"],
          gallery: ["Galeri", "Momen kami"],
          wishes: ["Ucapan & tebakan", "Kirim doa & konfirmasi"],
          gifts: ["Tanda sayang", "Kado untuk si kecil"],
          closing: {
            thanks: "Sampai jumpa!",
            text: "Terima kasih sudah ikut menebak dan mendoakan. Siapa pun si kecil nanti, ia sudah dicintai banyak orang.",
          },
          attend: { maybe: "Mungkin" },
          sent: "Yeay, ucapanmu sudah terkirim!",
          wishPlaceholder: "Tulis doa dan tebakanmu: cowok atau cewek?",
          closedNote: "Rahasianya sudah terungkap. Terima kasih atas doa dan tebakannya, ucapan masih bisa dikirim lewat form ini.",
          giftIntro: "Kehadiran dan doamu sudah cukup. Kalau ingin memberi kado untuk si kecil, bisa lewat:",
          familyLabel: null,
        }}
        hero={(
          <header className={s.hero}>
            <Art name="konfeti" className={s.heroKonfeti} />
            <Art name="tanya" className={s.heroTanya} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{names}</h1>
            {note && <p className={s.heroNote}>{note}</p>}
            <Vote date={date} />
            <Art name="bayi" className={s.heroBayi} />
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="tanya" /></span>,
          node: <Art name="tanya" />,
          portrait: <Art name="tanya" className={s.portraitQ} />,
          countDecor: <Art name="konfeti" className={s.countKonfeti} />,
          closingDecor: <div className={s.closingBayi} aria-hidden><Art name="bayi" /></div>,
          closingEmblem: <Art name="tanya" className={s.closingTanya} />,
          sentArt: <Art name="tanya" />,
        }}
      />
    </ThemeShell>
  );
}
