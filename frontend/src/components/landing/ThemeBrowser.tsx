"use client";

import { useEffect, useRef, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import base from "@/app/landing.module.css";
import styles from "@/app/marketing-pages.module.css";
import { IconPencil, IconSearch, IconSparkle } from "@/components/brand/icons";
import { CategoryBar } from "@/components/landing/TemplateInteractions";

export type BrowserTemplate = {
  id: string; slug: string; name: string; category: string; preview?: string; demoHref: string; isPremium: boolean; price: string;
};

const PAGE = 12;

function withNames(href: string, names: string) {
  const trimmed = names.trim();
  if (!trimmed) return href;
  return `${href}${href.includes("?") ? "&" : "?"}names=${encodeURIComponent(trimmed)}`;
}

export function ThemeCard({ template, names = "" }: { template: BrowserTemplate; names?: string }) {
  return (
    <article className={styles.themeCard}>
      <Link href={`/templates/${template.slug}`} aria-label={`Detail tema ${template.name}`}>
        {template.isPremium && <span className={`${styles.flag} ${styles.flagPrimary}`}>Premium</span>}
        {template.preview
          ? <Image src={template.preview} alt="" fill sizes="(max-width: 1080px) 50vw, 25vw" unoptimized={!template.preview.startsWith("/")} />
          : <span className={styles.placeholder} aria-hidden>{template.name.slice(0, 1)}</span>}
      </Link>
      <div className={styles.themeInfo}>
        <strong><Link href={`/templates/${template.slug}`}>{template.name}</Link></strong>
        <em data-premium={template.isPremium ? "" : undefined}>{template.price}</em>
        <small>{template.category}</small>
        <a className={styles.demo} href={withNames(template.demoHref, names)} target="_blank" rel="noreferrer">Lihat demo</a>
      </div>
    </article>
  );
}

export function ThemeBrowser({ templates }: { templates: BrowserTemplate[] }) {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("");
  const [premiumOnly, setPremiumOnly] = useState(false);
  const [names, setNames] = useState("");
  const [limit, setLimit] = useState(PAGE);
  const search = useRef<HTMLInputElement>(null);

  const counts = templates.reduce<Record<string, number>>((acc, t) => ({ ...acc, [t.category]: (acc[t.category] ?? 0) + 1 }), {});
  const needle = query.trim().toLowerCase();
  const visible = templates.filter(t => (!category || t.category === category) && (!premiumOnly || t.isPremium)
    && (!needle || `${t.name} ${t.category}`.toLowerCase().includes(needle)));

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") { event.preventDefault(); search.current?.focus(); }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return <>
    <div className={browser.controls}>
      <label className={base.search} style={{ width: "100%" }}>
        <IconSearch size={18} />
        <span className="sr-only">Cari tema</span>
        <input ref={search} type="search" value={query} onChange={e => { setQuery(e.target.value); setLimit(PAGE); }} placeholder="Cari tema: rustic, adat jawa, minimalis, islami…" aria-controls="tema-grid" />
        <kbd aria-hidden>⌘K</kbd>
      </label>
      <label className={browser.names}>
        <IconSparkle size={14} />
        <span>Pratinjau dengan nama:</span>
        <input value={names} onChange={e => setNames(e.target.value)} placeholder="Nina & Dimas" aria-label="Nama untuk pratinjau demo" />
        <IconPencil size={13} />
      </label>
    </div>
    <div className={browser.filterBar}>
      <CategoryBar className={browser.tabs} categories={Object.keys(counts)} counts={counts} total={templates.length} value={category}
        onChange={value => { setCategory(value); setLimit(PAGE); }} />
      <button type="button" role="switch" className={browser.toggle} aria-checked={premiumOnly} onClick={() => { setPremiumOnly(v => !v); setLimit(PAGE); }}>
        <IconSparkle size={15} weight="fill" />
        <span>Hanya Premium</span>
        <i aria-hidden />
      </button>
    </div>
    <div className={browser.results}>
      <p className={browser.summary} role="status">Menampilkan {Math.min(limit, visible.length)} dari {visible.length} tema{category ? ` ${category}` : ""}</p>
      {visible.length === 0
        ? <p className={base.empty}>Belum ada tema yang cocok. Coba kata kunci lain.</p>
        : <div id="tema-grid" className={styles.grid4}>{visible.slice(0, limit).map(t => <ThemeCard key={t.id} template={t} names={names} />)}</div>}
      {visible.length > limit && (
        <div className={browser.more}><button type="button" className={base.btnOutline} onClick={() => setLimit(l => l + PAGE * 2)}>Muat {Math.min(PAGE * 2, visible.length - limit)} tema lagi</button></div>
      )}
    </div>
  </>;
}

// Small local class map so this component stays self-contained.
const browser = {
  controls: styles.browserControls,
  names: styles.browserNames,
  filterBar: styles.browserFilter,
  tabs: styles.browserTabs,
  toggle: styles.browserToggle,
  results: styles.browserResults,
  summary: styles.browserSummary,
  more: styles.browserMore,
};

/** "Coba dengan nama kalian" — opens the live demo with the couple's names filled in. */
export function TryNameForm({ demoHref }: { demoHref: string }) {
  const [names, setNames] = useState("");
  return (
    <form className={styles.tryName} onSubmit={event => { event.preventDefault(); window.open(withNames(demoHref, names), "_blank", "noopener"); }}>
      <label htmlFor="try-names">Coba dengan nama kalian</label>
      <div>
        <input id="try-names" value={names} onChange={e => setNames(e.target.value)} placeholder="Nina & Dimas" autoComplete="off" />
        <button type="submit" className={base.btnOutline}>Terapkan</button>
      </div>
    </form>
  );
}
