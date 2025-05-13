import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # Gửi yêu cầu GET đến trang web
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra nếu có lỗi HTTP
    except requests.exceptions.RequestException as e:
        print(f"Không thể truy cập URL: {url}")
        print(f"Lỗi: {e}")
        return

    # Phân tích HTML trả về
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trích xuất thông tin từ các thẻ HTML cụ thể (ví dụ: tiêu đề trang)
    title = soup.title.string if soup.title else "Không tìm thấy tiêu đề"
    print(f"Tiêu đề trang: {title}")

    # Ví dụ: Tìm tất cả các thẻ <a> và in ra liên kết
    links = soup.find_all('a', href=True)
    print("\nCác liên kết trên trang:")
    for link in links:
        print(link['href'])

    # Bạn có thể thay đổi logic ở đây để cào dữ liệu cụ thể hơn
    # Ví dụ: Tìm tất cả các thẻ <p>
    paragraphs = soup.find_all('p')
    print("\nNội dung các thẻ <p>:")
    for p in paragraphs:
        print(p.text)

# URL của trang web cần cào
url = "https://finance.vietstock.vn/FPT/tai-tai-lieu.htm?doctype=1"  # Thay URL trang web bạn muốn cào
scrape_website(url)