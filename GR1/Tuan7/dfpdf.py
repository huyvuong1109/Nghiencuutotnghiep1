import os
import time
import pdfplumber
import requests
from playwright.sync_api import sync_playwright
import openpyxl

# Bước 1: Tải trang Vietstock và lấy liên kết PDF BCTC
def get_pdf_link():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Sử dụng headless=True để tăng tốc độ
        page = browser.new_page()
        
        try:
            # Thử load trang với timeout 60 giây, và đợi DOM tải hoàn tất
            page.goto("https://finance.vietstock.vn/PVG/cong-bo-thong-tin.htm", timeout=60000, wait_until="domcontentloaded")  

            # Đợi cho đến khi phần tử có class 'attachment-list' xuất hiện
            page.wait_for_selector(".attachment-list", timeout=60000)  # Chờ tối đa 60 giây

            # Tìm tất cả các liên kết PDF
            links = page.locator("a[href$='.pdf']").all_texts()  # Lấy tất cả các liên kết PDF
            browser.close()

            if links:
                return links[0]  # Giả sử file PDF đầu tiên là file cần tải
            else:
                print("Không tìm thấy file PDF!")
                return None
        except Exception as e:
            print(f"Lỗi khi tải trang: {e}")
            browser.close()
            return None

# Bước 2: Tải file PDF về
def download_pdf(pdf_url, save_path):
    response = requests.get(pdf_url)
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"Đã tải về: {save_path}")

# Bước 3: Đọc dữ liệu từ file PDF
def extract_pdf_data(pdf_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        # Lấy dữ liệu từ tất cả các trang của PDF
        for page in pdf.pages:
            table = page.extract_table()  # Giả sử file PDF có bảng
            if table:
                for row in table:
                    data.append(row)
    return data

# Bước 4: Ghi dữ liệu vào file Excel
def write_to_excel(data, excel_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    for row in data:
        ws.append(row)
    wb.save(excel_path)
    print(f"Dữ liệu đã được ghi vào {excel_path}")

# Chạy tất cả các bước
def main():
    pdf_url = get_pdf_link()
    if pdf_url:
        pdf_filename = "bctc.pdf"
        download_pdf(pdf_url, pdf_filename)
        
        # Đọc dữ liệu từ PDF
        data = extract_pdf_data(pdf_filename)

        # Ghi dữ liệu ra Excel
        excel_filename = "bctc.xlsx"
        write_to_excel(data, excel_filename)

        # Xóa file PDF sau khi xử lý
        os.remove(pdf_filename)
        print("Hoàn thành!")
    else:
        print("Không thể lấy file PDF.")

if __name__ == "__main__":
    main()
