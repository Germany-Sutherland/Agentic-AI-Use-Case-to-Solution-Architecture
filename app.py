# app.py
# AWS Architecture Design Using Agentic AI Agents (Free-tier, no keys)
# Works on Streamlit Community Cloud + GitHub Free
import io
import time
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ---------- Basic page setup ----------
st.set_page_config(
    page_title="AWS Architecture Design — Agentic AI (Free)",
    page_icon="🧭",
    layout="wide",
)

# ---------- Session state defaults ----------
if "run_id" not in st.session_state:
    st.session_state.run_id = 0
if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = []
if "arch_text" not in st.session_state:
    st.session_state.arch_text = ""

# ---------- Small helpers ----------
def badge(text, tone="neutral"):
    tones = {
        "neutral": "#e9ecef",
        "primary": "#dbeafe",
        "success": "#dcfce7",
        "warning": "#fef9c3",
        "danger": "#fee2e2",
        "purple": "#ede9fe",
    }
    return f"<span style='background:{tones.get(tone, '#e9ecef')}; padding:4px 8px; border-radius:12px; font-size:12px; margin-right:6px;'>{text}</span>"

def think_line(agent_name, text):
    st.session_state.agent_logs.append(f"**{agent_name}**: {text}")

def clear_state():
    st.session_state.run_id += 1
    st.session_state.agent_logs = []
    st.session_state.arch_text = ""
    st.rerun()

# ---------- Left rail: How to use ----------
with st.sidebar:
    st.markdown("## 🌈 How to Use")
    st.markdown(
        """
1. **Paste your Use Case / RFP / Epic** in the big box.
2. **Set priorities** on the *radar chart* (Latency, Load Balancing, Cost, Performance, Security, Scalability).
3. Click **Run Agents** — watch **Sophia, Emilia, Kumar, Amit** think in real-time.
4. View the **Proposed Architecture** and **download** the Tutorial & TDD.
5. Click **🔄 New Design** to start fresh.
"""
    )
    st.markdown(badge("2050-ready", "purple") + badge("Agentic AI (simulated)", "primary") + badge("Zero-cost — Free GitHub + Free Streamlit", "success"), unsafe_allow_html=True)

# ---------- Main: Input + Radar ----------
st.markdown("### 🧩 Input")

col_txt, col_focus = st.columns([3, 1])
with col_txt:
    default_prompt = "Global supply chain platform for forecasting, event ingestion, and anomaly detection."
    use_case = st.text_area(
        "Paste Use Case / RFP / Epic user story",
        value=default_prompt,
        height=140,
        placeholder="Describe the system to build (what, who, scale, data, compliance)…",
    )

with col_focus:
    st.markdown("**Architecture Focus**")
    focus = st.selectbox(" ", ["AI/ML", "Serverless", "Data Platform", "Zero Trust", "E-commerce"], label_visibility="collapsed")
    show_diagram = st.checkbox("Show diagram", value=True)

st.markdown("---")

st.markdown("#### 🎯 Set Priorities (adjustable radar chart)")
sl_col1, sl_col2, sl_col3 = st.columns(3)
sl_col4, sl_col5, sl_col6 = st.columns(3)

latency = sl_col1.slider("Latency", 0, 10, 7)
load_bal = sl_col2.slider("Load Balancing", 0, 10, 6)
cost = sl_col3.slider("Cloud Cost", 0, 10, 5)
performance = sl_col4.slider("Performance", 0, 10, 7)
security = sl_col5.slider("Security", 0, 10, 8)
scalability = sl_col6.slider("Scalability", 0, 10, 8)

# Radar (spider) chart with matplotlib (no special styling to avoid warnings)
labels = ["Latency", "Load Bal.", "Cost", "Perf.", "Security", "Scalability"]
values = [latency, load_bal, cost, performance, security, scalability]
values += values[:1]  # close the loop
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

fig = plt.figure()
ax = plt.subplot(111, polar=True)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_rlabel_position(0)
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(["2", "4", "6", "8", "10"])
ax.plot(angles, values)
ax.fill(angles, values, alpha=0.15)
st.pyplot(fig, use_container_width=True)

# ---------- Agents area ----------
st.markdown("### 🤖 Agents in action (human-like, simulated)")

agent_cols = st.columns(4)
agent_cards = [
    ("Data Architect **Sophia**", "📊", "Analyzing data domains, storage, and throughput."),
    ("Security Architect **Emilia**", "🔐", "Mapping Zero Trust, IAM, and encryption paths."),
    ("Solution Architect **Kumar**", "🧭", "Selecting AWS building blocks & trade-offs."),
    ("AI Architect **Amit**", "🧠", "Adding MLOps, AI services, and model lifecycle."),
]
for i, (title, icon, desc) in enumerate(agent_cards):
    with agent_cols[i]:
        st.markdown(f"**{icon} {title}**")
        st.caption(desc)
        with st.status("Idle", expanded=False) as s:
            s.update(label="Ready", state="complete")

