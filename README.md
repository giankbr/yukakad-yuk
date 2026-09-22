# Yukakad

Platform undangan digital dengan backend Go dan frontend Next.js.
Branch `dev` berisi stack baru; aplikasi CodeIgniter tetap tersedia di branch `main`.

## Struktur

- `backend/` — REST API Go dan migrasi PostgreSQL.
- `frontend/` — Next.js, React, TypeScript, dan Tailwind CSS.
- `docs/` — arsitektur, rencana pengembangan, dan spesifikasi OpenAPI.
- `docker-compose.yml` — lingkungan development dengan PostgreSQL, Redis, dan MinIO.

## Menjalankan development

Dengan Docker dan Docker Compose terpasang:

```sh
docker compose up
```

Frontend tersedia di `http://localhost:3000`, API di `http://localhost:8080`,
dan konsol MinIO di `http://localhost:9011`. Port tersebut harus tersedia.
Konfigurasi dan kredensial bawaan Compose hanya untuk development lokal.

## Pemeriksaan kode

Backend (Go 1.25.3 atau lebih baru):

```sh
cd backend
go test ./...
```

Frontend:

```sh
cd frontend
npm ci
npm run lint
npm run build
```

Lihat [dokumentasi proyek](docs/README.md) dan
[arsitektur backend](docs/BACKEND_ARCHITECTURE.md) untuk detail.
