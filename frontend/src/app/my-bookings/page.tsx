"use client";
import { useState, useEffect } from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Link from "next/link";
import { FaCalendarAlt, FaClock, FaMapMarkerAlt, FaUser, FaComment, FaRobot, FaTimesCircle } from "react-icons/fa";

const TABS = ["Sắp tới", "Đang chờ", "Đã hoàn thành", "Đã hủy"];
// Removed MOCK_BOOKINGS


const API_BASE = "http://localhost:8000/api/v1";

export default function MyBookingsPage() {
  const [activeTab, setActiveTab] = useState("Sắp tới");
  const [bookings, setBookings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBookings = async () => {
      const token = localStorage.getItem("access_token");
      if (!token) {
        setLoading(false);
        return;
      }
      try {
        const res = await fetch(`${API_BASE}/bookings/my`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          const bookingsWithProps = await Promise.all(data.map(async (b: any) => {
            const propRes = await fetch(`${API_BASE}/properties/${b.property_id}`);
            const prop = propRes.ok ? await propRes.json() : null;
            return { ...b, property: prop };
          }));
          setBookings(bookingsWithProps);
        }
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchBookings();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      <Header />
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <h1 className="text-3xl font-bold italic text-slate-800 mb-6">Lịch xem của tôi</h1>

        {/* Tabs */}
        <div className="flex gap-2 mb-8">
          {TABS.map((tab) => (
            <button key={tab} onClick={() => setActiveTab(tab)}
              className={`px-5 py-2 rounded-full text-sm font-semibold transition-colors ${
                activeTab === tab ? "bg-[#0b132b] text-white" : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-50"
              }`}>
              {tab}
            </button>
          ))}
        </div>

        {/* Booking Cards */}
        {loading ? (
          <div className="text-center py-20 text-slate-500">Đang tải dữ liệu...</div>
        ) : bookings.length === 0 ? (
          <div className="text-center py-20 text-slate-500">Bạn chưa có lịch xem nhà nào.</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {bookings.map((booking) => (
              <div key={booking.id} className="bg-white rounded-2xl overflow-hidden border border-slate-100 shadow-sm hover:shadow-lg transition-all flex flex-col">
                <div className="relative h-48 bg-slate-200">
                  {booking.property?.media && booking.property.media.length > 0 ? (
                    <img src={booking.property.media[0].url} alt={booking.property?.title || "Property"} className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-4xl">🏠</div>
                  )}
                  <span className={`absolute top-3 right-3 px-3 py-1 rounded-full text-xs font-bold text-white ${
                    booking.status === "CONFIRMED" ? "bg-green-500" : "bg-orange-500"
                  }`}>
                    {booking.status}
                  </span>
                </div>

                <div className="p-5 flex flex-col flex-1">
                  <h3 className="text-lg font-bold text-slate-800 mb-2 line-clamp-1">{booking.property?.title || "Không rõ tên nhà"}</h3>
                  <div className="space-y-2 text-sm text-slate-500 mb-4">
                    <div className="flex items-center gap-2"><FaCalendarAlt className="text-teal-500 shrink-0" /> 
                      {booking.preferred_start ? new Date(booking.preferred_start).toLocaleString('vi-VN') : "Chưa có giờ cụ thể"}
                    </div>
                    <div className="flex items-center gap-2"><FaMapMarkerAlt className="text-teal-500 shrink-0" /> 
                      <span className="line-clamp-1">{booking.property?.address_full || "Chưa có địa chỉ"}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 mb-5 pb-4 border-t border-slate-100 pt-4 mt-auto">
                    <div className="w-9 h-9 rounded-full flex items-center justify-center bg-teal-100">
                      <FaRobot className="text-teal-500 text-sm" />
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-slate-800">Booking Bot</p>
                      <p className="text-xs text-slate-400">Trợ lý ảo xử lý</p>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <button className="flex-1 bg-white border border-slate-200 text-slate-600 py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-50">
                      Hủy lịch
                    </button>
                    {booking.status === "CONFIRMED" ? (
                      <Link href={`/properties/${booking.property_id}`} className="flex-1 text-center bg-[#0b132b] text-white py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-800">
                        Chi tiết
                      </Link>
                    ) : (
                      <Link href="/booking/confirmation" className="flex-1 bg-orange-500 text-white py-2.5 rounded-xl text-sm font-semibold hover:bg-orange-600 flex items-center justify-center gap-1">
                        Xác nhận ngay
                      </Link>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}
