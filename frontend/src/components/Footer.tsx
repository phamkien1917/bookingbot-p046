import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-[var(--ink)] text-white/70 py-16 border-t border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 mb-12 items-center">
          {/* Brand */}
          <div className="max-w-md">
            <Link href="/" className="inline-block mb-4">
              <img src="/brand/logo/nera-logo-reverse.svg" alt="Nera Logo" className="h-8 w-auto" />
            </Link>
            <p className="text-white/60 leading-relaxed text-sm">
              Tìm nhà bằng một cuộc trò chuyện · AI hiểu nhu cầu · Dữ liệu có thật · Sale xác nhận.
            </p>
          </div>

          {/* Links */}
          <div className="flex flex-wrap md:justify-end gap-x-8 gap-y-4 font-medium text-sm text-white/80">
            <Link href="/properties" className="hover:text-white transition-colors">Kho nhà</Link>
            <Link href="/chat" className="hover:text-white transition-colors">Trò chuyện với Nera</Link>
            <Link href="/saved" className="hover:text-white transition-colors">Đã lưu</Link>
            <Link href="/my-bookings" className="hover:text-white transition-colors">Lịch xem nhà</Link>
          </div>
        </div>

        {/* Bottom */}
        <div className="pt-8 border-t border-white/10 flex flex-col sm:flex-row justify-between items-center gap-4 text-xs text-white/40">
          <p>© 2026 Nera · AI Home Companion. Tất cả quyền được bảo lưu.</p>
          <p className="text-[11px] text-white/35">AI hiểu nhu cầu · Dữ liệu kiểm chứng · Con người xác nhận</p>
        </div>
      </div>
    </footer>
  );
}
