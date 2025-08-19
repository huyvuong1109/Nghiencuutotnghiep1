import pandas as pd

# ===  Đọc file CSV gốc bị lỗi OCR ===
input_path = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output/du_lieu_sach.csv"
with open(input_path, "r", encoding="utf-8") as f:
    raw_lines = f.readlines()

cleaned_rows = []

# ===  Làm sạch từng dòng ===
for line in raw_lines:
    if not line.strip():
        continue  # Bỏ dòng trắng

    # Tách dòng theo dấu phẩy
    parts = line.strip().split(",")

    # Tìm vị trí bắt đầu phần số liệu (giả định phần số bắt đầu từ một token toàn số hoặc gần giống số)
    split_index = None
    for i, token in enumerate(parts):
        cleaned_token = token.strip().replace(".", "").replace(",", "").replace("-", "")
        if cleaned_token.isdigit():
            split_index = i
            break

    if split_index is None:
        # Nếu không tìm thấy số, giả định cả dòng là văn bản
        text_part = ' '.join([p.strip() for p in parts if p.strip()])
        cleaned_rows.append([text_part])
    else:
        # Ghép phần văn bản
        text_tokens = parts[:split_index]
        text = ' '.join([t.strip() for t in text_tokens if t.strip()])

        # Làm sạch phần số liệu: xoá dấu chấm ở giữa số
        number_tokens = parts[split_index:]
        cleaned_numbers = [nt.strip().replace(".", "") for nt in number_tokens]

        # Tạo dòng hoàn chỉnh
        full_row = [text] + cleaned_numbers
        cleaned_rows.append(full_row)

# ===  Tạo bảng và xuất kết quả ===
# Tìm số cột lớn nhất
max_cols = max(len(row) for row in cleaned_rows)
columns = ["Chỉ tiêu"] + [f"Số liệu {i}" for i in range(1, max_cols)]

df_cleaned = pd.DataFrame(cleaned_rows, columns=columns[:max_cols])

# ===  Ghi ra file CSV đã làm sạch ===
output_path = "du_lieu_hoan_chinh_cleaned.csv"
df_cleaned.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ File đã được làm sạch và lưu tại: {output_path}")
