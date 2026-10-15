"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { API_URL, apiFetch } from "@/lib/api";
import { ThemeButton, ThemeGrid, type DashboardTemplate } from "./ThemeGrid";

export function TemplatePicker({
  invitationId,
  token,
  selectedTemplateId,
  onChange,
}: {
  invitationId: string;
  token: string;
  selectedTemplateId?: string;
  onChange?: (templateId: string) => void;
}) {
  const [templates, setTemplates] = useState<DashboardTemplate[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(selectedTemplateId ?? "");
  const [saving, setSaving] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [premiumBlocked, setPremiumBlocked] = useState("");

  useEffect(() => {
    fetch(`${API_URL}/api/templates`)
      .then((response) => response.json())
      .then((body: { items?: DashboardTemplate[] }) => setTemplates(body.items ?? []))
      .catch(() => setError("Tema gagal dimuat. Coba muat ulang halaman."))
      .finally(() => setLoading(false));
  }, []);

  async function selectTemplate(template: DashboardTemplate) {
    setSaving(template.id);
    setError("");
    setPremiumBlocked("");
    try {
      const response = await apiFetch(`/api/invitations/${invitationId}/template`, token, {
        method: "PUT",
        body: JSON.stringify({ template_id: template.id }),
      });
      if (response.status === 403) {
        setPremiumBlocked(template.name);
        return;
      }
      if (!response.ok) throw new Error();
      setSelected(template.id);
      onChange?.(template.id);
    } catch {
      setError("Tema belum tersimpan. Periksa koneksi lalu coba lagi.");
    } finally {
      setSaving(null);
    }
  }

  if (loading) return <p className="dashboard-state">Memuat tema...</p>;

  return (
    <div>
      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {premiumBlocked && (
        <p role="alert" className="dashboard-state dashboard-state-error">
          {premiumBlocked} adalah tema Premium. <Link href="/harga">Upgrade paket</Link> untuk memakainya.
        </p>
      )}
      <ThemeGrid
        templates={templates}
        selectedId={selected}
        action={(template, isSelected) => (
          <ThemeButton disabled={saving !== null || isSelected} onClick={() => selectTemplate(template)}>
            {isSelected ? "Sedang dipakai" : saving === template.id ? "Menyimpan..." : "Pakai tema"}
          </ThemeButton>
        )}
      />
    </div>
  );
}
