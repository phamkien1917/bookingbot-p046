import type { Metadata } from "next";
import "./globals.css";
import AuthProvider from "@/components/AuthProvider";
import ChatLauncher from "@/components/ChatLauncher";

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
          <ChatLauncher />
        </AuthProvider>
      </body>
    </html>
  );
}
