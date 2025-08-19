import aspose.pdf as ap

# Đường dẫn đến file PDF đầu vào
input_pdf = "output/pages/page_8.pdf"

# Đường dẫn lưu file Excel .xlsx đầu ra
output_excel = "output1.xlsx"

# Mở file PDF
document = ap.Document(input_pdf)

# Tạo tùy chọn lưu (mặc định là .xlsx)
save_options = ap.ExcelSaveOptions()

# Lưu file
document.save(output_excel, save_options)
