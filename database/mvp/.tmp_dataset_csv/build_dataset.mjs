import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputDir = "C:\\buildAI\\P-046\\database\\mvp\\outputs\\agent_dataset_20260803";
const qaDir = "C:\\buildAI\\P-046\\database\\mvp\\.tmp_dataset_csv\\qa";

function uuid(prefix, n) {
  return `${prefix}-0000-0000-0000-${String(n).padStart(12, "0")}`;
}

function csvCell(value) {
  if (value === null || value === undefined) return "";
  const text = String(value);
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function toCsv(headers, rows) {
  return "\uFEFF" + [headers, ...rows].map(row => row.map(csvCell).join(",")).join("\r\n") + "\r\n";
}

function columnLetter(index) {
  let n = index + 1;
  let result = "";
  while (n > 0) {
    n--;
    result = String.fromCharCode(65 + (n % 26)) + result;
    n = Math.floor(n / 26);
  }
  return result;
}

function addDataSheet(workbook, name, headers, rows, tableName, widths = {}) {
  const sheet = workbook.worksheets.add(name);
  sheet.showGridLines = false;
  sheet.getRangeByIndexes(0, 0, rows.length + 1, headers.length).values = [headers, ...rows];
  const lastColumn = columnLetter(headers.length - 1);
  const fullRange = sheet.getRange(`A1:${lastColumn}${rows.length + 1}`);
  fullRange.format.font = { name: "Aptos", size: 10, color: "#17233B" };
  sheet.getRange(`A1:${lastColumn}1`).format = {
    fill: "#17366D",
    font: { bold: true, color: "#FFFFFF", size: 10 },
    rowHeight: 28,
    wrapText: true,
    verticalAlignment: "center",
  };
  sheet.freezePanes.freezeRows(1);
  fullRange.format.autofitColumns();
  for (const [letter, width] of Object.entries(widths)) {
    sheet.getRange(`${letter}1:${letter}${rows.length + 1}`).format.columnWidth = width;
  }
  return sheet;
}

const saleNames = [
  [1, "Nguyễn Minh Khang", "Căn hộ", "Chi nhánh Thủ Đức"],
  [2, "Trần Ngọc Mai", "Nhà phố", "Chi nhánh Quận 7"],
  [3, "Lê Hoàng Nam", "Đất nền", "Chi nhánh Nhà Bè"],
  [4, "Phạm Thu Trang", "Căn hộ", "Chi nhánh Bình Chánh"],
  [5, "Võ Quốc Bảo", "Biệt thự", "Chi nhánh Quận 7"],
  [6, "Đặng Khánh Linh", "Nhà liền kề", "Chi nhánh Thủ Đức"],
  [7, "Bùi Đức Anh", "Đất nền", "Chi nhánh Bình Chánh"],
  [8, "Đỗ Thảo Vy", "Thương mại", "Chi nhánh Gò Vấp"],
  [9, "Huỳnh Thành Đạt", "Nhà phố", "Chi nhánh Nhà Bè"],
  [10, "Ngô Phương Thảo", "Căn hộ", "Chi nhánh Gò Vấp"],
];

const salesHeaders = [
  "user_id", "employee_code", "full_name", "email", "phone", "branch_name",
  "job_title", "specialties", "max_daily_tours", "is_accepting_tours"
];
const salesRows = saleNames.map(([n, fullName, specialty, branch]) => [
  uuid("11000000", n),
  `DEMO-SALE-${String(n).padStart(2, "0")}`,
  fullName,
  `sale${String(n).padStart(2, "0")}.demo@xhome.local`,
  `84970${String(n).padStart(6, "0")}`,
  branch,
  "Chuyên viên tư vấn bất động sản",
  JSON.stringify([specialty, "Tư vấn trực tiếp", "Đặt lịch xem nhà"]),
  5 + (n % 4),
  true,
]);

const projectData = [
  [1, "DEMO-METRO-EAST", "Metro East Residence", "Đường Nguyễn Xiển", "Long Thạnh Mỹ", "Thủ Đức", 10.8424, 106.8351, 30, 5, 1, "mid_range"],
  [2, "DEMO-SOUTH-GARDEN", "South Garden Residence", "Đường Nguyễn Hữu Thọ", "Tân Phong", "Quận 7", 10.7294, 106.7033, 30, 5, 1, "upper_mid"],
  [3, "DEMO-RIVERSIDE-NB", "Nhà Bè Riverside", "Đường Lê Văn Lương", "Phước Kiển", "Nhà Bè", 10.7040, 106.7020, 45, 10, 1, "mixed"],
  [4, "DEMO-WEST-GATE", "West Gate Town", "Đường Nguyễn Văn Linh", "An Phú Tây", "Bình Chánh", 10.6819, 106.6097, 60, 10, 2, "affordable"],
  [5, "DEMO-NORTH-PARK", "North Park Homes", "Đường Phan Văn Trị", "Phường 5", "Gò Vấp", 10.8275, 106.6886, 30, 5, 1, "urban"],
];
const projectsHeaders = [
  "id", "code", "name", "developer_name", "description", "status", "address_line",
  "ward", "district", "province", "latitude", "longitude", "default_hold_minutes",
  "hold_warning_minutes", "max_hold_extensions", "metadata"
];
const projectsRows = projectData.map(([n, code, name, address, ward, district, lat, lng, hold, warning, extensions, segment]) => [
  uuid("31000000", n), code, name, "XHome Demo",
  "Dự án tổng hợp phục vụ kiểm thử Agent; không phải tin đăng thật.",
  "ACTIVE", address, ward, district, "TP. Hồ Chí Minh", lat, lng,
  hold, warning, extensions, JSON.stringify({ demo_data: true, segment })
]);

const orientations = ["ĐÔNG", "TÂY", "NAM", "BẮC", "ĐÔNG NAM", "TÂY NAM"];
const propertyKinds = ["APARTMENT", "HOUSE", "LAND", "TOWNHOUSE", "VILLA", "COMMERCIAL"];

function projectFor(n) {
  const item = projectData[n - 1];
  return { id: uuid("31000000", n), address: item[3], ward: item[4], district: item[5], lat: item[6], lng: item[7] };
}

function areaFor(kind, i) {
  if (kind === "APARTMENT") return 48 + (i % 7) * 9;
  if (kind === "HOUSE") return 62 + (i % 8) * 14;
  if (kind === "LAND") return 80 + (i % 9) * 20;
  if (kind === "TOWNHOUSE") return 75 + (i % 7) * 15;
  if (kind === "VILLA") return 160 + (i % 8) * 35;
  return 70 + (i % 8) * 18;
}

function priceFor(kind, i) {
  if (kind === "APARTMENT") return 2200000000 + (i % 9) * 450000000;
  if (kind === "HOUSE") return 4800000000 + (i % 10) * 720000000;
  if (kind === "LAND") return 2800000000 + (i % 10) * 650000000;
  if (kind === "TOWNHOUSE") return 6800000000 + (i % 9) * 950000000;
  if (kind === "VILLA") return 13500000000 + (i % 8) * 2800000000;
  return 8500000000 + (i % 9) * 1600000000;
}

function kindCode(kind) {
  return { APARTMENT: "APT", HOUSE: "HOU", LAND: "LAN", TOWNHOUSE: "TOW", VILLA: "VIL", COMMERCIAL: "COM" }[kind];
}

function titleFor(kind, i) {
  const n = String(i).padStart(3, "0");
  if (kind === "APARTMENT") return `Căn hộ demo ${n} - ${1 + (i % 3)} phòng ngủ`;
  if (kind === "HOUSE") return `Nhà phố demo ${n} - khu dân cư hiện hữu`;
  if (kind === "LAND") return `Lô đất demo ${n} - pháp lý riêng`;
  if (kind === "TOWNHOUSE") return `Nhà liền kề demo ${n} - mặt tiền nội khu`;
  if (kind === "VILLA") return `Biệt thự demo ${n} - không gian sân vườn`;
  return `Mặt bằng thương mại demo ${n}`;
}

const propertiesHeaders = [
  "id", "project_id", "code", "property_kind", "title", "description", "status",
  "address_line", "ward", "district", "province", "latitude", "longitude", "area_sqm",
  "usable_area_sqm", "bedrooms", "bathrooms", "floor_number", "orientation", "legal_status",
  "list_price", "currency", "parcel_number", "map_sheet_number", "land_use_purpose",
  "land_use_term", "frontage_m", "road_width_m", "features", "published_at"
];

const propertiesRows = [];
for (let i = 1; i <= 60; i++) {
  const projectNo = ((i - 1) % 5) + 1;
  const project = projectFor(projectNo);
  const kind = propertyKinds[(i - 1) % 6];
  const area = areaFor(kind, i);
  const status = i % 23 === 0 ? "MAINTENANCE" : i % 17 === 0 ? "SOLD" : i % 11 === 0 ? "UNDER_OFFER" : "AVAILABLE";
  const bedrooms = kind === "APARTMENT" ? 1 + (i % 3) : kind === "HOUSE" ? 2 + (i % 4) : kind === "TOWNHOUSE" ? 3 + (i % 3) : kind === "VILLA" ? 4 + (i % 4) : null;
  const bathrooms = kind === "APARTMENT" ? 1 + (i % 2) : kind === "HOUSE" ? 2 + (i % 3) : kind === "TOWNHOUSE" ? 2 + (i % 3) : kind === "VILLA" ? 3 + (i % 3) : null;
  const frontage = ["HOUSE", "LAND", "TOWNHOUSE", "VILLA"].includes(kind) ? 4 + (i % 6) * 0.5 : null;
  const roadWidth = ["HOUSE", "LAND", "TOWNHOUSE", "VILLA", "COMMERCIAL"].includes(kind) ? 6 + (i % 5) * 2 : null;
  const code = `DEMO-${kindCode(kind)}-${String(i).padStart(3, "0")}`;
  const features = {
    demo_data: true,
    near_school: i % 2 === 0,
    near_hospital: i % 3 === 0,
    near_market: i % 4 !== 0,
    parking: kind !== "LAND",
    balcony: kind === "APARTMENT",
    elevator: ["APARTMENT", "COMMERCIAL"].includes(kind),
    river_view: [2, 3].includes(projectNo) && i % 2 === 0,
    pool: ["APARTMENT", "VILLA"].includes(kind) && i % 3 === 0,
    gym: kind === "APARTMENT" && i % 2 === 1,
    distance_to_center_km: 5 + (i % 16),
  };
  const published = new Date(Date.UTC(2026, 7, 3 - (i % 45))).toISOString().slice(0, 10);
  propertiesRows.push([
    uuid("41000000", i), project.id, code, kind, titleFor(kind, i),
    `Dữ liệu tổng hợp để kiểm thử AI Agent. Loại ${kind}, diện tích ${area} m², thuộc khu vực ${project.district}.`,
    status, `${project.address}, căn/lô ${String(i).padStart(3, "0")}`, project.ward,
    project.district, "TP. Hồ Chí Minh", +(project.lat + (i % 7) * 0.00025).toFixed(6),
    +(project.lng + (i % 5) * 0.0003).toFixed(6), area,
    kind === "LAND" ? null : +(area * 0.88).toFixed(2), bedrooms, bathrooms,
    ["APARTMENT", "COMMERCIAL"].includes(kind) ? 2 + (i % 22) : null,
    orientations[i % 6], kind === "LAND" ? "Sổ đỏ riêng - dữ liệu demo" : "Sổ hồng/Hợp đồng mua bán - dữ liệu demo",
    priceFor(kind, i), "VND", kind === "LAND" ? `DEMO-PARCEL-${String(i).padStart(3, "0")}` : null,
    kind === "LAND" ? `DEMO-MAP-${String(projectNo).padStart(2, "0")}` : null,
    kind === "LAND" ? "Đất ở tại đô thị" : null, kind === "LAND" ? "Lâu dài" : null,
    frontage, roadWidth, JSON.stringify(features), published,
  ]);
}

const assignmentHeaders = ["property_id", "sale_user_id", "is_primary", "assigned_at"];
const assignmentRows = propertiesRows.map((row, idx) => [
  row[0], uuid("11000000", (idx % 10) + 1), true, "2026-08-03 08:00:00"
]);

const busyHeaders = ["id", "sale_user_id", "unavailable_start", "unavailable_end", "reason", "source"];
const busyRows = [];
for (let saleNo = 1; saleNo <= 10; saleNo++) {
  busyRows.push([
    uuid("13000000", (saleNo - 1) * 2 + 1), uuid("11000000", saleNo),
    "2026-08-04 09:00:00", "2026-08-04 10:30:00",
    "Họp nội bộ - dữ liệu demo", "SYSTEM"
  ]);
  busyRows.push([
    uuid("13000000", (saleNo - 1) * 2 + 2), uuid("11000000", saleNo),
    "2026-08-05 14:00:00", "2026-08-05 16:00:00",
    "Đang dẫn khách - dữ liệu demo", "SYSTEM"
  ]);
}

await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(qaDir, { recursive: true });

const csvFiles = [
  ["properties.csv", propertiesHeaders, propertiesRows],
  ["sales.csv", salesHeaders, salesRows],
  ["projects.csv", projectsHeaders, projectsRows],
  ["property_sale_assignments.csv", assignmentHeaders, assignmentRows],
  ["sale_unavailability.csv", busyHeaders, busyRows],
];
for (const [fileName, headers, rows] of csvFiles) {
  await fs.writeFile(`${outputDir}\\${fileName}`, toCsv(headers, rows), "utf8");
}

const workbook = Workbook.create();
const readme = workbook.worksheets.add("README");
readme.showGridLines = false;
readme.getRange("A1:E1").merge();
readme.getRange("A1").values = [["XHOME — DATASET KIỂM THỬ AI AGENT"]];
readme.getRange("A1:E1").format = {
  fill: "#17366D", font: { bold: true, color: "#FFFFFF", size: 18 },
  horizontalAlignment: "center", verticalAlignment: "center", rowHeight: 42
};
readme.getRange("A3:E3").merge();
readme.getRange("A3").values = [["Dữ liệu tổng hợp phục vụ demo; không phải tin đăng hoặc báo giá thị trường chính thức."]];
readme.getRange("A3:E3").format = { fill: "#FFF3D6", font: { bold: true, color: "#8A5A00" }, wrapText: true, rowHeight: 32 };
readme.getRange("A5:B10").values = [
  ["Chỉ tiêu", "Số lượng"],
  ["Bất động sản", null],
  ["Sale", null],
  ["Dự án", null],
  ["Phân công sale", null],
  ["Khoảng lịch bận", null],
];
readme.getRange("A5:B5").format = { fill: "#2A73C5", font: { bold: true, color: "#FFFFFF" } };
readme.getRange("A5:B10").format.borders = { preset: "insideHorizontal", style: "thin", color: "#D9E2F0" };
readme.getRange("B6:B10").format.numberFormat = "#,##0";
readme.getRange("A12:E17").values = [
  ["File/Sheet", "Mục đích", "Dùng cho", "Có import thẳng DB?", "Ghi chú"],
  ["Properties", "60 căn/đất có giá và tiêu chí", "Agent tìm kiếm, lọc, so sánh", "Có, cần map đúng cột", "Cột features là JSON"],
  ["Sales", "10 hồ sơ sale tổng hợp", "Chọn sale và hiển thị thông tin", "Không trực tiếp", "SQL sẽ tách users và sale_profiles"],
  ["Projects", "5 dự án demo", "Lọc theo dự án/khu vực", "Có, cần map đúng cột", "Tất cả là dữ liệu tổng hợp"],
  ["Assignments", "Giao mỗi căn cho một sale", "Agent tìm sale phụ trách", "Có", "Khóa chính kép"],
  ["SaleBusyTimes", "20 khoảng thời gian bận", "Kiểm tra lịch sale", "Cần đổi 2 cột thời gian thành tstzrange", "Dùng SQL nếu muốn import nhanh"],
];
readme.getRange("A12:E12").format = { fill: "#309451", font: { bold: true, color: "#FFFFFF" }, wrapText: true };
readme.getRange("A12:E17").format.wrapText = true;
readme.getRange("A1:E17").format.font = { name: "Aptos", size: 11, color: "#17233B" };
readme.getRange("A1:E1").format.font = { name: "Aptos Display", size: 18, bold: true, color: "#FFFFFF" };
readme.getRange("A1:A17").format.columnWidth = 22;
readme.getRange("B1:B17").format.columnWidth = 34;
readme.getRange("C1:C17").format.columnWidth = 34;
readme.getRange("D1:D17").format.columnWidth = 20;
readme.getRange("E1:E17").format.columnWidth = 34;

const propertySheet = addDataSheet(workbook, "Properties", propertiesHeaders, propertiesRows, "PropertiesTable", { A: 38, B: 38, C: 20, D: 16, E: 38, F: 48, G: 16, H: 38, I: 18, J: 18, K: 22, T: 38, U: 24, V: 10, AC: 55, AD: 14 });
propertySheet.getRange("L2:M61").format.numberFormat = "0.000000";
propertySheet.getRange("N2:O61").format.numberFormat = "#,##0.00";
propertySheet.getRange("U2:U61").format.numberFormat = "#,##0";
propertySheet.getRange("AD2:AD61").format.numberFormat = "yyyy-mm-dd";
propertySheet.getRange("G2:G61").conditionalFormats.add("containsText", { text: "AVAILABLE", format: { fill: "#E6F5EA", font: { color: "#237A3B" } } });
propertySheet.getRange("G2:G61").conditionalFormats.add("containsText", { text: "SOLD", format: { fill: "#FDE8E8", font: { color: "#B42318" } } });
propertySheet.getRange("G2:G61").conditionalFormats.add("containsText", { text: "UNDER_OFFER", format: { fill: "#FFF3D6", font: { color: "#8A5A00" } } });

const salesSheet = addDataSheet(workbook, "Sales", salesHeaders, salesRows, "SalesTable", { A: 38, B: 18, C: 24, D: 32, E: 18, F: 24, G: 34, H: 50 });
salesSheet.getRange("E2:E11").format.numberFormat = "@";
addDataSheet(workbook, "Projects", projectsHeaders, projectsRows, "ProjectsTable", { A: 38, B: 24, C: 28, D: 20, E: 50, G: 34, H: 20, I: 18, J: 22, P: 40 });
const assignmentSheet = addDataSheet(workbook, "Assignments", assignmentHeaders, assignmentRows, "AssignmentsTable", { A: 38, B: 38, C: 14, D: 26 });
assignmentSheet.getRange("D2:D61").format.numberFormat = "yyyy-mm-dd hh:mm";
const busySheet = addDataSheet(workbook, "SaleBusyTimes", busyHeaders, busyRows, "BusyTimesTable", { A: 38, B: 38, C: 28, D: 28, E: 38, F: 14 });
busySheet.getRange("C2:D21").format.numberFormat = "yyyy-mm-dd hh:mm";

// Create every referenced sheet before adding cross-sheet formulas.
readme.getRange("B6").formulas = [["=COUNTA('Properties'!A2:A61)"]];
readme.getRange("B7").formulas = [["=COUNTA('Sales'!A2:A11)"]];
readme.getRange("B8").formulas = [["=COUNTA('Projects'!A2:A6)"]];
readme.getRange("B9").formulas = [["=COUNTA('Assignments'!A2:A61)"]];
readme.getRange("B10").formulas = [["=COUNTA('SaleBusyTimes'!A2:A21)"]];

const inspect = await workbook.inspect({ kind: "workbook,sheet,table", maxChars: 8000, tableMaxRows: 6, tableMaxCols: 8 });
await fs.writeFile(`${qaDir}\\inspect.ndjson`, inspect.ndjson, "utf8");
const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "final formula error scan",
});
await fs.writeFile(`${qaDir}\\formula-errors.ndjson`, errors.ndjson, "utf8");

const renderRanges = {
  README: "A1:E17",
  Properties: "A1:W12",
  Sales: "A1:J11",
  Projects: "A1:P6",
  Assignments: "A1:D20",
  SaleBusyTimes: "A1:F21",
};
for (const [sheetName, range] of Object.entries(renderRanges)) {
  const preview = await workbook.render({ sheetName, range, scale: 0.8, format: "png" });
  await fs.writeFile(`${qaDir}\\${sheetName}.png`, new Uint8Array(await preview.arrayBuffer()));
}

const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(`${outputDir}\\XHome_Agent_Test_Dataset.xlsx`);
