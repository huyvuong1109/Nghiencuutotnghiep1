import os
import re
from datetime import datetime
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# ======================================================================
# CẤU HÌNH (Bạn chỉ cần thay đổi các đường dẫn này)
# ======================================================================
# 1. Đường dẫn tới file PDF cần xử lý
pdf_path = "D:/x1g8/Nghiencuutotnghiep1/downloads/FPT/Báo_cáo_tài_chính_Công_ty_mẹ_quý_1_năm_2025.pdf"

# 2. Đường dẫn tới thư mục chứa kết quả
base_result_dir = "D:/x1g8/Nghiencuutotnghiep1/Kì hè/output"

# 3. Đường dẫn tới Tesseract OCR (thường không cần thay đổi)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ======================================================================
# ✨ CẤU HÌNH CÁC LOẠI BÁO CÁO CẦN TÌM ✨
# ======================================================================
# Chương trình sẽ tìm các trang chứa những từ khóa này và gom chúng lại.
# Tên file sẽ được đặt theo key (ví dụ: BANG_CAN_DOI_KE_TOAN.csv)
REPORT_SECTIONS = {
    "BANG_CAN_DOI_KE_TOAN": "BẢNG CÂN ĐỐI KẾ TOÁN",
    "KQHDKD": "BÁO CÁO KẾT QUẢ HOẠT ĐỘNG KINH DOANH",
    "LUU_CHUYEN_TIEN_TE": "BÁO CÁO LƯU CHUYỂN TIỀN TỆ"
}

# ======================================================================
# HÀM 1: TỰ ĐỘNG PHÂN LOẠI TRANG
# ======================================================================
def classify_pages(images, sections_config):
    """
    Quét qua tất cả các trang và phân loại chúng vào các nhóm báo cáo tương ứng.
    Trả về một dictionary, ví dụ: {'BANG_CAN_DOI_KE_TOAN': [5, 6], 'KQHDKD': [7], ...}
    """
    print("\n🧠 Bước 2: Bắt đầu tự động phân loại các trang...")
    
    classified_pages = {key: [] for key in sections_config.keys()}
    current_section = None

    for i, img in enumerate(images):
        page_num = i + 1
        print(f"   -> Đang quét trang {page_num}...")
        text = pytesseract.image_to_string(img, lang='vie').upper()

        # Kiểm tra xem trang này có phải là trang bắt đầu của một báo cáo mới không
        found_new_section = False
        for section_key, keyword in sections_config.items():
            if keyword in text:
                current_section = section_key
                print(f"      ✅ Nhận diện trang {page_num} thuộc về: {section_key}")
                found_new_section = True
                break
        
        # Nếu một trang được xác định, thêm nó vào nhóm tương ứng
        if current_section:
            # Điều kiện này để đảm bảo trang mục lục không bị thêm vào
            if "MỤC LỤC" not in text:
                 classified_pages[current_section].append(page_num)

    return classified_pages

# ======================================================================
# HÀM 2: THUẬT TOÁN TRÍCH XUẤT DỮ LIỆU TỪ ẢNH
# ======================================================================
def extract_data_from_image(image_object):
    """
    Trích xuất dữ liệu từ một ảnh dựa trên quy tắc đã được kiểm chứng.
    """
    print("      -> 🤖 Áp dụng thuật toán trích xuất chi tiết...")
    data = pytesseract.image_to_data(image_object, lang="vie", config="--psm 4", output_type=pytesseract.Output.DATAFRAME)
    data.dropna(subset=['text'], inplace=True)
    data = data[data.text.str.strip() != '']

    lines_by_tesseract = data.groupby(['page_num', 'block_num', 'par_num', 'line_num'])
    raw_lines = [' '.join(line_df.sort_values('left')['text']) for _, line_df in lines_by_tesseract]

    processed_rows = []
    start_processing = False
    
    for line in raw_lines:
        # Kích hoạt chế độ xử lý khi tìm thấy "Mã số" hoặc "CHỈ TIÊU"
        if not start_processing and ("Mã số" in line or "CHỈ TIÊU" in line):
            start_processing = True
            continue
        if not start_processing: continue

        columns = line.split()
        if not columns: continue

        # Kiểm tra xem dòng có bắt đầu bằng mã số/chỉ mục hợp lệ không
        if re.match(r'^[A-Z\d\.\(\)]+$', columns[0]):
            processed_rows.append(line)
        elif processed_rows:
            processed_rows[-1] += " " + line

    csv_rows = []
    for row_text in processed_rows:
        parts = row_text.split(maxsplit=1)
        if len(parts) == 2:
            code, rest = parts
            csv_rows.append(f'"{code}","{rest.strip()}"')
        else:
            csv_rows.append(f'"{row_text}"')

    return csv_rows

# ======================================================================
# QUY TRÌNH CHÍNH (MAIN WORKFLOW)
# ======================================================================
if __name__ == "__main__":
    print("⏳ Bước 1: Chuyển đổi PDF sang ảnh...")
    all_images = convert_from_path(pdf_path, dpi=300)
    print(f"✅ Chuyển đổi xong {len(all_images)} trang.")

    # Phân loại tất cả các trang trong file PDF
    pages_by_section = classify_pages(all_images, REPORT_SECTIONS)

    # Tạo thư mục lưu kết quả chung cho file PDF này
    pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf_specific_output_dir = os.path.join(base_result_dir, pdf_filename)
    os.makedirs(pdf_specific_output_dir, exist_ok=True)
    print(f"\n📂 Kết quả sẽ được lưu trong thư mục: {pdf_specific_output_dir}")

    # Xử lý và lưu file cho từng loại báo cáo
    for section_key, page_numbers in pages_by_section.items():
        if not page_numbers:
            print(f"\n⚠️ Không tìm thấy trang nào cho báo cáo: {section_key}")
            continue

        print(f"\n--- 🚀 Đang xử lý báo cáo: {section_key} (Trang: {page_numbers}) ---")
        
        section_all_rows = []
        for page_num in page_numbers:
            print(f"   -> Đang trích xuất dữ liệu từ trang {page_num}...")
            img = all_images[page_num - 1]
            rows = extract_data_from_image(img)
            section_all_rows.extend(rows)
            print(f"      -> Trích xuất được {len(rows)} dòng.")

        # Ghi kết quả của báo cáo này ra một file CSV riêng
        if section_all_rows:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Tạo tên file dựa trên key của báo cáo
            output_filename = f"{pdf_filename}_{section_key}_{timestamp}.csv"
            csv_output_path = os.path.join(pdf_specific_output_dir, output_filename)

            with open(csv_output_path, 'w', encoding='utf-8-sig', newline='') as f:
                f.write('"Mã số/Chỉ tiêu","Nội dung"\n')
                for row in section_all_rows:
                    f.write(row + '\n')
            
            print(f"   -> ✅ Đã lưu thành công {len(section_all_rows)} dòng vào file: {output_filename}")

    print(f"\n🎉 HOÀN TẤT TOÀN BỘ QUÁ TRÌNH!")
