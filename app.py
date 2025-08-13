import streamlit as st
import textwrap
from datetime import datetime

# -----------------------------
# App config & tiny helpers
# -----------------------------
st.set_page_config(
    page_title="AWS Architecture Design — Agentic AI (Free)",
    page_icon="🧠",
    layout="wide",
)

def pill(text, color_bg="#eef6ff", color_text="#0b5fff"):
    st.markdown(
        f"""
        <span style="
            background:{color_bg};
            color:{color_text};
            padding:4px 10px;
            border-radius:999px;
            font-size:12px;
            margin-right:6px;
            display:inline-block;
        ">{text}</span>
        """,
        unsafe_allow_html=True,
    )

def red_link_box(label, anchor):
    st.markdown(
        f"""
        <a href="#{anchor}" style="
          text-decoration:none;
          display:inline-block;
          background:#ffe6e6;
          color:#b00020;
          padding:10px 14px;
          border:2px solid #ffb3b3;
          border-radius:12px;
          font-weight:600;
        ">{label}</a>
        """,
        unsafe_allow_html=True,
    )

def section_title(icon, title):
    st.markdown(
        f"""<div style="font-size:22px;font-weight:700;margin:6px 0 6px 0;">
        {icon}&nbsp; {title}
        </div>""",
        unsafe_allow_html=True,
    )

def as_bullets(lines):
    return "\n".join([f"- {l}" for l in lines])

# -----------------------------
# Session State
# -----------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "agents_log" not in st.session_state:
    st.session_state.agents_log = []
if "diagram_dot" not in st.session_state:
    st.session_state.diagram_dot = None
if "tutorial_text" not in st.session_state:
    st.session_state.tutorial_text = None
if "tdd_text" not in st.session_state:
    st.session_state.tdd_text = None

# -----------------------------
# Sidebar — How to Use
# -----------------------------
with st.sidebar:
    st.markdown("### 🧭 How to Use")
    st.markdown(as_bullets([
        "Paste your **Use Case / RFP / Epic**.",
        "Adjust the **Radar sliders** (latency, cost, security, etc.).",
        "Click **Run Agents** — watch **Sophia, Emilia, Kumar, Amit** think in real time.",
        "See the **Proposed Architecture** diagram.",
        "Download the **Tutorial** and **Technical Design Document**.",
        "Click **Start New Architecture** to refresh and design another.",
    ]))
    st.divider()
    st.markdown("**Tip:** Short & specific inputs produce crisp architectures.")

# -----------------------------
# Header tags
# -----------------------------
pill("2050-ready", "#e6fff3", "#007a4d")
pill("Agentic AI (simulated)", "#eef6ff", "#0b5fff")
pill("Zero-cost — Free GitHub + Free Streamlit", "#f2ecff", "#5e35b1")

# -----------------------------
# Input + Radar
# -----------------------------
section_title("📝", "Input")

# Radar parameters (6) — sliders that influence architecture
col_r1, col_r2, col_r3 = st.columns([1,1,1])
with col_r1:
    latency = st.slider("Latency (speed needs)", 0, 10, 7, help="Higher = lower latency required")
with col_r2:
    load_bal = st.slider("Load Balancing", 0, 10, 6)
with col_r3:
    cloud_cost = st.slider("Cloud Cost Sensitivity", 0, 10, 5, help="Higher = more cost conscious")

col_r4, col_r5, col_r6 = st.columns([1,1,1])
with col_r4:
    performance = st.slider("Performance / Throughput", 0, 10, 7)
with col_r5:
    security = st.slider("Security / Compliance", 0, 10, 8)
with col_r6:
    scalability = st.slider("Scalability / Elasticity", 0, 10, 7)

st.caption("These sliders shape the design choices the agents will make.")

# Use case text
use_case = st.text_area(
    "Paste Use Case / RFP / Epic user story",
    value="Retail platform with real-time recommendations, low latency APIs, and global traffic.",
    height=110,
    placeholder="e.g., Global supply chain analytics platform; AI inference; streaming ingestion; strict Zero Trust...",
)

# Quick example buttons
col_ex1, col_ex2, col_ex3 = st.columns([1,1,1])
with col_ex1:
    if st.button("🛒 Retail AI Recommender", use_container_width=True):
        st.session_state.result = None
        st.session_state.agents_log = []
        st.session_state.diagram_dot = None
        st.session_state.tutorial_text = None
        st.session_state.tdd_text = None
        st.session_state.prefill = "Retail platform with real-time recommendations, low latency APIs, and global traffic."
        st.rerun()
