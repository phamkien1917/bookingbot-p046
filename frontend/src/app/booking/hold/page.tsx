"use client";

import { Suspense, useCallback, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { FaCheckCircle, FaClock, FaRobot, FaSpinner, FaTimesCircle } from "react-icons/fa";
import Header from "@/components/Header";
import ProtectedPage from "@/components/ProtectedPage";
import { apiFetch } from "@/lib/api";
import type { Booking } from "@/lib/types";

const CUSTOMER_ROLES = ["CUSTOMER"] as const;

function HoldContent() {
  const params = useSearchParams();
  const router = useRouter();
  const bookingId = params.get("booking_id");
  const [booking, setBooking] = useState<Booking | null>(null);
  const [remaining, setRemaining] = useState(0);
  const [error, setError] = useState("");
  const [cancelling, setCancelling] = useState(false);

  const load = useCallback(async () => {
    if (!bookingId) return;
    try {
      const data = await apiFetch<Booking>(`/bookings/${bookingId}`);
      setBooking(data);
      if (data.status === "BOOKED") router.replace(`/booking/confirmation?booking_id=${data.id}`);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Không tải được yêu cầu");
    }
  }, [bookingId, router]);

  useEffect(() => {
    const initial = window.setTimeout(() => void load(), 0);
    const poller = window.setInterval(() => void load(), 3000);
    return () => { window.clearTimeout(initial); window.clearInterval(poller); };
  }, [load]);

  useEffect(() => {
    if (!booking?.expires_at) return;
    const update = () => setRemaining(Math.max(0, Math.floor((new Date(booking.expires_at as string).getTime() - Date.now()) / 1000)));
    update();
    const timer = window.setInterval(update, 1000);
    return () => window.clearInterval(timer);
  }, [booking?.expires_at]);

  const cancel = async () => {
    if (!bookingId || !window.confirm("Bạn chắc chắn muốn hủy yêu cầu xem nhà này?")) return;
    setCancelling(true);
    try {
      await apiFetch(`/bookings/${bookingId}/cancel`, { method: "POST", body: JSON.stringify({ reason: "Khách hàng hủy từ giao diện" }) });
      router.replace("/my-bookings");
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Không thể hủy yêu cầu");
    } finally {
      setCancelling(false);
    }
  };

  const minutes = String(Math.floor(remaining / 60)).padStart(2, "0");
  const seconds = String(remaining % 60).padStart(2, "0");
  const terminal = booking && ["REJECTED", "EXPIRED", "CANCELLED"].includes(booking.status);

  return (
    <ProtectedPage roles={[...CUSTOMER_ROLES]}>
      <div className="min-h-screen bg-slate-50"><Header /><main className="max-w-4xl mx-auto px-4 py-10">
        {!bookingId ? <div className="text-center py-20"><p className="text-red-500">Thiếu mã yêu cầu.</p><Link href="/my-bookings" className="text-teal-700">Xem lịch của tôi</Link></div> : !booking && !error ? <div className="py-24 grid place-items-center"><FaSpinner className="animate-spin text-3xl text-teal-500" /></div> : (
          <div className="grid md:grid-cols-[1fr_320px] gap-7">
            <section className="bg-white rounded-3xl p-7 border border-slate-100 shadow-sm">
              {terminal ? <><FaTimesCircle className="text-5xl text-red-400 mb-5" /><h1 className="text-2xl font-bold text-slate-800">Yêu cầu không được xác nhận</h1><p className="text-slate-500 mt-2">Trạng thái: {booking?.status}. Bạn có thể chọn một khung giờ khác.</p><Link href={`/booking/schedule?property_id=${booking?.property.id}`} className="inline-block mt-6 bg-teal-500 text-white px-6 py-3 rounded-xl">Chọn lịch khác</Link></> : <><div className="flex items-center gap-3 text-teal-600 mb-5"><FaRobot className="text-3xl" /><span className="font-bold">AI đang chuyển yêu cầu đến sale phù hợp</span></div><h1 className="text-3xl font-bold text-slate-800">Đang chờ sale xác nhận</h1><p className="text-slate-500 mt-3">Trang tự động cập nhật mỗi 3 giây. Bạn có thể để trang mở hoặc xem trạng thái trong “Lịch xem của tôi”.</p><div className="mt-8 space-y-5"><div className="flex gap-3"><FaCheckCircle className="text-teal-500 mt-1" /><div><p className="font-semibold">Đã kiểm tra căn</p><p className="text-sm text-slate-500">Bất động sản khả dụng tại thời điểm gửi yêu cầu.</p></div></div><div className="flex gap-3"><FaCheckCircle className="text-teal-500 mt-1" /><div><p className="font-semibold">Đã giữ khung giờ</p><p className="text-sm text-slate-500">Khung giờ được giữ tạm trong 15 phút.</p></div></div><div className="flex gap-3"><FaSpinner className="text-orange-500 mt-1 animate-spin" /><div><p className="font-semibold">Đang chờ phản hồi</p><p className="text-sm text-slate-500">Sale có thể nhận hoặc từ chối yêu cầu trên dashboard.</p></div></div></div></>}
              {error && <div role="alert" className="mt-6 bg-red-50 text-red-600 p-4 rounded-xl">{error}</div>}
            </section>
            {booking && <aside className="bg-slate-900 text-white rounded-3xl p-6 h-fit"><p className="text-xs text-slate-400 uppercase">Thời gian giữ còn lại</p><p className="text-5xl font-bold text-orange-400 my-4">{minutes}:{seconds}</p><h2 className="font-bold text-lg">{booking.property.title}</h2><p className="text-sm text-slate-300 mt-2">{booking.property.address}</p><div className="border-t border-white/10 mt-5 pt-5 text-sm space-y-2"><p><FaClock className="inline mr-2" />{new Date(booking.preferred_start).toLocaleString("vi-VN")}</p><p>Mã yêu cầu: {booking.request_code}</p></div>{!terminal && <button onClick={cancel} disabled={cancelling} className="w-full mt-6 border border-red-400 text-red-300 py-3 rounded-xl hover:bg-red-500/10 disabled:opacity-50">{cancelling ? "Đang hủy..." : "Hủy yêu cầu"}</button>}</aside>}
          </div>
        )}
      </main></div>
    </ProtectedPage>
  );
}

export default function HoldPage() {
  return <Suspense fallback={<div className="min-h-screen grid place-items-center"><FaSpinner className="animate-spin text-3xl text-teal-500" /></div>}><HoldContent /></Suspense>;
}
