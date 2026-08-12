/* eslint-disable @next/next/no-img-element */
"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Link from "next/link";
import { FaMapMarkerAlt, FaBed, FaBath, FaRulerCombined, FaSwimmingPool, FaDumbbell, FaParking, FaShieldAlt, FaTree, FaShoppingCart, FaCalendarAlt, FaClock, FaSpinner } from "react-icons/fa";
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
        {/* Image Gallery */}
        <div className="grid grid-cols-3 gap-4 mb-8 h-[400px]">
          <div className="col-span-2 rounded-2xl overflow-hidden bg-slate-200 relative">
            {property.media && property.media[0] ? (
              <img src={property.media[0].url} alt="Main" className="absolute inset-0 w-full h-full object-cover" />
            ) : (
              <div className="absolute inset-0 flex items-center justify-center text-4xl text-slate-400">🏠</div>
            )}
          </div>
          <div className="flex flex-col gap-4">
            <div className="flex-1 rounded-2xl overflow-hidden bg-slate-200 relative">
              {property.media && property.media[1] ? (
                <img src={property.media[1].url} alt="Sub1" className="absolute inset-0 w-full h-full object-cover" />
              ) : (
                <div className="absolute inset-0 flex items-center justify-center text-2xl text-slate-400">📷</div>
              )}
            </div>
            <div className="flex-1 rounded-2xl overflow-hidden bg-slate-200 relative">
              {property.media && property.media[2] ? (
                <img src={property.media[2].url} alt="Sub2" className="absolute inset-0 w-full h-full object-cover" />
              ) : (
                <div className="absolute inset-0 flex items-center justify-center text-2xl text-slate-400">📷</div>
              )}
            </div>
          </div>
        </div>

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
      </main>
      <Footer />
    </div>
  );
}
