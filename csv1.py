# 将列表写入 students.csv 并读回
import csv
from pathlib import Path

students = [['Alice', 90], ['Bob', 85]]
file_path = Path('students.csv')

# 写入
with open(file_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'score'])
    writer.writerows(students)

# 读回
with open(file_path, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)