/* eslint-disable @next/next/no-img-element */
"use client";

import { FormEvent, Suspense, useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FaBed, FaBookmark, FaCalendarAlt, FaMapMarkerAlt, FaPaperPlane, FaPlus, FaRobot, FaTimes } from "react-icons/fa";
import { useAuth } from "@/components/AuthProvider";
import { apiFetch } from "@/lib/api";
import type { Property } from "@/lib/types";

interface ChatMessage { role: "user" | "assistant"; content: string; properties?: Property[] }
interface ChatResponse { response: string; session_id: string; properties: Property[]; insights: Record<string, unknown> }
interface SessionSummary { session_id: string; preview: string; message_count: number; last_active: string }
interface SessionDetail { messages: Array<{ role: string; content: string; properties?: Property[] }> }

const greeting: ChatMessage = { role: "assistant", content: "Xin chào! Tôi có thể giúp bạn tìm bất động sản. Khi thấy căn phù hợp, hãy bấm Đặt lịch để chọn giờ xem nhà thực tế." };

function formatPrice(price?: number | null) {
  if (!price) return "Liên hệ";
  return price >= 1e9 ? `${(price / 1e9).toFixed(1)} tỷ` : `${(price / 1e6).toFixed(0)} triệu`;
}

function ChatContent() {
  const { user } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const propertyId = searchParams.get("property_id");
  const [messages, setMessages] = useState<ChatMessage[]>([greeting]);
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [sessionId, setSessionId] = useState(() => crypto.randomUUID());
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selected, setSelected] = useState<Property | null>(null);
  const [savedIds, setSavedIds] = useState<Set<string>>(new Set());
  const bottomRef = useRef<HTMLDivElement>(null);
  const propertyLoaded = useRef(false);

  const loadSessions = useCallback(async () => {
    if (!user) { setSessions([]); return; }
    try { setSessions((await apiFetch<{ sessions: SessionSummary[] }>("/sessions")).sessions); } catch { setSessions([]); }
  }, [user]);

  useEffect(() => {
    const timer = window.setTimeout(() => void loadSessions(), 0);
    return () => window.clearTimeout(timer);
  }, [loadSessions]);
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, loading]);

  useEffect(() => {
    if (!propertyId || propertyLoaded.current) return;
    propertyLoaded.current = true;
    void apiFetch<Property>(`/properties/${propertyId}`).then((property) => {
      setMessages([greeting, { role: "assistant", content: `Bạn đang quan tâm đến “${property.title}”. Bạn có thể xem chi tiết hoặc đặt lịch ngay bên dưới.`, properties: [property] }]);
    }).catch((err: unknown) => setError(err instanceof Error ? err.message : "Không tìm thấy bất động sản"));
  }, [propertyId]);

  async function send(event?: FormEvent, quickText?: string) {
    event?.preventDefault();
    const text = (quickText ?? input).trim();
    if (!text || loading) return;
    setInput(""); setError(""); setLoading(true);
    setMessages((current) => [...current, { role: "user", content: text }]);
    try {
      const response = await apiFetch<ChatResponse>("/chat", { method: "POST", headers: { "X-Session-ID": sessionId }, body: JSON.stringify({ message: text }) });
      setSessionId(response.session_id || sessionId);
      setMessages((current) => [...current, { role: "assistant", content: response.response, properties: response.properties ?? [] }]);
      await loadSessions();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Chatbot chưa phản hồi");
    } finally { setLoading(false); }
  }

  async function loadSession(id: string) {
    try {
      const data = await apiFetch<SessionDetail>(`/session/${id}`);
      setSessionId(id);
      setMessages(data.messages.map((message) => ({ role: message.role.toLowerCase() === "user" ? "user" : "assistant", content: message.content, properties: message.properties })));
      setError("");
    } catch (err) { setError(err instanceof Error ? err.message : "Không tải được cuộc trò chuyện"); }
  }

  function newChat() { setSessionId(crypto.randomUUID()); setMessages([greeting]); setInput(""); setError(""); }
  function save(property: Property) { setSavedIds((current) => { const next = new Set(current); if (next.has(property.id)) next.delete(property.id); else next.add(property.id); return next; }); }
  function book(property: Property) {
    if (!user) { router.push(`/login?next=${encodeURIComponent(`/booking/schedule?property_id=${property.id}`)}`); return; }
    if (user.role !== "CUSTOMER") { setError("Chỉ tài khoản khách hàng có thể đặt lịch xem nhà."); return; }
    router.push(`/booking/schedule?property_id=${property.id}`);
  }

  return <div className="flex h-screen overflow-hidden bg-slate-50 text-slate-900">
    <aside className="hidden w-72 shrink-0 flex-col bg-[#0b132b] text-white md:flex"><div className="border-b border-white/10 p-6"><Link href="/" className="flex items-center gap-3 font-bold"><FaRobot className="text-2xl text-teal-400"/>Booking Bot AI</Link></div><div className="p-4"><button onClick={newChat} className="flex w-full items-center justify-center gap-2 rounded-xl bg-teal-500 py-3 text-sm font-semibold hover:bg-teal-600"><FaPlus/> Cuộc trò chuyện mới</button></div><div className="flex-1 overflow-y-auto p-4"><p className="mb-3 text-xs uppercase tracking-wider text-slate-400">Lịch sử của bạn</p>{!user ? <Link href="/login?next=/chat" className="text-sm text-teal-300 hover:underline">Đăng nhập để lưu lịch sử</Link> : sessions.length === 0 ? <p className="text-sm text-slate-400">Chưa có cuộc trò chuyện.</p> : sessions.map((session)=><button key={session.session_id} onClick={()=>void loadSession(session.session_id)} className={`mb-2 w-full rounded-xl p-3 text-left text-sm ${session.session_id===sessionId ? "bg-white/15" : "hover:bg-white/10"}`}><span className="block truncate">{session.preview}</span><span className="text-xs text-slate-400">{session.message_count} tin nhắn</span></button>)}</div><div className="border-t border-white/10 p-4 text-sm">{user ? <><p className="font-semibold">{user.full_name}</p><p className="text-xs text-slate-400">{user.role}</p></> : <p className="text-slate-400">Khách chưa đăng nhập</p>}</div></aside>

    <main className="flex min-w-0 flex-1 flex-col"><header className="flex items-center justify-between border-b border-slate-100 bg-white px-4 py-4 sm:px-6"><div className="flex items-center gap-3"><span className="rounded-full bg-cyan-500 p-2.5 text-white"><FaRobot/></span><div><h1 className="font-bold">Trợ lý tìm nhà AI</h1><p className="text-xs text-slate-500">Tìm căn phù hợp, sau đó chọn lịch xem thực tế</p></div></div><div className="flex items-center gap-2"><Link href={propertyId ? `/booking/manual?property_id=${propertyId}` : "/booking/manual"} className="hidden rounded-lg border border-teal-200 px-3 py-2 text-xs font-semibold text-teal-700 hover:bg-teal-50 sm:block">Đặt lịch thủ công</Link><button onClick={newChat} className="rounded-lg border border-slate-200 p-2 md:hidden" aria-label="Cuộc trò chuyện mới"><FaPlus/></button></div></header>
      <div className="flex-1 overflow-y-auto p-4 sm:p-6"><div className="mx-auto max-w-4xl space-y-5">{messages.map((message,index)=><div key={`${message.role}-${index}`} className={message.role==="user" ? "flex justify-end" : "flex gap-3"}>{message.role==="assistant" && <span className="mt-1 h-fit rounded-full bg-cyan-500 p-2 text-white"><FaRobot/></span>}<div className="max-w-3xl"><div className={`rounded-2xl px-5 py-3 text-sm leading-relaxed ${message.role==="user" ? "rounded-tr-none bg-[#0b132b] text-white" : "rounded-tl-none border border-slate-100 bg-white text-slate-700 shadow-sm"}`}>{message.content}</div>{message.properties?.map((property)=><article key={property.id} className="mt-4 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm sm:flex"><div className="h-48 bg-slate-100 sm:h-auto sm:w-56">{(property.image || property.media?.[0]?.url) ? <img src={property.image || property.media[0].url} alt={property.title} className="h-full w-full object-cover"/> : <div className="flex h-full min-h-40 items-center justify-center text-4xl">🏠</div>}</div><div className="flex-1 p-5"><div className="flex flex-wrap justify-between gap-2"><h2 className="font-bold">{property.title}</h2><span className="font-bold text-indigo-700">{formatPrice(property.list_price)}</span></div><p className="mt-2 text-xs text-slate-500"><FaMapMarkerAlt className="mr-1 inline"/>{property.address_full || [property.address_line,property.district,property.province].filter(Boolean).join(", ")}</p><p className="mt-3 text-xs text-slate-600"><FaBed className="mr-1 inline text-teal-500"/>{property.bedrooms ?? 0} phòng ngủ · {property.area_sqm} m²</p><div className="mt-5 flex flex-wrap gap-2"><button onClick={()=>setSelected(property)} className="rounded-lg border border-slate-200 px-4 py-2 text-xs font-semibold hover:bg-slate-50">Chi tiết</button><button onClick={()=>save(property)} aria-pressed={savedIds.has(property.id)} className="rounded-lg border border-indigo-200 px-4 py-2 text-xs font-semibold text-indigo-700 hover:bg-indigo-50"><FaBookmark className="mr-1 inline"/>{savedIds.has(property.id) ? "Đã lưu" : "Lưu"}</button><button onClick={()=>book(property)} className="rounded-lg bg-indigo-700 px-4 py-2 text-xs font-semibold text-white hover:bg-indigo-800"><FaCalendarAlt className="mr-1 inline"/>Đặt lịch</button></div></div></article>)}</div></div>)}{loading && <div className="flex gap-3 text-sm text-slate-500"><FaRobot className="text-cyan-500"/>AI đang xử lý…</div>}{error && <div role="alert" className="rounded-xl bg-red-50 p-4 text-sm text-red-700"><p>{error}</p><Link href={propertyId ? `/booking/manual?property_id=${propertyId}` : "/booking/manual"} className="mt-3 inline-block rounded-lg bg-red-700 px-4 py-2 font-semibold text-white">Chuyển sang đặt lịch thủ công</Link></div>}<div ref={bottomRef}/></div></div>
      <form onSubmit={(event)=>void send(event)} className="border-t border-slate-100 bg-white p-4"><div className="relative mx-auto max-w-4xl"><label htmlFor="chat-input" className="sr-only">Tin nhắn</label><input id="chat-input" value={input} onChange={(event)=>setInput(event.target.value)} placeholder="Ví dụ: Tôi cần căn hộ 2 phòng ngủ ở Quận 2 dưới 5 tỷ" className="w-full rounded-xl border-2 border-slate-200 py-4 pl-4 pr-14 text-sm outline-none focus:border-indigo-600"/><button disabled={loading || !input.trim()} className="absolute right-2 top-2 rounded-lg bg-indigo-950 p-3 text-white disabled:opacity-40" aria-label="Gửi tin nhắn"><FaPaperPlane/></button></div></form>
    </main>

    {selected && <div role="dialog" aria-modal="true" aria-label="Chi tiết bất động sản" className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4"><div className="relative max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-2xl bg-white p-6"><button onClick={()=>setSelected(null)} className="absolute right-4 top-4 rounded-full bg-slate-100 p-2" aria-label="Đóng"><FaTimes/></button><h2 className="pr-10 text-2xl font-bold">{selected.title}</h2><p className="mt-2 font-bold text-indigo-700">{formatPrice(selected.list_price)}</p>{(selected.image || selected.media?.[0]?.url) && <img src={selected.image || selected.media[0].url} alt={selected.title} className="mt-5 h-72 w-full rounded-xl object-cover"/>}<p className="mt-5 whitespace-pre-line text-sm leading-7 text-slate-600">{selected.description || "Thông tin mô tả đang được cập nhật."}</p><div className="mt-6 flex gap-3"><Link href={`/properties/${selected.id}`} className="flex-1 rounded-xl border border-slate-200 py-3 text-center font-semibold">Trang chi tiết</Link><button onClick={()=>book(selected)} className="flex-1 rounded-xl bg-indigo-700 py-3 font-semibold text-white">Đặt lịch xem nhà</button></div></div></div>}
  </div>;
}

export default function ChatPage() { return <Suspense fallback={<div className="p-8">Đang tải chatbot…</div>}><ChatContent/></Suspense>; }
