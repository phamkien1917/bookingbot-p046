"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { FaRobot, FaPaperPlane, FaCalendarAlt, FaClock, FaMapMarkerAlt, FaBed, FaHistory, FaUser, FaEllipsisV, FaCheckCircle, FaQuestionCircle, FaBookmark, FaExchangeAlt, FaTimes, FaPlus } from "react-icons/fa";

export default function ChatPage() {
  const INITIAL_MESSAGES = [
    { role: "bot", text: "Xin chào! Tôi là Trợ lý AI của hệ thống Booking Bot. Tôi có thể giúp bạn tìm kiếm thông tin căn hộ, giải đáp thắc mắc, hoặc đặt lịch xem nhà trực tiếp. Bạn cần tôi hỗ trợ gì hôm nay?" },
    { role: "bot", text: "", buttons: ["Tôi muốn đặt lịch xem nhà", "Tìm căn hộ 2 phòng ngủ", "Tư vấn giá thuê"] }
  ];

  const [messages, setMessages] = useState<any[]>(INITIAL_MESSAGES);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessions, setSessions] = useState<any[]>([]);
  const [insights, setInsights] = useState<any>({});
  const [selectedProperty, setSelectedProperty] = useState<any>(null);

  // Fetch all sessions on load
  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/v1/sessions");
      const data = await res.json();
      if (data.sessions) {
        setSessions(data.sessions);
      }
    } catch (err) {
      console.error("Failed to fetch sessions", err);
    }
  };

  const loadSession = async (id: string) => {
    setIsLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/api/v1/session/${id}`);
      const data = await res.json();
      if (data.messages) {
        setMessages(data.messages);
        setSessionId(id);
        setInsights(data.metadata?.insights || {});
      }
    } catch (err) {
      console.error("Failed to load session", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSend = async (textInput = input) => {
    if (!textInput.trim() || isLoading) return;
    
    setMessages((prev) => [...prev, { role: "user", text: textInput }]);
    if (textInput === input) setInput("");
    
    setIsLoading(true);
    // Add temporary loading message
    setMessages((prev) => [...prev, { role: "bot", text: "Đang suy nghĩ...", isLoading: true }]);

    try {
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
      };
      if (sessionId) {
        headers["x-session-id"] = sessionId;
      }
      
      const res = await fetch("http://localhost:8000/api/v1/chat", {
        method: "POST",
        headers,
        body: JSON.stringify({ message: textInput }),
      });
      
      const data = await res.json();
      
      if (data.session_id && data.session_id !== sessionId) {
        setSessionId(data.session_id);
        fetchSessions(); // refresh history
      }
      
      if (data.insights) {
        setInsights(data.insights);
      }
      
      setMessages((prev) => {
        const newMsgs = [...prev];
        newMsgs.pop(); // remove loading message
        newMsgs.push({ 
          role: "bot", 
          text: data.response,
          properties: data.properties 
        });
        return newMsgs;
      });
    } catch (err) {
      setMessages((prev) => {
        const newMsgs = [...prev];
        newMsgs.pop();
        newMsgs.push({ role: "bot", text: "Xin lỗi, đã có lỗi kết nối tới Server AI. Vui lòng thử lại sau." });
        return newMsgs;
      });
    } finally {
      setIsLoading(false);
    }
  };

  const startNewChat = () => {
    setMessages(INITIAL_MESSAGES);
    setSessionId("");
    setInsights({});
  };

  const formatPrice = (price: any) => {
    if (!price) return "Liên hệ";
    return price >= 1e9 ? `${(price / 1e9).toFixed(1)} tỷ` : `${(price / 1e6).toFixed(0)} triệu`;
  };

  // Convert insights object to array for UI
  const collectedInsights = Object.entries(insights)
    .filter(([_, v]) => v !== null && v !== undefined && v !== "")
    .map(([k, v]) => {
      if (k === 'min_price' || k === 'max_price') return `${k === 'min_price' ? 'Từ' : 'Đến'} ${formatPrice(v)}`;
      if (k === 'min_bedrooms') return `Tối thiểu ${v} phòng ngủ`;
      if (k === 'property_kind') return `Loại hình: ${v}`;
      if (k === 'district') return `Khu vực: ${v}`;
      if (k === 'keyword') return `Từ khóa: ${v}`;
      return `${v}`;
    });

  const progressPercent = Math.min(100, Math.max(10, collectedInsights.length * 20));

  return (
    <div className="h-screen overflow-hidden bg-slate-50 font-sans text-slate-900 flex">
      {/* Left Sidebar */}
      <div className="w-72 bg-[#0b132b] text-white flex flex-col shrink-0 overflow-y-auto hidden md:flex">
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center">
            <FaRobot className="text-2xl text-teal-400 mr-3" />
            <span className="font-bold text-lg">Booking Bot AI</span>
          </div>
        </div>

        <div className="p-4 border-b border-white/5">
          <button onClick={startNewChat} className="w-full bg-teal-500 hover:bg-teal-600 text-white py-3 rounded-xl text-sm font-semibold transition-colors flex items-center justify-center">
            <FaPlus className="mr-2" /> Cuộc hội thoại mới
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          <p className="text-xs text-slate-400 uppercase tracking-wider mb-3">Lịch sử chat</p>
          {sessions.length === 0 ? (
            <p className="text-xs text-slate-500 italic">Chưa có lịch sử</p>
          ) : (
            sessions.map((s, idx) => (
              <button 
                key={s.session_id} 
                onClick={() => loadSession(s.session_id)}
                className={`w-full text-left p-3 rounded-xl transition-colors ${sessionId === s.session_id ? 'bg-white/10 border border-white/20 text-white' : 'hover:bg-white/5 text-slate-300'}`}
              >
                <p className="text-sm font-semibold truncate">{s.preview}</p>
                <p className="text-xs text-slate-500 mt-1">{s.message_count} tin nhắn</p>
              </button>
            ))
          )}
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
      <div className="flex-1 flex flex-col min-w-0">
        {/* Chat Header */}
        <div className="bg-white border-b border-slate-100 px-6 py-4 flex items-center justify-between shrink-0">
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
            <div key={idx} className={`flex ${(msg.role === "user" || msg.role === "USER") ? "justify-end" : "items-start gap-3"}`}>
              {(msg.role === "bot" || msg.role === "assistant" || msg.role === "ASSISTANT") && (
                <div className="bg-[#00b4d8] p-2 rounded-full shrink-0 mt-1">
                  <FaRobot className="text-white text-sm" />
                </div>
              )}
              <div className="max-w-3xl w-full">
                {(msg.text || msg.content) && (
                  <div className={`inline-block px-5 py-3.5 rounded-2xl text-sm leading-relaxed whitespace-pre-line ${
                    (msg.role === "user" || msg.role === "USER")
                      ? "bg-[#0b132b] text-white rounded-tr-none float-right"
                      : "bg-white border border-slate-100 text-slate-700 rounded-tl-none shadow-sm"
                  } ${msg.isLoading ? "animate-pulse" : ""}`}>
                    {msg.text || msg.content}
                  </div>
                )}
                {/* Clear float if user */}
                {(msg.role === "user" || msg.role === "USER") && <div className="clear-both"></div>}
                
                {msg.buttons && (
                  <div className="flex flex-wrap gap-2 mt-2">
                    {msg.buttons.map((btn: string, bi: number) => (
                      <button key={bi} onClick={() => handleSend(btn)} className="bg-white border border-slate-200 text-slate-700 px-4 py-2 rounded-full text-xs font-medium hover:bg-slate-50 transition-colors">
                        {btn}
                      </button>
                    ))}
                  </div>
                )}
                
                {/* Property Suggestions Cards */}
                {msg.properties && msg.properties.length > 0 && (
                  <div className="mt-4 space-y-4">
                    {msg.properties.map((prop: any, pi: number) => (
                      <div key={pi} className="bg-white border border-slate-200 rounded-2xl overflow-hidden flex flex-col md:flex-row shadow-sm hover:shadow-md transition-shadow">
                        <div className="relative w-full md:w-64 h-48 md:h-auto shrink-0 bg-slate-100">
                          {prop.image ? (
                            <img src={prop.image} alt={prop.title} className="w-full h-full object-cover" />
                          ) : (
                            <div className="w-full h-full flex items-center justify-center text-slate-400 text-xs">Không có ảnh</div>
                          )}
                          {pi === 0 && (
                            <div className="absolute top-3 left-3 px-3 py-1 bg-teal-500 text-white text-[10px] uppercase font-bold rounded-full shadow-sm">
                              ★ Phù hợp nhất
                            </div>
                          )}
                        </div>
                        <div className="p-5 flex-1 flex flex-col">
                          <div className="flex justify-between items-start mb-2">
                            <h3 className="font-bold text-lg text-slate-800">{prop.title}</h3>
                            <span className="font-bold text-[#4338ca] text-base">{formatPrice(prop.list_price)}</span>
                          </div>
                          <p className="text-xs text-slate-500 mb-3 flex items-center">
                            <FaMapMarkerAlt className="mr-1 shrink-0" /> {prop.district ? `${prop.district}, ${prop.province}` : 'Đang cập nhật'}
                          </p>
                          
                          <div className="flex gap-2 mb-4 flex-wrap">
                            {prop.bedrooms && <span className="bg-slate-100 text-slate-600 px-2.5 py-1.5 text-xs font-medium rounded-md flex items-center"><FaBed className="mr-1.5 text-slate-400"/> {prop.bedrooms} PN</span>}
                            {prop.area_sqm && <span className="bg-slate-100 text-slate-600 px-2.5 py-1.5 text-xs font-medium rounded-md flex items-center">📐 {prop.area_sqm} m²</span>}
                            {prop.property_kind && <span className="bg-slate-100 text-slate-600 px-2.5 py-1.5 text-xs font-medium rounded-md flex items-center">Loại: {prop.property_kind}</span>}
                          </div>
                          
                          <div className="flex gap-2 pt-3 mt-auto border-t border-slate-100">
                            <button onClick={() => handleSend(`Tôi muốn lưu lại căn ${prop.title}`)} className="flex-1 bg-[#4338ca] hover:bg-indigo-700 text-white py-2.5 rounded-lg text-xs font-bold flex items-center justify-center transition-colors">
                              <FaBookmark className="mr-2" /> Lưu lại
                            </button>
                            <button onClick={() => setSelectedProperty(prop)} className="flex-1 bg-white border border-[#4338ca] text-[#4338ca] hover:bg-indigo-50 py-2.5 rounded-lg text-xs font-bold flex items-center justify-center transition-colors">
                              Chi tiết
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Input */}
        <div className="bg-white border-t border-slate-100 p-4 shrink-0">
          <div className="relative flex items-center max-w-4xl mx-auto w-full">
            <input
              type="text"
              placeholder="Nhập yêu cầu tìm kiếm hoặc đặt lịch..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              className="w-full bg-white border-2 border-slate-200 focus:border-[#4338ca] rounded-xl pl-12 pr-14 py-4 text-sm outline-none transition-colors"
            />
            <button onClick={() => handleSend()} disabled={isLoading} className="absolute right-3 p-3 bg-[#1e1b4b] disabled:bg-slate-400 text-white rounded-lg hover:bg-indigo-900 transition-colors">
              <FaPaperPlane />
            </button>
          </div>
        </div>
      </div>

      {/* Right Sidebar - AI Insights */}
      <div className="w-80 bg-slate-50 border-l border-slate-200 p-6 hidden lg:flex flex-col shrink-0 overflow-y-auto relative">
        <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-teal-400 to-[#4338ca]"></div>
        
        <h3 className="font-bold text-[#1e1b4b] text-lg mb-1">Ai đang hiểu gì về bạn</h3>
        <p className="text-[10px] font-bold text-teal-600 tracking-widest uppercase mb-6 flex items-center">
          AI-Driven Insights <span className="w-1.5 h-1.5 rounded-full bg-teal-500 ml-2"></span>
        </p>

        {/* Progress */}
        <div className="bg-white border border-slate-200 rounded-2xl p-4 mb-6 flex items-center gap-4 shadow-sm">
          <div className="relative w-12 h-12 shrink-0">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
              <path strokeDasharray="100, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" stroke="#e2e8f0" strokeWidth="3" fill="none" />
              <path strokeDasharray={`${progressPercent}, 100`} d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" stroke="#0f766e" strokeWidth="3" fill="none" className="transition-all duration-1000 ease-out" />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-xs font-bold text-slate-800">{progressPercent}%</span>
            </div>
          </div>
          <div>
            <p className="font-bold text-slate-800 text-sm">
              {progressPercent < 50 ? 'Đang phân tích' : progressPercent < 100 ? 'Gần hoàn tất' : 'Đã hiểu rõ'}
            </p>
            <p className="text-[11px] text-slate-500 mt-0.5">Tiếp tục trò chuyện để AI hiểu thêm</p>
          </div>
        </div>

        {/* Collected Data */}
        <div className="mb-6">
          <p className="text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">Đã thu thập</p>
          <div className="space-y-2.5">
            {collectedInsights.length === 0 ? (
              <p className="text-xs text-slate-500 italic">Chưa có thông tin</p>
            ) : (
              collectedInsights.map((item, i) => (
                <div key={i} className="bg-white border border-slate-100 rounded-xl p-3.5 flex items-center shadow-sm">
                  <FaCheckCircle className="text-emerald-500 mr-3 shrink-0 text-base" />
                  <span className="text-sm font-medium text-slate-700 capitalize">{item}</span>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Asking Data */}
        <div className="mb-8">
          <p className="text-[10px] font-bold text-[#4338ca] tracking-widest uppercase mb-3 flex items-center">
            Đang hỏi <span className="w-1.5 h-1.5 rounded-full bg-[#4338ca] ml-2 animate-pulse"></span>
          </p>
          <div className="bg-indigo-50 border-l-4 border-[#4338ca] rounded-r-xl p-4 flex items-center shadow-sm">
            <FaQuestionCircle className="text-[#4338ca] mr-3 shrink-0 text-base" />
            <span className="text-sm font-bold text-[#1e1b4b]">Yêu cầu thêm</span>
          </div>
        </div>
      </div>
      
      {/* Property Modal */}
      {selectedProperty && (
        <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col md:flex-row shadow-2xl relative">
            <button 
              onClick={() => setSelectedProperty(null)}
              className="absolute top-4 right-4 z-10 w-8 h-8 bg-black/20 hover:bg-black/40 text-white rounded-full flex items-center justify-center transition-colors"
            >
              <FaTimes />
            </button>
            <div className="w-full p-6 overflow-y-auto max-h-[90vh] bg-slate-50">
              <div className="uppercase tracking-widest text-xs font-bold text-teal-600 mb-2">Thông tin chi tiết</div>
              <h2 className="text-2xl font-bold text-slate-800 mb-2">{selectedProperty.title}</h2>
              <div className="flex justify-between items-center mb-6">
                <p className="text-xl font-bold text-[#4338ca]">{formatPrice(selectedProperty.list_price)}</p>
                <div className="flex gap-4">
                  <span className="flex items-center text-slate-600 text-sm font-semibold"><FaMapMarkerAlt className="text-slate-400 mr-2" /> {selectedProperty.district ? `${selectedProperty.district}, ${selectedProperty.province}` : 'Đang cập nhật'}</span>
                  {selectedProperty.area_sqm && <span className="flex items-center text-slate-600 text-sm font-semibold">📐 {selectedProperty.area_sqm} m²</span>}
                  {selectedProperty.bedrooms && <span className="flex items-center text-slate-600 text-sm font-semibold"><FaBed className="text-slate-400 mr-2" /> {selectedProperty.bedrooms} PN</span>}
                </div>
              </div>

              {selectedProperty.image && (
                <div className="w-full h-64 md:h-80 bg-slate-200 rounded-xl overflow-hidden mb-8">
                  <img src={selectedProperty.image} alt={selectedProperty.title} className="w-full h-full object-cover" />
                </div>
              )}
              
              <div className="space-y-8">
                {/* Tổng quan */}
                <div>
                  <h3 className="text-lg font-bold text-slate-800 mb-3">Tổng quan</h3>
                  <p className="text-slate-600 text-sm leading-relaxed whitespace-pre-line">
                    {selectedProperty.description || "Em cần bán căn hộ đẹp nhất khu. Diện tích sổ đỏ rộng rãi. Tầng đẹp, view thoáng sáng. \n\nVị trí trung tâm tiện di chuyển, xung quanh tiện ích ngập tràn, gần trường học, bệnh viện, khu vực an ninh tốt, dân trí cao. \n\nGiá bán thỏa thuận. Nhà thật, ảnh thật, giá thật. Anh chị cô bác có nhu cầu vui lòng liên hệ."}
                  </p>
                </div>

                {/* Tiện ích nội khu */}
                <div>
                  <h3 className="text-lg font-bold text-slate-800 mb-3">Tiện ích nội khu</h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                    {[
                      { icon: '🏊', name: 'Hồ bơi vô cực' },
                      { icon: '🏋️', name: 'Phòng Gym 24/7' },
                      { icon: '🅿️', name: 'Bãi đỗ xe thông minh' },
                      { icon: '🛡️', name: 'An ninh đa lớp' },
                      { icon: '🌲', name: 'Công viên cây xanh' },
                      { icon: '🛒', name: 'Siêu thị tiện lợi' },
                    ].map((amenity, idx) => (
                      <div key={idx} className="bg-white border border-slate-100 rounded-lg p-3 flex items-center shadow-sm">
                        <span className="text-lg mr-3">{amenity.icon}</span>
                        <span className="text-sm font-medium text-slate-700">{amenity.name}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Vị trí */}
                <div>
                  <h3 className="text-lg font-bold text-slate-800 mb-3">Vị trí</h3>
                  <div className="w-full h-64 bg-slate-200 rounded-xl overflow-hidden relative border border-slate-200">
                    <iframe 
                      width="100%" 
                      height="100%" 
                      frameBorder="0" 
                      style={{ border: 0 }} 
                      src={`https://maps.google.com/maps?q=${encodeURIComponent(selectedProperty.district ? `${selectedProperty.district}, ${selectedProperty.province}` : 'Hanoi')}&t=&z=13&ie=UTF8&iwloc=&output=embed`}
                      allowFullScreen
                    ></iframe>
                  </div>
                </div>
              </div>
              
              <div className="flex gap-4 mt-8 pt-6 border-t border-slate-200 sticky bottom-0 bg-slate-50">
                <button 
                  onClick={() => {
                    handleSend(`Tôi muốn đặt lịch xem căn ${selectedProperty.title}`);
                    setSelectedProperty(null);
                  }} 
                  className="flex-1 bg-[#4338ca] hover:bg-indigo-700 text-white py-3.5 rounded-xl font-bold transition-colors shadow-md"
                >
                  Đặt lịch xem nhà
                </button>
                <button className="px-5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 rounded-xl font-bold transition-colors shadow-sm">
                  <FaBookmark className="mr-2 inline" /> Lưu tin
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
