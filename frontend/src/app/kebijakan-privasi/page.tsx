import type { Metadata } from "next";
import { LegalPage } from "@/components/landing/LegalPage";
import { privacy } from "@/lib/legal";
import { getLegal } from "@/lib/marketing";

export const metadata: Metadata = {
  title: "Kebijakan Privasi | Rawuh",
  description: "Data apa yang Rawuh kumpulkan dari pemilik undangan dan tamu, untuk apa, dan bagaimana kamu mengendalikannya.",
};

export default async function KebijakanPrivasiPage() {
  return <LegalPage doc={await getLegal(privacy)} />;
}
