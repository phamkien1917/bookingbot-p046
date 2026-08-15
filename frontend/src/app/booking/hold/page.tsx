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
      <div className="min-h-screen bg-[var(--paper)] text-[var(--ink)] font-sans">
        <Header />
        <main className="max-w-5xl mx-auto px-4 py-10">
          {!bookingId ? (
            <div className="text-center py-20"><p className="text-[var(--coral)] mb-4">Thiếu mã yêu cầu.</p><Link href="/my-bookings" className="text-[var(--forest)] font-semibold">Xem lịch của tôi</Link></div>
          ) : !booking && !error ? (
            <div className="py-24 grid place-items-center"><FaSpinner className="animate-spin text-3xl text-[var(--forest)]" /></div>
          ) : (
            <div className="grid md:grid-cols-[1fr_360px] gap-8">
              <section className="bg-white rounded-[1.5rem] p-8 border border-black/5 shadow-sm">
                {terminal ? (
                  <>
                    <FaTimesCircle className="text-5xl text-[var(--coral)] mb-5" />
                    <h1 className="text-3xl font-bold">Yêu cầu không được xác nhận</h1>
                    <p className="text-[var(--muted)] mt-3">Trạng thái: {booking?.status}. Bạn có thể chọn một khung giờ khác.</p>
                    <Link href={`/booking/schedule?property_id=${booking?.property.id}`} className="inline-block mt-8 bg-[var(--forest)] text-white px-8 py-3.5 rounded-full font-semibold transition-transform hover:scale-105">Chọn lịch khác</Link>
                  </>
                ) : (
                  <>
                    <div className="flex items-center gap-3 text-[var(--forest)] mb-5">
                      <FaRobot className="text-3xl" />
                      <span className="font-bold text-sm tracking-wide uppercase">AI đang xử lý yêu cầu</span>
                    </div>
                    <h1 className="text-3xl font-bold">Đang chờ sale xác nhận</h1>
                    <p className="text-[var(--muted)] mt-3">Trang tự động cập nhật mỗi 3 giây. Bạn có thể để trang mở hoặc xem trạng thái trong “Lịch xem của tôi”.</p>
                    
                    <div className="mt-10 space-y-6">
                      <div className="flex gap-4">
                        <FaCheckCircle className="text-[var(--sage)] mt-1 text-xl" />
                        <div>
                          <p className="font-semibold text-lg">Đã kiểm tra căn</p>
                          <p className="text-sm text-[var(--muted)] mt-1">Bất động sản khả dụng tại thời điểm gửi yêu cầu.</p>
                        </div>
                      </div>
                      <div className="flex gap-4">
                        <FaCheckCircle className="text-[var(--sage)] mt-1 text-xl" />
                        <div>
                          <p className="font-semibold text-lg">Đã giữ khung giờ</p>
                          <p className="text-sm text-[var(--muted)] mt-1">Khung giờ được giữ tạm trong 15 phút.</p>
                        </div>
                      </div>
                      <div className="flex gap-4">
                        <FaSpinner className="text-amber-500 mt-1 text-xl animate-spin" />
                        <div>
                          <p className="font-semibold text-lg">Đang chờ phản hồi</p>
                          <p className="text-sm text-[var(--muted)] mt-1">Sale có thể nhận hoặc từ chối yêu cầu trên dashboard.</p>
                        </div>
                      </div>
                    </div>
                  </>
                )}
                {error && <div role="alert" className="mt-8 bg-red-50 text-red-600 border border-red-200 p-4 rounded-xl">{error}</div>}
              </section>
              
              {booking && (
                <aside className="bg-[var(--ink)] text-white rounded-[1.5rem] p-7 h-fit shadow-xl">
                  <p className="text-xs font-bold tracking-[.15em] text-[#bcd2c1] uppercase">Thời gian giữ còn lại</p>
                  <p className="text-6xl font-bold text-[#e8a58d] my-6 font-mono">{minutes}:{seconds}</p>
                  <h2 className="font-bold text-xl leading-tight">{booking.property.title}</h2>
                  <p className="text-sm text-white/70 mt-2 line-clamp-2">{booking.property.address}</p>
                  <div className="border-t border-white/15 mt-6 pt-6 text-sm space-y-3">
                    <p className="flex items-center"><FaClock className="mr-3 text-[#a9c9b0]" />{new Date(booking.preferred_start).toLocaleString("vi-VN")}</p>
                    <p className="flex items-center"><FaRobot className="mr-3 text-[#a9c9b0]" />Mã YC: <span className="font-mono ml-1">{booking.request_code}</span></p>
                  </div>
                  {!terminal && (
                    <button onClick={cancel} disabled={cancelling} className="w-full mt-8 border border-[#e8a58d] text-[#e8a58d] py-3.5 rounded-xl font-semibold hover:bg-[#e8a58d]/10 transition-colors disabled:opacity-50">
                      {cancelling ? "Đang hủy..." : "Hủy yêu cầu này"}
                    </button>
                  )}
                </aside>
              )}
            </div>
          )}
        </main>
      </div>
    </ProtectedPage>
  );
}

export default function HoldPage() {
  return <Suspense fallback={<div className="min-h-screen bg-[var(--paper)] grid place-items-center"><FaSpinner className="animate-spin text-3xl text-[var(--forest)]" /></div>}><HoldContent /></Suspense>;
}
