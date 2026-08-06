import { FaMapMarkerAlt, FaBed, FaBath, FaRulerCombined, FaArrowRight } from "react-icons/fa";

export default function FeaturedProperties() {
  const properties = [
    {
      title: "The River Thủ Thiêm - Tháp Seine",
      address: "Đại lộ Vòng Cung, Thủ Thiêm, Quận 2",
      price: "4.5 Tỷ",
      beds: 2,
      baths: 2,
      area: 85,
      image: "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80"
    },
    {
      title: "Empire City - Linden Residences",
      address: "Khu đô thị mới Thủ Thiêm, Quận 2",
      price: "6.2 Tỷ",
      beds: 3,
      baths: 2,
      area: 110,
      image: "https://images.unsplash.com/photo-1600607687931-ce71171f1e73?auto=format&fit=crop&w=800&q=80"
    },
    {
      title: "Masteri Thảo Điền - Tòa T1",
      address: "Xa lộ Hà Nội, Thảo Điền, Quận 2",
      price: "3.8 Tỷ",
      beds: 2,
      baths: 1,
      area: 70,
      image: "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=800&q=80"
    }
  ];

  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-end mb-12">
          <div>
            <h2 className="text-3xl font-bold text-slate-900 mb-2">Căn hộ nổi bật</h2>
            <p className="text-slate-500">Gợi ý từ AI dựa trên xu hướng tìm kiếm</p>
          </div>
          <button className="text-teal-600 font-semibold flex items-center hover:text-teal-700">
            Xem tất cả <FaArrowRight className="ml-2 text-sm" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {properties.map((prop, idx) => (
            <div key={idx} className="bg-white rounded-3xl overflow-hidden border border-slate-100 shadow-sm hover:shadow-xl transition-all duration-300 group">
              {/* Image Container */}
              <div className="relative h-64 overflow-hidden bg-slate-200">
                <img 
                  src={prop.image} 
                  alt={prop.title} 
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
                
                {/* Badges */}
                <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm px-3 py-1.5 rounded-full text-xs font-bold text-teal-700 flex items-center shadow-sm">
                  <span className="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></span>
                  Có sẵn lịch xem
                </div>
                
                <div className="absolute bottom-4 right-4 bg-white px-4 py-2 rounded-xl font-bold text-lg text-slate-900 shadow-md">
                  {prop.price}
                </div>
              </div>

              {/* Info Container */}
              <div className="p-6">
                <h3 className="text-xl font-bold text-slate-800 mb-2 line-clamp-1">{prop.title}</h3>
                <div className="flex items-center text-slate-500 text-sm mb-6">
                  <FaMapMarkerAlt className="mr-2 text-slate-400 shrink-0" />
                  <span className="line-clamp-1">{prop.address}</span>
                </div>

                <div className="flex items-center justify-between text-sm text-slate-600 font-medium mb-8 pb-6 border-b border-slate-100">
                  <div className="flex items-center"><FaBed className="mr-2 text-[#00b4d8] text-lg" /> {prop.beds} PN</div>
                  <div className="flex items-center"><FaBath className="mr-2 text-[#00b4d8] text-lg" /> {prop.baths} WC</div>
                  <div className="flex items-center"><FaRulerCombined className="mr-2 text-[#00b4d8] text-lg" /> {prop.area} m²</div>
                </div>

                <div className="flex space-x-3">
                  <button className="flex-1 bg-white border border-slate-200 text-slate-700 py-3 rounded-xl font-semibold hover:bg-slate-50 transition-colors">
                    Chi tiết
                  </button>
                  <button className="flex-1 bg-[#0b132b] text-white py-3 rounded-xl font-semibold hover:bg-slate-800 transition-colors flex items-center justify-center">
                    <span className="mr-2">📅</span> Đặt lịch
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
