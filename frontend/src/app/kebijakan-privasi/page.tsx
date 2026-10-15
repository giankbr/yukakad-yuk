import type { Metadata } from "next";
import { LegalPage } from "@/components/landing/LegalPage";
import { privacy } from "@/lib/legal";

export const metadata: Metadata = {
  title: "Kebijakan Privasi | Rawuh",
  description: "Data apa yang Rawuh kumpulkan dari pemilik undangan dan tamu, untuk apa, dan bagaimana kamu mengendalikannya.",
};

export default function KebijakanPrivasiPage() {
  return <LegalPage doc={privacy} />;
}
