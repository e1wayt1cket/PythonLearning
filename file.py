from pathlib import Path

file_path = Path('sample.txt')
if not file_path.exists():
    print("sample.txt 不存在，已自动生成示例文件。")
    file_path.write_text("Hello world!\n\nPython is great.\n", encoding='utf-8')

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

total_lines = len(lines)
empty_lines = sum(1 for line in lines if line.strip() == '')
total_chars = sum(len(line) for line in lines)

print(f"总行数: {total_lines}")
print(f"空行数: {empty_lines}")
print(f"总字符数: {total_chars}")
