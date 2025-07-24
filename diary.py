
from pathlib import Path

file_path = Path('diary.txt')

print("请输入日记内容（单独输入空行结束）：")
lines = []
while True:
    line = input()
    if line == '':
        break
    lines.append(line + '\n')

# 写入
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

# 读回
with open(file_path, 'r', encoding='utf-8') as f:
    print("\n----- 日记内容 -----")
    print(f.read(), end='')