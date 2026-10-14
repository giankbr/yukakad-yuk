import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";

// Geist is self-hosted (SIL OFL, see fonts/OFL.txt) so builds don't depend on Google Fonts.
const geistSans = localFont({ src: "./fonts/Geist-Variable.woff2", variable: "--font-geist-sans", weight: "100 900", display: "swap" });
const geistMono = localFont({ src: "./fonts/GeistMono-Variable.woff2", variable: "--font-geist-mono", weight: "100 900", display: "swap" });

export const metadata: Metadata = {
  title: "Rawuh — Undangan digital yang terasa personal",
  description: "Buat undangan website dalam 10 menit dari HP. Kirim ke ratusan tamu, masing-masing dengan namanya.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="id" className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
