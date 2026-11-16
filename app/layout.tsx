import type { ReactNode } from "react";
import type { Metadata, Viewport } from "next";
import { RegisterSw } from "@/components/register-sw";
import "./globals.css";

export const metadata: Metadata = {
  title: "Casa Control",
  description: "Tarefas da casa para o Jonas, com acompanhamento do Léo e da Bárbara.",
  applicationName: "Casa Control",
  robots: { index: false, follow: false },
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "Casa",
  },
  icons: {
    icon: "/icon-192.png",
    apple: "/apple-touch-icon.png",
  },
};

export const viewport: Viewport = {
  themeColor: "#1f5c40",
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="min-h-dvh">
        {children}
        <RegisterSw />
      </body>
    </html>
  );
}
