from PIL import Image
import pytesseract
import pandas as pd
import os
from datetime import datetime

# ============================
# CẤU HÌNH ĐƯỜNG DẪN
# ============================
image_path = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output_images/VIC/page_6.png"  # Thay bằng đường dẫn ảnh của bạn
output_dir = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output"
os.makedirs(output_dir, exist_ok=True)

# ============================
# THÔNG SỐ CƠ BẢN
# ============================
OCR_LANG = "vie"  # "eng" nếu chưa cài tiếng Việt
COLUMN_GAP_THRESHOLD = 70  # Ngưỡng xác định khoảng cách phân tách cột

# ============================
# HÀM OCR TỪ ẢNH → BẢNG
# ============================
def extract_table_from_image(image_path, column_gap_threshold=70):
    image = Image.open(image_path)
    df = pytesseract.image_to_data(image, lang=OCR_LANG, config="--psm 4", output_type=pytesseract.Output.DATAFRAME)
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
                row_cells.append(current_cell.strip().replace(",", ""))  # ❌ Xóa dấu phẩy trong từng ô
                current_cell = text
            else:
                current_cell += ' ' + text
            current_left = left

        row_cells.append(current_cell.strip().replace(",", ""))  # ❌ Xóa dấu phẩy cuối dòng
        rows.append(row_cells)

    return pd.DataFrame(rows)

# ============================
# CHẠY OCR VÀ GHI FILE CSV
# ============================
df = extract_table_from_image(image_path, COLUMN_GAP_THRESHOLD)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_output_path = os.path.join(output_dir, f"ocr_table_cleaned_{timestamp}.csv")
df.to_csv(csv_output_path, index=False, encoding="utf-8-sig")  # utf-8-sig để Excel đọc tiếng Việt chuẩn

print(f"✅ Đã xuất bảng vào file CSV: {csv_output_path}")
