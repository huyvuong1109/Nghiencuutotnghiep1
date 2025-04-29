import pytesseract
from pdf2image import convert_from_path

def ocr_pdf_scan(pdf_path):
    images = convert_from_path(pdf_path)
    text_result = ""
    for img in images:
        text = pytesseract.image_to_string(img, lang="vie+eng")  # có thể thêm tiếng Việt nếu cài gói
        text_result += text + "\n"
    return text_result

# OCR cho file scan
ocr_text = ocr_pdf_scan(pdf_file)
print(ocr_text[:500])  # In thử 500 ký tự đầu
