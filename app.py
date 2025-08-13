import time
from typing import Dict, List
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# -----------------------------
# Page config + light CSS
# -----------------------------
st.set_page_config(
    page_title="AWS Architecture Design Using Agentic AI Agents (MVP)",
    page_icon="🛠️",
    layout="wide"
)

BADGE = """
<style>
.badge{display:inline-block;padding:.25rem .6rem;border-radius:999px;font-size:.78rem;
background:#eef2ff;color:#3730a3;margin-right:.35rem;border:1px solid #c7d2fe}
.badge.gray{background:#f1f5f9;color:#0f172a;border-color:#e2e8f0}
.badge.green{background:#ecfdf5;color:#065f46;border-color:#a7f3d0}
.badge.purple{background:#f5f3ff;color:#5b21b6;border-color:#ddd6fe}
.boxlink{display:inline-block;padding:.55rem .8rem;border-radius:.6rem;border:2px solid #ef4444;
background:#fff5f5;color:#b91c1c;font-weight:700;text-decoration:none}
.card{background:#ffffff;border:1px solid #e5e7eb;border-radius:16px;padding:14px}
.card h4{margin-top:0}
.agent{background:#f8fafc;border:1px dashed #cbd5e1;border-radius:16px;padding:12px}
.kpi{background:#f1f5f9;border-radius:12px;padding:.35rem .6rem;display:inline-block;margin-right:.4rem}
.footer-note{background:#fff7ed;border:1px solid #fed7aa;border-radius:10px;padding:8px 12px;color:#7c2d12}
.steps h4{margin-top:0}
.steps li{margin:.35rem 0}
hr.soft{border:none;border-top:1px solid #e5e7eb;margin:18px 0}
</style>
"""
st.markdown(BADGE, unsafe_allow_html=True)

# -----------------------------
# Session state
# -----------------------------
for k, v in {
    "use_case": "Retail platform with real-time recommendations, low latency APIs, and global traffic.",
    "focus": "AI/ML",
    "ran": False,
    "agent_logs": {},
    "agent_summaries": {},
    "arch_nodes": [],
    "weights": dict(latency=6, load=6, cost=5, perf=6, security=7, scale=7)
}.items():
    st.session_state.setdefault(k, v)

# -----------------------------
# Helpers
# -----------------------------
FOCI = ["AI/ML", "Serverless", "Data & Analytics", "Zero Trust", "Microservices", "API Platform"]

def weight(v):  # map 0-10 slider to 0..1
    return max(0, min(1, (v / 10.0)))

def pick_components(focus: str, w: Dict[str, int]) -> List[str]:
    """Rule-based (free) component chooser influenced by sliders."""
    L = []
    lat, ld, cost, perf, sec, scl = (w["latency"], w["load"], w["cost"], w["perf"], w["security"], w["scale"])

    if focus == "AI/ML":
        L = ["Data", "Amazon S3", "AWS Glue", "SageMaker (Train)", "Model Registry",
             "SageMaker Endpoint", "CloudWatch/Model Monitor"]
    elif focus == "Serverless":
        L = ["Client", "Amazon CloudFront", "API Gateway", "AWS Lambda", "Amazon DynamoDB",
             "SQS/SNS", "Step Functions", "CloudWatch"]
    elif focus == "Data & Analytics":
        L = ["Ingestion", "Kinesis/Kinesis Firehose", "Amazon S3 (Data Lake)", "AWS Glue",
             "Amazon Athena", "Amazon Redshift", "Quicksight"]
    elif focus == "Zero Trust":
        L = ["Client", "Amazon CloudFront + WAF", "Amazon Cognito", "Private VPC",
             "AWS IAM + SCP", "Security Hub + GuardDuty", "CloudTrail/Config", "KMS"]
    elif focus == "Microservices":
        L = ["Client", "ALB", "ECS Fargate/EKS", "App Mesh", "Cloud Map",
             "Aurora/RDS", "ElastiCache", "CloudWatch"]
    else:  # API Platform
        L = ["Client", "API Gateway", "Lambda/ECS/EKS", "Cognito", "WAF/Shield",
             "Usage Plans + Throttling", "CloudWatch + X-Ray"]

    # Adjustments by priorities
    if weight(lat) >= 0.7:
        if "Amazon CloudFront" not in L: L.insert(1, "Amazon CloudFront")
        if "Global Accelerator" not in L: L.append("Global Accelerator")
    if weight(ld) >= 0.6:
        if "ALB" not in L: L.insert(1, "ALB")
    if weight(cost) >= 0.7:
        # prefer cheaper lake/serverless
        if "Amazon Redshift" in L: L[L.index("Amazon Redshift")] = "Athena (serverless)"
        if "ECS Fargate/EKS" in L: L[L.index("ECS Fargate/EKS")] = "Lambda/ECS mix"
    if weight(perf) >= 0.7:
        if "ElastiCache" not in L: L.append("ElastiCache")
        if "Aurora/RDS" in L: L[L.index("Aurora/RDS")] = "Aurora (Performance)"
    if weight(sec) >= 0.7:
        for x in ["WAF/Shield", "KMS", "CloudTrail/Config"]:
            if x not in L: L.append(x)
    if weight(scl) >= 0.7:
        if "Auto Scaling" not in L: L.append("Auto Scaling")
    return L

