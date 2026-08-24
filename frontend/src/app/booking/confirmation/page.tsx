"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { FaCalendarPlus, FaCheckCircle, FaHome, FaMapMarkedAlt, FaPhone, FaSpinner } from "react-icons/fa";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ProtectedPage from "@/components/ProtectedPage";
import { apiFetch } from "@/lib/api";
import type { Booking } from "@/lib/types";

const CUSTOMER_ROLES = ["CUSTOMER"] as const;

function googleCalendarUrl(booking: Booking) {
  const compact = (value: string) => new Date(value).toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  const query = new URLSearchParams({
    action: "TEMPLATE",
    text: `Xem nhà - ${booking.property.title}`,
    dates: `${compact(booking.preferred_start)}/${compact(booking.preferred_end)}`,
    details: `Mã booking: ${booking.appointment?.booking_code ?? booking.request_code}`,
    location: booking.property.address,
  });
  return `https://calendar.google.com/calendar/render?${query.toString()}`;
}

function ConfirmationContent() {
  const bookingId = useSearchParams().get("booking_id");
  const [booking, setBooking] = useState<Booking | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!bookingId) return;
    let active = true;
    apiFetch<Booking>(`/bookings/${bookingId}`).then((data) => { if (active) setBooking(data); }).catch((reason: unknown) => { if (active) setError(reason instanceof Error ? reason.message : "Không tải được booking"); });
    return () => { active = false; };
  }, [bookingId]);

  return (
    <ProtectedPage roles={[...CUSTOMER_ROLES]}>
      <div className="min-h-screen bg-[var(--paper)] text-[var(--ink)] font-sans">
        <Header />
        <main className="max-w-5xl mx-auto px-4 py-14">
          {!bookingId ? (
            <div className="text-center py-20">Thiếu mã booking. <Link href="/my-bookings" className="text-[var(--forest)] font-semibold">Xem lịch của tôi</Link></div>
          ) : error ? (
            <div className="max-w-lg mx-auto bg-red-50 text-red-600 border border-red-200 p-5 rounded-[1.5rem] shadow-sm">{error}</div>
          ) : !booking ? (
            <div className="grid place-items-center py-24"><FaSpinner className="animate-spin text-3xl text-[var(--forest)]" /></div>
          ) : booking.status !== "BOOKED" || !booking.appointment ? (
            <div className="max-w-lg mx-auto text-center bg-white p-10 rounded-[1.5rem] border border-black/5 shadow-sm">
              <h1 className="text-2xl font-bold">Booking chưa được xác nhận</h1>
              <p className="text-[var(--muted)] mt-2 mb-8">Trạng thái hiện tại: {booking.status}</p>
              {["REJECTED", "EXPIRED", "CANCELLED"].includes(booking.status) ? (
                <Link href={`/booking/schedule?property_id=${booking.property.id}`} className="bg-[var(--forest)] text-white px-8 py-3.5 rounded-full font-semibold transition-transform hover:scale-105">Chọn lịch khác</Link>
              ) : (
                <Link href={`/booking/hold?booking_id=${booking.id}`} className="bg-[var(--ink)] text-white px-8 py-3.5 rounded-full font-semibold transition-transform hover:scale-105">Theo dõi yêu cầu</Link>
              )}
            </div>
          ) : (
            <div className="max-w-4xl mx-auto">
              <div className="text-center mb-12">
                <div className="w-24 h-24 bg-[#e6eee7] rounded-full grid place-items-center mx-auto mb-6">
                  <FaCheckCircle className="text-[var(--forest)] text-5xl" />
                </div>
                <h1 className="text-4xl font-bold tracking-tight">Lịch xem nhà đã được xác nhận</h1>
                <p className="text-[var(--muted)] mt-4">Sale đã nhận lịch. Thông tin dưới đây được lấy trực tiếp từ booking trong hệ thống.</p>
              </div>
              
              <div className="grid md:grid-cols-[1.2fr_1fr] gap-8 text-left mb-10">
                <section className="bg-white rounded-[1.5rem] p-8 border border-black/5 shadow-sm">
                  <h2 className="font-bold text-xl mb-6">Chi tiết lịch hẹn</h2>
                  <dl className="space-y-4 text-sm">
                    <div><dt className="text-[var(--muted)] mb-1">Mã booking</dt><dd className="font-bold font-mono text-lg">{booking.appointment.booking_code}</dd></div>
                    <div><dt className="text-[var(--muted)] mb-1">Bất động sản</dt><dd className="font-bold">{booking.property.title}</dd></div>
                    <div><dt className="text-[var(--muted)] mb-1">Thời gian</dt><dd className="font-bold">{new Date(booking.appointment.starts_at).toLocaleString("vi-VN", { weekday: "long", year: "numeric", month: "long", day: "numeric", hour: "2-digit", minute: "2-digit" })}</dd></div>
                    <div><dt className="text-[var(--muted)] mb-1">Địa chỉ</dt><dd className="font-bold">{booking.property.address}</dd></div>
                  </dl>
                </section>
                
                <section className="bg-white rounded-[1.5rem] p-8 border border-black/5 shadow-sm flex flex-col justify-center items-center text-center">
                  <h2 className="font-bold text-xl mb-6 w-full text-left">Nhân viên tư vấn</h2>
                  <div className="w-20 h-20 rounded-full bg-[var(--forest)] grid place-items-center text-white font-bold text-2xl mb-4 shadow-md">
                    {booking.sale?.full_name.charAt(0) ?? "S"}
                  </div>
                  <p className="font-bold text-xl">{booking.sale?.full_name}</p>
                  <p className="text-[var(--muted)] mt-1">{booking.sale?.job_title ?? "Chuyên viên tư vấn"}</p>
                  {booking.sale?.phone && (
                    <a href={`tel:${booking.sale.phone}`} className="mt-8 w-full border border-black/10 py-3.5 rounded-xl font-semibold flex justify-center items-center gap-2 hover:bg-[#fbfaf7] transition-colors">
                      <FaPhone className="text-[var(--coral)]" /> Gọi {booking.sale.phone}
                    </a>
                  )}
                </section>
              </div>
              
              <div className="flex flex-col sm:flex-row flex-wrap gap-4 justify-center">
                <a href={googleCalendarUrl(booking)} target="_blank" rel="noreferrer" className="bg-[var(--ink)] text-white px-8 py-4 rounded-full font-semibold flex items-center justify-center gap-2 transition-transform hover:scale-105 shadow-sm">
                  <FaCalendarPlus /> Thêm vào Calendar
                </a>
                <a href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(booking.property.address)}`} target="_blank" rel="noreferrer" className="bg-[var(--forest)] text-white px-8 py-4 rounded-full font-semibold flex items-center justify-center gap-2 transition-transform hover:scale-105 shadow-sm">
                  <FaMapMarkedAlt /> Xem chỉ đường
                </a>
                <Link href="/my-bookings" className="bg-white border border-black/10 text-[var(--ink)] px-8 py-4 rounded-full font-semibold flex items-center justify-center gap-2 transition-transform hover:scale-105 shadow-sm">
                  <FaHome /> Lịch của tôi
                </Link>
              </div>
            </div>
          )}
        </main>
        <Footer />
      </div>
    </ProtectedPage>
  );
}

export default function ConfirmationPage() {
  return <Suspense fallback={<div className="min-h-screen bg-[var(--paper)] grid place-items-center"><FaSpinner className="animate-spin text-3xl text-[var(--forest)]" /></div>}><ConfirmationContent /></Suspense>;
}
