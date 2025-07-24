# 列出当前目录下所有 .py 文件并打印绝对路径
from pathlib import Path

current = Path.cwd()
py_files = current.glob('*.py')

for py in py_files:
    print(py.resolve())