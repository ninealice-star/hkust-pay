import streamlit as st
from datetime import datetime
import time

# --- 1. 頁面配置與自定義 CSS 樣式 ---
st.set_page_config(page_title="HKUST Deposit System", page_icon="✅", layout="wide")

def apply_styles():
    st.markdown("""
    <style>
        /* 頂部導航欄樣式 */
        .nav-bar { background-color: #003366; padding: 12px 60px; display: flex; justify-content: space-between; align-items: center; color: white; border-bottom: 4px solid #A6937C; }
        .system-title { border-left: 2px solid #fff; padding-left: 15px; margin-left: 15px; font-size: 18px; font-weight: 500; }
        
        /* 付款成功介面樣式 */
        .success-container { text-align: center; margin-top: 80px; font-family: Arial, sans-serif; }
        .check-icon { background-color: #28a745; color: white; width: 85px; height: 85px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 48px; margin-bottom: 25px; }
        .amount-main { color: #333; font-size: 42px; font-weight: bold; margin-bottom: 5px; }
        .amount-sub { color: #666; font-size: 18px; margin-bottom: 40px; }
        
        /* 正式發票樣式 */
        .receipt-box { 
            background: white; border: 1px solid #003366; padding: 40px; 
            max-width: 750px; margin: auto; position: relative;
            font-family: 'Arial'; color: #333; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .watermark { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-30deg); font-size: 80px; color: rgba(0, 51, 102, 0.03); pointer-events: none; white-space: nowrap; }
        .official-stamp { border: 2px solid #d32f2f; color: #d32f2f; padding: 8px; border-radius: 4px; display: inline-block; transform: rotate(-10deg); font-weight: bold; font-size: 13px; text-align: center; }
        .info-table { margin: auto; width: 480px; text-align: left; color: #444; font-size: 15px; border-collapse: collapse; }
        .info-table td { padding: 12px 0; border-bottom: 1px solid #eee; }
        
        /* 提醒文字樣式 */
        .deadline-notice { color: #d32f2f; font-weight: bold; font-size: 15px; border: 1px solid #f8d7da; background-color: #f8d7da; padding: 15px; border-radius: 5px; margin: 15px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 固定數據與狀態管理 ---
PAYER_NAME = "XINGSHENG WANG (王兴生)"
HKD_VAL = "51,643"
CNY_VAL = "45,000"

if 'step' not in st.session_state:
    st.session_state.step = "input"

apply_styles()

# --- 3. 頂部導航欄 (HKUST 官方風格) ---
st.markdown(f"""
<div class="nav-bar">
    <div style="display: flex; align-items: center;">
        <img src="https://hkust.edu.hk" height="48">
        <div class="system-title">Deposit System<br><span style="font-size:14px; font-weight:normal;">保證金系統</span></div>
    </div>
    <div style="font-size: 14px;">{PAYER_NAME} ▼</div>
</div>
""", unsafe_allow_html=True)

# --- 4. 頁面切換邏輯 ---

# [第一階段：付款確認頁面]
if st.session_state.step == "input":
    st.write("## ")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="background:white; padding:30px; border-radius:10px; border:1px solid #eee;">
            <h3 style="color:#003366;">Secure Payment Confirmation</h3>
            <p><b>Payer:</b> {PAYER_NAME}</p>
            <p><b>Payment Item:</b> Program Admission Deposit (MSc in TLE)</p>
            <p><b>Total Amount:</b> <span style="font-size:24px; color:#003366; font-weight:bold;">HK$ {HKD_VAL}</span> 
               <span style="color:#888; font-size:14px;">(≈ CNY {CNY_VAL})</span></p>
            <div class="deadline-notice">
                ⚠️ Urgent Notice:<br>
                Please complete the payment by 4:00 PM on April 24th. 
                Otherwise, your admission offer and place in the MSc in TLE program will be cancelled.
            </div>
            <p style="font-size:12px; color:#666; margin-top:10px;">By clicking confirm, you agree to the electronic payment terms of HKUST.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Confirm and Process Payment", use_container_width=True, type="primary"):
            st.session_state.step = "success"
            st.rerun()

# [第二階段：支付成功提示 (3秒自動跳轉)]
elif st.session_state.step == "success":
    st.markdown(f"""
    <div class="success-container">
        <div class="check-icon">✓</div>
        <div style="font-size:32px; font-weight:bold;">Successful payment</div>
        <div class="amount-main">HK$ {HKD_VAL}</div>
        <div class="amount-sub">≈ CNY {CNY_VAL}</div>
        <table class="info-table">
            <tr><td style="color:#888;">Payment Date:</td><td style="text-align:right;">{datetime.now().strftime('%d %B %Y')}</td></tr>
            <tr><td style="color:#888;">Payer:</td><td style="text-align:right;">{PAYER_NAME}</td></tr>
            <tr><td style="color:#888;">Status:</td><td style="text-align:right; color:#28a745; font-weight:bold;">Verified</td></tr>
            <tr><td style="color:#888;">Transaction Ref:</td><td style="text-align:right;">REF{int(time.time())}</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(3) # 停留3秒
    st.session_state.step = "receipt"
    st.rerun()

# [第三階段：正式發票下載頁面]
elif st.session_state.step == "receipt":
    st.write("## ")
    st.success("Transaction verified. Your official receipt has been generated below.")
    
    st.markdown(f"""
    <div class="receipt-box">
        <div class="watermark">OFFICIAL RECEIPT</div>
        <div style="text-align: center; border-bottom: 2px solid #003366; padding-bottom: 15px; margin-bottom: 20px;">
            <h2 style="margin:0; color:#003366;">THE HONG KONG UNIVERSITY OF SCIENCE AND TECHNOLOGY</h2>
            <p style="font-size:12px; margin-top:5px;">Clear Water Bay, Kowloon, Hong Kong | Finance Office</p>
        </div>
        <h3 style="text-align:center; text-decoration: underline;">OFFICIAL RECEIPT</h3>
        <br>
        <table style="width:100%; font-size:15px; border-collapse: collapse;">
            <tr><td style="padding:8px 0;"><b>Receipt No:</b></td><td style="text-align:right;">UST{int(time.time())}</td></tr>
            <tr><td style="padding:8px 0;"><b>Date of Issue:</b></td><td style="text-align:right;">{datetime.now().strftime('%d %B %Y')}</td></tr>
            <tr><td style="padding:8px 0;"><b>Received from:</b></td><td style="text-align:right;">{PAYER_NAME}</td></tr>
            <tr><td style="padding:8px 0;"><b>Description:</b></td><td style="text-align:right;">Program Admission Deposit (MSc in TLE, 2025-26 Fall)</td></tr>
        </table>
        <br><br>
        <div style="text-align:right; border-top: 1px solid #eee; padding-top: 15px;">
            <p style="font-size:20px; margin:0;"><b>TOTAL RECEIVED:</b> <span style="color:#003366;">HK$ {HKD_VAL}</span></p>
            <p style="font-size:14px; color:#666;">(Equivalent to CNY {CNY_VAL})</p>
        </div>
        <br>
        <div style="display: flex; justify-content: space-between; align-items: flex-end;">
            <div class="official-stamp">HKUST FINANCE OFFICE<br>PAYMENT VERIFIED<br>VALID DOCUMENT</div>
            <div style="font-size:10px; color:#888; text-align:right;">* Computer generated document.<br>No signature required.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Print / Save as PDF", use_container_width=True):
            st.info("Browser print dialog opening... Please select 'Save as PDF' in the destination.")

# --- 5. 頁尾 ---
st.markdown("<br><br><p style='text-align:center; color:#AAA; font-size:11px;'>Copyright © 2024 The Hong Kong University of Science and Technology. All rights reserved.</p>", unsafe_allow_html=True)
