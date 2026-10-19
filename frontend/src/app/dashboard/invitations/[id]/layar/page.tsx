"use client";

import Link from "next/link";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";
import { GateNotice, usePageGate } from "../_lib";

export default function ScreenSetupPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const invitationId = routeParams?.id;
  const gate = usePageGate(invitationId, token, "screen");
  if (!ready || !invitationId) return null;

  if (gate.status !== "ok") {
    return (
      <DashboardShell active="screen" invitationId={invitationId}>
        <GateNotice gate={gate} invitationId={invitationId} />
      </DashboardShell>
    );
  }

  return (
    <DashboardShell active="screen" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Hari-H</p>
          <h1>Layar sapa</h1>
          <p className="dashboard-subtitle">Tampilkan di TV atau proyektor venue. Setiap tamu yang di-scan disambut namanya di layar, lengkap dengan nomor meja.</p>
        </div>
        <a className="dashboard-action" href={`/layar/${invitationId}`} target="_blank" rel="noreferrer">Buka layar sapa ↗</a>
      </header>

      <div className={styles.form}>
        <section className={styles.panel} aria-label="Yang tampil">
          <h2>Yang tampil di layar</h2>
          <ul className={styles.hint} style={{ margin: 0, paddingLeft: 18, display: "grid", gap: 6, fontSize: 14 }}>
            <li><strong>Sambutan nama</strong> — “Sugeng rawuh, Pak Budi Santoso · Silakan menuju meja 12” muncul begitu QR tamu di-scan di menu <Link className={styles.link} href={`/dashboard/invitations/${invitationId}/checkin`}>Check-in</Link>.</li>
            <li><strong>Ucapan tamu</strong> bergantian setiap 8 detik saat tidak ada tamu baru.</li>
            <li><strong>Foto dari tamu</strong> jadi latar mosaik, dan QR di pojok mengajak tamu mengirim foto &amp; ucapan.</li>
            <li><strong>Pemenang doorprize</strong> diumumkan besar-besaran saat diundi dari menu <Link className={styles.link} href={`/dashboard/invitations/${invitationId}/doorprize`}>Undian doorprize</Link>.</li>
          </ul>
        </section>
        <section className={styles.panel} aria-label="Cara pakai">
          <h2>Cara pakai di venue</h2>
          <ol className={styles.hint} style={{ margin: 0, paddingLeft: 18, display: "grid", gap: 6, fontSize: 14 }}>
            <li>Di laptop yang tersambung ke TV/proyektor, masuk ke akun Rawuh lalu klik <strong>Buka layar sapa</strong>.</li>
            <li>Arahkan kursor ke pojok kanan atas, klik <strong>Layar penuh</strong>.</li>
            <li>Penerima tamu memakai HP masing-masing (login akun yang sama) untuk scan check-in. Layar ikut berubah dalam 3 detik.</li>
          </ol>
        </section>
      </div>
    </DashboardShell>
  );
}
