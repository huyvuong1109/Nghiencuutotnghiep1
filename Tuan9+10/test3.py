from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time

def download_vietstock_pdf(download_dir, stock_code, report_name):
    # Cấu hình trình duyệt Chrome
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,  # Đặt thư mục tải xuống
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True  # Tự động mở file PDF
    }
    options.add_experimental_option("prefs", prefs)
    #options.add_argument("--headless")  # Chạy không hiển thị giao diện
    options.add_argument("--disable-gpu")

    # Đường dẫn tới ChromeDriver
    service = Service(r"D:/Downloads/chromedriver-win64/chromedriver.exe")  # Cập nhật đường dẫn thực tế tới ChromeDriver

    # Khởi tạo trình duyệt
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Truy cập trang tài liệu
        url = f"https://finance.vietstock.vn/{stock_code}/tai-tai-lieu.htm?doctype=1"
        driver.get(url)
        time.sleep(5)  # Chờ trang tải xong

        # Tìm tài liệu PDF theo tên
        pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
        for link in pdf_links:
            if report_name in link.text:
                print(f"Tìm thấy tài liệu: {link.text}")
                link.click()  # Nhấp vào liên kết để tải file PDF
                time.sleep(10)  # Chờ tải xuống hoàn tất
                return

        print("Không tìm thấy tài liệu phù hợp.")
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        driver.quit()

# Cấu hình và thông tin người dùng
download_dir = "./downloads"  # Thư mục lưu trữ file tải xuống
stock_code = "FPT"  # Mã cổ phiếu
report_name = "Báo cáo tài chính Công ty mẹ quý 1 năm 2025"  # Tên tài liệu cần tải

# Tạo thư mục nếu chưa tồn tại
os.makedirs(download_dir, exist_ok=True)

# Gọi hàm tải PDF
download_vietstock_pdf(download_dir, stock_code, report_name)