with col_ex2:
    if st.button("🏥 Healthcare Zero Trust", use_container_width=True):
        st.session_state.result = None
        st.session_state.agents_log = []
        st.session_state.diagram_dot = None
        st.session_state.tutorial_text = None
        st.session_state.tdd_text = None
        st.session_state.prefill = "Healthcare system to store patient records with strict Zero Trust, audit trails, and secure analytics."
        st.rerun()
with col_ex3:
    if st.button("📦 Global Supply Chain", use_container_width=True):
        st.session_state.result = None
        st.session_state.agents_log = []
        st.session_state.diagram_dot = None
        st.session_state.tutorial_text = None
        st.session_state.tdd_text = None
        st.session_state.prefill = "Global supply chain platform for forecasting, event ingestion, and anomaly detection."
        st.rerun()

# If prefill was set by a button above, show it and clear the flag
if "prefill" in st.session_state:
    use_case = st.session_state.prefill
    del st.session_state["prefill"]

st.markdown(
    "<div style='margin-top:6px;color:#6b7280'>"
    "💡 Instruction: Type **any AWS architecture or app** you want to build. "
    "Adjust the sliders to express your priorities (security, cost, latency, etc.).</div>",
    unsafe_allow_html=True,
)

# Clickable red box (renamed mini blog)
red_link_box("Click Here to Know Architecture Value Chain ROI for Vendors & Clients", "value-chain-roi")

st.write("")

# -----------------------------
# Agentic AI (simulated) — 4 agents
# -----------------------------
def log(agent, msg):
    st.session_state.agents_log.append((agent, msg))

def design_choices_from_radar():
    choices = []
    if security >= 7:
        choices += ["IAM guardrails", "least-privilege roles", "AWS WAF", "VPC isolation", "KMS encryption", "CloudTrail"]
    if latency >= 7:
        choices += ["Global Accelerator", "API Gateway + Lambda", "Edge caching (CloudFront)"]
    if performance >= 7:
        choices += ["Autoscaling groups", "Graviton compute", "SageMaker endpoints for real-time"]
    if scalability >= 7:
        choices += ["EKS/ECS with Fargate", "SQS buffering", "Event-driven decoupling"]
    if load_bal >= 6:
        choices += ["ALB/NLB", "Multi-AZ", "Blue/Green or Canary deploys"]
    if cloud_cost >= 7:
        choices += ["S3 IA/Glacier", "Spot instances", "Savings Plans"]
    return list(dict.fromkeys(choices))  # unique order-preserving

def run_agents(use_case_text):
    # Data Architect Sophia
    log("Data Architect Sophia", "Analyzing data sources, storage, and analytics needs…")
    data_recs = [
        "Amazon S3 (raw + curated buckets)",
        "AWS Glue Data Catalog",
        "Amazon Athena (ad-hoc SQL)",
    ]
    if "stream" in use_case_text.lower() or "real-time" in use_case_text.lower():
        data_recs.append("Amazon Kinesis (data streams)")
    if "recommend" in use_case_text.lower() or "ml" in use_case_text.lower():
        data_recs.append("Feature Store on S3 + Glue")
    log("Data Architect Sophia", f"Data stack: {', '.join(data_recs)}")

    # Security Architect Emilia
    log("Security Architect Emilia", "Applying Zero Trust, encryption, and governance…")
    sec_recs = ["KMS encryption", "CloudTrail + GuardDuty", "AWS WAF", "Private subnets + VPC endpoints"]
    if security >= 8:
        sec_recs.append("Macie (PII discovery)")
    log("Security Architect Emilia", f"Security stack: {', '.join(sec_recs)}")

    # Solution Architect Kumar
    log("Solution Architect Kumar", "Selecting core compute, APIs, and messaging…")
    sol_recs = ["API Gateway", "AWS Lambda", "SQS", "SNS"]
    if performance >= 7 or scalability >= 7:
        sol_recs.append("EKS (Fargate) or ECS (Fargate)")
    if latency >= 7:
        sol_recs.append("CloudFront + Global Accelerator")
    log("Solution Architect Kumar", f"Solution stack: {', '.join(sol_recs)}")

    # AI Architect Amit
    log("AI Architect Amit", "Designing model training/serving & MLOps…")
    ai_recs = []
    if "recommend" in use_case_text.lower() or "ml" in use_case_text.lower() or "anomaly" in use_case_text.lower():
        ai_recs = ["Amazon SageMaker (train)", "Model Registry", "SageMaker Endpoint (real-time)", "CloudWatch Model Monitor"]
    log("AI Architect Amit", f"AI/ML stack: {', '.join(ai_recs) if ai_recs else 'Not required for this use case'}")

    # Combine with radar-driven choices
    radar = design_choices_from_radar()
    log("All Agents", f"Adjusted by priorities (sliders): {', '.join(radar) if radar else 'no special constraints'}")

    # Return a consolidated result
    return {
        "data": data_recs,
        "security": sec_recs,
        "solution": sol_recs,
        "ai": ai_recs,
        "radar": radar,
    }

