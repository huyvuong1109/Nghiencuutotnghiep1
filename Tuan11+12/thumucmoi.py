import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import openpyxl
import os
from datetime import datetime

# Đường dẫn đến file Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Cấu hình đường dẫn
input_pdf = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output/pages/page_9.pdf"
output_dir = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output_images"
result_dir = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output"

os.makedirs(output_dir, exist_ok=True)
os.makedirs(result_dir, exist_ok=True)

# Tạo tên file Excel với timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
excel_output = os.path.join(result_dir, f"result_table_{timestamp}.xlsx")

# Chuyển PDF sang ảnh
images = convert_from_path(input_pdf, poppler_path=r"D:\Download\poppler-24.08.0\Library\bin")

# Tạo file Excel mới
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Extracted Table"

row_counter = 1

# OCR từng ảnh và ghi vào Excel
for i, img in enumerate(images):
    img_path = os.path.join(output_dir, f"page_{i+1}.png")
    img.save(img_path, "PNG")

    # Dùng cấu hình OCR cho dạng bảng
    custom_config = r'--psm 6'  # Mode 6: Assume a single uniform block of text
    text = pytesseract.image_to_string(Image.open(img_path), lang="vie", config=custom_config)

    for line in text.split("\n"):
        if line.strip():
            # Tách dòng thành cột bằng nhiều khoảng trắng
            columns = [col.strip() for col in line.split("  ") if col.strip()]
            for col_index, cell in enumerate(columns):
                ws.cell(row=row_counter, column=col_index + 1, value=cell)
            row_counter += 1

# Lưu file Excel
wb.save(excel_output)
print(f"✅ Đã tạo file Excel kết quả theo dạng bảng: {excel_output}")
