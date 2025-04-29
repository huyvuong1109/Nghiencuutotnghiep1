def get_data(conn, stock_code):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT quarter, indicator, value FROM financial_reports
        WHERE stock_code = ?
    ''', (stock_code,))
    results = cursor.fetchall()
    for row in results:
        print(row)

get_data(conn, "VNM")
