import pandas as pd
import pymysql
import re

# Đọc dữ liệu CSV
df = pd.read_csv("D:/Download/du_lieu_hoan_chinh123.csv", encoding="utf-8-sig")
print("📌 Cột trong file CSV:", df.columns.tolist())

# Chuẩn hoá tên cột
df.rename(columns=lambda x: x.strip(), inplace=True)
df.rename(columns={
    'Chỉ tiêu': 'chi_tieu',
    'Mã số': 'ma_so',
    'Thuyết minh': 'thuyet_minh',
    '31/3/2025': 'so_lieu_31_3_2025',
    '1/1/2025': 'so_lieu_1_1_2025'
}, inplace=True)

# Làm sạch dữ liệu số
def clean_number(x):
    if pd.isna(x):
        return None
    x = str(x).replace(".", "").replace(",", "").strip()
    try:
        return float(x)
    except:
        return None

df['so_lieu_31_3_2025'] = df['so_lieu_31_3_2025'].apply(clean_number)
df['so_lieu_1_1_2025'] = df['so_lieu_1_1_2025'].apply(clean_number)


cursor = conn.cursor()

# Tạo bảng nếu chưa có
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bao_cao_tai_chinh (
        chi_tieu VARCHAR(255),
        ma_so VARCHAR(50),
        thuyet_minh TEXT,
        so_lieu_31_3_2025 DOUBLE,
        so_lieu_1_1_2025 DOUBLE
    )
""")

# Chèn dữ liệu
count = 0
for _, row in df.iterrows():
    values = tuple(
        None if pd.isna(row.get(col)) else row.get(col)
        for col in ["chi_tieu", "ma_so", "thuyet_minh", "so_lieu_31_3_2025", "so_lieu_1_1_2025"]
    )
    try:
        cursor.execute("""
            INSERT INTO bao_cao_tai_chinh 
            (chi_tieu, ma_so, thuyet_minh, so_lieu_31_3_2025, so_lieu_1_1_2025)
            VALUES (%s, %s, %s, %s, %s)
        """, values)
        count += 1
    except Exception as e:
        print("❌ Lỗi khi chèn dòng:", values)
        print("   →", e)

# Kết thúc
conn.commit()
cursor.close()
conn.close()

print(f"✅ Đã import thành công {count} dòng vào MySQL.")
