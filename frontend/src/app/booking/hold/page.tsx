"use client";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Link from "next/link";
import { FaClock, FaCalendarAlt, FaUser, FaMapMarkerAlt, FaCheckCircle, FaSpinner, FaRobot } from "react-icons/fa";

const STEPS = [
  { label: "Đã kiểm tra căn hộ", desc: "Căn hộ khả dụng trong khung giờ bạn chọn.", done: true },
  { label: "Đã giữ căn tạm thời", desc: "Hệ thống đã khóa căn hộ trong 15 phút.", done: true },
  { label: "Đang tìm nhân viên tư vấn", desc: "AI đang phân tích lịch trình của các chuyên viên.", active: true },
  { label: "Chờ xác nhận", desc: "Nhân viên xác nhận lịch hẹn với bạn.", done: false },
  { label: "Hoàn tất", desc: "Lịch hẹn được thiết lập thành công.", done: false },
];

export default function HoldPage() {
  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      <Header />
      <main>
        {/* Hero Banner */}
        <div className="bg-[#0b132b] text-white py-12 text-center">
          <h1 className="text-3xl font-bold mb-3">Căn hộ đang được giữ cho bạn</h1>
          <p className="text-slate-300 max-w-xl mx-auto text-sm">Vui lòng không đóng trang này. Hệ thống đang tiến hành các bước tiếp theo để hoàn tất lịch hẹn của bạn.</p>
        </div>

        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="flex gap-8">
            {/* Left */}
            <div className="flex-1">
              {/* Timer */}
              <div className="bg-white border border-slate-100 rounded-2xl p-8 text-center mb-8 shadow-sm">
                <div className="text-5xl mb-2">⏱️</div>
                <p className="text-6xl font-bold text-orange-500 mb-2">13:42</p>
                <p className="text-sm text-slate-500">Thời gian giữ căn hộ tạm thời. Vui lòng chờ AI tìm nhân viên tư vấn.</p>
              </div>

              {/* Timeline */}
              <h3 className="font-bold text-slate-800 text-lg mb-6 flex items-center gap-2"><FaClock /> Tiến trình đặt lịch</h3>
              <div className="space-y-6 relative">
                <div className="absolute left-4 top-2 bottom-2 w-0.5 bg-slate-200"></div>
                {STEPS.map((step, idx) => (
                  <div key={idx} className="flex items-start gap-4 relative">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 z-10 ${
                      step.done ? "bg-teal-500 text-white" : step.active ? "bg-orange-500 text-white animate-pulse" : "bg-slate-200 text-slate-400"
                    }`}>
                      {step.done ? <FaCheckCircle className="text-sm" /> : step.active ? <FaSpinner className="text-sm animate-spin" /> : <span className="w-2 h-2 bg-slate-400 rounded-full"></span>}
                    </div>
                    <div>
                      <p className={`font-semibold text-sm ${step.active ? "text-orange-600" : step.done ? "text-slate-800" : "text-slate-400"}`}>{step.label}</p>
                      <p className="text-xs text-slate-500">{step.desc}</p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Agent Finding */}
              <div className="mt-8 bg-teal-50 border border-teal-200 rounded-2xl p-5">
                <p className="font-bold text-teal-800 text-sm mb-3 flex items-center gap-2"><FaRobot /> AI đang tìm nhân viên phù hợp</p>
                <p className="text-xs text-teal-700 mb-4">Thuật toán đang quét lịch trình, vị trí và chuyên môn của đội ngũ nhân viên để tìm người phù hợp nhất cho buổi xem nhà của bạn.</p>
                <div className="flex gap-3">
                  <div className="flex items-center gap-2 bg-white rounded-full px-4 py-2">
                    <div className="w-8 h-8 rounded-full bg-pink-200"></div>
                    <div><p className="text-xs font-bold">Nguyễn Thị A</p><p className="text-xs text-slate-400">Đang giữ yêu cầu...</p></div>
                  </div>
                  <div className="flex items-center gap-2 bg-white rounded-full px-4 py-2">
                    <div className="w-8 h-8 rounded-full bg-blue-200"></div>
                    <div><p className="text-xs font-bold">Trần Văn B</p><p className="text-xs text-slate-400">Chỉ phải xử...</p></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Right - Booking Summary */}
            <div className="w-96 shrink-0 hidden lg:block">
              <div className="sticky top-20 bg-white border border-slate-100 rounded-2xl p-6 shadow-sm">
                <h3 className="font-bold text-slate-800 text-lg mb-6">Chi tiết lịch hẹn</h3>
                <div className="flex items-start gap-4 mb-6 pb-6 border-b border-slate-100">
                  <img src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=100&q=80" alt="Property" className="w-16 h-16 rounded-xl object-cover" />
                  <div>
                    <p className="font-bold text-sm">Căn hộ 2PN - The Landmark 81, Vinhomes Central Park</p>
                    <p className="text-xs text-slate-500">Mã căn: L81-24.05</p>
                  </div>
                </div>

                <div className="space-y-4 text-sm">
                  <div className="flex items-start gap-3">
                    <FaClock className="text-teal-500 mt-0.5" />
                    <div><p className="text-slate-500">Thời gian</p><p className="font-bold">15:30 - Thứ Năm, 24/10/2024</p></div>
                  </div>
                  <div className="flex items-start gap-3">
                    <FaUser className="text-teal-500 mt-0.5" />
                    <div><p className="text-slate-500">Người đặt</p><p className="font-bold">Lê Khách Hàng - 0901234567</p></div>
                  </div>
                  <div className="flex items-start gap-3">
                    <FaMapMarkerAlt className="text-teal-500 mt-0.5" />
                    <div><p className="text-slate-500">Địa điểm</p><p className="font-bold">Sảnh L81, 720A Điện Biên Phủ, P.22, Q.Bình Thạnh</p></div>
                  </div>
                </div>

                <Link href="/booking/confirmation" className="block w-full mt-6 bg-[#0b132b] text-white py-3.5 rounded-xl text-sm font-bold text-center hover:bg-slate-800 transition-colors">
                  Tiếp tục chờ
                </Link>
                <button className="w-full mt-3 bg-white border border-red-200 text-red-500 py-3.5 rounded-xl text-sm font-bold hover:bg-red-50 transition-colors">
                  Hủy yêu cầu
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
