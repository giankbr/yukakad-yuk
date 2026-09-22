# Yukakad Backend Architecture

Status: proposed

Dokumen ini menjadi batas arsitektur backend sebelum fitur baru ditambahkan.

## Tujuan

- Menjadikan PostgreSQL sebagai satu-satunya sumber data produksi.
- Memisahkan HTTP, business rules, persistence, dan integrasi eksternal.
- Menjamin setiap data undangan terisolasi berdasarkan `owner_id`.
- Menyediakan kontrak API yang stabil untuk dashboard dan halaman publik.
- Membuat media, session, rate limit, dan job async bergantung pada service yang jelas.

## Bentuk sistem

```text
Next.js dashboard/public
          |
          v
      Go HTTP API
          |
  +-------+--------+----------------+
  |                |                |
PostgreSQL       Redis          S3/MinIO
data utama       session,       media asli
                 limiter, jobs
```

Backend tetap modular monolith sampai ada kebutuhan nyata untuk memisahkan service.
Modul berjalan dalam satu binary dan memakai satu database transaction boundary.

## Aturan runtime

- `ENVIRONMENT=production` wajib memiliki `DATABASE_URL`, `REDIS_URL`, `JWT_SECRET`, dan konfigurasi object storage yang valid.
- Startup gagal dengan pesan yang jelas jika dependency wajib tidak tersedia.
- Tidak ada `MemoryStore`, memory revoker, memory limiter, atau `storage=nil` pada runtime produksi.
- Fake repository hanya dipakai oleh unit test.
- Seed data berjalan melalui migration/command eksplisit, bukan saat setiap boot aplikasi.
- HTTP server memakai `http.Server` dengan read timeout, write timeout, idle timeout, dan graceful shutdown.

## Modul kode

```text
backend/
  cmd/api/                 composition root, startup, shutdown
  internal/platform/       config, logger, postgres, redis, object storage
  internal/http/            router, middleware, request/response helpers
  internal/auth/            password, session, token, authorization
  internal/users/           profile and account use cases
  internal/invitations/     invitation lifecycle and ownership
  internal/content/         couple, events, stories, gallery, settings
  internal/guests/          guest CRUD, import, broadcast records, check-in
  internal/rsvp/            public RSVP and dashboard summaries
  internal/wishes/          public wishes and moderation
  internal/gifts/           gift methods and transaction webhooks
  internal/templates/       template catalog and plan gating
  internal/media/           upload policy and object storage records
  internal/billing/         plans, entitlements, subscription boundary
  internal/admin/           CMS and platform administration
  internal/audit/           security and product audit events
  migrations/               ordered SQL migrations
```

Setiap modul memiliki bentuk yang sama:

```text
module/
  handler.go       HTTP adapter
  service.go       use cases and business rules
  repository.go    persistence interface
  postgres.go      PostgreSQL implementation
  model.go         domain/request/response types
  service_test.go  unit tests
```

Handler tidak boleh menjalankan query langsung dan service tidak boleh membaca `http.Request`.

## Ownership dan authorization

Semua operasi dashboard memakai pola:

1. Parse dan validasi ID dari request.
2. Ambil resource dengan `owner_id = actor.UserID` dalam query yang sama.
3. Kembalikan `404` untuk resource yang tidak dimiliki agar tidak membocorkan keberadaan ID.
4. Jalankan perubahan dalam transaction bila menyentuh lebih dari satu tabel.
5. Catat aksi penting ke `audit_events`.

Admin memiliki policy terpisah. Role dari token tidak cukup sebagai sumber kebenaran; service mengambil user aktif dari database untuk operasi sensitif.

## Auth dan session

Gunakan opaque session token yang disimpan sebagai hash di Redis atau tabel session:

- access session 24 jam untuk MVP;
- refresh/revoke dilakukan dengan menghapus session;
- password reset token single-use dengan expiry;
- response login tidak pernah mengembalikan password atau secret;
- endpoint login, reset password, dan public RSVP memiliki rate limit khusus;
- cookie production memakai `HttpOnly`, `Secure`, dan `SameSite=Lax` jika frontend/API satu site.

Token HMAC custom yang sekarang dipakai dipensiunkan setelah session endpoint baru aktif.

## Model data inti

### Identity dan billing

