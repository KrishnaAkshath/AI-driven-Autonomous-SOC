import streamlit as st
import os
import sys
import time
import json
import socket
import uuid
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Security Testing | SOC", page_icon="T", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .attack-log { background: rgba(0,0,0,0.4); border-radius: 8px; padding: 1rem; font-family: monospace; max-height: 300px; overflow-y: auto; }
    .log-info { color: #00D4FF; }
    .log-warning { color: #FF8C00; }
    .log-danger { color: #FF4444; }
    .log-success { color: #00C853; }
    .port-open { background: rgba(0,200,83,0.15); border-left: 4px solid #00C853; padding: 0.5rem; margin: 0.2rem 0; border-radius: 4px; }
    .vuln-high { background: rgba(255,68,68,0.15); border-left: 4px solid #FF4444; padding: 0.8rem; margin: 0.3rem 0; border-radius: 4px; }
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

st.markdown("# Security Testing")
st.markdown("Attack simulation and penetration testing tools")
st.markdown("---")

tab1, tab2 = st.tabs(["Attack Simulation", "Pentest Tools"])

with tab1:
    st.markdown("### Attack Simulation Lab")
    st.warning("**Educational Purpose** - Demonstrates how SOC detects threats")
    
    # Get device info
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "Unknown"
    
    try:
        public_ip = requests.get("https://api.ipify.org?format=json", timeout=5).json().get("ip", "Unknown")
    except:
        public_ip = "Unknown"
    
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,48,8)][::-1]).upper()
    
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"**Public IP:** {public_ip}")
    col2.markdown(f"**Local IP:** {local_ip}")
    col3.markdown(f"**MAC:** {mac}")
    
    attacks = {
        "DDoS Attack": {"risk": 95, "steps": ["Initializing botnet...", "Targeting server...", "Launching SYN flood...", "SOC ALERT: DDoS detected!", "BLOCKED - Rate limiting enabled"]},
        "Port Scan": {"risk": 72, "steps": ["Scanning ports...", "Open: 22, 80, 443", "SOC ALERT: Port scan!", "BLOCKED - IP banned"]},
        "Brute Force": {"risk": 78, "steps": ["Target: SSH", "Attempt 1: FAILED", "50+ attempts detected", "SOC ALERT: Brute force!", "BLOCKED - Account locked"]},
        "SQL Injection": {"risk": 91, "steps": ["Payload: ' OR 1=1", "Attempting bypass...", "SOC ALERT: SQLi detected!", "BLOCKED - Session terminated"]},
        "Ransomware": {"risk": 98, "steps": ["Malware executing...", "Connecting to C2...", "SOC ALERT: Ransomware!", "BLOCKED - Endpoint isolated"]}
    }
    
    attack = st.selectbox("Select Attack", list(attacks.keys()))
    
    if st.button("Launch Simulation", type="primary"):
        st.markdown("### Attack Log")
        log_area = st.empty()
        logs = []
        progress = st.progress(0)
        
        for i, step in enumerate(attacks[attack]["steps"]):
            time.sleep(0.4)
            color = "log-danger" if "ALERT" in step or "BLOCKED" in step else "log-info"
            logs.append(f'<span class="{color}">[{datetime.now().strftime("%H:%M:%S")}] {step}</span>')
            log_area.markdown(f'<div class="attack-log">{"<br>".join(logs)}</div>', unsafe_allow_html=True)
            progress.progress((i+1)/len(attacks[attack]["steps"]))
        
        st.success(f"Attack blocked! Risk: {attacks[attack]['risk']}/100")

with tab2:
    if user.get('role') != 'admin':
        st.error("Admin access required for penetration testing")
        st.stop()
    
    st.markdown("### Penetration Testing")
    st.warning("**Authorized Use Only** - Only test systems you own")
    
    target = st.text_input("Target IP", placeholder="192.168.1.1")
    scan_type = st.selectbox("Scan Type", ["Quick (22 ports)", "Web Ports", "Full (1-1024)"])
    
    port_lists = {
        "Quick (22 ports)": [21,22,23,25,53,80,110,139,143,443,445,993,1433,3306,3389,5432,5900,8080],
        "Web Ports": [80, 443, 8080, 8443, 8000],
        "Full (1-1024)": list(range(1, 1025))
    }
    
    if st.button("Start Scan", type="primary") and target:
        ports = port_lists[scan_type]
        
        def check_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                sock.close()
                return port if result == 0 else None
            except:
                return None
        
        with st.spinner(f"Scanning {len(ports)} ports..."):
            progress = st.progress(0)
            open_ports = []
            
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = {executor.submit(check_port, p): p for p in ports}
                done = 0
                for future in as_completed(futures):
                    done += 1
                    progress.progress(done/len(ports))
                    result = future.result()
                    if result:
                        open_ports.append(result)
            
            st.metric("Open Ports Found", len(open_ports))
            
            services = {21:"FTP", 22:"SSH", 23:"Telnet", 80:"HTTP", 443:"HTTPS", 3306:"MySQL", 3389:"RDP"}
            
            if open_ports:
                for p in sorted(open_ports):
                    svc = services.get(p, "")
                    st.markdown(f'<div class="port-open">Port {p} {f"({svc})" if svc else ""} - OPEN</div>', unsafe_allow_html=True)
                
                # Vulnerability check
                vulns = []
                if 23 in open_ports: vulns.append(("CRITICAL", "Telnet exposed - unencrypted"))
                if 445 in open_ports: vulns.append(("CRITICAL", "SMB exposed - ransomware risk"))
                if 3389 in open_ports: vulns.append(("HIGH", "RDP exposed - brute force risk"))
                
                if vulns:
                    st.markdown("### Vulnerabilities")
                    for sev, desc in vulns:
                        st.markdown(f'<div class="vuln-high">[{sev}] {desc}</div>', unsafe_allow_html=True)
            else:
                st.info("No open ports found")

st.markdown("---")
st.markdown('<div style="text-align: center; color: #8B95A5;"><p>AI-Driven Autonomous SOC | Security Testing</p></div>', unsafe_allow_html=True)
