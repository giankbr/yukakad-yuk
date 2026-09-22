# Yukakad Rebuild Plan

## 1. Overview
Yukakad adalah platform digital invitation builder untuk acara seperti pernikahan, ulang tahun, dan acara pribadi lainnya. Produk ini harus memisahkan pengalaman publik undangan dengan panel dashboard user dan admin.

Tujuan rebuild:
- Jangan copy-paste arsitektur legacy.
- Gunakan legacy repo sebagai reference fitur dan perilaku.
- Bangun platform yang modern, maintainable, scalable, dan mobile-first.
- Siapkan fondasi SaaS untuk banyak user, banyak undangan, banyak template, dan fitur premium di masa depan.

## 2. Product Goals
### Public invitation experience
- halaman undangan yang cepat dan responsif
- tema/customization yang rapi
- RSVP, ucapan, gift, gallery, location, countdown

### Dashboard user
- daftar undangan
- membuat dan mengelola undangan
- mengedit konten undangan
- mengelola tamu dan RSVP
- memilih template
- publish/unpublish
- preview mobile dan desktop

### Platform direction
- multi-user
- multi-invitation per user
- template-driven rendering
- paid tier / plan di masa depan

## 3. Recommended Stack
### Frontend
- Next.js
- TypeScript
- Tailwind CSS

### Backend
- Go
- REST API
- PostgreSQL
- Redis
- object storage (S3-compatible)

### Infra
- Docker Compose
- Nginx
- HTTPS
- CI/CD via GitHub Actions

## 4. Phase-Based Roadmap

### Phase 0 — Legacy Audit
Tujuan:
- pahami fitur lama
- melihat route, controller, model, view, database, auth, upload, dan flow public/admin

Output:
- feature inventory
- route inventory
- database entity inventory
- user flow
- admin flow
- public invitation flow
- preserve vs redesign list

### Phase 1 — Product Requirements
Buat PRD singkat untuk MVP.

MVP meliputi:
- register, login, logout
- dashboard user
- create invitation
- template selection
- couple info
- event info
- gallery
- RSVP
- wishes
- gift section
- preview dan publish

### Phase 2 — Architecture
Arsitektur utama:
- frontend app untuk dashboard dan public invitation
- backend API terpisah
- database PostgreSQL
- redis untuk cache, queue, atau session
- object storage untuk media

### Phase 3 — Database Design
Entitas utama:
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

Prinsip:
- foreign key yang jelas
- index pada query penting
- constraint unik pada slug dan identitas utama
- created_at dan updated_at di semua tabel utama

### Phase 4 — Backend Foundation
Bangun fondasi server:
- config
- migration runner
- HTTP server
- error handling
- logging
- validation
- auth foundation
- health check

### Phase 5 — Authentication & User Management
- register
- login
- logout
- forgot/reset password
- profile
- avatar

### Phase 6 — Invitation CRUD
- create invitation
- update invitation
- draft/publish
- duplicate/delete
- preview
- slug management

### Phase 7 — Public Invitation Engine
Route utama:
- /invitation/[slug]

Section publik:
- Cover
- Opening
- Couple
- Story
- Event
- Countdown
- Gallery
- RSVP
- Wishes
- Gift
- Location
- Closing

### Phase 8 — Template System
- reusable sections
- data-driven template config
- category template (modern, adat, editorial, motion)
- premium gating sesuai plan

### Phase 9 — Dashboard / Admin UX
Page utama:
- dashboard
- invitations list
- invitation create/edit
- guests
- RSVP
- wishes
- gift
- settings
- preview

### Phase 10 — Guest Management & RSVP
- add/edit/delete guest
- CSV import
- search/filter
- RSVP status
- attendance summary

### Phase 11 — Wishes, Gift, WA Share, QR Check-in
- wishes moderation
- gift methods (bank, QRIS, e-wallet)
- WA personal link
- batch sending tracking
- QR check-in (post-MVP atau early post-MVP)

### Phase 12 — Performance
- image optimization
- lazy loading
- caching
- CDN
- responsive image sizing
- font optimization

### Phase 13 — Security
- auth/authorization
- IDOR prevention
- upload validation
- rate limiting
- secure guest tokens
- SQL/XSS/CSRF checks

### Phase 14 — Observability
- structured logs
- request ID
- latency monitoring
- error tracking
- analytics dasar

### Phase 15 — Deployment
- Docker Compose untuk dev
- Nginx + HTTPS untuk prod
- PostgreSQL + Redis + object storage
- CI/CD pipeline

### Phase 16 — Testing
- backend API tests
- frontend component tests
- E2E critical flow tests

## 5. MVP Definition
MVP harus bisa:
1. register
2. login
3. create invitation
4. pilih template
5. isi couple info dan event info
6. upload gallery
7. konfigurasi gift/amplop digital
8. preview invitation
9. publish invitation
10. bagikan URL
11. add guest
12. kirim link per tamu via WhatsApp
13. terima RSVP
14. terima wishes
15. lihat dashboard RSVP

## 6. Post-MVP
- custom domain
- plan subscription
- payment gateway untuk amplop digital
- WhatsApp broadcast automation
- QR check-in
- invitation analytics
- advanced template motion

## 7. Engineering Principles
1. Build the product, not the legacy code.
2. Preserve behavior only where users depend on it.
3. Avoid premature microservices.
4. Keep invitation rendering fast.
5. Keep templates reusable.
6. Keep user data isolated.
7. Treat media as object storage, not database blobs.
8. Every feature must have a clear owner/user flow.
9. Every database change must include a migration.
10. Every important bug must get a regression test.

## 8. Recommended Execution Order
1. Legacy audit
2. Product requirements
3. Architecture
4. Database
5. Backend foundation
6. Auth
7. Invitation CRUD
8. Public invitation
9. Template engine
10. Dashboard
11. Media
12. Guest management
13. RSVP
14. Wishes
15. Gift
16. Publishing
17. Security
18. Performance
19. Testing
20. Deployment

## 9. Definition of Done
A feature is considered done when:
- backend implemented
- database migration added
- validation included
- authorization included
- error handling included
- frontend implemented
- loading state included
- empty/error states included
- mobile responsive
- tests added
- security reviewed
- performance reviewed
- documentation updated

## 10. Outcome
Dengan plan ini, project Yukakad dapat dibangun secara incremental, dengan fokus pada produk nyata, bukan sekadar porting source lama. Legacy repo hanya berfungsi sebagai referensi perilaku, sedangkan implementasi baru dibangun dengan arsitektur yang lebih modern dan siap untuk scale.
