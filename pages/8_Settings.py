# Redirect to original Settings
import streamlit as st
import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Settings | SOC", page_icon="S", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .settings-card { background: rgba(26, 31, 46, 0.8); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

from auth.auth_manager import check_auth, show_user_info

user = check_auth()
if not user:
    st.switch_page("pages/0_Login.py")
    st.stop()

show_user_info(user)

st.markdown("# Settings")
st.markdown("Configure SOC integrations and notifications")
st.markdown("---")

CONFIG_FILE = ".soc_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

config = load_config()

tab1, tab2, tab3, tab4 = st.tabs(["API Keys", "Notifications", "Thresholds", "About"])

with tab1:
    st.markdown("### API Keys")
    
    gemini_key = st.text_input("Google Gemini API Key", value=config.get("gemini_api_key", ""), type="password")
    vt_key = st.text_input("VirusTotal API Key", value=config.get("virustotal_api_key", ""), type="password")
    
    if st.button("Save API Keys", type="primary"):
        config["gemini_api_key"] = gemini_key
        config["virustotal_api_key"] = vt_key
        save_config(config)
        st.success("API keys saved!")

with tab2:
    st.markdown("### Notification Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Gmail")
        gmail_email = st.text_input("Gmail Address", value=config.get("gmail_email", ""))
        gmail_password = st.text_input("App Password", value=config.get("gmail_password", ""), type="password")
        gmail_recipient = st.text_input("Recipient Email", value=config.get("gmail_recipient", ""))
    
    with col2:
        st.markdown("#### Telegram")
        telegram_token = st.text_input("Bot Token", value=config.get("telegram_token", ""))
        telegram_chat = st.text_input("Chat ID", value=config.get("telegram_chat_id", ""))
    
    if st.button("Save Notifications"):
        config["gmail_email"] = gmail_email
        config["gmail_password"] = gmail_password
        config["gmail_recipient"] = gmail_recipient
        config["telegram_token"] = telegram_token
        config["telegram_chat_id"] = telegram_chat
        save_config(config)
        st.success("Notifications saved!")

with tab3:
    st.markdown("### Alert Thresholds")
    
    alert = st.slider("Alert Threshold", 0, 100, config.get("alert_threshold", 70))
    block = st.slider("Auto-Block Threshold", 0, 100, config.get("block_threshold", 70))
    
    auto_block = st.checkbox("Enable Auto-Block", value=config.get("auto_block", True))
    
    if st.button("Save Thresholds"):
        config["alert_threshold"] = alert
        config["block_threshold"] = block
        config["auto_block"] = auto_block
        save_config(config)
        st.success("Thresholds saved!")

with tab4:
    st.markdown("### About")
    st.markdown("""
    **AI-Driven Autonomous SOC**
    
    A comprehensive Security Operations Center dashboard featuring:
    - Real-time threat detection
    - ML-based anomaly scoring
    - Automated response actions
    - Multi-channel alerting
    """)

st.markdown("---")
st.markdown('<div style="text-align: center; color: #8B95A5;"><p>AI-Driven Autonomous SOC | Settings</p></div>', unsafe_allow_html=True)
