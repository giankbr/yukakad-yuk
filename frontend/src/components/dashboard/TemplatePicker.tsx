"use client";

import { useEffect, useState } from "react";
import { API_URL, apiFetch } from "@/lib/api";

type Template = {
  id: string;
  name: string;
  slug: string;
  category: string;
  preview_image?: string;
  preview_url?: string;
  is_premium: boolean;
};

const categories = ["all", "modern", "editorial", "adat", "motion"];

export function TemplatePicker({
  invitationId,
  token,
  selectedTemplateId,
}: {
  invitationId: string;
  token: string;
  selectedTemplateId?: string;
}) {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [category, setCategory] = useState("all");
  const [selected, setSelected] = useState(selectedTemplateId ?? "");
  const [saving, setSaving] = useState<string | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_URL}/api/templates`)
      .then((response) => response.json())
      .then((body: { items?: Template[] }) => setTemplates(body.items ?? []))
      .catch(() => setError("Template gagal dimuat. Coba muat ulang halaman."));
  }, []);

  async function selectTemplate(templateId: string) {
    setSaving(templateId);
    setError("");
    try {
      const response = await apiFetch(`/api/invitations/${invitationId}/template`, token, {
        method: "PUT",
        body: JSON.stringify({ template_id: templateId }),
      });
      if (!response.ok) throw new Error("Template belum tersimpan. Coba lagi.");
      setSelected(templateId);
    } catch {
      setError("Template belum tersimpan. Periksa koneksi lalu coba lagi.");
    } finally {
      setSaving(null);
    }
  }

  const visible = category === "all" ? templates : templates.filter((t) => t.category === category);

  return (
    <div>
      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      <div className="form-row" style={{ gridTemplateColumns: "repeat(5, auto)", gap: ".4rem" }}>
        {categories.map((cat) => (
          <button
            key={cat}
            type="button"
            className="table-action"
            style={{ textTransform: "capitalize", fontWeight: category === cat ? 700 : 500 }}
            onClick={() => setCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </div>
      <div className="card-grid">
        {visible.map((template) => (
          <div className="dashboard-card" key={template.id}>
            {template.preview_image && (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={template.preview_image} alt={template.name} />
            )}
            <div className="dashboard-card-meta">
              <h3>{template.name}</h3>
              {template.is_premium && <span className="badge badge-premium">Premium</span>}
            </div>
            <span className="badge" style={{ width: "fit-content", textTransform: "capitalize" }}>{template.category}</span>
            {template.preview_url && <a className="table-action" href={template.preview_url} target="_blank" rel="noreferrer">Preview template ↗</a>}
            <button
              type="button"
              className="table-action"
              disabled={saving !== null}
              onClick={() => selectTemplate(template.id)}
            >
              {selected === template.id ? "Selected ✓" : saving === template.id ? "Saving..." : "Use this template"}
            </button>
          </div>
        ))}
        {visible.length === 0 && <p className="dashboard-state">No templates in this category yet.</p>}
      </div>
    </div>
  );
}
