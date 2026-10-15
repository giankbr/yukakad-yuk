"use client";

import { useEffect, useState, type ReactNode } from "react";
import Link from "next/link";
import {
  Baby as PhBaby, BowlFood as PhBowlFood, Broadcast as PhBroadcast, CalendarPlus as PhCalendarPlus, CoatHanger as PhCoat, Gift as PhGift,
  HandHeart as PhHandHeart, ListChecks as PhListChecks, MapTrifold as PhMapTrifold, Plus as PhPlus, Question as PhQuestion,
  Quotes as PhQuotes, QrCode as PhQrCode, Trash as PhTrash, UsersThree as PhUsersThree, VideoCamera as PhVideoCamera,
} from "@phosphor-icons/react/ssr";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import type { InvitationExtras, WishlistItem } from "@/components/invitation/types";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";
import styles from "./sections.module.css";

type Key = Exclude<keyof InvitationExtras, "thankYou" | "onlineGift" | "guestPhotos" | "easyRead">;

const QUOTES = [
  { label: "QS. Ar-Rum: 21", text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang." },
  { label: "QS. Adz-Dzariyat: 49", text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah)." },
  { label: "QS. An-Nur: 32", text: "Dan nikahkanlah orang-orang yang masih membujang di antara kamu… Jika mereka miskin, Allah akan memberi kemampuan kepada mereka dengan karunia-Nya." },
  { label: "1 Korintus 13: 4–7", text: "Kasih itu sabar; kasih itu murah hati; ia tidak cemburu. Ia menutupi segala sesuatu, percaya segala sesuatu, mengharapkan segala sesuatu, sabar menanggung segala sesuatu." },
  { label: "Kejadian 2: 24", text: "Sebab itu seorang laki-laki akan meninggalkan ayahnya dan ibunya dan bersatu dengan isterinya, sehingga keduanya menjadi satu daging." },
];

/** Defaults used the first time a section is switched on. */
const DEFAULTS: { [K in Key]-?: NonNullable<InvitationExtras[K]> } = {
  quote: { text: QUOTES[0].text, source: QUOTES[0].label },
  child: { name: "" },
  calendar: {},
  livestream: { url: "", platform: "YouTube Live" },
  dressCode: { note: "", colors: ["#a3b18a", "#dad7cd"] },
  video: { url: "" },
  family: { names: [] },
  guestPass: {},
  rundown: { items: [{ time: "08.00", title: "Akad nikah" }] },
  travel: { items: [{ name: "" }] },
  wishlist: { items: [] },
  faq: { items: [{ q: "Boleh membawa anak?", a: "" }] },
  rsvpDietary: {},
};

const META: { key: Key; title: string; hint: string; icon: ReactNode; group: string }[] = [
  { key: "quote", title: "Ayat / kutipan pembuka", hint: "Ditampilkan setelah pembuka undangan.", icon: <PhQuotes size={18} />, group: "Pembuka" },
  { key: "child", title: "Profil anak", hint: "Untuk aqiqah, khitan, atau ulang tahun anak.", icon: <PhBaby size={18} />, group: "Pembuka" },
  { key: "calendar", title: "Simpan ke kalender", hint: "Tombol Google Calendar & iPhone/Outlook di bawah acara.", icon: <PhCalendarPlus size={18} />, group: "Acara" },
  { key: "rundown", title: "Susunan acara", hint: "Jadwal per jam di hari H.", icon: <PhListChecks size={18} />, group: "Acara" },
  { key: "dressCode", title: "Dress code", hint: "Catatan busana dan palet warna.", icon: <PhCoat size={18} />, group: "Acara" },
  { key: "livestream", title: "Live streaming", hint: "Link siaran untuk tamu yang tidak bisa hadir.", icon: <PhBroadcast size={18} />, group: "Acara" },
  { key: "guestPass", title: "QR tamu di undangan", hint: "Tamu dengan link pribadi melihat QR check-in miliknya.", icon: <PhQrCode size={18} />, group: "Acara" },
  { key: "video", title: "Video prewedding", hint: "YouTube, Vimeo, atau link .mp4.", icon: <PhVideoCamera size={18} />, group: "Cerita" },
  { key: "family", title: "Turut mengundang", hint: "Daftar keluarga besar yang turut mengundang.", icon: <PhUsersThree size={18} />, group: "Cerita" },
  { key: "travel", title: "Info tamu luar kota", hint: "Hotel, parkir, dan transportasi ke lokasi.", icon: <PhMapTrifold size={18} />, group: "Penutup" },
  { key: "wishlist", title: "Wishlist kado", hint: "Tamu menandai kado yang akan dibelikan agar tidak dobel.", icon: <PhGift size={18} />, group: "Penutup" },
  { key: "faq", title: "FAQ acara", hint: "Jawaban untuk pertanyaan yang sering muncul.", icon: <PhQuestion size={18} />, group: "Penutup" },
  { key: "rsvpDietary", title: "Pertanyaan alergi makanan", hint: "Kolom tambahan di form RSVP.", icon: <PhBowlFood size={18} />, group: "RSVP" },
];

function isOn(extras: InvitationExtras, key: Key) {
  if (key === "calendar") return extras.calendar?.enabled !== false;
  const value = extras[key] as { enabled?: boolean } | undefined;
  return Boolean(value) && value?.enabled !== false;
}

function newId() {
  return Math.random().toString(36).slice(2, 10);
}

export default function SectionsPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const invitationId = routeParams?.id;
  const [extras, setExtras] = useState<InvitationExtras>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [dirty, setDirty] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [open, setOpen] = useState<Key | "thankYou" | null>(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    if (!ready || !token || !invitationId) return;
    apiFetch(`/api/invitations/${invitationId}/settings`, token)
      .then(response => response.json())
      .then((body: { sections_config?: unknown }) => {
        const config = body.sections_config;
        setExtras(config && typeof config === "object" && !Array.isArray(config) ? config as InvitationExtras : {});
      })
      .catch(() => setError("Section gagal dimuat. Coba muat ulang halaman."))
      .finally(() => setLoading(false));
  }, [ready, token, invitationId]);

  function update<K extends keyof InvitationExtras>(key: K, value: InvitationExtras[K]) {
    setExtras(current => ({ ...current, [key]: value }));
    setDirty(true);
    setNotice("");
  }

  function patch<K extends Key>(key: K, value: Partial<NonNullable<InvitationExtras[K]>>) {
    update(key, { ...(extras[key] ?? DEFAULTS[key]), ...value } as InvitationExtras[K]);
  }

  function toggle(key: Key) {
    const enabled = !isOn(extras, key);
    update(key, { ...(extras[key] ?? DEFAULTS[key]), enabled } as InvitationExtras[typeof key]);
    if (enabled) setOpen(key);
  }

  async function save() {
    if (!token || !invitationId) return;
    setSaving(true);
    setError("");
    try {
      // Re-read wishlist claims made by guests since this page was opened so they aren't overwritten.
      const latest = await apiFetch(`/api/invitations/${invitationId}/settings`, token).then(r => r.json()).catch(() => ({}));
      const claims = new Map<string, string>(((latest?.sections_config?.wishlist?.items ?? []) as WishlistItem[])
        .filter(item => item.claimed_by).map(item => [item.id, item.claimed_by as string]));
      const base: InvitationExtras = extras.wishlist
        ? { ...extras, wishlist: { ...extras.wishlist, items: extras.wishlist.items.map(item => item.claimed_by === "" ? item : { ...item, claimed_by: item.claimed_by ?? claims.get(item.id) }) } }
        : extras;
      // These switches live on their own pages (Amplop, Foto dari tamu, Tema); keep whatever was saved there.
      const latestConfig = (latest?.sections_config ?? {}) as InvitationExtras;
      const merged: InvitationExtras = {
        ...base,
        onlineGift: latestConfig.onlineGift ?? extras.onlineGift,
        guestPhotos: latestConfig.guestPhotos ?? extras.guestPhotos,
        easyRead: latestConfig.easyRead ?? extras.easyRead,
      };
      const response = await apiFetch(`/api/invitations/${invitationId}/settings`, token, { method: "PATCH", body: JSON.stringify({ sections_config: merged }) });
      if (!response.ok) throw new Error();
      setExtras(merged);
      setDirty(false);
      setNotice("Tersimpan. Section langsung tampil di semua tema undangan.");
    } catch {
      setError("Belum tersimpan. Periksa koneksi lalu coba lagi.");
    } finally {
      setSaving(false);
    }
  }

  async function uploadChildPhoto(file: File) {
    if (!token || !invitationId) return;
    setUploading(true);
    try {
      const form = new FormData();
      form.append("file", file);
      form.append("type", "cover");
      const response = await apiFetch(`/api/invitations/${invitationId}/media`, token, { method: "POST", body: form });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error);
      patch("child", { photo: body.path });
    } catch {
      setError("Foto belum terunggah. Gunakan JPG, PNG, atau WebP maksimal 10 MB.");
    } finally {
      setUploading(false);
    }
  }

  if (!ready || !invitationId || !token) return null;

  const groups = Array.from(new Set(META.map(item => item.group)));
  const thankMode = extras.thankYou?.mode ?? "auto";

  function editor(key: Key): ReactNode {
    switch (key) {
      case "quote": {
        const quote = extras.quote ?? DEFAULTS.quote;
        return <>
          <div className={styles.presets}>
            {QUOTES.map(item => (
              <button key={item.label} type="button" aria-pressed={quote.source === item.label} onClick={() => patch("quote", { text: item.text, source: item.label })}>{item.label}</button>
            ))}
          </div>
          <Area label="Teks" value={quote.text} rows={4} onChange={text => patch("quote", { text })} />
          <Field label="Sumber" value={quote.source ?? ""} onChange={source => patch("quote", { source })} placeholder="QS. Ar-Rum: 21" />
        </>;
      }
      case "child": {
        const child = extras.child ?? DEFAULTS.child;
        return <>
          <div className={styles.row}>
            <Field label="Nama lengkap anak" value={child.name} onChange={name => patch("child", { name })} placeholder="Muhammad Arkan Pratama" />
            <Field label="Nama panggilan" value={child.nickname ?? ""} onChange={nickname => patch("child", { nickname })} placeholder="Arkan" />
          </div>
          <div className={styles.row}>
            <Field label="Tanggal lahir" type="date" value={child.birthDate?.slice(0, 10) ?? ""} onChange={birthDate => patch("child", { birthDate })} />
            <Field label="Putra/putri dari" value={child.parents ?? ""} onChange={parents => patch("child", { parents })} placeholder="Bpk. Rizky & Ibu Nadia" />
          </div>
          <Area label="Arti nama / doa" value={child.meaning ?? ""} rows={3} onChange={meaning => patch("child", { meaning })} />
          <div className={styles.upload}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            {child.photo && <img src={child.photo} alt="" />}
            <label className={styles.ghost}>{uploading ? "Mengunggah…" : child.photo ? "Ganti foto" : "Unggah foto anak"}
              <input type="file" accept="image/jpeg,image/png,image/webp" hidden disabled={uploading} onChange={event => { const file = event.target.files?.[0]; event.target.value = ""; if (file) void uploadChildPhoto(file); }} />
            </label>
            {child.photo && <button type="button" className={styles.link} onClick={() => patch("child", { photo: "" })}>Hapus foto</button>}
          </div>
        </>;
      }
      case "calendar":
        return <p className={styles.hint}>Otomatis dibuat dari tanggal dan jam di halaman Acara. Tidak perlu diisi.</p>;
      case "livestream": {
        const live = extras.livestream ?? DEFAULTS.livestream;
        return <>
          <Field label="Link siaran" value={live.url} onChange={url => patch("livestream", { url })} placeholder="https://youtube.com/live/…" type="url" />
          <div className={styles.row}>
            <Select label="Platform" value={live.platform ?? ""} onChange={platform => patch("livestream", { platform })} options={["YouTube Live", "Instagram Live", "Zoom", "Google Meet", "TikTok Live"]} />
            <Field label="Mulai siaran" type="datetime-local" value={toLocalInput(live.startsAt)} onChange={value => patch("livestream", { startsAt: value ? `${value}:00+07:00` : "" })} />
          </div>
          <Field label="Catatan (opsional)" value={live.note ?? ""} onChange={note => patch("livestream", { note })} placeholder="Tidak bisa hadir? Ikuti momen bahagia kami secara langsung." />
        </>;
      }
      case "dressCode": {
        const dress = extras.dressCode ?? DEFAULTS.dressCode;
        const colors = dress.colors ?? [];
        return <>
          <Field label="Catatan busana" value={dress.note} onChange={note => patch("dressCode", { note })} placeholder="Nuansa earth tone. Batik dipersilakan." />
          <div className={styles.field}>
            <span>Palet warna (maks. 6)</span>
            <div className={styles.colors}>
              {colors.map((color, index) => (
                <span key={index} className={styles.color}>
                  <input type="color" value={color} aria-label={`Warna ${index + 1}`} onChange={event => patch("dressCode", { colors: colors.map((c, i) => i === index ? event.target.value : c) })} />
                  <button type="button" aria-label="Hapus warna" onClick={() => patch("dressCode", { colors: colors.filter((_, i) => i !== index) })}>×</button>
                </span>
              ))}
              {colors.length < 6 && <button type="button" className={styles.addColor} onClick={() => patch("dressCode", { colors: [...colors, "#d4c5b0"] })} aria-label="Tambah warna"><PhPlus size={14} /></button>}
            </div>
          </div>
        </>;
      }
      case "video": {
        const video = extras.video ?? DEFAULTS.video;
        return <>
          <Field label="Link video" type="url" value={video.url} onChange={url => patch("video", { url })} placeholder="https://youtu.be/…" />
          <Field label="Judul (opsional)" value={video.title ?? ""} onChange={title => patch("video", { title })} placeholder="Our prewedding film" />
        </>;
      }
      case "family": {
        const family = extras.family ?? DEFAULTS.family;
        return <>
          <Field label="Judul" value={family.title ?? ""} onChange={title => patch("family", { title })} placeholder="Turut mengundang" />
          <Area label="Nama (satu per baris)" rows={6} value={family.names.join("\n")} onChange={value => patch("family", { names: value.split("\n") })} placeholder={"Kel. Besar Bpk. Hartono\nKel. Besar Bpk. Suryadi"} />
        </>;
      }
      case "guestPass": {
        const pass = extras.guestPass ?? DEFAULTS.guestPass;
        return <>
          <p className={styles.hint}>QR hanya muncul untuk tamu yang membuka link pribadi dari halaman <Link href={`/dashboard/invitations/${invitationId}/guests`}>Tamu</Link>. Scan di halaman Check-in.</p>
          <Field label="Catatan di bawah QR" value={pass.note ?? ""} onChange={note => patch("guestPass", { note })} placeholder="Tunjukkan kode ini ke penerima tamu saat tiba di lokasi." />
        </>;
      }
      case "rundown": {
        const items = (extras.rundown ?? DEFAULTS.rundown).items;
        const set = (next: typeof items) => patch("rundown", { items: next });
        return <Repeater
          items={items} onChange={set} empty={{ time: "", title: "" }} addLabel="Tambah agenda"
          render={(item, change) => <>
            <Field label="Jam" value={item.time} onChange={time => change({ ...item, time })} placeholder="08.00" className={styles.narrow} />
            <Field label="Agenda" value={item.title} onChange={title => change({ ...item, title })} placeholder="Akad nikah" />
            <Field label="Keterangan" value={item.note ?? ""} onChange={note => change({ ...item, note })} placeholder="Opsional" />
          </>}
        />;
      }
      case "travel": {
        const travel = extras.travel ?? DEFAULTS.travel;
        return <>
          <Area label="Catatan umum" rows={2} value={travel.note ?? ""} onChange={note => patch("travel", { note })} placeholder="Untuk tamu dari luar kota, berikut pilihan terdekat dari lokasi." />
          <Repeater
            items={travel.items} onChange={items => patch("travel", { items })} empty={{ name: "" }} addLabel="Tambah info"
            render={(item, change) => <>
              <Field label="Nama" value={item.name} onChange={name => change({ ...item, name })} placeholder="Hotel Santika" />
              <Field label="Keterangan" value={item.detail ?? ""} onChange={detail => change({ ...item, detail })} placeholder="± 800 m dari gedung" />
              <Field label="Link" type="url" value={item.url ?? ""} onChange={url => change({ ...item, url })} placeholder="https://maps.app.goo.gl/…" />
            </>}
          />
        </>;
      }
      case "wishlist": {
        const wishlist = extras.wishlist ?? DEFAULTS.wishlist;
        return <>
          <Field label="Catatan" value={wishlist.note ?? ""} onChange={note => patch("wishlist", { note })} placeholder="Tandai kado yang akan kamu berikan supaya tidak dobel." />
          <p className={styles.hint}>Kado “patungan” bisa dibayar bareng-bareng lewat amplop online. Aktifkan dulu amplop online di menu Amplop digital.</p>
          <Repeater
            items={wishlist.items} onChange={items => patch("wishlist", { items })} empty={{ id: newId(), name: "" } as WishlistItem} addLabel="Tambah kado"
            render={(item, change) => <>
              <Field label="Nama kado" value={item.name} onChange={name => change({ ...item, name })} placeholder="Rice cooker digital" />
              <Field label="Harga" value={item.price ?? ""} onChange={price => change({ ...item, price })} placeholder="± Rp850.000" className={styles.narrow} />
              <Field label="Link toko" type="url" value={item.url ?? ""} onChange={url => change({ ...item, url })} placeholder="https://…" />
              <label className={styles.field}><span>Patungan</span>
                <select value={item.fund ? "fund" : "claim"} onChange={event => change({ ...item, fund: event.target.value === "fund", target: event.target.value === "fund" ? item.target || Number((item.price ?? "").replace(/\D/g, "")) || undefined : item.target })}>
                  <option value="claim">Satu tamu membelikan</option>
                  <option value="fund">Patungan lewat amplop online</option>
                </select>
              </label>
              {item.fund && <Field label="Target (Rp)" inputMode="numeric" value={item.target ? String(item.target) : ""} onChange={value => change({ ...item, target: Number(value.replace(/\D/g, "")) || undefined })} placeholder="4000000" className={styles.narrow} />}
              {item.claimed_by && (
                <p className={styles.claimed}>Dipilih oleh <b>{item.claimed_by}</b> · <button type="button" className={styles.link} onClick={() => change({ ...item, claimed_by: "" })}>Buka lagi</button></p>
              )}
            </>}
            freshItem={(): WishlistItem => ({ id: newId(), name: "" })}
          />
        </>;
      }
      case "faq": {
        const items = (extras.faq ?? DEFAULTS.faq).items;
        return <Repeater
          items={items} onChange={next => patch("faq", { items: next })} empty={{ q: "", a: "" }} addLabel="Tambah pertanyaan" stacked
          render={(item, change) => <>
            <Field label="Pertanyaan" value={item.q} onChange={q => change({ ...item, q })} placeholder="Apakah tersedia parkir?" />
            <Area label="Jawaban" rows={2} value={item.a} onChange={a => change({ ...item, a })} />
          </>}
        />;
      }
      case "rsvpDietary": {
        const dietary = extras.rsvpDietary ?? DEFAULTS.rsvpDietary;
        return <>
          <Field label="Label pertanyaan" value={dietary.label ?? ""} onChange={label => patch("rsvpDietary", { label })} placeholder="Alergi / pantangan makanan (opsional)" />
          <p className={styles.hint}>Jawaban tamu muncul di pesan RSVP pada halaman RSVP.</p>
        </>;
      }
    }
  }

  return (
    <DashboardShell active="sections" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>Section Tambahan</h1>
          <p className="dashboard-subtitle">Aktifkan bagian ekstra. Semua otomatis mengikuti warna dan font tema yang kamu pilih.</p>
        </div>
        <Link className="dashboard-action" href={`/dashboard/invitations/${invitationId}/preview`}>Pratinjau undangan</Link>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}

      {loading ? <p className="dashboard-state">Memuat section…</p> : (
        <div className={styles.wrap}>
          {groups.map(group => (
            <section key={group} className={styles.group} aria-label={group}>
              <h2>{group}</h2>
              {META.filter(item => item.group === group).map(item => {
                const enabled = isOn(extras, item.key);
                const expanded = open === item.key;
                return (
                  <article key={item.key} className={styles.item} data-on={enabled || undefined}>
                    <div className={styles.itemHead}>
                      <span className={styles.icon}>{item.icon}</span>
                      <button type="button" className={styles.itemTitle} aria-expanded={expanded} onClick={() => setOpen(expanded ? null : item.key)}>
                        <strong>{item.title}</strong>
                        <small>{item.hint}</small>
                      </button>
                      <button type="button" role="switch" aria-checked={enabled} aria-label={`Aktifkan ${item.title}`} className={styles.switch} onClick={() => toggle(item.key)}><i /></button>
                    </div>
                    {expanded && <div className={styles.itemBody}>{editor(item.key)}</div>}
                  </article>
                );
              })}
            </section>
          ))}

          <section className={styles.group} aria-label="Setelah acara">
            <h2>Setelah acara</h2>
            <article className={styles.item} data-on={thankMode !== "off" || undefined}>
              <div className={styles.itemHead}>
                <span className={styles.icon}><PhHandHeart size={18} /></span>
                <button type="button" className={styles.itemTitle} aria-expanded={open === "thankYou"} onClick={() => setOpen(open === "thankYou" ? null : "thankYou")}>
                  <strong>Mode terima kasih</strong>
                  <small>Setelah acara, undangan berubah jadi ucapan terima kasih dan RSVP ditutup.</small>
                </button>
              </div>
              {open === "thankYou" && (
                <div className={styles.itemBody}>
                  <div className={styles.segment} role="radiogroup" aria-label="Mode terima kasih">
                    {([["auto", "Otomatis setelah acara"], ["on", "Aktif sekarang"], ["off", "Mati"]] as const).map(([value, label]) => (
                      <button key={value} type="button" role="radio" aria-checked={thankMode === value} onClick={() => update("thankYou", { ...extras.thankYou, mode: value })}>{label}</button>
                    ))}
                  </div>
                  <Area label="Pesan terima kasih" rows={3} value={extras.thankYou?.message ?? ""} onChange={message => update("thankYou", { mode: thankMode, ...extras.thankYou, message })}
                    placeholder="Terima kasih atas doa, kehadiran, dan kasih sayang yang kalian berikan di hari bahagia kami." />
                </div>
              )}
            </article>
          </section>
        </div>
      )}

      <div className={styles.saveBar} data-dirty={dirty || undefined}>
        <span role="status">{notice || (dirty ? "Ada perubahan yang belum disimpan." : "Semua perubahan tersimpan.")}</span>
        <button type="button" className={styles.save} disabled={saving || !dirty} onClick={save}>{saving ? "Menyimpan…" : "Simpan perubahan"}</button>
      </div>
    </DashboardShell>
  );
}

