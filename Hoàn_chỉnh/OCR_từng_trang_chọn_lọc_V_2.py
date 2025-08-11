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
pdf_path = "D:/x1g8/Nghiencuutotnghiep1/downloads/FPT/Báo_cáo_tài_chính_Công_ty_mẹ_quý_1_năm_2025.pdf"

# Thư mục chứa ảnh đầu ra
image_output_dir = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output_images/FPT"
os.makedirs(image_output_dir, exist_ok=True)

# Thư mục chứa file CSV đầu ra
result_dir = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output"
os.makedirs(result_dir, exist_ok=True)

# Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# CHỌN TRANG CẦN XỬ LÝ
pages_to_process = [5,6,7,8,9,10] # Để rỗng để xử lý tất cả các trang

# ============================
# CHUYỂN PDF → ẢNH
# ============================
print("⏳ Bắt đầu chuyển đổi PDF sang ảnh...")
images = convert_from_path(pdf_path, dpi=300)
image_paths = []

for i, img in enumerate(images):
    page_number = i + 1
    if pages_to_process and page_number not in pages_to_process:
        print(f"⏩ Bỏ qua trang {page_number} (không có trong danh sách xử lý).")
        continue

    img_path = os.path.join(image_output_dir, f"page_{page_number}.png")
    img.save(img_path, "PNG")
    image_paths.append(img_path)
    print(f"✅ Đã lưu ảnh trang {page_number} -> {img_path}")

# ============================
# OCR TỪNG ẢNH → BẢNG
# ============================
def extract_table_from_image(image_path, column_gap_threshold=50):
    """Trích xuất dữ liệu dạng bảng từ một file ảnh."""
    print(f"🤖 Đang OCR ảnh: {os.path.basename(image_path)}...")
    df = pytesseract.image_to_data(Image.open(image_path), lang="vie",
                                   config="--psm 6", output_type=pytesseract.Output.DATAFRAME)
    df = df[df.text.notnull()]
    df = df[df.text.str.strip() != ""]
    grouped = df.groupby(['page_num', 'block_num', 'par_num', 'line_num'])
    rows = []
    for _, line in grouped:
        words = line.sort_values('left')[['left', 'text']].values.tolist()
        if not words: continue
        current_cell = words[0][1]
        current_left = words[0][0]
        row_cells = []
        for j in range(1, len(words)):
            left, text = words[j]
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
# ✨ THAY ĐỔI MỚI: HÀM LỌC DÒNG CSV ✨
# ============================
def is_valid_row(row_string):
    """
    Kiểm tra xem một dòng có hợp lệ không dựa trên mã số ở ô đầu tiên.
    - Hợp lệ nếu mã số là số nguyên từ 1 đến 10.
    - Hợp lệ nếu mã số là số nguyên lớn hơn 10 VÀ chia hết cho 10 (20, 30, 40...).
    - Không hợp lệ trong các trường hợp khác.
    """
    try:
        # Tách chuỗi thành các cột dựa trên dấu phẩy
        first_cell = row_string.split(',')[0].strip()
        # Thử chuyển ô đầu tiên sang dạng số nguyên
        ma_so = int(first_cell)

        # Áp dụng điều kiện lọc
        if (1 <= ma_so <= 10) or (ma_so > 10 and ma_so % 10 == 0):
            return True
        else:
            return False
    except (ValueError, IndexError):
        # Nếu ô đầu tiên không phải là số (ví dụ: "Chỉ tiêu", "TÀI SẢN")
        # hoặc dòng bị rỗng, coi như không hợp lệ.
        return False

# ============================
# GHÉP TOÀN BỘ CSV
# ============================
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
csv_output_path = os.path.join(result_dir, f"{pdf_filename}_filtered_{timestamp}.csv")

with open(csv_output_path, 'w', encoding='utf-8', newline='') as f:
    for image_path in image_paths:
        rows = extract_table_from_image(image_path)
        for row in rows:
            # ✨ THAY ĐỔI MỚI: Chỉ ghi những dòng thỏa mãn điều kiện ✨
            if is_valid_row(row):
                f.write(row + '\n')

if not image_paths:
    print("⚠️ Không có trang nào được xử lý. Vui lòng kiểm tra lại danh sách `pages_to_process`.")
else:
    print(f"🎉 Đã xuất bảng đã lọc thành công -> {csv_output_path}")