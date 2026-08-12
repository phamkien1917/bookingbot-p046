/* eslint-disable @next/next/no-img-element */
"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { FaCalendarAlt, FaMapMarkerAlt, FaRobot, FaSpinner } from "react-icons/fa";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ProtectedPage from "@/components/ProtectedPage";
import { apiFetch } from "@/lib/api";
import type { Booking } from "@/lib/types";

const CUSTOMER_ROLES = ["CUSTOMER"] as const;
const TABS = [
  { key: "UPCOMING", label: "Sắp tới", statuses: ["BOOKED"] },
  { key: "PENDING", label: "Đang chờ", statuses: ["WAITING_APPROVAL", "DRAFT"] },
  { key: "DONE", label: "Đã hoàn thành", statuses: ["COMPLETED"] },
  { key: "CANCELLED", label: "Đã hủy", statuses: ["CANCELLED", "REJECTED", "EXPIRED"] },
] as const;

const STATUS_LABEL: Record<string, string> = {
  BOOKED: "Đã xác nhận", WAITING_APPROVAL: "Chờ sale", DRAFT: "Bản nháp", COMPLETED: "Hoàn thành", CANCELLED: "Đã hủy", REJECTED: "Sale từ chối", EXPIRED: "Hết hạn",
};

export default function MyBookingsPage() {
  const [activeTab, setActiveTab] = useState<(typeof TABS)[number]["key"]>("UPCOMING");
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    try { setBookings(await apiFetch<Booking[]>("/bookings/my")); setError(""); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Không tải được lịch xem"); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);
  const tab = TABS.find((item) => item.key === activeTab) ?? TABS[0];
  const filtered = useMemo(() => bookings.filter((booking) => (tab.statuses as readonly string[]).includes(booking.status)), [bookings, tab.statuses]);

  const cancel = async (booking: Booking) => {
    if (!window.confirm(`Hủy yêu cầu ${booking.request_code}?`)) return;
    try { await apiFetch(`/bookings/${booking.id}/cancel`, { method: "POST", body: JSON.stringify({ reason: "Khách hàng hủy từ danh sách" }) }); await load(); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Không thể hủy lịch"); }
  };

  return (
    <ProtectedPage roles={[...CUSTOMER_ROLES]}>
      <div className="min-h-screen bg-slate-50 text-slate-900"><Header /><main className="max-w-5xl mx-auto px-4 py-10"><h1 className="text-3xl font-bold text-slate-800 mb-6">Lịch xem của tôi</h1>
        <div className="flex gap-2 mb-8 overflow-x-auto pb-2">{TABS.map((item) => <button key={item.key} onClick={() => setActiveTab(item.key)} className={`whitespace-nowrap px-5 py-2 rounded-full text-sm font-semibold ${activeTab === item.key ? "bg-slate-900 text-white" : "bg-white border border-slate-200 text-slate-600"}`}>{item.label} ({bookings.filter((booking) => (item.statuses as readonly string[]).includes(booking.status)).length})</button>)}</div>
        {error && <div role="alert" className="bg-red-50 text-red-600 border border-red-200 p-4 rounded-xl mb-6">{error}</div>}
        {loading ? <div className="py-24 grid place-items-center"><FaSpinner className="animate-spin text-3xl text-teal-500" /></div> : filtered.length === 0 ? <div className="text-center py-20 bg-white rounded-3xl border border-slate-100"><FaCalendarAlt className="text-4xl text-slate-300 mx-auto mb-4" /><p className="text-slate-500">Không có lịch trong nhóm này.</p><Link href="/properties" className="inline-block mt-5 text-teal-700 font-semibold">Khám phá bất động sản</Link></div> : <div className="grid md:grid-cols-2 gap-6">{filtered.map((booking) => <article key={booking.id} className="bg-white rounded-2xl overflow-hidden border border-slate-100 shadow-sm flex flex-col"><div className="h-44 bg-slate-100">{booking.property.media[0]?.url ? <img src={booking.property.media[0].url} alt={booking.property.title} className="w-full h-full object-cover" /> : <div className="w-full h-full grid place-items-center text-4xl">🏠</div>}</div><div className="p-5 flex-1 flex flex-col"><div className="flex justify-between gap-3"><h2 className="font-bold text-slate-800 line-clamp-2">{booking.property.title}</h2><span className="shrink-0 text-xs bg-teal-50 text-teal-700 px-2 py-1 rounded-full h-fit">{STATUS_LABEL[booking.status] ?? booking.status}</span></div><div className="mt-4 space-y-2 text-sm text-slate-500"><p><FaCalendarAlt className="inline mr-2 text-teal-500" />{new Date(booking.preferred_start).toLocaleString("vi-VN")}</p><p className="line-clamp-2"><FaMapMarkerAlt className="inline mr-2 text-teal-500" />{booking.property.address}</p>{booking.sale && <p><FaRobot className="inline mr-2 text-teal-500" />Sale: {booking.sale.full_name}</p>}</div><div className="flex gap-2 mt-6 pt-4 border-t border-slate-100">{!["CANCELLED", "REJECTED", "EXPIRED", "COMPLETED"].includes(booking.status) && <button onClick={() => cancel(booking)} className="flex-1 border border-red-200 text-red-500 py-2.5 rounded-xl text-sm font-semibold">Hủy lịch</button>}{booking.status === "BOOKED" ? <Link href={`/booking/confirmation?booking_id=${booking.id}`} className="flex-1 text-center bg-slate-900 text-white py-2.5 rounded-xl text-sm font-semibold">Chi tiết</Link> : booking.status === "WAITING_APPROVAL" ? <Link href={`/booking/hold?booking_id=${booking.id}`} className="flex-1 text-center bg-orange-500 text-white py-2.5 rounded-xl text-sm font-semibold">Theo dõi</Link> : <Link href={`/properties/${booking.property.id}`} className="flex-1 text-center bg-slate-100 text-slate-700 py-2.5 rounded-xl text-sm font-semibold">Xem căn</Link>}</div></div></article>)}</div>}
      </main><Footer /></div>
    </ProtectedPage>
  );
}
