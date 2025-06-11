from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time
import shutil

def download_vietstock_pdf(download_dir, stock_code, report_name):
    # Tạo thư mục riêng cho mã cổ phiếu
    target_dir = os.path.join(download_dir, stock_code)
    os.makedirs(target_dir, exist_ok=True)

    # Cấu hình trình duyệt Chrome
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": os.path.abspath(download_dir),
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    }
    options.add_experimental_option("prefs", prefs)
    # Tắt chế độ headless để kiểm tra tải về
    # options.add_argument("--headless")  # Có thể bật lại sau khi test xong
    options.add_argument("--disable-gpu")

    # Đường dẫn tới ChromeDriver
    service = Service(r"D:/Download/chromedriver-win64/chromedriver.exe")

    # Khởi tạo trình duyệt
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Truy cập trang tài liệu
        url = f"https://finance.vietstock.vn/{stock_code}/tai-tai-lieu.htm?doctype=1"
        driver.get(url)
        time.sleep(5)

        # Tìm tài liệu PDF theo tên
        pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
        for link in pdf_links:
            if report_name in link.text:
                print(f"Tìm thấy tài liệu: {link.text}")
                pdf_url = link.get_attribute('href')

                # Mở link PDF trực tiếp để kích hoạt tải
                driver.execute_script(f"window.location.href='{pdf_url}'")
                time.sleep(10)  # Chờ tải xong

                # Tìm file PDF mới nhất trong thư mục tải
                downloaded_files = [f for f in os.listdir(download_dir) if f.endswith('.pdf')]
                if not downloaded_files:
                    print("Không tìm thấy file PDF đã tải.")
                    return

                newest_file = max(
                    [os.path.join(download_dir, f) for f in downloaded_files],
                    key=os.path.getctime
                )

                # Tạo tên file đích
                safe_filename = report_name.replace(" ", "_").replace("/", "_") + ".pdf"
                dest_file = os.path.join(target_dir, safe_filename)

                # Di chuyển file
                shutil.move(newest_file, dest_file)
                print(f"Đã lưu file vào: {dest_file}")
                return

        print("Không tìm thấy tài liệu phù hợp.")
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        driver.quit()

# Cấu hình và thông tin người dùng
download_dir = "./downloads"
stock_code = "FPT"
report_name = "Báo cáo tài chính Công ty mẹ quý 1 năm 2025"

# Tạo thư mục nếu chưa tồn tại
os.makedirs(download_dir, exist_ok=True)

# Gọi hàm tải PDF
download_vietstock_pdf(download_dir, stock_code, report_name)
