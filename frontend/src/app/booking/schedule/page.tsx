"use client";

import { Suspense, useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FaArrowLeft, FaArrowRight, FaClock, FaSpinner, FaCalendarAlt } from "react-icons/fa";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ProtectedPage from "@/components/ProtectedPage";
import { apiFetch } from "@/lib/api";
import type { AvailabilitySlot, Booking, Property } from "@/lib/types";

const CUSTOMER_ROLES = ["CUSTOMER"] as const;

function dateKey(value: Date) {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, "0");
  const day = String(value.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function ScheduleContent() {
  const params = useSearchParams();
  const router = useRouter();
  const propertyId = params.get("property_id");
  const dates = useMemo(() => Array.from({ length: 7 }, (_, index) => { const value = new Date(); value.setDate(value.getDate() + index + 1); return value; }), []);
  const [selectedDate, setSelectedDate] = useState(dateKey(dates[0]));
  const [property, setProperty] = useState<Property | null>(null);
  const [slots, setSlots] = useState<AvailabilitySlot[]>([]);
  const [selectedSlot, setSelectedSlot] = useState<AvailabilitySlot | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const fetchSlots = useCallback(async (quiet = false) => {
    if (!propertyId) return;
    if (!quiet) setLoading(true);
    try {
      const [propertyData, slotData] = await Promise.all([
        apiFetch<Property>(`/properties/${propertyId}`),
        apiFetch<{ slots: AvailabilitySlot[] }>(`/bookings/availability?property_id=${propertyId}&date=${selectedDate}`),
      ]);
      setProperty(propertyData);
      setSlots(slotData.slots);
      
      // Keep selected slot if still available, else pick first
      setSelectedSlot((prev) => {
        const stillAvailable = slotData.slots.find(s => s.starts_at === prev?.starts_at && s.sale_user_id === prev?.sale_user_id);
        return stillAvailable ?? slotData.slots[0] ?? null;
      });
      if (!quiet) setError("");
    } catch (reason: unknown) {
      if (!quiet) setError(reason instanceof Error ? reason.message : "Không tải được lịch trống");
    } finally {
      if (!quiet) setLoading(false);
    }
  }, [propertyId, selectedDate]);

  useEffect(() => {
    fetchSlots();
  }, [fetchSlots]);

  const submit = async () => {
    if (!propertyId || !selectedSlot) return;
    setSubmitting(true);
    setError("");
    try {
      const booking = await apiFetch<Booking>("/bookings", {
        method: "POST",
        body: JSON.stringify({
          property_id: propertyId,
          sale_user_id: selectedSlot.sale_user_id,
          preferred_start: selectedSlot.starts_at,
          preferred_end: selectedSlot.ends_at,
          pax_count: 1,
        }),
      });
      router.push(`/booking/hold?booking_id=${booking.id}`);
    } catch (reason) {
      const msg = reason instanceof Error ? reason.message : "Không thể tạo lịch xem";
      setError(msg);
      if (msg.includes("vui lòng chọn giờ khác")) {
        setSelectedSlot(null);
        void fetchSlots(true);
      }
    } finally {
      setSubmitting(false);
    }
  };

  if (!propertyId) return <div className="min-h-screen bg-[var(--paper)] grid place-items-center"><div className="text-center"><p className="text-[var(--coral)] mb-4">Thiếu mã bất động sản.</p><Link href="/properties" className="text-[var(--forest)] font-semibold">Chọn bất động sản</Link></div></div>;

  return (
    <ProtectedPage roles={[...CUSTOMER_ROLES]}>
      <div className="min-h-screen bg-[var(--paper)] text-[var(--ink)] font-sans">
        <Header />
        <main className="px-4 py-10">
          <div className="max-w-4xl mx-auto">
            <Link href={`/properties/${propertyId}`} className="inline-flex items-center text-[var(--muted)] hover:text-[var(--ink)] text-sm transition-colors"><FaArrowLeft className="mr-2" /> Quay lại căn hộ</Link>
            <h1 className="text-3xl font-bold mt-8">Chọn thời gian xem nhà</h1>
            <p className="text-[var(--muted)] mt-2 mb-8">{property?.title ?? "Đang tải thông tin bất động sản..."}</p>
            
            {error && <div role="alert" className="bg-red-50 border border-red-200 text-red-600 p-4 rounded-[1.5rem] mb-6 shadow-sm">{error}</div>}
            
            {loading ? <div className="py-20 grid place-items-center"><FaSpinner className="animate-spin text-3xl text-[var(--forest)]" /></div> : (
              <div className="grid md:grid-cols-[1.1fr_1fr] gap-8 bg-white p-6 sm:p-8 rounded-[1.5rem] border border-black/5 shadow-sm">
                <section>
                  <h2 className="font-bold mb-4">Chọn ngày</h2>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                    {dates.map((value) => { 
                      const key = dateKey(value); 
                      return (
                        <button key={key} onClick={() => { setLoading(true); setSelectedDate(key); }} className={`p-3 rounded-xl border text-sm transition-all duration-200 hover:scale-[1.02] ${selectedDate === key ? "bg-[var(--forest)] text-white border-[var(--forest)] shadow-md" : "border-black/10 bg-[#fbfaf7] hover:border-[var(--sage)]"}`}>
                          <span className="block font-bold">{value.toLocaleDateString("vi-VN", { weekday: "short" })}</span>
                          {value.toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit" })}
                        </button>
                      ); 
                    })}
                  </div>
                </section>
                
                <section>
                  <h2 className="font-bold mb-4">Khung giờ còn trống</h2>
                  {slots.length ? (
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
            )}
            
            <div className="flex flex-col sm:flex-row gap-4 items-center justify-between mt-8">
              <p className="text-sm text-[var(--muted)] flex items-center bg-white px-4 py-2 rounded-lg border border-black/5"><FaClock className="mr-2 text-[var(--coral)]" /> Yêu cầu được giữ 15 phút để sale xác nhận.</p>
              <button onClick={submit} disabled={!selectedSlot || submitting} className="w-full sm:w-auto bg-[var(--ink)] text-white px-8 py-3.5 rounded-full font-semibold disabled:opacity-50 flex items-center justify-center transition-transform hover:scale-105 active:scale-95">
                {submitting ? "Đang tạo yêu cầu..." : <>Tiếp tục <FaArrowRight className="ml-2" /></>}
              </button>
            </div>
          </div>
        </main>
        <Footer />
      </div>
    </ProtectedPage>
  );
}

export default function SchedulePage() {
  return <Suspense fallback={<div className="min-h-screen bg-[var(--paper)] grid place-items-center"><FaSpinner className="animate-spin text-3xl text-[var(--forest)]" /></div>}><ScheduleContent /></Suspense>;
}
