# Premium SOC Theme - Global Styles
# Import this in each page for consistent premium look

PREMIUM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* ===== GLOBAL STYLES ===== */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #0a0e17 0%, #151c2c 50%, #0d1320 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e17 0%, #151c2c 50%, #0d1320 100%);
    }
    
    /* ===== ANIMATED BACKGROUND ===== */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(ellipse at 20% 80%, rgba(0, 212, 255, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 40% 40%, rgba(255, 68, 68, 0.05) 0%, transparent 40%);
        pointer-events: none;
        z-index: 0;
        animation: backgroundPulse 15s ease-in-out infinite;
    }
    
    @keyframes backgroundPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* ===== GLASSMORPHISM CARDS ===== */
    .glass-card {
        background: rgba(26, 31, 46, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        border-color: rgba(0, 212, 255, 0.3);
    }
    
    /* ===== GRADIENT BORDERS ===== */
    .gradient-border {
        position: relative;
        background: rgba(26, 31, 46, 0.8);
        border-radius: 16px;
        padding: 1.5rem;
    }
    
    .gradient-border::before {
        content: '';
        position: absolute;
        inset: -2px;
        border-radius: 18px;
        background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 50%, #FF4444 100%);
        z-index: -1;
        opacity: 0.5;
        transition: opacity 0.3s ease;
    }
    
    .gradient-border:hover::before {
        opacity: 1;
    }
    
    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: linear-gradient(145deg, rgba(26, 31, 46, 0.9) 0%, rgba(15, 20, 30, 0.9) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: scale(1.02);
        border-color: rgba(0, 212, 255, 0.4);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00D4FF, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        animation: numberGlow 2s ease-in-out infinite;
    }
    
    @keyframes numberGlow {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.2); }
    }
    
    .metric-label {
        color: #8B95A5;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #00D4FF 0%, #0099CC 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Primary button glow effect */
    .stButton > button[kind="primary"] {
        animation: buttonGlow 3s ease-in-out infinite;
    }
    
    @keyframes buttonGlow {
        0%, 100% { box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3); }
        50% { box-shadow: 0 4px 25px rgba(0, 212, 255, 0.6); }
    }
    
    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 20, 30, 0.98) 0%, rgba(10, 14, 23, 0.98) 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        width: 100%;
        justify-content: flex-start;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(0, 212, 255, 0.15);
        border-color: rgba(0, 212, 255, 0.3);
    }
    
    /* ===== INPUTS ===== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: rgba(26, 31, 46, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: #FAFAFA;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #00D4FF;
        box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.2);
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(26, 31, 46, 0.5);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #8B95A5;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00D4FF 0%, #0099CC 100%);
        color: white;
    }
    
    /* ===== ALERTS ===== */
    .alert-card {
        background: rgba(26, 31, 46, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid;
        transition: all 0.3s ease;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .alert-critical { border-left-color: #FF4444; }
    .alert-high { border-left-color: #FF8C00; }
    .alert-medium { border-left-color: #FFD700; }
    .alert-low { border-left-color: #00C853; }
    
    .alert-card:hover {
        transform: translateX(10px);
        background: rgba(30, 36, 52, 0.9);
    }
    
    /* ===== PROGRESS BARS ===== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00D4FF, #8B5CF6, #FF4444);
        background-size: 200% 100%;
        animation: gradientFlow 2s linear infinite;
        border-radius: 10px;
    }
    
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    /* ===== LOADING SPINNER ===== */
    .loading-spinner {
        width: 50px;
        height: 50px;
        border: 3px solid rgba(255, 255, 255, 0.1);
        border-top: 3px solid #00D4FF;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* ===== FLOATING ELEMENTS ===== */
    .float-animation {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* ===== PULSE EFFECT ===== */
    .pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    /* ===== GLOW TEXT ===== */
    .glow-text {
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5), 0 0 20px rgba(0, 212, 255, 0.3);
    }
    
    /* ===== DATA TABLES ===== */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    .stDataFrame table {
        background: rgba(26, 31, 46, 0.8);
    }
    
    .stDataFrame th {
        background: rgba(0, 212, 255, 0.1) !important;
        color: #00D4FF !important;
    }
    
    /* ===== CHARTS ===== */
    .stPlotlyChart {
        border-radius: 16px;
        overflow: hidden;
        background: rgba(26, 31, 46, 0.5);
        padding: 1rem;
    }
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background: rgba(26, 31, 46, 0.8);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(30, 36, 52, 0.9);
    }
    
    /* ===== HIDE STREAMLIT BRANDING ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(26, 31, 46, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #00E5FF 0%, #9D6FFF 100%);
    }
</style>
"""

# Page header with animated gradient
def page_header(title, subtitle=""):
    return f"""
    <div style="
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: -50%;
            right: -10%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(0, 212, 255, 0.1) 0%, transparent 70%);
            animation: float 6s ease-in-out infinite;
        "></div>
        <h1 style="
            margin: 0;
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FFFFFF 0%, #00D4FF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            position: relative;
            z-index: 1;
        ">{title}</h1>
        <p style="
            color: #8B95A5;
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
            position: relative;
            z-index: 1;
        ">{subtitle}</p>
    </div>
    """

# Animated metric card
def metric_card(value, label, color="#00D4FF", icon=""):
    return f"""
    <div class="metric-card">
        <p style="font-size: 1.5rem; margin: 0;">{icon}</p>
        <p style="
            font-size: 2.5rem;
            font-weight: 800;
            color: {color};
            margin: 0.5rem 0;
            text-shadow: 0 0 20px {color}40;
        ">{value}</p>
        <p class="metric-label">{label}</p>
    </div>
    """

# Alert card with animation
def alert_card(severity, title, description, time_str=""):
    severity_map = {
        "critical": ("#FF4444", "alert-critical"),
        "high": ("#FF8C00", "alert-high"),
        "medium": ("#FFD700", "alert-medium"),
        "low": ("#00C853", "alert-low")
    }
    color, css_class = severity_map.get(severity.lower(), ("#8B95A5", ""))
    
    return f"""
    <div class="alert-card {css_class}">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="color: {color}; font-weight: 700; text-transform: uppercase; font-size: 0.8rem;">
                    {severity}
                </span>
                <h4 style="color: #FAFAFA; margin: 0.3rem 0;">{title}</h4>
                <p style="color: #8B95A5; margin: 0; font-size: 0.9rem;">{description}</p>
            </div>
            <span style="color: #8B95A5; font-size: 0.8rem;">{time_str}</span>
        </div>
    </div>
    """
