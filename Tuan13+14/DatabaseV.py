import pandas as pd
from sqlalchemy import create_engine
import pymysql

# Đọc file CSV
file_path = r"D:\x1g8\Nghiencuutotnghiep1\Tuan13+14\du_lieu_hoan_chinh_cleaned.csv"  # Thay bằng đường dẫn đầy đủ nếu cần
df = pd.read_csv(file_path)

# Làm sạch dữ liệu số: bỏ dấu phẩy, chuyển sang float
for col in df.columns[1:]:
    df[col] = df[col].replace(",", "", regex=True)
    df[col] = pd.to_numeric(df[col], errors='coerce')  # NaN nếu lỗi

# Thông tin kết nối MySQL – SỬA LẠI THEO CẤU HÌNH CỦA BẠN
username = "huyvuong"
password = "vuongquochuy1109@@"  # 🔐 Thay bằng mật khẩu thực tế
host = "localhost"
port = 3306
database = "baocaotc"
table_name = "baocao_taichinh"

# Tạo kết nối
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

# Ghi dữ liệu vào bảng (append = thêm mới, không xóa cũ)
df.to_sql(name=table_name, con=engine, if_exists="append", index=False)

print("✅ Đã nhập dữ liệu CSV vào MySQL thành công!")
