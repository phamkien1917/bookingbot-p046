import { FaMagic, FaSearch, FaBolt, FaLock, FaCheckCircle, FaRobot, FaPaperPlane } from "react-icons/fa";
import { BsFillLightningFill } from "react-icons/bs";
import Link from "next/link";

export default function HeroSection() {
  return (
    <section className="relative pt-20 pb-32 overflow-hidden">
      {/* Background gradients */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
        <div className="absolute top-[-10%] right-[-5%] w-[50%] h-[50%] rounded-full bg-cyan-100/40 blur-3xl" />
        <div className="absolute bottom-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-teal-50/50 blur-3xl" />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="lg:grid lg:grid-cols-12 lg:gap-16 items-center">
          
          {/* Left Column: Copy */}
          <div className="lg:col-span-6 text-center lg:text-left mb-16 lg:mb-0">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-[#0b132b] tracking-tight mb-6 leading-tight">
              Đặt lịch xem nhà trong vài phút với <span className="text-[#00b4d8]">trợ lý AI</span>
            </h1>
            <p className="text-lg text-slate-600 mb-8 max-w-2xl mx-auto lg:mx-0 leading-relaxed">
              Booking Bot AI giúp bạn kiểm tra căn hộ, chọn thời gian, giữ căn và kết nối với nhân viên tư vấn hoàn toàn tự động. Nhanh chóng, chính xác và bảo mật.
            </p>
            
            <div className="flex flex-col sm:flex-row justify-center lg:justify-start space-y-4 sm:space-y-0 sm:space-x-4 mb-10">
              <Link href="/chat" className="bg-[#00b4d8] text-white px-8 py-4 rounded-full font-semibold flex items-center justify-center hover:bg-cyan-600 transition-colors shadow-lg shadow-cyan-500/30">
                <FaMagic className="mr-2" /> Bắt đầu đặt lịch
              </Link>
              <Link href="/properties" className="bg-slate-100 text-slate-800 px-8 py-4 rounded-full font-semibold flex items-center justify-center hover:bg-slate-200 transition-colors">
                <FaSearch className="mr-2 text-slate-600" /> Khám phá căn hộ
              </Link>
            </div>

            {/* Feature Chips */}
            <div className="flex flex-wrap justify-center lg:justify-start gap-3">
              <span className="inline-flex items-center px-4 py-2 rounded-full bg-slate-100 text-sm font-medium text-slate-600">
                <BsFillLightningFill className="mr-2 text-yellow-500" /> Phản hồi 24/7
              </span>
              <span className="inline-flex items-center px-4 py-2 rounded-full bg-slate-100 text-sm font-medium text-slate-600">
                <FaLock className="mr-2 text-teal-600" /> Giữ căn tự động
              </span>
              <span className="inline-flex items-center px-4 py-2 rounded-full bg-slate-100 text-sm font-medium text-slate-600">
                <FaCheckCircle className="mr-2 text-green-500" /> Xác nhận nhanh
              </span>
              <span className="inline-flex items-center px-4 py-2 rounded-full bg-slate-100 text-sm font-medium text-slate-600">
                <FaLock className="mr-2 text-blue-500" /> Bảo mật
              </span>
            </div>
          </div>

          {/* Right Column: Chatbot UI */}
          <div className="lg:col-span-6 relative">
            <div className="bg-white rounded-3xl shadow-2xl shadow-slate-200/50 overflow-hidden border border-slate-100">
              {/* Chat Header */}
              <div className="bg-white border-b border-slate-100 px-6 py-4 flex items-center">
                <div className="bg-[#00b4d8] p-2 rounded-full mr-4">
                  <FaRobot className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="font-bold text-slate-800">Booking Bot AI</h3>
                  <div className="flex items-center text-xs text-slate-500">
                    <span className="w-2 h-2 rounded-full bg-green-500 mr-1"></span> Trực tuyến
                  </div>
                </div>
              </div>

              {/* Chat Messages */}
              <div className="bg-slate-50 p-6 space-y-6 h-[400px] overflow-y-auto">
                {/* Bot Message */}
                <div className="flex items-start">
                  <div className="bg-[#00b4d8] p-2 rounded-full mr-3 mt-1 shrink-0">
                    <FaRobot className="h-4 w-4 text-white" />
                  </div>
                  <div className="bg-white border border-slate-100 p-4 rounded-2xl rounded-tl-none shadow-sm text-slate-700 text-sm max-w-[85%]">
                    Chào bạn! Tôi là trợ lý ảo của Booking Bot. Bạn đang tìm căn hộ khu vực nào ạ?
                  </div>
                </div>

                {/* User Message */}
                <div className="flex justify-end">
                  <div className="bg-[#0b132b] p-4 rounded-2xl rounded-tr-none shadow-sm text-white text-sm max-w-[85%]">
                    Mình muốn tìm căn 2 phòng ngủ ở Quận 2, có ban công.
                  </div>
                </div>

                {/* Bot Message with actions */}
                <div className="flex items-start">
                  <div className="bg-[#00b4d8] p-2 rounded-full mr-3 mt-1 shrink-0">
                    <FaRobot className="h-4 w-4 text-white" />
                  </div>
                  <div>
                    <div className="bg-[#e0fbfc] p-4 rounded-2xl rounded-tl-none shadow-sm text-slate-800 text-sm max-w-md mb-3">
                      Tuyệt vời! Hiện tại hệ thống đang có 3 căn hộ phù hợp với yêu cầu của bạn ở dự án The River Thủ Thiêm và Empire City. Bạn muốn xem thông tin chi tiết hay đặt lịch tham quan ngay?
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <button className="bg-white border border-[#00b4d8] text-[#00b4d8] px-4 py-2 rounded-full text-xs font-semibold hover:bg-cyan-50 transition-colors">
                        Xem chi tiết căn hộ
                      </button>
                      <button className="bg-[#0077b6] text-white px-4 py-2 rounded-full text-xs font-semibold hover:bg-[#023e8a] transition-colors">
                        Đặt lịch tham quan
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              {/* Chat Input */}
              <div className="bg-white p-4">
                <div className="relative">
                  <input 
                    type="text" 
                    placeholder="Nhập tin nhắn..." 
                    className="w-full bg-slate-100 text-sm rounded-full pl-6 pr-12 py-4 outline-none focus:ring-2 focus:ring-[#00b4d8]/50"
                  />
                  <button className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-teal-600 hover:text-teal-700">
                    <FaPaperPlane className="h-5 w-5" />
                  </button>
                </div>
              </div>
            </div>
            
            {/* Decorative Elements */}
            <div className="absolute -top-6 -right-6 w-24 h-24 bg-dots-pattern opacity-50 -z-10"></div>
          </div>
        </div>
      </div>
    </section>
  );
}
