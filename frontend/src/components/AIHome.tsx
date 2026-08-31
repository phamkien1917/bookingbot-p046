"use client";

import { FormEvent, type RefObject, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  FaArrowRight,
  FaBrain,
  FaCalendarCheck,
  FaCheckCircle,
  FaChevronLeft,
  FaChevronRight,
  FaCompass,
  FaMagic,
  FaMapMarkerAlt,
  FaPaperPlane,
  FaRegBookmark,
  FaShieldAlt,
} from "react-icons/fa";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import PropertyTile from "@/components/PropertyTile";
import PropertyImage from "@/components/PropertyImage";
import { roleHome, useAuth } from "@/components/AuthProvider";
import { apiFetch } from "@/lib/api";
import type { Property } from "@/lib/types";

interface MemoryResponse {
  items: Record<string, unknown>;
  summary: string;
}

const suggestions = [
  "Căn 2 phòng ngủ ở Cầu Giấy, dưới 5 tỷ",
  "Nhà gần ĐH Quốc Gia, nhiều ánh sáng và có ban công",
  "Tìm căn hộ 3 phòng ngủ ở Thanh Xuân cho gia đình",
];

const needs = [
  {
    icon: "🌿",
    title: "Sống thoáng, ít ồn",
    text: "Ưu tiên ánh sáng, ban công và khoảng xanh yên tĩnh",
    prompt: "Tôi muốn nơi ở thoáng, yên tĩnh, nhiều ánh sáng tự nhiên và có ban công",
    accent: "from-emerald-500/20 to-teal-500/5",
    borderHover: "hover:border-emerald-400",
  },
  {
    icon: "🎒",
    title: "Tốt cho gia đình trẻ",
    text: "Gần trường học, tiện đi làm và đủ 2-3 phòng ngủ",
    prompt: "Tìm nhà phù hợp gia đình trẻ, 2 phòng ngủ, gần trường và tiện đi làm",
    accent: "from-amber-500/20 to-orange-500/5",
    borderHover: "hover:border-amber-400",
  },
  {
    icon: "📈",
    title: "Giữ giá & Pháp lý tốt",
    text: "Sổ đỏ sẵn sàng, khu vực có tiềm năng phát triển",
    prompt: "Tôi muốn mua để ở nhưng vẫn ưu tiên khả năng giữ giá và pháp lý rõ ràng",
    accent: "from-sky-500/20 to-blue-500/5",
    borderHover: "hover:border-sky-400",
  },
];

const districts = [
  { name: "Cầu Giấy", text: "Nhiều lựa chọn cho gia đình", tag: "Hot" },
  { name: "Thanh Xuân", text: "Kết nối giao thông thuận tiện", tag: "Phổ biến" },
  { name: "Nam Từ Liêm", text: "Nhiều dự án mới hiện đại", tag: "Mới" },
  { name: "Hà Đông", text: "Không gian rộng rãi, giá tốt", tag: "Ưu đãi" },
];

const locationShowcase = [
  { name: "Hà Nội", count: "hơn 3.700 BĐS đang mở xem", query: "Hà Nội", tone: "from-[#183d4e] via-[#477887] to-[#d5aa7b]", mark: "HN" },
  { name: "Hồ Chí Minh", count: "Kho nhà đang mở", query: "Hồ Chí Minh", tone: "from-[#172f42] via-[#436879] to-[#b97f61]", mark: "SG" },
  { name: "Đà Nẵng", count: "Kho nhà đang mở", query: "Đà Nẵng", tone: "from-[#17264e] via-[#3a5c9c] to-[#d89a68]", mark: "DN" },
  { name: "Bình Dương", count: "Kho nhà đang mở", query: "Bình Dương", tone: "from-[#183148] via-[#447393] to-[#8caa89]", mark: "BD" },
];

