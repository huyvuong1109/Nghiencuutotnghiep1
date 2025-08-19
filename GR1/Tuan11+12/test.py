import pytesseract
from PIL import Image
import pandas as pd
import os
from datetime import datetime

# Đường dẫn đến Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Đường dẫn ảnh đầu vào
image_path = r"D:/x1g8/Nghiencuutotnghiep1/Tuan6/output_images/page_1.png"

# Đường dẫn lưu kết quả CSV
result_dir = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output"
os.makedirs(result_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_output = os.path.join(result_dir, f"final_table_{timestamp}.csv")

# Đọc dữ liệu từ ảnh với bounding boxes
df = pytesseract.image_to_data(Image.open(image_path), lang='vie', config='--psm 6', output_type=pytesseract.Output.DATAFRAME)

# Lọc từ có nội dung
df = df[df.text.notnull()]
df = df[df.text.str.strip() != ""]

# Gom nhóm theo dòng
grouped = df.groupby(['block_num', 'par_num', 'line_num'])

# Các tham số tùy chỉnh
left_threshold = 300   # Phần text bên trái (mô tả chỉ tiêu)
col_gap = 60           # Khoảng cách giữa các cột số

rows = []

for _, group in grouped:
    words = group.sort_values('left')[['left', 'text']].values.tolist()
    
    # Gom các từ có left nhỏ hơn threshold thành cột đầu tiên (mô tả)
    col1_words = [text for left, text in words if left < left_threshold]
    right_side = [(left, text) for left, text in words if left >= left_threshold]

    row = [' '.join(col1_words).strip()]  # Cột đầu tiên: ghép từ
    
    # Gom các cột bên phải dựa vào khoảng cách giữa left
    if right_side:
        current_cell = right_side[0][1]
        current_left = right_side[0][0]
        for i in range(1, len(right_side)):
            left, text = right_side[i]
            if left - current_left > col_gap:
                row.append(current_cell.strip())
                current_cell = text
            else:
                current_cell += ' ' + text
            current_left = left
        row.append(current_cell.strip())
    
    rows.append(row)

# Ghi ra CSV
df_out = pd.DataFrame(rows)
df_out.to_csv(csv_output, index=False, header=False, encoding='utf-8-sig')

print(f"✅ Đã xuất file CSV chuẩn: {csv_output}")
