"use client";

import { useEffect, useRef, useState, type CSSProperties } from "react";
import Image from "next/image";
import Link from "next/link";
import styles from "@/app/landing.module.css";
import { IconArrowRight, IconMessage, IconSearch } from "@/components/brand/icons";

export function MobileMenu() {
  const menu = useRef<HTMLDetailsElement>(null);
  return <details ref={menu} className={styles.mobileMenu} onKeyDown={event => {
    if (event.key === "Escape" && menu.current?.open) {
      menu.current.open = false;
      menu.current.querySelector("summary")?.focus();
    }
  }}>
    <summary><span className={styles.menuClosed}>Menu</span><span className={styles.menuOpened}>Tutup</span></summary>
    <div onClick={event => {
      if ((event.target as HTMLElement).closest("a") && menu.current) menu.current.open = false;
    }}>
      <Link href="/templates">Tema</Link>
      <Link href="/fitur">Fitur</Link>
      <Link href="/harga">Harga</Link>
      <Link href="/produk/undangan-website">Produk</Link>
      <Link href="/tentang">Tentang kami</Link>
      <Link href="/auth/login">Masuk</Link>
    </div>
  </details>;
}

export type GalleryTemplate = {
  id: string; name: string; category: string; preview?: string; demoHref: string; isPremium: boolean; href?: string; price?: string;
};

const heights = [340, 260, 380, 280, 260, 360, 300, 340];

export function ThemeGallery({ templates, clip = false, title = "Cari tema yang kamu banget.", headingLevel = 2 }: {
  templates: GalleryTemplate[]; clip?: boolean; title?: string; headingLevel?: 1 | 2;
}) {
  const [category, setCategory] = useState("");
  const [query, setQuery] = useState("");
  const [expanded, setExpanded] = useState(false);
  const search = useRef<HTMLInputElement>(null);
  const counts = templates.reduce<Record<string, number>>((acc, template) => {
    if (template.category) acc[template.category] = (acc[template.category] ?? 0) + 1;
    return acc;
  }, {});
  const categories = Object.keys(counts);
  const needle = query.trim().toLowerCase();
  const visible = templates.filter(template => (!category || template.category === category)
    && (!needle || `${template.name} ${template.category}`.toLowerCase().includes(needle)));
  const clipped = clip && !expanded && visible.length > 8;
  const Heading = headingLevel === 1 ? "h1" : "h2";

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        search.current?.focus();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <div className={styles.themes}>
      <div className={styles.sectionHeader}>
        <div className={styles.titleGroup}>
          <p className={styles.eyebrow}>Galeri tema</p>
          <Heading className={styles.sectionTitle}>{title}</Heading>
        </div>
        <label className={styles.search}>
          <IconSearch size={18} />
          <span className="sr-only">Cari tema</span>
          <input ref={search} type="search" value={query} onChange={event => setQuery(event.target.value)}
            placeholder="Cari: rustic, adat jawa, minimalis…" aria-controls="theme-results" />
          <kbd aria-hidden="true">⌘K</kbd>
        </label>
      </div>
      <CategoryBar categories={categories} counts={counts} total={templates.length} value={category} onChange={setCategory} />
      {visible.length === 0 ? (
        <p className={styles.empty} role="status">Belum ada tema yang cocok. Coba kata kunci lain.</p>
      ) : (
        <div id="theme-results" className={styles.masonry} data-clipped={clipped ? "" : undefined} data-few={visible.length < 4 ? visible.length : undefined}>
          {visible.map((template, index) => (
            <article className={styles.themeCard} key={template.id}>
              <div className={styles.themePreview} style={{ height: heights[index % heights.length] }}>
                {template.preview
                  ? <Image src={template.preview} alt={`Pratinjau tema ${template.name}`} fill sizes="(max-width: 560px) 50vw, 25vw"
                      unoptimized={!template.preview.startsWith("/")} />
                  : <span className={styles.placeholder} aria-hidden>{template.name.slice(0, 1)}</span>}
                <div className={styles.themeOverlay}>
                  <Link className={styles.btnPrimary} href={`/auth/register?template=${encodeURIComponent(template.id)}`}>Pakai tema</Link>
                  <a className={styles.btnGhost} href={template.demoHref} target="_blank" rel="noreferrer">Lihat demo</a>
                </div>
              </div>
              <div className={styles.themeMeta}>
                <h3>{template.href ? <Link href={template.href}>{template.name}</Link> : template.name}</h3>
                <span className={template.isPremium ? styles.premium : undefined}>{template.isPremium ? "Premium" : template.category}</span>
              </div>
            </article>
          ))}
          {visible.length < 4 && (
            <FewThemesCard
              span={4 - visible.length}
              label={category || (needle ? `"${query.trim()}"` : "")}
              count={visible.length}
              total={templates.length}
              suggestions={templates.filter(template => !visible.includes(template)).slice(0, 3)}
              onReset={() => { setCategory(""); setQuery(""); }}
            />
          )}
        </div>
      )}
      {(visible.length === 0 || visible.length >= 4) && <div className={styles.galleryFooter}>
        {clipped
          ? <button type="button" className={styles.btnPrimary} onClick={() => setExpanded(true)}>Muat {visible.length - 8} tema lainnya <IconArrowRight size={14} /></button>
          : clip && <Link href="/templates" className={styles.btnPrimary}>Lihat semua tema <IconArrowRight size={14} /></Link>}
        <p role="status">{visible.length} tema{category ? ` ${category}` : ""}</p>
      </div>}
    </div>
  );
}

