"use client";

import { FormEvent, Suspense, useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import {
  FaBars, FaBed, FaBookmark, FaBrain, FaCalendarAlt, FaCheck, FaCheckCircle, FaChevronDown, FaChevronRight,
  FaCompass, FaEllipsisV, FaExclamationCircle, FaHistory, FaMagic, FaMapMarkerAlt,
  FaPaperPlane, FaPen, FaPlus, FaRegBookmark, FaShieldAlt, FaTimes, FaTimesCircle, FaTrash
} from "react-icons/fa";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useAuth } from "@/components/AuthProvider";
import PropertyImage from "@/components/PropertyImage";
import { apiFetch, ApiError, apiStream } from "@/lib/api";
import { formatPropertyPrice } from "@/components/PropertyTile";
import type { Property } from "@/lib/types";
import { formatPropertyAddress, formatPropertyTitle } from "@/lib/propertyAddress";
import { ErrorBoundary } from "@/components/ErrorBoundary";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  properties?: Property[];
  quickReplies?: string[];
  authRequired?: boolean;
  aiMode?: string;
  aiModel?: string | null;
  aiLatencyMs?: number;
}

interface ChatResponse {
  response: string;
  session_id: string;
  properties: Property[];
  insights: Record<string, unknown>;
  suggested_actions?: string[];
  memory_summary?: string;
  auth_required?: boolean;
  ai_mode: string;
  ai_model?: string | null;
  ai_latency_ms: number;
}

interface SessionSummary {
  session_id: string;
  preview: string;
  message_count: number;
  last_active: string;
}

interface SessionDetail {
  messages: Array<{
    role: string;
    content: string;
    properties?: Property[];
    ai_mode?: string;
    ai_model?: string | null;
  }>;
}

const greeting: ChatMessage = {
  role: "assistant",
  content: "Chào bạn, tôi là Nera. Hãy kể tự nhiên về nơi bạn muốn sống — điều gì quan trọng, điều gì bạn không thích, hoặc một căn bạn đang cân nhắc.",
  quickReplies: ["Tôi muốn thuê căn hộ", "Tôi muốn mua nhà", "Tìm nhà cho gia đình", "Gần trường, tiện đi làm"]
};

// ────────────────────────────────────────────────────────────
// Helper: derive quick-reply chips from AI message content
// ────────────────────────────────────────────────────────────
function deriveQuickReplies(content: string, propertyCount = 0): string[] {
  const lower = content.toLowerCase();
  if (lower.includes("bạn chọn căn số mấy")) {
    return Array.from({ length: Math.min(propertyCount, 5) }, (_, index) => `Chọn căn số ${index + 1}`);
  }
  if (lower.includes("khung giờ số mấy")) {
    const slotCount = (content.match(/\*\*\d+\./g) || []).length;
    return Array.from({ length: Math.min(slotCount, 4) }, (_, index) => `${index + 1}`);
  }
  if (lower.includes("vào ngày nào") || lower.includes("chọn ngày nào")) {
    return ["Ngày mai", "Thứ Bảy tuần sau"];
  }
  if (lower.includes("bao nhiêu phòng ngủ") || lower.includes("mấy phòng ngủ")) {
    return ["1 phòng ngủ", "2 phòng ngủ", "3 phòng ngủ", "Chưa chắc"];
  }
  if (lower.includes("ngân sách bao nhiêu") || lower.includes("khoảng giá nào")) {
    return ["Dưới 15 triệu/tháng", "15–20 triệu/tháng", "Trên 20 triệu/tháng", "Muốn mua, không thuê"];
  }
  if (lower.includes("ở khu vực nào") || lower.includes("quận nào") || lower.includes("nơi làm việc ở đâu")) {
    return ["Cầu Giấy", "Thanh Xuân", "Nam Từ Liêm", "Hà Đông"];
  }
  if (lower.includes("thời gian") || lower.includes("chuyển vào") || lower.includes("khi nào")) {
    return ["Cuối tháng này", "1–2 tháng nữa", "3–6 tháng nữa", "Chưa xác định"];
  }
  if (lower.includes("gia đình") || lower.includes("bao nhiêu người") || lower.includes("thành viên")) {
    return ["1–2 người", "Gia đình 3 người", "Gia đình 4+ người", "Còn độc thân"];
  }
  if (lower.includes("di chuyển") || lower.includes("đi làm") || lower.includes("phút")) {
    return ["Dưới 20 phút", "20–35 phút", "35–45 phút", "Không quan trọng"];
  }
  return [];
}

async function requestedCoordinates(text: string): Promise<{ user_latitude: number; user_longitude: number } | null> {
  if (!/(vị trí (hiện tại|của tôi|này)|chỗ tôi|nơi tôi đang ở|gần đây)/i.test(text)) return null;
  if (!("geolocation" in navigator)) return null;
  return new Promise(resolve => {
    navigator.geolocation.getCurrentPosition(
      position => resolve({
        user_latitude: position.coords.latitude,
        user_longitude: position.coords.longitude,
      }),
      () => resolve(null),
      { enableHighAccuracy: false, timeout: 6000, maximumAge: 300000 },
    );
  });
}

