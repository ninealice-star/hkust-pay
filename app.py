import streamlit as st
from datetime import datetime
import time

# --- 1. Page Config & CSS (Strong Fixes) ---
st.set_page_config(page_title="HKUST Deposit System", page_icon="✅", layout="wide")

def apply_clean_styles():
    st.markdown("""
    <style>
        /* Hide Streamlit elements on the top right */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Top Navigation Bar */
        .nav-bar { 
            background-color: #003366; 
            padding: 15px 60px; 
            display: flex; 
            justify-content: flex-start; 
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
        }
        
        /* Success Screen */
        .success-container { text-align: center; margin-top: 80px; font-family: Arial, sans-serif; }
        .check-icon { background-color: #28a745; color: white; width: 85px; height: 85px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 48px; margin-bottom: 25px; }
        
        /* Receipt Box */
        .receipt-box { 
            background: white; border: 1px solid #003366; padding: 40px; 
            max-width: 750px; margin: auto; position: relative;
            font-family: 'Arial'; color: #333;
        }
        .watermark { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-30deg); font-size: 80px; color: rgba(0, 51, 102, 0.03); pointer-events: none; }
        .official-stamp { border: 2px solid #d32f2f; color: #d32f2f; padding: 8px; border-radius: 4px; display: inline-block; transform: rotate(-10deg); font-weight: bold; font-size: 13px; text-align: center; }
        
        /* Notice Box */
        .deadline-notice { 
            color: #d32f2f; font-weight: bold; font-size: 15px; 
            border: 1px solid #f8d7da; background-color: #f8d7da; 
            padding: 15px; border-radius: 5px; margin: 15px 0; 
        }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Fixed Data ---
PAYER_NAME = "XINGSHENG WANG"
HKD_VAL = "51,643"
CNY_VAL = "45,000"

if 'step' not in st.session_state:
    st.session_state.step = "input"

apply_clean_styles()

# --- 3. Clean Top Navigation (Logo + Title Only) ---
st.markdown(f"""
<div class="nav-bar">
    <img src="https://hkust.edu.hk" height="40">
    <div class="system-title">
        Deposit System<br>
        <span style="font-size:12px; font-weight:normal;">Online Payment Portal</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 4. Content Logic ---

# [STEP 1: English Payment Confirmation]
if st.session_state.step == "input":
    st.write("## ")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"""
        <div style="background:white; padding:35px; border-radius:10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border:1px solid #eee;">
            <h2 style="color:#003366; margin-top:0;">Secure Payment Confirmation</h2>
            <p style="margin:10px 0;"><b>Payer:</b> {PAYER_NAME}</p>
            <p style="margin:10px 0;"><b>Item:</b> Admission Deposit (MSc in TLE)</p>
            <p style="margin:10px 0;"><b>Total Amount:</b> <span style="font-size:24px; color:#003366; font-weight:bold;">HK$ {HKD_VAL}</span> 
               <span style="color:#888; font-size:14px;">(≈ CNY {CNY_VAL})</span></p>
            
            <div class="deadline-notice">
                ⚠️ URGENT NOTICE:<br>
                Please complete the payment by 4:00 PM on April 24th. 
                Failure to do so will result in the cancellation of your admission offer and your place in the MSc in TLE program.
            </div>
            
            <p style="font-size:12px; color:#999; margin-top:20px;">By clicking the button below, you authorize the transaction to HKUST Finance Office.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("CONFIRM AND PROCESS PAYMENT", use_container_width=True, type="primary"):
            st.session_state.step = "success"
            st.rerun()

# [STEP 2: Success Screen]
elif st.session_state.step == "success":
    st.markdown(f"""
    <div class="success-container">
        <div class="check-icon">✓</div>
        <h1 style="font-size:36px;">Successful payment</h1>
        <div style="font-size:42px; font-weight:bold;">HK$ {HKD_VAL}</div>
        <div style="color:#666; font-size:18px; margin-bottom:40px;">≈ CNY {CNY_VAL}</div>
        <table style="margin:auto; width:450px; text-align:left; color:#666; border-collapse: collapse;">
            <tr style="border-bottom:1px solid #eee;"><td style="padding:10px 0;">Payment Date:</td><td style="text-align:right; color:#333;">{datetime.now().strftime('%d %b %Y')}</td></tr>
            <tr style="border-bottom:1px solid #eee;"><td style="padding:10px 0;">Payer:</td><td style="text-align:right; color:#333;">{PAYER_NAME}</td></tr>
            <tr><td style="padding:10px 0;">Transaction Ref:</td><td style="text-align:right; color:#333;">REF{int(time.time())}</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(3)
    st.session_state.step = "receipt"
    st.rerun()

# [STEP 3: Official English Receipt]
elif st.session_state.step == "receipt":
    st.write("## ")
    st.markdown(f"""
    <div class="receipt-box">
        <div class="watermark">OFFICIAL RECEIPT</div>
        <div style="text-align: center; border-bottom: 2px solid #003366; padding-bottom: 15px; margin-bottom: 20px;">
            <h2 style="margin:0; color:#003366;">THE HONG KONG UNIVERSITY OF SCIENCE AND TECHNOLOGY</h2>
            <p style="font-size:11px; margin-top:5px;">Clear Water Bay, Kowloon, Hong Kong | Finance Office</p>
        </div>
        <h3 style="text-align:center; text-decoration: underline;">OFFICIAL RECEIPT</h3>
        <br>
        <table style="width:100%; font-size:14px; border-collapse: collapse;">
            <tr><td style="padding:8px 0;"><b>Receipt No:</b></td><td style="text-align:right;">UST{int(time.time())}</td></tr>
            <tr><td style="padding:8px 0;"><b>Date of Issue:</b></td><td style="text-align:right;">{datetime.now().strftime('%d %B %Y')}</td></tr>
            <tr><td style="padding:8px 0;"><b>Received from:</b></td><td style="text-align:right;">{PAYER_NAME}</td></tr>
            <tr><td style="padding:8px 0;"><b>Description:</b></td><td style="text-align:right;">Program Admission Deposit (MSc in TLE)</td></tr>
        </table>
        <br><br>
        <div style="text-align:right; border-top: 1px solid #eee; padding-top: 15px;">
            <p style="font-size:20px; margin:0;"><b>TOTAL RECEIVED:</b> <span style="color:#003366;">HK$ {HKD_VAL}</span></p>
            <p style="font-size:13px; color:#666;">(Equivalent to CNY {CNY_VAL})</p>
        </div>
        <br>
        <div style="display: flex; justify-content: space-between; align-items: flex-end;">
            <div class="official-stamp">HKUST FINANCE OFFICE<br>PAYMENT VERIFIED<br>OFFICIAL DOCUMENT</div>
            <div style="font-size:9px; color:#999; text-align:right;">* This is a computer-generated document.<br>No signature is required.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("PRINT RECEIPT / SAVE AS PDF", use_container_width=True):
        st.info("Please use your browser's Print function (Ctrl+P).")

# --- 5. Footer ---
st.markdown("<br><br><p style='text-align:center; color:#BBB; font-size:10px;'>Copyright © 2024 The Hong Kong University of Science and Technology. All rights reserved.</p>", unsafe_allow_html=True)
