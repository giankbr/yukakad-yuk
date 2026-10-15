"use client";

import Link from "next/link";
import { useMemo, useState, type ReactNode } from "react";
import styles from "./theme-grid.module.css";

export type DashboardTemplate = {
  id: string;
  name: string;
  slug: string;
  category: string;
  preview_image?: string;
  preview_url?: string;
  is_premium: boolean;
};

export function previewOf(template: DashboardTemplate) {
  return template.preview_image || `/themes/previews/${template.slug || template.id}.webp`;
}

export function demoOf(template: DashboardTemplate) {
  return template.preview_url || `/invitation/demo?template=${encodeURIComponent(template.id)}`;
}

/** Filterable grid of Rawuh themes, shared by the template browser and the invitation settings. */
export function ThemeGrid({
  templates,
  selectedId,
  action,
}: {
  templates: DashboardTemplate[];
  selectedId?: string;
  action: (template: DashboardTemplate, selected: boolean) => ReactNode;
}) {
  const [category, setCategory] = useState("Semua");
  const [tier, setTier] = useState<"all" | "free" | "premium">("all");

  const categories = useMemo(
    () => ["Semua", ...Array.from(new Set(templates.map((t) => t.category).filter(Boolean)))],
    [templates],
  );

  const visible = templates.filter(
    (t) =>
      (category === "Semua" || t.category === category) &&
      (tier === "all" || (tier === "premium" ? t.is_premium : !t.is_premium)),
  );

  return (
    <div className={styles.wrap}>
      <div className={styles.filters}>
        <div className={styles.chips} role="tablist" aria-label="Kategori tema">
          {categories.map((cat) => (
            <button
              key={cat}
              type="button"
              role="tab"
              aria-selected={category === cat}
              className={styles.chip}
              onClick={() => setCategory(cat)}
            >
              {cat}
            </button>
          ))}
        </div>
        <div className={styles.segment} aria-label="Jenis tema">
          {(["all", "free", "premium"] as const).map((value) => (
            <button key={value} type="button" aria-pressed={tier === value} onClick={() => setTier(value)}>
              {value === "all" ? "Semua" : value === "free" ? "Gratis" : "Premium"}
            </button>
          ))}
        </div>
      </div>

      {visible.length === 0 ? (
        <p className="dashboard-state">Belum ada tema di kategori ini.</p>
      ) : (
        <div className={styles.grid}>
          {visible.map((template) => {
            const selected = selectedId === template.id;
            return (
              <article key={template.id} className={styles.card} data-selected={selected || undefined}>
                <a className={styles.thumb} href={demoOf(template)} target="_blank" rel="noreferrer" aria-label={`Lihat demo ${template.name}`}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={previewOf(template)} alt="" loading="lazy" />
                  {template.is_premium && <span className={styles.premium}>Premium</span>}
                  {selected && <span className={styles.current}>Dipakai</span>}
                  <span className={styles.peek}>Lihat demo ↗</span>
                </a>
                <div className={styles.body}>
                  <div>
                    <h3>{template.name}</h3>
                    <p>{template.category || "Umum"}</p>
                  </div>
                  {action(template, selected)}
                </div>
              </article>
            );
          })}
        </div>
      )}
    </div>
  );
}

export function ThemeLink({ href, children }: { href: string; children: ReactNode }) {
  return <Link className={styles.use} href={href}>{children}</Link>;
}

export function ThemeButton({ children, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button type="button" className={styles.use} {...props}>{children}</button>;
}
