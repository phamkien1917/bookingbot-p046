"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { FaMapMarkerAlt, FaBed, FaBath, FaRulerCombined, FaArrowRight, FaSpinner } from "react-icons/fa";
import { apiFetch } from "@/lib/api";
import type { Property } from "@/lib/types";
import { roleHome, useAuth } from "@/components/AuthProvider";
import PropertyImage from "@/components/PropertyImage";

export default function FeaturedProperties() {
  const { user } = useAuth();
  const [properties, setProperties] = useState<Property[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProperties = async () => {
      try {
        const data = await apiFetch<{ items: Property[] }>("/properties?limit=3");
        setProperties(data.items || []);
      } catch (err) {
        console.error("Failed to fetch featured properties:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchProperties();
  }, []);

  const formatPrice = (price: number) => {
    if (price >= 1_000_000_000) return `${(price / 1_000_000_000).toFixed(1)} Tỷ`;
    if (price >= 1_000_000) return `${(price / 1_000_000).toFixed(0)} Triệu`;
    return price.toLocaleString("vi-VN");
  };

  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-end mb-12">
          <div>
            <h2 className="text-3xl font-bold text-slate-900 mb-2">Căn hộ nổi bật</h2>
            <p className="text-slate-500">Gợi ý từ AI dựa trên xu hướng tìm kiếm</p>
          </div>
          <Link href="/properties" className="text-teal-600 font-semibold flex items-center hover:text-teal-700">
            Xem tất cả <FaArrowRight className="ml-2 text-sm" />
          </Link>
        </div>

        {loading ? (
          <div className="flex justify-center items-center py-12">
            <FaSpinner className="animate-spin text-4xl text-teal-500" />
          </div>
        ) : properties.length === 0 ? (
          <div className="text-center text-slate-500">Chưa có dữ liệu căn hộ nổi bật.</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {properties.map((prop, idx) => (
              <div key={prop.id || idx} className="bg-white rounded-3xl overflow-hidden border border-slate-100 shadow-sm hover:shadow-xl transition-all duration-300 group flex flex-col">
                {/* Image Container */}
                <div className="relative h-64 overflow-hidden bg-slate-200 shrink-0">
                  {prop.media && prop.media.length > 0 ? (
                    <PropertyImage
                      src={prop.media[0].url} 
                      alt={prop.title} 
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center bg-teal-50 text-4xl">🏠</div>
                  )}
                  
                  {/* Badges */}
                  <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm px-3 py-1.5 rounded-full text-xs font-bold text-teal-700 flex items-center shadow-sm">
                    <span className="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></span>
                    Có sẵn lịch xem
                  </div>
                  
                  <div className="absolute bottom-4 right-4 bg-white px-4 py-2 rounded-xl font-bold text-lg text-slate-900 shadow-md">
                    {prop.list_price ? formatPrice(prop.list_price) : "Liên hệ"}
                  </div>
                </div>

                {/* Info Container */}
                <div className="p-6 flex flex-col flex-1">
                  <h3 className="text-xl font-bold text-slate-800 mb-2 line-clamp-1">{prop.title}</h3>
                  <div className="flex items-center text-slate-500 text-sm mb-6">
                    <FaMapMarkerAlt className="mr-2 text-slate-400 shrink-0" />
                    <span className="line-clamp-1">{prop.address_full || prop.address_line || prop.district}</span>
                  </div>

                  <div className="flex items-center justify-between text-sm text-slate-600 font-medium mb-8 pb-6 border-b border-slate-100 mt-auto">
                    <div className="flex items-center"><FaBed className="mr-2 text-[#00b4d8] text-lg" /> {prop.bedrooms || 0} PN</div>
                    <div className="flex items-center"><FaBath className="mr-2 text-[#00b4d8] text-lg" /> {prop.bathrooms || 0} WC</div>
                    <div className="flex items-center"><FaRulerCombined className="mr-2 text-[#00b4d8] text-lg" /> {prop.area_sqm || 0} m²</div>
                  </div>

                  <div className="flex space-x-3 shrink-0">
                    <Link href={`/properties/${prop.id}`} className="flex-1 text-center bg-white border border-slate-200 text-slate-700 py-3 rounded-xl font-semibold hover:bg-slate-50 transition-colors">
                      Chi tiết
                    </Link>
                    <Link href={user && user.role !== "CUSTOMER" ? roleHome(user.role) : `/booking/schedule?property_id=${prop.id}`} className="flex-1 bg-[#0b132b] text-white py-3 rounded-xl font-semibold hover:bg-slate-800 transition-colors flex items-center justify-center">
                      <span className="mr-2">📅</span> {user && user.role !== "CUSTOMER" ? "Dashboard" : "Đặt lịch AI"}
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
