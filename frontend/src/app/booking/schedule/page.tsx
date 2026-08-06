"use client";
import { useState } from "react";
import Link from "next/link";
import { FaArrowLeft, FaRobot, FaClock, FaArrowRight } from "react-icons/fa";

const TIME_SLOTS = ["09:00", "10:00", "14:00", "16:30"];
const DAYS = [
  { d: "T2", n: "" }, { d: "T3", n: "" }, { d: "T4", n: "" }, { d: "T5", n: "" }, { d: "T6", n: "" }, { d: "T7", n: "" }, { d: "CN", n: "" },
  { d: "", n: "" }, { d: "", n: "1" }, { d: "", n: "2" }, { d: "", n: "3" }, { d: "", n: "4" }, { d: "", n: "5" }, { d: "", n: "" },
  { d: "", n: "6" }, { d: "", n: "7" }, { d: "", n: "8" }, { d: "", n: "9" }, { d: "", n: "10" }, { d: "", n: "11" }, { d: "", n: "12" },
  { d: "", n: "13" }, { d: "", n: "14" }, { d: "", n: "15" }, { d: "", n: "" }, { d: "", n: "" }, { d: "", n: "" }, { d: "", n: "" },
];

export default function SchedulePage() {
  const [selectedDate, setSelectedDate] = useState("10");
  const [selectedTime, setSelectedTime] = useState("14:00");

  return (
    <div className="min-h-screen bg-gradient-to-br from-cyan-50 via-white to-slate-50 font-sans text-slate-900">
      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="flex items-center justify-between mb-12">
          <Link href="/chat" className="text-slate-500 hover:text-slate-800 flex items-center text-sm font-medium">
            <FaArrowLeft className="mr-2" /> Quay lại
          </Link>
          <h1 className="text-xl font-bold text-slate-800">Booking Bot AI</h1>
          <div></div>
        </div>

        <h2 className="text-3xl font-bold text-slate-800 mb-2">Chọn thời gian bạn muốn xem căn hộ</h2>
        <p className="text-slate-500 mb-10">Căn hộ: Vinhomes Central Park - Park 1</p>

        <div className="flex gap-12">
          {/* Calendar */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-slate-800">Tháng 10, 2024</h3>
              <div className="flex gap-2">
                <button className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 hover:bg-slate-200">&lt;</button>
                <button className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 hover:bg-slate-200">&gt;</button>
              </div>
            </div>

            <div className="grid grid-cols-7 gap-2">
              {DAYS.map((day, idx) => (
                <div key={idx} className={`w-10 h-10 flex items-center justify-center text-sm rounded-full cursor-pointer transition-colors ${
                  day.d ? "font-bold text-slate-500 text-xs" :
                  day.n === selectedDate ? "bg-[#0b132b] text-white font-bold" :
                  day.n ? "hover:bg-slate-100 text-slate-700" : ""
                }`}
                onClick={() => day.n && setSelectedDate(day.n)}>
                  {day.d || day.n}
                </div>
              ))}
            </div>
          </div>

          {/* Time Slots */}
          <div className="flex-1">
            <h3 className="font-bold text-slate-800 mb-4">Thời gian trong ngày</h3>
            <div className="flex flex-wrap gap-3 mb-6">
              {TIME_SLOTS.map((time) => (
                <button key={time} onClick={() => setSelectedTime(time)}
                  className={`px-6 py-3 rounded-xl text-sm font-semibold border transition-colors ${
                    selectedTime === time
                      ? "bg-teal-50 border-teal-400 text-teal-700 ring-2 ring-teal-400/50"
                      : "bg-white border-slate-200 text-slate-700 hover:border-slate-300"
                  }`}>
                  {time}
                </button>
              ))}
              <div className="px-6 py-3 rounded-xl text-sm text-slate-400 bg-slate-100 border border-slate-200 line-through">16:30 <span className="text-xs block">Không giờ chót</span></div>
            </div>

            {/* AI Suggestion */}
            <div className="bg-teal-50 border border-teal-200 rounded-2xl p-5 flex items-start gap-3">
              <FaRobot className="text-teal-600 text-xl mt-0.5 shrink-0" />
              <div>
                <p className="font-bold text-teal-800 text-sm mb-1">AI đề xuất</p>
                <p className="text-sm text-teal-700">14:00 là thời gian phù hợp nhất dựa trên lịch sử xem nhà của bạn và lưu lượng giao thông dự kiến trong khu vực. Ánh sáng tự nhiên tại căn hộ cũng đạt mức tối ưu vào khung giờ này.</p>
              </div>
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between mt-12">
          <div className="flex items-center text-sm text-slate-500">
            <FaClock className="mr-2" /> Lịch xem sẽ được giữ trong 15 phút.
          </div>
          <Link href="/booking/hold" className="bg-[#0b132b] text-white px-8 py-3.5 rounded-full font-semibold flex items-center hover:bg-slate-800 transition-colors">
            Tiếp tục giữ căn <FaArrowRight className="ml-2" />
          </Link>
        </div>
      </div>
    </div>
  );
}
