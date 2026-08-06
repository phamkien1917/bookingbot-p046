"use client";
import Link from "next/link";
import { FaRobot, FaHome, FaCalendarAlt, FaBell, FaUsers, FaQuestionCircle, FaSignOutAlt, FaPlus, FaClock, FaMapMarkerAlt, FaBed, FaPhone, FaCheckCircle, FaTimesCircle, FaChevronLeft, FaChevronRight } from "react-icons/fa";

const SIDEBAR_ITEMS = [
  { icon: <FaHome />, label: "Tổng quan", active: true },
  { icon: <FaBell />, label: "Yêu cầu mới", badge: "2" },
  { icon: <FaCalendarAlt />, label: "Lịch của tôi" },
  { icon: <FaUsers />, label: "Khách hàng" },
];

const REQUESTS = [
  {
    customer: "Trần Thị B",
    phone: "090 123 4567",
    timer: "04:12",
    property: "Căn hộ Vinhome Grand Park - 2PN",
    location: "Quận 9, TP.HCM",
    distance: "2.5 km",
    preferred: "Yêu cầu xem: 14:30 - Hôm nay",
  },
  {
    customer: "Lê Văn C",
    phone: "098 765 4321",
    timer: "12:45",
    property: "Masteri Thảo Điền - 3PN",
    location: "Quận 2, TP.HCM",
    distance: "8.0 km",
    preferred: "Yêu cầu xem: 09:00 - Ngày mai",
  },
];

const SCHEDULE = [
  { time: "08:00", label: "" },
  { time: "09:00", label: "Dẫn khách xem Vinhome Central Park", sub: "08:30 - 09:15 • Anh Hoàng", color: "bg-teal-100 border-teal-300 text-teal-800" },
  { time: "10:00", label: "Hẹn ký hợp đồng cọc", sub: "10:00 - 11:00 • Chị Lan", color: "bg-orange-100 border-orange-300 text-orange-800" },
  { time: "11:00", label: "" },
  { time: "12:00", label: "" },
  { time: "13:00", label: "" },
  { time: "14:00", label: "Dự kiến: Lịch xem Masteri (chưa chốt)", sub: "14:00 - 14:45", color: "bg-slate-100 border-slate-300 text-slate-600" },
  { time: "15:00", label: "" },
];

