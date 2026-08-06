"use client";
import { useState } from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Link from "next/link";
import { FaCalendarAlt, FaClock, FaMapMarkerAlt, FaUser, FaComment, FaRobot, FaTimesCircle } from "react-icons/fa";

const TABS = ["Sắp tới", "Đang chờ", "Đã hoàn thành", "Đã hủy"];
const MOCK_BOOKINGS = [
  {
    id: "1",
    title: "Vinhomes Central Park - Căn...",
    time: "14:00 - 15:00, T5, 12/10/2024",
    address: "Tháp Landmark 2, 208 Nguyễn Hữu Cảnh",
    agent: "Nguyễn Trần My",
    agentRole: "Sale phụ trách",
    status: "confirmed",
    badge: "Đã xác nhận",
    image: "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=500&q=80",
  },
  {
    id: "2",
    title: "Masteri Thảo Điền - T2 3PN",
    time: "09:30 - 10:15, T7, 14/10/2024",
    address: "Tháp T2, 159 Xa Lộ Hà Nội, Quận 2",
    agent: "Bot Đặt Lịch",
    agentRole: "Đang xử lý",
    status: "holding",
    badge: "Đang giữ căn (12:45)",
    image: "https://images.unsplash.com/photo-1600607687931-ce71171f1e73?auto=format&fit=crop&w=500&q=80",
  },
];

export default function MyBookingsPage() {
  const [activeTab, setActiveTab] = useState("Sắp tới");

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
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {MOCK_BOOKINGS.map((booking) => (
            <div key={booking.id} className="bg-white rounded-2xl overflow-hidden border border-slate-100 shadow-sm hover:shadow-lg transition-all">
              <div className="relative h-48">
                <img src={booking.image} alt={booking.title} className="w-full h-full object-cover" />
                <span className={`absolute top-3 right-3 px-3 py-1 rounded-full text-xs font-bold text-white ${
                  booking.status === "confirmed" ? "bg-green-500" : "bg-orange-500"
                }`}>
                  {booking.badge}
                </span>
              </div>

              <div className="p-5">
                <h3 className="text-lg font-bold text-slate-800 mb-2">{booking.title}</h3>
                <div className="space-y-2 text-sm text-slate-500 mb-4">
                  <div className="flex items-center gap-2"><FaCalendarAlt className="text-teal-500" /> {booking.time}</div>
                  <div className="flex items-center gap-2"><FaMapMarkerAlt className="text-teal-500" /> {booking.address}</div>
                </div>

                <div className="flex items-center gap-3 mb-5 pb-4 border-t border-slate-100 pt-4">
                  <div className={`w-9 h-9 rounded-full flex items-center justify-center ${
                    booking.status === "confirmed" ? "bg-pink-100" : "bg-teal-100"
                  }`}>
                    {booking.status === "confirmed" ? <FaUser className="text-pink-500 text-sm" /> : <FaRobot className="text-teal-500 text-sm" />}
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-slate-800">{booking.agent}</p>
                    <p className="text-xs text-slate-400">{booking.agentRole}</p>
                  </div>
                  {booking.status === "confirmed" && <FaComment className="ml-auto text-teal-500 cursor-pointer" />}
                </div>

                <div className="flex gap-2">
                  <button className="flex-1 bg-white border border-slate-200 text-slate-600 py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-50">
                    Hủy lịch
                  </button>
                  {booking.status === "confirmed" ? (
                    <Link href={`/properties/${booking.id}`} className="flex-1 text-center bg-[#0b132b] text-white py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-800">
                      Chi tiết
                    </Link>
                  ) : (
                    <button className="flex-1 bg-orange-500 text-white py-2.5 rounded-xl text-sm font-semibold hover:bg-orange-600 flex items-center justify-center gap-1">
                      Xác nhận ngay
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>
      <Footer />
    </div>
  );
}
