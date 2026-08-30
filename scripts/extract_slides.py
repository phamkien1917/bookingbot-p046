import os
import re
import zipfile

pptx_path = r"C:\Users\LucVuu\Desktop\Nera_Conversational_Real_Estate.pptx"
out_dir = r"C:\Users\LucVuu\.gemini\antigravity-ide\brain\ecf2242c-c692-4f58-b945-920ce83d4b09\scratch\slides"
os.makedirs(out_dir, exist_ok=True)

with zipfile.ZipFile(pptx_path, "r") as z:
    for i in range(1, 9):
        rel_path = f"ppt/slides/_rels/slide{i}.xml.rels"
        if rel_path in z.namelist():
            rel_xml = z.read(rel_path).decode("utf-8")
            m = re.search(r'Target="\.\./media/(image\d+\.png)"', rel_xml)
            if m:
                img_name = m.group(1)
                img_data = z.read(f"ppt/media/{img_name}")
                out_path = os.path.join(out_dir, f"slide_{i}.png")
                with open(out_path, "wb") as f:
                    f.write(img_data)
                print(f"Slide {i} -> {out_path} ({len(img_data)} bytes)")
print("Extraction complete!")
