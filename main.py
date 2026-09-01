import os
import json
from core.engine import BoardroomEngine
from core.logger import AuditLogger
from surprise.adapt import SurpriseAdaptationEngine

def load_sample_case():
    case_path = "data/sample_case.json"
    if os.path.exists(case_path):
        with open(case_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "raw_business_case": "Standard B2B SaaS case study...",
        "sample_surprise_event": "Standard surprise event..."
    }

def main():
    print("==================================================================")
    print("  AGENTIC SWARM: THE AI BOARDROOM PROTOCOL RUNNER")
    print("  Evaluating 5-Stage Protocol & Mid-Event Surprise Adaptation")
    print("==================================================================")

    data = load_sample_case()
    raw_case = data.get("raw_business_case")
    surprise_text = data.get("sample_surprise_event")

    # 1. Initialize Core Engine & Logger
    engine = BoardroomEngine()
    logger = AuditLogger()

    # 2. Run Baseline Boardroom Protocol
    baseline_state = engine.run_boardroom_protocol(raw_case)
    
    # 3. Export Baseline Evidence (Required for Submission)
    logger.export_trace_json(baseline_state, "baseline_trace.json")
    logger.export_decision_markdown(baseline_state, "baseline_decision.md", "Baseline CEO Decision Dossier")

    # 4. Run Mid-Event Surprise Adaptation Protocol
    surprise_engine = SurpriseAdaptationEngine()
    revised_state = surprise_engine.process_surprise(baseline_state, surprise_text)

    print("\n==================================================================")
    print("  ALL RUNS COMPLETED SUCCESSFULLY!")
    print("  Baseline Trace: outputs/baseline_trace.json & outputs/baseline_decision.md")
    print("  Surprise Trace: outputs/surprise_trace.json & outputs/revised_decision.md")
    print("  Launch Web UI:  streamlit run app_ui.py")
    print("==================================================================")

if __name__ == "__main__":
    main()
