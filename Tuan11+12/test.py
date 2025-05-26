import os

def is_file_in_directory(file_path, directory):
    file_path = os.path.abspath(file_path)
    directory = os.path.abspath(directory)
    print("File path:", file_path)
    print("Folder path:", directory)
    return os.path.commonpath([file_path, directory]) == directory

# Ví dụ sử dụng:
file_to_check = r"D:\Downloads\UCITSS.docx"
folder = r"D:\Downloads"

if is_file_in_directory(file_to_check, folder):
    print("✅ File nằm trong thư mục.")
else:
    print("❌ File KHÔNG nằm trong thư mục.")
