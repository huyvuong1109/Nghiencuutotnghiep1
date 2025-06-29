import pandas as pd
import pymysql

# ============================
# CẤU HÌNH
# ============================
INPUT_CSV_PATH = 'cleaned_BCTC_for_db_v3_smart.csv'
TICKER = 'VIC'
QUARTER = 1
YEAR = 2025
TABLE_NAME = f"bctc_{TICKER.lower()}_q{QUARTER}_{YEAR}"

DB_HOST = 'localhost'
DB_USER = 'huyvuong'
DB_PASS = 'vuongquochuy1109@@'
DB_NAME = 'baocaotc'

# ============================
# XỬ LÝ DỮ LIỆU VÀ IMPORT
# ============================

def run_import():
    """Hàm chính để thực hiện toàn bộ quá trình import."""
    
    try:
        df = pd.read_csv(INPUT_CSV_PATH, encoding="utf-8")
        print(f"✅ Đã đọc thành công file '{INPUT_CSV_PATH}'.")
    except FileNotFoundError:
        print(f"❌ Lỗi: Không tìm thấy file tại '{INPUT_CSV_PATH}'.")
        return

    # Chuyển đổi các cột số, lỗi sẽ thành NaT (Not a Time) -> NaN
    df['số cuối kì'] = pd.to_numeric(df['số cuối kì'], errors='coerce')
    df['số đầu kì'] = pd.to_numeric(df['số đầu kì'], errors='coerce')
    print("✅ Đã chuyển đổi các cột số.")
    
    conn = None
    try:
        conn = pymysql.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME, charset='utf8mb4'
        )
        cursor = conn.cursor()
        print("✅ Kết nối tới database MySQL thành công.")

        print(f"🔧 Chuẩn bị tạo bảng '{TABLE_NAME}'...")
        cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME};")
        print(f"   - Đã xóa bảng cũ (nếu có).")

        create_table_query = f"""
        CREATE TABLE {TABLE_NAME} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ma_so VARCHAR(50),
            tai_san VARCHAR(255),
            thuyet_minh VARCHAR(100),
            so_cuoi_ky BIGINT,
            so_dau_ky BIGINT,
            ngay_nhap_lieu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        print(f"   - ✅ Đã tạo bảng mới '{TABLE_NAME}' với cấu trúc đúng.")

        insert_query = f"""
        INSERT INTO {TABLE_NAME} (ma_so, tai_san, thuyet_minh, so_cuoi_ky, so_dau_ky)
        VALUES (%s, %s, %s, %s, %s);
        """
        
        count = 0
        for _, row in df.iterrows():
            # ✨✨✨ SỬA LỖI TRIỆT ĐỂ ✨✨✨
            # Thay thế tất cả các giá trị NaN trong toàn bộ dòng bằng None của Python.
            # Dùng phương thức to_dict() để dễ dàng xử lý và kiểm tra.
            cleaned_row = row.where(pd.notnull(row), None).to_dict()
            
            record = (
                cleaned_row['mã số'],
                cleaned_row['tài sản'],
                cleaned_row['thuyết minh'],
                # Chuyển thành int nếu không phải None, để phù hợp với kiểu BIGINT
                int(cleaned_row['số cuối kì']) if cleaned_row['số cuối kì'] is not None else None,
                int(cleaned_row['số đầu kì']) if cleaned_row['số đầu kì'] is not None else None
            )

            try:
                cursor.execute(insert_query, record)
                count += 1
            except pymysql.Error as e:
                print(f"❌ Lỗi khi chèn dòng: {record}")
                print(f"   → {e}")
                
        conn.commit()
        print("-" * 30)
        print(f"🎉 Đã import thành công {count} dòng vào bảng '{TABLE_NAME}'.")

    except pymysql.Error as e:
        print(f"❌ Lỗi kết nối hoặc thực thi Database: {e}")
    finally:
        if conn and conn.open:
            cursor.close()
            conn.close()
            print("✅ Đã đóng kết nối database.")

if __name__ == '__main__':
    run_import()