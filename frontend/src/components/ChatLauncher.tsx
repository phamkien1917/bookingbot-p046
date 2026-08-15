/* eslint-disable @next/next/no-img-element */
"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { usePathname } from "next/navigation";
import { FaPaperPlane, FaRobot, FaTimes } from "react-icons/fa";
import { apiFetch } from "@/lib/api";
import type { Property } from "@/lib/types";

type ChatItem = { role: "user" | "assistant"; content: string; properties?: Property[] };
type ChatReply = { response: string; session_id: string; properties?: Property[] };

const suggestions = ["Tìm nhà Hà Nội trên 10 tỷ", "Căn hộ 2 phòng ngủ", "Tôi muốn đặt lịch xem nhà"];

function displayPrice(value?: number | null) {
  if (!value) return "Liên hệ";
  return value >= 1_000_000_000 ? `${(value / 1_000_000_000).toFixed(1)} tỷ` : `${(value / 1_000_000).toFixed(0)} triệu`;
}

export default function ChatLauncher() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => crypto.randomUUID());
  const [messages, setMessages] = useState<ChatItem[]>([
    { role: "assistant", content: "Xin chào! Tôi có thể giúp bạn tìm nhà, lọc theo ngân sách và đặt lịch xem." },
  ]);

  if (["/", "/chat", "/login", "/sale", "/admin", "/unauthorized"].some((prefix) => pathname === prefix || (prefix !== "/" && pathname.startsWith(`${prefix}/`)))) return null;

  async function send(event?: FormEvent, value?: string) {
    event?.preventDefault();
    const message = (value ?? input).trim();
    if (!message || loading) return;
    setInput("");
    setMessages((current) => [...current, { role: "user", content: message }]);
    setLoading(true);
    try {
      const reply = await apiFetch<ChatReply>("/chat", {
        method: "POST",
        headers: { "X-Session-ID": sessionId },
        body: JSON.stringify({ message }),
      });
      setMessages((current) => [...current, { role: "assistant", content: reply.response, properties: reply.properties ?? [] }]);
    } catch (reason) {
      setMessages((current) => [...current, { role: "assistant", content: reason instanceof Error ? reason.message : "Tôi chưa kết nối được máy chủ. Bạn thử lại nhé." }]);
    } finally { setLoading(false); }
  }

  return <div className="fixed bottom-5 right-5 z-50">
    {open && <section className="mb-3 flex h-[min(620px,calc(100vh-110px))] w-[min(390px,calc(100vw-32px))] flex-col overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-2xl" aria-label="Trợ lý tìm nhà">
      <header className="flex items-center justify-between bg-[#0b132b] px-5 py-4 text-white"><div className="flex items-center gap-3"><span className="rounded-full bg-teal-400 p-2 text-[#0b132b]"><FaRobot /></span><div><p className="font-bold">Trợ lý tìm nhà</p><p className="text-xs text-slate-300">Phản hồi nhanh · hỗ trợ 24/7</p></div></div><button onClick={() => setOpen(false)} className="rounded-full p-2 text-slate-300 hover:bg-white/10" aria-label="Đóng chatbot"><FaTimes /></button></header>
      <div className="flex-1 space-y-3 overflow-y-auto bg-slate-50 p-4">{messages.map((message, index) => <div key={`${message.role}-${index}`} className={message.role === "user" ? "flex justify-end" : "flex justify-start"}><div className={`max-w-[88%] rounded-2xl px-4 py-3 text-sm leading-6 ${message.role === "user" ? "rounded-br-sm bg-[#0b132b] text-white" : "rounded-bl-sm border border-slate-100 bg-white text-slate-700 shadow-sm"}`}><p className="whitespace-pre-line">{message.content}</p>{message.properties?.map((property) => { const imgUrl = property.image || property.media?.[0]?.url; return <article key={property.id} className="mt-3 overflow-hidden rounded-xl border border-slate-200 bg-white"><div className="h-28 bg-slate-100">{imgUrl ? <img src={imgUrl} alt={property.title} className="h-full w-full object-cover" /> : <div className="grid h-full place-items-center text-3xl">🏠</div>}</div><div className="p-3"><p className="line-clamp-2 text-xs font-bold text-slate-800">{property.title}</p><p className="mt-1 text-sm font-bold text-teal-700">{displayPrice(property.list_price)}</p><div className="mt-2 flex gap-2"><Link href={`/properties/${property.id}`} onClick={() => setOpen(false)} className="flex-1 rounded-lg border border-slate-200 py-1.5 text-center text-xs font-semibold">Chi tiết</Link><Link href={`/booking/schedule?property_id=${property.id}`} onClick={() => setOpen(false)} className="flex-1 rounded-lg bg-teal-600 py-1.5 text-center text-xs font-semibold text-white">Đặt lịch</Link></div></div></article>})}</div></div>)}{loading && <div className="flex items-center gap-2 text-xs text-slate-500"><span className="h-2 w-2 animate-pulse rounded-full bg-teal-500" />AI đang tìm kiếm...</div>}</div>
      <div className="border-t border-slate-100 bg-white p-3"><div className="mb-2 flex gap-2 overflow-x-auto">{suggestions.map((suggestion) => <button key={suggestion} onClick={() => void send(undefined, suggestion)} className="whitespace-nowrap rounded-full border border-teal-100 bg-teal-50 px-3 py-1.5 text-[11px] font-semibold text-teal-700">{suggestion}</button>)}</div><form onSubmit={(event) => void send(event)} className="flex gap-2"><input value={input} onChange={(event) => setInput(event.target.value)} placeholder="Bạn đang tìm căn nhà nào?" className="min-w-0 flex-1 rounded-xl border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-teal-500" aria-label="Tin nhắn cho trợ lý" /><button disabled={loading || !input.trim()} className="rounded-xl bg-[#0b132b] px-4 text-white disabled:opacity-40" aria-label="Gửi"><FaPaperPlane /></button></form></div>
    </section>}
    <button onClick={() => setOpen((value) => !value)} className="group flex items-center gap-3 rounded-full bg-[#0b132b] px-5 py-3.5 text-sm font-bold text-white shadow-xl shadow-slate-900/20 transition hover:-translate-y-0.5 hover:bg-slate-800" aria-expanded={open} aria-label={open ? "Đóng trợ lý" : "Mở trợ lý tìm nhà"}><span className="relative rounded-full bg-teal-400 p-2 text-[#0b132b]"><FaRobot /><span className="absolute -right-0.5 -top-0.5 h-2.5 w-2.5 rounded-full bg-emerald-400 ring-2 ring-[#0b132b]" /></span><span className="hidden sm:inline">Hỏi trợ lý tìm nhà</span></button>
  </div>;
}
