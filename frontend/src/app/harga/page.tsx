import type { Metadata } from "next";
import Link from "next/link";
import base from "@/app/landing.module.css";
import styles from "@/app/marketing-pages.module.css";
import { Breadcrumb, FaqSection, FinalCta, MarketingPage, PricingPlans, SplitTitle } from "@/components/landing/Sections";
import { IconCheck, IconGlobe, IconMinus, IconPrinter, IconReceipt, IconShield, IconUsers, IconVideo, IconWallet } from "@/components/brand/icons";
import { getPlans, getLandingContent, getSiteContact, priceLabel, planHref, activeLabel, type Plan } from "@/lib/marketing";

export const metadata: Metadata = {
  title: "Harga | Rawuh",
  description: "Sekali bayar, tanpa langganan. Bandingkan paket undangan digital Rawuh dan pilih yang pas untuk acaramu.",
};

type Cell = boolean | string;
type Row = { label: string; value: (plan: Plan) => Cell };

const groups: { title: string; rows: Row[] }[] = [
  {
    title: "Undangan",
    rows: [
      { label: "Jumlah tamu", value: plan => `${plan.max_guests.toLocaleString("id-ID")} tamu` },
      { label: "Masa aktif paket", value: plan => plan.price > 0 ? activeLabel(plan.duration_days).replace("Aktif ", "") : "—" },
      { label: "Tanpa watermark Rawuh", value: plan => !plan.has_watermark },
      { label: "Tema Premium", value: plan => Boolean(plan.premium_templates_allowed) },
    ],
  },
  {
    title: "Interaksi tamu",
    rows: [
      { label: "RSVP & konfirmasi", value: () => true },
      { label: "Buku ucapan", value: () => true },
      { label: "QR check-in di venue", value: () => true },
      { label: "Amplop digital", value: plan => plan.payment_gateway_allowed },
      { label: "Kolaborasi tim (keluarga, WO)", value: plan => plan.max_team_members === 0 ? "Tanpa batas" : plan.max_team_members ? `${plan.max_team_members} orang` : "—" },
    ],
  },
  {
    title: "Pengiriman",
    rows: [
      { label: "Nama tamu personal", value: () => true },
      { label: "Kirim via WhatsApp", value: () => true },
      { label: "Domain sendiri (.com/.id)", value: plan => plan.custom_domain_allowed },
    ],
  },
];

const addons = [
  { icon: <IconPrinter size={18} />, name: "Undangan cetak", desc: "Kartu fisik dengan QR ke undangan website.", price: "Rp3.500", unit: "/lembar" },
  { icon: <IconVideo size={18} />, name: "Video ucapan 3D", desc: "Video 30 detik untuk story & status WA.", price: "Rp99rb", unit: "" },
  { icon: <IconGlobe size={18} />, name: "Domain sendiri", desc: "nina-dimas.com aktif selama 1 tahun.", price: "Rp150rb", unit: "/tahun" },
  { icon: <IconUsers size={18} />, name: "Jasa input tamu", desc: "Kirim daftar dari Excel, kami rapikan.", price: "Rp50rb", unit: "/500 tamu" },
];

function Value({ cell }: { cell: Cell }) {
  if (cell === true) return <IconCheck className={styles.yes} size={16} strokeWidth={2.4} aria-label="Termasuk" />;
  if (cell === false) return <IconMinus className={styles.no} size={16} aria-label="Tidak termasuk" />;
  return <>{cell}</>;
}

export default async function HargaPage() {
  const [plans, { waLink }, landing] = await Promise.all([getPlans(), getSiteContact(), getLandingContent()]);
  const featuredIndex = plans.findIndex(plan => plan.id === "premium") >= 0 ? plans.findIndex(plan => plan.id === "premium") : plans.length >= 3 ? 1 : plans.length - 1;
  return (
    <MarketingPage current="harga">
      <section className={base.section} style={{ paddingTop: 64 }} aria-labelledby="harga-title">
        <div className={base.pricing}>
          <Breadcrumb items={[["Beranda", "/"], ["Harga"]]} />
          <div className={base.titleGroup}>
            <SplitTitle as="h1" id="harga-title" className={base.splitInline} lead="Sekali bayar," mono="tanpa langganan." />
            <p className={base.pricingDesc}>Hemat hingga 90% dibanding undangan cetak. Bayar hanya saat undangan siap dikirim.</p>
          </div>
          <PricingPlans plans={plans} />
        </div>
      </section>

      <section className={base.section} aria-labelledby="compare-title">
        <div className={base.titleGroup} style={{ marginBottom: 40 }}>
          <p className={base.eyebrow}>Perbandingan</p>
          <h2 id="compare-title" className={base.sectionTitle}>Bandingkan semua fitur.</h2>
        </div>
        <div className={styles.compare}>
          <div className={styles.compareScroll}>
            <table>
              <thead>
                <tr>
                  <th scope="col">Fitur</th>
                  {plans.map((plan, index) => (
                    <th key={plan.id} scope="col" data-featured={index === featuredIndex && plans.length > 1 ? "" : undefined}>
                      <strong>{plan.name}</strong>
                      <span>{priceLabel(plan.price)}</span>
                      <Link href={planHref(plan)} className={index === featuredIndex ? base.btnPrimary : base.btnOutline}>{plan.price > 0 ? `Pilih ${plan.name}` : "Mulai gratis"}</Link>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {groups.flatMap(group => [
                  <tr key={group.title} className={styles.group}><td colSpan={plans.length + 1}>{group.title}</td></tr>,
                  ...group.rows.map(row => (
                    <tr key={row.label}>
                      <td>{row.label}</td>
                      {plans.map((plan, index) => <td key={plan.id} data-featured={index === featuredIndex && plans.length > 1 ? "" : undefined}><Value cell={row.value(plan)} /></td>)}
                    </tr>
                  )),
                ])}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section className={base.section} aria-labelledby="addons-title">
        <div className={styles.headRow} style={{ marginBottom: 40 }}>
          <div className={base.titleGroup}>
            <p className={base.eyebrow}>Tambahan</p>
            <h2 id="addons-title" className={base.sectionTitle}>Lengkapi sesuai kebutuhan.</h2>
          </div>
          <p className={styles.headNote}>Bisa ditambahkan kapan saja, bahkan setelah undangan terkirim.</p>
        </div>
        <div className={styles.addons}>
          {addons.map(addon => (
            <div key={addon.name}>
              <span className={styles.iconBox}>{addon.icon}</span>
              <h3>{addon.name}</h3>
              <p>{addon.desc}</p>
              <strong>{addon.price}{addon.unit && <small>{addon.unit}</small>}</strong>
            </div>
          ))}
        </div>
        <div className={styles.promises} style={{ marginTop: 48 }}>
          <div><IconShield size={18} /><strong>Garansi 7 hari</strong><p>Uang kembali penuh jika tidak puas, tanpa pertanyaan.</p></div>
          <div><IconWallet size={18} /><strong>Bayar sesukamu</strong><p>QRIS, transfer bank, GoPay, OVO, DANA, ShopeePay.</p></div>
          <div><IconReceipt size={18} /><strong>Faktur resmi</strong><p>Untuk WO &amp; vendor yang butuh invoice perusahaan.</p></div>
        </div>
      </section>

      <FaqSection waLink={waLink} items={landing.faq} />
      <FinalCta />
    </MarketingPage>
  );
}
