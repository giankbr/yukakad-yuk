import Link from "next/link";
import base from "@/app/landing.module.css";
import page from "@/app/marketing-pages.module.css";
import styles from "./legal.module.css";
import { Breadcrumb, MarketingPage, SplitTitle } from "@/components/landing/Sections";
import { IconArrowRight, IconCheck, IconWhatsapp } from "@/components/brand/icons";
import { getSiteContact } from "@/lib/marketing";
import type { LegalDoc } from "@/lib/legal";

const siblings: Record<string, { href: string; label: string }> = {
  "syarat-ketentuan": { href: "/kebijakan-privasi", label: "Kebijakan Privasi" },
  "kebijakan-privasi": { href: "/syarat-ketentuan", label: "Syarat & Ketentuan" },
};

/** Long-form legal document: head, at-a-glance summary, sticky table of contents and numbered sections. */
export async function LegalPage({ doc }: { doc: LegalDoc }) {
  const { waLink } = await getSiteContact();
  const sibling = siblings[doc.slug];
  return (
    <MarketingPage>
      <section className={page.head} aria-labelledby="legal-title">
        <Breadcrumb items={[["Beranda", "/"], [doc.title]]} />
        <div className={styles.head}>
          <div className={base.titleGroup}>
            <p className={base.eyebrow}>Legal · Diperbarui {doc.updated}</p>
            <SplitTitle as="h1" id="legal-title" className={page.h1} lead={doc.lead} mono={doc.mono} />
          </div>
          <p className={page.lead}>{doc.intro}</p>
        </div>
        <ul className={styles.summary} aria-label="Ringkasan">
          {doc.summary.map(([title, text]) => (
            <li key={title}>
              <span aria-hidden><IconCheck size={16} weight="bold" /></span>
              <strong>{title}</strong>
              <p>{text}</p>
            </li>
          ))}
        </ul>
      </section>

      <div className={styles.layout}>
        <nav className={styles.toc} aria-label="Daftar isi">
          <p>Daftar isi</p>
          <ol>
            {doc.sections.map((section, index) => (
              <li key={section.id}><a href={`#${section.id}`}><span>{String(index + 1).padStart(2, "0")}</span>{section.title}</a></li>
            ))}
          </ol>
          {sibling && <Link className={styles.sibling} href={sibling.href}>Baca juga {sibling.label} <IconArrowRight size={14} /></Link>}
        </nav>

        <article className={styles.article}>
          {doc.sections.map((section, index) => (
            <section key={section.id} id={section.id} className={styles.section} aria-labelledby={`${section.id}-title`}>
              <h2 id={`${section.id}-title`}><span>{String(index + 1).padStart(2, "0")}</span>{section.title}</h2>
              {section.body.map((block, i) => Array.isArray(block)
                ? <ul key={i}>{block.map(item => <li key={item}>{item}</li>)}</ul>
                : <p key={i}>{block}</p>)}
            </section>
          ))}

          <aside className={styles.contact} aria-label="Kontak">
            <div>
              <strong>Ada pertanyaan soal {doc.title.toLowerCase()}?</strong>
              <p>Tim kami siap menjelaskan, termasuk permintaan akses atau penghapusan data.</p>
            </div>
            {waLink
              ? <a className={base.btnPrimary} href={waLink} target="_blank" rel="noreferrer"><IconWhatsapp size={16} /> Chat tim Rawuh</a>
              : <Link className={base.btnPrimary} href="/tentang#kontak">Hubungi kami <IconArrowRight size={14} /></Link>}
          </aside>
        </article>
      </div>
    </MarketingPage>
  );
}
