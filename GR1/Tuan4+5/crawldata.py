import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Cài đặt Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL của trang web HOSE (Hoặc bạn có thể thay bằng trang khác)
url = 'https://www.hsx.vn/'

# Mở trang web
driver.get(url)

# Đợi trang web load xong
driver.implicitly_wait(5)

# Lấy nội dung HTML của trang
html_content = driver.page_source

# Đóng trình duyệt
driver.quit()

# Phân tích HTML với BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Tìm tất cả các liên kết đến báo cáo tài chính (có thể là PDF hoặc hình ảnh)
# Ví dụ, báo cáo tài chính có thể chứa từ khóa như "PDF" trong thuộc tính href
report_links = soup.find_all('PDF', href=True)

# Tạo thư mục để lưu ảnh hoặc báo cáo
if not os.path.exists('bao_cao_tai_chinh'):
    os.makedirs('bao_cao_tai_chinh')

# Duyệt qua các liên kết và tải báo cáo PDF hoặc hình ảnh
for link in report_links:
    href = link['href']
    # Kiểm tra nếu liên kết có chứa 'pdf' hoặc ảnh
    if 'pdf' in href or 'image' in href:
        file_url = href if 'http' in href else f"https://www.hsx.vn{href}"
        try:
            # Tải xuống file báo cáo
            response = requests.get(file_url)
            if response.status_code == 200:
                # Lưu ảnh hoặc PDF vào thư mục
                file_name = os.path.join('bao_cao_tai_chinh', file_url.split('/')[-1])
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                print(f"Đã tải xuống {file_name}")
        except Exception as e:
            print(f"Lỗi khi tải xuống {file_url}: {e}")