def make_dot(result):
    # Simple DOT diagram assembled from chosen services
    nodes = [
        ("Data", "Data"),
        ("S3", "Amazon S3"),
        ("Glue", "AWS Glue"),
        ("Athena", "Amazon Athena"),
    ]
    edges = [("Data", "S3"), ("S3", "Glue"), ("Glue", "Athena")]

    if "Amazon Kinesis (data streams)" in result["data"]:
        nodes.append(("Kinesis", "Amazon Kinesis"))
        edges.insert(0, ("Data", "Kinesis"))
        edges.insert(1, ("Kinesis", "S3"))

    # Solution layer
    if "API Gateway" in result["solution"]:
        nodes.append(("APIGW", "API Gateway"))
        edges.append(("Athena", "APIGW"))
    if "AWS Lambda" in result["solution"]:
        nodes.append(("Lambda", "Lambda"))
        edges.append(("APIGW", "Lambda"))
    if any("EKS" in s or "ECS" in s for s in result["solution"]):
        nodes.append(("EKS", "EKS/ECS (Fargate)"))
        edges.append(("Lambda", "EKS"))
    if "CloudFront + Global Accelerator" in result["solution"]:
        nodes.append(("Edge", "CloudFront/GA"))
        edges.insert(0, ("Edge", "APIGW"))

    # AI
    if result["ai"]:
        nodes += [("SMTrain","SageMaker (Train)"), ("Reg","Model Registry"), ("SMRT","SageMaker Endpoint"), ("CW","CloudWatch/Model Monitor")]
        edges += [("S3","SMTrain"), ("SMTrain","Reg"), ("Reg","SMRT"), ("SMRT","CW")]

    # Security (represented as a guardrail node)
    if "AWS WAF" in result["security"]:
        nodes.append(("WAF","AWS WAF"))
        edges.insert(0, ("WAF","Edge" if any(n[0]=="Edge" for n in nodes) else "APIGW"))

    # Build DOT
    dot_lines = ['digraph G {', 'rankdir=LR;', 'node [shape=box, style="rounded,filled", color="#333333", fillcolor="#ffffff"];']
    for nid, label in nodes:
        dot_lines.append(f'"{nid}" [label="{label}"];')
    for a,b in edges:
        dot_lines.append(f'"{a}" -> "{b}";')
    dot_lines.append("}")
    return "\n".join(dot_lines)

def build_tutorial_and_tdd(use_case_text, result):
    radar_txt = f"""Priorities
- Latency: {latency}/10
- Load Balancing: {load_bal}/10
- Cost Sensitivity: {cloud_cost}/10
- Performance: {performance}/10
- Security: {security}/10
- Scalability: {scalability}/10
"""

    tutorial = f"""
Title: How to Build This Architecture (Step-by-Step)

Use Case
--------
{use_case_text}

{radar_txt}

1) Create S3 buckets (raw, curated). Enable default SSE-S3 or KMS.
2) Set up AWS Glue Data Catalog and crawlers for S3 datasets.
3) (If streaming) Create Kinesis stream and producers; connect to S3 sink.
4) Use Athena for ad-hoc SQL and reporting on curated S3 data.
5) Expose APIs with API Gateway; connect to Lambda for business logic.
6) (If needed) Deploy EKS/ECS with Fargate for microservices/long-running tasks.
7) Add SQS/SNS for async decoupling between services.
8) Put CloudFront (and Global Accelerator if global) in front of APIs/UI for low-latency.
9) Security: WAF on edge, IAM least-privilege, VPC endpoints, CloudTrail + GuardDuty, KMS everywhere.
10) (If AI/ML) Use SageMaker to train, register models, deploy real-time endpoints, and monitor with Model Monitor.

Validation
----------
- Load tests for latency/perf; scale via autoscaling, EKS/ECS HPA.
- Cost checks with S3 IA/Glacier, Spot, or Savings Plans (if needed).
- Compliance checks with IAM Access Analyzer, Config rules, Security Hub.

"""

    tdd = f"""
Technical Design Document (TDD)

Use Case
--------
{use_case_text}

Core Services
-------------
Data: {', '.join(result['data'])}
Security: {', '.join(result['security'])}
Solution: {', '.join(result['solution'])}
AI/ML: {', '.join(result['ai']) if result['ai'] else 'N/A'}
Adjusted by radar priorities: {', '.join(result['radar']) if result['radar'] else 'None'}

Non-Functional Requirements
---------------------------
- Latency target depends on workload (slider value {latency}/10); Edge acceleration and API Gateway used if high.
- Security emphasis {security}/10 drives WAF, KMS, CloudTrail, GuardDuty, private networking.
- Scalability {scalability}/10 → EKS/ECS on Fargate; decoupling with SQS; multi-AZ.
- Performance {performance}/10 → autoscaling, Graviton, tuning.
- Load balancing {load_bal}/10 → ALB/NLB selection; canary/blue-green where appropriate.
- Cost sensitivity {cloud_cost}/10 → S3 lifecycle, Spot, Savings Plans.

Observability
-------------
- CloudWatch metrics/logs/alarms
- X-Ray for tracing (if enabled)
- Model Monitor for ML drift (if applicable)

"""

    return tutorial.strip(), tdd.strip()

