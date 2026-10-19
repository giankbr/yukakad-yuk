"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";
import { friendly, GateNotice, lostAccess, usePageGate } from "../_lib";

type Domain = {
  id: string; domain: string; status: "pending" | "verified"; verified_at?: string;
  txt_name: string; txt_value: string; cname_target: string;
};
type Check = { ownership: boolean; routing: boolean; detail?: string };

/** The registered domain (rinabima.com, rinabima.co.id) that DNS panels are set up for. */
function rootDomain(domain: string) {
  // Treat common two-part suffixes (co.id, web.id, co.uk, …) as one label.
  const twoPart = /\.(co|or|ac|go|web|my|biz|sch|net|com)\.[a-z]{2}$/.test(domain);
  return domain.split(".").slice(twoPart ? -3 : -2).join(".");
}

/** Is the name the bare domain (rinabima.com) rather than a subdomain? Apex domains can't use CNAME. */
const isApex = (domain: string) => rootDomain(domain) === domain;

/** "Host" as DNS panels expect it: relative to the registered domain, "@" for the domain itself. */
function relativeHost(name: string, domain: string) {
  const root = rootDomain(domain);
  return name === root ? "@" : name.endsWith(`.${root}`) ? name.slice(0, -(root.length + 1)) : name;
}

export default function DomainPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const invitationId = routeParams?.id;
  const [items, setItems] = useState<Domain[]>([]);
  const [allowed, setAllowed] = useState(true);
  const [target, setTarget] = useState("domains.rawuh.id");
  const [checks, setChecks] = useState<Record<string, Check>>({});
  const [domain, setDomain] = useState("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState("");

  const gate = usePageGate(invitationId, token, "domain");
  const { lose } = gate;
  const open = gate.status === "ok";

  const load = useCallback(async () => {
    if (!token || !invitationId) return;
    const response = await apiFetch(`/api/invitations/${invitationId}/domains`, token);
    if (lostAccess(response.status)) { lose(); return; }
    const body = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(body.error);
    setItems(body.items ?? []);
    setAllowed(body.allowed !== false);
    if (body.cname_target) setTarget(body.cname_target);
  }, [token, invitationId, lose]);

  useEffect(() => {
    if (!ready || !token || !invitationId || !open) return;
    const timer = setTimeout(() => { load().catch((err) => setError(friendly(err, "Gagal memuat domain."))).finally(() => setLoading(false)); }, 0);
    return () => clearTimeout(timer);
  }, [ready, token, invitationId, open, load]);

  async function run(key: string, action: () => Promise<void>) {
    setBusy(key);
    setError("");
    try {
      await action();
    } catch (err) {
      setError(friendly(err, "Belum tersimpan."));
    } finally {
      setBusy(null);
    }
  }

  const add = (event: React.FormEvent) => {
    event.preventDefault();
    void run("add", async () => {
      const response = await apiFetch(`/api/invitations/${invitationId}/domains`, token!, { method: "POST", body: JSON.stringify({ domain: domain.trim() }) });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(body.error);
      setDomain("");
      await load();
    });
  };

  const verify = (item: Domain) => run(item.id, async () => {
    const response = await apiFetch(`/api/invitations/${invitationId}/domains/${item.id}/verify`, token!, { method: "POST", body: "{}" });
    const body = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(body.error);
    setChecks((current) => ({ ...current, [item.id]: body.check }));
    setItems((current) => current.map((d) => (d.id === item.id ? body.domain : d)));
  });

  const remove = (item: Domain) => {
    if (!window.confirm(`Hapus ${item.domain}? Tamu yang membuka domain ini tidak akan melihat undangan lagi.`)) return;
    void run(item.id, async () => {
      const response = await apiFetch(`/api/invitations/${invitationId}/domains/${item.id}`, token!, { method: "DELETE" });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(body.error);
      await load();
    });
  };

  const copy = async (value: string) => {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(value);
      setTimeout(() => setCopied((current) => (current === value ? "" : current)), 1800);
    } catch { /* value stays visible */ }
  };

  if (!ready || !token || !invitationId) return null;
  if (!open) {
    return (
      <DashboardShell active="domain" invitationId={invitationId}>
        <GateNotice gate={gate} invitationId={invitationId} deniedText="Hanya pemilik undangan yang bisa mengatur domain" />
      </DashboardShell>
    );
  }

  const record = (label: string, value: string) => (
    <div style={{ display: "grid", gridTemplateColumns: "minmax(0, 1fr) auto", gap: 8, alignItems: "center" }}>
      <label className={styles.field} style={{ margin: 0 }}><span>{label}</span><input readOnly value={value} className={styles.mono} onFocus={(e) => e.target.select()} /></label>
      <button type="button" className={styles.ghost} style={{ alignSelf: "end" }} onClick={() => copy(value)}>{copied === value ? "Disalin" : "Salin"}</button>
    </div>
  );

  return (
    <DashboardShell active="domain" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>Domain sendiri</h1>
          <p className="dashboard-subtitle">Pakai alamat kalian sendiri, misalnya <b>rinadanbima.com</b> atau <b>undangan.rinadanbima.com</b>. Link rawuh.id tetap berfungsi.</p>
        </div>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}

      <div className={styles.form}>
        {!allowed ? (
          <section className={styles.panel} aria-label="Butuh paket Premium">
            <h2>Tersedia di paket Premium</h2>
            <p className={styles.hint} style={{ margin: 0 }}>Upgrade paket untuk memakai domain sendiri. Domain bisa dibeli di penyedia mana saja (Niagahoster, Rumahweb, Cloudflare, dll).</p>
            <Link className="dashboard-action" href="/dashboard/paket" style={{ justifySelf: "start" }}>Lihat paket</Link>
          </section>
        ) : (
          <form className={styles.panel} onSubmit={add} aria-label="Tambah domain">
            <h2>Tambah domain</h2>
            <div className={styles.row} style={{ alignItems: "end" }}>
              <label className={styles.field}><span>Nama domain</span><input value={domain} onChange={(e) => setDomain(e.target.value)} placeholder="rinadanbima.com" autoCapitalize="none" autoCorrect="off" spellCheck={false} required /></label>
              <div><button type="submit" className="dashboard-action" disabled={busy === "add" || !domain.trim()}>{busy === "add" ? "Menambahkan…" : "Tambah domain"}</button></div>
            </div>
            <p className={styles.hint}>Belum punya domain? Beli dulu di penyedia domain, lalu kembali ke sini untuk menyambungkannya.</p>
          </form>
        )}

        {loading ? <p className="dashboard-state">Memuat…</p> : items.map((item) => {
          const check = checks[item.id];
          const apex = isApex(item.domain);
          const verified = item.status === "verified";
          return (
            <section key={item.id} className={styles.panel} aria-label={item.domain}>
              <div className={styles.panelHead}>
                <div>
                  <h2 style={{ wordBreak: "break-all" }}>{item.domain}</h2>
                  <p>{verified ? (check && !check.routing ? "Terverifikasi · menunggu arah DNS" : "Terhubung") : "Menunggu pengaturan DNS"}</p>
                </div>
                <span className={verified ? styles.ok : styles.hint} style={{ fontWeight: 700 }}>{verified ? "● Aktif" : "○ Belum aktif"}</span>
              </div>

              {verified && (!check || check.routing) ? (
                <p className={styles.hint} style={{ margin: 0 }}>
                  Tamu bisa membuka undangan di <a className={styles.link} href={`https://${item.domain}`} target="_blank" rel="noreferrer">https://{item.domain}</a>. Sertifikat HTTPS dibuat otomatis saat pertama kali dibuka (bisa butuh beberapa menit).
                </p>
              ) : (
                <>
                  <p className={styles.hint} style={{ margin: 0 }}>Buka pengaturan DNS <b>{rootDomain(item.domain)}</b> di penyedia domainmu, lalu tambahkan dua record ini:</p>
                  <div style={{ display: "grid", gap: 10 }}>
                    <strong style={{ fontSize: 13 }}>1. Bukti kepemilikan · tipe TXT</strong>
                    {record("Nama / Host", relativeHost(item.txt_name, item.domain))}
                    {record("Nilai / Value", item.txt_value)}
                    <strong style={{ fontSize: 13, marginTop: 6 }}>2. Arahkan domain · {apex ? "tipe A (atau ALIAS/ANAME)" : "tipe CNAME"}</strong>
                    {record("Nama / Host", relativeHost(item.domain, item.domain))}
                    {record(apex ? "Arahkan ke (ALIAS / ANAME)" : "Nilai / Target", item.cname_target || target)}
                    {apex && <p className={styles.hint} style={{ margin: 0 }}>Kalau penyedia domainmu tidak punya ALIAS/ANAME, pakai subdomain seperti <b>undangan.{item.domain}</b>, atau hubungi admin Rawuh untuk alamat IP record A.</p>}
                  </div>
                  {check?.detail && <p role="status" className={styles.hint} style={{ margin: 0, color: "var(--rw-ink)" }}>{check.detail}</p>}
                </>
              )}

              <div className={styles.itemActions} style={{ justifyContent: "flex-start", gap: 8 }}>
                <button type="button" className="dashboard-action" disabled={busy === item.id} onClick={() => verify(item)}>{busy === item.id ? "Mengecek DNS…" : verified ? "Cek ulang DNS" : "Cek & aktifkan"}</button>
                <button type="button" className="table-action table-action-danger" disabled={busy === item.id} onClick={() => remove(item)}>Hapus</button>
              </div>
            </section>
          );
        })}
      </div>
    </DashboardShell>
  );
}
