
"""
密码保险箱 v1.0 —— CSV 持久化
功能：增 / 查 / 列 / 删
"""
import csv
from pathlib import Path

VAULT = Path('vault.csv')

# 确保文件存在且有表头
if not VAULT.exists():
    VAULT.write_text('site,user,password\n', encoding='utf-8')


def load_vault():
    """返回 list[dict]"""
    with open(VAULT, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def save_vault(rows):
    with open(VAULT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['site', 'user', 'password'])
        writer.writeheader()
        writer.writerows(rows)
def add_account():
    site = input("网站：").strip()
    user = input("用户名：").strip()
    pwd = input("密码：").strip()
    rows = load_vault()
    rows.append({'site': site, 'user': user, 'password': pwd})
    save_vault(rows)
    print("✅ 已保存！")


def query_password():
    site = input("查询网站：").strip()
    rows = load_vault()
    for row in rows:
        if row['site'].lower() == site.lower():
            print(f"用户名：{row['user']}，密码：{row['password']}")
            return
    print("❌ 未找到该网站。")


def list_all():
    rows = load_vault()
    if not rows:
        print("📭 保险箱为空")
        return
    print("{:<20} {:<15} {:<15}".format("网站", "用户名", "密码"))
    print("-" * 55)
    for r in rows:
        print("{:<20} {:<15} {:<15}".format(r['site'], r['user'], r['password']))


def delete_account():
    site = input("删除网站：").strip()
    rows = load_vault()
    new_rows = [r for r in rows if r['site'].lower() != site.lower()]
    if len(new_rows) == len(rows):
        print("❌ 未找到该网站。")
    else:
        save_vault(new_rows)
        print("✅ 已删除！")


def main():
    menu = """
=== 密码保险箱 ===
1) 新增账号
2) 查询密码
3) 列出全部
4) 删除账号
0) 退出
请选择："""
    while True:
        choice = input(menu).strip()
        if choice == '1':
            add_account()
        elif choice == '2':
            query_password()
        elif choice == '3':
            list_all()
        elif choice == '4':
            delete_account()
        elif choice == '0':
            print("👋 再见！")
            break
        else:
            print("❌ 无效选项，请重试！")


if __name__ == "__main__":
    main()