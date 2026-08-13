/* eslint-disable @next/next/no-img-element */
"use client";

import { FormEvent, Suspense, useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FaBed, FaBookmark, FaBrain, FaCalendarAlt, FaCheck, FaCompass, FaEllipsisV, FaHistory, FaMagic, FaMapMarkerAlt, FaPaperPlane, FaPen, FaPlus, FaRegBookmark, FaShieldAlt, FaTimes, FaTrash } from "react-icons/fa";
import { useAuth } from "@/components/AuthProvider";
import { apiFetch } from "@/lib/api";
import { formatPropertyPrice } from "@/components/PropertyTile";
import type { Property } from "@/lib/types";

interface ChatMessage { role: "user" | "assistant"; content: string; properties?: Property[] }
interface ChatResponse { response: string; session_id: string; properties: Property[]; insights: Record<string, unknown>; memory_summary?: string }
interface SessionSummary { session_id: string; preview: string; message_count: number; last_active: string }
interface SessionDetail { messages: Array<{ role: string; content: string; properties?: Property[] }> }

const greeting: ChatMessage = { role: "assistant", content: "Chào bạn, tôi là Nera. Hãy kể tự nhiên về nơi bạn muốn sống — điều gì quan trọng, điều gì bạn không thích, hoặc một căn bạn đang cân nhắc." };

