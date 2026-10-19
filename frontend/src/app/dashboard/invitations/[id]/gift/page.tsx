"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type Gift = {
  id: string;
  type: string;
  bank_name?: string;
  account_number?: string;
  account_name?: string;
  ewallet_provider?: string;
  ewallet_number?: string;
  qris_image_url?: string;
  address?: string;
  is_active: boolean;
};
type Envelope = { id: string; amount: number; status: string; sender_name?: string; message?: string; created_at: string };
type Payout = { id: string; amount: number; status: string; bank_name: string; account_number: string; account_name: string; note?: string; created_at: string; processed_at?: string };
type Wallet = { fee_percent: number; count: number; received: number; fee: number; net: number; paid_out: number; requested: number; available: number };
type WalletResponse = {
  online: { enabled: boolean; allowed: boolean; gateway_ready: boolean; platform_open?: boolean; active: boolean; note?: string };
  settings: { fee_percent: number; min_payout: number };
  wallet: Wallet;
  transactions: Envelope[];
  payouts: Payout[];
};

const giftTypeLabels: Record<string, string> = { bank: "Transfer bank", ewallet: "E-wallet", qris: "QRIS", address: "Alamat kirim kado" };
const emptyForm = { type: "bank", bank_name: "", account_number: "", account_name: "", ewallet_provider: "gopay", ewallet_number: "", qris_image_url: "", address: "" };
const rupiah = (value: number) => `Rp${Math.round(value).toLocaleString("id-ID")}`;
const date = (value?: string) => (value ? new Date(value).toLocaleDateString("id-ID", { day: "numeric", month: "short", year: "numeric" }) : "");
const envelopeStatus: Record<string, string> = { confirmed: "Diterima", pending: "Menunggu bayar", failed: "Batal" };
const payoutStatus: Record<string, string> = { requested: "Diproses", paid: "Sudah ditransfer", rejected: "Ditolak" };

async function json(response: Response) {
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.error);
  return body;
}

