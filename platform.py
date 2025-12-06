# energy_micro_platform.py
import sqlite3, datetime, json, pandas as pd
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import streamlit as st
import requests, time

DB_FILE = "energy_platform.db"

# ---------- 1. 本地 SQLite 初始化 ----------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS bids (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    side TEXT CHECK(side IN ('buy','sell')),
                    user TEXT,
                    qty_kwh INTEGER,
                    price_yuan REAL,
                    ts TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS deals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    buyer TEXT,
                    seller TEXT,
                    qty_kwh INTEGER,
                    price_yuan REAL,
                    ts TEXT)""")
    conn.commit(); conn.close()
init_db()

# ---------- 2. 撮合引擎（双边拍卖） ----------
def match_orders() -> List[dict]:
    conn = sqlite3.connect(DB_FILE)
    bids = pd.read_sql("SELECT * FROM bids ORDER BY id", conn)
    if bids.empty:
        conn.close(); return []
    buys = bids[bids.side=='buy'].sort_values('price_yuan', ascending=False)
    sells = bids[bids.side=='sell'].sort_values('price_yuan', ascending=True)
    deals = []
    while not buys.empty and not sells.empty and buys.iloc[0].price_yuan >= sells.iloc[0].price_yuan:
        b, s = buys.iloc[0], sells.iloc[0]
        qty = min(b.qty_kwh, s.qty_kwh)
        price = round((b.price_yuan + s.price_yuan)/2, 3)
        deals.append({"buyer": b.user, "seller": s.user, "qty_kwh": qty, "price_yuan": price, "ts": datetime.datetime.utcnow().isoformat()})
        # 扣除数量
        if b.qty_kwh > qty:
            c = conn.cursor()
            c.execute("UPDATE bids SET qty_kwh = qty_kwh - ? WHERE id = ?", (qty, b.id))
        else:
            c.execute("DELETE FROM bids WHERE id = ?", (b.id,))
        if s.qty_kwh > qty:
            c.execute("UPDATE bids SET qty_kwh = qty_kwh - ? WHERE id = ?", (qty, s.id))
        else:
            c.execute("DELETE FROM bids WHERE id = ?", (s.id,))
        conn.commit()
        buys = pd.read_sql("SELECT * FROM bids WHERE side='buy' ORDER BY price_yuan DESC", conn)
        sells = pd.read_sql("SELECT * FROM bids WHERE side='sell' ORDER BY price_yuan ASC", conn)
    # 保存成交
    for d in deals:
        conn.execute("INSERT INTO deals (buyer,seller,qty_kwh,price_yuan,ts) VALUES (?,?,?,?,?)",
                     (d["buyer"], d["seller"], d["qty_kwh"], d["price_yuan"], d["ts"]))
    conn.commit(); conn.close()
    return deals

# ---------- 3. FastAPI 接口 ----------
app = FastAPI(title="PyEnergyMicro")

class Order(BaseModel):
    side: str   # buy or sell
    user: str
    qty_kwh: int
    price_yuan: float

@app.post("/order")
def submit_order(order: Order):
    if order.side not in ("buy","sell"):
        raise HTTPException(status_code=400, detail="side must be buy or sell")
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT INTO bids (side,user,qty_kwh,price_yuan,ts) VALUES (?,?,?,?,?)",
                 (order.side, order.user, order.qty_kwh, order.price_yuan, datetime.datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    return {"status": "received"}

@app.post("/match")
def run_match():
    deals = match_orders()
    for d in deals:
        save_to_chain(d)   # 目前只是打印，可替换为 fabric-sdk
    return {"deals": deals}

@app.get("/orders")
def list_orders():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM bids ORDER BY id DESC LIMIT 100", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/deals")
def list_deals():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM deals ORDER BY id DESC LIMIT 100", conn)
    conn.close()
    return df.to_dict(orient="records")

# ---------- 4. 链上存证（Mock） ----------
def save_to_chain(deal: dict):
    # TODO: 换成 fabric-sdk: client.submit_transaction(...)
    print("[Chain-Mock] Saved deal:", json.dumps(deal, ensure_ascii=False))

# ---------- 5. Streamlit 看板 ----------
st.set_page_config(page_title="PyEnergyMicro 看板")
st.title("🌞 分布式能源微型交易平台 (纯 Python Demo)")

st.header("1. 提交订单")
with st.form("order_form"):
    side = st.selectbox("类型", ("buy", "sell"))
    user = st.text_input("用户", "UserA")
    qty = st.number_input("电量 kWh", 1, 1000, 50)
    price = st.number_input("价格 元/kWh", 0.0, 2.0, 0.7, 0.01)
    submitted = st.form_submit_button("下单")
    if submitted:
        r = requests.post("http://localhost:8000/order", json={"side": side, "user": user, "qty_kwh": qty, "price_yuan": price})
        st.success("下单成功！" if r.status_code == 200 else r.text)

st.header("2. 一键撮合")
if st.button("开始撮合"):
    r = requests.post("http://localhost:8000/match")
    deals = r.json()["deals"]
    st.write(f"成交笔数: {len(deals)}")
    if deals:
        st.dataframe(pd.DataFrame(deals))

st.header("3. 实时订单 & 成交")
col1, col2 = st.columns(2)
with col1:
    st.subheader("当前挂单")
    df_o = pd.DataFrame(requests.get("http://localhost:8000/orders").json())
    st.dataframe(df_o)
with col2:
    st.subheader("历史成交")
    df_d = pd.DataFrame(requests.get("http://localhost:8000/deals").json())
    st.dataframe(df_d)

# 自动刷新
time.sleep(5)
st.experimental_rerun()