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

export const metadata: Metadata = {
  title: "Rawuh — Undangan digital yang terasa personal",
  description: "Buat undangan website dalam 10 menit dari HP. Kirim ke ratusan tamu, masing-masing dengan namanya.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="id" className={`${beVietnamPro.variable} ${geistMono.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
