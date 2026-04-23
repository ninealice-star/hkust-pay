import streamlit as st
from datetime import datetime
import time

# --- 1. Page Config & CSS Fixes (Forcing Text Visibility) ---
st.set_page_config(page_title="HKUST Payment Portal", page_icon="✅", layout="wide")

st.markdown("""
<style>
    /* 隱藏 Streamlit 官方組件 */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stHeader"] {display: none;}
    
    /* 頂部導航欄 */
    .nav-bar { 
        background-color: #003366; 
        padding: 15px 60px; 
        display: flex; 
        align-items: center; 
        color: white; 
        border-bottom: 4px solid #A6937C;
    }
    .system-title { 
        border-left: 2px solid #fff; 
        padding-left: 15px; 
        margin-left: 15px; 
        font-size: 18px; 
        font-weight: 500; 
        line-height: 1.2;
    }
    
    /* 付款確認卡片 - 強制所有文字為黑色 */
    .payment-card {
        background-color: #FFFFFF !important; 
        padding: 40px; 
        border-radius: 8px; 
        box-shadow: 0 4px 20px rgba(0,0,0,0.1); 
        border: 1px solid #ddd;
        color: #000000 !important;
    }
    .payment-card p, .payment-card b, .payment-card span {
        color: #000000 !important;
    }
    
    /* 紅色提醒區塊 */
    .deadline-box {
        color: #d32f2f !important; 
        font-weight: bold; 
        font-size: 15px; 
        background-color: #f8d7da !important; 
        padding: 18px; 
        border-radius: 4px; 
        margin: 20px 0;
        border: 1px solid #f5c6cb;
        line-height: 1.5;
    }
    
    /* 正式收據 */
    .receipt-box { 
        background-color: #FFFFFF !important; 
        border: 1px solid #003366; 
        padding: 40px; 
        max-width: 750px; 
        margin: auto; 
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. Data & State ---
if 'step' not in st.session_state:
    st.session_state.step = "input"

PAYER = "XINGSHENG WANG"
HKD = "51,643"
CNY = "45,000"

# --- 3. Top Navigation (Clean HKUST Logo) ---
logo_white = "https://hkust.edu.hk"

st.markdown(f"""
<div class="nav-bar">
<img src="{logo_white}" height="45">
<div class="system-title">Deposit System<br><span style="font-size:12px; font-weight:normal;">Official Payment Portal</span></div>
</div>
""", unsafe_allow_html=True)

# --- 4. Logic Flow ---

# [STEP 1: Payment Confirmation]
if st.session_state.step == "input":
    st.write("## ")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # 這裡的 HTML 完全不縮進，防止被 Streamlit 誤認為代碼塊
        html_body = f"""
<div class="payment-card">
<h2 style="color:#003366 !important; margin-top:0; border-bottom: 1px solid #eee; padding-bottom: 10px;">Secure Payment Confirmation</h2>
<p style="margin:20px 0; font-size:16px;"><b>Payer Name:</b> {PAYER}</p>
<p style="margin:20px 0; font-size:16px;"><b>Payment Item:</b> Program Admission Deposit (MSc in TLE)</p>
<p style="margin:20px 0; font-size:16px;"><b>Total Amount:</b> <span style="font-size:26px; color:#003366 !important; font-weight:bold;">HK$ {HKD}</span> <span style="color:#666 !important; font-size:14px; margin-left:5px;">(≈ CNY {CNY})</span></p>
<div class="deadline-box">
⚠️ URGENT NOTICE:<br>
Please complete the payment by 4:00 PM on April 24th. Failure to do so will result in the immediate cancellation of your admission offer and your place in the MSc in TLE program.
</div>
<p style="font-size:12px; color:#888 !important; margin-top:20px;">By proceeding, you agree to the payment terms of HKUST Finance Office.</p>
</div>
"""
        st.markdown(html_body, unsafe_allow_html=True)
        
        st.write("")
        if st.button("CONFIRM AND PROCESS PAYMENT", use_container_width=True, type="primary"):
            st.session_state.step = "success"
            st.rerun()

# [STEP 2: Success Screen]
elif st.session_state.step == "success":
    st.markdown(f"""
<div style="text-align:center; margin-top:100px;">
<div style="background:#28a745; color:white; width:85px; height:85px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:45px; margin-bottom:25px;">✓</div>
<h1 style="font-size:38px; color:#333 !important;">Successful payment</h1>
<div style="font-size:48px; font-weight:bold; color:#003366 !important;">HK$ {HKD}</div>
<div style="color:#666 !important; font-size:20px; margin-bottom:40px;">≈ CNY {CNY}</div>
<p style="color:#999 !important;">Redirecting to your official receipt...</p>
</div>
""", unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.step = "receipt"
    st.rerun()

# [STEP 3: Official Receipt]
elif st.session_state.step == "receipt":
    st.write("## ")
    st.markdown(f"""
<div class="receipt-box">
<div style="text-align: center; border-bottom: 2px solid #003366; padding-bottom: 15px; margin-bottom: 25px;">
<h2 style="margin:0; color:#003366 !important;">THE HONG KONG UNIVERSITY OF SCIENCE AND TECHNOLOGY</h2>
<p style="font-size:11px; margin-top:5px; color:#666 !important;">Clear Water Bay, Kowloon, Hong Kong | Finance Office</p>
</div>
<h3 style="text-align:center; text-decoration: underline; color:#000 !important;">OFFICIAL RECEIPT</h3>
<br>
<table style="width:100%; font-size:14px; border-collapse: collapse; color:#000 !important;">
<tr><td style="padding:12px 0; border-bottom:1px solid #eee;"><b>Receipt No:</b></td><td style="text-align:right; border-bottom:1px solid #eee;">UST{int(time.time())}</td></tr>
<tr><td style="padding:12px 0; border-bottom:1px solid #eee;"><b>Date of Issue:</b></td><td style="text-align:right; border-bottom:1px solid #eee;">{datetime.now().strftime('%d %B %Y')}</td></tr>
<tr><td style="padding:12px 0; border-bottom:1px solid #eee;"><b>Received from:</b></td><td style="text-align:right; border-bottom:1px solid #eee;">{PAYER}</td></tr>
<tr><td style="padding:12px 0; border-bottom:1px solid #eee;"><b>Description:</b></td><td style="text-align:right; border-bottom:1px solid #eee;">Admission Deposit (MSc in TLE)</td></tr>
</table>
<br><br>
<div style="text-align:right;">
<p style="font-size:22px; margin:0; color:#000 !important;"><b>TOTAL RECEIVED:</b> <span style="color:#003366 !important;">HK$ {HKD}</span></p>
<p style="font-size:14px; color:#666 !important;">(Equivalent to CNY {CNY})</p>
</div>
<br>
<div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top:30px;">
<div style="border:2px solid #d32f2f; color:#d32f2f !important; padding:10px; font-weight:bold; transform:rotate(-5deg); text-align:center; font-size:13px;">HKUST FINANCE OFFICE<br>PAYMENT VERIFIED</div>
<div style="font-size:9px; color:#999 !important;">* Computer-generated document. No signature required.</div>
</div>
</div>
""", unsafe_allow_html=True)
    st.write("")
    if st.button("PRINT / SAVE AS PDF", use_container_width=True):
        st.info("Please use 'Ctrl+P' to print or save this document.")

# --- Footer ---
st.markdown("<p style='text-align:center; color:#999 !important; font-size:10px; margin-top:50px;'>© 2024 The Hong Kong University of Science and Technology. All rights reserved.</p>", unsafe_allow_html=True)
