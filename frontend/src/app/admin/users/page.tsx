"use client";

import { useEffect, useMemo, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { useAdminAuth } from "@/lib/useAuthToken";

type User = { id: string; name: string; email: string; role: string; created_at: string; plan_id?: string; plan_name?: string; invitations?: number };
type Plan = { id: string; name: string };

export default function AdminUsersPage() {
  const { token, ready } = useAdminAuth();
  const [users, setUsers] = useState<User[]>([]);
  const [plans, setPlans] = useState<Plan[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  useEffect(() => {
    if (!ready || !token) return;
    Promise.all([
      apiFetch("/api/admin/users", token).then((r) => r.json()),
      apiFetch("/api/admin/plans", token).then((r) => r.json()),
    ])
      .then(([u, p]: [{ items?: User[] }, { items?: Plan[] }]) => { setUsers(u.items ?? []); setPlans(p.items ?? []); })
      .catch(() => setError("Gagal memuat pengguna"))
      .finally(() => setLoading(false));
  }, [ready, token]);

  async function change(user: User, kind: "plan" | "role", value: string) {
    if (!token) return;
    if (kind === "role" && !window.confirm(value === "admin" ? `Jadikan ${user.name} admin? Admin bisa mengubah seluruh konten dan paket.` : `Cabut akses admin ${user.name}?`)) return;
    setBusy(user.id);
    setError("");
    setNotice("");
    try {
      const response = await apiFetch(`/api/admin/users/${user.id}/${kind}`, token, {
        method: "PATCH",
        body: JSON.stringify(kind === "plan" ? { plan_id: value } : { role: value }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error);
      setUsers((current) => current.map((item) => (item.id === user.id
        ? { ...item, ...(kind === "plan" ? { plan_id: value, plan_name: plans.find((p) => p.id === value)?.name } : { role: value }) }
        : item)));
      setNotice(`${user.name} diperbarui.`);
    } catch (err) {
      setError(err instanceof Error && err.message ? err.message : "Belum tersimpan.");
    } finally {
      setBusy(null);
    }
  }

  const visible = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return users.filter((user) => !needle || `${user.name} ${user.email}`.toLowerCase().includes(needle));
  }, [users, query]);

  if (!ready || !token) return null;

  return (
    <DashboardShell active="users" variant="admin">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Bisnis</p>
          <h1>Pengguna</h1>
          <p className="dashboard-subtitle">{users.length} akun terdaftar. Ubah paket untuk memberi akses manual, misalnya setelah transfer bank.</p>
        </div>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {notice && <p role="status" className={styles.ok} style={{ margin: "0 0 12px" }}>{notice}</p>}

      <label className={styles.field} style={{ maxWidth: 360, marginBottom: 16 }}>
        <span className="sr-only">Cari pengguna</span>
        <input type="search" placeholder="Cari nama atau email…" value={query} onChange={(e) => setQuery(e.target.value)} />
      </label>

      {loading ? <p className="dashboard-state">Memuat pengguna…</p> : (
        <div className="dashboard-table-wrap">
          <table className="dashboard-table" style={{ minWidth: 720 }}>
            <thead><tr><th>Pengguna</th><th>Bergabung</th><th>Undangan</th><th>Paket</th><th>Peran</th></tr></thead>
            <tbody>
              {visible.map((user) => (
                <tr key={user.id}>
                  <td><strong>{user.name}</strong><span>{user.email}</span></td>
                  <td>{new Date(user.created_at).toLocaleDateString("id-ID", { day: "numeric", month: "short", year: "numeric" })}</td>
                  <td>{user.invitations ?? 0}</td>
                  <td>
                    <select className="table-input" style={{ width: 150 }} value={user.plan_id ?? ""} disabled={busy === user.id} aria-label={`Paket ${user.name}`}
                      onChange={(e) => change(user, "plan", e.target.value)}>
                      {!user.plan_id && <option value="">—</option>}
                      {plans.map((plan) => <option key={plan.id} value={plan.id}>{plan.name}</option>)}
                    </select>
                  </td>
                  <td>
                    <select className="table-input" style={{ width: 110 }} value={user.role} disabled={busy === user.id} aria-label={`Peran ${user.name}`}
                      onChange={(e) => change(user, "role", e.target.value)}>
                      <option value="user">Pengguna</option>
                      <option value="admin">Admin</option>
                    </select>
                  </td>
                </tr>
              ))}
              {visible.length === 0 && <tr><td colSpan={5}>Tidak ada pengguna yang cocok.</td></tr>}
            </tbody>
          </table>
        </div>
      )}
    </DashboardShell>
  );
}
