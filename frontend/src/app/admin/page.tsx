"use client";
import Link from "next/link";
import { FaRobot, FaHome, FaCalendarAlt, FaBuilding, FaUsers, FaCog, FaQuestionCircle, FaSignOutAlt, FaPlus, FaChartLine, FaClock, FaExclamationTriangle, FaCheckCircle, FaSearch, FaEye } from "react-icons/fa";

const SIDEBAR_ITEMS = [
  { icon: <FaHome />, label: "Tổng quan", active: true },
  { icon: <FaCalendarAlt />, label: "Lịch đặt chỗ" },
  { icon: <FaBuilding />, label: "Quản lý căn hộ" },
  { icon: <FaUsers />, label: "Khách hàng" },
  { icon: <FaCog />, label: "Cài đặt" },
];

const RECENT_BOOKINGS = [
  { id: "#BK-9284", customer: "Nguyễn Văn A", phone: "0901234567", property: "Apothecary 3BR - Tầng 12", sale: "Trần Thị B", status: "Mới tạo" },
  { id: "#BK-9283", customer: "Lê Hoàng C", phone: "0987654321", property: "Botanica 2BR - Tầng 05", sale: "Chưa gán", status: "Đã xác nhận" },
  { id: "#BK-9281", customer: "Phạm Thị D", phone: "", property: "Zen Studio - Tầng 22", sale: "Lê Văn H", status: "Hết hạn giữ" },
];

export default function AdminDashboard() {
  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 flex">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-slate-100 flex flex-col shrink-0">
        <div className="p-6 border-b border-slate-100">
          <div className="flex items-center gap-3">
            <FaRobot className="text-2xl text-teal-500" />
            <div>
              <p className="font-bold text-slate-800">Booking Bot</p>
              <p className="text-xs text-slate-400">Admin</p>
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-1">Quản trị hệ thống</p>
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
            <h1 className="text-2xl font-bold text-slate-800">Dashboard Quản trị</h1>
            <p className="text-sm text-slate-500">Tổng quan hiệu suất hoạt động hệ thống hôm nay.</p>
          </div>
          <div className="relative">
            <FaSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm" />
            <input type="text" placeholder="Tìm kiếm nhanh..." className="pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 text-sm w-64 outline-none focus:ring-2 focus:ring-teal-400/50" />
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-4 gap-6 mb-8">
          {[
            { label: "Tổng booking (Tháng)", value: "1,248", change: "+12.5% so với tháng trước", color: "text-green-600", icon: <FaCalendarAlt className="text-teal-500" /> },
            { label: "Booking chờ xử lý", value: "45", change: "Cần xác nhận trong 2h tới", color: "text-orange-600", icon: <FaClock className="text-orange-500" /> },
            { label: "Tỷ lệ hết hạn giữ căn", value: "8.2%", change: "-2.1% so với tuần trước", color: "text-red-600", icon: <FaExclamationTriangle className="text-red-500" /> },
            { label: "Hiệu suất Sale", value: "85%", change: "Tỷ lệ chốt deal trung bình", color: "text-teal-600", icon: <FaChartLine className="text-teal-500" /> },
          ].map((stat, idx) => (
            <div key={idx} className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-3">
                <p className="text-sm text-slate-500">{stat.label}</p>
                <span className="text-2xl">{stat.icon}</span>
              </div>
              <p className="text-3xl font-bold text-slate-800 mb-1">{stat.value}</p>
              <p className={`text-xs ${stat.color}`}>{stat.change}</p>
            </div>
          ))}
        </div>

        {/* Charts Placeholder */}
        <div className="grid grid-cols-3 gap-6 mb-8">
          <div className="col-span-2 bg-white border border-slate-100 rounded-2xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-slate-800">Số lượng booking theo ngày</h3>
              <select className="text-sm border border-slate-200 rounded-lg px-3 py-1.5"><option>7 ngày qua</option></select>
            </div>
            <div className="h-48 bg-slate-50 rounded-xl flex items-center justify-center text-slate-400">
              [Placeholder Biểu đồ Đường - Số lượng Booking]
            </div>
          </div>
          <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm">
            <h3 className="font-bold text-slate-800 mb-4">Tỷ lệ Trạng thái</h3>
            <div className="h-32 flex items-center justify-center text-slate-400 mb-4">
              [Biểu đồ Tròn]
            </div>
            <div className="space-y-2 text-xs">
              <div className="flex items-center gap-2"><span className="w-3 h-3 bg-teal-500 rounded-full"></span> Mới / Chờ xử lý <span className="ml-auto font-bold">45%</span></div>
              <div className="flex items-center gap-2"><span className="w-3 h-3 bg-green-500 rounded-full"></span> Đã xác nhận <span className="ml-auto font-bold">35%</span></div>
              <div className="flex items-center gap-2"><span className="w-3 h-3 bg-red-400 rounded-full"></span> Hủy / Hết hạn <span className="ml-auto font-bold">20%</span></div>
            </div>
          </div>
        </div>

        {/* Recent Bookings Table */}
        <div className="bg-white border border-slate-100 rounded-2xl shadow-sm overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-100">
            <h3 className="font-bold text-slate-800">Quản lý Booking Gần Đây</h3>
          </div>
          <table className="w-full">
            <thead className="bg-slate-50 text-xs text-slate-500 uppercase tracking-wider">
              <tr>
                <th className="text-left px-6 py-3">ID</th>
                <th className="text-left px-6 py-3">Khách hàng</th>
                <th className="text-left px-6 py-3">Căn hộ</th>
                <th className="text-left px-6 py-3">Sale phụ trách</th>
                <th className="text-left px-6 py-3">Trạng thái</th>
                <th className="text-left px-6 py-3">Hành động</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {RECENT_BOOKINGS.map((b, idx) => (
                <tr key={idx} className="hover:bg-slate-50">
                  <td className="px-6 py-4 text-sm font-mono font-bold text-slate-800">{b.id}</td>
                  <td className="px-6 py-4 text-sm"><p className="font-semibold">{b.customer}</p><p className="text-xs text-slate-400">{b.phone}</p></td>
                  <td className="px-6 py-4 text-sm text-slate-600">{b.property}</td>
                  <td className="px-6 py-4 text-sm">{b.sale !== "Chưa gán" ? <span className="flex items-center gap-2"><span className="w-6 h-6 rounded-full bg-pink-100"></span>{b.sale}</span> : <span className="text-slate-400">{b.sale}</span>}</td>
                  <td className="px-6 py-4"><span className={`px-3 py-1 rounded-full text-xs font-bold ${
                    b.status === "Mới tạo" ? "bg-blue-100 text-blue-700" : b.status === "Đã xác nhận" ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
                  }`}>{b.status}</span></td>
                  <td className="px-6 py-4">
                    <button className="text-xs bg-[#0b132b] text-white px-4 py-1.5 rounded-lg font-semibold hover:bg-slate-800">
                      {b.status === "Mới tạo" ? <><FaEye className="inline mr-1" />Xem</> : b.status === "Đã xác nhận" ? "Gán AI" : "Gán AI"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="px-6 py-3 text-xs text-slate-400 border-t border-slate-100">Hiển thị 1-10 trong số 138 kết quả</div>
        </div>
      </div>
    </div>
  );
}