def build_dot(nodes: List[str]) -> str:
    # Simple left-to-right chain
    parts = ['digraph G { rankdir=LR; node [shape=rounded, style="rounded,filled", color="#9ca3af", fillcolor="white"];']
    for i, n in enumerate(nodes):
        safe = n.replace('"', "'")
        parts.append(f'  n{i} [label="{safe}"];')
    for i in range(len(nodes)-1):
        parts.append(f'  n{i} -> n{i+1};')
    parts.append("}")
    return "\n".join(parts)

def agent_think(name: str, use_case: str, focus: str, nodes: List[str]) -> Dict[str, str]:
    """Simulated deliberate thinking."""
    steps = {
        "Step 1": f"Understanding the problem statement: “{use_case}”.",
        "Step 2": f"Key concerns based on focus ‘{focus}’: " + (
            "data quality, ingestion throughput" if name.startswith("Data") else
            "audit logging, encryption" if name.startswith("Security") else
            "reliability, scalability" if name.startswith("Solution") else
            "model drift, feature engineering"
        ),
        "Step 3": f"Candidate AWS components: {', '.join(nodes[:5])} ...",
        "Step 4": "Reasoning: prefer managed services, version data/models, enable monitoring."
    }
    summary = f"{name} recommends: " + ", ".join(nodes[:6]) + ". Notes: version artifacts, automate pipelines, monitor drift/latency."
    return {"steps": steps, "summary": summary}

def compose_tutorial(use_case: str, focus: str, nodes: List[str]) -> str:
    return (
f"""Tutorial — Build it from scratch

Use case: {use_case}
Focus: {focus}

1) Create an AWS account + Org + set SCP guardrails (deny root usage, regions you don't use).
2) Design VPC (CIDR, subnets, NAT, endpoints). Lock down with Security Groups + NACLs.
3) Set up IAM: roles for CI/CD, read-only audit, least-privilege per service.
4) Create logging/monitoring baseline: CloudTrail, Config, CloudWatch metrics + alarms, X-Ray.
5) Data layer: provision {nodes[1] if len(nodes)>1 else 'Amazon S3'} and define bucket structure and KMS keys.
6) Compute/control plane: enable {', '.join([n for n in nodes if 'SageMaker' in n or 'Lambda' in n or 'ECS' in n or 'EKS' in n][:2])} with least-privilege roles.
7) Networking edge: set CloudFront/WAF if exposed to internet; add ALB/API Gateway as needed.
8) Pipeline: use CodePipeline/GitHub Actions to deploy infra as code (CDK/Terraform).
9) Observability: dash for latency, error %, cold starts, cost.
10) Run game-day tests; document SLOs and rollback.
"""
).strip()

