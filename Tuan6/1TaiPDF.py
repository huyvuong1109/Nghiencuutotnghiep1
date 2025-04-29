import pdfplumber
import pandas as pd

def extract_pdf_tables(pdf_path):
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table)
                # Bỏ qua bảng nhỏ hoặc toàn ô trống
                if df.shape[1] > 2 and df.dropna(how='all').shape[0] > 1:
                    all_tables.append(df)
    print(f"✅ Đã trích xuất {len(all_tables)} bảng từ file PDF.")
    return all_tables

# Gọi hàm
tables = extract_pdf_tables("VNM_Q1_2024.pdf")
