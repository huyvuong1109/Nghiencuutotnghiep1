import requests

# URL của tệp PDF bạn muốn tải
url = "https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/FPT_Baocaotaichinh_Q1_2025_Congtyme.pdf"

# Tên file sẽ lưu sau khi tải xong
output_file = "FPT_Q1_2025.pdf"

# Tải tệp PDF
response = requests.get(url)
if response.status_code == 200:  # Kiểm tra nếu tải thành công
    with open(output_file, "wb") as file:
        file.write(response.content)  # Ghi nội dung vào file
    print(f"Tải thành công: {output_file}")
else:
    print(f"Tải thất bại. Mã lỗi: {response.status_code}")