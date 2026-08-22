"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Link from "next/link";
import { FaMapMarkerAlt, FaBed, FaBath, FaRulerCombined, FaSwimmingPool, FaDumbbell, FaParking, FaShieldAlt, FaTree, FaShoppingCart, FaCalendarAlt, FaClock, FaSpinner, FaChevronLeft, FaChevronRight, FaTimes, FaImages } from "react-icons/fa";
import { FaComments } from "react-icons/fa6";
import { apiFetch } from "@/lib/api";
import type { Property } from "@/lib/types";
import { roleHome, useAuth } from "@/components/AuthProvider";
import PropertyImage from "@/components/PropertyImage";

export default function PropertyDetail() {
  const { user } = useAuth();
  const params = useParams<{ id: string }>();
  const id = params.id;
  const [property, setProperty] = useState<Property | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeImageIndex, setActiveImageIndex] = useState(0);
  const [lightboxOpen, setLightboxOpen] = useState(false);

  useEffect(() => {
    if (!id) return;
    const timer = window.setTimeout(async () => {
      try {
        setProperty(await apiFetch<Property>(`/properties/${id}`));
      } catch (err) {
        setError(err instanceof Error ? err.message : "Không tìm thấy bất động sản");
      } finally {
        setLoading(false);
      }
    }, 0);
    return () => window.clearTimeout(timer);
  }, [id]);

  const galleryImages = property
    ? property.media?.length
      ? [...property.media].sort((a, b) => (a.sort_order ?? 0) - (b.sort_order ?? 0))
      : property.image
        ? [{ url: property.image }]
        : []
    : [];

  useEffect(() => {
    if (!lightboxOpen) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setLightboxOpen(false);
      if (event.key === "ArrowLeft" && galleryImages.length > 1) {
        setActiveImageIndex((index) => (index - 1 + galleryImages.length) % galleryImages.length);
      }
      if (event.key === "ArrowRight" && galleryImages.length > 1) {
        setActiveImageIndex((index) => (index + 1) % galleryImages.length);
      }
    };
    document.addEventListener("keydown", onKeyDown);
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = previousOverflow;
    };
  }, [lightboxOpen, galleryImages.length]);

  const showPreviousImage = () => setActiveImageIndex((index) => (index - 1 + galleryImages.length) % galleryImages.length);
  const showNextImage = () => setActiveImageIndex((index) => (index + 1) % galleryImages.length);
  const currentImageIndex = galleryImages.length ? Math.min(activeImageIndex, galleryImages.length - 1) : 0;

  const formatPrice = (price: number) => {
    if (price >= 1_000_000_000) return `${(price / 1_000_000_000).toFixed(1)} Tỷ`;
    if (price >= 1_000_000) return `${(price / 1_000_000).toFixed(0)} Triệu`;
    return price.toLocaleString("vi-VN");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[var(--paper)] flex flex-col">
        <Header />
        <div className="flex-1 flex justify-center items-center">
          <FaSpinner className="animate-spin text-4xl text-[var(--forest)]" />
        </div>
        <Footer />
      </div>
    );
  }

  if (error || !property) {
    return (
      <div className="min-h-screen bg-[var(--paper)] flex flex-col">
        <Header />
        <div className="flex-1 flex justify-center items-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-[var(--ink)] mb-2">Lỗi: {error || "Không tìm thấy căn hộ"}</h1>
            <Link href="/properties" className="text-[var(--forest)] hover:underline">Quay lại danh sách</Link>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[var(--paper)] font-sans text-[var(--ink)]">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Full image gallery */}
        <section className="mb-8" aria-label="Thư viện ảnh bất động sản">
          <div className="grid h-[360px] gap-3 sm:h-[460px] lg:grid-cols-[2fr_1fr]">
            <button type="button" onClick={() => galleryImages.length && setLightboxOpen(true)} className="group relative min-h-0 overflow-hidden rounded-[1.5rem] bg-[#e6eee7] text-left focus:outline-none focus:ring-4 focus:ring-[var(--forest)]/30 transition-transform hover:scale-[1.01] shadow-sm">
              {galleryImages[currentImageIndex] ? <PropertyImage src={galleryImages[currentImageIndex].url} alt={galleryImages[currentImageIndex].caption || property.title} className="absolute inset-0 h-full w-full object-cover transition duration-700 group-hover:scale-105" /> : <div className="absolute inset-0 flex items-center justify-center text-5xl text-[var(--sage)] opacity-50">🏠</div>}
              {galleryImages.length > 0 && <span className="absolute bottom-4 left-4 inline-flex items-center gap-2 rounded-full bg-[var(--ink)]/80 px-4 py-2 text-xs font-semibold text-white backdrop-blur-sm"><FaImages /> {galleryImages.length} ảnh · Bấm để phóng to</span>}
            </button>
            <div className="grid min-h-0 grid-cols-2 gap-3 lg:grid-cols-1 lg:grid-rows-2">
              {galleryImages.slice(1, 3).map((image, offset) => {
                const index = offset + 1;
                return <button key={`${image.url}-${index}`} type="button" onClick={() => { setActiveImageIndex(index); setLightboxOpen(true); }} className="group relative min-h-0 overflow-hidden rounded-[1.5rem] bg-[#e6eee7] text-left focus:outline-none focus:ring-4 focus:ring-[var(--forest)]/30 transition-transform hover:scale-[1.02] shadow-sm"><PropertyImage src={image.url} alt={image.caption || `${property.title} ${index + 1}`} className="absolute inset-0 h-full w-full object-cover transition duration-700 group-hover:scale-110" />{index === 2 && galleryImages.length > 3 && <span className="absolute inset-0 grid place-items-center bg-[var(--ink)]/50 backdrop-blur-sm text-sm font-bold text-white transition-opacity group-hover:bg-[var(--ink)]/60">+{galleryImages.length - 2} ảnh khác</span>}</button>;
              })}
              {galleryImages.length < 2 && <div className="hidden rounded-[1.5rem] bg-[#fbfaf7] border border-black/5 lg:block shadow-sm" />}
            </div>
          </div>
          {galleryImages.length > 0 && <div className="mt-4 flex gap-3 overflow-x-auto pb-2" aria-label="Chọn ảnh"><button type="button" onClick={() => { setActiveImageIndex(0); setLightboxOpen(true); }} className={`relative h-20 w-28 shrink-0 overflow-hidden rounded-xl border-2 transition-all ${activeImageIndex === 0 ? "border-[var(--forest)] ring-2 ring-[var(--forest)]/30" : "border-transparent opacity-70 hover:opacity-100 hover:scale-105"}`}><PropertyImage src={galleryImages[0].url} alt="Ảnh đại diện" className="h-full w-full object-cover" /></button>{galleryImages.slice(1).map((image, index) => { const actualIndex = index + 1; return <button key={`${image.url}-thumb`} type="button" onClick={() => { setActiveImageIndex(actualIndex); setLightboxOpen(true); }} className={`relative h-20 w-28 shrink-0 overflow-hidden rounded-xl border-2 transition-all ${activeImageIndex === actualIndex ? "border-[var(--forest)] ring-2 ring-[var(--forest)]/30" : "border-transparent opacity-70 hover:opacity-100 hover:scale-105"}`}><PropertyImage src={image.url} alt={`${property.title} ảnh ${actualIndex + 1}`} className="h-full w-full object-cover" /></button>; })}</div>}
        </section>

        {/* Badges */}
        <div className="flex gap-3 mb-6">
          <span className={`px-4 py-1.5 rounded-full text-xs font-bold shadow-sm ${property.status === "AVAILABLE" ? "bg-emerald-50 text-[var(--forest)]" : "bg-amber-50 text-amber-700"}`}>{property.status === "AVAILABLE" ? "Đang có sẵn" : "Đã đặt"}</span>
          <span className="px-4 py-1.5 bg-blue-50 text-blue-700 rounded-full text-xs font-bold shadow-sm">Đã xác minh</span>
          <span className="text-sm text-[var(--muted)] ml-auto font-mono bg-white px-3 py-1 rounded-lg border border-black/5">Mã căn: #{property.code}</span>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Left Content */}
          <div className="flex-1">
            <h1 className="text-4xl font-bold mb-3 tracking-tight">{property.title}</h1>
            <div className="flex items-center text-[var(--muted)] text-sm mb-6 bg-white w-fit px-4 py-2 rounded-xl border border-black/5 shadow-sm">
              <FaMapMarkerAlt className="mr-2 text-[var(--coral)]" /> {property.address_line || ""}, {property.ward || ""}, {property.district || ""}, {property.province || ""}
            </div>
            <p className="text-4xl font-bold text-[var(--coral)] mb-8 flex items-baseline gap-2">
              {property.list_price ? formatPrice(property.list_price) : "Liên hệ"} <span className="text-lg font-semibold text-[var(--muted)]">VNĐ</span>
            </p>

            {/* Specs */}
            <div className="flex flex-wrap gap-8 mb-10 pb-10 border-b border-black/10">
              <div className="flex-1 text-center bg-white p-4 rounded-[1.5rem] border border-black/5 shadow-sm hover:shadow-md transition-shadow">
                <FaRulerCombined className="text-[var(--forest)] text-3xl mx-auto mb-3" />
                <p className="text-xs text-[var(--muted)] uppercase tracking-wider font-semibold mb-1">Diện tích</p>
                <p className="font-bold text-lg">{property.area_sqm || 0} m²</p>
              </div>
              <div className="flex-1 text-center bg-white p-4 rounded-[1.5rem] border border-black/5 shadow-sm hover:shadow-md transition-shadow">
                <FaBed className="text-[var(--forest)] text-3xl mx-auto mb-3" />
                <p className="text-xs text-[var(--muted)] uppercase tracking-wider font-semibold mb-1">Phòng ngủ</p>
                <p className="font-bold text-lg">{property.bedrooms || 0} Phòng</p>
              </div>
              <div className="flex-1 text-center bg-white p-4 rounded-[1.5rem] border border-black/5 shadow-sm hover:shadow-md transition-shadow">
                <FaBath className="text-[var(--forest)] text-3xl mx-auto mb-3" />
                <p className="text-xs text-[var(--muted)] uppercase tracking-wider font-semibold mb-1">Phòng tắm</p>
                <p className="font-bold text-lg">{property.bathrooms || 0} Phòng</p>
              </div>
              <div className="flex-1 text-center bg-white p-4 rounded-[1.5rem] border border-black/5 shadow-sm hover:shadow-md transition-shadow">
                <FaMapMarkerAlt className="text-[var(--forest)] text-3xl mx-auto mb-3" />
                <p className="text-xs text-[var(--muted)] uppercase tracking-wider font-semibold mb-1">Hướng</p>
                <p className="font-bold text-lg">{String(property.features?.orientation ?? "Đang cập nhật")}</p>
              </div>
            </div>

            {/* Description */}
            <h2 className="text-2xl font-bold mb-5 flex items-center gap-2">Tổng quan</h2>
            <div className="bg-white p-6 md:p-8 rounded-[1.5rem] border border-black/5 shadow-sm mb-10">
              <p className="text-[var(--muted)] leading-relaxed whitespace-pre-wrap text-[15px]">
                {property.description || "Chưa có thông tin mô tả."}
              </p>
            </div>

            {/* Amenities */}
            <h2 className="text-2xl font-bold mb-5 flex items-center gap-2">Tiện ích nội khu</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-10">
              {[
                { icon: <FaSwimmingPool />, label: "Hồ bơi vô cực" },
                { icon: <FaDumbbell />, label: "Phòng Gym 24/7" },
                { icon: <FaParking />, label: "Bãi đỗ xe thông minh" },
                { icon: <FaShieldAlt />, label: "An ninh đa lớp" },
                { icon: <FaTree />, label: "Công viên cây xanh" },
                { icon: <FaShoppingCart />, label: "Siêu thị tiện lợi" },
              ].map((item, idx) => (
                <div key={idx} className="flex items-center gap-3 bg-white border border-black/5 shadow-sm rounded-xl px-5 py-4 text-sm font-medium hover:border-[var(--sage)] transition-colors">
                  <span className="text-[var(--forest)] text-xl">{item.icon}</span>
                  {item.label}
                </div>
              ))}
            </div>

            {/* Map Placeholder */}
            <h2 className="text-2xl font-bold mb-5 flex items-center gap-2">Vị trí</h2>
            <div className="bg-[#e6eee7] rounded-[1.5rem] h-[400px] flex items-center justify-center mb-8 overflow-hidden shadow-sm border border-black/5">
              <iframe
                width="100%"
                height="100%"
                frameBorder="0"
                style={{ border: 0 }}
                src={`https://maps.google.com/maps?q=${encodeURIComponent(
                  `${property.address_line || ''}, ${property.ward || ''}, ${property.district || ''}, ${property.province || ''}`
                )}&t=&z=15&ie=UTF8&iwloc=&output=embed`}
                allowFullScreen
              ></iframe>
            </div>
          </div>

          {/* Right Sidebar */}
          <div className="w-full lg:w-[380px] shrink-0 mb-8 lg:mb-0">
            <div className="lg:sticky lg:top-24 space-y-6">
              {/* Booking Card */}
              <div className="bg-white border border-black/5 rounded-[1.5rem] p-7 shadow-xl">
                <div className="flex justify-between items-center mb-6 pb-6 border-b border-black/5">
                  <div>
                    <p className="text-xs text-[var(--muted)] uppercase tracking-[.15em] font-bold mb-1">Trạng thái</p>
                    <p className="text-[var(--forest)] font-bold flex items-center text-sm">
                      <span className="w-2 h-2 rounded-full bg-[var(--forest)] mr-2 animate-pulse"></span> {property.status === "AVAILABLE" ? "Sẵn sàng để xem" : "Đã đặt"}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-[var(--muted)] uppercase tracking-[.15em] font-bold mb-1">Khung giờ</p>
                    <p className="text-[var(--ink)] font-bold text-sm">Kiểm tra theo ngày</p>
                  </div>
                </div>

                <p className="text-sm text-[var(--muted)] mb-5 leading-relaxed">Chọn ngày để xem các khung giờ và nhân viên Sale đang thực sự rảnh.</p>

                <div className="bg-[#fbfaf7] rounded-xl p-4 mb-6 border border-black/5">
                  <p className="text-xs text-[var(--muted)] leading-relaxed flex items-start"><FaClock className="text-[var(--coral)] mt-0.5 shrink-0 mr-2 text-sm" /> Hệ thống AI sẽ tự động giữ khung giờ trong 15 phút sau khi bạn chọn để đảm bảo trải nghiệm tốt nhất.</p>
                </div>

                <Link href={user && user.role !== "CUSTOMER" ? roleHome(user.role) : `/booking/schedule?property_id=${property.id}`} className="block w-full bg-[var(--ink)] text-white py-4 rounded-xl text-sm font-bold text-center hover:bg-[var(--forest)] hover:-translate-y-1 transition-all shadow-md mb-4">
                  <FaCalendarAlt className="inline mr-2 text-lg" /> {user && user.role !== "CUSTOMER" ? "Về dashboard" : "Đặt lịch xem với AI"}
                </Link>
                <Link href={`/chat?property_id=${property.id}`} className="block w-full bg-white border-2 border-[var(--ink)] text-[var(--ink)] py-3.5 rounded-xl text-sm font-bold text-center hover:bg-[#fbfaf7] hover:-translate-y-1 transition-all shadow-sm">
                  <FaComments className="inline mr-2 text-lg" /> Chat với trợ lý
                </Link>
              </div>
            </div>
          </div>
        </div>
        
        {lightboxOpen && galleryImages[currentImageIndex] && <div role="dialog" aria-modal="true" aria-label="Xem ảnh bất động sản" className="fixed inset-0 z-[70] flex items-center justify-center bg-[var(--ink)]/95 backdrop-blur-sm p-3 sm:p-6" onClick={() => setLightboxOpen(false)}>
          <div className="relative flex h-full w-full max-w-7xl flex-col items-center justify-center" onClick={(event) => event.stopPropagation()}>
            <button type="button" onClick={() => setLightboxOpen(false)} aria-label="Đóng thư viện ảnh" className="absolute right-0 top-0 z-10 rounded-full bg-white/10 p-3 text-xl text-white transition hover:bg-white/30"><FaTimes /></button>
            <div className="relative flex min-h-0 w-full flex-1 items-center justify-center">
              {galleryImages.length > 1 && <button type="button" onClick={showPreviousImage} aria-label="Ảnh trước" className="absolute left-0 z-10 rounded-full bg-white/15 p-4 text-xl text-white transition hover:bg-white/30 sm:left-3 hover:scale-110"><FaChevronLeft /></button>}
              <PropertyImage src={galleryImages[currentImageIndex].url} alt={galleryImages[currentImageIndex].caption || `${property.title} ảnh ${currentImageIndex + 1}`} className="max-h-[85vh] max-w-full rounded-2xl object-contain shadow-2xl" />
              {galleryImages.length > 1 && <button type="button" onClick={showNextImage} aria-label="Ảnh tiếp theo" className="absolute right-0 z-10 rounded-full bg-white/15 p-4 text-xl text-white transition hover:bg-white/30 sm:right-3 hover:scale-110"><FaChevronRight /></button>}
            </div>
            <div className="mt-4 flex w-full max-w-5xl items-center gap-3 overflow-x-auto pb-2"><span className="mr-3 shrink-0 text-sm font-bold tracking-widest text-white/70 bg-black/40 px-3 py-1 rounded-full">{currentImageIndex + 1} / {galleryImages.length}</span>{galleryImages.map((image, index) => <button key={`${image.url}-lightbox-thumb`} type="button" onClick={() => setActiveImageIndex(index)} aria-label={`Xem ảnh ${index + 1}`} className={`h-16 w-24 shrink-0 overflow-hidden rounded-xl border-2 transition-all ${index === currentImageIndex ? "border-[var(--coral)] ring-2 ring-[var(--coral)]/50 scale-105" : "border-transparent opacity-50 hover:opacity-100"}`}><PropertyImage src={image.url} alt="" className="h-full w-full object-cover" /></button>)}</div>
          </div>
        </div>}
      </main>
      <Footer />
    </div>
  );
}
