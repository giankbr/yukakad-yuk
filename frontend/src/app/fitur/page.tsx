import type { Metadata } from "next";
import Image from "next/image";
import base from "@/app/landing.module.css";
import styles from "@/app/marketing-pages.module.css";
import { Breadcrumb, FinalCta, MarketingPage, SplitTitle, StepsSection } from "@/components/landing/Sections";
import {
  IconBank, IconCalendar, IconChart, IconCheck, IconClock, IconCopy, IconGift, IconImages, IconLanguages, IconLock,
  IconMusic, IconPin, IconQr, IconRadio, IconSend, IconUsers,
} from "@/components/brand/icons";

export const metadata: Metadata = {
  title: "Fitur | Rawuh",
  description: "Dari kirim undangan sampai tamu pulang: kirim massal, RSVP, buku ucapan, amplop digital, dan QR check-in dalam satu tempat.",
};

function Kicker({ n, label }: { n: string; label: string }) {
  return <p className={styles.kicker}><b>{n}</b><i aria-hidden />{label}</p>;
}

function Checks({ items }: { items: string[] }) {
  return <ul className={styles.checks}>{items.map(item => <li key={item}><span><IconCheck size={12} strokeWidth={2.6} /></span>{item}</li>)}</ul>;
}

const guests = [
  ["Budi Santoso", "Keluarga", "Terkirim", "", true],
  ["Sari Wulandari", "Teman kantor", "Dibuka", "info", true],
  ["Pak RT Hadi", "Tetangga", "Terkirim", "", true],
  ["Dewi & Keluarga", "Keluarga", "Menunggu", "warn", false],
  ["Rizky Pratama", "Teman kuliah", "Dibuka", "info", false],
] as const;

const extras = [
  [<IconMusic key="i" size={18} />, "Musik latar", "Pilih dari koleksi lagu atau upload sendiri."],
  [<IconPin key="i" size={18} />, "Peta & rute", "Google Maps langsung dari undangan."],
  [<IconCalendar key="i" size={18} />, "Simpan ke kalender", "Satu tap ke Google/Apple Calendar."],
  [<IconImages key="i" size={18} />, "Galeri & video", "Foto prewedding dan video YouTube."],
  [<IconClock key="i" size={18} />, "Hitung mundur", "Countdown menuju hari bahagia."],
  [<IconLanguages key="i" size={18} />, "Dua bahasa", "Indonesia & Inggris dalam satu undangan."],
  [<IconLock key="i" size={18} />, "Undangan privat", "Link personal untuk setiap tamu."],
  [<IconRadio key="i" size={18} />, "Live streaming", "Tautan siaran untuk tamu jauh."],
] as const;