// ────────────────────────────────────────────────────────────
// Helper: match property features vs insights for "Vì sao?"
// ────────────────────────────────────────────────────────────
function buildMatchReasons(property: Property, insights: Record<string, unknown>): { ok: string[]; caution: string[] } {
  const ok: string[] = [];
  const caution: string[] = [];

  const maxPrice = insights.max_price as number | undefined;
  if (maxPrice && property.list_price) {
    if (property.list_price <= maxPrice) ok.push(`Giá phù hợp ngân sách`);
    else caution.push(`Có thể hơi cao so với ngân sách`);
  }

  const beds = (insights.min_bedrooms ?? insights.bedrooms) as number | undefined;
  if (beds && property.bedrooms != null) {
    if (property.bedrooms >= beds) ok.push(`Đủ ${property.bedrooms} phòng ngủ`);
    else caution.push(`Ít hơn yêu cầu phòng ngủ`);
  }

  const district = insights.district as string | undefined;
  if (district && property.district?.toLowerCase().includes(district.toLowerCase())) {
    ok.push(`Đúng khu vực ${district}`);
  }

  if (property.area_sqm && property.area_sqm >= 50) ok.push(`Diện tích rộng rãi (${property.area_sqm} m²)`);

  return { ok, caution };
}

// ────────────────────────────────────────────────────────────
// Insight label map
// ────────────────────────────────────────────────────────────
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
  soft_preferences: "Ưu tiên mềm",
  household_context: "Hoàn cảnh",
  commute_landmark: "Điểm đi làm",
  max_commute_minutes: "Di chuyển tối đa",
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
// Feedback Modal
// ────────────────────────────────────────────────────────────
const FEEDBACK_REASONS = [
  "Giá hơi cao", "Đi làm quá xa", "Diện tích hơi nhỏ",
  "Không thích khu vực", "Bếp không ưng ý", "Thiếu tiện ích", "Lý do khác"
];

