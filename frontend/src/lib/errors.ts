/**
 * Indonesian copy for the backend's English error messages. Many backend errors are already
 * Indonesian; those (and anything unknown) are passed through, with the first letter capitalised.
 */
const MESSAGES: Record<string, string> = {
  "invalid credentials": "Email atau kata sandi salah.",
  "email already exists": "Email ini sudah terdaftar. Coba masuk atau pakai email lain.",
  "name, email, and password are required": "Nama, email, dan kata sandi wajib diisi.",
  "email is required": "Email wajib diisi.",
  "invalid payload": "Data yang dikirim tidak valid. Coba lagi.",
  "password is too long": "Kata sandi terlalu panjang.",
  "authentication service unavailable": "Layanan masuk sedang bermasalah. Coba lagi sebentar lagi.",
  "invalid token": "Sesi kamu sudah berakhir. Silakan masuk lagi.",
  "missing authorization token": "Kamu perlu masuk dulu.",
  "admin access required": "Halaman ini khusus admin.",
  "forbidden": "Kamu tidak punya akses untuk melakukan ini.",
  "user not found": "Akun tidak ditemukan.",
  "invalid or expired reset token": "Link reset sudah tidak berlaku atau kedaluwarsa. Minta link baru.",
  "valid token and password of at least 8 characters are required": "Kata sandi baru minimal 8 karakter.",
  "token is required": "Link reset tidak lengkap. Buka lagi link dari email.",
  "password reset delivery is not configured": "Reset lewat email belum aktif. Hubungi admin Rawuh lewat WhatsApp.",
  "password reset service unavailable": "Layanan reset kata sandi sedang bermasalah. Coba lagi nanti.",
  "password reset delivery failed": "Email reset belum terkirim. Coba lagi sebentar lagi.",
  "rate limit exceeded, please try again later": "Terlalu banyak percobaan. Tunggu sebentar lalu coba lagi.",
  "rate limit service unavailable": "Layanan sedang sibuk. Coba lagi sebentar lagi.",
  "guest limit reached for your plan": "Kuota tamu di paketmu sudah penuh. Upgrade paket untuk menambah tamu.",
  "media storage is not configured": "Penyimpanan foto belum aktif. Hubungi admin Rawuh.",
  "object storage is not configured": "Penyimpanan foto belum aktif. Hubungi admin Rawuh.",
  "slug already exists": "Alamat URL ini sudah dipakai. Coba alamat lain.",
  "slug and title are required": "Nama acara dan alamat URL wajib diisi.",
  "invitation not found": "Undangan tidak ditemukan.",
  "template not found": "Tema tidak ditemukan.",
  "plan not found": "Paket tidak ditemukan.",
  "file too large": "Ukuran file terlalu besar.",
  "file too large (max 10mb)": "Ukuran file maksimal 10 MB.",
  "image must be jpeg, png, or webp": "Gunakan foto JPG, PNG, atau WebP.",
  "invalid csv": "File CSV tidak bisa dibaca. Periksa formatnya.",
  "method not allowed": "Permintaan tidak didukung.",
  "failed to fetch": "Tidak bisa terhubung ke server. Periksa koneksi internetmu.",
  "load failed": "Tidak bisa terhubung ke server. Periksa koneksi internetmu.",
  "networkerror when attempting to fetch resource.": "Tidak bisa terhubung ke server. Periksa koneksi internetmu.",
};

/** Maps a backend/network error message to friendly Indonesian copy. */
export function friendlyError(message: string | null | undefined, fallback = "Terjadi kesalahan. Coba lagi."): string {
  const text = (message ?? "").trim();
  if (!text) return fallback;
  const known = MESSAGES[text.toLowerCase()];
  if (known) return known;
  return text.charAt(0).toUpperCase() + text.slice(1);
}

/** Reads `{error}` from a failed response (tolerating non-JSON bodies) and maps it. */
export async function responseError(response: Response, fallback?: string): Promise<string> {
  const body = (await response.json().catch(() => null)) as { error?: string } | null;
  return friendlyError(body?.error, fallback);
}
