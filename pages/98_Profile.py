import streamlit as st
import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="My Profile | SOC", page_icon="U", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .profile-header {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .avatar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        color: white;
        margin: 0 auto 1rem auto;
    }
    .profile-card {
        background: rgba(26, 31, 46, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .stat-box {
        background: rgba(26, 31, 46, 0.7);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

from auth.auth_manager import check_auth, load_users, save_users, hash_password

user = check_auth()
if not user:
    st.switch_page("pages/0_Login.py")
    st.stop()

data = load_users()
user_data = data["users"].get(user["email"], {})

initials = "".join([n[0].upper() for n in user["name"].split()[:2]]) if user["name"] else "U"

st.markdown(f"""
    <div class="profile-header">
        <div class="avatar">{initials}</div>
        <h2 style="margin: 0; color: #FAFAFA;">{user['name']}</h2>
        <p style="color: #8B95A5; margin: 0.5rem 0;">{user['email']}</p>
        <span style="background: {'#FF4444' if user['role'] == 'admin' else '#00D4FF'}; color: white; padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.8rem; text-transform: uppercase;">{user['role']}</span>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class="stat-box">
            <p style="color: #00D4FF; font-size: 1.5rem; font-weight: 700; margin: 0;">Active</p>
            <p style="color: #8B95A5; margin: 0; font-size: 0.85rem;">Account Status</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    login_date = user_data.get('last_login', 'Never')
    if login_date and login_date != 'Never':
        try:
            login_date = datetime.fromisoformat(login_date).strftime('%Y-%m-%d')
        except:
            pass
    st.markdown(f"""
        <div class="stat-box">
            <p style="color: #FAFAFA; font-size: 1rem; font-weight: 600; margin: 0;">{login_date}</p>
            <p style="color: #8B95A5; margin: 0; font-size: 0.85rem;">Last Login</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    created = user_data.get('created', 'Unknown')
    if created and created != 'Unknown':
        try:
            created = datetime.fromisoformat(created).strftime('%Y-%m-%d')
        except:
            pass
    st.markdown(f"""
        <div class="stat-box">
            <p style="color: #FAFAFA; font-size: 1rem; font-weight: 600; margin: 0;">{created}</p>
            <p style="color: #8B95A5; margin: 0; font-size: 0.85rem;">Member Since</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Edit Profile", "Security", "Preferences"])

with tab1:
    st.markdown("### Edit Profile")
    
    with st.form("edit_profile"):
        new_name = st.text_input("Display Name", value=user["name"])
        new_email = st.text_input("Email", value=user["email"], disabled=True, help="Email cannot be changed")
        
        bio = st.text_area("Bio (Optional)", value=user_data.get('bio', ''), placeholder="Tell us about yourself...")
        
        if st.form_submit_button("Save Changes", type="primary"):
            if new_name:
                data["users"][user["email"]]["name"] = new_name
                data["users"][user["email"]]["bio"] = bio
                save_users(data)
                st.success("Profile updated successfully!")
                st.rerun()

with tab2:
    st.markdown("### Change Password")
    
    with st.form("change_password"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        if st.form_submit_button("Update Password", type="primary"):
            if not all([current_password, new_password, confirm_password]):
                st.warning("Please fill all fields")
            elif new_password != confirm_password:
                st.error("New passwords do not match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                from auth.auth_manager import verify_password
                if verify_password(current_password, user_data.get('password', '')):
                    data["users"][user["email"]]["password"] = hash_password(new_password)
                    save_users(data)
                    st.success("Password updated successfully!")
                else:
                    st.error("Current password is incorrect")
    
    st.markdown("### Active Sessions")
    st.info("You are currently logged in from this device.")

with tab3:
    st.markdown("### Notification Preferences")
    
    prefs = user_data.get('preferences', {})
    
    email_alerts = st.checkbox("Receive email alerts", value=prefs.get('email_alerts', True))
    telegram_alerts = st.checkbox("Receive Telegram alerts", value=prefs.get('telegram_alerts', True))
    daily_report = st.checkbox("Receive daily summary report", value=prefs.get('daily_report', False))
    
    if st.button("Save Preferences", type="primary"):
        if 'preferences' not in data["users"][user["email"]]:
            data["users"][user["email"]]["preferences"] = {}
        data["users"][user["email"]]["preferences"]["email_alerts"] = email_alerts
        data["users"][user["email"]]["preferences"]["telegram_alerts"] = telegram_alerts
        data["users"][user["email"]]["preferences"]["daily_report"] = daily_report
        save_users(data)
        st.success("Preferences saved!")

st.markdown("---")

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("Logout", type="primary", use_container_width=True):
        from auth.auth_manager import logout_user
        if "auth_token" in st.session_state:
            logout_user(st.session_state.auth_token)
            del st.session_state.auth_token
        st.switch_page("pages/0_Login.py")

st.markdown('<div style="text-align: center; color: #8B95A5; padding: 1rem;"><p style="margin: 0;">AI-Driven Autonomous SOC | User Profile</p></div>', unsafe_allow_html=True)