# ---------- Agent logic (local rules, no external calls) ----------
def agent_run(use_case_text, priorities, focus_choice):
    # Simulate incremental thinking with justified outputs
    sophia = []
    emilia = []
    kumar = []
    amit = []

    # Data Architect (Sophia)
    sophia.append("Identify raw vs processed data zones; choose S3 as data lake with lifecycle rules.")
    if priorities["latency"] >= 7:
        sophia.append("Add Kinesis/Data Streams for low-latency ingestion.")
    if priorities["performance"] >= 7:
        sophia.append("Use Glue/Spark for parallel transforms; consider Lake Formation for governance.")
    if "E-commerce" in focus_choice or "Serverless" in focus_choice:
        sophia.append("Expose product & clickstream through Athena and API Gateway.")

    # Security Architect (Emilia)
    emilia.append("Apply Zero Trust: IAM roles, least privilege, scoped tokens, VPC endpoints.")
    if priorities["security"] >= 8:
        emilia.append("Add KMS CMK for S3/Kinesis; guardrails with Config and Security Hub.")
    if "Healthcare" in use_case_text.lower() or "pii" in use_case_text.lower():
        emilia.append("HIPAA/PII data tagging; Macie + CloudTrail for continuous auditing.")

    # Solution Architect (Kumar)
    kumar.append("Choose region close to users; multi-AZ; ALB/CloudFront for global edge.")
    if priorities["scalability"] >= 8:
        kumar.append("Stateless services on ECS Fargate or Lambda; DynamoDB autoscaling.")
    if priorities["cost"] <= 4:
        kumar.append("Favor serverless to minimize idle cost; spot for batch compute.")
    if "AI/ML" in focus_choice:
        kumar.append("Interface services via API Gateway + Lambda; feature store for models.")

    # AI Architect (Amit)
    amit.append("Model lifecycle: data prep → training → registry → deployment → monitoring.")
    if "forecast" in use_case_text.lower() or "anomaly" in use_case_text.lower():
        amit.append("Use SageMaker for train/serve; CloudWatch + Model Monitor for drift.")
    if priorities["latency"] >= 7:
        amit.append("Add real-time inference endpoint; batch for nightly jobs.")

    # Combine into proposed architecture text (ASCII diagram)
    diagram = [
        "Data  →  Amazon S3 (Lake)  →  Glue/Spark (ETL)  →  Feature Store  →  SageMaker (Train)  →  Model Registry  →  Endpoint (Serve)  →  CloudWatch",
    ]
    if priorities["latency"] >= 7:
        diagram.insert(0, "Kinesis/Data Streams  →")
    if priorities["scalability"] >= 8:
        diagram.append(" + Auto Scaling (DynamoDB/Lambda)")
    if priorities["security"] >= 8:
        diagram.append(" + KMS + Config + SecurityHub")

    result = {
        "sophia": sophia,
        "emilia": emilia,
        "kumar": kumar,
        "amit": amit,
        "diagram": "  \n".join(diagram),
    }
    return result

# ---------- Run + Refresh buttons ----------
btn_col1, btn_col2, btn_col3 = st.columns([1.3, 1.0, 1.0])
run_clicked = btn_col1.button("▶️ Run Agents & Generate Architecture", type="primary")
refresh_clicked = btn_col2.button("🔄 New Design", help="Clear the page and design a new architecture")
download_section_placeholder = btn_col3.empty()  # reserved later

if refresh_clicked:
    clear_state()

