import csv
import os

# ============================
# CẤU HÌNH
# ============================
# Đường dẫn file CSV đầu vào
input_csv_path = 'D:/x1g8/Nghiencuutotnghiep1/Tuan6/output/Báo_cáo_tài_chính_Công_ty_mẹ_quý_1_năm_2025_filtered_20250630_085252.csv'

# Tên file CSV đầu ra (với logic xử lý thông minh hơn)
output_csv_path = 'cleaned_BCTC_for_db_v3_smart.csv'

# ============================
# HÀM XỬ LÝ
# ============================

def clean_financial_data_smart(input_path, output_path):
    """
    Đọc file CSV từ OCR, làm sạch và tái cấu trúc với logic thông minh hơn.
    - ✨ LOGIC MỚI: Phân biệt chính xác giữa 'tài sản' và 'thuyết minh' ngay cả khi
      cột thuyết minh bị trống, tránh lấy nhầm từ cuối của tài sản.
    - Loại bỏ triệt để các ký tự không mong muốn: '.', '(', ')'.
    """
    print(f"Bắt đầu xử lý file với logic thông minh: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"Lỗi: Không tìm thấy file đầu vào tại '{input_path}'")
        return

    with open(input_path, mode='r', encoding='utf-8') as infile, \
         open(output_path, mode='w', encoding='utf-8', newline='') as outfile:
        
        writer = csv.writer(outfile)
        header = ['mã số', 'tài sản', 'thuyết minh', 'số cuối kì', 'số đầu kì']
        writer.writerow(header)
        
        line_count = 0
        processed_count = 0
        
        # Bỏ qua dòng tiêu đề của file input nếu có
        next(infile, None)

        for line in infile:
            line_count += 1
            parts = [p.strip() for p in line.strip().split(',') if p.strip()]
            
            # Yêu cầu tối thiểu 4 cột: mã số, tài sản, số cuối, số đầu
            if len(parts) < 4:
                print(f"  - Dòng {line_count}: Bỏ qua do không đủ cột '{line.strip()}'")
                continue

            # --- ✨ LOGIC XỬ LÝ MỚI ✨ ---
            
            # 1. Xác định các cột cơ bản luôn có
            ma_so = parts[0]
            so_dau_ky = parts[-1]
            so_cuoi_ky = parts[-2]
            
            # 2. Xác định phần giữa (tài sản và có thể có thuyết minh)
            middle_parts = parts[1:-2]
            
            tai_san = ''
            thuyet_minh = ''

            # 3. Phân tích phần giữa để tách tài sản và thuyết minh
            if not middle_parts:
                # Trường hợp hiếm gặp: chỉ có mã số và 2 cột số
                tai_san = ''
                thuyet_minh = ''
            else:
                last_middle_part = middle_parts[-1]
                
                # Heuristic: Nếu phần tử cuối của phần giữa là một từ (chỉ chứa chữ cái),
                # nó thuộc về "tài sản". Ngược lại (nếu nó là số hoặc mã như 'V.01'),
                # nó là "thuyết minh".
                if last_middle_part.isalpha():
                    # Nó là một từ -> thuộc về tài sản, vậy thuyết minh rỗng
                    thuyet_minh = ''
                    tai_san = ' '.join(middle_parts)
                else:
                    # Nó là số hoặc mã -> đây chính là thuyết minh
                    thuyet_minh = last_middle_part
                    tai_san = ' '.join(middle_parts[:-1])

            # 4. Làm sạch triệt để các ký tự không mong muốn
            def clean_text(text):
                return text.replace('.', '').replace('(', '').replace(')', '').replace(',', '').strip()

            final_row = [
                clean_text(ma_so),
                clean_text(tai_san),
                clean_text(thuyet_minh),
                clean_text(so_cuoi_ky),
                clean_text(so_dau_ky)
            ]
            
            writer.writerow(final_row)
            processed_count += 1

    print("-" * 30)
    print(f"✅ Hoàn thành!")
    print(f"Tổng số dòng đã đọc: {line_count}")
    print(f"Số dòng đã xử lý và ghi vào file: {processed_count}")
    print(f"Dữ liệu đã được làm sạch và lưu tại: {output_path}")

# ============================
# THỰC THI
# ============================
if __name__ == '__main__':
    clean_financial_data_smart(input_csv_path, output_csv_path)