export default function SaleDashboard() {
  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 flex">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-slate-100 flex flex-col shrink-0">
        <div className="p-6 border-b border-slate-100">
          <div className="flex items-center gap-3">
            <FaRobot className="text-2xl text-teal-500" />
            <div>
              <p className="font-bold text-slate-800">Booking Bot</p>
              <p className="text-xs text-teal-600 font-semibold">Sale</p>
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-1">Nhân viên kinh doanh</p>
        </div>

        <div className="p-4">
          <button className="w-full bg-[#00b4d8] text-white py-3 rounded-xl text-sm font-semibold hover:bg-cyan-600 transition-colors flex items-center justify-center gap-2">
            <FaPlus /> Tạo lịch xem mới
          </button>
        </div>

        <nav className="flex-1 px-3 space-y-1">
          {SIDEBAR_ITEMS.map((item, idx) => (
            <button key={idx} className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors ${
              item.active ? "bg-teal-50 text-teal-700" : "text-slate-500 hover:bg-slate-50"
            }`}>
              {item.icon} {item.label}
              {item.badge && <span className="ml-auto bg-red-500 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">{item.badge}</span>}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-slate-100 space-y-1">
          <button className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-slate-500 hover:bg-slate-50 rounded-xl"><FaQuestionCircle /> Hỗ trợ</button>
          <button className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-red-500 hover:bg-red-50 rounded-xl"><FaSignOutAlt /> Đăng xuất</button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-slate-800">Xin chào, Nguyễn Văn A</h1>
            <p className="text-sm text-slate-500">Hôm nay bạn có 3 yêu cầu xem nhà mới cần xử lý.</p>
          </div>
          <button className="bg-[#0b132b] text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-800 flex items-center gap-2">
            <FaPlus /> Tạo lịch xem mới
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-6 mb-8">
          <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm">
            <div className="flex items-center gap-2 text-sm text-slate-500 mb-1"><FaCalendarAlt className="text-teal-500" /> Yêu cầu mới</div>
            <div className="flex items-baseline gap-2">
              <p className="text-4xl font-bold text-slate-800">12</p>
              <span className="text-xs text-orange-500 font-semibold bg-orange-50 px-2 py-0.5 rounded-full">+2 hôm nay</span>
            </div>
          </div>
          <div className="bg-teal-50 border border-teal-200 rounded-2xl p-6">
            <div className="flex items-center gap-2 text-sm text-teal-600 mb-1"><FaCheckCircle /> Lịch đã xác nhận (Tháng)</div>
            <p className="text-4xl font-bold text-slate-800">28</p>
          </div>
          <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm">
            <div className="flex items-center gap-2 text-sm text-slate-500 mb-1"><FaClock /> Tỷ lệ nhận lịch</div>
            <div className="flex items-baseline gap-2">
              <p className="text-4xl font-bold text-slate-800">85%</p>
              <span className="text-xs text-green-500 font-semibold">+5%</span>
            </div>
            <p className="text-xs text-slate-400">/ mục tiêu 80%</p>
          </div>
        </div>

        <div className="flex gap-8">
          {/* Requests */}
          <div className="flex-1">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-slate-800 flex items-center gap-2"><FaBell /> Yêu cầu mới</h3>
              <span className="text-xs text-slate-400">3 chờ xử lý</span>
            </div>

            <div className="space-y-4">
              {REQUESTS.map((req, idx) => (
                <div key={idx} className="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center text-purple-600 font-bold">{req.customer[0]}</div>
                      <div>
                        <p className="font-bold text-sm text-slate-800">{req.customer}</p>
                        <p className="text-xs text-slate-400">{req.phone}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-red-500">{req.timer}</p>
                      <p className="text-xs text-slate-400">Thời gian còn lại</p>
                    </div>
                  </div>

                  <div className="bg-slate-50 rounded-xl p-4 mb-4">
                    <p className="font-bold text-sm text-slate-800 mb-1 flex items-center gap-1"><FaBed className="text-teal-500" /> {req.property}</p>
                    <p className="text-xs text-slate-500 flex items-center gap-1"><FaMapMarkerAlt /> {req.location}</p>
                    <p className="text-xs text-slate-400 mt-1">🚗 Cách bạn {req.distance}</p>
                  </div>

                  <p className="text-xs text-slate-500 mb-4 flex items-center gap-1"><FaClock className="text-teal-500" /> {req.preferred}</p>

                  <div className="flex gap-2">
                    <button className="flex-1 bg-white border border-slate-200 text-slate-600 py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-50">Từ chối</button>
                    <button className="flex-1 bg-[#00b4d8] text-white py-2.5 rounded-xl text-sm font-semibold hover:bg-cyan-600 transition-colors">Nhận lịch</button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Calendar */}
          <div className="w-96 shrink-0">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-slate-800">Lịch làm việc của tôi</h3>
              <div className="flex items-center gap-2 text-sm text-slate-600">
                <FaChevronLeft className="cursor-pointer hover:text-slate-800" />
                <span>Hôm nay, 15 Thg 11</span>
                <FaChevronRight className="cursor-pointer hover:text-slate-800" />
              </div>
            </div>

            <div className="bg-white border border-slate-100 rounded-2xl shadow-sm overflow-hidden">
              {SCHEDULE.map((slot, idx) => (
                <div key={idx} className="flex border-b border-slate-50 last:border-0">
                  <div className="w-16 py-3 px-3 text-xs text-slate-400 text-right shrink-0 border-r border-slate-100">{slot.time}</div>
                  <div className="flex-1 py-2 px-3 min-h-[48px]">
                    {slot.label && (
                      <div className={`${slot.color} border rounded-lg px-3 py-2 text-xs font-medium`}>
                        <p className="font-semibold">{slot.label}</p>
                        <p className="opacity-70">{slot.sub}</p>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
