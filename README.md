# AI-Driven Autonomous Security Operations Center (SOC)

## Overview

This project implements an **AI-Driven Autonomous Security Operations Center (SOC)** that automates threat detection, risk evaluation, and incident response using machine learning and Zero Trust security principles.

The system simulates real-world SOC workflows by processing large-scale cybersecurity datasets, detecting anomalous behavior, enforcing Zero Trust decisions, and generating automated responses. The architecture is designed to reflect industry practices by separating full-scale local execution from lightweight cloud-based visualization.

---

## Objectives

- Detect anomalous network and host activities using machine learning
- Apply Zero Trust–based risk evaluation for access control decisions
- Automate incident response actions based on assessed risk
- Validate detection logic across multiple cybersecurity datasets
- Provide an interactive SOC dashboard for analysis and monitoring

---

## System Architecture

The SOC pipeline consists of the following stages:

### 1. Data Ingestion and Preprocessing
Raw datasets are cleaned, normalized, and transformed into SOC-ready feature sets.

### 2. Machine Learning Engine
An Isolation Forest model is trained to learn baseline behavior and detect anomalies.

### 3. Anomaly Scoring
Each event is assigned an anomaly score representing deviation from normal behavior.

### 4. Zero Trust Risk Engine
Anomaly scores are mapped to risk levels and access decisions:
- ALLOW
- RESTRICT
- BLOCK

### 5. Automated Incident Response
Response actions are generated automatically based on risk severity and policy rules.

### 6. SOC Dashboard
An interactive dashboard visualizes KPIs, alerts, risk distributions, and automated responses.

---

## Datasets Used

| Dataset | Category | Purpose |
|------|--------|--------|
| CICIDS 2017 | Network Intrusion Detection | Primary training and anomaly detection |
| UNSW-NB15 | Network Traffic & Attacks | Cross-dataset validation |
| ADFA-LD | Host-Based Intrusion Detection | Host-level behavioral validation |

---

## Technology Stack

- **Programming Language:** Python  
- **Machine Learning:** Scikit-learn (Isolation Forest)  
- **Data Processing:** Pandas, NumPy  
- **Backend API:** FastAPI  
- **Visualization:** Streamlit  
- **Environment Management:** Python Virtual Environment  
- **Operating System:** macOS (Local Execution)

---

## Project Structure

autonomous-soc/
├── ml_engine/ # ML training, scoring, validation
├── zero_trust/ # Zero Trust risk engine
├── response_engine/ # Automated incident response
├── backend/ # API layer
├── data/
│ ├── datasets/ # Raw datasets
│ └── parsed_logs/ # SOC-generated outputs
├── dashboard.py # Local SOC dashboard
├── requirements.txt
└── README.md


---

## Local Full SOC Execution (Recommended)

Due to dataset size and ML compute requirements, the **complete SOC pipeline is designed to run locally**.

### Environment Setup

```bash
cd autonomous-soc
source soc-env/bin/activate
pip install -r requirements.txt
```

### Pipeline Execution Order
```
python3 ml_engine/preprocess_cicids.py
python3 ml_engine/train_isolation_forest.py
python3 ml_engine/score_events.py
python3 zero_trust/risk_engine.py
python3 response_engine/incident_response.py
```

###This generates the final SOC output:
```
data/parsed_logs/incident_responses.csv
```

###Running the SOC Dashboard (Local)
```
streamlit run dashboard.py
```

###Access the dashboard at:
```
http://localhost:8501
```

The local dashboard runs in Full SOC Mode, analyzing real security events.

###Cloud Deployment (Visualization Only):
A lightweight version of the dashboard can be deployed for visualization purposes using simulated telemetry.
This deployment is intended strictly for demonstration and portfolio sharing.
The full SOC pipeline remains local due to:
Large dataset size
Machine learning compute requirements
Cloud resource limitations

###Key Features:
Machine learning–based anomaly detection
Zero Trust risk evaluation
Automated incident response
Multi-dataset validation
Explainable SOC decisions
Interactive dashboard visualization


###Academic and Industry Relevance:
The project mirrors real-world SOC architectures where:
Heavy analytics and ML inference run on secure local or on-premise infrastructure
Cloud dashboards are primarily used for monitoring and visualization
This design aligns with modern SOC and Zero Trust security best practices.

###Author

Krishna Akshath Kasibhatta
B.Tech – Computer Science and Engineering
Specialization: Cybersecurity
