import os
import sys
import json
from typing import Dict, Any, List

# Force UTF-8 encoding for Windows console output
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from config import router
from core.state import BoardroomState, CEODecision
from core.engine import BoardroomEngine
from core.logger import AuditLogger

def safe_print(text: str):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', errors='replace').decode('ascii'))

SYSTEM_SURPRISE_PROMPT = """You are the Input Interpreter and Adaptation Manager.
Your role: Compare the original business case brief with a sudden mid-event business surprise (e.g. competitor price drop, budget cut, supplier failure).

CRITICAL INSTRUCTIONS:
1. Identify which original facts or assumptions CHANGED.
2. Identify which original facts remained STABLE.
3. Name the SPECIFIC department agents materially affected (e.g. ["Finance", "Marketing & Sales"]).

You MUST respond ONLY with a valid JSON object matching this schema:
{
  "invalidated_facts": ["Original budget was $50k"],
  "new_surprise_facts": ["Budget slashed by 40% to $30k due to macroeconomic shift"],
  "stable_facts": ["Customer target demographic remains unchanged"],
  "affected_agents": ["Finance", "Marketing & Sales"]
}
"""

class SurpriseAdaptationEngine:
    def __init__(self):
        self.engine = BoardroomEngine()
        self.logger = AuditLogger()

    def process_surprise(self, base_state: BoardroomState, surprise_text: str, raw_case_text: str = None) -> BoardroomState:
        safe_print("\n=======================================================")
        safe_print("[RUNNING SURPRISE ADAPTATION PROTOCOL]")
        safe_print("=======================================================\n")

        # Step 1: Identify fact diffs
        base_brief_json = base_state.brief.model_dump_json() if base_state.brief else "{}"
        diff_prompt = f"Original Brief:\n{base_brief_json}\n\nSURPRISE EVENT ANNOUNCEMENT:\n{surprise_text}"
        
        res_text = router.call_agent_llm("Adaptation Engine", SYSTEM_SURPRISE_PROMPT, diff_prompt)
        
        try:
            cleaned = res_text.strip()
            if cleaned.startswith("```json"): cleaned = cleaned[7:]
            if cleaned.startswith("```"): cleaned = cleaned[3:]
            if cleaned.endswith("```"): cleaned = cleaned[:-3]
            diff_data = json.loads(cleaned.strip())
        except Exception:
            diff_data = {
                "invalidated_facts": ["Original financial budget assumptions"],
                "new_surprise_facts": [surprise_text],
                "stable_facts": ["Core market product relevance"],
                "affected_agents": ["Finance", "Marketing & Sales"]
            }

        safe_print(f"  Changed Facts: {diff_data.get('invalidated_facts')}")
        safe_print(f"  Surprise Factors: {diff_data.get('new_surprise_facts')}")
        safe_print(f"  Re-running Affected Agents: {diff_data.get('affected_agents')}\n")

        # Step 2: Combine original case + surprise event for selective re-execution
        base_case_str = raw_case_text if (raw_case_text and len(raw_case_text.strip()) > 0) else (base_state.brief.problem_statement if base_state and base_state.brief else "")
        updated_raw_case = f"{base_case_str}\n\n[MID-EVENT SURPRISE UPDATE]:\n{surprise_text}"
        
        # Re-run boardroom swarm with updated parameters
        revised_state = self.engine.run_boardroom_protocol(updated_raw_case)

        # Export surprise trace & decision
        self.logger.export_trace_json(revised_state, "surprise_trace.json")
        self.logger.export_decision_markdown(revised_state, "revised_decision.md", "Revised CEO Decision Dossier (Post-Surprise Adaptation)")

        return revised_state
