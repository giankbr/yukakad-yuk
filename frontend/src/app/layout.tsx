import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";

// Fonts are self-hosted (SIL OFL, see fonts/OFL*.txt) so builds don't depend on Google Fonts.
const beVietnamPro = localFont({
  src: [
    { path: "./fonts/BeVietnamPro-400.woff2", weight: "400", style: "normal" },
    { path: "./fonts/BeVietnamPro-400-italic.woff2", weight: "400", style: "italic" },
    { path: "./fonts/BeVietnamPro-500.woff2", weight: "500", style: "normal" },
    { path: "./fonts/BeVietnamPro-600.woff2", weight: "600", style: "normal" },
    { path: "./fonts/BeVietnamPro-700.woff2", weight: "700", style: "normal" },
  ],
  variable: "--font-be-vietnam",
  display: "swap",
});
const geistMono = localFont({ src: "./fonts/GeistMono-Variable.woff2", variable: "--font-geist-mono", weight: "100 900", display: "swap" });

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://rawuh.id";
const DEFAULT_TITLE = "Rawuh — Undangan digital yang terasa personal";
const DEFAULT_DESCRIPTION = "Buat undangan website dalam 10 menit dari HP. Kirim ke ratusan tamu, masing-masing dengan namanya.";

export const metadata: Metadata = {
  // Resolves relative og:image/canonical URLs (pages may override any of the defaults below).
  metadataBase: new URL(SITE_URL),
  title: DEFAULT_TITLE,
  description: DEFAULT_DESCRIPTION,
  applicationName: "Rawuh",
  openGraph: {
    type: "website",
    siteName: "Rawuh",
    locale: "id_ID",
    title: DEFAULT_TITLE,
    description: DEFAULT_DESCRIPTION,
    images: [{ url: "/rawuh/phone-kirana.webp", width: 1200, height: 655, alt: "Contoh undangan digital Rawuh" }],
  },
  twitter: { card: "summary_large_image", title: DEFAULT_TITLE, description: DEFAULT_DESCRIPTION, images: ["/rawuh/phone-kirana.webp"] },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="id" className={`${beVietnamPro.variable} ${geistMono.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
