import type { Metadata } from "next";
import "./globals.css";
import AuthProvider from "@/components/AuthProvider";

export const metadata: Metadata = {
  title: "Booking Bot AI - Đặt lịch xem nhà thông minh",
  description: "Giải pháp AI thông minh giúp tối ưu hóa quy trình tìm kiếm và đặt lịch xem bất động sản.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi" className="h-full antialiased">
      <body className="min-h-full flex flex-col font-sans"><AuthProvider>{children}</AuthProvider></body>
    </html>
  );
}
