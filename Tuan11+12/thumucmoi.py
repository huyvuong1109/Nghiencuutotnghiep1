import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import openpyxl
import os
from datetime import datetime  # 🕒 dùng để tạo timestamp

# Đường dẫn đến file Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Đường dẫn gốc
input_pdf = "C:/Users/Admin/OneDrive/Documents/GitHub/GR1/output/pages/page_9.pdf"       # File PDF đầu vào
output_dir = "C:/Users/Admin/OneDrive/Documents/GitHub/GR1/output_images"         # Thư mục ảnh trung gian
result_dir = "C:/Users/Admin/OneDrive/Documents/GitHub/GR1/output"  # File Excel đầu ra

# Tạo thư mục nếu chưa có
os.makedirs(output_dir, exist_ok=True)
os.makedirs(result_dir, exist_ok=True)

# Tạo tên file Excel có timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # vd: 20250515_193200
excel_output = os.path.join(result_dir, f"result_{timestamp}.xlsx")

# Chuyển PDF sang ảnh
images = convert_from_path(input_pdf, poppler_path=r"D:\Downloads\poppler-24.08.0\Library\bin")

# Tạo file Excel mới
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Extracted Text"
row_counter = 1

# OCR từng ảnh và ghi vào Excel
for i, img in enumerate(images):
    img_path = os.path.join(output_dir, f"page_{i+1}.png")
    img.save(img_path, "PNG")
    text = pytesseract.image_to_string(Image.open(img_path))
    for line in text.split("\n"):
        if line.strip():
            ws.cell(row=row_counter, column=1, value=line.strip())
            row_counter += 1

# Lưu file Excel với tên có timestamp
wb.save(excel_output)
print(f"✅ Đã tạo file kết quả: {excel_output}")
