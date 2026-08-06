"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { FaMapMarkerAlt, FaBed, FaBath, FaRulerCombined, FaSearch, FaRegHeart, FaFilter, FaSpinner } from "react-icons/fa";

const API_BASE = "http://localhost:8000/api/v1";

export default function PropertiesPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [properties, setProperties] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchProperties();
  }, []);

  const fetchProperties = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE}/properties?limit=20`);
      if (!res.ok) throw new Error("Không thể tải danh sách căn hộ");
      const data = await res.json();
      setProperties(data.items || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price: number) => {
    if (price >= 1_000_000_000) return `${(price / 1_000_000_000).toFixed(1)} Tỷ`;
    if (price >= 1_000_000) return `${(price / 1_000_000).toFixed(0)} Triệu`;
    return price.toLocaleString("vi-VN");
  };

  const filteredProperties = properties.filter((p) =>
    p.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.address_full?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold italic text-slate-800 mb-6">Tìm kiếm không gian mơ ước</h1>

        {/* Search Bar */}
        <div className="relative mb-4">
          <FaSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
          <input type="text" placeholder="Tìm theo tên dự án, đường, quận..."
            value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-12 pr-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none bg-white" />
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-3 mb-6">
          <select className="px-4 py-2 rounded-lg border border-slate-200 text-sm text-slate-600 bg-white"><option>Mức giá</option></select>
          <select className="px-4 py-2 rounded-lg border border-slate-200 text-sm text-slate-600 bg-white"><option>Loại hình</option></select>
          <select className="px-4 py-2 rounded-lg border border-slate-200 text-sm text-slate-600 bg-white"><option>Phòng ngủ</option></select>
          <select className="px-4 py-2 rounded-lg border border-slate-200 text-sm text-slate-600 bg-white"><option>Diện tích</option></select>
          <button className="px-6 py-2 bg-[#0b132b] text-white rounded-lg text-sm font-semibold flex items-center hover:bg-slate-800">
            <FaFilter className="mr-2" /> Áp dụng
          </button>
        </div>

        <p className="text-sm text-slate-500 mb-6">Tìm thấy {filteredProperties.length} kết quả</p>

        {loading && (
          <div className="text-center py-20">
            <FaSpinner className="animate-spin text-4xl text-teal-500 mx-auto mb-4" />
            <p className="text-slate-500">Đang tải dữ liệu từ Backend...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-6 py-4 rounded-2xl text-center">
            <p className="font-semibold mb-1">Lỗi kết nối Backend</p>
            <p className="text-sm">{error}</p>
            <p className="text-xs text-slate-400 mt-2">Hãy chắc chắn server Backend đang chạy ở http://localhost:8000</p>
          </div>
        )}

        {!loading && !error && (
          <div className="flex gap-8">
            <div className="flex-1">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {filteredProperties.map((prop: any) => (
                  <div key={prop.id} className="bg-white rounded-2xl overflow-hidden border border-slate-100 shadow-sm hover:shadow-lg transition-all duration-300 group">
                    <div className="relative h-52 overflow-hidden bg-slate-200">
                      {prop.media && prop.media.length > 0 ? (
                        <img src={prop.media[0].url} alt={prop.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                      ) : (
                        <div className="w-full h-full bg-gradient-to-br from-teal-100 to-cyan-50 flex items-center justify-center">
                          <span className="text-4xl">🏠</span>
                        </div>
                      )}
                      <div className="absolute top-3 left-3 px-3 py-1 rounded-full text-xs font-bold text-white bg-teal-500">
                        Có thể xem
                      </div>
                      <button className="absolute top-3 right-3 w-8 h-8 bg-white/80 backdrop-blur-sm rounded-full flex items-center justify-center hover:bg-white">
                        <FaRegHeart className="text-slate-500 text-sm" />
                      </button>
                    </div>

                    <div className="p-5">
                      <h3 className="text-lg font-bold text-slate-800 mb-1 line-clamp-1">{prop.title}</h3>
                      <p className="text-teal-600 font-bold text-lg mb-1">{prop.price ? formatPrice(prop.price) + " VNĐ" : "Liên hệ"}</p>
                      <div className="flex items-center text-slate-500 text-xs mb-4">
                        <FaMapMarkerAlt className="mr-1" /> {prop.address_full || prop.district || "Chưa có địa chỉ"}
                      </div>
                      <div className="flex items-center gap-4 text-xs text-slate-500 mb-5">
                        {prop.bedrooms && <span className="flex items-center"><FaBed className="mr-1" />{prop.bedrooms}</span>}
                        {prop.bathrooms && <span className="flex items-center"><FaBath className="mr-1" />{prop.bathrooms}</span>}
                        {prop.area_m2 && <span className="flex items-center"><FaRulerCombined className="mr-1" />{prop.area_m2}m²</span>}
                      </div>
                      <div className="flex gap-2">
                        <Link href={`/properties/${prop.id}`} className="flex-1 text-center bg-white border border-slate-200 text-slate-700 py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-50">
                          Xem chi tiết
                        </Link>
                        <Link href="/chat" className="flex-1 text-center bg-[#00b4d8] text-white py-2.5 rounded-xl text-sm font-semibold hover:bg-cyan-600 transition-colors">
                          Đặt lịch AI
                        </Link>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {filteredProperties.length === 0 && !loading && (
                <div className="text-center py-16 text-slate-400">
                  <p className="text-4xl mb-3">🏠</p>
                  <p className="font-semibold">Chưa có căn hộ nào</p>
                  <p className="text-sm">Hãy thêm dữ liệu vào Database hoặc thay đổi bộ lọc</p>
                </div>
              )}
            </div>

            {/* Map Placeholder */}
            <div className="hidden lg:block w-[400px] shrink-0">
              <div className="sticky top-20 h-[calc(100vh-120px)] bg-slate-200 rounded-2xl overflow-hidden flex items-center justify-center">
                <div className="text-center text-slate-500">
                  <FaMapMarkerAlt className="text-4xl mx-auto mb-3 text-teal-500" />
                  <p className="font-semibold">Bản đồ vị trí</p>
                  <p className="text-sm">Tích hợp Google Maps</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}
