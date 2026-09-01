import streamlit as st
import json, os, sys

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

st.set_page_config(page_title="Agentic Swarm — AI Boardroom", layout="wide")

st.title("🏛️ Agentic Swarm: Executive AI Boardroom")
st.caption("Autonomous 6-Agent Strategic Analysis, Department Debate & Surprise Adaptation Engine")

# Load sample case
case_file = "data/sample_case.json"
if os.path.exists(case_file):
    with open(case_file, "r", encoding="utf-8") as f:
        sample_data = json.load(f)
else:
    sample_data = {
        "raw_business_case": "Sample case text...",
        "sample_surprise_event": "Sample surprise text..."
    }

st.sidebar.header("🕹️ Boardroom Control Panel")
case_input = st.sidebar.text_area("1. Raw Business Case Input", value=sample_data.get("raw_business_case", ""), height=180)
surprise_input = st.sidebar.text_area("2. Surprise Event Update", value=sample_data.get("sample_surprise_event", ""), height=120)

run_baseline = st.sidebar.button("🚀 Run Baseline Boardroom Swarm", type="primary")
run_surprise = st.sidebar.button("🚨 Run Surprise Adaptation Protocol")

engine = BoardroomEngine()
logger = AuditLogger()
surprise_engine = SurpriseAdaptationEngine()

if run_baseline:
    with st.spinner("Executing 5-Stage Boardroom Protocol on Manual Input..."):
        baseline_state = engine.run_boardroom_protocol(case_input)
        logger.export_trace_json(baseline_state, "baseline_trace.json")
        logger.export_decision_markdown(baseline_state, "baseline_decision.md", "Baseline CEO Decision Dossier")
        st.session_state['baseline_data'] = baseline_state.model_dump()
        st.sidebar.success("✅ Baseline Swarm execution complete!")
        st.rerun()

if run_surprise:
    with st.spinner("Executing Surprise Adaptation Engine on Manual Input..."):
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

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1. Fact Brief (Interpreter)",
    "2. Department Analysis",
    "3. Debate & Conflict (Stage 3)",
    "4. Strategy Matrix (Stage 4)",
    "5. CEO Decision Dossier",
    "6. Surprise Adaptation Delta"
])

trace_path = "outputs/baseline_trace.json"
surprise_path = "outputs/surprise_trace.json"

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

    with tab1:
        st.subheader("📌 Structured Case Brief (Fact vs Assumption Extractor)")
        st.markdown(f"**Problem Statement**: {brief.get('problem_statement')}")
        
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("### ✅ Supplied Hard Facts")
                for f in brief.get("supplied_facts", []):
                    st.markdown(f"- {f}")
        with c2:
            with st.container(border=True):
                st.markdown("### 🏷️ Tagged Assumptions")
                for a in brief.get("identified_assumptions", []):
                    st.markdown(f"- `{a}`")

    with tab2:
        st.subheader("📊 Department Analysis & Quantitative Data Modeling (Stage 1 & 2)")
        
        # Render Data Analyst quantitative visual charts if present
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
                    st.bar_chart(seg_breakdown)
                
                if comp_benchmarks:
                    st.markdown("#### 🏆 Competitor Benchmarking Matrix")
                    st.table(comp_benchmarks)

        for name, data in dept_outputs.items():
            with st.container(border=True):
                st.markdown(f"### 🏢 {name}")
                st.markdown(f"**Summary**: {data.get('summary')}")
                st.markdown("**Key Findings**:")
                for kf in data.get("key_findings", []):
                    st.markdown(f"- {kf}")
                st.caption(f"Financial Impact: {data.get('financial_or_operational_impact')}")

    with tab3:
        st.subheader("⚡ Stage 3: Risk Challenge & Debate Trace")
        for ch in challenges:
            with st.container(border=True):
                st.markdown(f"**Challenger**: `{ch.get('challenger')}` ➔ **Target**: `{ch.get('target_agent')}`")
                st.markdown(f"- **Contested Point**: {ch.get('contested_point')}")
                st.markdown(f"- **Critique Rationale**: {ch.get('critique_rationale')}")
                st.markdown(f"- **Recommended Adjustment**: {ch.get('recommended_adjustment')}")
                if ch.get("rebuttal_response"):
                    st.markdown(f"💬 **Rebuttal Response**: {ch.get('rebuttal_response')}")

    with tab4:
        st.subheader("⚖️ Stage 4: Strategy Comparison Matrix")
        sc1, sc2 = st.columns(2)
        if len(strategies) >= 2:
            with sc1:
                with st.container(border=True):
                    st.markdown(f"### {strategies[0].get('name')}")
                    st.write(strategies[0].get('description'))
                    st.markdown("**Pros**:\n" + "\n".join([f"- {p}" for p in strategies[0].get('pros', [])]))
                    st.markdown("**Cons**:\n" + "\n".join([f"- {c}" for c in strategies[0].get('cons', [])]))
                    st.caption(f"Risk: {strategies[0].get('estimated_risk')} | ROI: {strategies[0].get('projected_roi')}")
            with sc2:
                with st.container(border=True):
                    st.markdown(f"### {strategies[1].get('name')}")
                    st.write(strategies[1].get('description'))
                    st.markdown("**Pros**:\n" + "\n".join([f"- {p}" for p in strategies[1].get('pros', [])]))
                    st.markdown("**Cons**:\n" + "\n".join([f"- {c}" for c in strategies[1].get('cons', [])]))
                    st.caption(f"Risk: {strategies[1].get('estimated_risk')} | ROI: {strategies[1].get('projected_roi')}")

    with tab5:
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

    with tab6:
        st.subheader("🚨 Mid-Event Surprise Adaptation Delta View")
        s_data = st.session_state.get('surprise_data')
        if not s_data and os.path.exists(surprise_path):
            with open(surprise_path, "r", encoding="utf-8") as f:
                s_data = json.load(f)

        if s_data:
            s_ceo = s_data.get("stage5_ceo_decision", {})
            s_brief = s_data.get("brief", {})

            col_base, col_surp = st.columns(2)

            with col_base:
                with st.container(border=True):
                    st.markdown("### 🏛️ Baseline Decision (Before Surprise)")
                    st.markdown(f"**Decision**: {ceo.get('decision_statement')}")
                    st.markdown("**Original Case Facts**: " + str(len(brief.get('supplied_facts', []))) + " facts parsed")
                    st.markdown("#### Baseline KPIs")
                    st.table(ceo.get("business_kpis", []))

            with col_surp:
                with st.container(border=True):
                    st.markdown("### 🚨 Revised Decision (Post-Surprise Pivot)")
                    st.markdown(f"**Revised Decision**: {s_ceo.get('decision_statement')}")
                    st.markdown("#### Updated Surprise KPIs")
                    st.table(s_ceo.get("business_kpis", []))

            st.markdown("---")
            st.markdown("### 🗺️ Revised Implementation Roadmap (30/60/90 Days)")
            st.json(s_ceo.get("implementation_roadmap", {}))
        else:
            st.info("No surprise adaptation run trace found yet. Click '🚨 Run Surprise Adaptation Protocol' in the sidebar to simulate the surprise round.")
else:
    st.info("No baseline run trace found yet. Click 'Run Baseline Boardroom Swarm' in the sidebar or run `python main.py` in your terminal.")
