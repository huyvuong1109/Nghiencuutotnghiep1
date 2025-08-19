import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)
        return all_tables

# Trích xuất và in thử 1 bảng
tables = extract_tables_from_pdf(pdf_file)
if tables:
    print(tables[0].head())
else:
    print("Không tìm thấy bảng.")
