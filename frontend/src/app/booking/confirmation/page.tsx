"use client";
import Link from "next/link";
import { FaCheckCircle, FaCalendarPlus, FaMapMarkedAlt, FaHome, FaPhone, FaComment, FaStar } from "react-icons/fa";

export default function ConfirmationPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white font-sans text-slate-900 flex flex-col items-center justify-center px-4 py-16">
      {/* Success Icon */}
      <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mb-8">
        <FaCheckCircle className="text-green-500 text-4xl" />
      </div>

      <h1 className="text-3xl font-bold text-slate-800 mb-3 text-center">Lịch xem nhà đã được xác nhận</h1>
      <p className="text-slate-500 text-center max-w-lg mb-12">Cảm ơn bạn đã đặt lịch. Chúng tôi đã gửi email xác nhận chi tiết đến địa chỉ của bạn.</p>

      <div className="flex flex-col md:flex-row gap-6 max-w-3xl w-full mb-12">
        {/* Booking Details */}
        <div className="flex-1 bg-white border border-slate-100 rounded-2xl p-6 shadow-sm">
          <h3 className="font-bold text-slate-800 text-lg mb-5 flex items-center gap-2">
            <FaCalendarPlus className="text-teal-500" /> Chi tiết lịch hẹn
          </h3>
          <div className="flex items-start gap-4 mb-4">
            <img src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=80&q=80" alt="Property" className="w-14 h-14 rounded-xl object-cover" />
            <div>
              <span className="text-xs bg-teal-100 text-teal-700 px-2 py-0.5 rounded-full font-bold">#BBA-8924</span>
            </div>
          </div>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between"><span className="text-slate-500">Mã đặt lịch:</span><span className="font-bold">#BBA-8924</span></div>
            <div className="flex justify-between"><span className="text-slate-500">Căn hộ:</span><span className="font-bold">The Metropole Thủ Thiêm<br/>Căn 2PN - Tòa Galleria</span></div>
            <div className="flex justify-between"><span className="text-slate-500">Thời gian:</span><span className="font-bold">14:30 - 15:30<br/>Thứ Sáu, 15/11/2024</span></div>
            <div className="flex justify-between"><span className="text-slate-500">Địa chỉ:</span><span className="font-bold">Khu đô thị mới Thủ Thiêm,<br/>Thành phố Thủ Đức, TP.HCM</span></div>
          </div>
        </div>

        {/* Agent Info */}
        <div className="flex-1 bg-white border border-slate-100 rounded-2xl p-6 shadow-sm">
          <h3 className="font-bold text-slate-800 text-lg mb-5 flex items-center gap-2">
            <span className="text-teal-500">👤</span> Nhân viên tư vấn
          </h3>
          <div className="flex items-center gap-4 mb-4">
            <div className="w-14 h-14 rounded-full bg-teal-100 flex items-center justify-center text-teal-600 font-bold text-xl">N</div>
            <div>
              <p className="font-bold text-slate-800">Nguyễn Trần Quang Hải</p>
              <p className="text-xs text-slate-500">Chuyên viên tư vấn cao cấp</p>
              <p className="text-xs text-yellow-500 flex items-center gap-1 mt-1"><FaStar /> 4.9 (128 đánh giá)</p>
            </div>
          </div>
          <div className="flex gap-3 mt-6">
            <button className="flex-1 bg-white border border-slate-200 text-slate-700 py-3 rounded-xl text-sm font-semibold hover:bg-slate-50 flex items-center justify-center gap-2">
              <FaPhone className="text-teal-500" /> Gọi điện
            </button>
            <button className="flex-1 bg-white border border-slate-200 text-slate-700 py-3 rounded-xl text-sm font-semibold hover:bg-slate-50 flex items-center justify-center gap-2">
              <FaComment className="text-teal-500" /> Nhắn tin
            </button>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex flex-wrap gap-4 justify-center">
        <button className="bg-[#0b132b] text-white px-6 py-3 rounded-full font-semibold flex items-center gap-2 hover:bg-slate-800 transition-colors">
          <FaCalendarPlus /> Thêm vào lịch
        </button>
        <button className="bg-teal-500 text-white px-6 py-3 rounded-full font-semibold flex items-center gap-2 hover:bg-teal-600 transition-colors">
          <FaMapMarkedAlt /> Xem chỉ đường
        </button>
        <Link href="/" className="bg-white border border-slate-200 text-slate-700 px-6 py-3 rounded-full font-semibold flex items-center gap-2 hover:bg-slate-50 transition-colors">
          <FaHome /> Về trang chủ
        </Link>
      </div>
    </div>
  );
}
