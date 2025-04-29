import csv
# data = [
#     ['name', 'age', 'address'],
#     ['John', '28', 'NY'],
#     ['Alice', '40', 'SF'],
#     ['Bob', '25', 'LA']
# ]

# with open('ex.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer = writer.writerows(data)

with open('ex.csv', 'r') as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row)
data = [
    {'name': 'John', 'age': '28', 'address': 'NY'},
    {'name': 'Bob', 'age': '25', 'address': 'LA'}
]
with open('ex2.csv', 'w', newline='') as file:
    fieldNames = ['name', 'age', 'address']
    writer = csv.DictWriter(file, fieldnames= fieldNames)
    writer.writeheader()
    writer.writerows(data)
