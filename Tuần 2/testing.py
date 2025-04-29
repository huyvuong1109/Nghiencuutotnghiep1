import pandas as pd
# df = pd.read_csv("ex.csv", sep = ",", header = None, names = ["MaSo", "Ten", "Lop", "QueQuan"])
df = pd.read_csv("sinhvien.txt", sep = ",", header = None, names = ["MaSo", "Ten", "Lop", "QueQuan"])
# df1 = pd.read_excel("SinhvienExcel.xlsx", header= None)
# df2 = df.sort_values(['Lop'])
qq = ["Thai Nguyen", "Nam Dinh"]
df2 = df.query('QueQuan in @qq')
print(df2)