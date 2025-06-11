import pandas as pd
import re

# === BƯỚC 1: Đọc file CSV gốc bị lỗi OCR ===
input_path = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output/du_lieu_sach.csv"  # Đường dẫn tới file CSV gốc
with open(input_path, "r", encoding="utf-8") as f:
    raw_lines = f.readlines()

cleaned_rows = []

# === BƯỚC 2: Làm sạch từng dòng ===
for line in raw_lines:
    if not line.strip():
        continue  # bỏ dòng trắng

    # Tách dòng theo dấu phẩy
    parts = line.strip().split(",")

    # Tìm vị trí bắt đầu phần số liệu (giả định số bắt đầu có chứa toàn chữ số hoặc số có dấu phẩy)
    split_index = None
    for i, token in enumerate(parts):
        cleaned_token = token.strip().replace(".", "").replace(",", "").replace("-", "")
        if cleaned_token.isdigit():
            split_index = i
            break

    if split_index is None:
        # Nếu không tìm thấy số, giả định cả dòng là text
        text_part = ' '.join([p.strip() for p in parts if p.strip()])
        cleaned_rows.append([text_part])
    else:
        # Ghép phần text từ các token trước đó
        text_tokens = parts[:split_index]
        text = ' '.join([t.strip() for t in text_tokens if t.strip()])

        # Giữ nguyên phần số liệu sau đó
        number_tokens = parts[split_index:]
        full_row = [text] + number_tokens
        cleaned_rows.append(full_row)

# === BƯỚC 3: Tạo bảng và xuất kết quả ===
# Tìm số cột lớn nhất để đặt tên cột tương ứng
max_cols = max(len(row) for row in cleaned_rows)
columns = ["Chỉ tiêu"] + [f"Số liệu {i}" for i in range(1, max_cols)]

df_cleaned = pd.DataFrame(cleaned_rows, columns=columns[:max_cols])

# === BƯỚC 4: Ghi ra file CSV đã làm sạch ===
output_path = "du_lieu_hoan_chinh_cleaned.csv"
df_cleaned.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ File đã được làm sạch và lưu tại: {output_path}")
