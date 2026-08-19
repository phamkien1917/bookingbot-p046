import { useMemo } from "react";
import { FaBrain, FaCheck, FaTimes, FaMagic, FaHistory, FaBookmark } from "react-icons/fa";
import type { Property } from "@/lib/types";
import { formatPropertyPrice } from "@/components/PropertyTile";

const INSIGHT_LABELS: Record<string, string> = {
  district: "Khu vực",
  province: "Tỉnh/TP",
  property_kind: "Loại nhà",
  bedrooms: "Phòng ngủ",
  min_price: "Giá từ",
  max_price: "Giá tới",
  budget: "Ngân sách",
  keyword: "Từ khoá",
  features: "Tiện ích",
  move_in: "Chuyển vào",
};

function formatInsightValue(key: string, value: unknown): string {
  if (Array.isArray(value)) return value.join(", ");
  if (key.includes("price") || key === "budget") {
    const num = Number(value);
    if (num >= 1_000_000_000) return `${(num / 1_000_000_000).toFixed(1)} tỷ`;
    if (num >= 1_000_000) return `${(num / 1_000_000).toFixed(0)} triệu`;
  }
  return String(value);
}

// ────────────────────────────────────────────────────────────
// AI Insights Sidebar Panel
// ────────────────────────────────────────────────────────────
function InsightsSidebar({ insights, memorySummary, savedProperties, latestMatches, onSelectProperty, onClearMemory }: {
  insights: Record<string, unknown>;
  memorySummary: string;
  savedProperties: Property[];
  latestMatches: Property[];
  onSelectProperty: (p: Property) => void;
  onClearMemory: () => void;
}) {
  const insightEntries = useMemo(
    () => Object.entries(insights).filter(([, v]) => v !== null && v !== "" && (!Array.isArray(v) || (v as unknown[]).length > 0)),
    [insights]
  );

  const totalFields = 6; // budget, bedrooms, district, property_kind, move_in, family_size
  const progress = Math.min(100, Math.round((insightEntries.length / totalFields) * 100));

  const ASKED_FIELDS = ["max_price", "bedrooms", "district", "property_kind", "move_in", "family_size"];
  const missing = ASKED_FIELDS.filter(f => !insights[f]);

  return (
    <aside className="hidden w-80 shrink-0 flex-col border-l border-black/5 bg-white xl:flex">
      <div className="border-b border-black/5 p-5">
        <p className="text-xs font-bold uppercase tracking-[.16em] text-[var(--coral)]">AI đang hiểu gì về bạn</p>
        <h2 className="mt-1 font-semibold">Hồ sơ nhu cầu</h2>
        <div className="mt-3">
          <div className="flex justify-between text-xs text-[var(--muted)] mb-1">
            <span>Mức độ hoàn thiện</span>
            <span className="font-bold text-[var(--forest)]">{progress}%</span>
          </div>
          <div className="h-1.5 rounded-full bg-black/8">
            <div
              className="h-full rounded-full bg-[var(--forest)] transition-all duration-700"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      </div>

      <div className="flex-1 space-y-5 overflow-y-auto p-5">
        {/* Collected criteria */}
        {insightEntries.length > 0 && (
          <section>
            <p className="flex items-center gap-2 text-xs font-bold uppercase tracking-[.1em] text-[var(--muted)] mb-2">
              <FaCheck className="text-emerald-500" /> Đã thu thập
            </p>
            <div className="space-y-2">
              {insightEntries.map(([key, value]) => (
                <div key={key} className="flex items-center justify-between rounded-xl bg-[#f0f5f1] px-3 py-2">
                  <span className="text-[10px] font-semibold uppercase tracking-wide text-[var(--muted)]">
                    {INSIGHT_LABELS[key] ?? key}
                  </span>
                  <span className="text-xs font-semibold text-[var(--forest)] text-right max-w-[55%] line-clamp-1">
                    {formatInsightValue(key, value)}
                  </span>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Still missing */}
        {missing.length > 0 && (
          <section>
            <p className="flex items-center gap-2 text-xs font-bold uppercase tracking-[.1em] text-[var(--muted)] mb-2">
              <FaBrain className="text-[var(--coral)]" /> Cần làm rõ
            </p>
            <div className="space-y-1">
              {missing.slice(0, 3).map(field => (
                <div key={field} className="flex items-center gap-2 rounded-xl border border-dashed border-black/10 px-3 py-2">
                  <span className="h-1.5 w-1.5 rounded-full bg-amber-400 shrink-0" />
                  <span className="text-xs text-[var(--muted)]">{INSIGHT_LABELS[field] ?? field}</span>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Memory long-term */}
        {memorySummary && (
          <section className="rounded-2xl bg-[#edf3ed] p-4">
            <p className="flex items-center gap-2 text-xs font-bold uppercase tracking-[.1em] text-[var(--forest)]">
              <FaBrain /> Memory dài hạn
            </p>
            <p className="mt-2 text-xs leading-5 text-[var(--muted)]">{memorySummary}</p>
            <div className="mt-3 flex items-center justify-between">
              <Link href="/memory" className="text-[11px] font-semibold text-[var(--forest)] hover:underline">
                Xem & chỉnh sửa →
              </Link>
              <button onClick={onClearMemory} className="text-[11px] text-[var(--muted)] hover:text-red-500">Xóa</button>
            </div>
          </section>
        )}

        {/* Latest matches */}
        {latestMatches.length > 0 && (
          <section>
            <div className="flex items-center justify-between mb-2">
              <h3 className="flex items-center gap-2 text-sm font-semibold">
                <FaCompass className="text-[var(--forest)]" /> Gợi ý gần nhất
              </h3>
            </div>
            <div className="space-y-2">
              {latestMatches.slice(0, 3).map(property => (
                <button key={property.id} onClick={() => onSelectProperty(property)}
                  className="flex w-full gap-3 rounded-xl border border-black/5 p-2 text-left transition hover:bg-stone-50">
                  {(property.image || property.media?.[0]?.url)
                    ? <img src={property.image || property.media[0].url} alt="" className="h-14 w-14 rounded-lg object-cover shrink-0" />
                    : <div className="grid h-14 w-14 place-items-center rounded-lg bg-stone-100 shrink-0">🏡</div>}
                  <span className="min-w-0">
                    <strong className="line-clamp-2 text-xs leading-4">{property.title}</strong>
                    <small className="mt-1 block text-[var(--coral)]">{formatPropertyPrice(property.list_price)}</small>
                  </span>
                </button>
              ))}
            </div>
          </section>
        )}

        {/* Saved */}
        {savedProperties.length > 0 && (
          <section>
            <div className="flex items-center justify-between mb-2">
              <h3 className="flex items-center gap-2 text-sm font-semibold">
                <FaBookmark className="text-[var(--forest)]" /> Đã lưu
              </h3>
              <Link href="/saved" className="text-[11px] font-semibold text-[var(--forest)]">Xem tất cả</Link>
            </div>
            {savedProperties.slice(0, 3).map(p => (
              <Link href={`/properties/${p.id}`} key={p.id}
                className="block truncate rounded-xl bg-[#fbfaf7] px-3 py-2.5 text-xs font-medium hover:bg-stone-100 mb-1">
                {p.title}
              </Link>
            ))}
          </section>
        )}

        {/* Compare CTA */}
        {savedProperties.length >= 2 && (
          <Link href="/compare"
            className="flex items-center justify-center gap-2 rounded-2xl border border-[var(--sage)]/40 bg-[#f0f5f1] px-4 py-3 text-xs font-semibold text-[var(--forest)] hover:bg-[#e0ece2]">
            So sánh {savedProperties.length} căn đã lưu →
          </Link>
        )}

        {/* Trust */}
        <section className="rounded-2xl border border-black/5 p-4">
          <p className="flex items-center gap-2 text-xs font-semibold">
            <FaShieldAlt className="text-[var(--forest)]" /> Quy trình minh bạch
          </p>
          <ol className="mt-3 space-y-2 text-xs text-[var(--muted)]">
            {["Nera tìm và giải thích lý do", "Bạn chọn căn muốn xem", "Sale xác nhận khung giờ thật"].map((item, i) => (
              <li key={item} className="flex items-center gap-2">
                <span className="grid h-5 w-5 place-items-center rounded-full bg-[#edf3ed] text-[9px] font-bold text-[var(--forest)]">{i + 1}</span>
                {item}
              </li>
            ))}
          </ol>
        </section>
      </div>
    </aside>
  );
}

// ────────────────────────────────────────────────────────────
// Main Chat Content
// ────────────────────────────────────────────────────────────
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
  const [feedbackProperty, setFeedbackProperty] = useState<Property | null>(null);
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

  const loadSessions = useCallback(async () => {
    if (!user) { setSessions([]); return; }
    try { setSessions((await apiFetch<{ sessions: SessionSummary[] }>("/sessions")).sessions); } catch { setSessions([]); }
  }, [user]);

  const loadSavedProperties = useCallback(async () => {
    if (user?.role !== "CUSTOMER") { setSavedIds(new Set()); setSavedProperties([]); return; }
    try {
      const data = await apiFetch<{ ids: string[]; items: Property[] }>("/favorites");
      setSavedIds(new Set(data.ids)); setSavedProperties(data.items ?? []);
    } catch { setSavedIds(new Set()); setSavedProperties([]); }
  }, [user]);

  const loadMemory = useCallback(async () => {
    if (user?.role !== "CUSTOMER") { setMemorySummary(""); return; }
    try { setMemorySummary((await apiFetch<{ summary: string }>("/memory")).summary); } catch { setMemorySummary(""); }
  }, [user]);

  useEffect(() => {
    const t = window.setTimeout(() => { void loadSessions(); void loadSavedProperties(); void loadMemory(); }, 0);
    return () => window.clearTimeout(t);
  }, [loadMemory, loadSavedProperties, loadSessions]);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, loading]);

  useEffect(() => {
    if (!propertyId || propertyLoaded.current) return;
    propertyLoaded.current = true;
    void apiFetch<Property>(`/properties/${propertyId}`)
      .then(p => setMessages([greeting, { role: "assistant", content: `Bạn đang quan tâm "${p.title}". Tôi đã mở căn này để mình cùng phân tích hoặc đặt lịch.`, properties: [p] }]))
      .catch(() => setError("Không tìm thấy bất động sản này."));
  }, [propertyId]);

  async function send(event?: FormEvent, quickText?: string) {
    event?.preventDefault();
    const text = (quickText ?? input).trim();
    if (!text || loading) return;
    setInput(""); setError(""); setLoading(true);
    setMessages(cur => [...cur, { role: "user", content: text }]);
    try {
      const res = await apiFetch<ChatResponse>("/chat", {
        method: "POST",
        headers: { "X-Session-ID": sessionId },
        body: JSON.stringify({ message: text })
      });
      setSessionId(res.session_id || sessionId);
      const chips = deriveQuickReplies(res.response);
      setMessages(cur => [...cur, { role: "assistant", content: res.response, properties: res.properties ?? [], quickReplies: chips }]);
      setInsights(res.insights ?? {});
      if (res.memory_summary) setMemorySummary(res.memory_summary);
      void loadSessions();
    } catch (err) { setError(err instanceof Error ? err.message : "Nera chưa phản hồi được."); }
    finally { setLoading(false); }
  }

  useEffect(() => {
    if (!initialPrompt || promptSent.current) return;
    const t = window.setTimeout(() => { if (!promptSent.current) { promptSent.current = true; void send(undefined, initialPrompt); } }, 0);
    return () => window.clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialPrompt]);

  async function loadSession(id: string) {
    try {
      const data = await apiFetch<SessionDetail>(`/session/${id}`);
      setSessionId(id);
      setMessages(data.messages.map(m => ({ role: m.role.toLowerCase() === "user" ? "user" : "assistant", content: m.content, properties: m.properties })));
      setError("");
    } catch { setError("Không tải được cuộc trò chuyện."); }
  }

  function newChat() { setSessionId(crypto.randomUUID()); setMessages([greeting]); setInput(""); setError(""); setInsights({}); router.replace("/chat"); }

  function beginRename(s: SessionSummary) { setSessionMenu(null); setRenamingSession(s); setSessionTitle(s.preview); }

  async function renameSession(e: FormEvent) {
    e.preventDefault();
    const title = sessionTitle.trim();
    if (!renamingSession || !title || sessionActionLoading) return;
    setSessionActionLoading(true);
    try {
      await apiFetch(`/session/${renamingSession.session_id}`, { method: "PATCH", body: JSON.stringify({ title }) });
      setSessions(cur => cur.map(item => item.session_id === renamingSession.session_id ? { ...item, preview: title } : item));
      setRenamingSession(null); setSessionTitle("");
    } catch (err) { setError(err instanceof Error ? err.message : "Không thể đổi tên."); }
    finally { setSessionActionLoading(false); }
  }

  async function deleteSession() {
    if (!deletingSession || sessionActionLoading) return;
    setSessionActionLoading(true);
    try {
      await apiFetch(`/session/${deletingSession.session_id}`, { method: "DELETE" });
      setSessions(cur => cur.filter(item => item.session_id !== deletingSession.session_id));
      if (deletingSession.session_id === sessionId) newChat();
      setDeletingSession(null);
    } catch (err) { setError(err instanceof Error ? err.message : "Không thể xóa."); }
    finally { setSessionActionLoading(false); }
  }

  async function save(property: Property) {
    if (!user) { router.push("/login?next=/chat"); return; }
    if (user.role !== "CUSTOMER") { setError("Chỉ tài khoản khách hàng có thể lưu nhà."); return; }
    const saved = savedIds.has(property.id);
    try { await apiFetch(`/favorites/${property.id}`, { method: saved ? "DELETE" : "PUT" }); await loadSavedProperties(); }
    catch { setError("Không thể cập nhật nhà đã lưu."); }
  }

  function book(property: Property) {
    if (!user) { router.push(`/login?next=${encodeURIComponent(`/booking/schedule?property_id=${property.id}`)}`); return; }
    if (user.role !== "CUSTOMER") { setError("Chỉ tài khoản khách hàng có thể đặt lịch xem nhà."); return; }
    router.push(`/booking/schedule?property_id=${property.id}`);
  }

  // Send feedback as a chat message (silent)
  async function submitFeedback(text: string) {
    setLoading(true);
    setMessages(cur => [...cur, { role: "user", content: text }]);
    try {
      const res = await apiFetch<ChatResponse>("/chat", {
        method: "POST",
        headers: { "X-Session-ID": sessionId },
        body: JSON.stringify({ message: text })
      });
      const chips = deriveQuickReplies(res.response);
      setMessages(cur => [...cur, { role: "assistant", content: res.response, properties: res.properties ?? [], quickReplies: chips }]);
      setInsights(res.insights ?? {});
      if (res.memory_summary) setMemorySummary(res.memory_summary);
      void loadSessions();
    } catch { /* silent */ }
    finally { setLoading(false); }
  }

  const latestMatches = useMemo(() => [...messages].reverse().find(m => m.properties?.length)?.properties ?? [], [messages]);

  return (
    <div className="flex h-screen overflow-hidden bg-[var(--paper)] text-[var(--ink)]">
      {/* ── Left sidebar: session history ── */}
      <aside className="hidden w-72 shrink-0 flex-col bg-[var(--ink)] text-white lg:flex">
        <div className="border-b border-white/10 p-5">
          <Link href="/" className="flex items-center gap-3 font-semibold">
            <span className="grid h-10 w-10 place-items-center rounded-2xl bg-white/10"><FaMagic className="text-[#a9c9b0]" /></span>
            <span>Nera<small className="block text-[10px] font-medium uppercase tracking-[.16em] text-white/45">AI home companion</small></span>
          </Link>
        </div>
        <div className="p-4">
          <button onClick={newChat} className="flex w-full items-center justify-center gap-2 rounded-2xl bg-white py-3 text-sm font-semibold text-[var(--ink)] transition hover:bg-[#e7eee7]">
            <FaPlus /> Cuộc trò chuyện mới
          </button>
        </div>
        <div className="flex-1 overflow-y-auto px-4 pb-4">
          <p className="mb-3 flex items-center gap-2 text-xs uppercase tracking-wider text-white/35"><FaHistory /> Lịch sử</p>
          {!user
            ? <Link href="/login?next=/chat" className="text-sm text-[#a9c9b0] hover:underline">Đăng nhập để lưu lịch sử</Link>
            : sessions.length === 0
              ? <p className="text-sm text-white/40">Chưa có cuộc trò chuyện.</p>
              : <div className="space-y-2">
                {sessions.map(session => (
                  <div key={session.session_id} className={`group relative rounded-xl transition ${session.session_id === sessionId ? "bg-white/12" : "hover:bg-white/7"}`}>
                    <button onClick={() => { setSessionMenu(null); void loadSession(session.session_id); }} className="w-full p-3 pr-10 text-left text-sm">
                      <span className="block truncate">{session.preview}</span>
                      <span className="text-xs text-white/35">{session.message_count} tin nhắn</span>
                    </button>
                    <button onClick={e => { e.stopPropagation(); setSessionMenu(cur => cur === session.session_id ? null : session.session_id); }}
                      aria-label={`Tùy chọn cho ${session.preview}`}
                      className={`absolute right-2 top-1/2 grid h-8 w-8 -translate-y-1/2 place-items-center rounded-lg text-white/55 transition hover:bg-white/10 hover:text-white ${sessionMenu === session.session_id ? "opacity-100 bg-white/10" : "opacity-0 group-hover:opacity-100"}`}>
                      <FaEllipsisV />
                    </button>
                    {sessionMenu === session.session_id && (
                      <div className="absolute right-2 top-[calc(50%+20px)] z-20 w-40 overflow-hidden rounded-xl border border-white/10 bg-[#243b34] py-1 shadow-2xl">
                        <button onClick={() => beginRename(session)} className="flex w-full items-center gap-2 px-3 py-2.5 text-left text-xs hover:bg-white/10"><FaPen /> Đổi tên</button>
                        <button onClick={() => { setSessionMenu(null); setDeletingSession(session); }} className="flex w-full items-center gap-2 px-3 py-2.5 text-left text-xs text-[#ffb4a0] hover:bg-white/10"><FaTrash /> Xóa</button>
                      </div>
                    )}
                  </div>
                ))}
              </div>}
        </div>
        <div className="border-t border-white/10 p-4 text-sm">
          {user
            ? <><p className="font-semibold">{user.full_name}</p><p className="text-xs text-white/40">Dữ liệu riêng theo tài khoản</p></>
            : <p className="text-white/40">Bạn đang trò chuyện ẩn danh</p>}
        </div>
      </aside>

      {/* ── Main chat area ── */}
      <main className="flex min-w-0 flex-1 flex-col">
        <header className="flex items-center justify-between border-b border-black/5 bg-white/85 px-4 py-4 backdrop-blur sm:px-6">
          <div className="flex items-center gap-3">
            <span className="grid h-10 w-10 place-items-center rounded-2xl bg-[var(--forest)] text-white"><FaMagic /></span>
            <div>
              <h1 className="font-semibold">Nera đang ở đây</h1>
              <p className="text-xs text-[var(--muted)]">Nói tự nhiên, không cần điền form</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {savedProperties.length >= 2 && (
              <Link href="/compare" className="hidden rounded-full border border-[var(--sage)]/60 bg-[#edf3ed] px-4 py-2 text-xs font-semibold text-[var(--forest)] sm:block">
                So sánh {savedProperties.length} căn
              </Link>
            )}
            <Link href="/memory" className="hidden rounded-full border border-black/10 px-4 py-2 text-xs font-semibold sm:block">Memory</Link>
            <button onClick={newChat} className="rounded-xl border border-black/10 p-2 lg:hidden" aria-label="Cuộc trò chuyện mới"><FaPlus /></button>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-4 sm:p-6">
          <div className="mx-auto max-w-3xl space-y-6">
            {messages.map((message, index) => (
              <div key={`${message.role}-${index}`} className={`animate-message-in ${message.role === "user" ? "flex justify-end" : "flex gap-3"}`}>
                {message.role === "assistant" && (
                  <span className="mt-1 grid h-9 w-9 shrink-0 place-items-center rounded-2xl bg-[var(--forest)] text-white"><FaMagic /></span>
                )}
                <div className="max-w-2xl w-full">
                  <div className={`whitespace-pre-line rounded-[1.35rem] px-5 py-3.5 text-[15px] leading-7 ${message.role === "user" ? "rounded-tr-md bg-[var(--ink)] text-white" : "rounded-tl-md border border-black/5 bg-white shadow-sm"}`}>
                    {message.content}
                  </div>

                  {/* Quick reply chips */}
                  {message.role === "assistant" && message.quickReplies && message.quickReplies.length > 0 && index === messages.length - 1 && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      {message.quickReplies.map(chip => (
                        <button key={chip} onClick={() => void send(undefined, chip)}
                          className="rounded-full border border-black/10 bg-white px-4 py-2 text-xs font-medium text-[var(--ink)] transition hover:-translate-y-0.5 hover:border-[var(--sage)] hover:shadow-sm">
                          {chip}
                        </button>
                      ))}
                    </div>
                  )}

                  {/* Property cards */}
                  {message.properties?.map((property, pi) => (
                    <PropertyCard
                      key={property.id}
                      property={property}
                      insights={insights}
                      savedIds={savedIds}
                      animDelay={pi * 80}
                      onDetail={() => setSelected(property)}
                      onSave={() => void save(property)}
                      onBook={() => book(property)}
                      onReject={() => setFeedbackProperty(property)}
                    />
                  ))}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex animate-message-in items-start gap-3">
                <span className="grid h-9 w-9 place-items-center rounded-2xl bg-[var(--forest)] text-white"><FaMagic /></span>
                <div className="flex gap-1 rounded-[1.35rem] rounded-tl-md bg-white px-5 py-5 shadow-sm">
                  <i className="typing-dot" /><i className="typing-dot [animation-delay:150ms]" /><i className="typing-dot [animation-delay:300ms]" />
                </div>
              </div>
            )}

            {error && (
              <div role="alert" className="rounded-2xl border border-red-100 bg-red-50 p-4 text-sm text-red-700">
                <p>{error}</p>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
        </div>

        <form onSubmit={e => void send(e)} className="border-t border-black/5 bg-white p-4">
          <div className="relative mx-auto max-w-3xl">
            <input
              aria-label="Tin nhắn"
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Nói điều bạn thích, không thích hoặc muốn thay đổi…"
              className="w-full rounded-2xl border border-black/10 bg-[#fbfaf7] py-4 pl-5 pr-14 text-sm outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10"
            />
            <button disabled={loading || !input.trim()}
              className="absolute right-2 top-2 grid h-10 w-10 place-items-center rounded-xl bg-[var(--ink)] text-white transition hover:scale-105 disabled:opacity-30"
              aria-label="Gửi tin nhắn">
              <FaPaperPlane />
            </button>
          </div>
          <p className="mx-auto mt-2 max-w-3xl text-center text-[10px] text-stone-400">
            Nera dùng dữ liệu hệ thống làm nguồn sự thật và không tự xác nhận lịch thay Sale.
          </p>
        </form>
      </main>

      {/* ── Right sidebar: AI insights ── */}
      <InsightsSidebar
        insights={insights}
        memorySummary={memorySummary}
        savedProperties={savedProperties}
        latestMatches={latestMatches}
        onSelectProperty={setSelected}
        onClearMemory={() => void apiFetch<void>("/memory", { method: "DELETE" }).then(() => setMemorySummary(""))}
      />

      {/* ── Modals ── */}
      {renamingSession && (
        <div role="dialog" aria-modal="true" aria-labelledby="rename-chat-title" className="fixed inset-0 z-50 grid place-items-center bg-black/55 p-4">
          <form onSubmit={e => void renameSession(e)} className="w-full max-w-md animate-message-in rounded-[1.7rem] bg-white p-6 shadow-2xl">
            <div className="flex items-center justify-between">
              <h2 id="rename-chat-title" className="text-xl font-semibold">Đổi tên cuộc trò chuyện</h2>
              <button type="button" onClick={() => setRenamingSession(null)} className="grid h-9 w-9 place-items-center rounded-full bg-stone-100" aria-label="Đóng"><FaTimes /></button>
            </div>
            <input autoFocus maxLength={80} value={sessionTitle} onChange={e => setSessionTitle(e.target.value)}
              className="mt-5 w-full rounded-xl border border-black/10 px-4 py-3 outline-none focus:border-[var(--sage)]" aria-label="Tên cuộc trò chuyện" />
            <div className="mt-5 flex gap-3">
              <button type="button" onClick={() => setRenamingSession(null)} className="flex-1 rounded-full border border-black/10 py-2.5 font-semibold">Hủy</button>
              <button disabled={!sessionTitle.trim() || sessionActionLoading} className="flex-1 rounded-full bg-[var(--forest)] py-2.5 font-semibold text-white disabled:opacity-40">
                {sessionActionLoading ? "Đang lưu…" : "Lưu tên"}
              </button>
            </div>
          </form>
        </div>
      )}

      {deletingSession && (
        <div role="dialog" aria-modal="true" aria-labelledby="delete-chat-title" className="fixed inset-0 z-50 grid place-items-center bg-black/55 p-4">
          <div className="w-full max-w-md animate-message-in rounded-[1.7rem] bg-white p-6 shadow-2xl">
            <span className="grid h-12 w-12 place-items-center rounded-2xl bg-red-50 text-red-600"><FaTrash /></span>
            <h2 id="delete-chat-title" className="mt-5 text-xl font-semibold">Xóa cuộc trò chuyện?</h2>
            <p className="mt-2 text-sm leading-6 text-[var(--muted)]">"{deletingSession.preview}" sẽ bị xóa vĩnh viễn.</p>
            <div className="mt-6 flex gap-3">
              <button onClick={() => setDeletingSession(null)} className="flex-1 rounded-full border border-black/10 py-2.5 font-semibold">Giữ lại</button>
              <button onClick={() => void deleteSession()} disabled={sessionActionLoading}
                className="flex-1 rounded-full bg-red-600 py-2.5 font-semibold text-white disabled:opacity-40">
                {sessionActionLoading ? "Đang xóa…" : "Xóa"}
              </button>
            </div>
          </div>
        </div>
      )}

      {selected && (
        <div role="dialog" aria-modal="true" className="fixed inset-0 z-50 grid place-items-center bg-black/60 p-4">
          <div className="relative max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-[1.7rem] bg-white p-6">
            <button onClick={() => setSelected(null)} className="absolute right-4 top-4 rounded-full bg-slate-100 p-2" aria-label="Đóng"><FaTimes /></button>
            <h2 className="pr-10 text-2xl font-bold">{selected.title}</h2>
            <p className="mt-2 font-bold text-[var(--coral)]">{formatPropertyPrice(selected.list_price)}</p>
            {(selected.image || selected.media?.[0]?.url) && (
              <img src={selected.image || selected.media[0].url} alt={selected.title} className="mt-5 h-72 w-full rounded-xl object-cover" />
            )}
            {/* AI match reasons in detail modal */}
            {(() => { const { ok, caution } = buildMatchReasons(selected, insights); return (ok.length > 0 || caution.length > 0) && (
              <div className="mt-5 rounded-2xl bg-[#f0f5f1] p-4">
                <p className="flex items-center gap-2 text-xs font-bold uppercase tracking-wide text-[var(--forest)] mb-3"><FaBrain /> Vì sao Nera gợi ý</p>
                {ok.map(r => <p key={r} className="flex items-center gap-2 text-xs text-[var(--forest)] mb-1"><FaCheckCircle className="text-emerald-500 shrink-0" />{r}</p>)}
                {caution.map(r => <p key={r} className="flex items-center gap-2 text-xs text-amber-700 mb-1"><FaExclamationCircle className="shrink-0" />{r}</p>)}
              </div>
            ); })()}
            <p className="mt-4 whitespace-pre-line text-sm leading-7 text-slate-600">{selected.description || "Thông tin mô tả đang được cập nhật."}</p>
            <div className="mt-6 flex gap-3">
              <Link href={`/properties/${selected.id}`} className="flex-1 rounded-xl border border-slate-200 py-3 text-center font-semibold">
                <FaCheck className="mr-1 inline" /> Trang chi tiết
              </Link>
              <button onClick={() => book(selected)} className="flex-1 rounded-xl bg-[var(--forest)] py-3 font-semibold text-white">Đặt lịch xem nhà</button>
            </div>
          </div>
        </div>
      )}

      {feedbackProperty && (
        <FeedbackModal
          property={feedbackProperty}
          onClose={() => setFeedbackProperty(null)}
          onSubmit={text => void submitFeedback(text)}
        />
      )}
    </div>
  );
}

export default function ChatPage() {
  return (
    <Suspense fallback={<div className="grid min-h-screen place-items-center bg-[var(--paper)]">Đang mở Nera…</div>}>
      <ChatContent />
    </Suspense>
  );
}