function HomepageExplore({
  properties,
  propertiesLoading,
  projectRailRef,
  moveProjects,
}: {
  properties: Property[];
  propertiesLoading: boolean;
  projectRailRef: RefObject<HTMLDivElement | null>;
  moveProjects: (direction: "left" | "right") => void;
}) {
  return (
    <>
      <section className="border-y border-black/5 bg-white px-4 py-16 sm:px-6 lg:px-8 lg:py-20">
        <div className="mx-auto max-w-7xl">
          <div className="mb-8 flex items-end justify-between gap-5">
            <div>
              <p className="text-xs font-bold uppercase tracking-[.2em] text-[var(--coral)]">
                Không gian đáng để xem
              </p>
              <h2 className="mt-3 text-3xl font-semibold tracking-[-.04em] sm:text-4xl text-stone-900">
                Dự án và cụm nhà nổi bật.
              </h2>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-[var(--muted)]">
                Nera gom những căn BĐS có thật thành một dòng khám phá. Bấm vào một thẻ để hỏi sâu hoặc đặt lịch xem thực tế.
              </p>
            </div>
            <div className="hidden items-center gap-2 sm:flex">
              <button
                type="button"
                onClick={() => moveProjects("left")}
                aria-label="Xem dự án trước"
                className="grid h-10 w-10 place-items-center rounded-full border border-black/10 bg-white text-[var(--forest)] shadow-xs transition hover:bg-[#edf3ed] hover:scale-105 active:scale-95"
              >
                <FaChevronLeft />
              </button>
              <button
                type="button"
                onClick={() => moveProjects("right")}
                aria-label="Xem dự án tiếp theo"
                className="grid h-10 w-10 place-items-center rounded-full border border-black/10 bg-white text-[var(--forest)] shadow-xs transition hover:bg-[#edf3ed] hover:scale-105 active:scale-95"
              >
                <FaChevronRight />
              </button>
            </div>
          </div>
          {propertiesLoading ? (
            <div className="flex gap-5 overflow-hidden">
              {Array.from({ length: 4 }).map((_, index) => (
                <div
                  key={index}
                  className="h-[330px] min-w-[280px] animate-pulse rounded-[1.4rem] bg-[#f2f3ef]"
                />
              ))}
            </div>
          ) : (
            <div
              ref={projectRailRef}
              className="flex snap-x gap-5 overflow-x-auto pb-4"
              style={{ scrollbarWidth: "none" }}
            >
              {properties.slice(0, 8).map((property, index) => {
                const image = property.image || property.media?.[0]?.url;
                const location =
                  [property.district, property.province].filter(Boolean).join(", ") ||
                  "Đang cập nhật vị trí";
                return (
                  <article
                    key={property.id}
                    className="group min-w-[280px] max-w-[340px] flex-1 snap-start overflow-hidden rounded-[1.45rem] border border-black/5 bg-[#fbfaf7] shadow-[0_10px_30px_rgba(22,47,42,.05)] transition-all duration-500 hover:-translate-y-1.5 hover:shadow-[0_20px_45px_rgba(22,47,42,.12)]"
                  >
                    <Link
                      href={`/properties/${property.id}`}
                      className="relative block h-48 overflow-hidden bg-gradient-to-br from-[#b8d0c0] to-[#e9c4ae]"
                    >
                      {image ? (
                        <PropertyImage
                          src={image}
                          alt={property.title}
                          className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
                        />
                      ) : (
                        <div className="grid h-full place-items-center text-5xl">🏙️</div>
                      )}
                      <span className="absolute left-3 top-3 inline-flex items-center gap-1 rounded-full bg-white/95 px-3 py-1.5 text-[10px] font-bold uppercase tracking-[.12em] text-[var(--forest)] shadow-xs backdrop-blur">
                        {index % 3 === 0 ? "🔥 Được quan tâm" : "🟢 Có thể xem"}
                      </span>
                      <span className="absolute bottom-3 right-3 rounded-full bg-black/55 px-2.5 py-1 text-xs font-semibold text-white backdrop-blur">
                        {property.media?.length || 1} ảnh
                      </span>
                    </Link>
                    <div className="p-5">
                      <div className="flex items-start justify-between gap-3">
                        <Link
                          href={`/properties/${property.id}`}
                          className="line-clamp-2 font-semibold leading-6 hover:text-[var(--forest)] transition-colors"
                        >
                          {property.title}
                        </Link>
                        <span className="shrink-0 text-sm font-bold text-[var(--coral)]">
                          {property.list_price
                            ? `${(property.list_price / 1e9).toFixed(1)} tỷ`
                            : "Liên hệ"}
                        </span>
                      </div>
                      <p className="mt-2.5 line-clamp-1 text-xs text-[var(--muted)]">
                        <FaMapMarkerAlt className="mr-1 inline text-[var(--forest)]" />
                        {location}
                      </p>
                      <div className="mt-4 flex items-center justify-between border-t border-black/5 pt-3.5 text-xs text-[var(--muted)]">
                        <span>
                          {property.area_sqm} m² · {property.bedrooms ?? "–"} PN
                        </span>
                        <Link
                          href={`/chat?property_id=${property.id}&prompt=${encodeURIComponent(
                            `Review chi tiết căn ${property.title}`
                          )}`}
                          className="font-semibold text-[var(--forest)] hover:underline inline-flex items-center gap-1"
                        >
                          Hỏi Nera <FaArrowRight className="text-[10px] transition-transform group-hover:translate-x-1" />
                        </Link>
                      </div>
                    </div>
                  </article>
                );
              })}
            </div>
          )}
          <Link
            href="/properties"
            className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-[var(--forest)] hover:underline"
          >
            Xem thêm trong kho hơn 3.700 nhà thật <FaArrowRight />
          </Link>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8 lg:py-24">
        <div className="mb-9 flex items-end justify-between gap-5">
          <div>
            <p className="text-xs font-bold uppercase tracking-[.2em] text-[var(--coral)]">
              Bản đồ nhu cầu
            </p>
            <h2 className="mt-3 text-3xl font-semibold tracking-[-.04em] sm:text-4xl text-stone-900">
              Bất động sản theo địa điểm.
            </h2>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-[var(--muted)]">
              Khám phá một khu vực trước, rồi để Nera thu hẹp theo ngân sách, nhịp sống và khoảng cách đi làm của bạn.
            </p>
          </div>
          <Link
            href="/properties"
            className="hidden items-center gap-2 text-sm font-semibold text-[var(--coral)] sm:flex hover:underline"
          >
            Xem toàn bộ <FaArrowRight />
          </Link>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {locationShowcase.map((location, index) => {
            const matched = properties.find((property) =>
              `${property.province} ${property.address_full}`
                .toLowerCase()
                .includes(location.query.toLowerCase())
            );
            const fallback = properties[index % Math.max(properties.length, 1)];
            const image =
              matched?.image ||
              matched?.media?.[0]?.url ||
              fallback?.image ||
              fallback?.media?.[0]?.url;
            const large = index === 0;
            return (
              <Link
                key={location.name}
                href={`/properties?keyword=${encodeURIComponent(location.query)}`}
                className={`group relative overflow-hidden rounded-[1.5rem] bg-gradient-to-br ${location.tone} shadow-sm transition-all duration-500 hover:-translate-y-1 hover:shadow-lg ${large ? "sm:col-span-2 sm:row-span-2 min-h-[330px]" : "min-h-[158px]"
                  }`}
              >
                {image && (
                  <PropertyImage
                    src={image}
                    alt={location.name}
                    className="absolute inset-0 h-full w-full object-cover opacity-50 mix-blend-luminosity transition-transform duration-700 group-hover:scale-105 group-hover:opacity-65"
                  />
                )}
                <div className="absolute inset-0 bg-gradient-to-t from-[#10231f]/80 via-[#10231f]/20 to-transparent" />
                <div className="relative flex h-full flex-col justify-between p-5 text-white sm:p-6">
                  <span className="text-xs font-bold uppercase tracking-[.22em] text-white/70">
                    {location.mark}
                  </span>
                  <div>
                    <h3 className={`${large ? "text-3xl" : "text-xl"} font-semibold tracking-[-.03em]`}>
                      {location.name}
                    </h3>
                    <p className="mt-1 text-sm text-white/80">{location.count}</p>
                    <span className="mt-4 inline-flex items-center gap-2 text-xs font-semibold text-white/95">
                      Khám phá ngay <FaArrowRight className="transition-transform group-hover:translate-x-1" />
                    </span>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </section>
    </>
  );
}

export default function AIHome() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [input, setInput] = useState("");
  const [memory, setMemory] = useState<MemoryResponse | null>(null);
  const [properties, setProperties] = useState<Property[]>([]);
  const [propertiesLoading, setPropertiesLoading] = useState(true);
  const [propertiesError, setPropertiesError] = useState(false);
  const projectRailRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let active = true;
    void apiFetch<{ items: Property[] }>("/properties?limit=9&sort=newest")
      .then((data) => {
        if (active) {
          setProperties(data.items ?? []);
          setPropertiesError(false);
        }
      })
      .catch(() => {
        if (active) setPropertiesError(true);
      })
      .finally(() => {
        if (active) setPropertiesLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (user?.role !== "CUSTOMER") {
      const timer = window.setTimeout(() => setMemory(null), 0);
      return () => window.clearTimeout(timer);
    }
    let active = true;
    void apiFetch<MemoryResponse>("/memory")
      .then((data) => {
        if (active) setMemory(data);
      })
      .catch(() => {
        if (active) setMemory(null);
      });
    return () => {
      active = false;
    };
  }, [user]);

  const firstName = useMemo(() => user?.full_name.trim().split(" ").at(-1), [user]);

  function startConversation(value: string) {
    const prompt = value.trim();
    if (prompt) router.push(`/chat?prompt=${encodeURIComponent(prompt)}&new=1`);
  }

  function submit(event: FormEvent) {
    event.preventDefault();
    startConversation(input);
  }

  function moveProjects(direction: "left" | "right") {
    projectRailRef.current?.scrollBy({
      left: direction === "right" ? 360 : -360,
      behavior: "smooth",
    });
  }

  if (!authLoading && user && user.role !== "CUSTOMER")
    return (
      <main className="grid min-h-screen place-items-center bg-[var(--paper)] px-6">
        <div className="max-w-lg rounded-[2rem] border border-black/5 bg-white p-10 text-center shadow-[0_30px_90px_rgba(22,47,42,.12)]">
          <span className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-[var(--ink)] text-white shadow-sm">
            <FaMagic />
          </span>
          <h1 className="mt-6 text-3xl font-semibold tracking-[-.04em]">Chào {firstName}</h1>
          <p className="mt-3 text-[var(--muted)]">Tài khoản của bạn có không gian vận hành riêng.</p>
          <Link
            href={roleHome(user.role)}
            className="mt-7 inline-flex items-center gap-2 rounded-full bg-[var(--ink)] px-6 py-3 font-semibold text-white shadow-md hover:bg-[var(--forest)] transition-colors"
          >
            Mở không gian làm việc <FaArrowRight />
          </Link>
        </div>
      </main>
    );

  return (
    <div className="min-h-screen overflow-hidden bg-[var(--paper)] text-[var(--ink)]">
      <Header />
      <main>
        {/* HERO SECTION */}
        <section className="relative border-b border-black/5 px-4 pb-16 pt-12 sm:px-6 lg:px-8 lg:pb-24 lg:pt-20">
          {/* Subtle Ambient Background Glows */}
          <div className="pointer-events-none absolute -right-24 top-0 h-[420px] w-[420px] rounded-full bg-gradient-to-br from-emerald-200/40 via-teal-100/30 to-transparent blur-3xl" />
          <div className="pointer-events-none absolute -left-20 bottom-0 h-[360px] w-[360px] rounded-full bg-gradient-to-tr from-orange-100/50 via-amber-100/30 to-transparent blur-3xl" />

          <div className="relative mx-auto grid max-w-7xl items-center gap-12 lg:grid-cols-[.84fr_1.16fr]">
            <div className="animate-soft-rise">
              <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-emerald-200/80 bg-emerald-50/80 px-4 py-2 text-xs sm:text-sm font-semibold text-[var(--forest)] shadow-xs backdrop-blur-md">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <FaMagic className="text-[var(--coral)]" /> Trợ lý AI BĐS • Đặt lịch xem O2O
              </div>
              <h1 className="max-w-xl text-4xl font-semibold leading-[1.08] tracking-[-.045em] sm:text-5xl lg:text-6xl text-stone-900">
                Không cần biết mình muốn gì.<br />
                <span className="text-[var(--forest)]">Chỉ cần kể, Nera sẽ hiểu.</span>
              </h1>
              <p className="mt-6 max-w-lg text-base sm:text-lg leading-8 text-[var(--muted)]">
                Nera lắng nghe, ghi nhớ điều bạn thích, giải thích lý do từng căn phù hợp và kết nối trực tiếp lịch làm việc của Sale.
              </p>
              <div className="mt-8 flex flex-wrap gap-x-6 gap-y-3 text-xs sm:text-sm text-[var(--muted)] font-medium">
                <span className="flex items-center gap-2">
                  <FaBrain className="text-[var(--forest)]" /> Nhớ sở thích đa lượt
                </span>
                <span className="flex items-center gap-2">
                  <FaShieldAlt className="text-[var(--forest)]" /> SQL Grounding hơn 3.700 BĐS
                </span>
                <span className="flex items-center gap-2">
                  <FaCalendarCheck className="text-[var(--forest)]" /> Sale duyệt giữ chỗ 15p
                </span>
              </div>
            </div>

            <div className="relative animate-soft-rise [animation-delay:120ms]">
              <div className="absolute -inset-3 rotate-1 rounded-[2.2rem] bg-gradient-to-r from-[var(--forest)]/10 via-[var(--sage)]/10 to-emerald-200/20 blur-sm" />
              <div className="relative overflow-hidden rounded-[2rem] border border-black/5 bg-white shadow-[0_35px_100px_rgba(21,48,42,.16)] backdrop-blur-sm">
                <div className="flex items-center justify-between border-b border-black/5 px-6 py-5 bg-stone-50/50">
                  <div className="flex items-center gap-3">
                    <span className="grid h-11 w-11 place-items-center rounded-2xl bg-[var(--forest)] text-white shadow-xs">
                      <img
                        src="/brand/logo/nera-symbol-light.svg"
                        alt="Nera"
                        className="h-6 w-6"
                      />
                    </span>
                    <div>
                      <p className="font-semibold text-stone-900">Nera</p>
                      <p className="text-xs text-[var(--muted)]">đang lắng nghe bạn</p>
                    </div>
                  </div>
                  <span className="flex items-center gap-2 text-xs font-semibold text-emerald-700 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-100">
                    <i className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" /> Sẵn sàng
                  </span>
                </div>

                {memory?.summary ? (
                  // RETURNING USER EXPERIENCE
                  <div className="min-h-[340px] flex flex-col justify-center bg-[#fbfaf7] p-5 sm:p-7 text-center">
                    <span className="text-4xl mb-3">👋</span>
                    <p className="text-[var(--forest)] font-bold text-xs uppercase tracking-wide">
                      Chào bạn quay lại
                    </p>
                    <h3 className="text-2xl font-semibold mt-2 text-stone-900">
                      Tiếp tục từ nơi bạn đã dừng
                    </h3>
                    <p className="text-sm text-[var(--muted)] mt-2 mx-auto max-w-sm leading-6">
                      Lần trước, Nera ghi nhớ bạn quan tâm: <strong>{memory.summary}</strong>.
                    </p>

                    <div className="mt-6 flex justify-center">
                      <div className="flex items-center text-xs text-[var(--muted)] font-medium">
                        <span className="flex flex-col items-center gap-1">
                          <span className="grid h-5 w-5 place-items-center rounded-full bg-[var(--forest)] text-white">
                            <FaCheckCircle />
                          </span>
                          Nhu cầu
                        </span>
                        <span className="w-8 h-px bg-black/10 mx-2" />
                        <span className="flex flex-col items-center gap-1">
                          <span className="grid h-5 w-5 place-items-center rounded-full bg-[var(--forest)] text-white">
                            <FaCheckCircle />
                          </span>
                          Gợi ý
                        </span>
                        <span className="w-8 h-px bg-black/10 mx-2" />
                        <span className="flex flex-col items-center gap-1">
                          <span className="grid h-5 w-5 place-items-center rounded-full border border-black/20 text-black/30">
                            3
                          </span>
                          Tiếp tục
                        </span>
                      </div>
                    </div>

                    <div className="mt-8 flex flex-col gap-3">
                      <button
                        onClick={() =>
                          startConversation("Tiếp tục tìm kiếm với nhu cầu cũ của tôi")
                        }
                        className="rounded-full bg-[var(--ink)] py-3.5 px-6 text-sm font-semibold text-white shadow-sm transition-all hover:bg-[var(--forest)] hover:shadow-md"
                      >
                        Tiếp tục hành trình →
                      </button>
                      <button
                        onClick={() =>
                          startConversation("Tôi muốn thay đổi nhu cầu tìm kiếm")
                        }
                        className="rounded-full border border-black/10 py-3.5 px-6 text-sm font-semibold transition hover:bg-stone-50"
                      >
                        Có, tôi muốn thay đổi nhu cầu
                      </button>
                    </div>
                  </div>
                ) : (
                  // NEW USER EXPERIENCE
                  <>
                    <div className="min-h-[340px] space-y-5 bg-[#fbfaf7] p-5 sm:p-7">
                      <div className="max-w-[90%] animate-message-in rounded-[1.4rem] rounded-tl-md bg-white p-5 text-[15px] leading-7 shadow-xs border border-black/5 text-stone-800">
                        {firstName ? `Chào ${firstName}. ` : "Chào bạn. "}
                        Bạn đang hình dung nơi ở tiếp theo như thế nào? Cứ nói tự nhiên — chưa cần biết chính xác quận hay dự án.
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {suggestions.map((suggestion) => (
                          <button
                            key={suggestion}
                            onClick={() => startConversation(suggestion)}
                            className="rounded-full border border-black/8 bg-white px-4 py-2.5 text-left text-xs font-medium text-[var(--muted)] shadow-xs transition-all duration-300 hover:-translate-y-0.5 hover:border-[var(--sage)] hover:text-[var(--forest)] hover:shadow-sm"
                          >
                            {suggestion}
                          </button>
                        ))}
                      </div>
                    </div>
                    <form
                      onSubmit={submit}
                      className="border-t border-black/5 bg-white p-4 sm:p-5"
                    >
                      <div className="flex items-end gap-3 rounded-[1.35rem] border border-black/10 bg-[#fbfaf7] p-2 pl-4 focus-within:border-[var(--sage)] focus-within:ring-4 focus-within:ring-[var(--sage)]/10 transition-all">
                        <textarea
                          aria-label="Nói điều bạn đang tìm"
                          rows={2}
                          value={input}
                          onChange={(event) => setInput(event.target.value)}
                          onKeyDown={(event) => {
                            if (event.key === "Enter" && !event.shiftKey) {
                              event.preventDefault();
                              startConversation(input);
                            }
                          }}
                          placeholder="Ví dụ: Căn 2 phòng ngủ ở Cầu Giấy, gần trường học, tầm 3 tỷ..."
                          className="max-h-32 min-h-12 flex-1 resize-none bg-transparent py-2 text-[15px] leading-6 outline-none placeholder:text-stone-400"
                        />
                        <button
                          disabled={!input.trim()}
                          className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-[var(--ink)] text-white shadow-sm transition-all hover:scale-105 hover:bg-[var(--forest)] disabled:opacity-30"
                          aria-label="Bắt đầu trò chuyện"
                        >
                          <FaPaperPlane />
                        </button>
                      </div>
                      <p className="mt-3 text-center text-[11px] text-stone-400">
                        Nhấn <strong>Enter</strong> để gửi · Nera sẽ tự động phân tích và tìm trong hơn 3.700 BĐS có sẵn
                      </p>
                    </form>
                  </>
                )}
              </div>
            </div>
          </div>
        </section>

        {/* SECTION: BẮT ĐẦU TỪ NHU CẦU THẬT */}
        <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8 lg:py-24">
          <div className="mb-9 max-w-2xl">
            <p className="text-xs font-bold uppercase tracking-[.2em] text-[var(--coral)]">
              Bắt đầu từ nhu cầu thật
            </p>
            <h2 className="mt-3 text-3xl font-semibold tracking-[-.04em] sm:text-4xl text-stone-900">
              Không cần biết tên dự án để bắt đầu.
            </h2>
            <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
              Chọn một tình huống gần với bạn, rồi điều chỉnh chi tiết qua cuộc trò chuyện với Nera.
            </p>
          </div>
          <div className="grid gap-5 md:grid-cols-3">
            {needs.map((need) => (
              <button
                key={need.title}
                onClick={() => startConversation(need.prompt)}
                className={`group relative overflow-hidden rounded-[1.7rem] border border-black/5 bg-white p-7 text-left shadow-[0_10px_35px_rgba(22,47,42,.05)] transition-all duration-500 hover:-translate-y-1.5 hover:shadow-[0_22px_55px_rgba(22,47,42,.12)] ${need.borderHover}`}
              >
                <div className={`absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r ${need.accent}`} />
                <span className="text-3xl sm:text-4xl">{need.icon}</span>
                <h3 className="mt-5 text-xl font-semibold text-stone-900 group-hover:text-[var(--forest)] transition-colors">
                  {need.title}
                </h3>
                <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{need.text}</p>
                <span className="mt-5 inline-flex items-center gap-2 text-xs sm:text-sm font-semibold text-[var(--forest)]">
                  Trao đổi với Nera <FaArrowRight className="text-xs transition-transform group-hover:translate-x-1.5" />
                </span>
              </button>
            ))}
          </div>
        </section>

        {/* SECTION: KHÁM PHÁ THEO KHU VỰC */}
        <section className="border-y border-black/5 bg-[#e7eee7]/70 px-4 py-16 sm:px-6 lg:px-8 lg:py-20">
          <div className="mx-auto max-w-7xl">
            <div className="grid items-end gap-7 lg:grid-cols-[.75fr_1.25fr]">
              <div>
                <p className="text-xs font-bold uppercase tracking-[.2em] text-[var(--coral)]">
                  Khám phá theo khu vực
                </p>
                <h2 className="mt-3 text-3xl font-semibold tracking-[-.04em] text-stone-900">
                  Chọn nơi bạn đã nghĩ tới.
                </h2>
                <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
                  Nera có sẵn dữ liệu tọa độ Geocode chuẩn cho toàn bộ các quận trọng điểm tại Hà Nội.
                </p>
              </div>
              <div className="grid gap-3.5 sm:grid-cols-2">
                {districts.map(({ name, text, tag }) => (
                  <Link
                    key={name}
                    href={`/properties?district=${encodeURIComponent(name)}`}
                    className="group flex items-center justify-between rounded-2xl bg-white/85 p-5 shadow-2xs transition-all duration-300 hover:bg-white hover:shadow-md hover:-translate-y-0.5 border border-black/5"
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <strong className="block text-stone-900">{name}</strong>
                        <span className="text-[10px] font-bold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-100">
                          {tag}
                        </span>
                      </div>
                      <small className="mt-1 block text-xs text-[var(--muted)]">{text}</small>
                    </div>
                    <FaArrowRight className="text-[var(--forest)] transition-transform group-hover:translate-x-1.5" />
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* SECTION: NHÀ MỚI ĐÁNG ĐỂ BẮT ĐẦU */}
        <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8 lg:py-24">
          <div className="mb-9 flex items-end justify-between gap-5">
            <div>
              <div className="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-[.2em] text-[var(--coral)]">
                <span className="h-2 w-2 rounded-full bg-[var(--coral)] animate-ping" />
                Dữ liệu thật từ kho nhà
              </div>
              <h2 className="mt-3 text-3xl font-semibold tracking-[-.04em] sm:text-4xl text-stone-900">
                Nhà mới đáng để bắt đầu cuộc trò chuyện.
              </h2>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-[var(--muted)]">
                Xem nhanh thông tin chính, lưu lại, đặt lịch hoặc nhờ Nera phân tích sâu và đo lộ trình Goong Maps.
              </p>
            </div>
            <Link
              href="/properties"
              className="hidden shrink-0 items-center gap-2 rounded-full border border-black/10 bg-white px-5 py-3 text-sm font-semibold text-[var(--forest)] shadow-xs transition hover:bg-stone-50 sm:flex"
            >
              Xem toàn bộ hơn 3.700 BĐS <FaArrowRight />
            </Link>
          </div>
          {propertiesLoading ? (
            <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {Array.from({ length: 6 }).map((_, index) => (
                <div
                  key={index}
                  className="h-[390px] animate-pulse rounded-[1.7rem] bg-white/70"
                />
              ))}
            </div>
          ) : propertiesError ? (
            <div className="rounded-[1.7rem] border border-amber-200 bg-amber-50 p-8 text-center">
              <p className="font-semibold text-amber-900">Kho nhà tạm thời chưa kết nối.</p>
              <p className="mt-2 text-sm text-amber-700">
                Bạn vẫn có thể trò chuyện với Nera hoặc thử tải lại sau.
              </p>
            </div>
          ) : (
            <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {properties.slice(0, 6).map((property) => (
                <PropertyTile key={property.id} property={property} />
              ))}
            </div>
          )}
          <Link
            href="/properties"
            className="mt-7 flex items-center justify-center gap-2 rounded-full border border-black/10 bg-white px-5 py-3 text-sm font-semibold text-[var(--forest)] shadow-xs sm:hidden"
          >
            Xem toàn bộ hơn 3.700 BĐS <FaArrowRight />
          </Link>
        </section>

        <HomepageExplore
          properties={properties}
          propertiesLoading={propertiesLoading}
          projectRailRef={projectRailRef}
          moveProjects={moveProjects}
        />

        {/* SECTION: TÌM NHÀ ĐÁNG TIN HƠN */}
        <section className="bg-[var(--ink)] px-4 py-16 text-white sm:px-6 lg:px-8 lg:py-20">
          <div className="mx-auto grid max-w-7xl gap-10 lg:grid-cols-[.9fr_1.1fr]">
            <div>
              <p className="text-xs font-bold uppercase tracking-[.2em] text-[#e8a58d]">
                Tìm nhà đáng tin hơn
              </p>
              <h2 className="mt-3 text-3xl font-semibold tracking-[-.04em] sm:text-4xl">
                AI giải thích. Dữ liệu kiểm chứng. Con người xác nhận.
              </h2>
              <p className="mt-5 max-w-xl leading-7 text-white/70">
                Nera không thay Sale quyết định lịch và không bịa căn ngoài hệ thống. Mỗi gợi ý đều dẫn về hơn 3.700 BĐS thật có thể đi xem thực tế.
              </p>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              {[
                [FaCompass, "Gợi ý có lý do", "Biết căn nào hợp ngân sách và điểm nào cần cân nhắc."],
                [FaCheckCircle, "Dữ liệu kiểm chứng", "Giá, diện tích và trạng thái lấy từ kho hơn 3.700 BĐS thật."],
                [FaCalendarCheck, "Luồng đặt lịch O2O", "Khóa giữ chỗ 15 phút, Sale nhận và xác nhận lịch."],
                [FaRegBookmark, "Hành trình xuyên suốt", "Chat, nhà đã lưu và sở thích lưu cùng một tài khoản."],
              ].map(([Icon, title, text]) => {
                const IconComponent = Icon as typeof FaCompass;
                return (
                  <div
                    key={String(title)}
                    className="rounded-2xl border border-white/10 bg-white/5 p-5 transition hover:bg-white/10 hover:border-white/20"
                  >
                    <IconComponent className="text-[#a9c9b0] text-xl" />
                    <h3 className="mt-4 font-semibold text-white">{String(title)}</h3>
                    <p className="mt-2 text-sm leading-6 text-white/60">{String(text)}</p>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* SECTION: CTA CUỐI TRANG */}
        <section className="px-4 py-16 sm:px-6 lg:px-8 lg:py-24">
          <div className="mx-auto max-w-5xl overflow-hidden rounded-[2.2rem] bg-[#dfe9e0] p-8 sm:p-12 shadow-sm">
            <div className="grid items-center gap-8 md:grid-cols-[1fr_auto]">
              <div>
                <span className="grid h-12 w-12 place-items-center rounded-2xl bg-white text-[var(--forest)] shadow-xs">
                  <FaMapMarkerAlt />
                </span>
                <h2 className="mt-5 text-3xl font-semibold tracking-[-.04em] text-stone-900">
                  Lần sau, Nera không hỏi lại từ đầu.
                </h2>
                <p className="mt-3 max-w-2xl text-[var(--muted)]">
                  Đăng nhập để lưu giữ lịch sử trò chuyện, danh sách căn đã lưu và những tiêu chí quan trọng với bạn.
                </p>
              </div>
              {!user ? (
                <Link
                  href="/login?next=/"
                  className="rounded-full bg-[var(--ink)] px-6 py-3.5 text-center text-sm font-semibold text-white shadow-sm transition hover:bg-[var(--forest)] hover:shadow-md"
                >
                  Đăng nhập để Nera nhớ bạn
                </Link>
              ) : (
                <Link
                  href="/chat"
                  className="inline-flex items-center justify-center gap-2 rounded-full bg-[var(--ink)] px-6 py-3.5 text-sm font-semibold text-white shadow-sm transition hover:bg-[var(--forest)] hover:shadow-md"
                >
                  Tiếp tục trò chuyện <FaArrowRight />
                </Link>
              )}
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
}
