import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import openpyxl
import os

# Đường dẫn đến file tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # ⚠️ chỉnh cho đúng máy bạn

input_pdf = "output/pages/page_8.pdf"       # File PDF đầu vào
output_dir = "output_images"         # Thư mục ảnh trung gian
excel_output = "output/result.xlsx"  # File Excel đầu ra

# Bước 1: Chuyển PDF thành ảnh
os.makedirs(output_dir, exist_ok=True)
images = convert_from_path(input_pdf)

# Bước 2: Tạo workbook Excel mới
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Extracted Text"

row_counter = 1

# Bước 3: Duyệt qua từng ảnh, OCR và ghi ra Excel
for i, img in enumerate(images):
    img_path = os.path.join(output_dir, f"page_{i+1}.png")
    img.save(img_path, "PNG")

    # OCR trên ảnh
    text = pytesseract.image_to_string(Image.open(img_path))

    # Ghi từng dòng văn bản vào Excel
    for line in text.split("\n"):
        if line.strip():  # Bỏ dòng trống
            ws.cell(row=row_counter, column=1, value=line.strip())
            row_counter += 1

# Bước 4: Lưu file Excel
wb.save(excel_output)
print(f"Đã chuyển PDF sang Excel tại: {excel_output}")