def compose_tdd(use_case: str, focus: str, nodes: List[str], weights: Dict[str, int]) -> str:
    return (
f"""Technical Design Document (TDD)

Use case
--------
{use_case}

Architecture focus: {focus}

Quality attributes (0-10): 
- latency={weights['latency']}  load_balancing={weights['load']}  cost={weights['cost']}
- performance={weights['perf']}  security={weights['security']}  scalability={weights['scale']}

Core components
---------------
{', '.join(nodes)}

Security
--------
KMS for encryption, IAM least-privilege, WAF/Shield at edge, CloudTrail/Config for audit.

Availability & Scale
--------------------
Multi-AZ where applicable; ALB/Auto Scaling or managed endpoints; caching with ElastiCache.

Data/ML
-------
Versioned artifacts, lineage, monitoring (drift/latency). Disaster recovery: S3 CRR if needed.

Costs
-----
Prefer serverless/managed where feasible; tag all resources; budget alarms; use S3+Athena for ad-hoc.

Risks
-----
Misconfigured IAM, unbounded costs, model drift, underprovisioned concurrency.

"""
).strip()

def value_chain_df():
    rows = [
        ("Sand/Quartz Mining & Refining", 1),
        ("Wafer Fabrication (Foundry — e.g., TSMC)", 8),
        ("IP/EDA Tools (Design toolchains)", 3),
        ("Chip Packaging & OSAT", 2),
        ("Server OEM / GPU Vendors (e.g., NVIDIA, AMD)", 10),
        ("Cloud Provider (e.g., AWS)", 15),
        ("Networking & CDN/ISP", 5),
        ("SaaS Platform Engineering", 18),
        ("SaaS Infrastructure Ops (SRE/Monitoring)", 4),
        ("Third-party Services/APIs", 4),
        ("Payment Processing/Fees", 3),
        ("App Stores/Distribution", 2),
        ("Sales/Marketing/Customer Success", 11),
        ("Taxes/Compliance/Legal", 5),
        ("Corporate Overheads", 4),
        ("Profit Margin", 5),
    ]
    df = pd.DataFrame(rows, columns=["Stage", "₹ Share"])
    df["% of ₹100"] = df["₹ Share"].astype(str) + "%"
    return df

# -----------------------------
# Header
# -----------------------------
st.markdown("<h1>🧭 AWS Architecture Design Using Agentic AI Agents</h1>", unsafe_allow_html=True)
st.markdown(
    '<span class="badge green">2050-ready</span>'
    '<span class="badge purple">Agentic AI (simulated)</span>'
    '<span class="badge gray">Zero-cost — Free GitHub + Free Streamlit</span>', 
    unsafe_allow_html=True
)

st.markdown("")

# -----------------------------
# Top Controls (Radar + Input)
# -----------------------------
left, right = st.columns([1, 1.2], gap="large")

with left:
    st.subheader("Priorities (adjust)")
    st.caption("These sliders shape design choices.")
    w = st.session_state["weights"]
    w["latency"]  = st.slider("Latency (speed needs)", 0, 10, w["latency"])
    w["load"]     = st.slider("Load Balancing",       0, 10, w["load"])
    w["cost"]     = st.slider("Cloud Cost Sensitivity",0,10, w["cost"])
    w["perf"]     = st.slider("Performance / Throughput",0,10, w["perf"])
    w["security"] = st.slider("Security / Compliance",0,10, w["security"])
    w["scale"]    = st.slider("Scalability / Elasticity",0,10, w["scale"])

    # live radar
    categories = ["Latency","Load","Cost","Performance","Security","Scalability"]
    vals = [w["latency"], w["load"], w["cost"], w["perf"], w["security"], w["scale"]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals + [vals[0]], theta=categories + [categories[0]], fill='toself', name='Priorities'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,10])), showlegend=False, margin=dict(l=10,r=10,t=10,b=10), height=300)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Input")
    st.caption("Type or Paste Use Case / RFP / Epic user story")

    st.session_state.use_case = st.text_area(
        " ",  # blank label
        st.session_state.use_case,
        height=110,
        key="use_case_box"
    )

    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        if st.button("🛍️ Retail AI Recommender", use_container_width=True):
            st.session_state.use_case = "Retail platform with real-time recommendations, low latency APIs, and global traffic."
            st.session_state.focus = "AI/ML"
            st.rerun()
    with c2:
        if st.button("🏥 Healthcare Zero Trust", use_container_width=True):
            st.session_state.use_case = "Healthcare system to store patient records with strict Zero Trust, audit trails, and secure analytics."
            st.session_state.focus = "Zero Trust"
            st.rerun()
    with c3:
        if st.button("🌐 Global Supply Chain", use_container_width=True):
            st.session_state.use_case = "Global supply chain forecasting with event ingestion, anomaly detection, and cross-region replication."
            st.session_state.focus = "Data & Analytics"
            st.rerun()

    st.selectbox("Architecture Focus", FOCI, index=FOCI.index(st.session_state.focus), key="focus")

    st.markdown(
        '<a class="boxlink" href="#value-chain-roi">Click Here to Know Architecture Value Chain ROI for Vendors & Clients</a>',
        unsafe_allow_html=True
    )

