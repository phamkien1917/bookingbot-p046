"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { FaMapMarkerAlt, FaBed, FaBath, FaRulerCombined, FaSearch, FaRegHeart, FaFilter, FaSpinner } from "react-icons/fa";

const API_BASE = "http://localhost:8000/api/v1";

export default function PropertiesPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [priceFilter, setPriceFilter] = useState("all");
  const [typeFilter, setTypeFilter] = useState("all");
  const [bedFilter, setBedFilter] = useState("all");
  const [areaFilter, setAreaFilter] = useState("all");
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 9;
  
  const [properties, setProperties] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchProperties();
  }, []);

  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, priceFilter, typeFilter, bedFilter, areaFilter]);

  const fetchProperties = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE}/properties?limit=50`);
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

  const filteredProperties = properties.filter((p) => {
    // Search Term Filter
    if (searchTerm && !(p.title?.toLowerCase().includes(searchTerm.toLowerCase()) || p.address_full?.toLowerCase().includes(searchTerm.toLowerCase()))) {
      return false;
    }

    // Type Filter
    if (typeFilter !== "all" && p.property_kind !== typeFilter) {
      return false;
    }

    // Bedrooms Filter
    if (bedFilter !== "all") {
      const beds = p.bedrooms || 0;
      if (bedFilter === "1" && beds !== 1) return false;
      if (bedFilter === "2" && beds !== 2) return false;
      if (bedFilter === "3+" && beds < 3) return false;
    }

    // Price Filter
    if (priceFilter !== "all") {
      const price = p.list_price || 0;
      if (priceFilter === "under_3b" && price >= 3_000_000_000) return false;
      if (priceFilter === "3b_to_5b" && (price < 3_000_000_000 || price > 5_000_000_000)) return false;
      if (priceFilter === "over_5b" && price <= 5_000_000_000) return false;
    }

    // Area Filter
    if (areaFilter !== "all") {
      const area = p.area_sqm || 0;
      if (areaFilter === "under_50" && area >= 50) return false;
      if (areaFilter === "50_to_100" && (area < 50 || area > 100)) return false;
      if (areaFilter === "over_100" && area <= 100) return false;
    }

    return true;
  });

  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedProperties = filteredProperties.slice(startIndex, startIndex + itemsPerPage);
  const totalPages = Math.ceil(filteredProperties.length / itemsPerPage);

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 flex flex-col">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
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
          <select value={priceFilter} onChange={(e) => setPriceFilter(e.target.value)} className="px-4 py-2 rounded-lg border border-slate-200 text-sm text-slate-600 bg-white">
            <option value="all">Mọi mức giá</option>
            <option value="under_3b">Dưới 3 Tỷ</option>
            <option value="3b_to_5b">3 Tỷ - 5 Tỷ</option>
            <option value="over_5b">Trên 5 Tỷ</option>
          </select>
          <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)} className="px-4 py-2 rounded-lg border border-slate-200 text-sm text-slate-600 bg-white">
            <option value="all">Mọi loại hình</option>
            <option value="APARTMENT">Căn hộ chung cư</option>
            <option value="HOUSE">Nhà phố</option>
            <option value="VILLA">Biệt thự</option>
          </select>
          <select value={bedFilter} onChange={(e) => setBedFilter(e.target.value)} className="px-4 py-2 rounded-lg border border-slate-200 text-sm text-slate-600 bg-white">
            <option value="all">Phòng ngủ</option>
            <option value="1">1 Phòng</option>
            <option value="2">2 Phòng</option>
            <option value="3+">3 Phòng trở lên</option>
          </select>
          <select value={areaFilter} onChange={(e) => setAreaFilter(e.target.value)} className="px-4 py-2 rounded-lg border border-slate-200 text-sm text-slate-600 bg-white">
            <option value="all">Diện tích</option>
            <option value="under_50">Dưới 50m²</option>
            <option value="50_to_100">50m² - 100m²</option>
            <option value="over_100">Trên 100m²</option>
          </select>
          <button onClick={() => { setPriceFilter("all"); setTypeFilter("all"); setBedFilter("all"); setAreaFilter("all"); setSearchTerm(""); }} className="px-6 py-2 bg-slate-200 text-slate-700 rounded-lg text-sm font-semibold hover:bg-slate-300">
            Xóa bộ lọc
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
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {paginatedProperties.map((prop: any) => (
                  <div key={prop.id} className="bg-white rounded-2xl overflow-hidden border border-slate-100 shadow-sm hover:shadow-lg transition-all duration-300 group flex flex-col">
                    <div className="relative h-52 overflow-hidden bg-slate-200 shrink-0">
                      {prop.media && prop.media.length > 0 ? (
                        <img src={prop.media[0].url} alt={prop.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                      ) : (
                        <div className="w-full h-full bg-gradient-to-br from-teal-100 to-cyan-50 flex items-center justify-center">
                          <span className="text-4xl">🏠</span>
                        </div>
                      )}
                      <div className="absolute top-3 left-3 px-3 py-1 rounded-full text-xs font-bold text-white bg-teal-500 shadow-sm">
                        Có thể xem
                      </div>
                      <button className="absolute top-3 right-3 w-8 h-8 bg-white/80 backdrop-blur-sm rounded-full flex items-center justify-center hover:bg-white shadow-sm">
                        <FaRegHeart className="text-slate-500 text-sm" />
                      </button>
                    </div>

                    <div className="p-5 flex flex-col flex-1">
                      <h3 className="text-lg font-bold text-slate-800 mb-1 line-clamp-1">{prop.title}</h3>
                      <p className="text-teal-600 font-bold text-lg mb-1">{prop.list_price ? formatPrice(prop.list_price) + " VNĐ" : "Liên hệ"}</p>
                      <div className="flex items-center text-slate-500 text-xs mb-4">
                        <FaMapMarkerAlt className="mr-1 shrink-0" /> <span className="line-clamp-1">{prop.address_line || ""}, {prop.ward || ""}, {prop.district || prop.address_full}</span>
                      </div>
                      <div className="flex items-center gap-4 text-xs text-slate-500 mb-5 mt-auto">
                        <span className="flex items-center"><FaBed className="mr-1 text-teal-500" />{prop.bedrooms || 0}</span>
                        <span className="flex items-center"><FaBath className="mr-1 text-teal-500" />{prop.bathrooms || 0}</span>
                        <span className="flex items-center"><FaRulerCombined className="mr-1 text-teal-500" />{prop.area_sqm || 0}m²</span>
                      </div>
                      <div className="flex gap-2 shrink-0">
                        <Link href={`/properties/${prop.id}`} className="flex-1 text-center bg-white border border-slate-200 text-slate-700 py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-50">
                          Xem chi tiết
                        </Link>
                        <Link href={`/chat?property_id=${prop.id}`} className="flex-1 text-center bg-[#00b4d8] text-white py-2.5 rounded-xl text-sm font-semibold hover:bg-cyan-600 transition-colors">
                          Đặt lịch AI
                        </Link>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="flex justify-center items-center gap-2 mt-10">
                  <button
                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                    disabled={currentPage === 1}
                    className="px-4 py-2 rounded-xl border border-slate-200 text-slate-600 bg-white hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
                  >
                    Trước
                  </button>
                  <div className="flex gap-1">
                    {Array.from({ length: totalPages }).map((_, idx) => (
                      <button
                        key={idx}
                        onClick={() => setCurrentPage(idx + 1)}
                        className={`w-10 h-10 rounded-xl font-bold transition-colors ${
                          currentPage === idx + 1
                            ? "bg-teal-500 text-white shadow-md shadow-teal-500/20"
                            : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-50"
                        }`}
                      >
                        {idx + 1}
                      </button>
                    ))}
                  </div>
                  <button
                    onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                    disabled={currentPage === totalPages}
                    className="px-4 py-2 rounded-xl border border-slate-200 text-slate-600 bg-white hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
                  >
                    Sau
                  </button>
                </div>
              )}

              {filteredProperties.length === 0 && !loading && (
                <div className="text-center py-16 text-slate-400 bg-white rounded-2xl border border-slate-100">
                  <p className="text-4xl mb-3">🏠</p>
                  <p className="font-semibold">Chưa có căn hộ nào phù hợp</p>
                  <p className="text-sm mt-1">Hãy thay đổi bộ lọc hoặc từ khóa tìm kiếm</p>
                </div>
              )}
            </div>


          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}
