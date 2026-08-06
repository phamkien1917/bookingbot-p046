import { FaRobot } from "react-icons/fa";
import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-[#03045E] text-slate-300 py-16 border-t border-[#0b132b]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 mb-12">
          
          {/* Brand */}
          <div className="max-w-md">
            <div className="flex items-center text-white mb-6">
              <FaRobot className="h-8 w-8 text-teal-400" />
              <span className="ml-2 text-2xl font-bold">Booking Bot AI</span>
            </div>
            <p className="text-slate-400 leading-relaxed text-sm">
              Giải pháp AI thông minh giúp tối ưu hóa quy trình tìm kiếm và đặt lịch xem bất động sản.
            </p>
          </div>

          {/* Links */}
          <div className="flex flex-wrap md:justify-end gap-x-8 gap-y-4 font-medium text-sm">
            <Link href="#" className="hover:text-white transition-colors">Về chúng tôi</Link>
            <Link href="#" className="hover:text-white transition-colors">Điều khoản dịch vụ</Link>
            <Link href="#" className="hover:text-white transition-colors">Chính sách bảo mật</Link>
            <Link href="#" className="hover:text-white transition-colors">Liên hệ</Link>
          </div>
        </div>

        {/* Bottom */}
        <div className="pt-8 border-t border-slate-700/50 flex justify-between items-center text-xs text-slate-500">
          <p>© 2024 Booking Bot AI Agent. Tất cả quyền được bảo lưu.</p>
        </div>
      </div>
    </footer>
  );
}