# -----------------------------
# Run Agents button row
# -----------------------------
col_go, col_refresh = st.columns([1,1])
with col_go:
    if st.button("▶️ Run Agents & Generate Architecture", use_container_width=True):
        st.session_state.result = run_agents(use_case)
        st.session_state.diagram_dot = make_dot(st.session_state.result)
        st.session_state.tutorial_text, st.session_state.tdd_text = build_tutorial_and_tdd(use_case, st.session_state.result)

with col_refresh:
    if st.button("🔄 Start New Architecture", type="secondary", use_container_width=True):
        for k in ["result","agents_log","diagram_dot","tutorial_text","tdd_text"]:
            st.session_state[k] = None if k!="agents_log" else []
        st.rerun()

# -----------------------------
# Agents Thinking (visible)
# -----------------------------
st.markdown("#### 🤖 Agents (human-like) — live thinking")
if st.session_state.agents_log:
    for agent, msg in st.session_state.agents_log:
        st.info(f"**{agent}:** {msg}")
else:
    st.caption("Agents will think out loud here after you click **Run Agents & Generate Architecture**.")

# -----------------------------
# Proposed Architecture (renamed) + downloads
# -----------------------------
if st.session_state.diagram_dot:
    section_title("🗺️", "Proposed Architecture")
    # Graphviz diagram (built-in; no extra system package needed on Streamlit Cloud)
    st.graphviz_chart(st.session_state.diagram_dot, use_container_width=True)

    # Downloads
    col_d1, col_d2 = st.columns([1,1])
    with col_d1:
        st.download_button(
            "📘 Download Tutorial (TXT)",
            st.session_state.tutorial_text,
            file_name=f"tutorial_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col_d2:
        st.download_button(
            "📗 Download Technical Design Document (TXT)",
            st.session_state.tdd_text,
            file_name=f"tdd_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

# -----------------------------
# Agents vs Humans table (brief)
# -----------------------------
st.markdown("---")
section_title("🧑‍💻", "Agents vs Humans — what’s similar, what’s different?")
st.table({
    "Agent / Human": [
        "Data Architect Sophia",
        "Security Architect Emilia",
        "Solution Architect Kumar",
        "AI Architect Amit",
    ],
    "Advantages (2–3)": [
        "Fast patterns recognition; consistent templates; never forgets governance checklists.",
        "Instant Zero Trust guardrails; constant policy reminders; exhaustive audit points.",
        "Rapid trade-off matrices; HA patterns on demand; cost visibility from templates.",
        "Suggests MLOps scaffolding; flags drift/latency risks; proposes A/B and canary.",
    ],
})
st.caption("Note: Agents here are simulated. Production setups should mix human review + automated design checks.")

# -----------------------------
# Value-chain ROI (click target)
# -----------------------------
st.markdown('<div id="value-chain-roi"></div>', unsafe_allow_html=True)
st.markdown("### 💰 Architecture Value Chain ROI — Vendors & Clients (quick view)")
st.markdown(as_bullets([
    "Semiconductor to Cloud to SaaS adds value in layers: silicon → data center → managed cloud → platform → app.",
    "If an end user pays ₹100 for a SaaS transaction, **illustrative split** might be: 10–20% infra, 10–15% platform, 20–30% R&D/ops, 10–20% support/sales, remainder margin/taxes.",
    "Design choices (serverless, autoscaling, caching) directly influence infra %, latency, and reliability.",
]))

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    """<div style="margin-top:20px;color:#6b7280">
    Built for free-tier: Streamlit + GitHub. No external APIs. You can copy this repo, deploy, and list the URL on your resume.
    </div>""",
    unsafe_allow_html=True,
)