function FeedbackModal({ property, onClose, onSubmit }: {
  property: Property;
  onClose: () => void;
  onSubmit: (text: string) => void;
}) {
  const [selected, setSelected] = useState<string[]>([]);
  const [extra, setExtra] = useState("");

  function toggle(reason: string) {
    setSelected(prev => prev.includes(reason) ? prev.filter(r => r !== reason) : [...prev, reason]);
  }

  function submit() {
    const parts = [...selected];
    if (extra.trim()) parts.push(extra.trim());
    if (parts.length === 0) return;
    const text = `Về căn "${property.title}", tôi không thích vì: ${parts.join(", ")}`;
    onSubmit(text);
    onClose();
  }

  return (
    <div role="dialog" aria-modal="true" className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/55 p-4">
      <div
        className="w-full max-w-md animate-message-in rounded-[1.7rem] bg-white shadow-2xl overflow-hidden"
        style={{ backgroundImage: "url(" + (property.image || property.media?.[0]?.url || "") + ")", backgroundSize: "cover", backgroundPosition: "center" }}
      >
        <div className="bg-white/95 backdrop-blur-sm">
          <div className="p-5 border-b border-black/5 flex items-center gap-3">
            <div className="flex-1">
              <p className="text-xs font-bold uppercase tracking-wide text-[var(--coral)]">Phản hồi của bạn</p>
              <h2 className="font-semibold text-sm mt-0.5 line-clamp-1">{property.title}</h2>
            </div>
            <button onClick={onClose} className="grid h-8 w-8 place-items-center rounded-full bg-black/5 hover:bg-black/10" aria-label="Đóng"><FaTimes /></button>
          </div>
          <div className="p-5">
            <p className="font-semibold">Điều gì khiến căn này chưa phù hợp?</p>
            <p className="text-xs text-[var(--muted)] mt-1">Phản hồi giúp Nera hiểu bạn hơn và gợi ý chính xác hơn.</p>
            <div className="mt-4 flex flex-wrap gap-2">
              {FEEDBACK_REASONS.map(reason => (
                <button key={reason} onClick={() => toggle(reason)}
                  className={`rounded-full border px-3 py-1.5 text-xs font-medium transition ${selected.includes(reason) ? "border-[var(--forest)] bg-[var(--forest)] text-white" : "border-black/10 hover:border-[var(--sage)]"}`}>
                  {reason}
                </button>
              ))}
            </div>
            <textarea
              value={extra} onChange={e => setExtra(e.target.value)}
              placeholder="Nói thêm nếu bạn muốn… (không bắt buộc)"
              rows={2}
              className="mt-4 w-full rounded-xl border border-black/10 px-4 py-3 text-sm outline-none resize-none focus:border-[var(--sage)] focus:ring-2 focus:ring-[var(--sage)]/10"
            />
            <div className="mt-4 flex gap-3">
              <button onClick={onClose} className="flex-1 rounded-full border border-black/10 py-2.5 text-sm font-semibold">Bỏ qua</button>
              <button onClick={submit} disabled={selected.length === 0 && !extra.trim()}
                className="flex-1 rounded-full bg-[var(--forest)] py-2.5 text-sm font-semibold text-white disabled:opacity-40">
                Gửi phản hồi
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ────────────────────────────────────────────────────────────
// Typewriter Markdown for streaming animated text output
// ────────────────────────────────────────────────────────────
function TypewriterMarkdown({
  content,
  isStreaming,
  onComplete,
}: {
  content: string;
  isStreaming: boolean;
  onComplete?: () => void;
}) {
  const [displayedLength, setDisplayedLength] = useState(() => (isStreaming ? 0 : content.length));
  const onCompleteRef = useRef(onComplete);
  onCompleteRef.current = onComplete;

  useEffect(() => {
    if (!isStreaming) {
      setDisplayedLength(content.length);
      return;
    }

    if (displayedLength >= content.length) {
      const timer = setTimeout(() => {
        onCompleteRef.current?.();
      }, 0);
      return () => clearTimeout(timer);
    }

    const step = content.length > 600 ? 8 : content.length > 250 ? 5 : 3;
    const timer = setTimeout(() => {
      setDisplayedLength((prev) => Math.min(prev + step, content.length));
    }, 12);

    return () => clearTimeout(timer);
  }, [content, isStreaming, displayedLength]);

  const displayedContent = isStreaming ? content.slice(0, displayedLength) : content;
  const isTyping = isStreaming && displayedLength < content.length;

  const handleFinishEarly = useCallback(() => {
    if (isTyping) {
      setDisplayedLength(content.length);
      setTimeout(() => {
        onCompleteRef.current?.();
      }, 0);
    }
  }, [isTyping, content.length]);

  return (
    <div
      onClick={handleFinishEarly}
      className={isTyping ? "cursor-pointer" : ""}
      title={isTyping ? "Bấm để hiển thị toàn bộ ngay" : undefined}
    >
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          table: ({ ...props }) => (
            <div className="my-4 overflow-x-auto rounded-2xl border border-stone-200/80 bg-white shadow-xs">
              <table className="w-full text-left text-[14px] border-collapse min-w-[480px]" {...props} />
            </div>
          ),
          thead: ({ ...props }) => <thead className="bg-[#eef4ee] text-[var(--forest)] font-bold border-b border-stone-200" {...props} />,
          tr: ({ ...props }) => <tr className="even:bg-stone-50/50 hover:bg-emerald-50/30 transition-colors" {...props} />,
          th: ({ ...props }) => <th className="py-3 px-4 font-bold text-[14px] text-[var(--forest)] border-r border-stone-200/70 last:border-r-0 whitespace-nowrap" {...props} />,
          td: ({ ...props }) => <td className="py-3 px-4 text-[14px] text-stone-700 border-t border-stone-200/60 border-r border-stone-200/60 last:border-r-0 align-top leading-6" {...props} />,
          p: ({ ...props }) => <p className="mb-3 last:mb-0 leading-relaxed text-[15px]" {...props} />,
          ul: ({ ...props }) => <ul className="my-2.5 list-disc pl-5 space-y-1.5" {...props} />,
          ol: ({ ...props }) => <ol className="my-2.5 list-decimal pl-5 space-y-1.5" {...props} />,
          li: ({ ...props }) => <li className="text-[15px] leading-relaxed" {...props} />,
          h1: ({ ...props }) => <h1 className="text-lg font-bold my-3 text-[var(--forest)]" {...props} />,
          h2: ({ ...props }) => <h2 className="text-base font-bold my-2.5 text-[var(--forest)]" {...props} />,
          h3: ({ ...props }) => <h3 className="text-[15px] font-bold my-2 text-[var(--forest)]" {...props} />,
          strong: ({ ...props }) => <strong className="font-semibold text-stone-900" {...props} />,
        }}
      >
        {displayedContent}
      </ReactMarkdown>
      {isTyping && (
        <span className="inline-block w-1.5 h-4 ml-1 bg-[var(--forest)] animate-pulse align-middle" />
      )}
    </div>
  );
}

