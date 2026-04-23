import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# --- 資料庫邏輯 ---
def get_db_connection():
    conn = sqlite3.connect('hkust_system.db', check_same_thread=False)
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS payments 
                 (v_code TEXT PRIMARY KEY, payer TEXT, amount REAL, 
                  item TEXT, status TEXT, date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- HKUST 視覺風格 (CSS) ---
st.set_page_config(page_title="HKUST Payment & Receipt", page_icon="📜")
st.markdown("""
<style>
    .stApp { background-color: #f4f4f4; }
    .header { background-color: #003366; color: white; padding: 20px; text-align: center; border-bottom: 5px solid #996600; }
    .receipt-box { 
        background: white; border: 2px solid #003366; padding: 40px; 
        max-width: 600px; margin: auto; position: relative;
        font-family: 'Arial'; color: #333;
    }
    .receipt-watermark {
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-30deg);
        font-size: 80px; color: rgba(0, 51, 102, 0.05); white-space: nowrap; pointer-events: none;
    }
    .stamp {
        border: 3px solid #d32f2f; color: #d32f2f; padding: 5px 10px;
        border-radius: 5px; display: inline-block; transform: rotate(-10deg);
        font-weight: bold; border-style: double; font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# --- 側邊導航 ---
page = st.sidebar.radio("Navigation", ["Make Payment", "Download Receipt", "Admin Panel"])

# --- 1. 付款頁面 ---
if page == "Make Payment":
    st.markdown("<div class='header'><h1>HKUST Online Payment</h1></div><br>", unsafe_allow_html=True)
    with st.form("pay_form"):
        payer = st.text_input("Payer Full Name")
        amount = st.number_input("Amount (CNY/HKD)", min_value=1.0)
        item_name = st.selectbox("Payment Item", ["Tuition Deposit", "Activity Fee", "Application Fee"])
        submit = st.form_submit_button("Generate Payment Info")

        if submit and payer:
            v_code = f"UST{datetime.now().strftime('%m%d%H%M%S')}"
            conn = get_db_connection()
            conn.execute("INSERT INTO payments VALUES (?, ?, ?, ?, ?, ?)", 
                         (v_code, payer, amount, item_name, "Confirmed", datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            st.success(f"Payment successful! Your Receipt Code is: {v_code}")
            st.info("Please go to 'Download Receipt' and enter this code.")

# --- 2. 電子收據生成頁面 ---
elif page == "Download Receipt":
    st.markdown("<h2 style='color:#003366; text-align:center;'>Official Electronic Receipt</h2>", unsafe_allow_html=True)
    search_code = st.text_input("Enter your Receipt Code (e.g. UST1234...)")
    
    if search_code:
        conn = get_db_connection()
        data = conn.execute("SELECT * FROM payments WHERE v_code=?", (search_code,)).fetchone()
        
        if data:
            # 收據 HTML 模板
            st.markdown(f"""
            <div class="receipt-box">
                <div class="receipt-watermark">HKUST HKUST HKUST</div>
                <div style="text-align: center; border-bottom: 1px solid #ddd; padding-bottom: 10px;">
                    <h3 style="margin:0; color:#003366;">OFFICIAL RECEIPT</h3>
                    <p style="font-size:12px;">The Hong Kong University of Science and Technology</p>
                </div>
                <br>
                <table style="width:100%; font-size:14px;">
                    <tr><td><b>Receipt No:</b></td><td>{data[0]}</td></tr>
                    <tr><td><b>Date:</b></td><td>{data[5]}</td></tr>
                    <tr><td><b>Payer:</b></td><td>{data[1]}</td></tr>
                    <tr><td><b>Description:</b></td><td>{data[3]}</td></tr>
                </table>
                <hr style="border:0.5px solid #eee;">
                <div style="text-align:right;">
                    <p style="font-size:18px;"><b>TOTAL PAID:</b> <span style="color:#003366;">${data[2]}</span></p>
                </div>
                <br>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div class="stamp">FINANCE OFFICE<br>PAID</div>
                    <div style="font-size:10px; color:#888;">* This is a computer-generated document. <br>No signature is required.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.button("Print / Save as PDF (Ctrl+P)")
        else:
            st.error("Receipt Code not found.")

# --- 3. 後台管理 ---
elif page == "Admin Panel":
    pwd = st.sidebar.text_input("Password", type="password")
    if pwd == "ustadmin":
        st.write("### Transaction Management")
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM payments", conn)
        st.dataframe(df)
        if st.button("Clear Records"):
            conn.execute("DELETE FROM payments")
            conn.commit()
            st.experimental_rerun()

st.markdown("<p style='text-align:center; color:#999; font-size:10px; margin-top:100px;'>Copyright © 2024 HKUST. All rights reserved.</p>", unsafe_allow_html=True)
