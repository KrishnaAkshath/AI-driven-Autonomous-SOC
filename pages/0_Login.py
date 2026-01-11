import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Login | SOC", page_icon="L", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e17 0%, #151c2c 50%, #0d1320 100%);
    }
    
    /* Animated background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(255, 68, 68, 0.05) 0%, transparent 40%);
        animation: bgFloat 20s ease-in-out infinite;
        pointer-events: none;
    }
    
    @keyframes bgFloat {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }
    
    /* Login container */
    .login-container {
        background: rgba(26, 31, 46, 0.8);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 28px;
        padding: 3rem;
        max-width: 420px;
        margin: 2rem auto;
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .login-container::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: conic-gradient(
            from 0deg,
            transparent 0deg 340deg,
            rgba(0, 212, 255, 0.1) 340deg 360deg
        );
        animation: borderRotate 8s linear infinite;
    }
    
    @keyframes borderRotate {
        100% { transform: rotate(360deg); }
    }
    
    .login-inner {
        position: relative;
        z-index: 1;
    }
    
    /* Logo area */
    .logo-area {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .logo-shield {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 100%);
        border-radius: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        box-shadow: 0 10px 40px rgba(0, 212, 255, 0.3);
        animation: logoFloat 4s ease-in-out infinite;
    }
    
    @keyframes logoFloat {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-8px) rotate(2deg); }
    }
    
    .logo-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #00D4FF 50%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .logo-subtitle {
        color: #8B95A5;
        font-size: 0.95rem;
        margin-top: 0.3rem;
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        background: rgba(15, 20, 30, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        color: #FAFAFA !important;
        padding: 1rem 1.2rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00D4FF !important;
        box-shadow: 0 0 0 4px rgba(0, 212, 255, 0.15) !important;
    }
    
    .stTextInput > label {
        color: #8B95A5 !important;
        font-weight: 500 !important;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #00D4FF 0%, #0099CC 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.35) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(0, 212, 255, 0.5) !important;
    }
    
    /* Divider */
    .divider {
        display: flex;
        align-items: center;
        margin: 1.5rem 0;
        gap: 1rem;
    }
    
    .divider-line {
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    }
    
    .divider-text {
        color: #8B95A5;
        font-size: 0.85rem;
    }
    
    /* Features */
    .features {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-top: 2rem;
    }
    
    .feature-item {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-item:hover {
        background: rgba(0, 212, 255, 0.1);
        transform: translateY(-2px);
    }
    
    .feature-icon {
        font-size: 1.5rem;
        margin-bottom: 0.3rem;
    }
    
    .feature-text {
        color: #8B95A5;
        font-size: 0.75rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header { visibility: hidden; }
    section[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

from auth.auth_manager import login_user, register_user, check_auth

if check_auth():
    st.switch_page("pages/1_Dashboard.py")

st.markdown("""
<div class="login-container">
    <div class="login-inner">
        <div class="logo-area">
            <div class="logo-shield">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="white">
                    <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/>
                </svg>
            </div>
            <h1 class="logo-title">SOC Platform</h1>
            <p class="logo-subtitle">Autonomous Security Operations</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'

col1, col2 = st.columns(2)
with col1:
    if st.button("Login", use_container_width=True, type="primary" if st.session_state.auth_mode == 'login' else "secondary"):
        st.session_state.auth_mode = 'login'
        st.rerun()
with col2:
    if st.button("Register", use_container_width=True, type="primary" if st.session_state.auth_mode == 'register' else "secondary"):
        st.session_state.auth_mode = 'register'
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.auth_mode == 'login':
    email = st.text_input("Email", placeholder="you@company.com", key="login_email")
    password = st.text_input("Password", type="password", placeholder="Enter password", key="login_pass")
    
    if st.button("Sign In", type="primary", use_container_width=True):
        if email and password:
            success, message, user = login_user(email, password)
            if success and user:
                st.session_state.auth_token = user.get('token')
                st.success("Welcome back!")
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error(message)
        else:
            st.warning("Please enter email and password")
            
else:
    name = st.text_input("Full Name", placeholder="John Doe", key="reg_name")
    email = st.text_input("Email", placeholder="you@company.com", key="reg_email")
    password = st.text_input("Password", type="password", placeholder="Min 6 characters", key="reg_pass")
    
    if st.button("Create Account", type="primary", use_container_width=True):
        if name and email and password:
            if len(password) < 6:
                st.error("Password must be at least 6 characters")
            elif "@" not in email:
                st.error("Please enter a valid email")
            else:
                success, message = register_user(email, password, name)
                if success:
                    st.success("Account created! Please login.")
                    st.session_state.auth_mode = 'login'
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.warning("Please fill all fields")

st.markdown("""
<div style="margin-top: 2rem; text-align: center;">
    <div class="features">
        <div class="feature-item">
            <div class="feature-icon">🛡️</div>
            <div class="feature-text">Zero Trust</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">🤖</div>
            <div class="feature-text">AI-Powered</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">⚡</div>
            <div class="feature-text">Real-time</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">🔒</div>
            <div class="feature-text">Encrypted</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #8B95A5; font-size: 0.8rem;">Default: admin@soc.local / admin123</div>', unsafe_allow_html=True)
