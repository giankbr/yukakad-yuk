// Centered Rawuh card for not-found / error states. Server-safe (no hooks); actions are passed in.
import Link from "next/link";
import type { ReactNode } from "react";
import { RawuhMark } from "@/components/brand/RawuhMark";
import styles from "./state.module.css";

export function StateCard({ code, title, children, actions }: { code?: string; title: string; children: ReactNode; actions: ReactNode }) {
  return (
    <main className={styles.page}>
      <section className={styles.card} aria-labelledby="state-title">
        <Link href="/" className={styles.logo} aria-label="Rawuh — beranda"><RawuhMark size={30} color="var(--rw-primary)" />rawuh</Link>
        {code && <p className={styles.code}>{code}</p>}
        <h1 id="state-title" className={styles.title}>{title}</h1>
        <p className={styles.text}>{children}</p>
        <div className={styles.actions}>{actions}</div>
      </section>
    </main>
  );
}

export const stateStyles = styles;
