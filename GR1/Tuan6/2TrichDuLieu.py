import pdfplumber
import pandas as pd

# --- BƯỚC 1: Trích xuất tất cả bảng từ file PDF ---
def extract_pdf_tables(pdf_path):
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table)
                # Lọc bảng có từ 3 cột trở lên và không hoàn toàn rỗng
                if df.shape[1] >= 3 and df.dropna(how='all').shape[0] > 1:
                    all_tables.append(df)
    print(f"✅ Đã trích xuất {len(all_tables)} bảng từ file PDF.")
    return all_tables

# --- BƯỚC 2: Ghi các bảng vào file Excel ---
def save_tables_to_excel(tables, output_excel):
    if len(tables) == 0:
        print("❌ Không có bảng nào được trích xuất từ file PDF. Không thể lưu vào Excel.")
        return

    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        for idx, table in enumerate(tables):
            sheet_name = f"Sheet{idx+1}"
            table.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
    print(f"✅ Đã lưu thành công vào file: {output_excel}")

# --- CHẠY CHÍNH ---
pdf_file = "VNM_BCTC_Q1_2025.pdf"  # Tên file bạn đã tải về
excel_output = "VNM_Q1_2025_tables.xlsx"

tables = extract_pdf_tables(pdf_file)
save_tables_to_excel(tables, excel_output)