# Run / Refresh buttons
r1, r2 = st.columns([1.1, 0.9])
with r1:
    run_clicked = st.button("▶️ Run Agents & Generate Architecture", type="primary", use_container_width=True)
with r2:
    if st.button("↻ Start New Architecture", use_container_width=True):
        # clear outputs, keep UI selections
        for k in ["ran", "agent_logs", "agent_summaries", "arch_nodes"]:
            st.session_state[k] = {} if 'logs' in k or 'summaries' in k else ([] if 'nodes' in k else False)
        st.rerun()

st.markdown("<hr class='soft'/>", unsafe_allow_html=True)

# -----------------------------
# Run agents (simulated thinking)
# -----------------------------
if run_clicked:
    st.session_state.ran = True
    nodes = pick_components(st.session_state.focus, st.session_state.weights)
    st.session_state.arch_nodes = nodes

    names = ["Data Architect Sophia", "Security Architect Emilia", "Solution Architect Kumar", "AI Architect Amit"]
    cols = st.columns(4, gap="small")
    st.info("Agents are working… watch the live thinking below.", icon="🧠")

    st.session_state.agent_logs, st.session_state.agent_summaries = {}, {}

    for i, name in enumerate(names):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"**{name}**")
                out = agent_think(name, st.session_state.use_case, st.session_state.focus, nodes)
                st.session_state.agent_logs[name] = out["steps"]
                st.session_state.agent_summaries[name] = out["summary"]
                for step, text in out["steps"].items():
                    st.write(f"{step}: {text}")
                    time.sleep(0.15)  # small delay to feel "human"
                st.success(out["summary"])

# -----------------------------
# Consolidated report + Diagram (always shown after run)
# -----------------------------
if st.session_state.ran:
    st.markdown("### Proposed Architecture")
    dot = build_dot(st.session_state.arch_nodes or ["Input","Design"])
    st.graphviz_chart(dot, use_container_width=True)

    # Consolidated narrative
    st.markdown("#### Consolidated Architecture Report")
    narrative = " • ".join([v for _, v in st.session_state.agent_summaries.items()])
    st.write(f"**Use case:** {st.session_state.use_case}")
    st.write(f"**Focus:** {st.session_state.focus}")
    st.write(narrative)

    # Downloads
    tutorial_txt = compose_tutorial(st.session_state.use_case, st.session_state.focus, st.session_state.arch_nodes)
    tdd_txt = compose_tdd(st.session_state.use_case, st.session_state.focus, st.session_state.arch_nodes, st.session_state.weights)

    cdl1, cdl2 = st.columns(2)
    with cdl1:
        st.download_button("📥 Download Tutorial (TXT)", tutorial_txt, file_name="tutorial_build_from_scratch.txt", mime="text/plain", use_container_width=True)
    with cdl2:
        st.download_button("📥 Download Technical Design Doc (TXT)", tdd_txt, file_name="technical_design_document.txt", mime="text/plain", use_container_width=True)

st.markdown("<hr class='soft'/>", unsafe_allow_html=True)

# -----------------------------
# Agents vs Humans quick table
# -----------------------------
st.markdown("#### 🤝 Agents vs Humans — what’s similar, what’s different?")
tbl = pd.DataFrame([
    ["Data Architect Sophia", "Fast patterns recognition; consistent templates; never forgets governance checklists."],
    ["Security Architect Emilia", "Instant Zero Trust guardrails; constant policy reminders; exhaustive audit points."],
    ["Solution Architect Kumar", "Rapid trade-off matrices; HA patterns on demand; cost visibility from templates."],
    ["AI Architect Amit", "Suggests MLOps scaffolding; flags drift/latency risks; proposes A/B and canary."],
], columns=["Agent / Human", "Advantages (2–3)"])
st.dataframe(tbl, use_container_width=True, hide_index=True)

