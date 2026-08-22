"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { FaCalendarAlt, FaMapMarkerAlt, FaRobot, FaSpinner } from "react-icons/fa";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ProtectedPage from "@/components/ProtectedPage";
import PropertyImage from "@/components/PropertyImage";
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
  const [cancellingBooking, setCancellingBooking] = useState<Booking | null>(null);
  const [cancelReason, setCancelReason] = useState("");
  const [isCancelling, setIsCancelling] = useState(false);

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

  const submitCancel = async () => {
    if (!cancellingBooking) return;
    setIsCancelling(true);
    try { 
      await apiFetch(`/bookings/${cancellingBooking.id}/cancel`, { 
        method: "POST", 
        body: JSON.stringify({ reason: cancelReason || "Khách hàng yêu cầu hủy" }) 
      }); 
      setCancellingBooking(null);
      setCancelReason("");
      await load(); 
    }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Không thể hủy lịch"); }
    finally { setIsCancelling(false); }
  };

  return (
    <ProtectedPage roles={[...CUSTOMER_ROLES]}>
      <div className="min-h-screen bg-[var(--paper)] text-[var(--ink)] font-sans">
        <Header />
        <main className="max-w-5xl mx-auto px-4 py-10">
          <h1 className="text-3xl font-bold mb-6">Lịch xem của tôi</h1>
          
          <div className="flex gap-2 mb-8 overflow-x-auto pb-2">
            {TABS.map((item) => (
              <button 
                key={item.key} 
                onClick={() => setActiveTab(item.key)} 
                className={`whitespace-nowrap px-5 py-2.5 rounded-full text-sm font-semibold transition-all duration-200 hover:scale-[1.02] ${activeTab === item.key ? "bg-[var(--ink)] text-white shadow-md" : "bg-white border border-black/10 text-[var(--muted)] hover:border-[var(--sage)]"}`}
              >
                {item.label} ({bookings.filter((booking) => (item.statuses as readonly string[]).includes(booking.status)).length})
              </button>
            ))}
          </div>
          
          {error && <div role="alert" className="bg-red-50 text-red-600 border border-red-200 p-4 rounded-[1.5rem] mb-6 shadow-sm">{error}</div>}
          
          {loading ? (
            <div className="py-24 grid place-items-center"><FaSpinner className="animate-spin text-3xl text-[var(--forest)]" /></div>
          ) : filtered.length === 0 ? (
            <div className="text-center py-20 bg-white rounded-[1.5rem] border border-black/5 shadow-sm">
              <FaCalendarAlt className="text-4xl text-[var(--sage)] opacity-50 mx-auto mb-4" />
              <p className="text-[var(--muted)]">Không có lịch trong nhóm này.</p>
              <Link href="/properties" className="inline-block mt-5 text-[var(--forest)] font-semibold transition-transform hover:scale-105">Khám phá kho nhà</Link>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 gap-6">
              {filtered.map((booking) => (
                <article key={booking.id} className="bg-white rounded-[1.5rem] overflow-hidden border border-black/5 shadow-sm flex flex-col transition-all duration-300 hover:shadow-md hover:-translate-y-1">
                  <div className="h-48 bg-[#e6eee7]">
                    {booking.property.media[0]?.url ? (
                      <PropertyImage src={booking.property.media[0].url} alt={booking.property.title} className="w-full h-full object-cover" />
                    ) : (
                      <div className="w-full h-full grid place-items-center text-5xl">🏠</div>
                    )}
                  </div>
                  <div className="p-6 flex-1 flex flex-col">
                    <div className="flex justify-between items-start gap-3">
                      <h2 className="font-bold text-lg leading-tight line-clamp-2">{booking.property.title}</h2>
                      <span className={`shrink-0 text-xs px-3 py-1.5 rounded-full font-semibold ${booking.status === "BOOKED" ? "bg-emerald-50 text-[var(--forest)]" : booking.status === "WAITING_APPROVAL" ? "bg-amber-50 text-amber-700" : "bg-stone-100 text-[var(--muted)]"}`}>
                        {STATUS_LABEL[booking.status] ?? booking.status}
                      </span>
                    </div>
                    
                    <div className="mt-5 space-y-2.5 text-sm text-[var(--muted)]">
                      <p><FaCalendarAlt className="inline mr-2 text-[var(--forest)]" />{new Date(booking.preferred_start).toLocaleString("vi-VN")}</p>
                      <p className="line-clamp-2"><FaMapMarkerAlt className="inline mr-2 text-[var(--forest)]" />{booking.property.address}</p>
                      {booking.sale && <p><FaRobot className="inline mr-2 text-[var(--forest)]" />Sale: <span className="font-medium text-[var(--ink)]">{booking.sale.full_name}</span></p>}
                    </div>
                    
                    <div className="mt-6 pt-5 border-t border-black/5">
                      <div className="flex gap-2">
                        {booking.status === "BOOKED" ? (
                          <>
                            <Link href={`/booking/confirmation?booking_id=${booking.id}`} className="flex-1 text-center bg-[var(--ink)] text-white py-3 rounded-xl text-sm font-semibold transition-transform hover:scale-[1.02]">Chi tiết</Link>
                            <Link href={`/booking/reschedule?booking_id=${booking.id}`} className="flex-1 text-center bg-white border border-[var(--ink)] text-[var(--ink)] py-3 rounded-xl text-sm font-semibold transition-transform hover:scale-[1.02]">Dời lịch</Link>
                          </>
                        ) : booking.status === "WAITING_APPROVAL" ? (
                          <Link href={`/booking/hold?booking_id=${booking.id}`} className="flex-1 text-center bg-[var(--coral)] text-white py-3 rounded-xl text-sm font-semibold transition-transform hover:scale-[1.02]">Theo dõi</Link>
                        ) : (
                          <Link href={`/properties/${booking.property.id}`} className="flex-1 text-center bg-[#fbfaf7] border border-black/10 text-[var(--ink)] py-3 rounded-xl text-sm font-semibold transition-transform hover:scale-[1.02]">Xem lại căn</Link>
                        )}
                      </div>
                      
                      {!["CANCELLED", "REJECTED", "EXPIRED", "COMPLETED"].includes(booking.status) && (
                        <button onClick={() => setCancellingBooking(booking)} className="w-full mt-3 text-red-500 py-2 rounded-xl text-sm font-semibold hover:bg-red-50 transition-colors">Hủy lịch này</button>
                      )}
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
        </main>

        {cancellingBooking && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4 animate-in fade-in">
            <div className="w-full max-w-md bg-white rounded-3xl shadow-xl overflow-hidden">
              <div className="p-6">
                <h3 className="text-xl font-bold mb-2">Hủy lịch xem nhà</h3>
                <p className="text-sm text-[var(--muted)] mb-5">
                  Bạn đang hủy lịch xem căn <strong className="text-[var(--ink)]">{cancellingBooking.property.title}</strong>.
                </p>
                
                <label className="block text-sm font-semibold mb-2">Lý do hủy</label>
                <div className="flex flex-wrap gap-2 mb-3">
                  {["Tôi có việc bận đột xuất", "Tôi đã tìm được căn khác", "Đổi ý không xem nữa"].map(reason => (
                    <button
                      key={reason}
                      onClick={() => setCancelReason(reason)}
                      className={`px-3 py-1.5 text-xs rounded-full border transition-colors ${cancelReason === reason ? "bg-[var(--coral)] text-white border-[var(--coral)]" : "bg-white text-[var(--muted)] border-black/10 hover:border-black/30"}`}
                    >
                      {reason}
                    </button>
                  ))}
                </div>
                
                <textarea
                  value={cancelReason}
                  onChange={(e) => setCancelReason(e.target.value)}
                  placeholder="Nhập lý do khác..."
                  className="w-full border border-black/10 rounded-xl p-3 text-sm focus:outline-none focus:border-[var(--forest)] resize-none"
                  rows={3}
                />
              </div>
              
              <div className="flex gap-3 p-4 bg-stone-50 border-t border-black/5">
                <button 
                  onClick={() => { setCancellingBooking(null); setCancelReason(""); }}
                  className="flex-1 py-2.5 rounded-xl text-sm font-semibold text-[var(--muted)] hover:bg-black/5 transition-colors"
                >
                  Đóng
                </button>
                <button 
                  disabled={isCancelling}
                  onClick={submitCancel}
                  className="flex-1 py-2.5 rounded-xl text-sm font-semibold bg-red-500 text-white hover:bg-red-600 transition-colors disabled:opacity-50 flex justify-center items-center"
                >
                  {isCancelling ? <FaSpinner className="animate-spin" /> : "Xác nhận hủy"}
                </button>
              </div>
            </div>
          </div>
        )}

        <Footer />
      </div>
    </ProtectedPage>
  );
}