- `users`
- `sessions`
- `password_reset_tokens`
- `plans`
- `subscriptions`
- `user_entitlements`

### Invitation aggregate

- `invitations`: owner, slug, status, template, published timestamps
- `invitation_settings`: theme, colors, fonts, opening/closing, section order
- `couples`: profile pasangan
- `invitation_events`: semua acara, termasuk akad dan resepsi
- `stories`
- `galleries`
- `media`

### Guest engagement

- `guests`: data tamu dan token publik yang di-hash
- `rsvps`: satu response aktif per guest/invitation
- `wishes`: message dan moderation status
- `guest_checkins`: histori check-in, bukan hanya timestamp terakhir
- `broadcast_logs`: status link generated/opened/confirmed/failed

### Commerce dan platform

- `gifts`: metode rekening/e-wallet/QRIS yang ditampilkan publik
- `gift_transactions`: webhook/payment state machine
- `templates`: metadata dan JSON config tervalidasi
- `audit_events`
- `site_content`, `features`, `testimonials`

## API contract

Prefix versi: `/api/v1`.

```text
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/forgot-password
POST   /api/v1/auth/reset-password
GET    /api/v1/me

GET    /api/v1/invitations
POST   /api/v1/invitations
GET    /api/v1/invitations/{id}
PATCH  /api/v1/invitations/{id}
DELETE /api/v1/invitations/{id}
POST   /api/v1/invitations/{id}/publish
POST   /api/v1/invitations/{id}/duplicate

GET/PATCH  /api/v1/invitations/{id}/settings
GET/POST   /api/v1/invitations/{id}/couple
GET/POST   /api/v1/invitations/{id}/events
PATCH/DELETE /api/v1/invitations/{id}/events/{eventId}
GET/POST   /api/v1/invitations/{id}/stories
GET/POST   /api/v1/invitations/{id}/gallery
GET/PUT    /api/v1/invitations/{id}/template

GET/POST/PATCH/DELETE /api/v1/invitations/{id}/guests
POST   /api/v1/invitations/{id}/guests/import
POST   /api/v1/invitations/{id}/guests/{guestId}/check-in
GET    /api/v1/invitations/{id}/rsvps
GET    /api/v1/invitations/{id}/rsvps/summary
GET/PATCH /api/v1/invitations/{id}/wishes
GET/POST/PATCH/DELETE /api/v1/invitations/{id}/gifts
POST   /api/v1/invitations/{id}/media

GET    /api/v1/public/invitations/{slug}
POST   /api/v1/public/invitations/{slug}/rsvp
GET/POST /api/v1/public/invitations/{slug}/wishes
GET    /api/v1/public/invitations/{slug}/gifts
```

Semua response memakai bentuk konsisten:

```json
{"data": {}, "meta": {"request_id": "..."}}
```

Error:

```json
{"error": {"code": "validation_error", "message": "...", "fields": {}}}
```

List endpoint wajib memiliki `page`, `page_size`, dan `total` atau cursor yang terdokumentasi.

## Migration policy

- Satu file migration per perubahan schema.
- Tabel `schema_migrations` menyimpan version dan checksum.
- Migration dijalankan sekali sebelum server menerima traffic.
- Tidak ada perubahan schema tersembunyi di `Seed*` atau constructor store.
- Model event lama 1:1 dimigrasikan penuh ke `invitation_events`, lalu endpoint lama dipertahankan hanya selama masa kompatibilitas.
- Semua foreign key, unique constraint, check constraint, dan index ditulis di SQL.

## Urutan implementasi

1. Runtime strict: config validation, dependency checks, graceful shutdown, migration tracking.
2. HTTP foundation: `/api/v1`, error envelope, request ID, typed validation, pagination.
3. Auth/session dan user profile.
4. Invitation aggregate dan ownership policy.
5. Content editor: settings, couple, events, stories, gallery, template.
6. Guests, RSVP, wishes, check-in, broadcast records.
7. Media upload lifecycle dan object storage.
8. Gifts dan payment boundary.
9. Plans/entitlements dan admin CMS.
10. Remove legacy routes, memory runtime, and frontend content fallback.

## Keputusan yang sengaja ditunda

- Microservices.
- Full event sourcing.
- WhatsApp provider otomatis sebelum billing dan consent flow jelas.
- Payment gateway vendor tertentu sebelum kebutuhan bisnis dipilih.

