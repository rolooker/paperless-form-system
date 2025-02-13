import streamlit as st
import sqlite3
import pandas as pd

# SQLite Database Setup
# 初始化資料庫，建立 forms 資料表

def init_db():
    conn = sqlite3.connect('production_forms.db')  # 連接 SQLite 資料庫
    c = conn.cursor()

    # 建立新的資料表（僅當不存在時）
    c.execute('''CREATE TABLE IF NOT EXISTS forms
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT NOT NULL,
                  start_time TEXT NOT NULL,
                  end_time TEXT NOT NULL,
                  product TEXT NOT NULL,
                  quantity INTEGER NOT NULL,
                  signature TEXT NOT NULL,
                  notes TEXT)''')
    conn.commit()
    conn.close()

# 將表單資料寫入資料庫
def insert_form(date, start_time, end_time, product, quantity, signature, notes):
    conn = sqlite3.connect('production_forms.db')
    c = conn.cursor()
    c.execute("INSERT INTO forms (date, start_time, end_time, product, quantity, signature, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (date, start_time, end_time, product, quantity, signature, notes))
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

# 刪除指定表單紀錄
def delete_forms(selected_ids):
    conn = sqlite3.connect('production_forms.db')
    c = conn.cursor()
    for form_id in selected_ids:
        c.execute("DELETE FROM forms WHERE id = ?", (form_id,))
    conn.commit()
    conn.close()

# Streamlit 應用程式
st.title("📋 生產表單無紙化系統")

menu = ["填寫表單", "查看表單紀錄"]
choice = st.sidebar.selectbox("選擇操作", menu)

if choice == "填寫表單":
    st.header("✍️ 填寫生產表單")
    date = st.date_input("生產日期")

    col1, col2 = st.columns([1, 1])
    with col1:
        start_hour = st.selectbox("開始時間 (時)", list(range(0, 24)))
        start_minute = st.number_input("開始時間 (分)", min_value=0, max_value=59, step=1)
    with col2:
        end_hour = st.selectbox("結束時間 (時)", list(range(0, 24)))
        end_minute = st.number_input("結束時間 (分)", min_value=0, max_value=59, step=1)
    
    start_time = f"{start_hour:02d}:{start_minute:02d}"
    end_time = f"{end_hour:02d}:{end_minute:02d}"

    products = ["", "零零三 薄 透氧日拋隱形眼鏡", "純粹氧水潤高透氧矽水膠日拋隱形眼鏡", "真水感濾藍光清透日拋隱形眼鏡"]
    product = st.selectbox("品項名稱", products)

    quantity = st.number_input("生產數量", min_value=1, step=1)
    signature = st.text_input("人員電子簽名")
    notes = st.text_area("備註欄 (可選填)")

    if st.button("提交表單"):
        if not date:
            st.error("⚠️ 請選擇生產日期！")
        elif not product:
            st.error("⚠️ 請選擇品項名稱！")
        elif not quantity:
            st.error("⚠️ 請輸入生產數量！")
        elif not signature:
            st.error("⚠️ 請輸入人員電子簽名！")
        else:
            insert_form(date, start_time, end_time, product, quantity, signature, notes)
            st.success("✅ 表單已成功提交！")

elif choice == "查看表單紀錄":
    st.header("📊 表單紀錄")
    forms = get_forms()
    if forms:
        df = pd.DataFrame(forms, columns=["ID", "生產日期", "開始時間", "結束時間", "品項名稱", "生產數量", "人員簽名", "備註"])
        selected_rows = st.multiselect("選擇要刪除的資料", df.index, format_func=lambda x: f"ID {df.iloc[x, 0]} - {df.iloc[x, 4]}")
        if st.button("刪除選定的表單"):
            if selected_rows:
                delete_forms(df.iloc[selected_rows, 0].tolist())
                st.success("✅ 選定的表單已刪除！請重新整理頁面查看更新。")
            else:
                st.warning("⚠️ 請選擇要刪除的表單！")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8-sig')  # 使用 utf-8-sig 編碼
        st.download_button("📥 下載 CSV", csv, "forms_record.csv", "text/csv")
    else:
        st.info("目前尚無表單紀錄。")

# 初始化資料庫
init_db()
