from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os
from datetime import datetime
import glob

# ============================
# CẤU HÌNH
# ============================
# Đường dẫn file PDF
pdf_path = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/VNM_BCTC_Q1_2025.pdf"

# Thư mục chứa ảnh đầu ra
image_output_dir = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output_images"
os.makedirs(image_output_dir, exist_ok=True)

# Thư mục chứa file CSV đầu ra
result_dir = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output"
os.makedirs(result_dir, exist_ok=True)

# Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ============================
# CHUYỂN PDF → ẢNH
# ============================
images = convert_from_path(pdf_path, dpi=300)
image_paths = []

for i, img in enumerate(images):
    img_path = os.path.join(image_output_dir, f"page_{i+1}.png")
    img.save(img_path, "PNG")
    image_paths.append(img_path)
    print(f"✅ Đã lưu ảnh trang {i+1} -> {img_path}")

# ============================
# OCR TỪNG ẢNH → BẢNG
# ============================
def extract_table_from_image(image_path, column_gap_threshold=50):
    df = pytesseract.image_to_data(Image.open(image_path), lang="vie", config="--psm 6", output_type=pytesseract.Output.DATAFRAME)
    df = df[df.text.notnull()]
    df = df[df.text.str.strip() != ""]

    grouped = df.groupby(['page_num', 'block_num', 'par_num', 'line_num'])
    rows = []

    for _, line in grouped:
        words = line.sort_values('left')[['left', 'text']].values.tolist()

        if not words:
            continue

        current_cell = words[0][1]
        current_left = words[0][0]
        row_cells = []

        for i in range(1, len(words)):
            left, text = words[i]
            if left - current_left > column_gap_threshold:
                row_cells.append(current_cell.strip())
                current_cell = text
            else:
                current_cell += ' ' + text
            current_left = left

        row_cells.append(current_cell.strip())
        rows.append(','.join(row_cells))
    
    return rows

# ============================
# GHÉP TOÀN BỘ CSV
# ============================
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_output_path = os.path.join(result_dir, f"parsed_table_{timestamp}.csv")

with open(csv_output_path, 'w', encoding='utf-8', newline='') as f:
    for image_path in image_paths:
        rows = extract_table_from_image(image_path)
        for row in rows:
            f.write(row + '\n')

print(f"🎉 Đã xuất bảng phân cột thành công -> {csv_output_path}")