# ---------- Execute agents when Run is clicked ----------
if run_clicked:
    st.session_state.agent_logs = []
    priorities = {
        "latency": latency,
        "load": load_bal,
        "cost": cost,
        "performance": performance,
        "security": security,
        "scalability": scalability,
    }

    with st.spinner("Agents thinking…"):
        # Simulate progress + visible thoughts
        think_line("Data Architect Sophia", "Reading data domain hints from the use case…")
        time.sleep(0.3)
        think_line("Security Architect Emilia", "Applying Zero Trust and encryption guardrails…")
        time.sleep(0.3)
        think_line("Solution Architect Kumar", "Mapping AWS components to priorities…")
        time.sleep(0.3)
        think_line("AI Architect Amit", "Adding MLOps and inference topology…")
        time.sleep(0.3)

        out = agent_run(use_case, priorities, focus)

    # Show agent thoughts
    st.info("**Agent thoughts (trace):**")
    for k in ["sophia", "emilia", "kumar", "amit"]:
        for line in out[k]:
            st.write(f"- {line}")

    # Proposed Architecture (renamed from SIMPLE AWS DIAGRAM)
    if show_diagram:
        st.markdown("### 🏗️ Proposed Architecture")
        st.code(out["diagram"])

    # Build two reports (Tutorial + TDD) and offer downloads
    tutorial = io.StringIO()
    tutorial.write("# Tutorial: How to Build This Architecture from Scratch\n\n")
    tutorial.write(f"Generated: {datetime.utcnow().isoformat()}Z\n\n")
    tutorial.write("## Steps\n")
    tutorial.write("1) Create S3 buckets (raw, processed) with lifecycle policies.\n")
    tutorial.write("2) Set up IAM roles & KMS keys (least privilege, encryption).\n")
    tutorial.write("3) Ingestion via Kinesis/Data Streams (if low latency needed).\n")
    tutorial.write("4) Glue/Spark ETL to curated zone; partition by time/business key.\n")
    tutorial.write("5) Register features in Feature Store; version datasets.\n")
    tutorial.write("6) Train with SageMaker; track experiments and artifacts.\n")
    tutorial.write("7) Register model in Model Registry; promote via stages.\n")
    tutorial.write("8) Deploy real-time endpoint; add autoscaling per traffic.\n")
    tutorial.write("9) Monitor with CloudWatch + Model Monitor; alerts on drift/latency.\n")
    tutorial.write("10) Expose APIs with API Gateway + Lambda; secure with IAM/authorizers.\n")

    tdd = io.StringIO()
    tdd.write("# Technical Design Document (TDD)\n\n")
    tdd.write(f"Generated: {datetime.utcnow().isoformat()}Z\n\n")
    tdd.write("## Non-functional priorities\n")
    tdd.write(f"- Latency: {latency}/10, Load Bal.: {load_bal}/10, Cost: {cost}/10, Performance: {performance}/10, Security: {security}/10, Scalability: {scalability}/10\n\n")
    tdd.write("## Core AWS Components\n")
    tdd.write("- S3 (Lake), Glue/Spark ETL, Kinesis (optional), DynamoDB or Aurora, API Gateway, Lambda/ECS Fargate, SageMaker, CloudWatch, KMS, Config, Security Hub\n\n")
    tdd.write("## Data Model & Governance\n")
    tdd.write("- Raw/Processed/Curated zones; Lake Formation; data tags for PII; column-level encryption where needed.\n\n")
    tdd.write("## Security & Zero Trust\n")
    tdd.write("- Least privilege IAM, VPC endpoints, KMS-encrypted storage & streams, audit via CloudTrail.\n\n")
    tdd.write("## MLOps\n")
    tdd.write("- Feature store, experiment tracking, model registry, canary/blue-green deployments, continuous monitoring.\n")

    st.download_button("📥 Download Tutorial (TXT)", tutorial.getvalue(), file_name="tutorial_build_steps.txt")
    st.download_button("📥 Download Technical Design Doc (TXT)", tdd.getvalue(), file_name="technical_design_document.txt")

st.markdown("---")

# ---------- Red clickable box for value chain blog ----------
with st.expander("🟥  Click Here to Know Architecture Value Chain ROI for Vendors & Clients", expanded=False):
    st.markdown(
        """
**Sand → Silicon → Wafer → Chip → Cloud Hardware (GPU/CPU) → AWS Services → SaaS App → End User price.**

If a user pays **₹100** to a SaaS app:
- **Chip & infra makers** (fabs, GPU vendors): ~₹20–30  
- **Cloud provider** (compute, storage, network): ~₹25–35  
- **Platform & tools** (monitoring, CI, security): ~₹10–15  
- **SaaS company** (R&D, ops, sales, margin): ~₹20–35  

Numbers vary by workload, compliance, and scale.
"""
    )

st.markdown("---")

# ---------- Agents vs Humans table ----------
st.markdown("### 🧑‍🤝‍🧑 Agents vs Humans — what’s similar, what’s different?")
tbl = pd.DataFrame(
    [
        ["Data Architect Sophia", "Fast pattern recognition; consistent templates; never forgets governance checklists."],
        ["Security Architect Emilia", "Instant Zero Trust guardrails; constant policy reminders; exhaustive audit points."],
        ["Solution Architect Kumar", "Rapid trade-off matrices; HA patterns on demand; cost visibility from templates."],
        ["AI Architect Amit", "Suggests MLOps scaffolding; flags drift/latency risks; proposes A/B and canary."],
    ],
    columns=["Agent / Human", "Advantages (2–3)"],
)
st.table(tbl)
st.caption("Note: Agents here are **simulated**. Production setups should mix human review + automated design checks.")

# ---------- Friendly footer ----------
st.markdown("---")
st.markdown(
    "<div style='text-align:center; opacity:0.8'>Built for portfolios — free & open source. Deploy on Streamlit Community Cloud.</div>",
    unsafe_allow_html=True,
)
