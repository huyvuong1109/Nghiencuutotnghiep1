import pandas as pd
import os

# ======================
# BƯỚC 1: Đọc dữ liệu thô từng dòng (bỏ qua lỗi cột không đều)
# ======================
file_path = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output/du_lieu_sach.csv"  # Thay bằng đường dẫn file thực tế

with open(file_path, "r", encoding="utf-8") as f:
    raw_lines = f.readlines()

# ======================
# BƯỚC 2: Làm sạch từng dòng văn bản
# ======================
cleaned_rows = []

for line in raw_lines:
    # Tách các từ bằng dấu phẩy (vì lỗi OCR tạo ra nhiều dấu phẩy)
    parts = line.strip().split(",")
    # Loại bỏ các từ rỗng và ghép lại bằng khoảng trắng
    cleaned_text = ' '.join([word.strip() for word in parts if word.strip()])
    if cleaned_text:  # Bỏ dòng trắng
        cleaned_rows.append([cleaned_text])

# ======================
# BƯỚC 3: Tạo bảng DataFrame
# ======================
df = pd.DataFrame(cleaned_rows, columns=["Chỉ tiêu"])

# ======================
# BƯỚC 4: Xuất ra file CSV sạch
# ======================
output_path = "du_lieu_sach_chi_tieu_cleaned.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"🎉 Đã làm sạch xong và lưu tại: {output_path}")
