import csv
from pathlib import Path

VAULT = Path.home() / ".contacts.csv"   # 存到用户目录
if not VAULT.exists():
    VAULT.write_text("name,phone\n", encoding='utf-8')

def _load():
    with open(VAULT, newline='', encoding='utf-8') as f:
        return {row['name']: row['phone'] for row in csv.DictReader(f)}

def _save(data):
    with open(VAULT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'phone'])
        writer.writerows(data.items())

def add(name, phone):
    data = _load()
    data[name] = phone
    _save(data)
    print(f"✅ Added {name}: {phone}")

def query(name):
    data = _load()
    print(data.get(name, "❌ Not found"))

def list_all():
    data = _load()
    if not data:
        print("📭 Empty")
    else:
        for n, p in data.items():
            print(f"{n}: {p}")

def delete(name):
    data = _load()
    if name in data:
        del data[name]
        _save(data)
        print(f" Deleted {name}")
    else:
        print(" Not found")