/** Horizontally scrollable category pills with counts, edge fades and prev/next buttons. */
export function CategoryBar({ categories, counts, total, value, onChange, allLabel = "Semua tema", className }: {
  categories: string[]; counts: Record<string, number>; total: number; value: string; onChange: (value: string) => void;
  allLabel?: string; className?: string;
}) {
  const row = useRef<HTMLDivElement>(null);
  const [edges, setEdges] = useState({ start: false, end: false });

  useEffect(() => {
    const element = row.current;
    if (!element) return;
    const update = () => setEdges({ start: element.scrollLeft > 4, end: element.scrollLeft + element.clientWidth < element.scrollWidth - 4 });
    update();
    element.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    return () => { element.removeEventListener("scroll", update); window.removeEventListener("resize", update); };
  }, []);

  function scroll(direction: 1 | -1) {
    row.current?.scrollBy({ left: direction * row.current.clientWidth * 0.7, behavior: "smooth" });
  }

  return (
    <div className={`${styles.tagBar} ${className ?? ""}`} data-start={edges.start || undefined} data-end={edges.end || undefined}>
      <button type="button" className={styles.tagNav} data-dir="prev" onClick={() => scroll(-1)} aria-label="Kategori sebelumnya" tabIndex={-1} hidden={!edges.start}>
        <IconArrowRight size={16} />
      </button>
      <div ref={row} className={styles.tags} role="group" aria-label="Filter kategori tema">
        {["", ...categories].map(item => (
          <button type="button" key={item || "all"} aria-pressed={value === item} onClick={() => onChange(item)}>
            <span>{item || allLabel}</span>
            <small>{item ? counts[item] : total}</small>
          </button>
        ))}
      </div>
      <button type="button" className={styles.tagNav} data-dir="next" onClick={() => scroll(1)} aria-label="Kategori berikutnya" tabIndex={-1} hidden={!edges.end}>
        <IconArrowRight size={16} />
      </button>
    </div>
  );
}

/** Fills the empty columns when a filter leaves only 1–3 themes, so the row never looks broken. */
function FewThemesCard({ span, label, count, total, suggestions, onReset }: {
  span: number; label: string; count: number; total: number; suggestions: GalleryTemplate[]; onReset: () => void;
}) {
  return (
    <aside className={styles.fewCard} style={{ "--span": span } as CSSProperties} data-span={span}>
      <div className={styles.fewCopy}>
        <p className={styles.eyebrow}>Baru {count} tema{label ? ` ${label}` : ""}</p>
        <h3>Belum nemu yang pas?</h3>
        <p>Tema baru rutin ditambah. Sementara itu, intip {total - count} tema lain yang sama-sama siap dipakai.</p>
        <button type="button" className={styles.btnPrimary} onClick={onReset}>Lihat semua {total} tema <IconArrowRight size={14} /></button>
      </div>
      {suggestions.length > 0 && (
        <div className={styles.fewStack} aria-label="Tema lainnya">
          {suggestions.map(template => (
            <Link key={template.id} href={template.href ?? template.demoHref} className={styles.fewThumb} title={template.name}>
              {template.preview && <Image src={template.preview} alt={template.name} fill sizes="160px" unoptimized={!template.preview.startsWith("/")} />}
              <span>{template.name}</span>
            </Link>
          ))}
        </div>
      )}
    </aside>
  );
}

export type Voice = {
  id: string; name: string; role?: string; messages: string[]; time?: string; isSample?: boolean;
};
export type VoicePhoto = { src: string; caption: string; afterIndex: number };

function initials(name: string) {
  return name.replace(/[^\p{L} ]/gu, "").split(/\s+/).filter(Boolean).slice(0, 2).map(part => part[0]).join("").toUpperCase();
}

export function VoiceWall({ voices, photos }: { voices: Voice[]; photos: VoicePhoto[] }) {
  const [tab, setTab] = useState("");
  const categoryOf = (voice: Voice) => voice.role?.split("·")[0]?.trim() ?? "";
  const tabs = Array.from(new Set(voices.map(categoryOf).filter(Boolean)));
  const visible = voices.filter(voice => !tab || categoryOf(voice) === tab);
  const items: ({ kind: "voice"; voice: Voice } | { kind: "photo"; photo: VoicePhoto })[] = [];
  visible.forEach((voice, index) => {
    items.push({ kind: "voice", voice });
    if (!tab) photos.filter(photo => photo.afterIndex === index).forEach(photo => items.push({ kind: "photo", photo }));
  });

  return <>
    {tabs.length > 1 && <div className={styles.voiceTabs} role="group" aria-label="Filter jenis acara">
      {["", ...tabs].map(value => <button key={value || "all"} type="button" aria-pressed={tab === value} onClick={() => setTab(value)}>{value || "Semua"}</button>)}
    </div>}
    <div className={styles.wall}>
      {items.map(item => item.kind === "photo"
        ? <figure key={item.photo.src} className={styles.photoCard}>
            <Image src={item.photo.src} alt="" fill sizes="(max-width: 900px) 100vw, 33vw" />
            <span>{item.photo.caption}</span>
          </figure>
        : <figure key={item.voice.id} className={styles.chat}>
            <figcaption className={styles.chatHead}>
              <span className={styles.av} aria-hidden>{initials(item.voice.name)}</span>
              <span><strong>{item.voice.name}</strong>{item.voice.role && <small>{item.voice.role}</small>}</span>
              <IconMessage size={16} />
            </figcaption>
            {item.voice.messages.map(message => <blockquote key={message} className={styles.bubble}>{message}</blockquote>)}
            <div className={styles.chatTime}><span>{item.voice.time ? `${item.voice.time}  ✓✓` : "✓✓"}</span>{item.voice.isSample && <span className={styles.sample}>Contoh</span>}</div>
          </figure>)}
    </div>
  </>;
}
