import pandas as pd
import pymysql

# Đọc file CSV
df = pd.read_csv("D:/Download/du_lieu_hoan_chinh123.csv", encoding="utf-8")

# Kết nối MySQL
conn = pymysql.connect(
    host='localhost',
    user='huyvuong',
    password='vuongquochuy1109@@',
    database='baocaotc',
    charset='utf8mb4'
)
cursor = conn.cursor()

# Tên bảng phù hợp với CREATE TABLE bạn đã tạo trước đó
for _, row in df.iterrows():
    # Chuyển NaN → None (MySQL chấp nhận NULL)
    values = tuple(None if pd.isna(v) else v for v in row.iloc[:5])

    cursor.execute(
        """
        INSERT INTO bao_cao_tai_chinh 
        (chi_tieu, ma_so, thuyet_minh, so_lieu_31_3_2025, so_lieu_1_1_2025)
        VALUES (%s, %s, %s, %s, %s)
        """,
        values
    )


conn.commit()
cursor.close()
conn.close()

print("Import thành công!")
