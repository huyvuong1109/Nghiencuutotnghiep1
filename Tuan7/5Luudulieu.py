import sqlite3

def init_db():
    conn = sqlite3.connect("financial_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS financial_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_code TEXT,
            quarter TEXT,
            indicator TEXT,
            value TEXT
        )
    ''')
    conn.commit()
    return conn

def save_table_to_db(conn, stock_code, quarter, table_df):
    for index, row in table_df.iterrows():
        indicator = row[0]
        for col in row[1:]:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO financial_reports (stock_code, quarter, indicator, value)
                VALUES (?, ?, ?, ?)
            ''', (stock_code, quarter, indicator, col))
    conn.commit()

# Demo lưu dữ liệu
conn = init_db()
if tables:
    save_table_to_db(conn, "VNM", "Q4/2023", tables[0])
