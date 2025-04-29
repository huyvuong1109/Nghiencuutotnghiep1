import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def get_report_links(stock_code, chrome_driver_path):
    # ✅ Kiểm tra tồn tại của chromedriver.exe
    if not os.path.isfile(chrome_driver_path):
        print(f"❌ chromedriver.exe không tồn tại tại: {chrome_driver_path}")
        print("👉 Hãy kiểm tra lại đường dẫn hoặc tải đúng phiên bản từ: https://googlechromelabs.github.io/chrome-for-testing/")
        return []

    # ✅ Thiết lập Chrome không giao diện (headless)
    options = Options()
    options.add_argument("--headless")
    service = Service(executable_path=chrome_driver_path)

    try:
        driver = webdriver.Chrome(service=service, options=options)
        url = f"https://s.cafef.vn/bao-cao-tai-chinh/VNM/cong-ty-co-phan.chn"
        driver.get(url)

        # ⏳ Đợi trang tải JS
        time.sleep(3)

        # ✅ Lấy các link .pdf
        elements = driver.find_elements(By.TAG_NAME, "a")
        links = [elem.get_attribute("href") for elem in elements if elem.get_attribute("href") and ".pdf" in elem.get_attribute("href")]

        driver.quit()
        return links

    except Exception as e:
        print("❌ Lỗi khi mở Chrome:", e)
        return []

# 🔧 Thay đường dẫn này thành nơi bạn đặt chromedriver.exe
chrome_driver_path = r"C:\Users\Admin\Downloads\chromedriver-win64\chromedriver.exe"  # <== chỉnh lại nếu khác

# 🧪 Ví dụ: Lấy link PDF của mã chứng khoán VNM
stock_code = "VNM"
pdf_links = get_report_links(stock_code, chrome_driver_path)

# ✅ In ra các link lấy được
if pdf_links:
    print(f"✅ Tìm thấy {len(pdf_links)} file PDF cho mã VNM:")
    for link in pdf_links:
        print(link)
else:
    print("⚠️ Không tìm thấy link PDF nào.")
