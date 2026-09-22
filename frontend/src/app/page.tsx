import Link from "next/link";
import density from "./landing-density.module.css";

const API_BASE = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

type Hero = { heading?: string; subheading?: string; cta_label?: string; cta_href?: string };
type Kontak = { heading?: string; subheading?: string; whatsapp?: string };
type Footer = { heading?: string; copyright?: string; instagram?: string };
type Feature = { id: string; title: string; description: string; icon?: string };
type Testimonial = { id: string; name: string; role?: string; quote: string; avatar_url?: string };
type Template = { id: string; name: string; slug: string; category: string; preview_image?: string; is_premium: boolean };
type Plan = { id: string; name: string; max_guests: number; has_watermark: boolean; custom_domain_allowed: boolean; payment_gateway_allowed: boolean; price: number };

const defaultFeatures: Feature[] = [
  { id: "design", title: "Desain yang terasa kamu", description: "Pilih template yang sudah dirancang dengan detail, lalu ubah warna, foto, dan cerita kalian.", icon: "✦" },
  { id: "guest", title: "Tamu lebih teratur", description: "Kelola daftar tamu, RSVP, ucapan, dan check-in dari satu workspace yang rapi.", icon: "↗" },
  { id: "share", title: "Siap dibagikan", description: "Dapatkan link undangan yang mudah dikirim lewat WhatsApp, Instagram, atau email.", icon: "⌁" },
];

const defaultTemplates: Template[] = [
  { id: "seraya", name: "Seraya", slug: "seraya", category: "Editorial", is_premium: false },
  { id: "aksara", name: "Aksara", slug: "aksara", category: "Adat", is_premium: true },
  { id: "senja", name: "Senja", slug: "senja", category: "Modern", is_premium: false },
];

const defaultPlans: Plan[] = [
  { id: "free", name: "Mulai", max_guests: 100, has_watermark: true, custom_domain_allowed: false, payment_gateway_allowed: false, price: 0 },
  { id: "pro", name: "Rayakan", max_guests: 1000, has_watermark: false, custom_domain_allowed: true, payment_gateway_allowed: true, price: 149000 },
];

async function getJSON<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(`${API_BASE}${path}`, { next: { revalidate: 60 } });
    if (!response.ok) return fallback;
    return response.json();
  } catch {
    return fallback;
  }
}

function formatIDR(amount: number) {
  if (amount <= 0) return "Gratis";
  return new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", maximumFractionDigits: 0 }).format(amount);
}

