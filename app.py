import streamlit as st
from datetime import datetime
import time

# --- 1. Page Config & CSS Fixes ---
st.set_page_config(page_title="HKUST Payment Portal", page_icon="✅", layout="wide")

# 統一 CSS 處理，避免在 markdown 中出現縮排
st.markdown("""
<style>
    /* 隱藏 Streamlit 官方元素 */
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
    
    /* 付款確認卡片 */
    .payment-card {
        background: white; 
        padding: 30px; 
        border-radius: 8px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
        border: 1px solid #eee;
    }
    
    /* 紅色提醒區塊 - 嚴格禁止縮排以免被誤認為代碼 */
    .deadline-box {
        color: #d32f2f; 
        font-weight: bold; 
        font-size: 15px; 
        background-color: #f8d7da; 
        padding: 15px; 
        border-radius: 4px; 
        margin: 15px 0;
        border: 1px solid #f5c6cb;
    }
    
    /* 正式收據 */
    .receipt-box { 
        background: white; border: 1px solid #003366; padding: 40px; 
        max-width: 750px; margin: auto; color: #333;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. Data & State ---
if 'step' not in st.session_state:
    st.session_state.step = "input"

PAYER = "XINGSHENG WANG"
HKD = "51,643"
CNY = "45,000"

# --- 3. Top Navigation (Logo Fix) ---
# 使用科大正式的白色透明 Logo
logo_url = "https://hkust.edu.hk"

st.markdown(f"""
<div class="nav-bar">
<img src="{logo_url}" height="45">
<div class="system-title">Deposit System<br><span style="font-size:12px; font-weight:normal;">Official Payment Portal</span></div>
</div>
""", unsafe_allow_html=True)

# --- 4. Logic Flow ---

# [STEP 1: Payment Confirmation]
if st.session_state.step == "input":
    st.write("## ")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # 使用不帶縮排的 HTML 字符串避免黑框
        html_content = f"""
<div class="payment-card">
<h2 style="color:#003366; margin-top:0;">Secure Payment Confirmation</h2>
<p style="margin:10px 0;"><b>Payer Name:</b> {PAYER}</p>
<p style="margin:10px 0;"><b>Payment Item:</b> Program Admission Deposit (MSc in TLE)</p>
<p style="margin:10px 0;"><b>Total Amount:</b> <span style="font-size:24px; color:#003366; font-weight:bold;">HK$ {HKD}</span> <span style="color:#888; font-size:14px;">(≈ CNY {CNY})</span></p>
<div class="deadline-box">
⚠️ URGENT NOTICE:<br>
Please complete the payment by 4:00 PM on April 24th. Failure to do so will result in the immediate cancellation of your admission offer and your place in the MSc in TLE program.
</div>
<p style="font-size:12px; color:#999; margin-top:15px;">By proceeding, you agree to the payment terms of HKUST Finance Office.</p>
</div>
"""
        st.markdown(html_content, unsafe_allow_html=True)
        
        if st.button("CONFIRM AND PROCESS PAYMENT", use_container_width=True, type="primary"):
            st.session_state.step = "success"
            st.rerun()

# [STEP 2: Success Splash]
elif st.session_state.step == "success":
    st.markdown(f"""
<div style="text-align:center; margin-top:100px;">
<div style="background:#28a745; color:white; width:80px; height:80px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:40px; margin-bottom:20px;">✓</div>
<h1 style="font-size:36px; color:#333;">Successful payment</h1>
<div style="font-size:42px; font-weight:bold; color:#003366;">HK$ {HKD}</div>
<div style="color:#666; font-size:18px; margin-bottom:40px;">≈ CNY {CNY}</div>
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
<h2 style="margin:0; color:#003366;">THE HONG KONG UNIVERSITY OF SCIENCE AND TECHNOLOGY</h2>
<p style="font-size:11px; margin-top:5px; color:#666;">Clear Water Bay, Kowloon, Hong Kong | Finance Office</p>
</div>
<h3 style="text-align:center; text-decoration: underline;">OFFICIAL RECEIPT</h3>
<br>
<table style="width:100%; font-size:14px; border-collapse: collapse;">
<tr><td style="padding:10px 0; border-bottom:1px solid #eee;"><b>Receipt No:</b></td><td style="text-align:right; border-bottom:1px solid #eee;">UST{int(time.time())}</td></tr>
<tr><td style="padding:10px 0; border-bottom:1px solid #eee;"><b>Date of Issue:</b></td><td style="text-align:right; border-bottom:1px solid #eee;">{datetime.now().strftime('%d %B %Y')}</td></tr>
<tr><td style="padding:10px 0; border-bottom:1px solid #eee;"><b>Received from:</b></td><td style="text-align:right; border-bottom:1px solid #eee;">{PAYER}</td></tr>
<tr><td style="padding:10px 0; border-bottom:1px solid #eee;"><b>Description:</b></td><td style="text-align:right; border-bottom:1px solid #eee;">Admission Deposit (MSc in TLE)</td></tr>
</table>
<br><br>
<div style="text-align:right;">
<p style="font-size:20px; margin:0;"><b>TOTAL RECEIVED:</b> <span style="color:#003366;">HK$ {HKD}</span></p>
<p style="font-size:14px; color:#777;">(Equivalent to CNY {CNY})</p>
</div>
<br>
<div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top:30px;">
<div style="border:2px solid #d32f2f; color:#d32f2f; padding:8px; font-weight:bold; transform:rotate(-5deg); text-align:center; font-size:13px;">HKUST FINANCE OFFICE<br>PAYMENT VERIFIED</div>
<div style="font-size:9px; color:#999;">* Computer-generated document. No signature required.</div>
</div>
</div>
""", unsafe_allow_html=True)
    st.write("")
    if st.button("PRINT / SAVE AS PDF", use_container_width=True):
        st.info("Please use 'Ctrl+P' to print or save this document.")

# --- Footer ---
st.markdown("<p style='text-align:center; color:#999; font-size:10px; margin-top:50px;'>© 2024 The Hong Kong University of Science and Technology. All rights reserved.</p>", unsafe_allow_html=True)
