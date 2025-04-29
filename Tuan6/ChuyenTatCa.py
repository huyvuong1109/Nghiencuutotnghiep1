import aspose.pdf as ap
import os

input_dir = "output/pages/"        # Thư mục chứa các file PDF đã tách
output_dir = "output/excels/"      # Nơi lưu Excel sau khi chuyển

os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(input_dir):
    if file.endswith(".pdf"):
        input_pdf = os.path.join(input_dir, file)
        output_excel = os.path.join(output_dir, file.replace(".pdf", ".xlsx"))

        document = ap.Document(input_pdf)
        save_options = ap.ExcelSaveOptions()
        save_options.minimize_the_number_of_worksheets = True  # Tối ưu file Excel đơn giản hơn

        document.save(output_excel, save_options)

print(f"Đã chuyển đổi tất cả các trang sang Excel tại: {output_dir}")
