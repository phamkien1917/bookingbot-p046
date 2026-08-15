import { FaSearch, FaComments, FaCalendarAlt, FaShieldAlt } from "react-icons/fa";

export default function HowItWorks() {
  const steps = [
    {
      number: "1",
      title: "Chọn căn hộ",
      desc: "Duyệt qua danh sách các căn hộ đang mở bán/cho thuê với thông tin đầy đủ, minh bạch.",
      icon: <FaSearch className="text-white text-xl" />,
      iconBg: "bg-[#0b132b]",
    },
    {
      number: "2",
      title: "Trao đổi với AI",
      desc: "Tương tác tự nhiên với Booking Bot để hỏi đáp chi tiết và lọc ra lựa chọn tối ưu nhất.",
      icon: <FaComments className="text-white text-xl" />,
      iconBg: "bg-[#00b4d8]",
    },
    {
      number: "3",
      title: "Chọn lịch & giữ căn",
      desc: "Xem lịch trống real-time, chọn khung giờ phù hợp và hệ thống sẽ tự động tạm giữ căn cho bạn.",
      icon: <FaCalendarAlt className="text-white text-xl" />,
      iconBg: "bg-[#0077b6]",
    },
    {
      number: "4",
      title: "Nhận xác nhận",
      desc: "Nhận tin nhắn/email xác nhận ngay lập tức kèm thông tin liên hệ của chuyên viên tư vấn.",
      icon: <FaShieldAlt className="text-white text-xl" />,
      iconBg: "bg-[#023e8a]",
    },
  ];

  return (
    <section className="py-24 bg-slate-50 border-t border-slate-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-slate-900 mb-4">Trải nghiệm đặt lịch liền mạch</h2>
          <p className="text-slate-600 max-w-2xl mx-auto">
            Chỉ với 4 bước đơn giản, trợ lý AI sẽ giúp bạn hoàn tất quy trình tìm kiếm và đặt lịch xem nhà một cách nhanh chóng nhất.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <div key={index} className="relative bg-white p-8 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow pt-12">
              {/* Step Number Badge */}
              <div className="absolute -top-4 -left-4 w-10 h-10 bg-[#0b132b] text-white rounded-full flex items-center justify-center font-bold shadow-lg border-4 border-slate-50">
                {step.number}
              </div>
              
              {/* Icon */}
              <div className={`w-14 h-14 ${step.iconBg} rounded-2xl flex items-center justify-center mb-6 shadow-sm`}>
                {step.icon}
              </div>

              {/* Content */}
              <h3 className="text-xl font-bold text-slate-800 mb-3">{step.title}</h3>
              <p className="text-slate-600 text-sm leading-relaxed">
                {step.desc}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
