import os
import requests
import time
from bs4 import BeautifulSoup

# ==============================================================================
# KHU VỰC TÙY CHỈNH
# ==============================================================================
STOCK_CODES_TO_DOWNLOAD = ["VNM", "FPT", "HPG"] # Chỉ chạy 3 mã để test cho nhanh
KEYWORD_FILTERS = [
    "bao cao tai chinh cong ty me",
    "bao cao tai chinh hop nhat quy"
]
# ==============================================================================

# ... (Hàm sanitize_filename giữ nguyên) ...
def sanitize_filename(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in (' ', '_', '-')]).rstrip()

def download_reports_final_api(download_dir, stock_code, keyword_filters):
    target_dir = os.path.join(download_dir, stock_code)
    os.makedirs(target_dir, exist_ok=True)
    print(f"--- Bắt đầu xử lý mã {stock_code} qua API ---")
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    })
    try:
        main_page_url = f"https://finance.vietstock.vn/{stock_code}/tai-tai-lieu.htm"
        print(f"Đang truy cập trang chính để lấy token...")
        main_page_response = session.get(main_page_url, timeout=30)
        main_page_response.raise_for_status()
        soup = BeautifulSoup(main_page_response.text, 'lxml')
        token = soup.find('input', {'name': '__RequestVerificationToken'}).get('value')
        print("✔️ Lấy token thành công!")

        api_url = "https://finance.vietstock.vn/data/getdocument"
        page = 1
        while True:
            payload = { "code": stock_code, "page": page, "type": 1, "__RequestVerificationToken": token }
            print(f"\nĐang yêu cầu dữ liệu trang {page}...")
            api_response = session.post(api_url, data=payload, timeout=30)
            reports = api_response.json()
            if not reports: break

            for report in reports:
                report_title = report.get('Title', '').strip()
                pdf_url = report.get('Url', '').strip()

                # !!! DÒNG DEBUG ĐƯỢC THÊM VÀO ĐÂY !!!
                # In ra tất cả các tiêu đề mà API trả về để chúng ta kiểm tra
                print(f"  [DEBUG] API trả về tiêu đề: {report_title}")

                if not report_title or not pdf_url: continue
                
                normalized_title = report_title.lower()
                if any(keyword.lower() in normalized_title for keyword in keyword_filters):
                    # ... (Phần code tải file sẽ không chạy vì không khớp) ...
                    # Nhưng chúng ta sẽ thấy được các tiêu đề thật sự là gì
                    pass
            page += 1
            time.sleep(1)
    except Exception as e:
        print(f"Lỗi nghiêm trọng khi xử lý mã {stock_code}: {e}")
    print(f"\n==================== Hoàn thành mã {code} ====================")

# --- HÀM THỰC THI CHÍNH ---
if __name__ == "__main__":
    for code in STOCK_CODES_TO_DOWNLOAD:
        download_reports_final_api("./downloads", code, KEYWORD_FILTERS)
        time.sleep(3)