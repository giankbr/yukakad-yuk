import type { Metadata } from "next";
import { LegalPage } from "@/components/landing/LegalPage";
import { terms } from "@/lib/legal";

export const metadata: Metadata = {
  title: "Syarat & Ketentuan | Rawuh",
  description: "Aturan penggunaan Rawuh: akun, konten undangan, paket & pembayaran, pengembalian dana, dan amplop digital.",
};

export default function SyaratKetentuanPage() {
  return <LegalPage doc={terms} />;
}
