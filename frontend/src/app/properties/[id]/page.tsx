/* eslint-disable @next/next/no-img-element */
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
      <div className="min-h-screen bg-slate-50 flex flex-col">
        <Header />
        <div className="flex-1 flex justify-center items-center">
          <FaSpinner className="animate-spin text-4xl text-teal-500" />
        </div>
        <Footer />
      </div>
    );
  }

  if (error || !property) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col">
        <Header />
        <div className="flex-1 flex justify-center items-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-slate-800 mb-2">Lỗi: {error || "Không tìm thấy căn hộ"}</h1>
            <Link href="/properties" className="text-teal-600 hover:underline">Quay lại danh sách</Link>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Full image gallery */}
        <section className="mb-8" aria-label="Thư viện ảnh bất động sản">
          <div className="grid h-[360px] gap-3 sm:h-[460px] lg:grid-cols-[2fr_1fr]">
            <button type="button" onClick={() => galleryImages.length && setLightboxOpen(true)} className="group relative min-h-0 overflow-hidden rounded-2xl bg-slate-200 text-left focus:outline-none focus:ring-4 focus:ring-teal-500/30">
              {galleryImages[currentImageIndex] ? <img src={galleryImages[currentImageIndex].url} alt={galleryImages[currentImageIndex].caption || property.title} className="absolute inset-0 h-full w-full object-cover transition duration-500 group-hover:scale-[1.02]" /> : <div className="absolute inset-0 flex items-center justify-center text-4xl text-slate-400">🏠</div>}
              {galleryImages.length > 0 && <span className="absolute bottom-4 left-4 inline-flex items-center gap-2 rounded-full bg-black/65 px-4 py-2 text-xs font-semibold text-white"><FaImages /> {galleryImages.length} ảnh · Bấm để phóng to</span>}
            </button>
            <div className="grid min-h-0 grid-cols-2 gap-3 lg:grid-cols-1 lg:grid-rows-2">
              {galleryImages.slice(1, 3).map((image, offset) => {
                const index = offset + 1;
                return <button key={`${image.url}-${index}`} type="button" onClick={() => { setActiveImageIndex(index); setLightboxOpen(true); }} className="group relative min-h-0 overflow-hidden rounded-2xl bg-slate-200 text-left focus:outline-none focus:ring-4 focus:ring-teal-500/30"><img src={image.url} alt={image.caption || `${property.title} ${index + 1}`} className="absolute inset-0 h-full w-full object-cover transition duration-500 group-hover:scale-[1.03]" />{index === 2 && galleryImages.length > 3 && <span className="absolute inset-0 grid place-items-center bg-black/45 text-sm font-bold text-white">+{galleryImages.length - 2} ảnh khác</span>}</button>;
              })}
              {galleryImages.length < 2 && <div className="hidden rounded-2xl bg-slate-100 lg:block" />}
            </div>
          </div>
          {galleryImages.length > 0 && <div className="mt-3 flex gap-2 overflow-x-auto pb-1" aria-label="Chọn ảnh"><button type="button" onClick={() => { setActiveImageIndex(0); setLightboxOpen(true); }} className={`relative h-16 w-24 shrink-0 overflow-hidden rounded-lg border-2 ${activeImageIndex === 0 ? "border-teal-500" : "border-transparent"}`}><img src={galleryImages[0].url} alt="Ảnh đại diện" className="h-full w-full object-cover" /></button>{galleryImages.slice(1).map((image, index) => { const actualIndex = index + 1; return <button key={`${image.url}-thumb`} type="button" onClick={() => { setActiveImageIndex(actualIndex); setLightboxOpen(true); }} className={`relative h-16 w-24 shrink-0 overflow-hidden rounded-lg border-2 ${activeImageIndex === actualIndex ? "border-teal-500" : "border-transparent"}`}><img src={image.url} alt={`${property.title} ảnh ${actualIndex + 1}`} className="h-full w-full object-cover" /></button>; })}</div>}
        </section>

        {/* Badges */}
        <div className="flex gap-3 mb-4">
          <span className="px-4 py-1.5 bg-teal-100 text-teal-700 rounded-full text-xs font-bold">{property.status === "AVAILABLE" ? "Đang có sẵn" : "Đã đặt"}</span>
          <span className="px-4 py-1.5 bg-blue-100 text-blue-700 rounded-full text-xs font-bold">Đã xác minh</span>
          <span className="text-sm text-slate-500 ml-auto">Mã căn: #{property.code}</span>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Left Content */}
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-slate-800 mb-2">{property.title}</h1>
            <div className="flex items-center text-slate-500 text-sm mb-4">
              <FaMapMarkerAlt className="mr-2" /> {property.address_line || ""}, {property.ward || ""}, {property.district || ""}, {property.province || ""}
            </div>
            <p className="text-3xl font-bold text-[#0b132b] mb-6">
              {property.list_price ? formatPrice(property.list_price) : "Liên hệ"} <span className="text-base font-normal text-slate-400">VNĐ</span>
            </p>

            {/* Specs */}
            <div className="flex gap-8 mb-8 pb-8 border-b border-slate-200">
              <div className="text-center">
                <FaRulerCombined className="text-teal-500 text-2xl mx-auto mb-2" />
                <p className="text-sm text-slate-500">Diện tích</p>
                <p className="font-bold">{property.area_sqm || 0} m²</p>
              </div>
              <div className="text-center">
                <FaBed className="text-teal-500 text-2xl mx-auto mb-2" />
                <p className="text-sm text-slate-500">Phòng ngủ</p>
                <p className="font-bold">{property.bedrooms || 0} Phòng</p>
              </div>
              <div className="text-center">
                <FaBath className="text-teal-500 text-2xl mx-auto mb-2" />
                <p className="text-sm text-slate-500">Phòng tắm</p>
                <p className="font-bold">{property.bathrooms || 0} Phòng</p>
              </div>
              <div className="text-center">
                <FaMapMarkerAlt className="text-teal-500 text-2xl mx-auto mb-2" />
                <p className="text-sm text-slate-500">Hướng</p>
                <p className="font-bold">{String(property.features?.orientation ?? "Đang cập nhật")}</p>
              </div>
            </div>

            {/* Description */}
            <h2 className="text-xl font-bold text-slate-800 mb-4">Tổng quan</h2>
            <p className="text-slate-600 leading-relaxed mb-8 whitespace-pre-wrap">
              {property.description || "Chưa có thông tin mô tả."}
            </p>

            {/* Amenities */}
            <h2 className="text-xl font-bold text-slate-800 mb-4">Tiện ích nội khu</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
              {[
                { icon: <FaSwimmingPool />, label: "Hồ bơi vô cực" },
                { icon: <FaDumbbell />, label: "Phòng Gym 24/7" },
                { icon: <FaParking />, label: "Bãi đỗ xe thông minh" },
                { icon: <FaShieldAlt />, label: "An ninh đa lớp" },
                { icon: <FaTree />, label: "Công viên cây xanh" },
                { icon: <FaShoppingCart />, label: "Siêu thị tiện lợi" },
              ].map((item, idx) => (
                <div key={idx} className="flex items-center gap-3 bg-white border border-slate-100 rounded-xl px-4 py-3 text-sm text-slate-700">
                  <span className="text-teal-500 text-lg">{item.icon}</span>
                  {item.label}
                </div>
              ))}
            </div>

            {/* Map Placeholder */}
            <h2 className="text-xl font-bold text-slate-800 mb-4">Vị trí</h2>
            <div className="bg-slate-200 rounded-2xl h-72 flex items-center justify-center mb-8 overflow-hidden">
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
          <div className="w-full lg:w-[360px] shrink-0 mb-8 lg:mb-0">
            <div className="lg:sticky lg:top-20 space-y-6">
              {/* Booking Card */}
              <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm">
                <div className="flex justify-between items-center mb-4">
                  <div>
                    <p className="text-xs text-slate-500 uppercase tracking-wide">Trạng thái</p>
                    <p className="text-teal-600 font-bold flex items-center text-sm">
                      <span className="w-2 h-2 rounded-full bg-teal-500 mr-2"></span> {property.status === "AVAILABLE" ? "Sẵn sàng để xem" : "Đã đặt"}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-slate-500 uppercase tracking-wide">Khung giờ</p>
                    <p className="text-teal-600 font-bold text-sm">Kiểm tra theo ngày</p>
                  </div>
                </div>

                <p className="text-sm text-slate-600 mb-3">Chọn ngày để xem các khung giờ và nhân viên Sale đang thực sự rảnh.</p>

                <div className="bg-slate-50 rounded-xl p-3 mb-6 flex items-start gap-2">
                  <FaClock className="text-slate-400 mt-0.5 shrink-0" />
                  <p className="text-xs text-slate-500">Hệ thống AI sẽ tự động giữ khung giờ trong 15 phút sau khi bạn chọn để đảm bảo trải nghiệm tốt nhất.</p>
                </div>

                <Link href={user && user.role !== "CUSTOMER" ? roleHome(user.role) : `/booking/schedule?property_id=${property.id}`} className="block w-full bg-[#00b4d8] text-white py-3.5 rounded-xl text-sm font-bold text-center hover:bg-cyan-600 transition-colors mb-3">
                  <FaCalendarAlt className="inline mr-2" /> {user && user.role !== "CUSTOMER" ? "Về dashboard" : "Đặt lịch xem với AI"}
                </Link>
                <Link href={`/chat?property_id=${property.id}`} className="block w-full bg-white border border-slate-200 text-slate-700 py-3.5 rounded-xl text-sm font-bold text-center hover:bg-slate-50 transition-colors">
                  <FaComments className="inline mr-2" /> Chat với trợ lý
                </Link>
              </div>
            </div>
          </div>
        </div>
        {lightboxOpen && galleryImages[currentImageIndex] && <div role="dialog" aria-modal="true" aria-label="Xem ảnh bất động sản" className="fixed inset-0 z-[70] flex items-center justify-center bg-black/90 p-3 sm:p-6" onClick={() => setLightboxOpen(false)}>
          <div className="relative flex h-full w-full max-w-7xl flex-col items-center justify-center" onClick={(event) => event.stopPropagation()}>
            <button type="button" onClick={() => setLightboxOpen(false)} aria-label="Đóng thư viện ảnh" className="absolute right-0 top-0 z-10 rounded-full bg-white/10 p-3 text-xl text-white transition hover:bg-white/20"><FaTimes /></button>
            <div className="relative flex min-h-0 w-full flex-1 items-center justify-center">
              {galleryImages.length > 1 && <button type="button" onClick={showPreviousImage} aria-label="Ảnh trước" className="absolute left-0 z-10 rounded-full bg-white/15 p-3 text-xl text-white transition hover:bg-white/30 sm:left-3"><FaChevronLeft /></button>}
              <img src={galleryImages[currentImageIndex].url} alt={galleryImages[currentImageIndex].caption || `${property.title} ảnh ${currentImageIndex + 1}`} className="max-h-[78vh] max-w-full rounded-xl object-contain" />
              {galleryImages.length > 1 && <button type="button" onClick={showNextImage} aria-label="Ảnh tiếp theo" className="absolute right-0 z-10 rounded-full bg-white/15 p-3 text-xl text-white transition hover:bg-white/30 sm:right-3"><FaChevronRight /></button>}
            </div>
            <div className="mt-3 flex w-full max-w-5xl items-center gap-2 overflow-x-auto pb-1"><span className="mr-2 shrink-0 text-sm font-semibold text-white">{currentImageIndex + 1} / {galleryImages.length}</span>{galleryImages.map((image, index) => <button key={`${image.url}-lightbox-thumb`} type="button" onClick={() => setActiveImageIndex(index)} aria-label={`Xem ảnh ${index + 1}`} className={`h-14 w-20 shrink-0 overflow-hidden rounded-lg border-2 ${index === currentImageIndex ? "border-white" : "border-transparent opacity-60 hover:opacity-100"}`}><img src={image.url} alt="" className="h-full w-full object-cover" /></button>)}</div>
          </div>
        </div>}
      </main>
      <Footer />
    </div>
  );
}
