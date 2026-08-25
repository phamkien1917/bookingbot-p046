"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FaArrowLeft, FaArrowRight, FaClock, FaSpinner, FaCalendarAlt } from "react-icons/fa";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ProtectedPage from "@/components/ProtectedPage";
import { apiFetch } from "@/lib/api";
import type { AvailabilitySlot, Booking } from "@/lib/types";

const CUSTOMER_ROLES = ["CUSTOMER"] as const;
interface RescheduleProposal { id: string; sale_user_id: string; starts_at: string; ends_at: string; expires_at: string }

function dateKey(value: Date) {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, "0");
  const day = String(value.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function RescheduleContent() {
  const params = useSearchParams();
  const router = useRouter();
  const bookingId = params.get("booking_id");
  
  const dates = useMemo(() => Array.from({ length: 7 }, (_, index) => { const value = new Date(); value.setDate(value.getDate() + index + 1); return value; }), []);
  const [selectedDate, setSelectedDate] = useState(dateKey(dates[0]));
  const [booking, setBooking] = useState<Booking | null>(null);
  const [slots, setSlots] = useState<AvailabilitySlot[]>([]);
  const [selectedSlot, setSelectedSlot] = useState<AvailabilitySlot | null>(null);
  const [proposals, setProposals] = useState<RescheduleProposal[]>([]);
  
  const [loading, setLoading] = useState(true);
  const [loadingSlots, setLoadingSlots] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  // Load old booking
  useEffect(() => {
    if (!bookingId) return;
    apiFetch<Booking>(`/bookings/${bookingId}`)
      .then((data) => {
        setBooking(data);
        setError("");
      })
      .catch((reason) => setError(reason instanceof Error ? reason.message : "Không tải được thông tin lịch hẹn"))
      .finally(() => setLoading(false));
  }, [bookingId]);

  // Load new slots
  useEffect(() => {
    if (!booking) return;
    setLoadingSlots(true);
    apiFetch<{ slots: AvailabilitySlot[] }>(`/bookings/availability?property_id=${booking.property.id}&date=${selectedDate}`)
      .then((data) => {
        setSlots(data.slots);
        setSelectedSlot(data.slots[0] ?? null);
      })
      .catch(() => setSlots([]))
      .finally(() => setLoadingSlots(false));
  }, [booking, selectedDate]);

  const submit = async () => {
    if (!bookingId || !selectedSlot) return;
    setSubmitting(true);
    setError("");
    try {
      const newBooking = await apiFetch<Booking>(`/bookings/${bookingId}/reschedule`, {
        method: "POST",
        body: JSON.stringify({
          sale_user_id: selectedSlot.sale_user_id,
          new_preferred_start: selectedSlot.starts_at,
          new_preferred_end: selectedSlot.ends_at,
        }),
      });
      router.push(`/booking/hold?booking_id=${newBooking.id}`);
    } catch (reason) {
      try {
        const alternatives = await apiFetch<RescheduleProposal[]>(`/bookings/${bookingId}/reschedule/proposals`, {
          method: "POST",
          body: JSON.stringify({ desired_start: selectedSlot.starts_at, reason: "SCHEDULE_CONFLICT" }),
        });
        setProposals(alternatives);
        setError("Khung giờ vừa xung đột. Lịch cũ vẫn được giữ cho đến khi bạn xác nhận một lựa chọn thay thế.");
        return;
      } catch {
        // Keep the original conflict message when no alternative exists.
      }
      setError(reason instanceof Error ? reason.message : "Không thể dời lịch xem");
    } finally {
      setSubmitting(false);
    }
  };

  const confirmProposal = async (proposal: RescheduleProposal) => {
    if (!bookingId) return;
    setSubmitting(true);
    setError("");
    try {
      const newBooking = await apiFetch<Booking>(`/bookings/${bookingId}/reschedule/proposals/${proposal.id}/confirm`, { method: "POST" });
      router.push(`/booking/hold?booking_id=${newBooking.id}`);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Đề xuất đã hết hiệu lực");
    } finally {
      setSubmitting(false);
    }
  };

  if (!bookingId) return <div className="min-h-screen bg-[var(--paper)] grid place-items-center"><div className="text-center"><p className="text-[var(--coral)] mb-4">Thiếu mã booking.</p><Link href="/my-bookings" className="text-[var(--forest)] font-semibold">Về lịch của tôi</Link></div></div>;

  return (
    <ProtectedPage roles={[...CUSTOMER_ROLES]}>
      <div className="min-h-screen bg-[var(--paper)] text-[var(--ink)] font-sans">
        <Header />
        <main className="px-4 py-10">
          <div className="max-w-4xl mx-auto">
            <Link href="/my-bookings" className="inline-flex items-center text-[var(--muted)] hover:text-[var(--ink)] text-sm transition-colors"><FaArrowLeft className="mr-2" /> Quay lại lịch của tôi</Link>
            <h1 className="text-3xl font-bold mt-8">Đề xuất dời lịch xem</h1>
            <p className="text-[var(--muted)] mt-2 mb-8">{booking?.property.title ?? "Đang tải thông tin..."}</p>
            
            {error && <div role="alert" className="bg-red-50 border border-red-200 text-red-600 p-4 rounded-[1.5rem] mb-6 shadow-sm">{error}</div>}
            
            {proposals.length > 0 && (
              <section className="mb-6 rounded-[1.5rem] border border-amber-200 bg-amber-50 p-5">
                <h2 className="font-semibold">Khung giờ thay thế — cần bạn xác nhận</h2>
                <p className="mt-1 text-xs text-[var(--muted)]">Hệ thống chưa thay đổi lịch cũ.</p>
                <div className="mt-3 flex flex-wrap gap-3">
                  {proposals.map((proposal) => (
                    <button key={proposal.id} onClick={() => void confirmProposal(proposal)} disabled={submitting} className="rounded-xl bg-white px-4 py-3 text-sm font-semibold shadow-sm disabled:opacity-50">
                      {new Date(proposal.starts_at).toLocaleString("vi-VN")}
                    </button>
                  ))}
                </div>
              </section>
            )}

            {loading ? <div className="py-20 grid place-items-center"><FaSpinner className="animate-spin text-3xl text-[var(--forest)]" /></div> : booking ? (
              <div className="grid md:grid-cols-[300px_1fr] gap-8 mb-8">
                {/* Old Booking Info */}
                <aside className="bg-white p-6 rounded-[1.5rem] border border-black/5 shadow-sm h-fit">
                  <p className="text-xs font-bold uppercase tracking-[.15em] text-[var(--coral)] mb-4">Lịch cũ</p>
                  <p className="font-semibold text-lg">{new Date(booking.preferred_start).toLocaleString("vi-VN", { weekday: "long", day: "2-digit", month: "2-digit", year: "numeric" })}</p>
                  <p className="text-sm text-[var(--muted)] flex items-center mt-1"><FaClock className="mr-2 text-[var(--forest)]" /> {new Date(booking.preferred_start).toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" })} – {new Date(booking.preferred_end).toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" })}</p>
                  <hr className="my-4 border-black/10" />
                  <p className="text-sm"><strong>Sale:</strong> {booking.sale?.full_name ?? "Đang chờ phân bổ"}</p>
                  <p className="text-sm mt-1"><strong>Mã yêu cầu:</strong> <span className="font-mono">{booking.request_code}</span></p>
                </aside>

                {/* New Slot Selection */}
                <div className="bg-white p-6 sm:p-8 rounded-[1.5rem] border border-black/5 shadow-sm">
                  <section className="mb-8">
                    <h2 className="font-bold mb-4">Chọn ngày mới</h2>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                      {dates.map((value) => { 
                        const key = dateKey(value); 
                        return (
                          <button key={key} onClick={() => setSelectedDate(key)} className={`p-3 rounded-xl border text-sm transition-all duration-200 hover:scale-[1.02] ${selectedDate === key ? "bg-[var(--forest)] text-white border-[var(--forest)] shadow-md" : "border-black/10 bg-[#fbfaf7] hover:border-[var(--sage)]"}`}>
                            <span className="block font-bold">{value.toLocaleDateString("vi-VN", { weekday: "short" })}</span>
                            {value.toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit" })}
                          </button>
                        ); 
                      })}
                    </div>
                  </section>
                  
                  <section>
                    <h2 className="font-bold mb-4">Khung giờ còn trống</h2>
                    {loadingSlots ? <div className="py-10 grid place-items-center"><FaSpinner className="animate-spin text-2xl text-[var(--forest)]" /></div> : slots.length ? (
                      <div className="grid grid-cols-2 gap-3">
                        {slots.map((slot) => (
                          <button key={`${slot.sale_user_id}-${slot.starts_at}`} onClick={() => setSelectedSlot(slot)} className={`p-4 rounded-xl border text-left transition-all duration-200 hover:scale-[1.02] ${selectedSlot?.starts_at === slot.starts_at ? "bg-[#e6eee7] border-[var(--forest)] ring-2 ring-[var(--sage)]/50" : "border-black/10 bg-white"}`}>
                            <span className="block font-bold">{slot.label}</span>
                            <span className="text-xs text-[var(--muted)]">{slot.sale_name}</span>
                          </button>
                        ))}
                      </div>
                    ) : (
                      <div className="bg-[#fbfaf7] p-6 rounded-xl border border-black/5 text-center text-[var(--muted)] flex flex-col items-center">
                        <FaCalendarAlt className="text-3xl mb-2 opacity-50" />
                        <p className="text-sm">Ngày này chưa có khung giờ phù hợp.</p>
                      </div>
                    )}
                  </section>
                </div>
              </div>
            ) : null}

            <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
              <p className="text-sm text-[var(--muted)] flex items-center bg-white px-4 py-2 rounded-lg border border-black/5"><FaClock className="mr-2 text-[var(--coral)]" /> Yêu cầu mới sẽ được chờ xác nhận.</p>
              <button onClick={submit} disabled={!selectedSlot || submitting} className="w-full sm:w-auto bg-[var(--ink)] text-white px-8 py-3.5 rounded-full font-semibold disabled:opacity-50 flex items-center justify-center transition-transform hover:scale-105 active:scale-95">
                {submitting ? "Đang gửi..." : <>Xác nhận dời lịch <FaArrowRight className="ml-2" /></>}
              </button>
            </div>
          </div>
        </main>
        <Footer />
      </div>
    </ProtectedPage>
  );
}

export default function ReschedulePage() {
  return <Suspense fallback={<div className="min-h-screen bg-[var(--paper)] grid place-items-center"><FaSpinner className="animate-spin text-3xl text-[var(--forest)]" /></div>}><RescheduleContent /></Suspense>;
}
