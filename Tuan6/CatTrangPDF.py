from PyPDF2 import PdfReader, PdfWriter
import os

input_pdf_path = "VNM_BCTC_Q1_2025.pdf"  # Đường dẫn file PDF gốc
output_dir = "output/pages/"  # Thư mục chứa các trang đã tách

# Tạo thư mục đầu ra nếu chưa có
os.makedirs(output_dir, exist_ok=True)

reader = PdfReader(input_pdf_path)
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)

    output_path = os.path.join(output_dir, f"page_{i+1}.pdf")
    with open(output_path, "wb") as f:
        writer.write(f)

print(f"Đã tách {len(reader.pages)} trang vào thư mục: {output_dir}")