export default async function Home() {
  const [hero, kontak, footer, featuresResult, testimonialsResult, templatesResult, plansResult] = await Promise.all([
    getJSON<Hero>("/api/public/site-content/hero", {}),
    getJSON<Kontak>("/api/public/site-content/kontak", {}),
    getJSON<Footer>("/api/public/site-content/footer", {}),
    getJSON<{ items?: Feature[] }>("/api/public/features", {}),
    getJSON<{ items?: Testimonial[] }>("/api/public/testimonials", {}),
    getJSON<{ items?: Template[] }>("/api/templates", {}),
    getJSON<{ items?: Plan[] }>("/api/public/plans", {}),
  ]);

  const features = featuresResult.items?.length ? featuresResult.items : defaultFeatures;
  const testimonials = testimonialsResult.items ?? [];
  const templates = templatesResult.items?.length ? templatesResult.items : defaultTemplates;
  const plans = (plansResult.items?.length ? plansResult.items : defaultPlans).slice().sort((a, b) => a.price - b.price);
  const waLink = kontak.whatsapp ? `https://wa.me/${kontak.whatsapp.replace(/[^0-9]/g, "")}` : undefined;

  return (
    <main className={`landing-page ${density.compact}`}>
      <div className="landing-announcement"><span>Yukakad Studio</span><a href="#fitur">Undangan digital yang siap dibagikan <b>↗</b></a></div>
      <nav className="landing-nav">
        <Link href="/" className="landing-logo"><span className="landing-logo-mark">y</span> yukakad<span>.</span></Link>
        <div className="landing-nav-links">
          <a href="#fitur">Produk</a>
          <a href="#template">Template</a>
          <a href="#harga">Harga</a>
          {testimonials.length > 0 && <a href="#testimoni">Testimoni</a>}
        </div>
        <div className="landing-nav-actions">
          <a href="/auth/login">Masuk</a>
          <a href="/auth/register" className="landing-cta-button">
            Mulai gratis <span>→</span>
          </a>
        </div>
      </nav>

      <section className="landing-agent-hero">
        <div className="landing-agent-frame">
          <div className="landing-launch-note"><span /> Baru untuk perayaan yang lebih rapi</div>
          <div className="landing-agent-copy">
            <div className="landing-kicker"><span className="landing-kicker-dot" /> Undangan digital untuk hari yang berarti</div>
            <h1>{hero.heading ?? "Hari besar kalian, dibuat lebih sederhana."}</h1>
            <p>{hero.subheading ?? "Buat undangan pernikahan yang hangat, cantik, dan mudah dikelola. Dari cerita pertama sampai tamu terakhir pulang."}</p>
            <div className="landing-hero-actions">
              <a href={hero.cta_href ?? "/auth/register"} className="landing-cta-button">
                {hero.cta_label ?? "Buat undangan gratis"} <span>→</span>
              </a>
              <Link href="/invitation/demo" className="landing-secondary-button">
                Lihat contoh undangan
              </Link>
            </div>
            <div className="landing-hero-trust" aria-label="Keunggulan Yukakad">
              <span><b>01</b> link siap kirim</span>
              <span><b>02</b> RSVP real-time</span>
            </div>
          </div>
          <div className="landing-agent-visual">
            <div className="landing-hero-rsvp">
              <div className="hero-rsvp-top"><span>RSVP</span><span className="hero-rsvp-live">● live</span></div>
              <div className="hero-rsvp-row"><span className="hero-rsvp-dot ok" /> Hadir</div>
              <div className="hero-rsvp-row"><span className="hero-rsvp-dot no" /> Tidak hadir</div>
              <div className="hero-rsvp-row"><span className="hero-rsvp-dot maybe" /> Masih ragu</div>
              <div className="hero-rsvp-bar"><i /></div>
            </div>
            <div className="landing-agent-demo">
              <div className="preview-card-top"><span>yukakad.com</span><span className="preview-live">● live</span></div>
              <div className="preview-photo" />
              <div className="preview-card-copy"><span className="landing-hero-preview-kicker">The wedding of</span><h2>Alya <i>&amp;</i> Rizky</h2><p>Sabtu, 12 Oktober 2025</p><div className="preview-card-line" /><span className="preview-card-link">Buka undangan <b>↗</b></span></div>
            </div>
            <div className="landing-preview-badge">
              <span className="landing-preview-badge-icon">↗</span>
              <span><b>274</b> tamu sudah membuka</span>
            </div>
          </div>
        </div>
      </section>

      <section className="landing-agent-logos">
        <span>Undangan yang terasa personal, tanpa pekerjaan tambahan.</span>
        <div><b>1.200+</b> pasangan sudah merayakan bersama Yukakad</div>
        <span className="proof-stars">★★★★★</span>
      </section>

      <section className="landing-momentum" aria-label="Ringkasan manfaat Yukakad">
        <div><span>Template yang kamu suka</span><strong>01 pilihan awal</strong></div>
        <div><span>Waktu menyiapkan undangan</span><strong>beberapa menit</strong></div>
        <div><span>Konfirmasi tamu</span><strong>langsung terpantau</strong></div>
      </section>

      <section className="landing-compatibility" aria-label="Kanal berbagi undangan">
        <p>Undangan siap dibagikan ke mana pun tamu kalian berada.</p>
        <div><span>WhatsApp</span><span>Instagram</span><span>Email</span><span>QR code</span><span>+ lainnya</span></div>
      </section>

      <section className="landing-problem" id="produk">
        <div className="landing-problem-heading"><p className="landing-section-kicker">Sebelum hari H</p><h2>Jangan biarkan detail kecil mengambil alih momen besar.</h2><p>Yukakad menyatukan undangan, daftar tamu, dan konfirmasi ke dalam satu alur yang tenang.</p></div>
        <div className="landing-problem-grid">
          <article className="landing-problem-card problem-card-invite"><div className="problem-window"><span>yukakad.com</span><b>Undangan sudah siap</b><small>tinggal kirim ke tamu</small></div><h3>Undangan tidak lagi tercecer.</h3><p>Satu link yang rapi untuk setiap cerita, detail acara, dan arah lokasi.</p></article>
          <article className="landing-problem-card problem-card-rsvp"><div className="problem-rsvp"><span>Konfirmasi hadir</span><strong>86<span>%</span></strong><div><i /><i /><i /></div></div><h3>Jawaban tamu lebih jelas.</h3><p>Pantau RSVP tanpa mengumpulkan balasan dari banyak chat dan spreadsheet.</p></article>
          <article className="landing-problem-card problem-card-checkin"><div className="problem-ticket"><span>CHECK-IN</span><b>Alya &amp; Rizky</b><small>12.10.2025 · 10.00 WIB</small><em>✓</em></div><h3>Hari acara terasa lebih ringan.</h3><p>Gunakan QR check-in untuk menyambut tamu tanpa antrean dan catatan manual.</p></article>
        </div>
      </section>

      {features.length > 0 && (
        <section className="landing-system" id="fitur">
          <div className="landing-system-heading"><p className="landing-section-kicker">Satu sistem, satu cerita</p><h2>Semua yang dibutuhkan untuk menyambut tamu.</h2><p>Mulai dari memilih desain sampai melihat siapa yang hadir, tanpa alur yang berbelit.</p></div>
          <div className="landing-system-grid">
            {features.map((feature) => (
              <article className="landing-system-card" key={feature.id}>
                <div className="system-card-stage"><span>{feature.icon ?? "✦"}</span><i /></div>
                <div><small>0{features.indexOf(feature) + 1}</small><h3>{feature.title}</h3><p>{feature.description}</p></div>
              </article>
            ))}
          </div>
        </section>
      )}

      <section className="landing-steps" aria-label="Cara kerja Yukakad">
        <div><span className="step-number">01</span><strong>5 menit</strong><p>Waktu untuk memulai undangan pertama kalian.</p><h3>Setup yang singkat</h3></div>
        <div><span className="step-number">02</span><strong>1 link</strong><p>Satu tautan untuk cerita, acara, galeri, dan RSVP.</p><h3>Semua lebih terarah</h3></div>
        <div><span className="step-number">03</span><strong>100%</strong><p>Detail penting tetap bisa kalian ubah kapan saja.</p><h3>Kontrol tetap di tangan</h3></div>
      </section>

      {templates.length > 0 && (
        <section className="landing-showcase" id="template">
          <div className="landing-showcase-heading"><p className="landing-section-kicker">Ruang yang terasa milik kalian</p><h2>Setiap cerita punya cara sendiri untuk dibuka.</h2><p>Temukan titik awal yang pas, lalu bentuk menjadi undangan yang sepenuhnya kalian.</p></div>
          <div className="landing-template-grid">
            {templates.map((template) => (
              <div className="landing-template-card" key={template.id}>
                <div className="landing-template-preview" style={template.preview_image ? { backgroundImage: `url(${template.preview_image})` } : undefined} />
                <div className="landing-template-meta">
                  <div>
                    <h3>{template.name}</h3>
                    <span>{template.category}</span>
                  </div>
                  {template.is_premium && <span className="badge badge-premium">Premium</span>}
                </div>
                <a href="/auth/register" className="landing-secondary-button">
                  Pakai template ini
                </a>
              </div>
            ))}
          </div>
        </section>
      )}

      {plans.length > 0 && (
        <section className="landing-pricing" id="harga">
          <div className="landing-pricing-heading"><p className="landing-section-kicker">Harga yang jelas</p><h2>Mulai dengan yang dibutuhkan hari ini.</h2><p>Buat undangan pertama secara gratis. Tambahkan ruang saat acara kalian membutuhkannya.</p></div>
          <div className="landing-pricing-grid">
            {plans.map((plan, index) => (
              <div className={`landing-plan-card${index === 1 ? " featured" : ""}`} key={plan.id}>
                <h3>{plan.name}</h3>
                <div className="landing-plan-price">{formatIDR(plan.price)}</div>
                <ul>
                  <li>Sampai {plan.max_guests} tamu</li>
                  <li>{plan.has_watermark ? "Dengan watermark" : "Tanpa watermark"}</li>
                  {plan.custom_domain_allowed && <li>Custom domain</li>}
                  {plan.payment_gateway_allowed && <li>Payment gateway amplop digital</li>}
                </ul>
                <a href="/auth/register" className="landing-cta-button">
                  Mulai dengan {plan.name} <span>→</span>
                </a>
              </div>
            ))}
          </div>
        </section>
      )}

      {testimonials.length > 0 && (
        <section className="landing-voices" id="testimoni">
          <div><p className="landing-section-kicker">Cerita dari pasangan</p><h2>Momen besar, dengan persiapan yang lebih ringan.</h2></div>
          <div className="landing-testimonial-grid">
            {testimonials.map((testimonial) => (
              <div className="landing-testimonial-card" key={testimonial.id}>
                <p>&ldquo;{testimonial.quote}&rdquo;</p>
                <div className="landing-testimonial-author">
                  <strong>{testimonial.name}</strong>
                  {testimonial.role && <span>{testimonial.role}</span>}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      <section className="landing-assurance">
        <div><p className="landing-section-kicker">Dibuat untuk momen pribadi</p><h2>Detail acara kalian tetap berada dalam kendali.</h2><p>Bagikan hanya yang tamu perlu lihat, kelola tamu dari satu dashboard, dan biarkan informasi penting tersusun rapi sampai hari acara.</p></div>
        <div className="landing-assurance-list"><div><b>01</b><span><strong>Link yang mudah dikirim</strong><small>Satu tautan undangan yang siap dibagikan di kanal apa pun.</small></span></div><div><b>02</b><span><strong>Data tamu tertata</strong><small>Catatan RSVP dan check-in tersimpan dalam workspace kalian.</small></span></div><div><b>03</b><span><strong>Kontrol di tangan kalian</strong><small>Ubah informasi undangan kapan pun diperlukan.</small></span></div></div>
      </section>

      <section className="landing-faq" aria-labelledby="faq-title">
        <div><p className="landing-section-kicker">FAQ</p><h2 id="faq-title">Masih ada yang ingin ditanyakan?</h2><p>Jawaban singkat untuk hal-hal yang biasanya ingin kalian pastikan sebelum mulai.</p></div>
        <div className="landing-faq-list"><details open><summary>Apakah bisa mulai tanpa membayar?</summary><p>Bisa. Paket Mulai dapat dipakai untuk membuat undangan pertama tanpa biaya.</p></details><details><summary>Apakah tamu perlu membuat akun?</summary><p>Tidak. Tamu cukup membuka link undangan dan mengisi konfirmasi hadir.</p></details><details><summary>Bisakah detail acara diubah setelah link dibagikan?</summary><p>Bisa. Perubahan yang kalian simpan akan langsung tampil di link undangan.</p></details><details><summary>Apakah tersedia RSVP dan check-in?</summary><p>Ya. Yukakad membantu mencatat RSVP dan memudahkan check-in di hari acara.</p></details></div>
      </section>

      <section className="landing-cta-banner" id="kontak">
        <div className="landing-cta-copy"><p className="landing-section-kicker">Mulai bersama Yukakad</p><h2>{kontak.heading ?? "Siap bikin undangan digitalmu?"}</h2><p>{kontak.subheading ?? "Daftar gratis dan buat undangan pertamamu hari ini."}</p></div>
        <div className="landing-cta-actions landing-hero-actions">
          <a href="/auth/register" className="landing-cta-button">
            Buat undangan gratis
          </a>
          {waLink && (
            <a href={waLink} className="landing-secondary-button" target="_blank" rel="noreferrer">
              Chat WhatsApp
            </a>
          )}
        </div>
      </section>

      <footer className="landing-footer">
        <div className="landing-footer-inner">
          <div className="landing-logo">
            {footer.heading ?? "yukakad"}
            <span>.</span>
          </div>
          <p>{footer.copyright ?? `© ${new Date().getFullYear()} Yukakad. All rights reserved.`}</p>
          {footer.instagram && <a href={`https://instagram.com/${footer.instagram.replace(/^@/, "")}`}>{footer.instagram}</a>}
        </div>
        <div className="landing-footer-columns">
          <div><span>Produk</span><a href="#fitur">Fitur</a><a href="#template">Template</a><a href="#harga">Harga</a></div>
          <div><span>Perusahaan</span><a href="#produk">Tentang Yukakad</a><a href="#testimoni">Cerita pasangan</a><a href="#kontak">Kontak</a></div>
          <div><span>Bantuan</span><a href="#faq-title">FAQ</a><a href="/auth/login">Masuk</a><a href="/auth/register">Mulai gratis</a></div>
        </div>
        <span className="landing-footer-watermark" aria-hidden>{footer.heading ?? "yukakad"}</span>
      </footer>
    </main>
  );
}
