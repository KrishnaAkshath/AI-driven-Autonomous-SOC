import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime

# ======================================================
# PAGE CONFIGURATION
# ======================================================
st.set_page_config(
    page_title="AI-Driven Autonomous SOC",
    layout="wide"
)

st.title("AI-Driven Autonomous SOC Dashboard")

st.markdown(
    """
    This dashboard demonstrates an **AI-driven Autonomous Security Operations Center (SOC)** 
    supporting both **historical dataset analysis** and **near real-time monitoring of live
    network traffic captured via Wireshark**.
    """
)

# ======================================================
# SIDEBAR – MODE SELECTION
# ======================================================
st.sidebar.header("SOC Operating Mode")

mode = st.sidebar.radio(
    "Select SOC Mode",
    [
        "Dataset Analysis Mode",
        "Live Network Monitoring Mode (Wireshark)"
    ]
)

st.sidebar.markdown("---")

# ======================================================
# PATH SELECTION
# ======================================================
DATASET_PATH = "data/parsed_logs/incident_responses.csv"
LIVE_PATH = "data/parsed_logs/live_events.csv"

if mode == "Dataset Analysis Mode":
    DATA_PATH = DATASET_PATH
    MODE_DESC = "Historical SOC Analysis using CICIDS 2017, UNSW-NB15, ADFA-LD"
else:
    DATA_PATH = LIVE_PATH
    MODE_DESC = "Near Real-Time SOC Monitoring using Wireshark Captures"

st.success(f"Operating Mode: {MODE_DESC}")
st.divider()

# ======================================================
# DATA LOADING (OPTIMIZED)
# ======================================================
@st.cache_data
def load_data(path: str, max_rows: int = 100_000) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Keep only recent events (SOC rolling window)
    if len(df) > max_rows:
        df = df.tail(max_rows)

    return df

if not os.path.exists(DATA_PATH):
    st.error("Required data file not found for the selected mode.")
    st.stop()

df = load_data(DATA_PATH)

# ======================================================
# SIDEBAR CONTROLS
# ======================================================
st.sidebar.header("SOC Controls")

rows_to_display = st.sidebar.selectbox(
    "Records to display",
    [50, 100, 250, 500],
    index=1
)

auto_refresh = False
if mode == "Live Network Monitoring Mode (Wireshark)":
    auto_refresh = st.sidebar.checkbox(
        "Enable Auto Refresh (every 10 seconds)",
        value=False
    )

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Performance Notes**
    - Dashboard uses a rolling window of recent events
    - Visualizations use statistical sampling
    - Auto-refresh applies only to live monitoring
    """
)

# ======================================================
# AUTO-REFRESH (LIVE MODE ONLY)
# ======================================================
if auto_refresh and mode == "Live Network Monitoring Mode (Wireshark)":
    time.sleep(10)
    st.rerun()

# ======================================================
# SAMPLE DATA FOR VISUALS (FAST)
# ======================================================
viz_df = df.sample(
    min(len(df), 20_000),
    random_state=42
)

# ======================================================
# KPI SECTION
# ======================================================
total_events = len(df)
blocked = (df["access_decision"] == "BLOCK").sum()
restricted = (df["access_decision"] == "RESTRICT").sum()
allowed = (df["access_decision"] == "ALLOW").sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Security Events", f"{total_events:,}")
c2.metric("Blocked", f"{blocked:,}")
c3.metric("Restricted", f"{restricted:,}")
c4.metric("Allowed", f"{allowed:,}")

st.divider()

# ======================================================
# LIVE STATUS
# ======================================================
last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

c5, c6 = st.columns(2)
c5.metric("Last Update", last_updated)
c6.metric("Active Event Window", f"{total_events:,}")

st.divider()

# ======================================================
# RISK DISTRIBUTION
# ======================================================
st.subheader("Risk Score Distribution")

risk_dist = viz_df["risk_score"].round().value_counts().sort_index()
st.bar_chart(risk_dist)

st.caption(
    "Distribution of anomaly-based risk scores across observed security events."
)

st.divider()

# ======================================================
# ACTIVE ALERTS
# ======================================================
st.subheader("Active Security Alerts")

alerts = df[df["access_decision"] != "ALLOW"]

st.dataframe(
    alerts.head(rows_to_display),
    width="stretch"
)

st.caption(
    f"Showing the top {rows_to_display} events requiring analyst attention."
)

st.divider()

# ======================================================
# AUTOMATED RESPONSES
# ======================================================
st.subheader("Automated Incident Responses")

response_df = df[
    ["risk_score", "access_decision", "automated_response"]
].head(rows_to_display)

st.dataframe(
    response_df,
    width="stretch"
)

st.caption(
    "Responses are generated automatically using Zero Trust decision logic."
)

st.divider()

# ======================================================
# SOC ACTIVITY TIMELINE (SAMPLED)
# ======================================================
st.subheader("SOC Activity Timeline")

timeline_df = viz_df["risk_score"].reset_index(drop=True)
st.line_chart(timeline_df)

st.caption(
    "Timeline illustrating fluctuations in security risk levels over time."
)

st.divider()

# ======================================================
# DATASET COVERAGE (DATASET MODE ONLY)
# ======================================================
if mode == "Dataset Analysis Mode":
    st.subheader("Dataset Coverage and Validation Summary")

    dataset_df = pd.DataFrame({
        "Dataset": ["CICIDS 2017", "UNSW-NB15", "ADFA-LD"],
        "Domain": [
            "Network Intrusion Detection",
            "Network Traffic & Attack Simulation",
            "Host-Based Intrusion Detection"
        ],
        "Purpose in SOC": [
            "Primary training and anomaly detection",
            "Cross-dataset validation",
            "Host behavior validation"
        ],
        "Status": [
            "Fully Integrated",
            "Validated",
            "Validated"
        ]
    })

    st.table(dataset_df)
    st.divider()

# ======================================================
# FOOTER
# ======================================================
st.caption(
    """
    This project implements an **AI-driven Autonomous Security Operations Center**
    combining anomaly detection, Zero Trust access control, and automated incident
    response using both benchmark cybersecurity datasets and live network traffic.
    """
)
