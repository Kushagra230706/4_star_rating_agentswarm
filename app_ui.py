import streamlit as st
import json
import os

from core.engine import BoardroomEngine
from core.logger import AuditLogger
from surprise.adapt import SurpriseAdaptationEngine

st.set_page_config(page_title="Agentic Swarm — AI Boardroom", layout="wide")


def load_sample_case():
    case_file = "data/sample_case.json"
    if os.path.exists(case_file):
        with open(case_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "raw_business_case": "Sample case text...",
        "sample_surprise_event": "Sample surprise text..."
    }


sample_data = load_sample_case()

if "boardroom_case_input" not in st.session_state:
    st.session_state["boardroom_case_input"] = sample_data.get("raw_business_case", "")
if "boardroom_surprise_input" not in st.session_state:
    st.session_state["boardroom_surprise_input"] = sample_data.get("sample_surprise_event", "")


st.title("🏛️ Agentic Swarm: Executive AI Boardroom")
st.caption("Autonomous 6-Agent Strategic Analysis, Department Debate & Surprise Adaptation Engine")

st.sidebar.header("🕹️ Boardroom Control Panel")

with st.sidebar.form("boardroom_form"):
    case_input = st.text_area(
        "1. Raw Business Case Input",
        key="boardroom_case_input",
        value=st.session_state["boardroom_case_input"],
        height=180,
    )
    surprise_input = st.text_area(
        "2. Surprise Event Update",
        key="boardroom_surprise_input",
        value=st.session_state["boardroom_surprise_input"],
        height=120,
    )

    c1, c2 = st.columns(2)
    with c1:
        run_baseline = st.form_submit_button("🚀 Run Baseline", type="primary")
    with c2:
        run_surprise = st.form_submit_button("🚨 Run Surprise")


if run_baseline or run_surprise:
    case_text = (case_input or "").strip() or sample_data.get("raw_business_case", "")
    surprise_text = (surprise_input or "").strip() or sample_data.get("sample_surprise_event", "")

    with st.spinner("Running boardroom analysis..."):
        engine = BoardroomEngine()
        logger = AuditLogger()

        baseline_state = engine.run_boardroom_protocol(case_text)
        logger.export_trace_json(baseline_state, "baseline_trace.json")
        logger.export_decision_markdown(
            baseline_state,
            "baseline_decision.md",
            "Baseline CEO Decision Dossier",
        )

        if run_surprise:
            surprise_engine = SurpriseAdaptationEngine()
            revised_state = surprise_engine.process_surprise(baseline_state, surprise_text)
            st.session_state["active_state"] = revised_state.model_dump()
            st.session_state["active_mode"] = "surprise"
        else:
            st.session_state["active_state"] = baseline_state.model_dump()
            st.session_state["active_mode"] = "baseline"

    st.success("Boardroom run completed successfully.")


trace_source = st.session_state.get("active_state")
trace_path = "outputs/baseline_trace.json"
if trace_source is None and os.path.exists(trace_path):
    with open(trace_path, "r", encoding="utf-8") as f:
        trace_source = json.load(f)


def render_trace(trace_data):
    if not trace_data:
        st.info("No boardroom run trace found yet. Enter your case text and click a run button.")
        return

    brief = trace_data.get("brief", {})
    dept_outputs = trace_data.get("stage1_department_outputs", {})
    challenges = trace_data.get("stage3_challenges", [])
    strategies = trace_data.get("stage4_strategies", [])
    ceo = trace_data.get("stage5_ceo_decision", {})

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1. Fact Brief (Interpreter)",
        "2. Department Analysis",
        "3. Debate & Conflict (Stage 3)",
        "4. Strategy Matrix (Stage 4)",
        "5. CEO Decision Dossier (Stage 5)",
    ])

    with tab1:
        st.subheader("📌 Structured Case Brief (Fact vs Assumption Extractor)")
        st.markdown(f"**Problem Statement**: {brief.get('problem_statement')}")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### ✅ Supplied Hard Facts")
            for fact in brief.get("supplied_facts", []):
                st.markdown(f"- {fact}")
        with c2:
            st.markdown("### 🏷️ Tagged Assumptions")
            for assumption in brief.get("identified_assumptions", []):
                st.info(assumption)

    with tab2:
        st.subheader("📊 Department Analysis (Stage 1 & 2)")
        for name, data in dept_outputs.items():
            with st.expander(f"🏢 {name} Department Report", expanded=True):
                st.markdown(f"**Summary**: {data.get('summary')}")
                st.markdown("**Key Findings**:")
                for kf in data.get("key_findings", []):
                    st.markdown(f"- {kf}")
                st.caption(f"Financial Impact: {data.get('financial_or_operational_impact')}")

    with tab3:
        st.subheader("⚡ Stage 3: Risk Challenge & Debate Trace")
        for ch in challenges:
            st.warning(f"**Challenger**: {ch.get('challenger')} ➔ **Target**: {ch.get('target_agent')}")
            st.markdown(f"- **Contested Point**: {ch.get('contested_point')}")
            st.markdown(f"- **Critique**: {ch.get('critique_rationale')}")
            st.markdown(f"- **Recommended Adjustment**: {ch.get('recommended_adjustment')}")
            if ch.get("rebuttal_response"):
                st.success(f"**Rebuttal Response**: {ch.get('rebuttal_response')}")

    with tab4:
        st.subheader("⚖️ Stage 4: Strategy Comparison Matrix")
        strategy_cols = st.columns(2)
        if len(strategies) >= 2:
            for idx, column in enumerate(strategy_cols):
                with column:
                    strategy = strategies[idx]
                    st.markdown(f"### {strategy.get('name')}")
                    st.write(strategy.get('description'))
                    st.success("Pros: " + ", ".join(strategy.get('pros', [])))
                    st.error("Cons: " + ", ".join(strategy.get('cons', [])))

    with tab5:
        st.subheader("👑 Stage 5: Final CEO Decision Dossier")
        if ceo:
            st.success(f"### 📌 Final Order: {ceo.get('decision_statement')}")
            st.markdown("#### ❌ Rejected Alternative & Rationale")
            st.json(ceo.get("rejected_alternative", {}))
            st.markdown("#### 📊 Business KPIs")
            st.table(ceo.get("business_kpis", []))


if trace_source is not None:
    render_trace(trace_source)
else:
    st.info("No baseline run trace found yet. Enter your case text and click the run button.")
