"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FaArrowLeft, FaArrowRight, FaClock, FaSpinner } from "react-icons/fa";
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

  useEffect(() => {
    if (!propertyId) return;
    let active = true;
    Promise.all([
      apiFetch<Property>(`/properties/${propertyId}`),
      apiFetch<{ slots: AvailabilitySlot[] }>(`/bookings/availability?property_id=${propertyId}&date=${selectedDate}`),
    ]).then(([propertyData, slotData]) => {
      if (!active) return;
      setProperty(propertyData);
      setSlots(slotData.slots);
      setSelectedSlot(slotData.slots[0] ?? null);
      setError("");
    }).catch((reason: unknown) => {
      if (active) setError(reason instanceof Error ? reason.message : "Không tải được lịch trống");
    }).finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [propertyId, selectedDate]);

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
      setError(reason instanceof Error ? reason.message : "Không thể tạo lịch xem");
    } finally {
      setSubmitting(false);
    }
  };

  if (!propertyId) return <div className="min-h-screen grid place-items-center"><div className="text-center"><p className="text-red-500 mb-4">Thiếu mã bất động sản.</p><Link href="/properties" className="text-teal-700 font-semibold">Chọn bất động sản</Link></div></div>;

  return (
    <ProtectedPage roles={[...CUSTOMER_ROLES]}>
      <main className="min-h-screen bg-gradient-to-br from-cyan-50 via-white to-slate-50 px-4 py-10">
        <div className="max-w-4xl mx-auto">
          <Link href={`/properties/${propertyId}`} className="inline-flex items-center text-slate-500 hover:text-slate-800 text-sm"><FaArrowLeft className="mr-2" /> Quay lại căn hộ</Link>
          <h1 className="text-3xl font-bold text-slate-800 mt-8">Chọn thời gian xem nhà</h1>
          <p className="text-slate-500 mt-2 mb-8">{property?.title ?? "Đang tải thông tin bất động sản..."}</p>
          {error && <div role="alert" className="bg-red-50 border border-red-200 text-red-600 p-4 rounded-xl mb-6">{error}</div>}
          {loading ? <div className="py-20 grid place-items-center"><FaSpinner className="animate-spin text-3xl text-teal-500" /></div> : (
            <div className="grid md:grid-cols-[1.1fr_1fr] gap-8 bg-white p-5 sm:p-8 rounded-3xl border border-slate-100 shadow-sm">
              <section><h2 className="font-bold text-slate-800 mb-4">Chọn ngày</h2><div className="grid grid-cols-2 sm:grid-cols-3 gap-3">{dates.map((value) => { const key = dateKey(value); return <button key={key} onClick={() => { setLoading(true); setSelectedDate(key); }} className={`p-3 rounded-xl border text-sm ${selectedDate === key ? "bg-slate-900 text-white border-slate-900" : "border-slate-200 hover:border-teal-400"}`}><span className="block font-bold">{value.toLocaleDateString("vi-VN", { weekday: "short" })}</span>{value.toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit" })}</button>; })}</div></section>
              <section><h2 className="font-bold text-slate-800 mb-4">Khung giờ còn trống</h2>{slots.length ? <div className="grid grid-cols-2 gap-3">{slots.map((slot) => <button key={`${slot.sale_user_id}-${slot.starts_at}`} onClick={() => setSelectedSlot(slot)} className={`p-4 rounded-xl border text-left ${selectedSlot?.starts_at === slot.starts_at ? "bg-teal-50 border-teal-500 ring-2 ring-teal-200" : "border-slate-200"}`}><span className="block font-bold text-slate-800">{slot.label}</span><span className="text-xs text-slate-500">{slot.sale_name}</span></button>)}</div> : <p className="text-sm text-slate-500 bg-slate-50 p-4 rounded-xl">Ngày này chưa có khung giờ phù hợp.</p>}</section>
            </div>
          )}
          <div className="flex flex-col sm:flex-row gap-4 items-center justify-between mt-8"><p className="text-sm text-slate-500 flex items-center"><FaClock className="mr-2" /> Yêu cầu được giữ 15 phút để sale xác nhận.</p><button onClick={submit} disabled={!selectedSlot || submitting} className="w-full sm:w-auto bg-slate-900 text-white px-8 py-3.5 rounded-full font-semibold disabled:opacity-50 flex items-center justify-center">{submitting ? "Đang tạo yêu cầu..." : <>Tiếp tục <FaArrowRight className="ml-2" /></>}</button></div>
        </div>
      </main>
    </ProtectedPage>
  );
}

export default function SchedulePage() {
  return <Suspense fallback={<div className="min-h-screen grid place-items-center"><FaSpinner className="animate-spin text-3xl text-teal-500" /></div>}><ScheduleContent /></Suspense>;
}
