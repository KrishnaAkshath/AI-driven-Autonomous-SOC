import streamlit as st
import requests
import base64
import time
import os
import sys
import json
from datetime import datetime
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="URL Scanner | SOC", page_icon="🔗", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .scan-result {
        background: rgba(26, 31, 46, 0.8);
        border-radius: 16px;
        padding: 1.5rem;
        border-left: 4px solid;
        margin: 1rem 0;
    }
    .result-safe { border-left-color: #00C853; }
    .result-suspicious { border-left-color: #FF8C00; }
    .result-malicious { border-left-color: #FF4444; }
    .vendor-row {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 1rem 0;
    }
    .stat-item {
        background: rgba(26, 31, 46, 0.7);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    .history-item {
        background: rgba(26, 31, 46, 0.5);
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

CONFIG_FILE = ".soc_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

config = load_config()
VT_API_KEY = config.get('virustotal_api_key', '')


def scan_url_virustotal(url: str) -> dict:
    if not VT_API_KEY:
        return {'error': 'VirusTotal API key not configured'}
    
    headers = {'x-apikey': VT_API_KEY}
    
    try:
        submit_response = requests.post(
            'https://www.virustotal.com/api/v3/urls',
            headers=headers,
            data={'url': url},
            timeout=30
        )
        
        if submit_response.status_code == 200:
            analysis_id = submit_response.json()['data']['id']
            
            for _ in range(10):
                time.sleep(2)
                
                result_response = requests.get(
                    f'https://www.virustotal.com/api/v3/analyses/{analysis_id}',
                    headers=headers,
                    timeout=15
                )
                
                if result_response.status_code == 200:
                    data = result_response.json()['data']
                    status = data['attributes']['status']
                    
                    if status == 'completed':
                        stats = data['attributes']['stats']
                        results = data['attributes']['results']
                        
                        return {
                            'url': url,
                            'status': 'completed',
                            'stats': stats,
                            'results': results,
                            'malicious': stats.get('malicious', 0),
                            'suspicious': stats.get('suspicious', 0),
                            'harmless': stats.get('harmless', 0),
                            'undetected': stats.get('undetected', 0)
                        }
            
            return {'error': 'Scan timeout - try again'}
        else:
            return {'error': f'API error: {submit_response.status_code}'}
            
    except Exception as e:
        return {'error': str(e)}


def get_url_report(url: str) -> dict:
    if not VT_API_KEY:
        return {'error': 'VirusTotal API key not configured'}
    
    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip('=')
    
    headers = {'x-apikey': VT_API_KEY}
    
    try:
        response = requests.get(
            f'https://www.virustotal.com/api/v3/urls/{url_id}',
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()['data']['attributes']
            stats = data.get('last_analysis_stats', {})
            
            return {
                'url': url,
                'status': 'completed',
                'stats': stats,
                'malicious': stats.get('malicious', 0),
                'suspicious': stats.get('suspicious', 0),
                'harmless': stats.get('harmless', 0),
                'undetected': stats.get('undetected', 0),
                'categories': data.get('categories', {}),
                'last_analysis_date': data.get('last_analysis_date'),
                'reputation': data.get('reputation', 0)
            }
        elif response.status_code == 404:
            return scan_url_virustotal(url)
        else:
            return {'error': f'API error: {response.status_code}'}
            
    except Exception as e:
        return {'error': str(e)}


st.markdown("# 🔗 URL & Domain Scanner")
st.markdown("Check if a URL is malicious, phishing, or unsafe using VirusTotal")
st.markdown("---")

if not VT_API_KEY:
    st.error("⚠️ VirusTotal API key not configured. Go to Settings to add it.")
else:
    st.success("✅ VirusTotal API connected")

tab1, tab2 = st.tabs(["🔍 Scan URL", "📜 Scan History"])

with tab1:
    url_input = st.text_input(
        "Enter URL to scan",
        placeholder="https://example.com or suspicious-site.com",
        help="Enter a full URL including http:// or https://"
    )
    
    if not url_input.startswith(('http://', 'https://')) and url_input:
        url_input = 'https://' + url_input
    
    col1, col2 = st.columns([1, 3])
    with col1:
        scan_btn = st.button("🔍 Scan URL", type="primary", use_container_width=True)
    
    if scan_btn and url_input:
        with st.spinner("Scanning URL with 70+ security vendors..."):
            result = get_url_report(url_input)
            
            if 'error' in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                malicious = result.get('malicious', 0)
                suspicious = result.get('suspicious', 0)
                harmless = result.get('harmless', 0)
                
                if malicious > 0:
                    verdict = "MALICIOUS"
                    verdict_color = "#FF4444"
                    result_class = "result-malicious"
                    icon = "🔴"
                elif suspicious > 2:
                    verdict = "SUSPICIOUS"
                    verdict_color = "#FF8C00"
                    result_class = "result-suspicious"
                    icon = "🟠"
                else:
                    verdict = "SAFE"
                    verdict_color = "#00C853"
                    result_class = "result-safe"
                    icon = "🟢"
                
                parsed = urlparse(url_input)
                
                st.markdown(f"""
                    <div class="scan-result {result_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-size: 2rem;">{icon}</span>
                                <span style="font-size: 1.5rem; font-weight: 700; color: {verdict_color}; margin-left: 0.5rem;">{verdict}</span>
                            </div>
                            <span style="color: #8B95A5; font-size: 0.9rem;">Scanned: {datetime.now().strftime('%H:%M:%S')}</span>
                        </div>
                        <p style="color: #FAFAFA; font-size: 1.1rem; margin: 1rem 0; word-break: break-all;">{url_input}</p>
                        <p style="color: #8B95A5; margin: 0;">Domain: <span style="color: #00D4FF;">{parsed.netloc}</span></p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📊 Detection Results")
                
                col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                
                with col_s1:
                    st.markdown(f"""
                        <div class="stat-item" style="border: 1px solid #FF4444;">
                            <p style="color: #FF4444; font-size: 2rem; font-weight: 700; margin: 0;">{malicious}</p>
                            <p style="color: #8B95A5; margin: 0; font-size: 0.8rem;">Malicious</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_s2:
                    st.markdown(f"""
                        <div class="stat-item" style="border: 1px solid #FF8C00;">
                            <p style="color: #FF8C00; font-size: 2rem; font-weight: 700; margin: 0;">{suspicious}</p>
                            <p style="color: #8B95A5; margin: 0; font-size: 0.8rem;">Suspicious</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_s3:
                    st.markdown(f"""
                        <div class="stat-item" style="border: 1px solid #00C853;">
                            <p style="color: #00C853; font-size: 2rem; font-weight: 700; margin: 0;">{harmless}</p>
                            <p style="color: #8B95A5; margin: 0; font-size: 0.8rem;">Clean</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_s4:
                    total = malicious + suspicious + harmless + result.get('undetected', 0)
                    st.markdown(f"""
                        <div class="stat-item" style="border: 1px solid #00D4FF;">
                            <p style="color: #00D4FF; font-size: 2rem; font-weight: 700; margin: 0;">{total}</p>
                            <p style="color: #8B95A5; margin: 0; font-size: 0.8rem;">Total Vendors</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                if result.get('categories'):
                    st.markdown("### 🏷️ Categories")
                    cats = result['categories']
                    cat_str = ", ".join([f"**{v}**" for v in cats.values() if v])
                    st.markdown(cat_str if cat_str else "No categories detected")
                
                if 'scan_history' not in st.session_state:
                    st.session_state.scan_history = []
                
                st.session_state.scan_history.append({
                    'url': url_input,
                    'verdict': verdict,
                    'malicious': malicious,
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
                if malicious > 0:
                    st.error("⚠️ **Warning**: This URL has been flagged as malicious by security vendors. Do NOT visit this site!")

with tab2:
    st.markdown("### 📜 Recent Scan History")
    
    if 'scan_history' in st.session_state and st.session_state.scan_history:
        for scan in reversed(st.session_state.scan_history[-10:]):
            if scan['verdict'] == 'MALICIOUS':
                icon = "🔴"
                color = "#FF4444"
            elif scan['verdict'] == 'SUSPICIOUS':
                icon = "🟠"
                color = "#FF8C00"
            else:
                icon = "🟢"
                color = "#00C853"
            
            st.markdown(f"""
                <div class="history-item">
                    <div>
                        <span>{icon}</span>
                        <span style="color: #FAFAFA; margin-left: 0.5rem;">{scan['url'][:50]}{'...' if len(scan['url']) > 50 else ''}</span>
                    </div>
                    <div>
                        <span style="color: {color}; font-weight: 600;">{scan['verdict']}</span>
                        <span style="color: #8B95A5; margin-left: 1rem; font-size: 0.8rem;">{scan['time']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No scans yet. Scan a URL to see history.")

st.markdown("---")
st.markdown('<div style="text-align: center; color: #8B95A5; padding: 1rem;"><p style="margin: 0;">🛡️ AI-Driven Autonomous SOC | URL Scanner powered by VirusTotal</p></div>', unsafe_allow_html=True)
