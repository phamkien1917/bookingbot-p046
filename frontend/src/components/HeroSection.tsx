import { FaMagic, FaSearch, FaLock, FaCheckCircle } from "react-icons/fa";
import { BsFillLightningFill } from "react-icons/bs";
import Link from "next/link";

export default function HeroSection() {
  return (
    <section className="relative pt-32 pb-32 overflow-hidden flex flex-col items-center justify-center text-center">
      {/* Background gradients */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
        <div className="absolute top-[-10%] right-[10%] w-[50%] h-[50%] rounded-full bg-cyan-100/40 blur-3xl" />
        <div className="absolute bottom-[-10%] left-[10%] w-[40%] h-[40%] rounded-full bg-teal-50/50 blur-3xl" />
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold text-[#0b132b] tracking-tight mb-8 leading-tight">
          Đặt lịch xem nhà cực nhanh cùng <span className="text-[#00b4d8]">Booking Bot AI</span>
        </h1>
        
        <p className="text-xl text-slate-600 mb-12 max-w-3xl mx-auto leading-relaxed">
          Booking Bot AI giúp bạn kiểm tra danh sách căn hộ, chọn thời gian, giữ căn và kết nối với nhân viên tư vấn hoàn toàn tự động. Nhanh chóng, chính xác và bảo mật tuyệt đối.
        </p>
        
        <div className="flex flex-col sm:flex-row justify-center items-center gap-6 mb-16">
          <Link href="/chat" className="bg-[#00b4d8] text-white px-12 py-5 rounded-full text-lg font-bold flex items-center justify-center hover:bg-cyan-600 transition-all transform hover:scale-105 shadow-xl shadow-cyan-500/30">
            <FaMagic className="mr-3 text-xl" /> Bắt đầu đặt lịch ngay
          </Link>
          <Link href="/properties" className="bg-white border-2 border-slate-200 text-slate-700 px-10 py-5 rounded-full text-lg font-bold flex items-center justify-center hover:bg-slate-50 transition-all hover:scale-105 shadow-sm">
            <FaSearch className="mr-3 text-slate-500 text-xl" /> Khám phá căn hộ
          </Link>
        </div>

        {/* Feature Chips */}
        <div className="flex flex-wrap justify-center gap-4">
          <span className="inline-flex items-center px-5 py-2.5 rounded-full bg-white shadow-sm border border-slate-100 text-sm font-semibold text-slate-700">
            <BsFillLightningFill className="mr-2 text-yellow-500" /> Phản hồi 24/7
          </span>
          <span className="inline-flex items-center px-5 py-2.5 rounded-full bg-white shadow-sm border border-slate-100 text-sm font-semibold text-slate-700">
            <FaLock className="mr-2 text-teal-600" /> Giữ căn tự động
          </span>
          <span className="inline-flex items-center px-5 py-2.5 rounded-full bg-white shadow-sm border border-slate-100 text-sm font-semibold text-slate-700">
            <FaCheckCircle className="mr-2 text-green-500" /> Xác nhận nhanh
          </span>
          <span className="inline-flex items-center px-5 py-2.5 rounded-full bg-white shadow-sm border border-slate-100 text-sm font-semibold text-slate-700">
            <FaLock className="mr-2 text-blue-500" /> Bảo mật
          </span>
        </div>
      </div>
    </section>
  );
}
