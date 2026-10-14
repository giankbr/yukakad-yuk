import Image from "next/image";
import Link from "next/link";
import type { ReactNode } from "react";
import theme from "@/components/ui/workspace-theme.module.css";
import { RawuhLogo } from "@/components/landing/SiteChrome";
import { IconStar } from "@/components/brand/icons";

/** Split auth layout from the Rawuh "Masuk" design: form on the left, story photo on the right. */
export function AuthLayout({ children, topRight }: { children: ReactNode; topRight?: ReactNode }) {
  return (
    <main className={`auth-page ${theme.auth}`}>
      <section className="auth-main">
        <div className="auth-top">
          <RawuhLogo />
          {topRight && <p className="auth-top-link">{topRight}</p>}
        </div>
        <div className="auth-panel">{children}</div>
        <footer className="auth-foot">
          <span>© {new Date().getFullYear()} Rawuh.id</span>
          <nav aria-label="Tautan bantuan"><Link href="/">Syarat &amp; Ketentuan</Link><span aria-hidden>·</span><Link href="/">Privasi</Link><span aria-hidden>·</span><Link href="/#faq">Bantuan</Link></nav>
        </footer>
      </section>
      <aside className="auth-aside" aria-label="Cerita pengguna Rawuh">
        <Image src="/rawuh/login-photo.webp" alt="" fill sizes="50vw" preload />
        <figure className="auth-quote">
          <div className="auth-stars" aria-label="5 dari 5 bintang">{Array.from({ length: 5 }, (_, i) => <IconStar key={i} size={16} />)}</div>
          <blockquote>“Undangan jadi dalam semalam, 400 tamu terkirim besok paginya. Ibu sampai tanya ini bikin di mana.”</blockquote>
          <figcaption>
            <Image src="/rawuh/avatar-laras-adit.webp" alt="" width={40} height={40} />
            <span><strong>Laras &amp; Adit</strong><small>Menikah di Solo · Tema Lentera</small></span>
          </figcaption>
        </figure>
      </aside>
    </main>
  );
}

/** Two-tone headline used across auth screens: sans line in brand orange, mono line in ink. */
export function AuthHeading({ lead, mono, children }: { lead: string; mono: string; children?: ReactNode }) {
  return (
    <div className="auth-heading">
      <h1><span>{lead}</span> <span>{mono}</span></h1>
      {children && <p>{children}</p>}
    </div>
  );
}
