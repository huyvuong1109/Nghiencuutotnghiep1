import os
import requests

def download_pdf(url, save_dir="pdf_reports"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    file_name = url.split("/")[-1]
    response = requests.get(url)
    file_path = os.path.join(save_dir, file_name)

    with open(file_path, "wb") as f:
        f.write(response.content)
    
    return file_path

# Tải 1 file mẫu
pdf_file = download_pdf(links[0])
print(f"PDF saved at: {pdf_file}")
