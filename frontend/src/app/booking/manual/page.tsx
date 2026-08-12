"use client";

import { FormEvent, Suspense, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FaArrowLeft, FaCalendarAlt, FaSpinner } from "react-icons/fa";
import ProtectedPage from "@/components/ProtectedPage";
import { useAuth } from "@/components/AuthProvider";
import { apiFetch } from "@/lib/api";
import type { AvailabilitySlot, Booking, Property } from "@/lib/types";

function dateKey(value: Date) {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, "0");
  const day = String(value.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function ManualBookingContent() {
  const { user } = useAuth();
  const router = useRouter();
  const params = useSearchParams();
  const initialPropertyId = params.get("property_id") ?? "";
  const tomorrow = useMemo(() => { const value = new Date(); value.setDate(value.getDate() + 1); return dateKey(value); }, []);
  const [properties, setProperties] = useState<Property[]>([]);
  const [propertyId, setPropertyId] = useState(initialPropertyId);
  const [date, setDate] = useState(tomorrow);
  const [slots, setSlots] = useState<AvailabilitySlot[]>([]);
  const [slot, setSlot] = useState<AvailabilitySlot | null>(null);
  const [partySize, setPartySize] = useState(1);
  const [note, setNote] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const timer = window.setTimeout(async () => {
      try {
        const data = await apiFetch<{ items: Property[] }>("/properties?limit=100");
        setProperties(data.items);
        if (!initialPropertyId && data.items[0]) setPropertyId(data.items[0].id);
      } catch (reason) {
        setError(reason instanceof Error ? reason.message : "Không tải được danh sách bất động sản");
      } finally { setLoading(false); }
    }, 0);
    return () => window.clearTimeout(timer);
  }, [initialPropertyId]);

  useEffect(() => {
    if (!propertyId || !date) return;
    let active = true;
    const timer = window.setTimeout(() => {
      setLoading(true);
      setError("");
      void apiFetch<{ slots: AvailabilitySlot[] }>(`/bookings/availability?property_id=${propertyId}&date=${date}`)
        .then((data) => { if (active) { setSlots(data.slots); setSlot(data.slots[0] ?? null); } })
        .catch((reason: unknown) => { if (active) { setSlots([]); setSlot(null); setError(reason instanceof Error ? reason.message : "Không kiểm tra được lịch trống"); } })
        .finally(() => { if (active) setLoading(false); });
    }, 0);
    return () => { active = false; window.clearTimeout(timer); };
  }, [date, propertyId]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!propertyId || !slot) return;
    setSubmitting(true); setError("");
    try {
      const booking = await apiFetch<Booking>("/bookings", {
        method: "POST",
        body: JSON.stringify({
          property_id: propertyId,
          sale_user_id: slot.sale_user_id,
          preferred_start: slot.starts_at,
          preferred_end: slot.ends_at,
          pax_count: partySize,
          customer_note: note.trim() || null,
        }),
      });
      router.push(`/booking/hold?booking_id=${booking.id}`);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Không gửi được yêu cầu đặt lịch");
    } finally { setSubmitting(false); }
  }

  return <ProtectedPage roles={["CUSTOMER"]}><main className="min-h-screen bg-slate-50 px-4 py-10"><div className="mx-auto max-w-3xl"><Link href="/chat" className="inline-flex items-center text-sm text-slate-500 hover:text-slate-800"><FaArrowLeft className="mr-2"/>Quay lại chatbot</Link><div className="mt-6 rounded-3xl border border-slate-100 bg-white p-6 shadow-sm sm:p-9"><div className="mb-7 flex items-start gap-4"><span className="rounded-2xl bg-teal-50 p-3 text-2xl text-teal-600"><FaCalendarAlt/></span><div><h1 className="text-2xl font-bold text-slate-800">Đặt lịch xem nhà thủ công</h1><p className="mt-1 text-sm text-slate-500">Form này gửi trực tiếp cho Sale, không phụ thuộc chatbot hay AI Agent.</p></div></div>{error && <div role="alert" className="mb-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}<form onSubmit={submit} className="space-y-5"><div className="grid gap-4 sm:grid-cols-2"><label className="text-sm font-medium text-slate-700">Họ tên<input disabled value={user?.full_name ?? ""} className="mt-1 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-500"/></label><label className="text-sm font-medium text-slate-700">Liên hệ<input disabled value={user?.phone || user?.email || ""} className="mt-1 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-500"/></label></div><label className="block text-sm font-medium text-slate-700">Bất động sản<select required value={propertyId} onChange={(event)=>setPropertyId(event.target.value)} className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-4 py-3"><option value="">Chọn bất động sản</option>{properties.map((property)=><option key={property.id} value={property.id}>{property.title} — {property.district || property.province}</option>)}</select></label><div className="grid gap-4 sm:grid-cols-2"><label className="text-sm font-medium text-slate-700">Ngày xem<input required type="date" min={tomorrow} value={date} onChange={(event)=>setDate(event.target.value)} className="mt-1 w-full rounded-xl border border-slate-200 px-4 py-3"/></label><label className="text-sm font-medium text-slate-700">Số người<input required type="number" min={1} max={20} value={partySize} onChange={(event)=>setPartySize(Number(event.target.value))} className="mt-1 w-full rounded-xl border border-slate-200 px-4 py-3"/></label></div><fieldset><legend className="mb-2 text-sm font-medium text-slate-700">Khung giờ và Sale phụ trách</legend>{loading ? <div className="grid place-items-center rounded-xl bg-slate-50 p-8"><FaSpinner className="animate-spin text-2xl text-teal-500"/></div> : slots.length ? <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">{slots.map((item)=><button key={`${item.sale_user_id}-${item.starts_at}`} type="button" onClick={()=>setSlot(item)} className={`rounded-xl border p-3 text-left ${slot?.starts_at===item.starts_at ? "border-teal-500 bg-teal-50 ring-2 ring-teal-100" : "border-slate-200"}`}><span className="block font-bold">{item.label}</span><span className="text-xs text-slate-500">{item.sale_name}</span></button>)}</div> : <p className="rounded-xl bg-orange-50 p-4 text-sm text-orange-700">Ngày này không còn lịch trống, hãy chọn ngày khác.</p>}</fieldset><label className="block text-sm font-medium text-slate-700">Ghi chú cho Sale<textarea value={note} onChange={(event)=>setNote(event.target.value)} maxLength={1000} rows={4} placeholder="Ví dụ: Tôi muốn xem kỹ pháp lý, đi cùng 2 người…" className="mt-1 w-full resize-none rounded-xl border border-slate-200 px-4 py-3"/></label><button disabled={!slot || loading || submitting} className="w-full rounded-xl bg-slate-900 py-3.5 font-bold text-white disabled:opacity-40">{submitting ? "Đang gửi yêu cầu…" : "Gửi yêu cầu cho Sale"}</button></form></div></div></main></ProtectedPage>;
}

export default function ManualBookingPage() {
  return <Suspense fallback={<div className="min-h-screen grid place-items-center"><FaSpinner className="animate-spin text-3xl text-teal-500"/></div>}><ManualBookingContent/></Suspense>;
}
