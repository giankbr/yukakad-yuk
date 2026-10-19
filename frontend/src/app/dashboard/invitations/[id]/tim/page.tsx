"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { ROLE_DESCRIPTIONS, ROLE_LABELS, type AccessRole } from "@/lib/invitation-access";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type MemberRole = Exclude<AccessRole, "owner">;
type Member = { id: string; name?: string; email?: string; role: MemberRole; status: "pending" | "active"; expires_at?: string; accepted_at?: string; created_at: string };
const ROLES: MemberRole[] = ["receptionist", "editor", "organizer"];

export default function TeamPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const invitationId = routeParams?.id;
  const [members, setMembers] = useState<Member[]>([]);
  const [limit, setLimit] = useState<number | null>(null);
  const [role, setRole] = useState<MemberRole>("receptionist");
  const [email, setEmail] = useState("");
  const [link, setLink] = useState<{ url: string; label: string } | null>(null);
  const [copied, setCopied] = useState(false);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const load = useCallback(async () => {
    if (!token || !invitationId) return;
    const response = await apiFetch(`/api/invitations/${invitationId}/team`, token);
    const body = await response.json();
    if (!response.ok) throw new Error(body.error);
    setMembers(body.items ?? []);
    setLimit(typeof body.limit === "number" ? body.limit : null);
  }, [token, invitationId]);

  useEffect(() => {
    if (!ready || !token || !invitationId) return;
    const timer = setTimeout(() => { load().catch(() => setError("Gagal memuat tim")).finally(() => setLoading(false)); }, 0);
    return () => clearTimeout(timer);
  }, [ready, token, invitationId, load]);

  async function run(key: string, action: () => Promise<void>) {
    setBusy(key);
    setError("");
    setNotice("");
    try {
      await action();
    } catch (err) {
      setError(err instanceof Error && err.message ? err.message : "Belum tersimpan.");
    } finally {
      setBusy(null);
    }
  }

  const invite = (event: React.FormEvent) => {
    event.preventDefault();
    void run("invite", async () => {
      const response = await apiFetch(`/api/invitations/${invitationId}/team`, token!, { method: "POST", body: JSON.stringify({ role, email: email.trim() }) });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error);
      setLink({ url: body.invite_url, label: `${ROLE_LABELS[role]}${email.trim() ? ` · ${email.trim()}` : ""}` });
      setCopied(false);
      setEmail("");
      await load();
    });
  };

  const newLink = (member: Member) => run(member.id, async () => {
    const response = await apiFetch(`/api/invitations/${invitationId}/team/${member.id}/link`, token!, { method: "POST" });
    const body = await response.json();
    if (!response.ok) throw new Error(body.error);
    setLink({ url: body.invite_url, label: `${ROLE_LABELS[member.role]}${member.email ? ` · ${member.email}` : ""}` });
    setCopied(false);
  });

  const changeRole = (member: Member, next: MemberRole) => run(member.id, async () => {
    const response = await apiFetch(`/api/invitations/${invitationId}/team/${member.id}`, token!, { method: "PATCH", body: JSON.stringify({ role: next }) });
    const body = await response.json();
    if (!response.ok) throw new Error(body.error);
    setMembers((current) => current.map((m) => (m.id === member.id ? { ...m, role: next } : m)));
    setNotice(`${member.name || member.email || "Anggota"} sekarang ${ROLE_LABELS[next]}.`);
  });

  const remove = (member: Member) => {
    if (!window.confirm(`Cabut akses ${member.name || member.email || "anggota ini"}?`)) return;
    void run(member.id, async () => {
      const response = await apiFetch(`/api/invitations/${invitationId}/team/${member.id}`, token!, { method: "DELETE" });
      if (!response.ok) throw new Error((await response.json()).error);
      setMembers((current) => current.filter((m) => m.id !== member.id));
      setNotice("Akses dicabut.");
    });
  };

  async function copy() {
    if (!link) return;
    try { await navigator.clipboard.writeText(link.url); setCopied(true); } catch { setCopied(false); }
  }

  if (!ready || !invitationId) return null;
  const waText = link ? encodeURIComponent(`Halo! Aku mengajakmu membantu undangan kami di Rawuh sebagai ${link.label.split(" · ")[0]}. Buka link ini untuk bergabung (berlaku 7 hari):\n${link.url}`) : "";

  return (
    <DashboardShell active="team" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan ini</p>
          <h1>Tim &amp; akses</h1>
          <p className="dashboard-subtitle">Ajak keluarga, WO, atau penerima tamu membantu. Mereka masuk dengan akun Rawuh masing-masing dan hanya melihat menu sesuai perannya.</p>
        </div>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {notice && <p role="status" className={styles.ok} style={{ margin: "0 0 12px" }}>{notice}</p>}

      <div className={styles.form}>
        <form className={styles.panel} onSubmit={invite} aria-label="Undang anggota">
          <h2>Undang anggota</h2>
          {limit !== null && limit > 0 && (
            <p className={styles.hint} style={{ margin: 0 }}>
              {members.length} dari {limit} anggota terpakai di paketmu.
              {members.length >= limit && <> Tim sudah penuh. <Link className={styles.link} href="/dashboard/paket">Upgrade paket →</Link></>}
            </p>
          )}
          <div role="radiogroup" aria-label="Peran" style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 10 }}>
            {ROLES.map((r) => (
              <label key={r} className={styles.item} style={{ display: "grid", gap: 4, cursor: "pointer", ...(role === r ? { borderColor: "var(--rw-primary)", background: "var(--rw-primary-soft)" } : {}) }}>
                <span style={{ display: "flex", alignItems: "center", justifyContent: "flex-start", gap: 8 }}>
                  <input type="radio" name="role" value={r} checked={role === r} onChange={() => setRole(r)} style={{ flex: "none", width: 16, height: 16, minHeight: 0, margin: 0, padding: 0, accentColor: "var(--rw-primary)" }} />
                  <strong style={{ fontSize: 14 }}>{ROLE_LABELS[r]}</strong>
                </span>
                <small className={styles.hint}>{ROLE_DESCRIPTIONS[r]}</small>
              </label>
            ))}
          </div>
          <div className={styles.row} style={{ alignItems: "end" }}>
            <label className={styles.field}><span>Email (opsional, sebagai catatan)</span><input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="tante.sri@gmail.com" /></label>
            <div><button type="submit" className="dashboard-action" disabled={busy === "invite"}>{busy === "invite" ? "Membuat link…" : "Buat link undangan"}</button></div>
          </div>
          <p className={styles.hint}>Siapa pun yang membuka link ini dan masuk ke akunnya akan bergabung, jadi kirim lewat chat pribadi. Link berlaku 7 hari dan hanya bisa dipakai sekali.</p>
        </form>

        {link && (
          <section className={styles.panel} aria-label="Link undangan" style={{ borderColor: "var(--rw-primary-border)" }}>
            <div className={styles.panelHead}><div><h2>Link untuk {link.label}</h2><p>Kirimkan ke orangnya. Setelah bergabung, mereka muncul di daftar di bawah.</p></div></div>
            <label className={styles.field}><span className="sr-only">Link undangan</span><input readOnly value={link.url} className={styles.mono} onFocus={(e) => e.target.select()} /></label>
            <div className={styles.actions}>
              <button type="button" className="dashboard-action" onClick={copy}>{copied ? "Tersalin ✓" : "Salin link"}</button>
              <a className={styles.ghost} href={`https://wa.me/?text=${waText}`} target="_blank" rel="noreferrer">Kirim lewat WhatsApp</a>
            </div>
          </section>
        )}

        <section className={styles.panel} aria-label="Anggota tim">
          <div className={styles.panelHead}><div><h2>Anggota tim</h2><p>{members.filter((m) => m.status === "active").length} bergabung · {members.filter((m) => m.status === "pending").length} menunggu</p></div></div>
          {loading ? <p className="dashboard-state">Memuat…</p> : members.length === 0 ? <p className={styles.empty}>Belum ada anggota. Kamu satu-satunya yang bisa mengelola undangan ini.</p> : (
            <ul className={styles.list}>
              {members.map((member) => {
                const expired = member.status === "pending" && member.expires_at && new Date(member.expires_at) < new Date();
                return (
                  <li key={member.id} className={styles.item} style={{ alignItems: "center" }}>
                    <div className={styles.itemBody}>
                      <strong>{member.name || member.email || "Belum bergabung"}</strong>
                      <small>
                        {member.status === "active"
                          ? `${member.email ?? ""}${member.accepted_at ? ` · bergabung ${new Date(member.accepted_at).toLocaleDateString("id-ID", { day: "numeric", month: "short" })}` : ""}`
                          : expired ? "Link kedaluwarsa" : "Menunggu bergabung lewat link"}
                      </small>
                    </div>
                    <label className={styles.field} style={{ width: 190 }}><span className="sr-only">Peran</span>
                      <select value={member.role} disabled={busy === member.id} onChange={(e) => changeRole(member, e.target.value as MemberRole)}>
                        {ROLES.map((r) => <option key={r} value={r}>{ROLE_LABELS[r]}</option>)}
                      </select>
                    </label>
                    <div className={styles.itemActions}>
                      {member.status === "pending" && <button type="button" className="table-action" disabled={busy === member.id} onClick={() => newLink(member)}>Link baru</button>}
                      <button type="button" className="table-action table-action-danger" disabled={busy === member.id} onClick={() => remove(member)}>{member.status === "pending" ? "Batalkan" : "Cabut akses"}</button>
                    </div>
                  </li>
                );
              })}
            </ul>
          )}
        </section>

        <section className={styles.panel} aria-label="Hak akses per peran">
          <h2>Hak akses per peran</h2>
          <div className="dashboard-table-wrap">
            <table className="dashboard-table" style={{ minWidth: 560 }}>
              <thead><tr><th>Bisa…</th><th>Penerima tamu</th><th>Keluarga</th><th>WO / vendor</th></tr></thead>
              <tbody>
                {[
                  ["Scan check-in & catat amplop", true, false, true],
                  ["Buka layar sapa", true, true, true],
                  ["Ubah isi undangan (mempelai, acara, galeri, tema)", false, true, true],
                  ["Kelola tamu, RSVP & ucapan", false, true, true],
                  ["Lihat buku buwuh", false, true, true],
                  ["Doorprize & foto tamu", false, false, true],
                  ["Rekening, saldo amplop & pencairan", false, false, false],
                  ["Terbitkan, ganti link, hapus undangan, kelola tim", false, false, false],
                ].map(([label, ...flags]) => (
                  <tr key={String(label)}><td>{label}</td>{flags.map((flag, i) => <td key={i}>{flag ? "✓" : "—"}</td>)}</tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className={styles.hint}>Hal yang menyangkut uang dan pengaturan undangan selalu hanya bisa dilakukan pemilik.</p>
        </section>
      </div>
    </DashboardShell>
  );
}
