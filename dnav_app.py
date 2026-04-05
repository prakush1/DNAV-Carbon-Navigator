import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
import os
import time
import uuid

# --- PATH CONFIG ---
BASE_DIR = Path(__file__).resolve().parent

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="DNAV: Audit-Ready Carbon NAV Engine | April 2026", 
    layout="wide", 
    page_icon="🧬",
    initial_sidebar_state="expanded"
)


# --- GLOBAL STYLES (VISUALLY BALANCED LIGHT MODE) ---
st.markdown("""
    <style>
        /* Comfortable reading baseline */
        html, body, [class*="css"], .stMarkdown, p, div, span, label {
            font-size: 1.15rem !important;
            line-height: 1.65 !important;
            color: #1f2328 !important;
        }
        
        /* Clean Light Workspace */
        [data-testid="stAppViewContainer"] { background-color: #f6f8fa; }
        [data-testid="stHeader"] { background-color: rgba(255,255,255,0.85); }
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #d0d7de;
        }

        /* Header Card */
        .main-header {
            background: #ffffff;
            padding: 28px !important;
            border-radius: 12px;
            border: 1px solid #d0d7de;
            margin-bottom: 25px;
            box-shadow: 0 1px 3px rgba(31,35,40,0.12);
        }
        
        h1 { font-size: 2.4rem !important; font-weight: 700 !important; color: #1f2328 !important; }
        h2 { font-size: 1.9rem !important; color: #0969da !important; margin-top: 25px !important; }
        h3 { font-size: 1.5rem !important; color: #1f2328 !important; }
        
        /* Metrics - prominent but clean */
        [data-testid="stMetricLabel"] {
            font-size: 1.2rem !important;
            font-weight: 500 !important;
            color: #57606a !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 2.4rem !important;
            color: #0969da !important;
            font-weight: 700 !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab"] {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #57606a !important;
        }
        .stTabs [aria-selected="true"] { color: #0969da !important; }
        
        /* Sidebar */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
            color: #1f2328 !important;
            font-size: 1.4rem !important;
        }
        
        [data-testid="stMetricDelta"] svg { fill: #0969da !important; }
        .stAlert p { font-size: 1.1rem !important; color: inherit !important; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

def add_audit_entry(action, detail):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.audit_log.insert(0, f"[{timestamp}] {action}: {detail}")

if "portfolio" not in st.session_state:
    st.session_state.portfolio = None
if "kill_switch" not in st.session_state:
    st.session_state.kill_switch = False
if "walkthrough_active" not in st.session_state:
    st.session_state.walkthrough_active = True
if "fraud_data" not in st.session_state:
    st.session_state.fraud_data = None
if "optimized_portfolio" not in st.session_state:
    st.session_state.optimized_portfolio = None

# --- DEBUG: LOG ROOT PATH ---
if "initial_load" not in st.session_state:
    st.session_state.initial_load = True
    add_audit_entry("PATH_CHECK", f"Root: {BASE_DIR}")

# --- MOCK DATA GENERATOR ---
def generate_demo_data():
    tickers = ["AAPL", "MSFT", "TSLA", "XOM", "BP", "JPM", "GS", "NEE", "C", "BA", "NVIDIA", "VALE", "REL", "PETRB", "BMW", "AMZN", "GOOGL", "META", "BRK.B", "V", "ADBE", "CRM", "AVGO", "TXN"]
    sectors = ["Technology", "Technology", "Consumer Discretionary", "Energy", "Energy", "Financials", "Financials", "Utilities", "Financials", "Industrials", "Technology", "Mining", "Energy", "Energy", "Automotive", "Retail", "Technology", "Technology", "Financials", "Financials", "Technology", "Technology", "Technology", "Technology"]
    vendors = ["MSCI ESG", "Sustainalytics", "S&P Global", "Refinitiv", "SBTi Verified"]
    verification_sites = ["PCAF Portal", "SBTi Registry", "CDP Database", "ISSB Hub"]
    
    indices = np.random.choice(len(tickers), 12, replace=False)
    data = {
        "Ticker": [tickers[i] for i in indices],
        "Sector": [sectors[i] for i in indices],
        "Quantity": np.random.randint(500, 15000, 12),
        "Price_USD": np.round(np.random.uniform(40, 950, 12), 2),
        "Carbon_Intensity_S1_S2": np.round(np.random.normal(250, 180, 12).clip(5, 1500), 1),
        "Industry_Vendor": [np.random.choice(vendors) for _ in range(12)],
        "Verification_Site": [np.random.choice(verification_sites) for _ in range(12)],
        "Audit_Score": np.random.randint(70, 100, 12),
        "Blockchain_ID": [f"0x{uuid.uuid4().hex[:12].upper()}" for _ in range(12)]
    }
    df = pd.DataFrame(data)
    df["Market_Value"] = df["Quantity"] * df["Price_USD"]
    return df

if st.session_state.portfolio is None:
    st.session_state.portfolio = generate_demo_data()

# --- AI OPTIMIZER LOGIC ---
def optimize_portfolio(df):
    new_df = df.copy()
    new_df = new_df.sort_values("Carbon_Intensity_S1_S2", ascending=False)
    new_df.iloc[:3, new_df.columns.get_loc("Quantity")] = (new_df.iloc[:3]["Quantity"] * 0.2).astype(int)
    new_df.iloc[-3:, new_df.columns.get_loc("Quantity")] = (new_df.iloc[-3:]["Quantity"] * 2.5).astype(int)
    new_df["Market_Value"] = new_df["Quantity"] * new_df["Price_USD"]
    return new_df

# --- HEADER (CLEAN LIGHT MODE) ---
def show_header():
    st.markdown(f"""
        <div class="main-header">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h1 style="color: #0969da; margin: 0; font-weight: 700;">🧬 DNAV Carbon Navigator</h1>
                    <p style="color: #57606a; margin-top: 5px; font-size: 1.1rem; font-weight: 400;">Institutional Carbon-NAV Engine & GRC Audit Hub</p>
                </div>
                <div style="text-align: right;">
                    <span style="background: rgba(9, 105, 218, 0.08); color: #0969da; padding: 6px 15px; border-radius: 6px; font-size: 0.85rem; font-weight: 700; border: 1px solid rgba(9, 105, 218, 0.4); white-space: nowrap;">
                        ● GRC COMPLIANT 2026
                    </span>
                    <p style="color: #57606a; margin-top: 10px; font-size: 0.8rem; font-family: monospace;">UUID: {uuid.uuid4().hex[:10].upper()}</p>
                </div>
            </div>
            <div style="display: flex; gap: 40px; margin-top: 20px; border-top: 1px solid #d0d7de; padding-top: 20px;">
                <div style="border-left: 3px solid #0969da; padding-left: 15px;"><b style="font-size: 0.9rem; color: #1f2328;">Project Lead</b><br><span style="color: #57606a; font-size: 0.85rem;">Prakush Shende (AI PM)</span></div>
                <div style="border-left: 3px solid #2da44e; padding-left: 15px;"><b style="font-size: 0.9rem; color: #1f2328;">Logic Tier</b><br><span style="color: #57606a; font-size: 0.85rem;">SFDR 2.0 / PCAF V3 / BRSR</span></div>
                <div style="border-left: 3px solid #9a6700; padding-left: 15px;"><b style="font-size: 0.9rem; color: #1f2328;">System Connectivity</b><br><span style="color: #57606a; font-size: 0.85rem;">Oracle / SAP BTP Hub</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- WALKTHROUGH COMPONENT ---
def show_walkthrough(step_name, description, guide_steps=[]):
    if st.session_state.walkthrough_active:
        with st.expander(f"📖 STEP-BY-STEP GUIDE: {step_name}", expanded=True):
            st.markdown(f"**Context:** {description}")
            if guide_steps:
                st.markdown("**Actionable Steps:**")
                for i, step in enumerate(guide_steps):
                    st.markdown(f"{i+1}. {step}")
            st.caption("💡 Hint: Toggle 'Walkthroughs' in sidebar to hide.")

# --- MAIN APP ---
def main():
    show_header()
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.header("🗺️ Decision Hub")
        jurisdiction = st.selectbox(
            "Regulatory Region", 
            ["EU (SFDR 2.0)", "India (SEBI/BRSR)", "USA (SEC/S-K)", "Global (ISSB/IFRS)"]
        )
        
        icp_defaults = {"EU": 145, "India": 55, "USA": 92}
        default_price = icp_defaults.get(jurisdiction.split(" ")[0], 85)
        carbon_price = st.slider("Carbon Price ($)", 0, 1000, default_price)
        
        st.markdown("---")
        st.session_state.kill_switch = st.toggle("🚫 AI Kill Switch", value=st.session_state.kill_switch)
        st.session_state.walkthrough_active = st.toggle("📖 Interactive Guides", value=st.session_state.walkthrough_active)
        
        if st.button("🔄 Regen Market Data", type="primary", use_container_width=True):
            st.session_state.portfolio = generate_demo_data()
            st.session_state.optimized_portfolio = None
            add_audit_entry("DATA_RESET", "Re-seeded portfolio.")
            st.rerun()

        st.subheader("📜 Session Audit Trail")
        for entry in st.session_state.audit_log[:10]:
            st.caption(f"● {entry}")

    # --- TABS ---
    tabs = st.tabs([
        "📊 Dashboard", 
        "🧪 AI Rebalancer",
        "📡 Connectivity", 
        "🔮 Stress Testing", 
        "🛡️ GRC Sentry", 
        "🗺️ Lineage",
        "📂 Documentation"
    ])

    df = st.session_state.portfolio
    total_mv = df["Market_Value"].sum()
    total_cargo = (df["Market_Value"] / 1e6 * df["Carbon_Intensity_S1_S2"]).sum()
    carbon_liability = total_cargo * carbon_price
    canav = total_mv - carbon_liability
    waci = total_cargo / (total_mv / 1e6)

    # --- TAB 1: DASHBOARD ---
    with tabs[0]:
        show_walkthrough(
            "Portfolio Health Check",
            "Comparing Fair Value NAV vs Carbon-Adjusted NAV (caNAV).",
            ["Wait for metrics to load.", "Examine the 2030 Temperature alignment."]
        )
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Financial NAV", f"${total_mv/1e6:,.1f}M")
        c1.metric("caNAV (Adjusted)", f"${canav/1e6:,.1f}M", delta=f"{(canav/total_mv-1)*100:.1f}%")
        
        c2.metric("WACI (tCO2e/$M)", f"{waci:.1f}")
        alignment, color = ("1.5°C", "green") if waci < 100 else ("2.0°C", "orange") if waci < 250 else ("3.2°C", "red")
        c2.markdown(f"### Projection: <span style='color:{color}; font-size: 2rem;'>{alignment}</span>", unsafe_allow_html=True)

        with c3:
            st.subheader("📋 Audit Summary")
            st.info(f"Reg Body: {jurisdiction}\nAssurance: Reasonable")
            if st.button("📥 Generate CEO Disclosures"):
                st.toast("Building PDF...")
                add_audit_entry("REPORT_GEN", "Full Compliance Report generated.")
                time.sleep(1)
                st.success("Download Ready: DNAV_2026.pdf")

        st.markdown("---")
        fig = px.scatter(df, x="Market_Value", y="Carbon_Intensity_S1_S2", size="Quantity", color="Sector", hover_name="Ticker", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    # --- TAB 2: AI OPTIMIZER ---
    with tabs[1]:
        show_walkthrough("AI Portfolio Rebalancer", "Suggests capital shifts to reach Net-Zero goals.", ["Run AI Optimizer."])
        if st.button("🚀 Execute AI Net-Zero Target", type="primary", use_container_width=True):
            st.session_state.optimized_portfolio = optimize_portfolio(df)
            add_audit_entry("OPTIMIZATION_RUN", "Stochastic rebalancing completed.")
            st.success("Optimization Applied.")

        if st.session_state.optimized_portfolio is not None:
            opt_df = st.session_state.optimized_portfolio
            opt_mv = opt_df["Market_Value"].sum()
            opt_cargo = (opt_df["Market_Value"] / 1e6 * opt_df["Carbon_Intensity_S1_S2"]).sum()
            opt_canav = opt_mv - (opt_cargo * carbon_price)
            st.markdown("---")
            oc1, oc2 = st.columns(2)
            oc1.metric("Current caNAV", f"${canav/1e6:,.1f}M")
            oc2.metric("Optimized caNAV", f"${opt_canav/1e6:,.1f}M", delta=f"{(opt_canav/canav - 1)*100:.1f}%")

    # --- TAB 3: CONNECTIVITY ---
    with tabs[2]:
        st.subheader("📡 Integration Gateways")
        ic1, ic2 = st.columns(2)
        if ic1.button("Sync SAP BTP"):
            with st.spinner("Polling..."): time.sleep(1)
            st.success("Fetched 48 emission records.")
        if ic2.button("Scan MS Graph"):
            st.success("No new certificates identified.")

    # --- TAB 4: STRESS TESTING ---
    with tabs[3]:
        st.subheader("🔮 Carbon Price Stress Test")
        if st.session_state.kill_switch: st.error("AI logic suspended.")
        else:
            prices = np.linspace(0, 1000, 100)
            impact = [total_mv - (total_cargo * p) for p in prices]
            fig_stress = go.Figure()
            fig_stress.add_trace(go.Scatter(x=prices, y=impact, name="NAV Curve", line=dict(color="#58a6ff", width=4)))
            fig_stress.add_hline(y=0, line_dash="dot", line_color="red", annotation_text="Insolvency Line")
            fig_stress.update_layout(template="plotly_dark", height=500)
            st.plotly_chart(fig_stress, use_container_width=True)

    # --- TAB 5: GRC SENTRY ---
    with tabs[4]:
        st.subheader("🛡️ AI Fraud Action Center")
        if st.session_state.fraud_data is None:
            st.session_state.fraud_data = pd.DataFrame({
                "Asset": ["XOM", "BP", "VALE"],
                "Flags": ["Intensity Mismatch", "Certificate Re-use", "Under-reported Scope 3"],
                "Action": ["Hold", "Review", "Block"]
            })
        st.data_editor(st.session_state.fraud_data, use_container_width=True)
        if st.button("Commit to Ledger"):
            add_audit_entry("FRAUD_REVIEW", "Analyst cleared flagged anomalies.")

    # --- TAB 6: LINEAGE ---
    with tabs[5]:
        st.subheader("🌐 Institutional Data Lineage (End-to-End Traceability)")
        st.graphviz_chart("""
            digraph {
                rankdir=LR;
                node [shape=box, style=filled, fontname="Helvetica", fontsize=11, margin=0.2];
                
                subgraph cluster_upstream {
                    label = "UPSTREAM (Data Sources)";
                    style=filled;
                    color="#f8f9fa";
                    ERP [label="SAP S/4HANA (GHG Ledger)", fillcolor="#DEEBF7"];
                    Utility [label="Oracle Fusion (Utility API)", fillcolor="#DEEBF7"];
                    Docs [label="MS Graph (Verified PDF Certs)", fillcolor="#DEEBF7"];
                    Grid [label="IEA Emission Factors API", fillcolor="#DEEBF7"];
                }

                subgraph cluster_middle {
                    label = "MIDDLE (Processing & GRC)";
                    style=filled;
                    color="#fffdf0";
                    Ingest [label="OData Ingestion Hub", fillcolor="#FFF2CC"];
                    Normal [label="AI Normalizer / PCAF Mapping", fillcolor="#FFF2CC"];
                    Sentry [label="AI Sentry (Anomaly Detection)", fillcolor="#F8CBAD"];
                    Engine [label="Scope 3 Allocation Engine", fillcolor="#FFF2CC"];
                }

                subgraph cluster_downstream {
                    label = "DOWNSTREAM (Regulation & Audit)";
                    style=filled;
                    color="#f1f8e9";
                    NAV [label="caNAV Master Engine", fillcolor="#C6E0B4"];
                    PDF [label="PDF Compliance Disclosures", fillcolor="#D9D9D9"];
                    BC [label="Blockchain Audit Vault", fillcolor="#D9D9D9"];
                    SFDR [label="SFDR/BRSR Registry API", fillcolor="#D9D9D9"];
                }
                
                ERP -> Ingest; Utility -> Ingest; Docs -> Ingest; Grid -> Ingest;
                Ingest -> Normal;
                Normal -> Sentry;
                Sentry -> Engine [label="CLEAN"];
                Engine -> NAV;
                NAV -> PDF; NAV -> BC; NAV -> SFDR;
                
                Sentry -> BC [label="Flags/Logs", style=dotted, color=red];
            }
        """)
        st.caption("Full auditability enabled for PCAF Reasonable Assurance and SEC/SFDR 2026 mandates.")

    # --- TAB 7: DOCUMENTATION ---
    with tabs[6]:
        doc_tabs = st.tabs(["📄 PRD/MVP", "📐 BRD", "🏗️ FRD", "📖 SOP", "📚 Glossary"])
        def load_md(fname):
            # Resolve absolute path for Windows robustness
            path = (BASE_DIR / fname).resolve()
            if not path.exists():
                # Fallback: scan local directory just in case Streamlit's CWD is different
                path = (Path.cwd() / "DNAV" / fname).resolve()
                if not path.exists():
                    path = (Path.cwd() / fname).resolve()
            
            try:
                if path.exists():
                    with open(path, "r", encoding="utf-8") as f: 
                        st.markdown(f.read())
                else:
                    st.error(f"⚠️ DOCUMENT NOT FOUND: {fname}")
                    st.caption(f"System searched everywhere including: `{path}`")
            except Exception as e: 
                st.error(f"❌ LOAD ERROR: {fname}")
                st.warning(f"Technical context: {str(e)}")
            
        with doc_tabs[0]: load_md("PRD.md")
        with doc_tabs[1]: load_md("BRD.md")
        with doc_tabs[2]: load_md("FRD.md")
        with doc_tabs[3]: load_md("SOP.md")
        with doc_tabs[4]: load_md("Glossary_DeepDive.md")

    st.markdown("---")
    st.markdown("<center style='color:#8b949e;'>© 2026 DNAV Enterprise | Architecture by Prakush Shende</center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
