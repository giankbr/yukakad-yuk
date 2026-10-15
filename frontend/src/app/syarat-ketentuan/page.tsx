import type { Metadata } from "next";
import { LegalPage } from "@/components/landing/LegalPage";
import { terms } from "@/lib/legal";
import { getLegal } from "@/lib/marketing";

export const metadata: Metadata = {
  title: "Syarat & Ketentuan | Rawuh",
  description: "Aturan penggunaan Rawuh: akun, konten undangan, paket & pembayaran, pengembalian dana, dan amplop digital.",
};

export default async function SyaratKetentuanPage() {
  return <LegalPage doc={await getLegal(terms)} />;
}