st.markdown("<hr class='soft'/>", unsafe_allow_html=True)

# -----------------------------
# Value Chain ROI section (anchor target)
# -----------------------------
st.markdown('<a name="value-chain-roi"></a>', unsafe_allow_html=True)
st.markdown("### 📊 Architecture Value Chain ROI (₹100 example) — who gets what?")
vc = value_chain_df()
st.dataframe(vc, use_container_width=True, hide_index=True)
st.caption("Illustrative only. Shares vary by company, workload, and region.")

st.markdown("<hr class='soft'/>", unsafe_allow_html=True)

# -----------------------------
# Long, simple How-to (for non-engineers)
# -----------------------------
st.markdown("### 📚 How to Use this Web App — step by step (easy mode)")
st.markdown(
    """
<div class="steps card">
<ol>
<li>Read the title: this tool drafts an AWS architecture using four “human-like” agents.</li>
<li>Look at the six sliders on the left (speed, load, cost, performance, security, scale).</li>
<li>Move sliders to show what matters most to you.</li>
<li>On the right, type or paste your Use Case (what you want to build).</li>
<li>Pick an “Architecture Focus” (e.g., AI/ML, Serverless).</li>
<li>Optionally click a preset (Retail, Healthcare, Supply Chain) to auto-fill the text.</li>
<li>Click “Run Agents & Generate Architecture”.</li>
<li>Watch four boxes: Sophia, Emilia, Kumar, Amit think step-by-step.</li>
<li>Each box shows what they understand, worry about, propose, and why.</li>
<li>Scroll down to see “Proposed Architecture” diagram (always visible).</li>
<li>Below the diagram is a clear, consolidated summary.</li>
<li>Click “Download Tutorial (TXT)” to get a build guide, step-by-step.</li>
<li>Click “Download Technical Design Doc (TXT)” to get a TDD summary.</li>
<li>Want to start again? Click “Start New Architecture”.</li>
<li>Change sliders and text to explore different trade-offs.</li>
<li>Latency high? Tool prefers CloudFront/Accelerator/caching.</li>
<li>Security high? Tool adds KMS, WAF, GuardDuty, CloudTrail/Config.</li>
<li>Cost high? Tool leans to serverless (Athena/Lambda).</li>
<li>Performance high? Tool suggests Aurora (Performance), ElastiCache.</li>
<li>Scale high? Tool includes Auto Scaling and global edge options.</li>
<li>For microservices, look for ECS/EKS, App Mesh, ALB.</li>
<li>For AI/ML, look for S3, SageMaker, Model Monitor.</li>
<li>Value chain ROI table shows how ₹100 in SaaS travels across the stack.</li>
<li>This MVP uses no paid APIs; all logic is local and rule-based.</li>
<li>Use outputs in resumes/portfolios (note: simulated agents).</li>
<li>Discuss with interviewers: which trade-offs would you change and why?</li>
<li>Export TXT files and attach them to your job applications.</li>
<li>Iterate quickly; short use cases work best.</li>
<li>Prefer explicit requirements (SLOs, PII rules, regions) for cleaner results.</li>
<li>Remember to tag resources and set budget alarms in real projects.</li>
<li>Add CI/CD and IaC (CDK/Terraform) when you move past this MVP.</li>
<li>Plan game-days and chaos drills for reliability.</li>
<li>Review security with a human; this tool is a fast starting point.</li>
<li>Keep diagrams simple and readable for executives.</li>
<li>When done, use “Start New Architecture” to reset and design another.</li>
</ol>
</div>
""",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='footer-note'>Thought Leadership: agentic patterns make architecture explainable and repeatable. Humans stay on strategy & empathy while agents handle guardrails and templates. MVP only — Streamlit-friendly, zero credentials.</p>",
    unsafe_allow_html=True
)
