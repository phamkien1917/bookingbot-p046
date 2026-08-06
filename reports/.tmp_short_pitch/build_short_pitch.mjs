import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const OUT = "C:\\buildAI\\P-046\\reports\\Thuyet_trinh_ngan_AI_tim_nha_dat_lich_XHome.pptx";
const QA = "C:\\buildAI\\P-046\\reports\\.tmp_short_pitch\\qa";
const IMG1 = "C:\\Users\\Admin\\AppData\\Local\\Temp\\codex-clipboard-b6774342-7299-4d27-9bfe-b63761aac880.png";
const IMG2 = "C:\\Users\\Admin\\AppData\\Local\\Temp\\codex-clipboard-d9c09d47-520f-4c91-86e5-cd502dff77df.png";
const IMG3 = "C:\\Users\\Admin\\AppData\\Local\\Temp\\codex-clipboard-41e052f0-5ba5-4d71-bb15-17d61f4d9f97.png";

const C = {
  navy: "#102A5E", blue: "#2878D0", green: "#309451", orange: "#F39A19",
  purple: "#7952B3", red: "#D74343", ink: "#17233B", muted: "#64748B",
  pale: "#F7F9FC", line: "#D9E2F0", white: "#FFFFFF", paleBlue: "#EAF3FF",
  paleGreen: "#EAF7EF", paleOrange: "#FFF4E4", palePurple: "#F2EDFB"
};

async function writeBlob(path, blob) {
  await fs.writeFile(path, new Uint8Array(await blob.arrayBuffer()));
}
async function readImageBlob(path) {
  const bytes = await fs.readFile(path);
  return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
}
function rect(slide, x, y, w, h, fill = C.white, line = C.line, radius = "rounded-xl") {
  return slide.shapes.add({ geometry: "roundRect", position: { left:x, top:y, width:w, height:h },
    fill, line:{style:"solid", fill:line, width:1}, borderRadius:radius });
}
function textBox(slide, text, x, y, w, h, size=20, color=C.ink, bold=false, align="left") {
  const s = slide.shapes.add({ geometry:"textbox", position:{left:x,top:y,width:w,height:h},
    fill:"none", line:{style:"solid",fill:"none",width:0} });
  s.text = text;
  s.text.style = { fontFamily:"Aptos", fontSize:size, color, bold, alignment:align, verticalAlignment:"middle" };
  return s;
}
function title(slide, t, kicker) {
  if (kicker) textBox(slide, kicker.toUpperCase(), 64, 31, 340, 24, 14, C.blue, true);
  textBox(slide, t, 64, 54, 1152, 55, 38, C.navy, true);
  slide.shapes.add({geometry:"rect",position:{left:64,top:116,width:1152,height:3},fill:C.line,line:{style:"solid",fill:C.line,width:0}});
}
function footer(slide, n) {
  textBox(slide, `XHOME  •  MENTOR DUTY #2`, 64, 681, 330, 20, 12, C.muted, true);
  textBox(slide, String(n).padStart(2,"0"), 1162, 681, 54, 20, 12, C.muted, true, "right");
}
function addNotes(slide, body, sources=[]) {
  let note = body;
  if (sources.length) note += `\n\n[Sources]\n${sources.map(s=>`- User-provided image: ${s}`).join("\n")}`;
  slide.speakerNotes.textFrame.setText(note);
}
async function addFramedImage(slide, path, alt, x, y, w, h) {
  rect(slide, x-7, y-7, w+14, h+14, C.white, C.line, "rounded-xl");
  slide.images.add({ blob:await readImageBlob(path), contentType:"image/png", alt, fit:"contain",
    position:{left:x,top:y,width:w,height:h}, geometry:"rect" });
}

