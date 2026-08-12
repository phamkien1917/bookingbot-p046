"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { FaCalendarPlus, FaCheckCircle, FaHome, FaMapMarkedAlt, FaPhone, FaSpinner } from "react-icons/fa";
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
      <main className="min-h-screen bg-gradient-to-b from-green-50 to-white px-4 py-14">
        {!bookingId ? <div className="text-center">Thiếu mã booking. <Link href="/my-bookings" className="text-teal-700">Xem lịch của tôi</Link></div> : error ? <div className="max-w-lg mx-auto bg-red-50 text-red-600 p-5 rounded-xl">{error}</div> : !booking ? <div className="grid place-items-center py-24"><FaSpinner className="animate-spin text-3xl text-teal-500" /></div> : booking.status !== "BOOKED" || !booking.appointment ? <div className="max-w-lg mx-auto text-center"><h1 className="text-2xl font-bold">Booking chưa được xác nhận</h1><p className="text-slate-500 mt-2 mb-6">Trạng thái hiện tại: {booking.status}</p><Link href={`/booking/hold?booking_id=${booking.id}`} className="bg-slate-900 text-white px-6 py-3 rounded-xl">Theo dõi yêu cầu</Link></div> : (
          <div className="max-w-3xl mx-auto text-center">
            <div className="w-20 h-20 bg-green-100 rounded-full grid place-items-center mx-auto mb-6"><FaCheckCircle className="text-green-500 text-4xl" /></div>
            <h1 className="text-3xl font-bold text-slate-800">Lịch xem nhà đã được xác nhận</h1>
            <p className="text-slate-500 mt-3 mb-9">Sale đã nhận lịch. Thông tin dưới đây được lấy trực tiếp từ booking trong hệ thống.</p>
            <div className="grid md:grid-cols-2 gap-6 text-left">
              <section className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm"><h2 className="font-bold text-lg mb-5">Chi tiết lịch hẹn</h2><dl className="space-y-3 text-sm"><div><dt className="text-slate-500">Mã booking</dt><dd className="font-bold">{booking.appointment.booking_code}</dd></div><div><dt className="text-slate-500">Bất động sản</dt><dd className="font-bold">{booking.property.title}</dd></div><div><dt className="text-slate-500">Thời gian</dt><dd className="font-bold">{new Date(booking.appointment.starts_at).toLocaleString("vi-VN")}</dd></div><div><dt className="text-slate-500">Địa chỉ</dt><dd className="font-bold">{booking.property.address}</dd></div></dl></section>
              <section className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm"><h2 className="font-bold text-lg mb-5">Nhân viên tư vấn</h2><div className="w-14 h-14 rounded-full bg-teal-100 grid place-items-center text-teal-700 font-bold text-xl mb-4">{booking.sale?.full_name.charAt(0) ?? "S"}</div><p className="font-bold text-slate-800">{booking.sale?.full_name}</p><p className="text-sm text-slate-500">{booking.sale?.job_title ?? "Chuyên viên tư vấn"}</p>{booking.sale?.phone && <a href={`tel:${booking.sale.phone}`} className="mt-6 w-full border border-slate-200 py-3 rounded-xl flex justify-center items-center gap-2 hover:bg-slate-50"><FaPhone className="text-teal-500" /> Gọi {booking.sale.phone}</a>}</section>
            </div>
            <div className="flex flex-wrap gap-3 justify-center mt-9"><a href={googleCalendarUrl(booking)} target="_blank" rel="noreferrer" className="bg-slate-900 text-white px-6 py-3 rounded-full flex items-center gap-2"><FaCalendarPlus /> Thêm vào Google Calendar</a><a href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(booking.property.address)}`} target="_blank" rel="noreferrer" className="bg-teal-500 text-white px-6 py-3 rounded-full flex items-center gap-2"><FaMapMarkedAlt /> Xem chỉ đường</a><Link href="/my-bookings" className="bg-white border border-slate-200 px-6 py-3 rounded-full flex items-center gap-2"><FaHome /> Lịch của tôi</Link></div>
          </div>
        )}
      </main>
    </ProtectedPage>
  );
}

export default function ConfirmationPage() {
  return <Suspense fallback={<div className="min-h-screen grid place-items-center"><FaSpinner className="animate-spin text-3xl text-teal-500" /></div>}><ConfirmationContent /></Suspense>;
}
