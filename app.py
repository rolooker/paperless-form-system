import streamlit as st
import sqlite3
import pandas as pd

# SQLite Database Setup
# 初始化資料庫，建立 forms 資料表
def init_db():
    conn = sqlite3.connect('production_forms.db')  # 連接 SQLite 資料庫
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS forms
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT NOT NULL,
                  time TEXT NOT NULL,
                  product TEXT NOT NULL,
                  quantity INTEGER NOT NULL,
                  signature TEXT NOT NULL,
                  notes TEXT)''')  # 建立表單資料表
    conn.commit()
    conn.close()

# 將表單資料寫入資料庫
def insert_form(date, time, product, quantity, signature, notes):
    conn = sqlite3.connect('production_forms.db')
    c = conn.cursor()
    c.execute("INSERT INTO forms (date, time, product, quantity, signature, notes) VALUES (?, ?, ?, ?, ?, ?)",
              (date, time, product, quantity, signature, notes))
    conn.commit()
    conn.close()

# 查詢所有表單紀錄
def get_forms():
    conn = sqlite3.connect('production_forms.db')
    c = conn.cursor()
    c.execute("SELECT * FROM forms")
    forms = c.fetchall()
    conn.close()
    return forms

# Streamlit 應用程式
st.title("📋 生產表單無紙化系統")

menu = ["填寫表單", "查看表單紀錄"]
choice = st.sidebar.selectbox("選擇操作", menu)

if choice == "填寫表單":
    st.header("✍️ 填寫生產表單")
    date = st.date_input("生產日期")
    hour = st.selectbox("時", list(range(0, 24)))
    minute = st.selectbox("分", list(range(0, 60, 5)))  # 以 5 分鐘為間隔
    time = f"{hour:02d}:{minute:02d}"

    products = [
        "零零三 薄 透氧日拋隱形眼鏡",
        "純粹氧水潤高透氧矽水膠日拋隱形眼鏡",
        "真水感濾藍光清透日拋隱形眼鏡"
    ]
    product = st.selectbox("品項名稱", products)

    quantity = st.number_input("生產數量", min_value=1)
    signature = st.text_input("人員電子簽名")
    notes = st.text_area("備註欄")

    if st.button("提交表單"):
        if signature and product and quantity:
            insert_form(date, time, product, quantity, signature, notes)
            st.success("✅ 表單已成功提交！")
        else:
            st.warning("⚠️ 請完整填寫所有欄位！")

elif choice == "查看表單紀錄":
    st.header("📊 表單紀錄")
    forms = get_forms()
    if forms:
        df = pd.DataFrame(forms, columns=["ID", "生產日期", "時間", "品項名稱", "生產數量", "人員簽名", "備註"])
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 下載 CSV", csv, "forms_record.csv", "text/csv")
    else:
        st.info("目前尚無表單紀錄。")

# 初始化資料庫
init_db()