async function main() {
  await fs.mkdir(QA,{recursive:true});
  await fs.mkdir("C:\\buildAI\\P-046\\reports",{recursive:true});
  const p = Presentation.create({slideSize:{width:1280,height:720}});

  // Slide 1 — minimal opening.
  {
    const s=p.slides.add(); s.background.fill=C.pale;
    s.shapes.add({geometry:"rect",position:{left:0,top:0,width:18,height:720},fill:C.blue,line:{style:"solid",fill:C.blue,width:0}});
    textBox(s,"AI TRỢ LÝ TÌM NHÀ",70,78,520,30,16,C.blue,true);
    textBox(s,"Nói nhu cầu một lần.\nTừ gợi ý đến lịch xem nhà.",70,128,720,142,54,C.navy,true);
    textBox(s,"AI giúp người mua/thuê tìm phương án phù hợp, rồi chuyển hồ sơ rõ ràng cho sale xử lý tiếp.",72,292,650,72,23,C.muted,false);
    // One flat visual chain.
    const y=445;
    textBox(s,"NGƯỜI TÌM NHÀ",82,y,250,32,18,C.blue,true,"center");
    textBox(s,"→",333,y-2,70,34,32,C.muted,true,"center");
    textBox(s,"AI LÀM RÕ NHU CẦU",405,y,300,32,18,C.purple,true,"center");
    textBox(s,"→",706,y-2,70,34,32,C.muted,true,"center");
    textBox(s,"SALE CHỐT LỊCH",778,y,250,32,18,C.green,true,"center");
    s.shapes.add({geometry:"rect",position:{left:82,top:y+45,width:946,height:5},fill:C.line,line:{style:"solid",fill:C.line,width:0}});
    textBox(s,"BÁO CÁO TIẾN ĐỘ NGẮN  •  MVP ĐANG HOÀN THIỆN DATASET",72,612,750,28,15,C.muted,true);
    footer(s,1);
    addNotes(s,"Bài toán của nhóm em khá đơn giản: người tìm nhà thường nói nhu cầu theo cách rất đời thường, còn sale lại cần thông tin rõ để tư vấn và xếp lịch. Sản phẩm của nhóm em dùng AI làm phần ở giữa: hiểu nhu cầu, hỏi thêm khi thiếu, gợi ý căn phù hợp và hỗ trợ đặt lịch xem nhà.");
  }

  // Slide 2 — audiences.
  {
    const s=p.slides.add(); s.background.fill=C.white; title(s,"AI đứng giữa người tìm nhà và sale","Giá trị chính");
    textBox(s,"AI không thay sale; AI giảm việc lọc tin và hỏi lại từ đầu.",64,139,950,38,22,C.muted,false);
    s.shapes.add({geometry:"rect",position:{left:639,top:202,width:2,height:363},fill:C.line,line:{style:"solid",fill:C.line,width:0}});
    textBox(s,"CHO NGƯỜI MUA / THUÊ",78,205,500,34,24,C.blue,true);
    textBox(s,"Nói nhu cầu như đang nhắn tin",78,266,500,32,27,C.ink,true);
    textBox(s,"“Em cần căn 2 phòng ngủ, gần trường,\nngân sách khoảng 3 tỷ.”",78,309,475,70,22,C.muted,false);
    textBox(s,"✓ AI hỏi thêm phần còn thiếu\n✓ Lọc và so sánh vài lựa chọn phù hợp\n✓ Đặt lịch xem nhà ngay trên web",78,410,480,126,20,C.ink,false);
    textBox(s,"CHO SALE / ĐIỀU PHỐI",686,205,500,34,24,C.green,true);
    textBox(s,"Nhận một lead đã rõ nhu cầu",686,266,500,32,27,C.ink,true);
    textBox(s,"Ngân sách • tiêu chí bắt buộc • ưu tiên\n• căn quan tâm • giờ muốn liên hệ",686,309,480,70,22,C.muted,false);
    textBox(s,"✓ Đỡ mất thời gian hỏi lại\n✓ Kiểm tra lịch và xác nhận trước khi chốt\n✓ Theo dõi trạng thái lịch hẹn",686,410,480,126,20,C.ink,false);
    rect(s,360,585,560,54,C.paleBlue,C.blue,"rounded-xl");
    textBox(s,"Kết quả: khách đỡ rối — sale xử lý nhanh hơn",378,593,524,38,21,C.navy,true,"center");
    footer(s,2);
    addNotes(s,"AI có hai nhóm người dùng chính. Với người mua hoặc thuê, họ chỉ cần nói nhu cầu như đang nhắn tin; hệ thống sẽ hỏi thêm và lọc căn. Với sale, AI chuyển sang một hồ sơ đã có ngân sách, tiêu chí và căn quan tâm. Vì vậy sale không phải hỏi lại mọi thứ từ đầu, nhưng sale vẫn là người xác nhận cuối cùng.");
  }

  // Slide 3 — overall flow image.
  {
    const s=p.slides.add(); s.background.fill=C.pale; title(s,"Một cuộc trò chuyện đi đến một lịch hẹn","Luồng tổng thể");
    await addFramedImage(s,IMG1,"Sơ đồ luồng hoạt động tổng thể của dự án",64,137,1152,472);
    rect(s,122,624,1036,42,C.navy,C.navy,"rounded-xl");
    textBox(s,"NÓI NHU CẦU   →   AI HỎI THÊM   →   LỌC & SO SÁNH   →   SALE DUYỆT   →   LƯU LỊCH",142,630,996,30,17,C.white,true,"center");
    footer(s,3);
    addNotes(s,"Luồng hoạt động có thể hiểu rất đời thường. Khách vào web, nói muốn mua hay thuê và mô tả nhu cầu. AI xem thông tin đã đủ chưa; thiếu thì hỏi thêm, có mâu thuẫn thì hỏi khách ưu tiên cái gì. Khi đủ dữ liệu, hệ thống lọc và so sánh các căn. Khách chọn phương án thì hồ sơ được chuyển cho sale; sau đó hệ thống kiểm tra lịch, đề xuất giờ và chỉ lưu lịch khi sale xác nhận.",[IMG1]);
  }

  // Slide 4 — core problems with image.
  {
    const s=p.slides.add(); s.background.fill=C.white; title(s,"Ba điểm nghẽn chính đều có bước kiểm soát","Cách giải quyết");
    const rows=[
      ["1","Khách nói nhu cầu còn mơ hồ","AI hỏi lại cho đủ rồi mới gợi ý",C.blue,C.paleBlue],
      ["2","Sale phải hỏi lại từ đầu","Chuyển hồ sơ nhu cầu tường minh",C.green,C.paleGreen],
      ["3","Lịch sale dễ bị trùng","Kiểm tra lịch và chờ sale xác nhận",C.orange,C.paleOrange]
    ];
    rows.forEach((r,i)=>{
      const y=158+i*135;
      textBox(s,r[0],64,y,46,46,30,r[3],true,"center");
      textBox(s,r[1],122,y-2,400,32,22,C.ink,true);
      textBox(s,"→  "+r[2],122,y+38,420,54,19,C.muted,false);
      s.shapes.add({geometry:"rect",position:{left:122,top:y+102,width:410,height:2},fill:C.line,line:{style:"solid",fill:C.line,width:0}});
    });
    await addFramedImage(s,IMG2,"Sơ đồ chuyển giao cho sale và đặt lịch xem nhà",578,149,638,462);
    rect(s,64,590,468,66,C.paleGreen,C.green,"rounded-xl");
    textBox(s,"Nguyên tắc HITL: sale xác nhận trước khi chốt lịch",83,602,430,42,19,C.green,true,"center");
    footer(s,4);
    addNotes(s,"Nhóm em tập trung xử lý ba vấn đề chính. Một là nhu cầu mơ hồ: AI không đoán mà hỏi lại. Hai là sale nhận lead thiếu thông tin: hệ thống tạo hồ sơ rõ ràng để sale xử lý tiếp. Ba là trùng lịch: hệ thống kiểm tra lịch trống và vẫn yêu cầu sale xác nhận trước khi chốt. Nếu giờ khách chọn không phù hợp thì hệ thống đề xuất giờ khác.",[IMG2]);
  }

  // Slide 5 — dataset issue and immediate MVP plan.
  {
    const s=p.slides.add(); s.background.fill=C.pale; title(s,"Vướng hiện tại là dataset — không phải luồng sản phẩm","Tiến độ MVP");
    textBox(s,"AI chỉ tư vấn tốt khi dữ liệu căn và lịch sale đủ rõ, đồng nhất và còn hiệu lực.",64,137,1130,36,21,C.muted,false);
    textBox(s,"VIỆC NHÓM ĐANG LÀM",64,202,450,30,21,C.orange,true);
    const steps=[
      ["01","Chốt trường bắt buộc","giá, vị trí, loại căn, trạng thái"],
      ["02","Tạo dataset mẫu đủ demo","có cả trường hợp thiếu dữ liệu"],
      ["03","Gắn lịch sale & trạng thái căn","để kiểm tra trước khi đặt"],
      ["04","Test luồng hỏi lại","AI thiếu gì thì hỏi đúng cái đó"]
    ];
    steps.forEach((r,i)=>{
      const y=248+i*74;
      textBox(s,r[0],64,y,45,40,18,C.orange,true,"center");
      textBox(s,r[1],122,y-3,390,27,20,C.ink,true);
      textBox(s,r[2],122,y+25,390,26,16,C.muted,false);
    });
    await addFramedImage(s,IMG3,"Sơ đồ luồng dữ liệu và nguyên tắc AI không bịa thông tin",558,195,658,355);
    rect(s,558,571,658,76,C.navy,C.navy,"rounded-xl");
    textBox(s,"MỤC TIÊU GẦN NHẤT",582,579,205,22,14,"#A9C7F5",true);
    textBox(s,"Chạy trọn luồng: nhu cầu → gợi ý → sale duyệt → lịch hẹn",582,601,610,34,20,C.white,true);
    rect(s,64,574,448,73,C.paleOrange,C.orange,"rounded-xl");
    textBox(s,"Thiếu dữ liệu thì hỏi thêm — tuyệt đối không tự bịa.",82,588,412,44,19,C.orange,true,"center");
    footer(s,5);
    addNotes(s,"Hiện tại điểm nhóm em đang vướng là dataset. Dữ liệu căn còn cần chuẩn hóa và phải gắn được với trạng thái thực tế, còn lịch sale cũng phải đủ để kiểm tra. Cách xử lý là chốt các trường bắt buộc, tạo một bộ dữ liệu mẫu đủ cho demo, thêm cả tình huống thiếu dữ liệu để test việc AI hỏi lại. Nguyên tắc của nhóm là thiếu thì hỏi, không có dữ liệu thì không kết luận. Mốc gần nhất là chạy trọn một luồng từ nhu cầu đến lịch hẹn.",[IMG3]);
  }

  for (const [i,s] of p.slides.items.entries()) {
    const stem=`slide-${String(i+1).padStart(2,"0")}`;
    await writeBlob(`${QA}\\${stem}.png`,await p.export({slide:s,format:"png",scale:1.5}));
    const layout=await s.export({format:"layout"});
    await fs.writeFile(`${QA}\\${stem}.layout.json`,await layout.text());
  }
  await writeBlob(`${QA}\\montage.webp`,await p.export({format:"webp",montage:true,scale:1}));
  const inspect=await p.inspect({kind:"slide,textbox,shape,image,notes",maxChars:20000});
  await fs.writeFile(`${QA}\\inspect.ndjson`,inspect.ndjson);
  const pptx=await PresentationFile.exportPptx(p);
  await pptx.save(OUT);
}

main().catch(e=>{console.error(e);process.exitCode=1;});