function ChatContent() {
  const { user } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const propertyId = searchParams.get("property_id");
  const initialPrompt = searchParams.get("prompt");
  const [messages, setMessages] = useState<ChatMessage[]>([greeting]);
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [sessionId, setSessionId] = useState(() => crypto.randomUUID());
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selected, setSelected] = useState<Property | null>(null);
  const [savedIds, setSavedIds] = useState<Set<string>>(new Set());
  const [savedProperties, setSavedProperties] = useState<Property[]>([]);
  const [memorySummary, setMemorySummary] = useState("");
  const [insights, setInsights] = useState<Record<string, unknown>>({});
  const [sessionMenu, setSessionMenu] = useState<string | null>(null);
  const [renamingSession, setRenamingSession] = useState<SessionSummary | null>(null);
  const [deletingSession, setDeletingSession] = useState<SessionSummary | null>(null);
  const [sessionTitle, setSessionTitle] = useState("");
  const [sessionActionLoading, setSessionActionLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const propertyLoaded = useRef(false);
  const promptSent = useRef(false);

  const loadSessions = useCallback(async () => { if (!user) { setSessions([]); return; } try { setSessions((await apiFetch<{ sessions: SessionSummary[] }>("/sessions")).sessions); } catch { setSessions([]); } }, [user]);
  const loadSavedProperties = useCallback(async () => { if (user?.role !== "CUSTOMER") { setSavedIds(new Set()); setSavedProperties([]); return; } try { const data = await apiFetch<{ ids: string[]; items: Property[] }>("/favorites"); setSavedIds(new Set(data.ids)); setSavedProperties(data.items ?? []); } catch { setSavedIds(new Set()); setSavedProperties([]); } }, [user]);
  const loadMemory = useCallback(async () => { if (user?.role !== "CUSTOMER") { setMemorySummary(""); return; } try { setMemorySummary((await apiFetch<{ summary: string }>("/memory")).summary); } catch { setMemorySummary(""); } }, [user]);

  useEffect(() => { const timer = window.setTimeout(() => { void loadSessions(); void loadSavedProperties(); void loadMemory(); }, 0); return () => window.clearTimeout(timer); }, [loadMemory, loadSavedProperties, loadSessions]);
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, loading]);
  useEffect(() => { if (!propertyId || propertyLoaded.current) return; propertyLoaded.current = true; void apiFetch<Property>(`/properties/${propertyId}`).then((property) => setMessages([greeting, { role: "assistant", content: `Bạn đang quan tâm “${property.title}”. Tôi đã mở căn này để mình cùng phân tích hoặc đặt lịch.`, properties: [property] }])).catch(() => setError("Không tìm thấy bất động sản này.")); }, [propertyId]);

  async function send(event?: FormEvent, quickText?: string) {
    event?.preventDefault();
    const text = (quickText ?? input).trim();
    if (!text || loading) return;
    setInput(""); setError(""); setLoading(true); setMessages((current) => [...current, { role: "user", content: text }]);
    try {
      const response = await apiFetch<ChatResponse>("/chat", { method: "POST", headers: { "X-Session-ID": sessionId }, body: JSON.stringify({ message: text }) });
      setSessionId(response.session_id || sessionId);
      setMessages((current) => [...current, { role: "assistant", content: response.response, properties: response.properties ?? [] }]);
      setInsights(response.insights ?? {});
      if (response.memory_summary) setMemorySummary(response.memory_summary);
      await loadSessions();
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Nera chưa phản hồi được."); }
    finally { setLoading(false); }
  }

  useEffect(() => {
    if (!initialPrompt || promptSent.current) return;
    const timer = window.setTimeout(() => { if (!promptSent.current) { promptSent.current = true; void send(undefined, initialPrompt); } }, 0);
    return () => window.clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialPrompt]);

  async function loadSession(id: string) { try { const data = await apiFetch<SessionDetail>(`/session/${id}`); setSessionId(id); setMessages(data.messages.map((message) => ({ role: message.role.toLowerCase() === "user" ? "user" : "assistant", content: message.content, properties: message.properties }))); setError(""); } catch { setError("Không tải được cuộc trò chuyện."); } }
  function newChat() { setSessionId(crypto.randomUUID()); setMessages([greeting]); setInput(""); setError(""); setInsights({}); router.replace("/chat"); }
  function beginRename(session: SessionSummary) { setSessionMenu(null); setRenamingSession(session); setSessionTitle(session.preview); }
  async function renameSession(event: FormEvent) {
    event.preventDefault();
    const title = sessionTitle.trim();
    if (!renamingSession || !title || sessionActionLoading) return;
    setSessionActionLoading(true);
    try {
      await apiFetch(`/session/${renamingSession.session_id}`, { method: "PATCH", body: JSON.stringify({ title }) });
      setSessions((current) => current.map((item) => item.session_id === renamingSession.session_id ? { ...item, preview: title } : item));
      setRenamingSession(null);
      setSessionTitle("");
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Không thể đổi tên cuộc trò chuyện."); }
    finally { setSessionActionLoading(false); }
  }
  async function deleteSession() {
    if (!deletingSession || sessionActionLoading) return;
    setSessionActionLoading(true);
    try {
      await apiFetch(`/session/${deletingSession.session_id}`, { method: "DELETE" });
      setSessions((current) => current.filter((item) => item.session_id !== deletingSession.session_id));
      if (deletingSession.session_id === sessionId) newChat();
      setDeletingSession(null);
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Không thể xóa cuộc trò chuyện."); }
    finally { setSessionActionLoading(false); }
  }
  async function save(property: Property) { if (!user) { router.push("/login?next=/chat"); return; } if (user.role !== "CUSTOMER") { setError("Chỉ tài khoản khách hàng có thể lưu nhà."); return; } const saved = savedIds.has(property.id); try { await apiFetch(`/favorites/${property.id}`, { method: saved ? "DELETE" : "PUT" }); await loadSavedProperties(); } catch { setError("Không thể cập nhật nhà đã lưu."); } }
  function book(property: Property) { if (!user) { router.push(`/login?next=${encodeURIComponent(`/booking/schedule?property_id=${property.id}`)}`); return; } if (user.role !== "CUSTOMER") { setError("Chỉ tài khoản khách hàng có thể đặt lịch xem nhà."); return; } router.push(`/booking/schedule?property_id=${property.id}`); }

  const latestMatches = useMemo(() => [...messages].reverse().find((message) => message.properties?.length)?.properties ?? [], [messages]);
  const insightItems = useMemo(() => Object.entries(insights).filter(([, value]) => value !== null && value !== "" && (!Array.isArray(value) || value.length)).slice(0, 4), [insights]);

  return <div className="flex h-screen overflow-hidden bg-[var(--paper)] text-[var(--ink)]">
    <aside className="hidden w-72 shrink-0 flex-col bg-[var(--ink)] text-white lg:flex">
      <div className="border-b border-white/10 p-5"><Link href="/" className="flex items-center gap-3 font-semibold"><span className="grid h-10 w-10 place-items-center rounded-2xl bg-white/10"><FaMagic className="text-[#a9c9b0]" /></span><span>Nera<small className="block text-[10px] font-medium uppercase tracking-[.16em] text-white/45">AI home companion</small></span></Link></div>
      <div className="p-4"><button onClick={newChat} className="flex w-full items-center justify-center gap-2 rounded-2xl bg-white py-3 text-sm font-semibold text-[var(--ink)] transition hover:bg-[#e7eee7]"><FaPlus /> Cuộc trò chuyện mới</button></div>
      <div className="flex-1 overflow-y-auto px-4 pb-4"><p className="mb-3 flex items-center gap-2 text-xs uppercase tracking-wider text-white/35"><FaHistory /> Lịch sử</p>{!user ? <Link href="/login?next=/chat" className="text-sm text-[#a9c9b0] hover:underline">Đăng nhập để lưu lịch sử</Link> : sessions.length === 0 ? <p className="text-sm text-white/40">Chưa có cuộc trò chuyện.</p> : <div className="space-y-2">{sessions.map((session) => <div key={session.session_id} className={`group relative rounded-xl transition ${session.session_id === sessionId ? "bg-white/12" : "hover:bg-white/7"}`}><button onClick={() => { setSessionMenu(null); void loadSession(session.session_id); }} className="w-full p-3 pr-10 text-left text-sm"><span className="block truncate">{session.preview}</span><span className="text-xs text-white/35">{session.message_count} tin nhắn</span></button><button onClick={(event) => { event.stopPropagation(); setSessionMenu((current) => current === session.session_id ? null : session.session_id); }} aria-label={`Tùy chọn cho ${session.preview}`} aria-expanded={sessionMenu === session.session_id} className={`absolute right-2 top-1/2 grid h-8 w-8 -translate-y-1/2 place-items-center rounded-lg text-white/55 transition hover:bg-white/10 hover:text-white focus:opacity-100 ${sessionMenu === session.session_id ? "bg-white/10 opacity-100" : "opacity-0 group-hover:opacity-100"}`}><FaEllipsisV /></button>{sessionMenu === session.session_id && <div className="absolute right-2 top-[calc(50%+20px)] z-20 w-40 overflow-hidden rounded-xl border border-white/10 bg-[#243b34] py-1 shadow-2xl"><button onClick={() => beginRename(session)} className="flex w-full items-center gap-2 px-3 py-2.5 text-left text-xs hover:bg-white/10"><FaPen /> Đổi tên</button><button onClick={() => { setSessionMenu(null); setDeletingSession(session); }} className="flex w-full items-center gap-2 px-3 py-2.5 text-left text-xs text-[#ffb4a0] hover:bg-white/10"><FaTrash /> Xóa</button></div>}</div>)}</div>}</div>
      <div className="border-t border-white/10 p-4 text-sm">{user ? <><p className="font-semibold">{user.full_name}</p><p className="text-xs text-white/40">Dữ liệu riêng theo tài khoản</p></> : <p className="text-white/40">Bạn đang trò chuyện ẩn danh</p>}</div>
    </aside>

    <main className="flex min-w-0 flex-1 flex-col">
      <header className="flex items-center justify-between border-b border-black/5 bg-white/85 px-4 py-4 backdrop-blur sm:px-6"><div className="flex items-center gap-3"><span className="grid h-10 w-10 place-items-center rounded-2xl bg-[var(--forest)] text-white"><FaMagic /></span><div><h1 className="font-semibold">Nera đang ở đây</h1><p className="text-xs text-[var(--muted)]">Nói tự nhiên, không cần điền form</p></div></div><div className="flex items-center gap-2"><Link href="/properties" className="hidden rounded-full border border-black/10 px-4 py-2 text-xs font-semibold sm:block">Kho nhà</Link><Link href={propertyId ? `/booking/manual?property_id=${propertyId}` : "/booking/manual"} className="hidden rounded-full bg-[#eef3ee] px-4 py-2 text-xs font-semibold text-[var(--forest)] sm:block">Đặt lịch thủ công</Link><button onClick={newChat} className="rounded-xl border border-black/10 p-2 lg:hidden" aria-label="Cuộc trò chuyện mới"><FaPlus /></button></div></header>
      <div className="flex-1 overflow-y-auto p-4 sm:p-6"><div className="mx-auto max-w-3xl space-y-6">{messages.map((message, index) => <div key={`${message.role}-${index}`} className={`animate-message-in ${message.role === "user" ? "flex justify-end" : "flex gap-3"}`}>{message.role === "assistant" && <span className="mt-1 grid h-9 w-9 shrink-0 place-items-center rounded-2xl bg-[var(--forest)] text-white"><FaMagic /></span>}<div className="max-w-2xl"><div className={`whitespace-pre-line rounded-[1.35rem] px-5 py-3.5 text-[15px] leading-7 ${message.role === "user" ? "rounded-tr-md bg-[var(--ink)] text-white" : "rounded-tl-md border border-black/5 bg-white shadow-sm"}`}>{message.content}</div>{message.properties?.map((property, propertyIndex) => <article key={property.id} style={{ animationDelay: `${propertyIndex * 80}ms` }} className="animate-card-rise mt-4 overflow-hidden rounded-[1.5rem] border border-black/5 bg-white shadow-[0_14px_40px_rgba(22,47,42,.08)] sm:flex"><div className="h-48 bg-stone-100 sm:h-auto sm:w-48">{(property.image || property.media?.[0]?.url) ? <img src={property.image || property.media[0].url} alt={property.title} className="h-full w-full object-cover" /> : <div className="grid h-full min-h-40 place-items-center text-4xl">🏠</div>}</div><div className="flex-1 p-5"><div className="flex flex-wrap justify-between gap-2"><h2 className="max-w-sm font-semibold leading-6">{property.title}</h2><span className="font-semibold text-[var(--coral)]">{formatPropertyPrice(property.list_price)}</span></div><p className="mt-2 text-xs text-[var(--muted)]"><FaMapMarkerAlt className="mr-1 inline" />{property.address_full || [property.address_line, property.district, property.province].filter(Boolean).join(", ")}</p><p className="mt-3 text-xs text-[var(--muted)]"><FaBed className="mr-1 inline text-[var(--forest)]" />{property.bedrooms ?? 0} phòng ngủ · {property.area_sqm} m²</p><div className="mt-5 flex flex-wrap gap-2"><button onClick={() => setSelected(property)} className="rounded-full border border-black/10 px-4 py-2 text-xs font-semibold">Chi tiết</button><button onClick={() => void save(property)} aria-pressed={savedIds.has(property.id)} className="rounded-full border border-[var(--sage)]/50 px-4 py-2 text-xs font-semibold text-[var(--forest)]">{savedIds.has(property.id) ? <FaBookmark className="mr-1 inline" /> : <FaRegBookmark className="mr-1 inline" />}{savedIds.has(property.id) ? "Đã lưu" : "Lưu"}</button><button onClick={() => book(property)} className="rounded-full bg-[var(--forest)] px-4 py-2 text-xs font-semibold text-white"><FaCalendarAlt className="mr-1 inline" />Đặt lịch xem</button></div></div></article>)}</div></div>)}
        {loading && <div className="flex animate-message-in items-start gap-3"><span className="grid h-9 w-9 place-items-center rounded-2xl bg-[var(--forest)] text-white"><FaMagic /></span><div className="flex gap-1 rounded-[1.35rem] rounded-tl-md bg-white px-5 py-5 shadow-sm"><i className="typing-dot" /><i className="typing-dot [animation-delay:150ms]" /><i className="typing-dot [animation-delay:300ms]" /></div></div>}
        {error && <div role="alert" className="rounded-2xl border border-red-100 bg-red-50 p-4 text-sm text-red-700"><p>{error}</p><Link href={propertyId ? `/booking/manual?property_id=${propertyId}` : "/booking/manual"} className="mt-3 inline-block rounded-full bg-red-700 px-4 py-2 font-semibold text-white">Chuyển sang đặt lịch thủ công</Link></div>}<div ref={bottomRef} /></div></div>
      <form onSubmit={(event) => void send(event)} className="border-t border-black/5 bg-white p-4"><div className="relative mx-auto max-w-3xl"><input aria-label="Tin nhắn" value={input} onChange={(event) => setInput(event.target.value)} placeholder="Nói điều bạn thích, không thích hoặc muốn thay đổi…" className="w-full rounded-2xl border border-black/10 bg-[#fbfaf7] py-4 pl-5 pr-14 text-sm outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10" /><button disabled={loading || !input.trim()} className="absolute right-2 top-2 grid h-10 w-10 place-items-center rounded-xl bg-[var(--ink)] text-white transition hover:scale-105 disabled:opacity-30" aria-label="Gửi tin nhắn"><FaPaperPlane /></button></div><p className="mx-auto mt-2 max-w-3xl text-center text-[10px] text-stone-400">Nera dùng dữ liệu hệ thống làm nguồn sự thật và không tự xác nhận lịch thay Sale.</p></form>
    </main>

    <aside className="hidden w-80 shrink-0 flex-col border-l border-black/5 bg-white xl:flex"><div className="border-b border-black/5 p-5"><p className="text-xs font-bold uppercase tracking-[.16em] text-[var(--coral)]">Bảng đồng hành</p><h2 className="mt-2 font-semibold">Nera hiểu gì về bạn</h2></div><div className="flex-1 space-y-5 overflow-y-auto p-5">
      <section className="rounded-2xl bg-[#edf3ed] p-4"><p className="flex items-center gap-2 text-xs font-bold uppercase tracking-[.12em] text-[var(--forest)]"><FaBrain /> Hồ sơ nhu cầu</p><p className="mt-3 text-sm leading-6 text-[var(--muted)]">{memorySummary || "Cứ trò chuyện, Nera sẽ tóm tắt sở thích quan trọng tại đây."}</p>{insightItems.length > 0 && <div className="mt-3 flex flex-wrap gap-2">{insightItems.map(([key, value]) => <span key={key} className="rounded-full bg-white px-3 py-1.5 text-[10px] font-semibold text-[var(--forest)]">{Array.isArray(value) ? value.join(", ") : String(value)}</span>)}</div>}{memorySummary && <button onClick={() => void apiFetch<void>("/memory", { method: "DELETE" }).then(() => setMemorySummary(""))} className="mt-3 text-[11px] text-[var(--muted)] underline">Xóa memory</button>}</section>
      <section><div className="flex items-center justify-between"><h3 className="flex items-center gap-2 text-sm font-semibold"><FaCompass className="text-[var(--forest)]" /> Kết quả gần nhất</h3><Link href="/properties" className="text-[11px] font-semibold text-[var(--forest)]">Xem kho nhà</Link></div>{latestMatches.length ? <div className="mt-3 space-y-3">{latestMatches.slice(0, 3).map((property) => <button key={property.id} onClick={() => setSelected(property)} className="flex w-full gap-3 rounded-xl border border-black/5 p-2 text-left transition hover:bg-stone-50">{(property.image || property.media?.[0]?.url) ? <img src={property.image || property.media[0].url} alt="" className="h-14 w-16 rounded-lg object-cover" /> : <div className="grid h-14 w-16 place-items-center rounded-lg bg-stone-100">🏡</div>}<span className="min-w-0"><strong className="line-clamp-2 text-xs leading-4">{property.title}</strong><small className="mt-1 block text-[var(--coral)]">{formatPropertyPrice(property.list_price)}</small></span></button>)}</div> : <p className="mt-3 text-xs leading-5 text-[var(--muted)]">Nhà phù hợp sẽ xuất hiện sau khi Nera hiểu đủ nhu cầu.</p>}</section>
      <section><div className="flex items-center justify-between"><h3 className="flex items-center gap-2 text-sm font-semibold"><FaBookmark className="text-[var(--forest)]" /> Đã lưu</h3><span className="text-xs text-[var(--muted)]">{savedProperties.length}</span></div>{savedProperties.length ? <div className="mt-3 space-y-2">{savedProperties.slice(0, 3).map((property) => <Link href={`/properties/${property.id}`} key={property.id} className="block truncate rounded-xl bg-[#fbfaf7] px-3 py-2.5 text-xs font-medium hover:bg-stone-100">{property.title}</Link>)}</div> : <p className="mt-3 text-xs text-[var(--muted)]">Các căn bạn lưu sẽ nằm ở đây và trong tài khoản.</p>}</section>
      <section className="rounded-2xl border border-black/5 p-4"><p className="flex items-center gap-2 text-xs font-semibold"><FaShieldAlt className="text-[var(--forest)]" /> Quy trình minh bạch</p><ol className="mt-3 space-y-2 text-xs text-[var(--muted)]">{["Nera tìm và giải thích", "Bạn chọn căn muốn xem", "Sale xác nhận khung giờ"].map((item, index) => <li key={item} className="flex items-center gap-2"><span className="grid h-5 w-5 place-items-center rounded-full bg-[#edf3ed] text-[9px] font-bold text-[var(--forest)]">{index + 1}</span>{item}</li>)}</ol></section>
    </div></aside>

    {renamingSession && <div role="dialog" aria-modal="true" aria-labelledby="rename-chat-title" className="fixed inset-0 z-50 grid place-items-center bg-black/55 p-4"><form onSubmit={(event) => void renameSession(event)} className="w-full max-w-md animate-message-in rounded-[1.7rem] bg-white p-6 shadow-2xl"><div className="flex items-center justify-between"><h2 id="rename-chat-title" className="text-xl font-semibold">Đổi tên cuộc trò chuyện</h2><button type="button" onClick={() => setRenamingSession(null)} className="grid h-9 w-9 place-items-center rounded-full bg-stone-100" aria-label="Đóng"><FaTimes /></button></div><p className="mt-2 text-sm text-[var(--muted)]">Đặt tên ngắn để dễ tìm lại trong lịch sử.</p><input autoFocus maxLength={80} value={sessionTitle} onChange={(event) => setSessionTitle(event.target.value)} className="mt-5 w-full rounded-xl border border-black/10 px-4 py-3 outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10" aria-label="Tên cuộc trò chuyện" /><div className="mt-2 text-right text-xs text-[var(--muted)]">{sessionTitle.length}/80</div><div className="mt-5 flex gap-3"><button type="button" onClick={() => setRenamingSession(null)} className="flex-1 rounded-full border border-black/10 py-2.5 font-semibold">Hủy</button><button disabled={!sessionTitle.trim() || sessionActionLoading} className="flex-1 rounded-full bg-[var(--forest)] py-2.5 font-semibold text-white disabled:opacity-40">{sessionActionLoading ? "Đang lưu…" : "Lưu tên"}</button></div></form></div>}

    {deletingSession && <div role="dialog" aria-modal="true" aria-labelledby="delete-chat-title" className="fixed inset-0 z-50 grid place-items-center bg-black/55 p-4"><div className="w-full max-w-md animate-message-in rounded-[1.7rem] bg-white p-6 shadow-2xl"><span className="grid h-12 w-12 place-items-center rounded-2xl bg-red-50 text-red-600"><FaTrash /></span><h2 id="delete-chat-title" className="mt-5 text-xl font-semibold">Xóa cuộc trò chuyện?</h2><p className="mt-2 text-sm leading-6 text-[var(--muted)]">“{deletingSession.preview}” và toàn bộ tin nhắn bên trong sẽ bị xóa vĩnh viễn.</p><div className="mt-6 flex gap-3"><button onClick={() => setDeletingSession(null)} className="flex-1 rounded-full border border-black/10 py-2.5 font-semibold">Giữ lại</button><button onClick={() => void deleteSession()} disabled={sessionActionLoading} className="flex-1 rounded-full bg-red-600 py-2.5 font-semibold text-white disabled:opacity-40">{sessionActionLoading ? "Đang xóa…" : "Xóa lịch sử"}</button></div></div></div>}

    {selected && <div role="dialog" aria-modal="true" className="fixed inset-0 z-50 grid place-items-center bg-black/60 p-4"><div className="relative max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-[1.7rem] bg-white p-6"><button onClick={() => setSelected(null)} className="absolute right-4 top-4 rounded-full bg-slate-100 p-2" aria-label="Đóng"><FaTimes /></button><h2 className="pr-10 text-2xl font-bold">{selected.title}</h2><p className="mt-2 font-bold text-[var(--coral)]">{formatPropertyPrice(selected.list_price)}</p>{(selected.image || selected.media?.[0]?.url) && <img src={selected.image || selected.media[0].url} alt={selected.title} className="mt-5 h-72 w-full rounded-xl object-cover" />}<p className="mt-5 whitespace-pre-line text-sm leading-7 text-slate-600">{selected.description || "Thông tin mô tả đang được cập nhật."}</p><div className="mt-6 flex gap-3"><Link href={`/properties/${selected.id}`} className="flex-1 rounded-xl border border-slate-200 py-3 text-center font-semibold"><FaCheck className="mr-1 inline" /> Trang chi tiết</Link><button onClick={() => book(selected)} className="flex-1 rounded-xl bg-[var(--forest)] py-3 font-semibold text-white">Đặt lịch xem nhà</button></div></div></div>}
  </div>;
}

export default function ChatPage() { return <Suspense fallback={<div className="grid min-h-screen place-items-center bg-[var(--paper)]">Đang mở Nera…</div>}><ChatContent /></Suspense>; }
