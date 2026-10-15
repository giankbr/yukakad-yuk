"use client";

import { useId, useState } from "react";
import { apiFetch } from "@/lib/api";
import styles from "./editor.module.css";

/** Image picker for admin content: upload to object storage, or paste a path/URL. */
export function ImageField({ label, value, onChange, token, folder = "site", hint }: {
  label: string; value: string; onChange: (value: string) => void; token: string; folder?: string; hint?: string;
}) {
  const id = useId();
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  async function upload(file: File) {
    setUploading(true);
    setError("");
    try {
      const form = new FormData();
      form.append("file", file);
      form.append("folder", folder);
      const response = await apiFetch("/api/admin/uploads", token, { method: "POST", body: form });
      const body = await response.json().catch(() => ({}));
      if (!response.ok || !body.url) throw new Error(response.status === 503 ? "Penyimpanan file belum dikonfigurasi. Isi path gambar secara manual." : body.error);
      onChange(body.url);
    } catch (err) {
      setError(err instanceof Error && err.message ? err.message : "Gagal mengunggah. Gunakan JPG, PNG, atau WebP maksimal 10 MB.");
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className={styles.image}>
      {/* eslint-disable-next-line @next/next/no-img-element */}
      {value ? <img src={value} alt="" /> : <span className={styles.imageEmpty}>Tanpa foto</span>}
      <div className={styles.imageBody}>
        <label className={styles.field} htmlFor={id}><span>{label}</span>
          <input id={id} className={styles.mono} value={value} onChange={(e) => onChange(e.target.value)} placeholder="/rawuh/foto.webp atau https://…" />
        </label>
        <div>
          <label className={styles.ghost} style={{ opacity: uploading ? 0.6 : 1 }}>
            {uploading ? "Mengunggah…" : "Unggah gambar"}
            <input type="file" accept="image/jpeg,image/png,image/webp" hidden disabled={uploading}
              onChange={(e) => { const file = e.target.files?.[0]; e.target.value = ""; if (file) void upload(file); }} />
          </label>
          {hint && <span className={styles.hint}>{hint}</span>}
        </div>
        {error && <span role="alert" className={styles.error}>{error}</span>}
      </div>
    </div>
  );
}
