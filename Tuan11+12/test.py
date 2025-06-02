import pytesseract
from PIL import Image
import os
from datetime import datetime

# Đường dẫn Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Đường dẫn ảnh đầu vào
image_path = r"D:/x1g8/Nghiencuutotnghiep1/Tuan6/output_images/page_1.png"

# Đường dẫn lưu CSV
result_dir = "D:/x1g8/Nghiencuutotnghiep1/Tuan6/output"
os.makedirs(result_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_output = os.path.join(result_dir, f"parsed_table_{timestamp}.csv")

# Đọc ảnh và lấy dữ liệu OCR dạng bảng có bounding box
tsv_data = pytesseract.image_to_data(Image.open(image_path), lang="vie", config="--psm 6", output_type=pytesseract.Output.DATAFRAME)

# Lọc từ hợp lệ
tsv_data = tsv_data[tsv_data.text.notnull()]
tsv_data = tsv_data[tsv_data.text.str.strip() != ""]

# Gom nhóm theo dòng
grouped = tsv_data.groupby(['page_num', 'block_num', 'par_num', 'line_num'])

rows = []
column_gap_threshold = 50  # Ngưỡng pixel để tách giữa các cột

for _, line in grouped:
    words = line.sort_values('left')[['left', 'text']].values.tolist()

    current_cell = words[0][1]
    current_left = words[0][0]
    row_cells = []

    for i in range(1, len(words)):
        left, text = words[i]
        if left - current_left > column_gap_threshold:
            # Cách đủ xa → sang cột mới
            row_cells.append(current_cell.strip())
            current_cell = text
        else:
            # Vẫn trong cùng ô → ghép vào
            current_cell += ' ' + text
        current_left = left

    row_cells.append(current_cell.strip())  # Thêm ô cuối cùng
    rows.append(','.join(row_cells))

# Ghi file CSV
with open(csv_output, 'w', encoding='utf-8', newline='') as f:
    for row in rows:
        f.write(row + '\n')

print(f"✅ Đã xuất bảng có phân cột (CSV): {csv_output}")
