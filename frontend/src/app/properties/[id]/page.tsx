"use client";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Link from "next/link";
import { FaMapMarkerAlt, FaBed, FaBath, FaRulerCombined, FaSwimmingPool, FaDumbbell, FaParking, FaShieldAlt, FaTree, FaShoppingCart, FaRobot, FaComments, FaCalendarAlt, FaClock } from "react-icons/fa";

export default function PropertyDetail() {
  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Image Gallery */}
        <div className="grid grid-cols-3 gap-4 mb-8 h-[400px]">
          <div className="col-span-2 rounded-2xl overflow-hidden">
            <img src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80" alt="Main" className="w-full h-full object-cover" />
          </div>
          <div className="flex flex-col gap-4">
            <div className="flex-1 rounded-2xl overflow-hidden">
              <img src="https://images.unsplash.com/photo-1600607687931-ce71171f1e73?auto=format&fit=crop&w=600&q=80" alt="Sub1" className="w-full h-full object-cover" />
            </div>
            <div className="flex-1 rounded-2xl overflow-hidden">
              <img src="https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=600&q=80" alt="Sub2" className="w-full h-full object-cover" />
            </div>
          </div>
        </div>

        {/* Badges */}
        <div className="flex gap-3 mb-4">
          <span className="px-4 py-1.5 bg-teal-100 text-teal-700 rounded-full text-xs font-bold">Đang có sẵn</span>
          <span className="px-4 py-1.5 bg-blue-100 text-blue-700 rounded-full text-xs font-bold">Đã xác minh</span>
          <span className="text-sm text-slate-500 ml-auto">Mã căn: #VH-CP-204</span>
        </div>

        <div className="flex gap-8">
          {/* Left Content */}
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-slate-800 mb-2">Căn hộ cao cấp Vinhomes Central Park</h1>
            <div className="flex items-center text-slate-500 text-sm mb-4">
              <FaMapMarkerAlt className="mr-2" /> 208 Nguyễn Hữu Cảnh, Phường 22, Bình Thạnh, TP.HCM
            </div>
            <p className="text-3xl font-bold text-[#0b132b] mb-6">4.5 Tỷ <span className="text-base font-normal text-slate-400">VNĐ</span></p>

            {/* Specs */}
            <div className="flex gap-8 mb-8 pb-8 border-b border-slate-200">
              <div className="text-center">
                <FaRulerCombined className="text-teal-500 text-2xl mx-auto mb-2" />
                <p className="text-sm text-slate-500">Diện tích</p>
                <p className="font-bold">75 m²</p>
              </div>
              <div className="text-center">
                <FaBed className="text-teal-500 text-2xl mx-auto mb-2" />
                <p className="text-sm text-slate-500">Phòng ngủ</p>
                <p className="font-bold">2 Phòng</p>
              </div>
              <div className="text-center">
                <FaBath className="text-teal-500 text-2xl mx-auto mb-2" />
                <p className="text-sm text-slate-500">Phòng tắm</p>
                <p className="font-bold">2 Phòng</p>
              </div>
              <div className="text-center">
                <FaMapMarkerAlt className="text-teal-500 text-2xl mx-auto mb-2" />
                <p className="text-sm text-slate-500">Hướng</p>
                <p className="font-bold">Đông Nam</p>
              </div>
            </div>

            {/* Description */}
            <h2 className="text-xl font-bold text-slate-800 mb-4">Tổng quan</h2>
            <p className="text-slate-600 leading-relaxed mb-8">
              Căn hộ tọa lạc tại tầng 15 của tòa tháp, mang đến tầm nhìn toàn cảnh ra sông Sài Gòn tuyệt đẹp. Thiết kế nội thất theo phong cách Minimalism hiện đại, tối ưu hóa không gian sống và đón ánh sáng tự nhiên. Trang bị đầy đủ nội thất cao cấp nhập khẩu, sẵn sàng để ở hoặc cho thuê sinh lời ngay. Hệ thống smarthome tích hợp giúp quản lý năng lượng và an ninh hiệu quả.
            </p>

            {/* Amenities */}
            <h2 className="text-xl font-bold text-slate-800 mb-4">Tiện ích nội khu</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
              {[
                { icon: <FaSwimmingPool />, label: "Hồ bơi vô cực" },
                { icon: <FaDumbbell />, label: "Phòng Gym 24/7" },
                { icon: <FaParking />, label: "Bãi đỗ xe thông minh" },
                { icon: <FaShieldAlt />, label: "An ninh đa lớp" },
                { icon: <FaTree />, label: "Công viên cây xanh" },
                { icon: <FaShoppingCart />, label: "Siêu thị tiện lợi" },
              ].map((item, idx) => (
                <div key={idx} className="flex items-center gap-3 bg-white border border-slate-100 rounded-xl px-4 py-3 text-sm text-slate-700">
                  <span className="text-teal-500 text-lg">{item.icon}</span>
                  {item.label}
                </div>
              ))}
            </div>

            {/* Floor Plan Placeholder */}
            <h2 className="text-xl font-bold text-slate-800 mb-4">Mặt bằng căn hộ</h2>
            <div className="bg-white border border-slate-200 rounded-2xl h-64 flex items-center justify-center mb-8">
              <p className="text-slate-400">Sơ đồ mặt bằng căn hộ</p>
            </div>

            {/* Map Placeholder */}
            <h2 className="text-xl font-bold text-slate-800 mb-4">Vị trí</h2>
            <div className="bg-slate-200 rounded-2xl h-72 flex items-center justify-center mb-8">
              <div className="text-center text-slate-500">
                <FaMapMarkerAlt className="text-3xl mx-auto mb-2 text-teal-500" />
                <p className="font-semibold">Vinhomes Central Park</p>
                <p className="text-sm">Bản đồ Google Maps</p>
              </div>
            </div>
          </div>

          {/* Right Sidebar */}
          <div className="hidden lg:block w-[360px] shrink-0">
            <div className="sticky top-20 space-y-6">
              {/* Booking Card */}
              <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm">
                <div className="flex justify-between items-center mb-4">
                  <div>
                    <p className="text-xs text-slate-500 uppercase tracking-wide">Trạng thái</p>
                    <p className="text-teal-600 font-bold flex items-center text-sm">
                      <span className="w-2 h-2 rounded-full bg-teal-500 mr-2"></span> Sẵn sàng để xem
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-slate-500 uppercase tracking-wide">Lịch xem sớm nhất</p>
                    <p className="text-teal-600 font-bold text-sm">14:30 Hôm nay</p>
                  </div>
                </div>

                <p className="text-sm text-slate-600 mb-3">Gợi ý từ trợ lý AI</p>
                <div className="flex gap-2 mb-4">
                  <button className="flex-1 bg-teal-50 border border-teal-200 text-teal-700 py-2.5 rounded-xl text-sm font-semibold flex items-center justify-center hover:bg-teal-100">
                    <FaCalendarAlt className="mr-2" /> 14:30 T5
                  </button>
                  <button className="flex-1 bg-white border border-slate-200 text-slate-700 py-2.5 rounded-xl text-sm font-semibold flex items-center justify-center hover:bg-slate-50">
                    <FaCalendarAlt className="mr-2" /> 09:00 T6
                  </button>
                </div>

                <div className="bg-slate-50 rounded-xl p-3 mb-6 flex items-start gap-2">
                  <FaClock className="text-slate-400 mt-0.5 shrink-0" />
                  <p className="text-xs text-slate-500">Hệ thống AI sẽ tự động giữ khung giờ trong 15 phút sau khi bạn chọn để đảm bảo trải nghiệm tốt nhất.</p>
                </div>

                <Link href="/booking/schedule" className="block w-full bg-[#00b4d8] text-white py-3.5 rounded-xl text-sm font-bold text-center hover:bg-cyan-600 transition-colors mb-3">
                  <FaCalendarAlt className="inline mr-2" /> Đặt lịch xem với AI
                </Link>
                <Link href="/chat" className="block w-full bg-white border border-slate-200 text-slate-700 py-3.5 rounded-xl text-sm font-bold text-center hover:bg-slate-50 transition-colors">
                  <FaComments className="inline mr-2" /> Chat với trợ lý
                </Link>
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
