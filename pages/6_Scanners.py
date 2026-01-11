import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Scanners | SOC", page_icon="S", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
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

st.markdown("# Security Scanners")
st.markdown("File, URL, and Network scanning tools")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["File Scanner", "URL Scanner", "Network Monitor"])

# Import the original page content as functions would be complex
# Instead, provide links to dedicated tools

with tab1:
    st.markdown("### PDF File Scanner")
    st.markdown("Scan PDF files for malware, JavaScript, and phishing indicators.")
    
    from services.pdf_scanner import scan_pdf_file
    import tempfile
    
    uploaded = st.file_uploader("Upload PDF", type=['pdf'])
    if uploaded:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(uploaded.getvalue())
            tmp_path = tmp.name
        
        if st.button("Scan PDF", type="primary"):
            with st.spinner("Scanning..."):
                result = scan_pdf_file(tmp_path)
                
                verdict = result.get('verdict', 'UNKNOWN')
                risk = result.get('risk_score', 0)
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Verdict", verdict)
                col2.metric("Risk Score", f"{risk}/100")
                col3.metric("Threats", len(result.get('threats_found', [])))
                
                if result.get('threats_found'):
                    st.error("Threats Found:")
                    for t in result['threats_found']:
                        st.markdown(f"- {t}")
                else:
                    st.success("No threats detected")
                
                os.unlink(tmp_path)

with tab2:
    st.markdown("### URL Scanner")
    st.markdown("Check URLs for malicious content using VirusTotal.")
    
    import json
    import requests
    import base64
    from datetime import datetime
    
    config = {}
    if os.path.exists('.soc_config.json'):
        with open('.soc_config.json', 'r') as f:
            config = json.load(f)
    
    VT_KEY = config.get('virustotal_api_key', '')
    
    if not VT_KEY:
        st.warning("Add VirusTotal API key in Settings")
    else:
        url = st.text_input("Enter URL", placeholder="https://example.com")
        
        if st.button("Scan URL", type="primary") and url:
            if not url.startswith('http'):
                url = 'https://' + url
            
            with st.spinner("Scanning with 70+ vendors..."):
                try:
                    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip('=')
                    resp = requests.get(
                        f'https://www.virustotal.com/api/v3/urls/{url_id}',
                        headers={'x-apikey': VT_KEY},
                        timeout=15
                    )
                    
                    if resp.status_code == 200:
                        data = resp.json()['data']['attributes']
                        stats = data.get('last_analysis_stats', {})
                        
                        mal = stats.get('malicious', 0)
                        sus = stats.get('suspicious', 0)
                        
                        if mal > 0:
                            st.error(f"MALICIOUS - {mal} vendors flagged this URL")
                        elif sus > 2:
                            st.warning(f"SUSPICIOUS - {sus} vendors flagged this URL")
                        else:
                            st.success("SAFE - No threats detected")
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Malicious", mal)
                        col2.metric("Suspicious", sus)
                        col3.metric("Clean", stats.get('harmless', 0))
                    else:
                        st.error("URL not found, submitting for scan...")
                except Exception as e:
                    st.error(f"Error: {e}")

with tab3:
    st.markdown("### Network Monitor")
    st.markdown("Upload PCAP files for traffic analysis.")
    
    from services.live_monitor import analyze_pcap_file
    
    pcap = st.file_uploader("Upload PCAP", type=['pcap', 'pcapng'])
    
    if pcap:
        path = f"uploaded_{pcap.name}"
        with open(path, 'wb') as f:
            f.write(pcap.getbuffer())
        
        if st.button("Analyze PCAP", type="primary"):
            with st.spinner("Analyzing..."):
                result = analyze_pcap_file(path)
                
                if 'error' not in result or result.get('total_packets', 0) > 0:
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Packets", result.get('total_packets', 0))
                    col2.metric("Sources", len(result.get('unique_sources', [])))
                    col3.metric("Threats", len(result.get('threats', [])))
                    
                    if result.get('threats'):
                        st.error("Threats Detected:")
                        for t in result['threats']:
                            st.markdown(f"- [{t['severity']}] {t['type']}: {t['detail']}")
                    else:
                        st.success("No threats detected")
                else:
                    st.error(f"Error: {result.get('error')}")

st.markdown("---")
st.markdown('<div style="text-align: center; color: #8B95A5;"><p>AI-Driven Autonomous SOC | Scanners</p></div>', unsafe_allow_html=True)
