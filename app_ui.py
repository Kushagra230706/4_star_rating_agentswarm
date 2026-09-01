import streamlit as st
import json, os, sys
import pandas as pd

# Force UTF-8 encoding for Windows console output
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def safe_print(text: str):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', errors='replace').decode('ascii'))

from core.engine import BoardroomEngine
from core.logger import AuditLogger
from surprise.adapt import SurpriseAdaptationEngine
from core.state import BoardroomState

st.set_page_config(page_title="Agentic Swarm — AI Boardroom", layout="wide", initial_sidebar_state="expanded")

# Dark Glassmorphism Executive Theme
bg_color = "#0b0f19"
sidebar_bg = "#111827"
card_bg = "rgba(255, 255, 255, 0.04)"
card_border = "rgba(255, 255, 255, 0.12)"
text_color = "#f8fafc"
subtext_color = "#94a3b8"
accent_green = "#10b981"
btn_bg = "#1f2937"
btn_text = "#f8fafc"
input_bg = "#1f2937"
code_bg = "rgba(16, 185, 129, 0.15)"
code_text = "#34d399"
header_gradient = "linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%)"
mermaid_theme = "dark"

# Harmonized CSS Design System
st.markdown(f"""
<style>
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {card_border} !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}
    section[data-testid="stSidebar"] textarea, section[data-testid="stSidebar"] select {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {card_border} !important;
        border-radius: 8px !important;
    }}
    
    .animated-stage {{
        animation: fadeIn 0.35s ease-out forwards;
    }}
    
    /* Project Title Banner Card */
    .project-header-card {{
        background: {header_gradient};
        border: 1px solid {card_border};
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 20px;
    }}
    
    .project-title {{
        font-size: 1.8rem;
        font-weight: 800;
        color: {text_color} !important;
        margin: 0;
    }}
    
    .project-subtitle {{
        font-size: 0.95rem;
        color: {subtext_color} !important;
        margin-top: 6px;
    }}
    
    /* Containers & Cards */
    div[data-testid="stContainer"] {{
        background: {card_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}
    
    /* Metrics Fix for Light Mode */
    div[data-testid="stMetric"] {{
        background: {card_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 12px;
        padding: 12px 16px;
    }}
    div[data-testid="stMetricValue"] > div {{
        color: {text_color} !important;
        font-weight: 800 !important;
    }}
    div[data-testid="stMetricLabel"] > div > p {{
        color: {subtext_color} !important;
        font-weight: 600 !important;
    }}

    /* Assumptions / Inline Code Fix */
    code {{
        background-color: {code_bg} !important;
        color: {code_text} !important;
        border: 1px solid {card_border} !important;
        border-radius: 6px !important;
        padding: 4px 8px !important;
        font-size: 0.88rem !important;
        word-break: break-word !important;
    }}

    /* Buttons Styling */
    div.stButton > button {{
        background-color: {btn_bg} !important;
        color: {btn_text} !important;
        border: 1px solid {card_border} !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 10px 14px !important;
        transition: all 0.2s ease-in-out !important;
    }}
    
    div.stButton > button[data-testid="stBaseButton-primary"] {{
        background-color: {accent_green} !important;
        color: #ffffff !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# Wide Banner Graphic (cropped tight without dark top/bottom bars)
banner_path = "assets/boardroom_banner_wide.jpg"
if not os.path.exists(banner_path):
    banner_path = "assets/boardroom_banner_hex.jpg"

if os.path.exists(banner_path):
    st.image(banner_path, use_container_width=True)

# Project Definition Header Box
st.markdown("""
<div class="project-header-card">
    <div class="project-title">🏛️ Agentic Swarm: Executive AI Boardroom</div>
    <div class="project-subtitle">Autonomous 7-Agent Corporate Strategy Synthesis, Department Debate & Mid-Event Surprise Adaptation System</div>
</div>
""", unsafe_allow_html=True)

# Load official test cases
preset_file = "data/official_test_cases.json"
official_presets = {}
if os.path.exists(preset_file):
    with open(preset_file, "r", encoding="utf-8") as f:
        official_presets = json.load(f)

st.sidebar.header("🕹️ Boardroom Control Panel")

# Theme & Test Case Preset Selector
if official_presets:
    st.sidebar.markdown("### 🎯 Select Official Problem Case")
    theme_options = ["Custom Input"] + list(official_presets.keys())
    selected_theme = st.sidebar.selectbox("Select Business Theme", theme_options)
    
    default_case_text = ""
    default_surprise_text = ""
    
    if selected_theme != "Custom Input":
        tc_options = list(official_presets[selected_theme].keys())
        selected_tc = st.sidebar.selectbox("Select Test Case", tc_options)
        tc_data = official_presets[selected_theme][selected_tc]
        default_case_text = tc_data.get("raw_business_case", "")
        default_surprise_text = tc_data.get("sample_surprise_event", "")
    else:
        case_file = "data/sample_case.json"
        if os.path.exists(case_file):
            with open(case_file, "r", encoding="utf-8") as f:
                sample_data = json.load(f)
            default_case_text = sample_data.get("raw_business_case", "")
            default_surprise_text = sample_data.get("sample_surprise_event", "")

    case_input = st.sidebar.text_area("1. Raw Business Case Input", value=default_case_text, height=180)
    surprise_input = st.sidebar.text_area("2. Surprise Event Update", value=default_surprise_text, height=120)
else:
    case_input = st.sidebar.text_area("1. Raw Business Case Input", value="Sample case text...", height=180)
    surprise_input = st.sidebar.text_area("2. Surprise Event Update", value="Sample surprise text...", height=120)

run_baseline = st.sidebar.button("🚀 Run Baseline Swarm Protocol", type="primary")
run_surprise = st.sidebar.button("🚨 Run Surprise Adaptation Protocol")

engine = BoardroomEngine()
logger = AuditLogger()
surprise_engine = SurpriseAdaptationEngine()

if run_baseline:
    with st.spinner("Executing 5-Stage Boardroom Protocol with Live LLM Agents..."):
        baseline_state = engine.run_boardroom_protocol(case_input)
        logger.export_trace_json(baseline_state, "baseline_trace.json")
        logger.export_decision_markdown(baseline_state, "baseline_decision.md", "Baseline CEO Decision Dossier")
        st.session_state['baseline_data'] = baseline_state.model_dump()
        st.sidebar.success("✅ Baseline Swarm execution complete!")
        st.rerun()

if run_surprise:
    with st.spinner("Executing Surprise Adaptation Engine on Input..."):
        trace_path = "outputs/baseline_trace.json"
        if 'baseline_data' in st.session_state:
            base_state = BoardroomState(**st.session_state['baseline_data'])
        elif os.path.exists(trace_path):
            with open(trace_path, "r", encoding="utf-8") as f:
                base_data = json.load(f)
            base_state = BoardroomState(**base_data)
        else:
            base_state = engine.run_boardroom_protocol(case_input)
            logger.export_trace_json(base_state, "baseline_trace.json")
            st.session_state['baseline_data'] = base_state.model_dump()

        revised_state = surprise_engine.process_surprise(base_state, surprise_input, raw_case_text=case_input)
        logger.export_trace_json(revised_state, "surprise_trace.json")
        logger.export_decision_markdown(revised_state, "revised_decision.md", "Revised CEO Decision Dossier (Post-Surprise Adaptation)")
        st.session_state['surprise_data'] = revised_state.model_dump()
        st.sidebar.success("✅ Surprise Adaptation execution complete!")
        st.rerun()

# Harmonized Stage Selector Buttons
st.markdown("### 🎛️ Boardroom Stage Navigator")
stage_buttons = [
    "📌 Stage 0: Brief",
    "📊 Stage 1: Analysis",
    "⚡ Stage 3: Debate",
    "⚖️ Stage 4: Strategy",
    "👑 Stage 5: Decision",
    "🚨 Surprise Delta"
]

if "active_stage" not in st.session_state:
    st.session_state["active_stage"] = "📌 Stage 0: Brief"

b_cols = st.columns(6)
for i, b_name in enumerate(stage_buttons):
    with b_cols[i]:
        btn_type = "primary" if st.session_state["active_stage"] == b_name else "secondary"
        if st.button(b_name, key=f"nav_btn_{i}", type=btn_type):
            st.session_state["active_stage"] = b_name
            st.rerun()

active_stage = st.session_state["active_stage"]

trace_path = "outputs/baseline_trace.json"
surprise_path = "outputs/surprise_trace.json"

def render_roadmap_cards(roadmap: dict, title: str = "🗺️ Implementation Roadmap (30/60/90 Days)"):
    st.markdown(f"### {title}")
    if isinstance(roadmap, dict) and roadmap:
        r1, r2, r3 = st.columns(3)
        
        p1 = roadmap.get("first_30_days") or roadmap.get("days_1_to_30") or roadmap.get("days_1-30") or []
        p2 = roadmap.get("days_31_to_60") or roadmap.get("days_31-60") or []
        p3 = roadmap.get("days_61_to_90") or roadmap.get("days_61-90") or []
        
        with r1:
            with st.container(border=True):
                st.markdown("#### 🚀 Days 1 – 30")
                st.caption("Phase 1: Foundation & Setup")
                if p1:
                    for step in p1:
                        st.markdown(f"📌 {step}")
                else:
                    st.write("Initial setup & onboarding")

        with r2:
            with st.container(border=True):
                st.markdown("#### 📈 Days 31 – 60")
                st.caption("Phase 2: Execution & Scaling")
                if p2:
                    for step in p2:
                        st.markdown(f"📌 {step}")
                else:
                    st.write("Channel scaling & partner growth")

        with r3:
            with st.container(border=True):
                st.markdown("#### 🎯 Days 61 – 90")
                st.caption("Phase 3: Optimization & Break-Even")
                if p3:
                    for step in p3:
                        st.markdown(f"📌 {step}")
                else:
                    st.write("Unit economics optimization & review")
    else:
        st.write(str(roadmap))

state_data = st.session_state.get('baseline_data')
if not state_data and os.path.exists(trace_path):
    with open(trace_path, "r", encoding="utf-8") as f:
        state_data = json.load(f)

if state_data:
    brief = state_data.get("brief", {})
    dept_outputs = state_data.get("stage1_department_outputs", {})
    challenges = state_data.get("stage3_challenges", [])
    strategies = state_data.get("stage4_strategies", [])
    ceo = state_data.get("stage5_ceo_decision", {})

    st.markdown('<div class="animated-stage">', unsafe_allow_html=True)

    if active_stage == "📌 Stage 0: Brief":
        st.subheader("📌 Stage 0: Structured Case Brief (Fact vs Assumption Extractor)")
        st.markdown(f"**Problem Statement**: {brief.get('problem_statement')}")
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Supplied Hard Facts", len(brief.get("supplied_facts", [])))
        with m2:
            st.metric("Tagged Assumptions", len(brief.get("identified_assumptions", [])))
        with m3:
            st.metric("Hard Constraints", len(brief.get("hard_constraints", [])))

        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("### ✅ Supplied Hard Facts")
                for f in brief.get("supplied_facts", []):
                    st.markdown(f"• {f}")
        with c2:
            with st.container(border=True):
                st.markdown("### 🏷️ Tagged Assumptions")
                for a in brief.get("identified_assumptions", []):
                    st.markdown(f"• `{a}`")

    elif active_stage == "📊 Stage 1: Analysis":
        st.subheader("📊 Stage 1 & 2: Department Analysis & Quantitative Data Modeling")
        
        if "Data Analyst" in dept_outputs:
            da_metrics = dept_outputs["Data Analyst"].get("metrics", {})
            seg_breakdown = da_metrics.get("segment_breakdown", {})
            comp_benchmarks = da_metrics.get("competitor_benchmarks", [])
            
            with st.container(border=True):
                st.markdown("### 📈 Quantitative Data Analyst Insights")
                m_col1, m_col2, m_col3 = st.columns(3)
                with m_col1:
                    st.metric("Portfolio Risk / Default", f"{da_metrics.get('Portfolio_Default_Rate', 4.5)}%")
                with m_col2:
                    st.metric("Expected ROI / Yield", f"{da_metrics.get('Expected_ROI', da_metrics.get('Expected_Annual_ROI', 16.5))}%")
                with m_col3:
                    st.metric("Capital Deployment", f"{da_metrics.get('Capital_Utilization', 90.0)}%")
                
                if seg_breakdown:
                    st.markdown("#### 📊 Customer Segment & Capital Allocation Breakdown (%)")
                    df_seg = pd.DataFrame.from_dict(seg_breakdown, orient='index', columns=['Allocation (%)'])
                    st.bar_chart(df_seg)
                
                if comp_benchmarks:
                    st.markdown("#### 🏆 Competitor Benchmarking Matrix")
                    st.table(comp_benchmarks)

        for name, data in dept_outputs.items():
            icon = "💼" if "Research" in name else ("💰" if "Finance" in name else ("📣" if "Marketing" in name else "📈"))
            with st.container(border=True):
                st.markdown(f"### {icon} {name}")
                st.markdown(f"**Summary**: {data.get('summary')}")
                st.markdown("**Key Findings**:")
                for kf in data.get("key_findings", []):
                    st.markdown(f"- {kf}")
                st.caption(f"Financial Impact: {data.get('financial_or_operational_impact')}")

    elif active_stage == "⚡ Stage 3: Debate":
        st.subheader("⚡ Stage 3: Risk Challenge & Department Debate Trace")

        for ch in challenges:
            with st.container(border=True):
                st.markdown(f"🛑 **Challenger**: `{ch.get('challenger')}` ➔ **Target**: `{ch.get('target_agent')}`")
                st.markdown(f"• **Contested Point**: {ch.get('contested_point')}")
                st.markdown(f"• **Critique Rationale**: {ch.get('critique_rationale')}")
                st.markdown(f"• **Recommended Adjustment**: {ch.get('recommended_adjustment')}")
                if ch.get("rebuttal_response"):
                    st.markdown(f"💬 **Rebuttal Response**: {ch.get('rebuttal_response')}")

    elif active_stage == "⚖️ Stage 4: Strategy":
        st.subheader("⚖️ Stage 4: Dynamic Strategy Comparison Matrix")
        sc1, sc2 = st.columns(2)
        if len(strategies) >= 2:
            with sc1:
                with st.container(border=True):
                    st.markdown(f"### 🅰️ {strategies[0].get('name')}")
                    st.write(strategies[0].get('description'))
                    st.markdown("**Pros**:\n" + "\n".join([f"- {p}" for p in strategies[0].get('pros', [])]))
                    st.markdown("**Cons**:\n" + "\n".join([f"- {c}" for c in strategies[0].get('cons', [])]))
                    st.caption(f"Risk: {strategies[0].get('estimated_risk')} | ROI: {strategies[0].get('projected_roi')}")
            with sc2:
                with st.container(border=True):
                    st.markdown(f"### 🅱️ {strategies[1].get('name')}")
                    st.write(strategies[1].get('description'))
                    st.markdown("**Pros**:\n" + "\n".join([f"- {p}" for p in strategies[1].get('pros', [])]))
                    st.markdown("**Cons**:\n" + "\n".join([f"- {c}" for c in strategies[1].get('cons', [])]))
                    st.caption(f"Risk: {strategies[1].get('estimated_risk')} | ROI: {strategies[1].get('projected_roi')}")

    elif active_stage == "👑 Stage 5: Decision":
        st.subheader("👑 Stage 5: Final CEO Decision Dossier")
        if ceo:
            st.success(f"### 📌 Final Order\n**{ceo.get('decision_statement')}**")
            
            st.markdown("#### ❌ Rejected Alternative & Rationale")
            rej = ceo.get("rejected_alternative", {})
            if isinstance(rej, dict):
                strat_name = rej.get("strategy_name", "Rejected Strategy")
                reason = rej.get("core_business_flaw") or rej.get("rejection_reason", "High financial/operational risk.")
                pushback = rej.get("department_pushback", "Finance & Marketing identified negative ROI/runway risk.")
                downside = rej.get("downside_risk_scenario", "High insolvency probability before break-even horizon.")
                quant = rej.get("quantitative_comparison", "Lower capital efficiency vs selected strategy.")
                
                with st.container(border=True):
                    st.markdown(f"### 🛑 {strat_name}")
                    st.markdown(f"**Core Business Flaw**: {reason}")
                    st.markdown(f"**Department Evidence & Pushback**: {pushback}")
                    st.markdown(f"**Downside Risk & Insolvency Horizon**: {downside}")
                    st.markdown(f"**Quantitative Comparison**: `{quant}`")
            else:
                st.write(str(rej))
            
            st.markdown("#### 📊 Business KPIs")
            st.table(ceo.get("business_kpis", []))
            
            st.markdown("---")
            render_roadmap_cards(ceo.get("implementation_roadmap", {}), "🗺️ Baseline Implementation Roadmap")

    elif active_stage == "🚨 Surprise Delta":
        st.subheader("🚨 Mid-Event Surprise Adaptation Delta View")
        s_data = st.session_state.get('surprise_data')
        if not s_data and os.path.exists(surprise_path):
            with open(surprise_path, "r", encoding="utf-8") as f:
                s_data = json.load(f)

        if s_data:
            s_ceo = s_data.get("stage5_ceo_decision", {})
            s_brief = s_data.get("brief", {})
            s_dept = s_data.get("stage1_department_outputs", {})

            col_base, col_surp = st.columns(2)

            with col_base:
                with st.container(border=True):
                    st.markdown("### 🏛️ Baseline Decision (Before Surprise)")
                    st.markdown(f"**Decision**: {ceo.get('decision_statement')}")
                    st.markdown("**Original Case Facts**: " + str(len(brief.get('supplied_facts', []))) + " facts parsed")
                    st.markdown("#### Baseline KPIs")
                    st.table(ceo.get("business_kpis", []))
                    
                    if "Data Analyst" in dept_outputs:
                        b_da = dept_outputs["Data Analyst"].get("metrics", {})
                        b_seg = b_da.get("segment_breakdown", {})
                        b_comp = b_da.get("competitor_benchmarks", [])
                        st.markdown("#### 📊 Baseline Segment Mix")
                        if b_seg:
                            st.bar_chart(pd.DataFrame.from_dict(b_seg, orient='index', columns=['Allocation (%)']))
                        if b_comp:
                            st.markdown("#### 🏆 Baseline Competitor Matrix")
                            st.table(b_comp)

            with col_surp:
                with st.container(border=True):
                    st.markdown("### 🚨 Revised Decision (Post-Surprise Pivot)")
                    st.markdown(f"**Revised Decision**: {s_ceo.get('decision_statement')}")
                    st.markdown("#### Updated Surprise KPIs")
                    st.table(s_ceo.get("business_kpis", []))
                    
                    if "Data Analyst" in s_dept:
                        s_da = s_dept["Data Analyst"].get("metrics", {})
                        s_seg = s_da.get("segment_breakdown", {})
                        s_comp = s_da.get("competitor_benchmarks", [])
                        st.markdown("#### 📊 Post-Surprise Reallocated Segment Mix")
                        if s_seg:
                            st.bar_chart(pd.DataFrame.from_dict(s_seg, orient='index', columns=['Allocation (%)']))
                        if s_comp:
                            st.markdown("#### ⚡ Post-Surprise Competitor Shock Matrix")
                            st.table(s_comp)

            st.markdown("---")
            render_roadmap_cards(s_ceo.get("implementation_roadmap", {}), "🗺️ Revised Implementation Roadmap (Post-Surprise Pivot)")
        else:
            st.info("No surprise adaptation run trace found yet. Click '🚨 Run Surprise Adaptation Protocol' in the sidebar to simulate the surprise round.")

    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No baseline run trace found yet. Click 'Run Baseline Swarm Protocol' in the sidebar or run `python main.py` in your terminal.")
