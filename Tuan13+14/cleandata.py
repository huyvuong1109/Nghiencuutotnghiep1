import pandas as pd
import re
from sqlalchemy import create_engine

# --- KẾT NỐI MYSQL ---
engine = create_engine('mysql+pymysql://root:matkhau@localhost:3306/ten_database')  # sửa thông tin của bạn

# --- ĐỌC FILE DÒNG THEO DÒNG ---
with open('bao_cao.csv', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip() != ""]

# --- TÌM PHẦN CHỨA DỮ LIỆU BẢNG TÀI CHÍNH ---
data_lines = []
capture = False

for line in lines:
    # Khi thấy dòng chứa "NGUỒN VỐN", bắt đầu lấy dữ liệu
    if "NGUÔỒN" in line or "NGUỒN" in line:
        capture = True
    if capture:
        # Nếu dòng có quá ít từ hoặc là chú thích/metadata, thì bỏ qua
        if any(keyword in line for keyword in ["Người lập", "Ngày", "Cúc thuyết", "Kế toán", "Giám đốc"]):
            break
        data_lines.append(line)

# --- XỬ LÝ DÒNG DỮ LIỆU ---
structured_rows = []

for line in data_lines:
    # Tách cột theo dấu phẩy
    row = [col.strip() for col in line.split(',')]
    # Bỏ dòng nếu quá ngắn
    if len(row) < 4:
        continue
    structured_rows.append(row)

# --- TÌM HEADER ---
headers = structured_rows[1]  # thường là dòng chứa: Mã, Thuyết minh, 31/3/2025, 1/1/2025
data = structured_rows[2:]   # bỏ header và dòng đầu

# --- CHUYỂN THÀNH DATAFRAME ---
df = pd.DataFrame(data, columns=headers[:len(data[0])])  # cắt header vừa đúng số cột thực tế

# --- LÀM SẠCH DỮ LIỆU SỐ ---
def clean_number(val):
    if not isinstance(val, str):
        return val
    val = val.replace('.', '').replace(',', '')
    val = re.sub(r'[^\d\-]', '', val)
    return pd.to_numeric(val, errors='coerce')

for col in df.columns:
    df[col] = df[col].apply(clean_number if 'VND' in col or re.search(r'\d{4}', col) else lambda x: x)

# --- ĐỔ VÀO MYSQL ---
table_name = "nguon_von_baocao"
df.to_sql(table_name, con=engine, if_exists='replace', index=False)

print(f"✅ Đã import bảng `{table_name}` vào MySQL.")
