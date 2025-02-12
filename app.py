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
                  name TEXT NOT NULL,
                  date TEXT NOT NULL,
                  product TEXT NOT NULL,
                  quantity INTEGER NOT NULL)''')  # 建立表單資料表
    conn.commit()
    conn.close()

# 將表單資料寫入資料庫
def insert_form(name, date, product, quantity):
    conn = sqlite3.connect('production_forms.db')
    c = conn.cursor()
    c.execute("INSERT INTO forms (name, date, product, quantity) VALUES (?, ?, ?, ?)",
              (name, date, product, quantity))
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
    name = st.text_input("姓名")
    date = st.date_input("日期")
    product = st.text_input("產品名稱")
    quantity = st.number_input("數量", min_value=1)

    if st.button("提交表單"):
        if name and product:
            insert_form(name, date, product, quantity)
            st.success("✅ 表單已成功提交！")
        else:
            st.warning("⚠️ 請完整填寫所有欄位！")

elif choice == "查看表單紀錄":
    st.header("📊 表單紀錄")
    forms = get_forms()
    if forms:
        df = pd.DataFrame(forms, columns=["ID", "姓名", "日期", "產品名稱", "數量"])
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 下載 CSV", csv, "forms_record.csv", "text/csv")
    else:
        st.info("目前尚無表單紀錄。")

# 初始化資料庫
init_db()
