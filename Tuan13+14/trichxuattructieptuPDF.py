import pdfplumber
import pandas as pd
import os
from datetime import datetime

# ============================
# CẤU HÌNH
# ============================
pdf_path = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/VNM_BCTC_Q1_2025.pdf"  # Đường dẫn file PDF gốc
output_dir = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output"
os.makedirs(output_dir, exist_ok=True)

# ============================
# ĐỌC PDF & TRÍCH XUẤT BẢNG
# ============================
all_tables = []

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for table in tables:
            if table:
                df = pd.DataFrame(table)
                df.insert(0, 'Trang', i + 1)
                all_tables.append(df)

# ============================
# GHÉP VÀ XUẤT RA CSV
# ============================
if all_tables:
    combined = pd.concat(all_tables, ignore_index=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(output_dir, f"bctc_pdf_tables_{timestamp}.csv")
    combined.to_csv(csv_path, index=False)
    print(f"✅ Đã trích xuất bảng PDF và lưu vào: {csv_path}")
else:
    print("⚠️ Không tìm thấy bảng nào trong PDF.")
