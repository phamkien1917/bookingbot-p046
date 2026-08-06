"use client";
import { useState } from "react";
import Link from "next/link";
import { FaRobot, FaPaperPlane, FaCalendarAlt, FaClock, FaMapMarkerAlt, FaBed, FaHistory, FaUser, FaEllipsisV } from "react-icons/fa";

const MOCK_MESSAGES = [
  { role: "bot", text: "Xin chào! Tôi là Trợ lý AI của hệ thống. Tôi thấy bạn đang quan tâm đến các căn hộ tại khu vực Quận 2. Bạn muốn đặt lịch xem nhà vào thời gian nào để tôi sắp xếp nhân viên hỗ trợ?" },
  { role: "bot", text: "", buttons: ["Sáng mai (09:00 - 11:00)", "Cuối tuần này", "Xem các căn có sẵn hôm nay"] },
  { role: "user", text: "Mình muốn xem căn hộ The Vista mã VIS-204 vào chiều mai khoảng 14:00." },
  { role: "bot", text: "Đã hiểu! Tôi đang kiểm tra lịch trống của căn VIS-204 và giữ chỗ tạm thời cho bạn vào lúc 14:00, Ngày mai.\n\nHệ thống đang tìm kiếm nhân viên phụ trách khu vực này để xác nhận lịch với bạn. Vui lòng xem thông tin tóm tắt bên phải nhé." },
];

