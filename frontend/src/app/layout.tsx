import type { Metadata } from "next";
import "./globals.css";
import AuthProvider from "@/components/AuthProvider";
import ChatLauncher from "@/components/ChatLauncher";
import { Toaster } from "sonner";

export const metadata: Metadata = {
  title: "Nera — Trợ lý AI tìm và đặt lịch xem nhà",
  description: "Trợ lý tìm nhà có trí nhớ: hiểu nhu cầu, gợi ý bất động sản và kết nối Sale để đặt lịch xem.",
  icons: {
    icon: "/brand/logo/nera-symbol.svg",
    shortcut: "/brand/logo/nera-symbol.svg",
    apple: "/brand/png/logo/nera-symbol.png",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi" className="h-full antialiased" data-scroll-behavior="smooth">
      <body className="min-h-full font-sans">
        <AuthProvider>
          {children}
          <Toaster richColors position="bottom-center" />
          <ChatLauncher />
        </AuthProvider>
      </body>
    </html>
  );
}
