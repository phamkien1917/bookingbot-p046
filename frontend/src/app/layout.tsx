import type { Metadata } from "next";
import "./globals.css";
import AuthProvider from "@/components/AuthProvider";
import ChatLauncher from "@/components/ChatLauncher";
import { Toaster } from "sonner";

const SITE_URL = "https://www.nerahome.space";
const TITLE = "Nera — Trợ lý AI tìm và đặt lịch xem nhà";
const DESCRIPTION =
  "Mô tả nhu cầu bằng lời thường, Nera gợi ý căn có thật trong kho 3.796 tin đã kiểm chứng toạ độ, rồi đặt lịch xem theo giờ trống thật của nhân viên sale.";

export const metadata: Metadata = {
  // Next needs an absolute base to turn the image path below into the full URL
  // that Zalo, Messenger and Discord fetch when someone shares the link.
  metadataBase: new URL(SITE_URL),
  title: TITLE,
  description: DESCRIPTION,
  openGraph: {
    type: "website",
    locale: "vi_VN",
    url: SITE_URL,
    siteName: "Nera",
    title: TITLE,
    description: DESCRIPTION,
    images: [
      {
        url: "/og/nera-og.png",
        width: 1672,
        height: 941,
        alt: "Nera — tìm nhà bằng một cuộc trò chuyện",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: TITLE,
    description: DESCRIPTION,
    images: ["/og/nera-og.png"],
  },
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