// ────────────────────────────────────────────────────────────
// Property Card with AI match reasons
// ────────────────────────────────────────────────────────────
function PropertyCard({ property, insights, savedIds, onDetail, onSave, onBook, onReject, animDelay }: {
  property: Property;
  insights: Record<string, unknown>;
  savedIds: Set<string>;
  onDetail: () => void;
  onSave: () => void;
  onBook: () => void;
  onReject: () => void;
  animDelay: number;
}) {
  const [showReasons, setShowReasons] = useState(false);
  const { ok, caution } = useMemo(() => buildMatchReasons(property, insights), [property, insights]);
  const hasInsights = ok.length > 0 || caution.length > 0;

  return (
    <article
      style={{ animationDelay: `${animDelay}ms` }}
      className="animate-card-rise mt-4 overflow-hidden rounded-[1.5rem] border border-black/5 bg-white shadow-[0_14px_40px_rgba(22,47,42,.08)]"
    >
      <div className="sm:flex">
        <div className="h-48 bg-stone-100 sm:h-auto sm:w-52 shrink-0">
          {(property.image || property.media?.[0]?.url)
            ? <PropertyImage src={property.image || property.media[0].url} alt={property.title} className="h-full w-full object-cover" />
            : <div className="grid h-full min-h-40 place-items-center text-4xl">🏠</div>}
        </div>
        <div className="flex-1 p-5">
          <div className="flex flex-wrap justify-between gap-2">
            <h2 className="max-w-sm font-semibold leading-6">{formatPropertyTitle(property.title)}</h2>
            <span className="font-semibold text-[var(--coral)]">{formatPropertyPrice(property.list_price)}</span>
          </div>
          <p className="mt-2 text-xs text-[var(--muted)]">
            <FaMapMarkerAlt className="mr-1 inline" />
            {formatPropertyAddress(property)}
          </p>
          <p className="mt-2 text-xs text-[var(--muted)]">
            <FaBed className="mr-1 inline text-[var(--forest)]" />{property.bedrooms ?? 0} phòng ngủ · {property.area_sqm} m²
          </p>
          {property.distance_evidence && (
            <p className="mt-2 rounded-lg bg-[#eef4ee] px-3 py-2 text-xs font-medium text-[var(--forest)]">
              <FaCompass className="mr-1.5 inline" />
              {property.distance_evidence.distance_km} km · {property.distance_evidence.duration_minutes} phút đến {property.distance_evidence.destination}
              <span className="ml-1 text-[10px] font-normal text-[var(--muted)]">· {property.distance_evidence.attribution ?? property.distance_evidence.provider}</span>
            </p>
          )}
          {property.nearby_evidence?.[0] && (
            <p className="mt-2 text-xs text-[var(--muted)]">
              <FaMapMarkerAlt className="mr-1 inline text-[var(--forest)]" />
              Gần {property.nearby_evidence[0].name} (~{property.nearby_evidence[0].straight_line_km} km đường chim bay)
            </p>
          )}

          {/* "Vì sao phù hợp?" expandable section */}
          {hasInsights && (
            <button
              onClick={() => setShowReasons(v => !v)}
              className="mt-3 flex items-center gap-1.5 text-xs font-semibold text-[var(--forest)] hover:underline"
            >
              <FaBrain className="text-[var(--sage)]" />
              Vì sao Nera gợi ý căn này?
              {showReasons ? <FaChevronDown className="text-[8px]" /> : <FaChevronRight className="text-[8px]" />}
            </button>
          )}
          {showReasons && (
            <div className="mt-2 rounded-xl bg-[#f0f5f1] px-4 py-3 space-y-1 text-xs">
              {ok.map(r => (
                <p key={r} className="flex items-start gap-1.5 text-[var(--forest)]">
                  <FaCheckCircle className="mt-0.5 shrink-0 text-emerald-500" />{r}
                </p>
              ))}
              {caution.map(r => (
                <p key={r} className="flex items-start gap-1.5 text-amber-700">
                  <FaExclamationCircle className="mt-0.5 shrink-0" />{r}
                </p>
              ))}
            </div>
          )}

          <div className="mt-4 flex flex-wrap gap-2">
            <button onClick={onDetail} className="rounded-full border border-black/10 px-4 py-2 text-xs font-semibold hover:bg-stone-50">Chi tiết</button>
            <button onClick={onSave} aria-pressed={savedIds.has(property.id)}
              className="rounded-full border border-[var(--sage)]/50 px-4 py-2 text-xs font-semibold text-[var(--forest)] hover:bg-[#edf3ed]">
              {savedIds.has(property.id) ? <FaBookmark className="mr-1 inline" /> : <FaRegBookmark className="mr-1 inline" />}
              {savedIds.has(property.id) ? "Đã lưu" : "Lưu"}
            </button>
            <button onClick={onBook} className="rounded-full bg-[var(--forest)] px-4 py-2 text-xs font-semibold text-white hover:opacity-90">
              <FaCalendarAlt className="mr-1 inline" />Đặt lịch xem
            </button>
            <button onClick={onReject}
              className="rounded-full border border-black/8 px-4 py-2 text-xs font-medium text-[var(--muted)] hover:border-red-200 hover:text-red-500">
              <FaTimesCircle className="mr-1 inline" />Không phù hợp
            </button>
          </div>
        </div>
      </div>
    </article>
  );
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
                    ? <PropertyImage src={property.image || property.media[0].url} alt="" className="h-14 w-14 rounded-lg object-cover shrink-0" />
                    : <div className="grid h-14 w-14 place-items-center rounded-lg bg-stone-100 shrink-0">🏡</div>}
                  <span className="min-w-0">
                    <strong className="line-clamp-2 text-xs leading-4">{formatPropertyTitle(property.title)}</strong>
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
                {formatPropertyTitle(p.title)}
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
  const isNewParam = searchParams.get("new") === "1";
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [sessionId, setSessionId] = useState<string>(() => {
    if (typeof window !== "undefined") {
      const stored = window.sessionStorage.getItem("nera_chat_session_id");
      if (stored) return stored;
    }
    return crypto.randomUUID();
  });
  const [messages, setMessages] = useState<ChatMessage[]>(() => {
    if (typeof window !== "undefined") {
      const storedId = window.sessionStorage.getItem("nera_chat_session_id");
      if (storedId) {
        const cached = window.sessionStorage.getItem(`nera_chat_messages_${storedId}`);
        if (cached) {
          try {
            const parsed = JSON.parse(cached);
            if (Array.isArray(parsed) && parsed.length > 0) return parsed;
          } catch { }
        }
      }
    }
    return [greeting];
  });
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [streamingIndex, setStreamingIndex] = useState<number | null>(null);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  // Label of the graph node currently running, streamed from the backend.
  const [stage, setStage] = useState("");
  const [error, setError] = useState("");
  const [selected, setSelected] = useState<Property | null>(null);
  const [feedbackProperty, setFeedbackProperty] = useState<Property | null>(null);
  const [savedIds, setSavedIds] = useState<Set<string>>(new Set());
  const [savedProperties, setSavedProperties] = useState<Property[]>([]);
  const [memorySummary, setMemorySummary] = useState("");
  const [insights, setInsights] = useState<Record<string, unknown>>({});
  const [expandedCards, setExpandedCards] = useState<Record<number, boolean>>({});
  const [sessionMenu, setSessionMenu] = useState<string | null>(null);
  const [renamingSession, setRenamingSession] = useState<SessionSummary | null>(null);
  const [deletingSession, setDeletingSession] = useState<SessionSummary | null>(null);
  const [sessionTitle, setSessionTitle] = useState("");
  const [sessionActionLoading, setSessionActionLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const propertyLoaded = useRef(false);
  const handledPromptRef = useRef<string | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

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

  const sessionLoadedOnMount = useRef(false);

  const stopGenerating = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setLoading(false);
  }, []);

  async function send(event?: FormEvent, quickText?: string, targetSessionId?: string) {
    event?.preventDefault();
    if (loading) return; // Prevent double submit while generating
    const text = (quickText ?? input).trim();
    if (!text) return;

    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }

    const controller = new AbortController();
    abortControllerRef.current = controller;

    const activeSessionId = targetSessionId || sessionId;

    setInput(""); setError(""); setLoading(true); setStreamingIndex(null); setStage("");
    setMessages(cur => [...cur, { role: "user", content: text }]);
    try {
      const coordinates = await requestedCoordinates(text);
      const payload = { message: text, property_id: propertyId || undefined, ...(coordinates ?? {}) };
      const streamed: { result?: ChatResponse; sawStage: boolean } = { sawStage: false };

      // Stream first so the customer sees which step is running while they wait.
      try {
        let streamError: string | undefined;
        await apiStream("/chat/stream", {
          body: payload,
          headers: { "X-Session-ID": activeSessionId },
          signal: controller.signal,
          onEvent: (event, data) => {
            if (event === "stage") {
              streamed.sawStage = true;
              setStage((data as { label?: string }).label ?? "");
            } else if (event === "result") {
              streamed.result = data as ChatResponse;
            } else if (event === "error") {
              streamError = (data as { detail?: string }).detail;
            }
          },
        });
        if (streamError) throw new ApiError(streamError, 503);
      } catch (streamErr: unknown) {
        if (streamErr instanceof Error && (streamErr.name === "AbortError" || streamErr.message.includes("abort"))) {
          throw streamErr;
        }
        // Receiving a stage proves the server ran this turn. Retrying over POST
        // would make it run and persist a second time, duplicating the message.
        if (streamed.sawStage) throw streamErr;
      }

      // Falling back only when streaming never started: an older backend, or a
      // proxy that does not pass text/event-stream through.
      const res = streamed.result ?? await apiFetch<ChatResponse>("/chat", {
        method: "POST",
        headers: { "X-Session-ID": activeSessionId },
        body: JSON.stringify(payload),
        signal: controller.signal
      });

      setStage("");
      setSessionId(res.session_id || activeSessionId);

      const chips = res.suggested_actions?.length
        ? res.suggested_actions
        : deriveQuickReplies(res.response, res.properties?.length ?? 0);

      setMessages(cur => {
        const next: ChatMessage[] = [...cur, { role: "assistant", content: res.response, properties: res.properties ?? [], quickReplies: chips, authRequired: res.auth_required, aiMode: res.ai_mode, aiModel: res.ai_model, aiLatencyMs: res.ai_latency_ms }];
        setStreamingIndex(next.length - 1);
        return next;
      });
      setInsights(res.insights ?? {});
      if (res.memory_summary) setMemorySummary(res.memory_summary);
      void loadSessions();
    } catch (err: unknown) {
      if (err instanceof Error && (err.name === "AbortError" || err.message.includes("abort"))) {
        return;
      }
      setError(err instanceof Error ? err.message : "Nera chưa phản hồi được.");
    } finally {
      if (abortControllerRef.current === controller) {
        abortControllerRef.current = null;
        setLoading(false);
        setStage("");
      }
    }
  }

  useEffect(() => {
    if (typeof window !== "undefined" && sessionId) {
      try {
        window.sessionStorage.setItem("nera_chat_session_id", sessionId);
        if (messages.length > 1 || (messages.length === 1 && messages[0] !== greeting)) {
          window.sessionStorage.setItem(`nera_chat_messages_${sessionId}`, JSON.stringify(messages));
        }
      } catch { }
    }
  }, [sessionId, messages]);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, loading]);

  useEffect(() => {
    if (!propertyId || propertyLoaded.current) return;
    propertyLoaded.current = true;
    void apiFetch<Property>(`/properties/${propertyId}`)
      .then(p => setMessages([greeting, { role: "assistant", content: `Bạn đang quan tâm "${p.title}". Tôi đã mở căn này để mình cùng phân tích hoặc đặt lịch.`, properties: [p] }]))
      .catch(() => setError("Không tìm thấy bất động sản này."));
  }, [propertyId]);

  async function loadSession(id: string) {
    if (typeof window !== "undefined") {
      const cached = window.sessionStorage.getItem(`nera_chat_messages_${id}`);
      if (cached) {
        try {
          const parsed = JSON.parse(cached);
          if (Array.isArray(parsed) && parsed.length > 0) {
            setSessionId(id);
            setMessages(parsed);
            setExpandedCards({});
            setError("");
          }
        } catch { }
      }
    }
    try {
      const data = await apiFetch<SessionDetail>(`/session/${id}`);
      setSessionId(id);
      if (data.messages && data.messages.length > 0) {
        setMessages(data.messages.map(m => ({ role: m.role.toLowerCase() === "user" ? "user" : "assistant", content: m.content, properties: m.properties, aiMode: m.ai_mode, aiModel: m.ai_model })));
      } else {
        setMessages([greeting]);
      }
      setExpandedCards({});
      setError("");
    } catch { setError("Không tải được cuộc trò chuyện."); }
  }

  function newChat() {
    const nextSession = crypto.randomUUID();
    window.sessionStorage.setItem("nera_chat_session_id", nextSession);
    setSessionId(nextSession); setMessages([greeting]); setInput(""); setError(""); setInsights({}); setExpandedCards({}); router.replace("/chat");
  }

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

  async function submitFeedback(text: string) {
    setLoading(true);
    setMessages(cur => [...cur, { role: "user", content: text }]);
    try {
      const res = await apiFetch<ChatResponse>("/chat", {
        method: "POST",
        headers: { "X-Session-ID": sessionId },
        body: JSON.stringify({ message: text })
      });
      const chips = res.suggested_actions?.length
        ? res.suggested_actions
        : deriveQuickReplies(res.response, res.properties?.length ?? 0);
      setMessages(cur => {
        const next: ChatMessage[] = [...cur, { role: "assistant", content: res.response, properties: res.properties ?? [], quickReplies: chips, authRequired: res.auth_required, aiMode: res.ai_mode, aiModel: res.ai_model, aiLatencyMs: res.ai_latency_ms }];
        setStreamingIndex(next.length - 1);
        return next;
      });
      setInsights(res.insights ?? {});
      if (res.memory_summary) setMemorySummary(res.memory_summary);
      void loadSessions();
    } catch { /* silent */ }
    finally { setLoading(false); }
  }

  const latestMatches = useMemo(() => [...messages].reverse().find(m => m.properties?.length)?.properties ?? [], [messages]);

  useEffect(() => {
    if (initialPrompt && handledPromptRef.current !== initialPrompt) {
      handledPromptRef.current = initialPrompt;
      const nextSession = crypto.randomUUID();
      window.sessionStorage.setItem("nera_chat_session_id", nextSession);
      setSessionId(nextSession);
      sessionLoadedOnMount.current = true;
      window.history.replaceState({}, "", "/chat");
      router.replace("/chat");
      void send(undefined, initialPrompt, nextSession);
      return;
    }
    if (isNewParam && !initialPrompt) {
      const nextSession = crypto.randomUUID();
      window.sessionStorage.setItem("nera_chat_session_id", nextSession);
      setSessionId(nextSession);
      setMessages([greeting]);
      sessionLoadedOnMount.current = true;
      window.history.replaceState({}, "", "/chat");
      router.replace("/chat");
      return;
    }
    const stored = window.sessionStorage.getItem("nera_chat_session_id");
    if (stored) {
      setSessionId(stored);
      if (user && !propertyId && !sessionLoadedOnMount.current) {
        sessionLoadedOnMount.current = true;
        void apiFetch<SessionDetail>(`/session/${stored}`)
          .then(data => {
            if (data.messages && data.messages.length > 0) {
              setMessages(data.messages.map(m => ({
                role: m.role.toLowerCase() === "user" ? "user" : "assistant",
                content: m.content,
                properties: m.properties,
                aiMode: m.ai_mode,
                aiModel: m.ai_model,
              })));
            }
          })
          .catch(() => { });
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, initialPrompt, propertyId, isNewParam]);

  return (
    <div className="flex h-screen overflow-hidden bg-[var(--paper)] text-[var(--ink)]">
      {/* ── Mobile backdrop for sidebar ── */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm lg:hidden"
          onClick={() => setSidebarOpen(false)}
          aria-label="Đóng lịch sử"
        />
      )}

      {/* ── Left sidebar: session history ── */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 flex flex-col bg-[var(--ink)] text-white shadow-2xl transition-all duration-300 ease-in-out lg:static lg:z-auto lg:shadow-none ${sidebarOpen
            ? "w-72 translate-x-0 opacity-100"
            : "-translate-x-full pointer-events-none lg:translate-x-0 lg:w-0 lg:overflow-hidden lg:opacity-0"
          }`}
      >
        <div className="flex h-full w-72 flex-col">
          <div className="flex items-center justify-between border-b border-white/10 p-5">
            <Link href="/" className="flex items-center gap-3 font-semibold">
              <span className="grid h-10 w-10 place-items-center rounded-2xl bg-white/10"><FaMagic className="text-[#a9c9b0]" /></span>
              <span>Nera<small className="block text-[10px] font-medium uppercase tracking-[.16em] text-white/45">AI home companion</small></span>
            </Link>
            <button
              onClick={() => setSidebarOpen(false)}
              className="grid h-8 w-8 place-items-center rounded-xl text-white/60 transition hover:bg-white/10 hover:text-white"
              aria-label="Thu gọn lịch sử"
              title="Thu gọn lịch sử"
            >
              <FaBars />
            </button>
          </div>
          <div className="p-4">
            <button onClick={newChat} className="flex w-full items-center justify-center gap-2 rounded-2xl bg-white py-3 text-sm font-semibold text-[var(--ink)] transition hover:bg-[#e7eee7]">
              <FaPlus /> Cuộc trò chuyện mới
            </button>
          </div>
          <div className="flex-1 overflow-y-auto px-4 pb-4 dark-sidebar-scroll">
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
        </div>
      </aside>

      {/* ── Main chat area ── */}
      <main className="flex min-w-0 flex-1 flex-col">
        <header className="flex items-center justify-between border-b border-black/5 bg-white/85 px-4 py-4 backdrop-blur sm:px-6">
          <div className="flex items-center gap-3">
            {!sidebarOpen && (
              <button
                onClick={() => setSidebarOpen(true)}
                className="grid h-10 w-10 shrink-0 place-items-center rounded-2xl border border-black/10 bg-white text-stone-700 shadow-sm transition hover:border-black/20 hover:bg-stone-50 hover:text-black"
                aria-label="Mở thanh lịch sử"
                title="Mở thanh lịch sử"
              >
                <FaBars />
              </button>
            )}
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
              <div key={`${message.role}-${index}`} className="animate-message-in">
                {message.role === "user" ? (
                  <div className="flex justify-end">
                    <div className="w-fit max-w-[80%] rounded-[1.35rem] rounded-tr-xs bg-[var(--ink)] px-5 py-3 text-[15px] leading-relaxed text-white shadow-xs whitespace-pre-line break-words">
                      {message.content}
                    </div>
                  </div>
                ) : (
                  <div className="flex items-start gap-3">
                    <span className="mt-1 grid h-9 w-9 shrink-0 place-items-center rounded-2xl bg-[var(--forest)] text-white shadow-xs"><FaMagic /></span>
                    <div className="w-fit max-w-[88%] min-w-0 space-y-3">
                      <div className="w-fit max-w-full rounded-[1.35rem] rounded-tl-xs border border-black/5 bg-white px-5 py-3.5 text-[15px] leading-relaxed text-stone-800 shadow-xs">
                        <div className="prose prose-sm max-w-none text-stone-800 leading-relaxed">
                          <TypewriterMarkdown
                            content={message.content}
                            isStreaming={streamingIndex === index}
                            onComplete={() => setStreamingIndex(null)}
                          />
                        </div>
                      </div>

                      {/* Quick reply chips */}
                      {message.quickReplies && message.quickReplies.length > 0 && index === messages.length - 1 && (
                        <div className="flex flex-wrap gap-2">
                          {message.quickReplies.map(chip => (
                            <button
                              key={chip}
                              disabled={loading}
                              onClick={() => void send(undefined, chip)}
                              className={`rounded-full border border-black/10 bg-white px-4 py-2 text-xs font-medium text-[var(--ink)] transition hover:-translate-y-0.5 hover:border-[var(--sage)] hover:shadow-sm ${loading ? "opacity-50 cursor-not-allowed pointer-events-none" : ""
                                }`}
                            >
                              {chip}
                            </button>
                          ))}
                        </div>
                      )}

                      {/* Auth required */}
                      {message.authRequired && index === messages.length - 1 && (
                        <Link href="/login?next=/chat" className="inline-flex rounded-full bg-[var(--forest)] px-5 py-2.5 text-xs font-semibold text-white">
                          Đăng nhập để tiếp tục
                        </Link>
                      )}

                      {/* Property cards */}
                      {message.properties && message.properties.length > 0 && (() => {
                        const isExpanded = expandedCards[index] ?? false;
                        const totalCards = message.properties.length;
                        const displayed = isExpanded ? message.properties : message.properties.slice(0, 5);
                        const hasMore = totalCards > 5;

                        return (
                          <div className="space-y-3 pt-1">
                            {displayed.map((property, pi) => (
                              <PropertyCard
                                key={property.id}
                                property={property}
                                insights={insights}
                                savedIds={savedIds}
                                animDelay={pi * 60}
                                onDetail={() => setSelected(property)}
                                onSave={() => void save(property)}
                                onBook={() => book(property)}
                                onReject={() => setFeedbackProperty(property)}
                              />
                            ))}

                            {hasMore && (
                              <button
                                type="button"
                                onClick={() => setExpandedCards(prev => ({ ...prev, [index]: !prev[index] }))}
                                className="mt-3 flex w-full items-center justify-center gap-2 rounded-2xl border border-[var(--forest)]/20 bg-[#f4f8f4] hover:bg-[#e8f1e8] px-4 py-3.5 text-xs font-semibold text-[var(--forest)] shadow-xs transition-all hover:border-[var(--forest)]/40 active:scale-[0.99] cursor-pointer"
                              >
                                <span>
                                  {isExpanded
                                    ? "Thu gọn danh sách (chỉ hiện 5 căn đầu)"
                                    : `Xem tất cả ${totalCards} bất động sản (còn ${totalCards - 5} căn khác)`}
                                </span>
                                <FaChevronDown className={`transition-transform duration-200 text-xs ${isExpanded ? "rotate-180" : ""}`} />
                              </button>
                            )}
                          </div>
                        );
                      })()}
                    </div>
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex animate-message-in items-start gap-3">
                <span className="grid h-9 w-9 place-items-center rounded-2xl bg-[var(--forest)] text-white shadow-xs animate-pulse">
                  <FaMagic />
                </span>
                <div className="flex items-center gap-3 rounded-[1.35rem] rounded-tl-xs bg-white px-5 py-4 shadow-xs border border-stone-100">
                  <div className="flex gap-1.5">
                    <i className="typing-dot" /><i className="typing-dot [animation-delay:150ms]" /><i className="typing-dot [animation-delay:300ms]" />
                  </div>
                  {/* The streamed stage says what is actually running; the static
                      line covers the moment before the first stage arrives. */}
                  <span aria-live="polite" className="text-xs font-medium text-stone-500 animate-pulse">
                    {stage || "Nera đang phân tích yêu cầu & tìm kiếm dữ liệu…"}
                  </span>
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
              disabled={loading}
              onChange={e => setInput(e.target.value)}
              placeholder={loading ? "Nera đang trả lời, vui lòng chờ trong giây lát…" : "Nói điều bạn thích, không thích hoặc muốn thay đổi…"}
              className={`w-full rounded-2xl border border-black/10 bg-[#fbfaf7] py-4 pl-5 pr-14 text-sm outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10 transition-colors ${loading ? "opacity-60 cursor-not-allowed bg-stone-100/70" : ""
                }`}
            />
            {loading ? (
              <button
                type="button"
                onClick={stopGenerating}
                className="absolute right-2 top-2 grid h-10 w-10 place-items-center rounded-xl bg-[var(--forest)] text-white shadow-xs transition hover:scale-105 hover:bg-[#163825] active:scale-95 cursor-pointer"
                aria-label="Tạm dừng"
                title="Bấm để dừng"
              >
                <span className="h-3.5 w-3.5 rounded-[3px] bg-white block" />
              </button>
            ) : (
              <button
                type="submit"
                disabled={!input.trim() || loading}
                className="absolute right-2 top-2 grid h-10 w-10 place-items-center rounded-xl bg-[var(--ink)] text-white transition hover:scale-105 disabled:opacity-30 cursor-pointer disabled:cursor-not-allowed"
                aria-label="Gửi tin nhắn"
              >
                <FaPaperPlane />
              </button>
            )}
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
            <p className="mt-2 text-sm leading-6 text-[var(--muted)]">“{deletingSession.preview}” sẽ bị xóa vĩnh viễn.</p>
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
            <h3 className="text-lg font-bold">{formatPropertyTitle(selected.title)}</h3>
            <p className="mt-2 font-bold text-[var(--coral)]">{formatPropertyPrice(selected.list_price)}</p>
            {(selected.image || selected.media?.[0]?.url) && (
              <PropertyImage src={selected.image || selected.media[0].url} alt={selected.title} className="mt-5 h-72 w-full rounded-xl object-cover" />
            )}
            {(() => {
              const { ok, caution } = buildMatchReasons(selected, insights); return (ok.length > 0 || caution.length > 0) && (
                <div className="mt-5 rounded-2xl bg-[#f0f5f1] p-4">
                  <p className="flex items-center gap-2 text-xs font-bold uppercase tracking-wide text-[var(--forest)] mb-3"><FaBrain /> Vì sao Nera gợi ý</p>
                  {ok.map(r => <p key={r} className="flex items-center gap-2 text-xs text-[var(--forest)] mb-1"><FaCheckCircle className="text-emerald-500 shrink-0" />{r}</p>)}
                  {caution.map(r => <p key={r} className="flex items-center gap-2 text-xs text-amber-700 mb-1"><FaExclamationCircle className="shrink-0" />{r}</p>)}
                </div>
              );
            })()}
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
    <ErrorBoundary>
      <Suspense fallback={<div className="grid min-h-screen place-items-center bg-[var(--paper)]">Đang mở Nera…</div>}>
        <ChatContent />
      </Suspense>
    </ErrorBoundary>
  );
}