export default function FiturPage() {
  return (
    <MarketingPage current="fitur">
      <section className={`${styles.head} ${styles.headCenter}`} aria-labelledby="fitur-title">
        <Breadcrumb items={[["Beranda", "/"], ["Fitur"]]} />
        <SplitTitle as="h1" id="fitur-title" className={styles.h1} lead="Dari kirim undangan" mono="sampai tamu pulang." />
        <p className={styles.lead}>Satu tempat untuk mengundang, mengelola tamu, menerima ucapan &amp; amplop, hingga check-in di venue.</p>
        <nav className={styles.segment} aria-label="Lompat ke fitur">
          <a href="#kirim"><IconSend size={14} />Kirim</a>
          <a href="#rsvp"><IconUsers size={14} />RSVP &amp; Ucapan</a>
          <a href="#amplop"><IconGift size={14} />Amplop</a>
          <a href="#checkin"><IconQr size={14} />Check-in</a>
          <a href="#lainnya"><IconChart size={14} />Lainnya</a>
        </nav>
      </section>

      <section className={base.section} id="kirim">
        <div className={styles.featureRow}>
          <div className={styles.featureCopy}>
            <Kicker n="01" label="Kirim" />
            <h2 className={base.sectionTitle}>Satu klik, ratusan undangan personal.</h2>
            <p className={styles.lead}>Upload daftar tamu dari Excel atau kontak HP. Setiap tamu dapat link dengan namanya sendiri — tanpa copy-paste satu per satu.</p>
            <Checks items={["Kirim massal via WhatsApp", "Nama tamu otomatis di sampul undangan", "Pantau siapa yang sudah membuka"]} />
          </div>
          <div className={styles.stage} aria-hidden data-aos="fade-up">
            <div className={styles.panel}>
              <div className={styles.panelHead}>Daftar tamu · 248<span>Kirim ke 3 terpilih</span></div>
              {guests.map(([name, group, status, tone, checked]) => (
                <div key={name} className={styles.guestRow}>
                  <span className={styles.box} data-on={checked ? "" : undefined}>{checked && <IconCheck size={12} strokeWidth={3} />}</span>
                  <span className={styles.av}>{name[0]}</span>
                  <div><strong>{name}</strong><small>{group}</small></div>
                  <span className={styles.status} data-tone={tone || undefined}><i />{status}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className={base.section} id="rsvp">
        <div className={styles.featureRow} data-flip="">
          <div className={styles.featureCopy}>
            <Kicker n="02" label="RSVP & ucapan" />
            <h2 className={base.sectionTitle}>Tahu siapa yang datang, sebelum katering dipesan.</h2>
            <p className={styles.lead}>Tamu konfirmasi kehadiran &amp; jumlah orang langsung dari undangan. Kamu pantau semuanya real-time dari HP.</p>
            <Checks items={["Konfirmasi hadir + jumlah rombongan", "Buku ucapan yang bisa dibaca ulang", "Rekap kehadiran untuk WO & katering"]} />
          </div>
          <div className={styles.stage} aria-hidden data-aos="fade-up">
            <div className={styles.rsvpStack}>
              <div className={styles.tiles}>
                <div className={styles.tile}><small>Hadir</small><strong>186</strong><em data-good="">+12 hari ini</em></div>
                <div className={styles.tile}><small>Tidak hadir</small><strong>21</strong><em>8%</em></div>
                <div className={styles.tile}><small>Belum jawab</small><strong>41</strong><em>kirim pengingat</em></div>
              </div>
              <div className={styles.card}>
                <div className={styles.cardRow}><b>Respons tamu</b><span>207 / 248</span></div>
                <div className={styles.split}><i style={{ width: "50%", background: "var(--rw-primary)" }} /><i style={{ width: "17%", background: "#f1a280" }} /></div>
              </div>
              <div className={styles.card}>
                <div className={styles.wish}><span className={styles.av}>S</span><div><strong>Sari W.<span>2m</span></strong><p>Selamat ya Nina &amp; Dimas! Semoga sakinah mawaddah warahmah 🤍</p></div></div>
                <div className={styles.wish}><span className={styles.av}>O</span><div><strong>Om Hendra<span>14m</span></strong><p>Doa terbaik dari keluarga Bandung. Insyaallah hadir.</p></div></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className={base.section} id="amplop">
        <div className={styles.featureRow}>
          <div className={styles.featureCopy}>
            <Kicker n="03" label="Amplop digital" />
            <h2 className={base.sectionTitle}>Hadiah masuk tanpa ribet nomor rekening.</h2>
            <p className={styles.lead}>Tamu yang berhalangan tetap bisa memberi. Rekening bank dan e-wallet kalian tampil rapi, lengkap dengan tombol salin.</p>
            <Checks items={["Rekening bank & e-wallet", "Tombol salin nomor sekali tap", "Alamat kirim kado fisik"]} />
          </div>
          <div className={`${styles.stage} ${styles.stageSoft}`} aria-hidden data-aos="fade-up">
            <div className={styles.giftLayout}>
              <div className={styles.giftCard}>
                Kirim hadiah untuk<br />Nina &amp; Dimas
                <div className={styles.giftQr}><IconQr /></div>
                <small>QRIS · semua e-wallet</small>
                <div className={styles.bank}><IconBank size={14} /><span>BCA · 1234 5678 90<small>a.n. Nina Larasati</small></span><IconCopy size={13} /></div>
              </div>
              <div className={styles.gifts}>
                {[["Rizky P.", "Rp250.000", "Maaf belum bisa hadir 🙏"], ["Tante Rina", "Rp500.000", "Bahagia selalu ya!"], ["Tim Kantor", "Rp1.200.000", "Dari kami semua ✨"]].map(([name, amount, note]) => (
                  <div key={name} className={styles.gift}><span><IconGift size={14} /></span><div><strong>{name}<span>{amount}</span></strong><small>{note}</small></div></div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className={base.section} id="checkin">
        <div className={styles.featureRow} data-flip="">
          <div className={styles.featureCopy}>
            <Kicker n="04" label="Check-in" />
            <h2 className={base.sectionTitle}>Tamu scan QR, buku tamu terisi sendiri.</h2>
            <p className={styles.lead}>Tidak perlu antre tanda tangan. Penerima tamu cukup scan QR dari HP, nama &amp; jumlah rombongan langsung tercatat.</p>
            <Checks items={["Scan dengan HP, tanpa alat khusus", "Nama tamu langsung muncul saat scan", "Pantau kehadiran live dari dashboard"]} />
          </div>
          <div className={`${styles.stage} ${styles.stagePhoto}`} data-aos="fade-up">
            <Image src="/rawuh/product-checkin.webp" alt="Penerima tamu memindai QR undangan di meja penyambutan" fill sizes="(max-width: 900px) 100vw, 560px" />
            <div className={styles.floatTop} aria-hidden><strong>312 / 400</strong><small>tamu sudah hadir</small></div>
            <div className={styles.floatBottom} aria-hidden><span><IconCheck size={16} strokeWidth={3} /></span><div><strong>Budi Santoso + 3 orang</strong><small>Meja 12 · check-in 18:42</small></div></div>
          </div>
        </div>
      </section>

      <section className={base.section} id="lainnya" style={{ background: "var(--rw-surface-2)" }} aria-labelledby="extras-title">
        <div className={base.titleGroup} style={{ marginBottom: 40 }}>
          <p className={base.eyebrow}>Dan masih banyak lagi</p>
          <SplitTitle id="extras-title" className={base.splitInline} lead="Detail kecil," mono="kesan besar." />
        </div>
        <div className={styles.iconGrid}>
          {extras.map(([icon, title, desc]) => <div key={title}>{icon}<h3>{title}</h3><p>{desc}</p></div>)}
        </div>
      </section>

      <StepsSection />
      <FinalCta />
    </MarketingPage>
  );
}