export default function ChatPage() {
  const [messages, setMessages] = useState(MOCK_MESSAGES);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: "user", text: input }]);
    setInput("");
    setTimeout(() => {
      setMessages((prev) => [...prev, { role: "bot", text: "Cảm ơn bạn! Tôi đang xử lý yêu cầu của bạn..." }]);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 flex">
      {/* Left Sidebar */}
      <div className="w-64 bg-[#0b132b] text-white flex flex-col shrink-0">
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center">
            <FaRobot className="text-2xl text-teal-400 mr-3" />
            <span className="font-bold text-lg">Booking Bot AI</span>
          </div>
        </div>

        <div className="p-4">
          <button className="w-full bg-white/10 border border-white/20 text-white py-3 rounded-xl text-sm font-semibold hover:bg-white/20 transition-colors mb-6">
            + Cuộc hội thoại mới
          </button>
          <button className="w-full bg-teal-500/20 border border-teal-400/30 text-teal-300 py-3 rounded-xl text-sm font-semibold hover:bg-teal-500/30 transition-colors mb-6">
            Cuộc hội thoại hiện tại
          </button>
        </div>

        <div className="px-4 mt-2">
          <p className="text-xs text-slate-400 uppercase tracking-wider mb-3">Lối tắt</p>
          <nav className="space-y-1">
            <Link href="/my-bookings" className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-slate-300 hover:bg-white/10">
              <FaHistory /> Lịch sử đặt lịch
            </Link>
            <Link href="/my-bookings" className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-slate-300 hover:bg-white/10">
              <FaCalendarAlt /> Lịch xem của tôi
            </Link>
            <Link href="#" className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-slate-300 hover:bg-white/10">
              <FaUser /> Hồ sơ
            </Link>
          </nav>
        </div>

        {/* User */}
        <div className="mt-auto p-4 border-t border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-full bg-teal-500 flex items-center justify-center text-white font-bold text-sm">N</div>
            <div>
              <p className="text-sm font-semibold">Nguyễn Văn A</p>
              <p className="text-xs text-slate-400">Khách hàng</p>
            </div>
          </div>
        </div>
      </div>

      {/* Chat Main */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="bg-white border-b border-slate-100 px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-[#00b4d8] p-2.5 rounded-full">
              <FaRobot className="text-white text-lg" />
            </div>
            <div>
              <h2 className="font-bold text-slate-800">Trợ lý Đặt Lịch AI</h2>
              <p className="text-xs text-slate-500">Tôi có thể giúp bạn đặt lịch 24/7</p>
            </div>
          </div>
          <FaEllipsisV className="text-slate-400 cursor-pointer" />
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "items-start gap-3"}`}>
              {msg.role === "bot" && (
                <div className="bg-[#00b4d8] p-2 rounded-full shrink-0 mt-1">
                  <FaRobot className="text-white text-sm" />
                </div>
              )}
              <div>
                {msg.text && (
                  <div className={`max-w-lg px-5 py-3.5 rounded-2xl text-sm leading-relaxed whitespace-pre-line ${
                    msg.role === "user"
                      ? "bg-[#0b132b] text-white rounded-tr-none"
                      : "bg-white border border-slate-100 text-slate-700 rounded-tl-none shadow-sm"
                  }`}>
                    {msg.text}
                  </div>
                )}
                {msg.buttons && (
                  <div className="flex flex-wrap gap-2 mt-2">
                    {msg.buttons.map((btn, bi) => (
                      <button key={bi} className="bg-white border border-slate-200 text-slate-700 px-4 py-2 rounded-full text-xs font-medium hover:bg-slate-50">
                        {btn}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Input */}
        <div className="bg-white border-t border-slate-100 p-4">
          <p className="text-xs text-slate-400 text-center mb-2">AI có thể đưa ra thông tin chưa chính xác. Vui lòng kiểm tra lại.</p>
          <div className="relative flex items-center">
            <input
              type="text"
              placeholder="Nhập tin nhắn để yêu cầu AI hỗ trợ..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              className="w-full bg-slate-100 rounded-full pl-6 pr-14 py-4 text-sm outline-none focus:ring-2 focus:ring-teal-400/50"
            />
            <button onClick={handleSend} className="absolute right-2 p-3 bg-[#00b4d8] text-white rounded-full hover:bg-cyan-600 transition-colors">
              <FaPaperPlane />
            </button>
          </div>
        </div>
      </div>

      {/* Right Sidebar - Booking Info */}
      <div className="w-80 bg-white border-l border-slate-100 p-6 hidden xl:block overflow-y-auto">
        <h3 className="font-bold text-slate-800 text-lg mb-6">Thông tin đặt lịch</h3>

        {/* Hold Status */}
        <div className="bg-orange-50 border border-orange-200 rounded-2xl p-5 mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-orange-600 font-bold text-xs flex items-center">
              <span className="w-2 h-2 rounded-full bg-orange-500 mr-2 animate-pulse"></span> ĐANG GIỮ CĂN
            </span>
          </div>
          <p className="text-4xl font-bold text-[#0b132b] text-center my-3">14:30</p>
          <p className="text-xs text-slate-500 text-center">Phút con lại</p>
          <p className="text-xs text-slate-500 text-center mt-2">Hệ thống đang ưu tiên giữ khung giờ này cho bạn.</p>
        </div>

        {/* Property Info */}
        <div className="bg-white border border-slate-100 rounded-2xl overflow-hidden mb-6">
          <div className="relative h-36">
            <img src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=400&q=80" alt="Property" className="w-full h-full object-cover" />
            <span className="absolute top-2 right-2 bg-white px-2 py-1 rounded-lg text-xs font-bold">VIS-204</span>
          </div>
          <div className="p-4">
            <h4 className="font-bold text-slate-800">The Vista An Phú - 2PN</h4>
            <p className="text-xs text-slate-500 flex items-center mt-1"><FaMapMarkerAlt className="mr-1" /> Quận 2, TP. Hồ Chí Minh</p>
            <div className="mt-3 space-y-2 text-xs text-slate-600">
              <div className="flex justify-between"><span>Thời gian xem:</span><span className="font-bold text-teal-600">14:00, Ngày mai</span></div>
              <div className="flex justify-between"><span>Loại hình:</span><span className="font-bold">Trực tiếp</span></div>
            </div>
          </div>
        </div>

        {/* Finding Agent */}
        <div className="bg-slate-50 border border-slate-100 rounded-2xl p-4 flex items-start gap-3">
          <div className="w-8 h-8 bg-teal-100 rounded-full flex items-center justify-center shrink-0 animate-pulse">
            <FaUser className="text-teal-600 text-sm" />
          </div>
          <div>
            <p className="font-semibold text-sm text-slate-800">Đang tìm nhân viên...</p>
            <p className="text-xs text-slate-500">Hệ thống đang ghép nối với chuyên viên khu vực.</p>
          </div>
        </div>

        <button className="w-full mt-6 bg-white border border-red-200 text-red-500 py-3 rounded-xl text-sm font-semibold hover:bg-red-50 transition-colors">
          Hủy yêu cầu đặt lịch
        </button>
      </div>
    </div>
  );
}