export default function GiftPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const invitationId = routeParams?.id;

  const [gifts, setGifts] = useState<Gift[]>([]);
  const [wallet, setWallet] = useState<WalletResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [form, setForm] = useState(emptyForm);
  const [payout, setPayout] = useState({ amount: "", bank_name: "", account_number: "", account_name: "" });
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!token || !invitationId) return;
    const [g, w]: [{ items?: Gift[] }, WalletResponse | null] = await Promise.all([
      apiFetch(`/api/invitations/${invitationId}/gifts`, token).then((r) => r.json()),
      apiFetch(`/api/invitations/${invitationId}/gift-wallet`, token).then((r) => (r.ok ? r.json() : null)),
    ]);
    setGifts(g.items ?? []);
    setWallet(w);
    if (w) setNote(w.online.note ?? "");
  }, [token, invitationId]);

  useEffect(() => {
    if (!ready || !token || !invitationId) return;
    const timer = setTimeout(() => {
      load().catch(() => setError("Gagal memuat data amplop")).finally(() => setLoading(false));
    }, 0);
    return () => clearTimeout(timer);
  }, [ready, token, invitationId, load]);

  async function run(key: string, action: () => Promise<void>, success?: string) {
    setBusy(key);
    setError("");
    setNotice("");
    try {
      await action();
      if (success) setNotice(success);
    } catch (err) {
      setError(err instanceof Error && err.message ? err.message : "Belum tersimpan. Coba lagi.");
    } finally {
      setBusy(null);
    }
  }

  // The switch lives in settings.sections_config.onlineGift; merge so other sections are untouched.
  const saveOnline = (enabled: boolean, text = note) => run("online", async () => {
    if (!token || !invitationId) return;
    setWallet((current) => (current ? { ...current, online: { ...current.online, enabled } } : current));
    try {
      const current = await apiFetch(`/api/invitations/${invitationId}/settings`, token).then((r) => r.json());
      const config = current.sections_config && typeof current.sections_config === "object" && !Array.isArray(current.sections_config) ? current.sections_config : {};
      await json(await apiFetch(`/api/invitations/${invitationId}/settings`, token, {
        method: "PATCH", body: JSON.stringify({ sections_config: { ...config, onlineGift: { enabled, note: text.trim() } } }),
      }));
    } finally {
      await load().catch(() => undefined);
    }
  }, enabled ? "Amplop online tampil di undangan." : "Amplop online disembunyikan dari undangan.");

  const toggleMethod = (gift: Gift) => run(gift.id, async () => {
    if (!token || !invitationId) return;
    await json(await apiFetch(`/api/invitations/${invitationId}/gifts/${gift.id}`, token, { method: "PATCH", body: JSON.stringify({ is_active: !gift.is_active }) }));
    await load();
  });

  const addMethod = (event: React.FormEvent) => {
    event.preventDefault();
    void run("add", async () => {
      if (!token || !invitationId) return;
      await json(await apiFetch(`/api/invitations/${invitationId}/gifts`, token, { method: "POST", body: JSON.stringify(form) }));
      setForm(emptyForm);
      await load();
    }, "Metode ditambahkan.");
  };

  const uploadQris = (file: File) => run("qris", async () => {
    if (!token || !invitationId) return;
    const data = new FormData();
    data.append("file", file);
    data.append("type", "qris");
    const body = await json(await apiFetch(`/api/invitations/${invitationId}/media`, token, { method: "POST", body: data }));
    setForm((prev) => ({ ...prev, qris_image_url: body.path }));
  });

  const verify = () => run("verify", async () => {
    if (!token || !invitationId) return;
    setWallet(await json(await apiFetch(`/api/invitations/${invitationId}/gift-wallet/verify`, token, { method: "POST" })));
  }, "Status pembayaran diperbarui.");

  const requestPayout = (event: React.FormEvent) => {
    event.preventDefault();
    void run("payout", async () => {
      if (!token || !invitationId) return;
      const response = await apiFetch(`/api/invitations/${invitationId}/gift-payouts`, token, {
        method: "POST", body: JSON.stringify({ ...payout, amount: Number(payout.amount.replace(/\D/g, "")) }),
      });
      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        throw new Error(String(body.error).includes("balance")
          ? "Nominal melebihi saldo yang bisa dicairkan."
          : `Periksa nominal (minimal ${rupiah(wallet?.settings.min_payout ?? 0)}) dan data rekening.`);
      }
      setPayout((current) => ({ ...current, amount: "" }));
      await load();
    }, "Pengajuan pencairan terkirim. Tim Rawuh akan mentransfer dalam 1–2 hari kerja.");
  };

  if (!ready || !invitationId) return null;

  const online = wallet?.online;
  const w = wallet?.wallet;
  const minPayout = wallet?.settings.min_payout ?? 0;
  const activeMethods = gifts.filter((gift) => gift.is_active).length;
  const showWallet = Boolean(online?.enabled || (wallet?.transactions.length ?? 0) > 0 || (wallet?.payouts.length ?? 0) > 0);

  return (
    <DashboardShell active="gift" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>Amplop digital</h1>
          <p className="dashboard-subtitle">Pilih cara tamu memberi: transfer langsung ke rekening kalian, amplop online lewat Rawuh, atau keduanya sekaligus.</p>
        </div>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {notice && <p role="status" className={styles.ok} style={{ margin: "0 0 12px" }}>{notice}</p>}

      {loading ? <p className="dashboard-state">Memuat…</p> : (
        <div className={styles.form}>
          <div className={styles.twoCol}>
            <section className={styles.panel} aria-label="Langsung ke rekening">
              <div className={styles.panelHead}>
                <div><h2>Langsung ke rekening kalian</h2><p>Tamu menyalin nomor rekening, e-wallet, atau scan QRIS kalian.</p></div>
                <span className={`status ${activeMethods ? "status-published" : "status-draft"}`}>{activeMethods ? `${activeMethods} tampil` : "Belum ada"}</span>
              </div>
              <ul className={styles.hint} style={{ margin: 0, paddingLeft: 18, display: "grid", gap: 4 }}>
                <li>Gratis, uang langsung masuk ke rekening kalian.</li>
                <li>Kalian cek sendiri siapa yang sudah transfer.</li>
              </ul>
              <a href="#metode" className={styles.link}>Atur rekening &amp; QRIS ↓</a>
            </section>

            <section className={styles.panel} aria-label="Amplop online lewat Rawuh">
              <div className={styles.panelHead}>
                <div><h2>Amplop online lewat Rawuh</h2><p>Tamu bayar langsung di undangan pakai QRIS, VA, atau e-wallet.</p></div>
                {online?.allowed && online.gateway_ready && online.platform_open && (
                  <label className={styles.check}>
                    <input type="checkbox" checked={online.enabled} disabled={busy === "online"} onChange={(e) => saveOnline(e.target.checked)} /> {online.enabled ? "Tampil" : "Nonaktif"}
                  </label>
                )}
              </div>
              <ul className={styles.hint} style={{ margin: 0, paddingLeft: 18, display: "grid", gap: 4 }}>
                <li>Tercatat otomatis lengkap dengan nama &amp; ucapan pengirim.</li>
                <li>Dana ditampung Rawuh, lalu kalian cairkan ke rekening kapan saja.</li>
                <li>Biaya layanan {wallet?.settings.fee_percent ? `${wallet.settings.fee_percent}% per amplop` : "gratis"} · minimal pencairan {rupiah(minPayout || 50000)}.</li>
              </ul>
              {online && online.platform_open === false ? (
                <p className={styles.hint}><strong>Segera hadir.</strong> Amplop online lewat Rawuh sedang kami siapkan. Sementara ini tamu bisa kirim lewat transfer langsung ke rekening kalian.</p>
              ) : !online?.allowed ? (
                <p className={styles.hint}><strong>Tersedia di paket dengan fitur amplop digital.</strong> <Link className={styles.link} href="/harga">Lihat paket →</Link></p>
              ) : !online.gateway_ready ? (
                <p className={styles.hint}>Pembayaran online belum dikonfigurasi. Hubungi admin Rawuh.</p>
              ) : null}
            </section>
          </div>

          {showWallet && w && (
            <section className={styles.panel} aria-label="Saldo amplop online">
              <div className={styles.panelHead}>
                <div><h2>Saldo amplop online</h2><p>{w.count} amplop diterima lewat Rawuh.</p></div>
                <button type="button" className={styles.ghost} disabled={busy === "verify"} onClick={verify}>{busy === "verify" ? "Memeriksa…" : "Cek pembayaran tertunda"}</button>
              </div>
              <div className={styles.row3}>
                <div className={styles.item} style={{ display: "grid", gap: 2 }}>
                  <small className={styles.hint}>Total diterima</small><strong style={{ fontSize: 20 }}>{rupiah(w.received)}</strong>
                  {w.fee > 0 && <small className={styles.hint}>Biaya layanan {rupiah(w.fee)}</small>}
                </div>
                <div className={styles.item} style={{ display: "grid", gap: 2 }}>
                  <small className={styles.hint}>Sudah dicairkan</small><strong style={{ fontSize: 20 }}>{rupiah(w.paid_out)}</strong>
                  {w.requested > 0 && <small className={styles.hint}>{rupiah(w.requested)} sedang diproses</small>}
                </div>
                <div className={styles.item} style={{ display: "grid", gap: 2, borderColor: "var(--rw-primary-border)", background: "var(--rw-primary-soft)" }}>
                  <small className={styles.hint}>Bisa dicairkan</small><strong style={{ fontSize: 20, color: "var(--rw-primary)" }}>{rupiah(w.available)}</strong>
                </div>
              </div>

              {online?.enabled && (
                <div className={styles.row} style={{ alignItems: "end" }}>
                  <label className={styles.field}><span>Pesan di atas formulir amplop (opsional)</span>
                    <input value={note} maxLength={200} onChange={(e) => setNote(e.target.value)} placeholder="Doa restu kalian sudah lebih dari cukup." />
                  </label>
                  <div><button type="button" className={styles.ghost} disabled={busy === "online"} onClick={() => saveOnline(true, note)}>Simpan pesan</button></div>
                </div>
              )}

              <form className={styles.editor} onSubmit={requestPayout} aria-label="Ajukan pencairan">
                <strong>Ajukan pencairan</strong>
                <div className={styles.row}>
                  <label className={styles.field}><span>Nominal (Rp)</span>
                    <input inputMode="numeric" value={payout.amount} placeholder={String(Math.floor(w.available))} onChange={(e) => setPayout({ ...payout, amount: e.target.value.replace(/[^\d]/g, "") })} required />
                  </label>
                  <label className={styles.field}><span>Bank</span><input value={payout.bank_name} onChange={(e) => setPayout({ ...payout, bank_name: e.target.value })} placeholder="BCA" required /></label>
                  <label className={styles.field}><span>Nomor rekening</span><input inputMode="numeric" value={payout.account_number} onChange={(e) => setPayout({ ...payout, account_number: e.target.value })} required /></label>
                  <label className={styles.field}><span>Atas nama</span><input value={payout.account_name} onChange={(e) => setPayout({ ...payout, account_name: e.target.value })} required /></label>
                </div>
                <div className={styles.actions}>
                  <button type="submit" className="dashboard-action" disabled={busy === "payout" || w.available < minPayout || w.available <= 0}>{busy === "payout" ? "Mengirim…" : "Ajukan pencairan"}</button>
                  <button type="button" className={styles.ghost} disabled={w.available <= 0} onClick={() => setPayout({ ...payout, amount: String(Math.floor(w.available)) })}>Cairkan semua</button>
                  {w.available < minPayout && <span className={styles.hint}>Minimal pencairan {rupiah(minPayout)}.</span>}
                </div>
              </form>

              {wallet.transactions.length > 0 && (
                <div className="dashboard-table-wrap">
                  <table className="dashboard-table" style={{ minWidth: 560 }}>
                    <thead><tr><th>Pengirim</th><th>Nominal</th><th>Status</th><th>Tanggal</th></tr></thead>
                    <tbody>
                      {wallet.transactions.map((tx) => (
                        <tr key={tx.id}>
                          <td><strong>{tx.sender_name || "Tamu"}</strong>{tx.message && <span>{tx.message}</span>}</td>
                          <td>{rupiah(tx.amount)}</td>
                          <td><span className={`status ${tx.status === "confirmed" ? "status-published" : "status-draft"}`}>{envelopeStatus[tx.status] ?? tx.status}</span></td>
                          <td>{date(tx.created_at)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {wallet.payouts.length > 0 && (
                <>
                  <strong style={{ fontSize: 14 }}>Riwayat pencairan</strong>
                  <div className="dashboard-table-wrap">
                    <table className="dashboard-table" style={{ minWidth: 560 }}>
                      <thead><tr><th>Tanggal</th><th>Nominal</th><th>Rekening</th><th>Status</th></tr></thead>
                      <tbody>
                        {wallet.payouts.map((p) => (
                          <tr key={p.id}>
                            <td>{date(p.created_at)}</td>
                            <td>{rupiah(p.amount)}</td>
                            <td><strong>{p.bank_name} · {p.account_number}</strong><span>{p.account_name}</span></td>
                            <td><span className={`status ${p.status === "paid" ? "status-published" : "status-draft"}`}>{payoutStatus[p.status] ?? p.status}</span>{p.note && <span>{p.note}</span>}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </>
              )}
            </section>
          )}

          <section className={styles.panel} id="metode" aria-label="Rekening, e-wallet, dan QRIS">
            <div className={styles.panelHead}><div><h2>Rekening, e-wallet &amp; QRIS kalian</h2><p>Tampil di undangan untuk tamu yang ingin transfer langsung.</p></div></div>
            {gifts.length > 0 ? (
              <ul className={styles.list}>
                {gifts.map((gift) => (
                  <li key={gift.id} className={styles.item}>
                    <div className={styles.itemBody}>
                      <strong>{giftTypeLabels[gift.type] ?? gift.type}</strong>
                      <small>
                        {gift.type === "bank" && `${gift.bank_name} · ${gift.account_number} · a.n. ${gift.account_name}`}
                        {gift.type === "ewallet" && `${gift.ewallet_provider} · ${gift.ewallet_number}`}
                        {gift.type === "qris" && "Gambar QRIS"}
                        {gift.type === "address" && gift.address}
                      </small>
                    </div>
                    <span className={`status ${gift.is_active ? "status-published" : "status-draft"}`}>{gift.is_active ? "Tampil" : "Disembunyikan"}</span>
                    <div className={styles.itemActions}>
                      <button type="button" className="table-action" disabled={busy === gift.id} onClick={() => toggleMethod(gift)}>{gift.is_active ? "Sembunyikan" : "Tampilkan"}</button>
                    </div>
                  </li>
                ))}
              </ul>
            ) : <p className={styles.empty}>Belum ada rekening. Tambahkan di bawah.</p>}

            <form className={styles.editor} onSubmit={addMethod} aria-label="Tambah metode">
              <strong>Tambah metode</strong>
              <label className={styles.field}><span>Jenis</span>
                <select value={form.type} onChange={(e) => setForm({ ...emptyForm, type: e.target.value })}>
                  <option value="bank">Transfer bank</option>
                  <option value="ewallet">E-wallet</option>
                  <option value="qris">QRIS</option>
                  <option value="address">Alamat kirim kado</option>
                </select>
              </label>
              {form.type === "bank" && (
                <div className={styles.row3}>
                  <label className={styles.field}><span>Nama bank</span><input value={form.bank_name} onChange={(e) => setForm({ ...form, bank_name: e.target.value })} placeholder="BCA" required /></label>
                  <label className={styles.field}><span>Nomor rekening</span><input inputMode="numeric" value={form.account_number} onChange={(e) => setForm({ ...form, account_number: e.target.value })} required /></label>
                  <label className={styles.field}><span>Atas nama</span><input value={form.account_name} onChange={(e) => setForm({ ...form, account_name: e.target.value })} required /></label>
                </div>
              )}
              {form.type === "ewallet" && (
                <div className={styles.row}>
                  <label className={styles.field}><span>Penyedia</span>
                    <select value={form.ewallet_provider} onChange={(e) => setForm({ ...form, ewallet_provider: e.target.value })}>
                      <option value="gopay">GoPay</option><option value="ovo">OVO</option><option value="dana">DANA</option><option value="shopeepay">ShopeePay</option>
                    </select>
                  </label>
                  <label className={styles.field}><span>Nomor</span><input inputMode="numeric" value={form.ewallet_number} onChange={(e) => setForm({ ...form, ewallet_number: e.target.value })} placeholder="081234567890" required /></label>
                </div>
              )}
              {form.type === "qris" && (
                <label className={styles.ghost} style={{ justifySelf: "start" }}>
                  {busy === "qris" ? "Mengunggah…" : form.qris_image_url ? "QRIS terunggah — ganti gambar" : "Unggah gambar QRIS"}
                  <input type="file" accept="image/jpeg,image/png,image/webp" hidden disabled={busy === "qris"} onChange={(e) => { const file = e.target.files?.[0]; e.target.value = ""; if (file) void uploadQris(file); }} />
                </label>
              )}
              {form.type === "address" && (
                <label className={styles.field}><span>Alamat</span><textarea rows={2} value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} required /></label>
              )}
              <div className={styles.actions}>
                <button type="submit" className="dashboard-action" disabled={busy === "add" || (form.type === "qris" && !form.qris_image_url)}>{busy === "add" ? "Menambahkan…" : "Tambah metode"}</button>
              </div>
            </form>
          </section>
        </div>
      )}
    </DashboardShell>
  );
}
