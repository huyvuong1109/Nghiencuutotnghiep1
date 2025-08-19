import os
import re
from datetime import datetime
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# ======================================================================
# CẤU HÌNH
# ======================================================================
pdf_path = "D:/x1g8/Nghiencuutotnghiep1/downloads/FPT/Báo_cáo_tài_chính_Công_ty_mẹ_quý_1_năm_2025.pdf"
pages_to_process = [5, 6, 7, 8, 9, 10] # Có thể để trống [] để dùng logic tìm trang tự động
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
base_result_dir = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output"

# ======================================================================
# ✨ THUẬT TOÁN TRÍCH XUẤT ĐƠN GIẢN VÀ HIỆU QUẢ ✨
# ======================================================================
def extract_data_with_simple_rules(image_object):
    """
    Hàm trích xuất dữ liệu dựa trên quy tắc đơn giản và đáng tin cậy hơn:
    1. Tìm dòng tiêu đề chứa "Mã số".
    2. Bắt đầu ghi lại các dòng bắt đầu bằng số.
    3. Ghép các dòng không bắt đầu bằng số vào dòng trước đó.
    """
    print("   -> 🤖 Áp dụng thuật toán trích xuất theo quy tắc đơn giản...")
    # Dùng --psm 4 để Tesseract tự động phân tích layout trang
    data = pytesseract.image_to_data(image_object, lang="vie", config="--psm 4", output_type=pytesseract.Output.DATAFRAME)
    data.dropna(subset=['text'], inplace=True)
    data = data[data.text.str.strip() != '']

    # Gom các từ thành các dòng dựa trên vị trí Tesseract trả về
    lines_by_tesseract = data.groupby(['page_num', 'block_num', 'par_num', 'line_num'])
    
    raw_lines = []
    for _, line_df in lines_by_tesseract:
        # Sắp xếp các từ trong dòng từ trái qua phải
        line_df = line_df.sort_values('left')
        line_text = ' '.join(line_df['text'])
        raw_lines.append(line_text)

    # Xử lý logic lọc và ghép dòng
    processed_rows = []
    start_processing = False
    header_skip_count = 2 # Bỏ qua 2 dòng sau khi tìm thấy "Mã số" (thường là tiêu đề)

    for line in raw_lines:
        # Kích hoạt chế độ xử lý khi tìm thấy "Mã số"
        if not start_processing and "Mã số" in line:
            start_processing = True
            print("   -> ✅ Đã tìm thấy tiêu đề, bắt đầu xử lý dữ liệu...")
            continue

        if not start_processing:
            continue
        
        # Bỏ qua các dòng tiêu đề
        if header_skip_count > 0:
            header_skip_count -= 1
            continue

        columns = line.split()
        if not columns: continue

        # Kiểm tra xem dòng có bắt đầu bằng một mã số hợp lệ không
        # (Chỉ chứa số, có thể có chữ cái ở đầu như 'A.', 'B.', 'I.', 'II.')
        if re.match(r'^[A-Z\d\.]+$', columns[0]):
            processed_rows.append(line)
        elif processed_rows:
            # Nếu không phải dòng mới, ghép vào dòng trước đó
            processed_rows[-1] += " " + line

    # Định dạng lại thành CSV
    csv_rows = []
    for row_text in processed_rows:
        # Tách cột đầu tiên (Mã số)
        parts = row_text.split(maxsplit=1)
        if len(parts) == 2:
            code, rest = parts
            # Phần còn lại có thể chứa nhiều cột số liệu, chúng ta tạm gộp chúng
            # và để người dùng tự xử lý trong Excel/CSV nếu cần
            # Bọc trong dấu ngoặc kép để tránh lỗi do dấu phẩy
            csv_rows.append(f'"{code}","{rest.strip()}"')
        else:
            # Xử lý các dòng chỉ có 1 cột (hiếm gặp)
            csv_rows.append(f'"{row_text}"')

    return csv_rows

# ======================================================================
# QUY TRÌNH CHÍNH (MAIN WORKFLOW)
# ======================================================================
if __name__ == "__main__":
    print("⏳ Bước 1: Chuyển đổi PDF sang ảnh...")
    all_images = convert_from_path(pdf_path, dpi=300)
    print(f"✅ Chuyển đổi xong {len(all_images)} trang.")

    # Nếu pages_to_process để trống, có thể thêm lại logic tìm trang tự động ở đây
    if not pages_to_process:
        print("\n🧠 Không có trang nào được chỉ định, vui lòng điền vào biến `pages_to_process`.")
        # Hoặc gọi các hàm find_toc_page, find_pages_by_keyword_fallback...
        exit()
    
    print(f"🎯 Sẽ xử lý các trang được chỉ định: {pages_to_process}")

    # Tạo thư mục lưu kết quả
    pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf_specific_output_dir = os.path.join(base_result_dir, pdf_filename)
    os.makedirs(pdf_specific_output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_output_path = os.path.join(pdf_specific_output_dir, f"{pdf_filename}_data_{timestamp}.csv")
    print(f"   -> File kết quả sẽ được lưu tại: {csv_output_path}")

    all_extracted_rows = []
    for page_number in pages_to_process:
        if page_number > len(all_images):
            print(f"⚠️ Cảnh báo: Trang {page_number} không tồn tại trong file PDF.")
            continue
        
        print(f"\n--- Đang xử lý trang vật lý {page_number} ---")
        img = all_images[page_number - 1]
        
        # Gọi hàm trích xuất mới và đơn giản hơn
        rows = extract_data_with_simple_rules(img)
        
        all_extracted_rows.extend(rows)
        print(f"   -> 📊 Trích xuất được {len(rows)} dòng dữ liệu từ trang này.")

    # Ghi kết quả ra file
    if all_extracted_rows:
        with open(csv_output_path, 'w', encoding='utf-8-sig', newline='') as f:
            f.write('"Mã số","Nội dung"\n') # Ghi tiêu đề cho file CSV
            for row in all_extracted_rows:
                f.write(row + '\n')
    
    print(f"\n🎉 HOÀN TẤT! Đã xử lý {len(pages_to_process)} trang và trích xuất tổng cộng {len(all_extracted_rows)} dòng dữ liệu.")