# Yukakad Development Phases

## Phase 0 — Audit Legacy
### Goal
Mengevaluasi repo lama untuk memahami fitur yang sudah ada dan mana yang harus dipertahankan, dibenahi, atau dibuang.

### Fokus
- route analysis
- controller and model review
- database relationships
- public invitation behavior
- dashboard and admin flows
- auth/session behavior
- upload and media handling
- guest management, RSVP, wishes, gallery

### Output
- feature inventory
- route inventory
- database inventory
- user flow
- admin flow
- public invitation flow
- technical debt list
- security concerns

---

## Phase 1 — Product Requirements
### Goal
Menentukan kebutuhan MVP dan area yang masuk scope rebuild.

### Scope utama
- auth
- dashboard user
- invitation CRUD
- invitation editor
- template selection
- guest management
- RSVP
- wishes
- gift section

### Outcome
- PRD MVP
- backlog post-MVP
- fitur yang dipertahankan dan didesain ulang

---

## Phase 2 — Architecture
### Goal
Memilih stack dan bentuk arsitektur yang tepat.

### Rekomendasi
- Next.js + TypeScript + Tailwind
- Go API
- PostgreSQL
- Redis
- object storage
- Docker Compose

### Outcome
- diagram arsitektur
- modul utama
- separation of concerns

---

## Phase 3 — Database Design
### Goal
Merancang schema yang kuat dan siap berkembang.

### Entitas utama
- users
- plans
- invitations
- invitation_settings
- couples
- events
- stories
- galleries
- guests
- rsvps
- wishes
- gifts
- templates
- media

### Outcome
- ERD
- migrations
- index + constraints

---

## Phase 4 — Backend Foundation
### Goal
Membuat fondasi server yang siap untuk fitur produk.

### Include
- config env
- migration system
- HTTP server
- logging
- validation
- request IDs
- auth foundation
- health checks

---

## Phase 5 — Auth & User
### Goal
Menyediakan autentikasi dan profil pengguna dasar.

### Features
- register
- login
- logout
- forgot/reset password
- profile
- avatar

---

## Phase 6 — Invitation CRUD
### Goal
Membuat undangan dari user sampai bisa preview dan publish.

### Features
- create invitation
- list invitation
- edit content
- publish/unpublish
- preview
- slug

---

## Phase 7 — Public Invitation Engine
### Goal
Menyiapkan halaman publik undangan yang cepat dan reusable.

### Sections
- cover
- opening
- couple
- story
- event
- countdown
- gallery
- RSVP
- wishes
- gift
- location
- closing

---

## Phase 8 — Template System
### Goal
Membuat sistem template yang data-driven dan reusable.

### Fokus
- varians section
- theme config
- kategori template
- premium gating

---

## Phase 9 — Dashboard UX
### Goal
Membuat panel operasional untuk manajemen undangan.

### Pages
- dashboard
- invitations list
- create/edit invitation
- couple info
- events
- gallery
- guests
- RSVP
- wishes
- gift
- settings
- preview

---

## Phase 10 — Guest + RSVP
### Goal
Menyediakan guest management dan response flow.

### Features
- add/edit/delete guest
- search/filter
- CSV import
- RSVP status
- attendance summary

---

## Phase 11 — Wishes, Gift, WhatsApp, Check-in
### Goal
Menyempurnakan fitur standar pasar di undangan digital.

### Scope
- wishes moderation
- gift methods
- WA share link
- broadcast logs
- QR check-in

---

## Phase 12 — Performance
### Goal
Membuat halaman publik cepat di perangkat mobile.

### Langkah utama
- responsive images
- lazy loading
- font optimization
- caching
- CDN
- minimize JS

---

## Phase 13 — Security
### Goal
Hardening produk sebelum scale.

### Fokus
- auth validation
- authorization
- IDOR prevention
- upload security
- guest token
- rate limiting
- CSRF/XSS protection

---

## Phase 14 — Observability
### Goal
Memudahkan debugging dan monitoring di production.

### Features
- request ID
- structured logs
- error tracking
- latency monitoring
- basic analytics

---

## Phase 15 — Deployment
### Goal
Menyediakan jalur deploy yang repeatable.

### Infrastruktur
- Docker Compose local
- services: frontend, backend, postgres, redis
- production nginx + HTTPS
- object storage
- CI/CD pipeline

---

## Phase 16 — Testing
### Goal
Memastikan fitur yang dibangun benar-benar bekerja.

### Test area
- API tests
- frontend tests
- critical E2E flow

---

## Phase 17 — Sprint Execution
### Sprint 1
- repo setup
- docker
- database
- auth
- API foundation

### Sprint 2
- invitation CRUD
- couple and event
- public invitation base

### Sprint 3
- template system
- gallery
- music
- countdown

### Sprint 4
- guest management
- RSVP
- wishes

### Sprint 5
- gift
- preview
- publish flow

### Sprint 6
- performance and security
- tests

### Sprint 7
- deploy
- monitoring
- docs