/* ── Small form helpers ─────────────────────────────────────────── */

function toLocalInput(value?: string) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  // Show the time in WIB regardless of the browser's zone.
  return new Date(date.getTime() + 7 * 60 * 60 * 1000).toISOString().slice(0, 16);
}

function Field({ label, value, onChange, className, ...props }: { label: string; value: string; onChange: (value: string) => void; className?: string } & Omit<React.InputHTMLAttributes<HTMLInputElement>, "value" | "onChange" | "className">) {
  return <label className={`${styles.field} ${className ?? ""}`}><span>{label}</span><input value={value} onChange={event => onChange(event.target.value)} {...props} /></label>;
}

function Area({ label, value, onChange, ...props }: { label: string; value: string; onChange: (value: string) => void } & Omit<React.TextareaHTMLAttributes<HTMLTextAreaElement>, "value" | "onChange">) {
  return <label className={styles.field}><span>{label}</span><textarea value={value} onChange={event => onChange(event.target.value)} {...props} /></label>;
}

function Select({ label, value, onChange, options }: { label: string; value: string; onChange: (value: string) => void; options: string[] }) {
  return (
    <label className={styles.field}><span>{label}</span>
      <select value={value} onChange={event => onChange(event.target.value)}>{options.map(option => <option key={option}>{option}</option>)}</select>
    </label>
  );
}

function Repeater<T>({ items, onChange, render, empty, addLabel, stacked, freshItem }: {
  items: T[]; onChange: (items: T[]) => void; render: (item: T, change: (item: T) => void) => ReactNode; empty: T; addLabel: string; stacked?: boolean; freshItem?: () => T;
}) {
  return (
    <div className={styles.repeater}>
      {items.map((item, index) => (
        <div key={index} className={styles.repeatRow} data-stacked={stacked || undefined}>
          {render(item, next => onChange(items.map((entry, i) => i === index ? next : entry)))}
          <button type="button" className={styles.remove} aria-label="Hapus baris" onClick={() => onChange(items.filter((_, i) => i !== index))}><PhTrash size={15} /></button>
        </div>
      ))}
      <button type="button" className={styles.ghost} onClick={() => onChange([...items, freshItem ? freshItem() : { ...empty }])}><PhPlus size={14} /> {addLabel}</button>
    </div>
  );
}
