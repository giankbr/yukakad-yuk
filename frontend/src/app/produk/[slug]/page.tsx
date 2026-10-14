import type { Metadata } from "next";
import type { ReactNode } from "react";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import base from "@/app/landing.module.css";
import styles from "@/app/marketing-pages.module.css";
import { Breadcrumb, FinalCta, MarketingPage, SplitTitle } from "@/components/landing/Sections";
import {
  IconArrowRight, IconCalendar, IconDownload, IconFile, IconGift, IconGlobe, IconImages, IconLink, IconMail, IconMusic,
  IconPin, IconPrinter, IconQr, IconRefresh, IconSparkle, IconTruck, IconUser, IconUsers, IconVideo, IconWifiOff,
} from "@/components/brand/icons";
import { getSiteContact, products } from "@/lib/marketing";

const icons: Record<string, (size: number) => ReactNode> = {
  globe: s => <IconGlobe size={s} />, video: s => <IconVideo size={s} />, qr: s => <IconQr width={s} height={s} />, printer: s => <IconPrinter size={s} />,
  user: s => <IconUser size={s} />, users: s => <IconUsers size={s} />, calendar: s => <IconCalendar size={s} />, pin: s => <IconPin size={s} />,
  images: s => <IconImages size={s} />, music: s => <IconMusic size={s} />, gift: s => <IconGift size={s} />, sparkle: s => <IconSparkle size={s} />,
  refresh: s => <IconRefresh size={s} />, link: s => <IconLink size={s} />, wifi: s => <IconWifiOff size={s} />, download: s => <IconDownload size={s} />,
  file: s => <IconFile size={s} />, mail: s => <IconMail size={s} />, truck: s => <IconTruck size={s} />,
};
const icon = (name: string, size = 16) => icons[name]?.(size) ?? null;

export function generateStaticParams() {
  return products.map(product => ({ slug: product.slug }));
}

export async function generateMetadata({ params }: PageProps<"/produk/[slug]">): Promise<Metadata> {
  const { slug } = await params;
  const product = products.find(item => item.slug === slug);
  if (!product) return {};
  return { title: `${product.name} | Rawuh`, description: product.lead };
}

export default async function ProductPage({ params }: PageProps<"/produk/[slug]">) {
  const { slug } = await params;
  const product = products.find(item => item.slug === slug);
  if (!product) notFound();
  const { waLink } = await getSiteContact();
  const resolve = (href: string) => href === "contact" ? (waLink ?? "/tentang#kontak") : href;
  const others = products.filter(item => item.slug !== product.slug);

  return (
    <MarketingPage current="produk">
      <section className={styles.productHero} aria-labelledby="product-title">
        <div className={styles.productCopy}>
          <Breadcrumb items={[["Beranda", "/"], [product.name]]} />
          <p className={base.eyebrow}>Produk · {product.name}</p>
          <SplitTitle as="h1" id="product-title" className={styles.h1} lead={product.headline[0]} mono={product.headline[1]} />
          <p className={styles.lead}>{product.lead}</p>
          <div className={styles.actions}>
            <Link href={resolve(product.primary.href)} className={base.btnPrimary}>{product.primary.label}</Link>
            <Link href={resolve(product.secondary.href)} className={base.btnOutline}>{product.secondary.label}</Link>
          </div>
          <p className={styles.priceTag}>{product.price}</p>
        </div>
        <div className={styles.productVisual}>
          <Image src={product.image} alt={product.name} fill sizes="(max-width: 900px) 100vw, 560px" preload />
          <span className={styles.productBadge}><span>{icon(product.icon, 14)}</span>{product.name}</span>
        </div>
      </section>

      <div className={styles.statThree}>
        {product.stats.map(([value, label]) => <div key={label}><strong>{value}</strong><small>{label}</small></div>)}
      </div>

      <section className={base.section} aria-labelledby="how-title">
        <div className={base.titleGroup} style={{ marginBottom: 40 }}>
          <p className={base.eyebrow}>Cara kerja</p>
          <h2 id="how-title" className={base.sectionTitle}>Tiga langkah, selesai.</h2>
        </div>
        <ol className={styles.stepRow}>
          {product.steps.map(([title, desc], index) => <li key={title}><b>{String(index + 1).padStart(2, "0")}</b><h3>{title}</h3><p>{desc}</p></li>)}
        </ol>
      </section>

      <section className={base.section} style={{ background: "var(--rw-surface-2)" }} aria-labelledby="perks-title">
        <div className={styles.perkLayout}>
          <div className={base.titleGroup} style={{ alignContent: "start" }}>
            <p className={base.eyebrow}>Yang kamu dapat</p>
            <h2 id="perks-title" className={base.sectionTitle}>Lengkap tanpa ribet.</h2>
            <p className={styles.lead} style={{ fontSize: 16 }}>Semua fitur sudah termasuk. Tidak ada biaya tersembunyi.</p>
          </div>
          <div className={styles.perkGrid}>
            {product.perks.map(([name, label]) => <div key={label}><span>{icon(name)}</span>{label}</div>)}
          </div>
        </div>
      </section>

      <section className={base.section} aria-labelledby="others-title">
        <div className={styles.rowHead}>
          <h2 id="others-title" className={base.sectionTitle}>Lengkapi dengan produk lain</h2>
          <Link href="/harga" className={styles.textLink}>Lihat harga <IconArrowRight size={14} /></Link>
        </div>
        <div className={styles.related}>
          {others.map(other => (
            <Link key={other.slug} href={`/produk/${other.slug}`}>
              <div><Image src={other.image} alt="" fill sizes="(max-width: 900px) 100vw, 33vw" /></div>
              <strong>{icon(other.icon)}{other.name}</strong>
              <small>{other.price}</small>
            </Link>
          ))}
        </div>
      </section>

      <FinalCta />
    </MarketingPage>
  );
}
