import os
import sys
import datetime
from typing import Dict, Any

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

from core.state import BoardroomState, TraceEntry
from agents.input_interpreter import InputInterpreterAgent
from agents.business_research import BusinessResearchAgent
from agents.finance import FinanceAgent
from agents.marketing import MarketingAgent
from agents.data_analyst import DataAnalystAgent
from agents.risk_reviewer import RiskReviewerAgent
from agents.ceo import CEOAgent

class BoardroomEngine:
    """
    Coordinates the 5-Stage Boardroom Protocol:
    Stage 1: Analyse (Parallel Independent Department Analysis)
    Stage 2: Share (State publication & structured data bus)
    Stage 3: Challenge (Risk Agent pushback & rebuttal)
    Stage 4: Compare (Strategy A vs B comparison matrix)
    Stage 5: Decide (Final CEO Decision Dossier with KPIs)
    """
    def __init__(self):
        self.interpreter = InputInterpreterAgent()
        self.research = BusinessResearchAgent()
        self.finance = FinanceAgent()
        self.marketing = MarketingAgent()
        self.analyst = DataAnalystAgent()
        self.risk = RiskReviewerAgent()
        self.ceo = CEOAgent()

    def run_boardroom_protocol(self, raw_case_text: str) -> BoardroomState:
        state = BoardroomState()
        safe_print("\n=======================================================")
        safe_print("[RUNNING BOARDROOM PROTOCOL: BASELINE]")
        safe_print("=======================================================\n")

        # Stage 0: Input Interpretation
        safe_print("[STAGE 0] Deconstructing Raw Business Case into Facts vs Assumptions...")
        state.brief = self.interpreter.run(raw_case_text)
        self._log_trace(state, "Stage 0", "Input Interpreter", "Extracted Structured Brief", state.brief.model_dump())

        # Stage 1: Independent Department Analysis
        safe_print("[STAGE 1: ANALYSE] Running Department Analysis...")
        dept_research = self.research.run(state.brief)
        dept_finance = self.finance.run(state.brief)
        dept_marketing = self.marketing.run(state.brief)
        dept_analyst = self.analyst.run(state.brief)

        # Stage 2: Share
        safe_print("[STAGE 2: SHARE] Publishing Department Outputs to Central Shared Bus...")
        state.stage1_department_outputs["Business Research"] = dept_research
        state.stage1_department_outputs["Finance"] = dept_finance
        state.stage1_department_outputs["Marketing & Sales"] = dept_marketing
        state.stage1_department_outputs["Data Analyst"] = dept_analyst

        for agent_name, out in state.stage1_department_outputs.items():
            self._log_trace(state, "Stage 1 & 2", agent_name, "Published Department Analysis", out.model_dump())

        # Stage 3: Challenge & Debate Trigger
        safe_print("[STAGE 3: CHALLENGE] Risk & Reviewer Evaluating Department Disagreements...")
        challenges = self.risk.run(state.stage1_department_outputs)
        state.stage3_challenges = challenges

        for ch in state.stage3_challenges:
            target = ch.target_agent
            if target in state.stage1_department_outputs:
                rebuttal = self.risk.generate_rebuttal(ch, state.stage1_department_outputs[target])
                ch.rebuttal_response = rebuttal
                safe_print(f"  [CHALLENGE -> {target}]: {ch.contested_point}")
                safe_print(f"  [REBUTTAL <- {target}]: {rebuttal}\n")

            self._log_trace(state, "Stage 3", "Risk & Reviewer", f"Issued Challenge to {ch.target_agent}", ch.model_dump())

        state.debate_cycle_count = 1  # Guaranteed capped debate cycle

        # Stage 4: Strategy Comparison
        safe_print("[STAGE 4: COMPARE] Formulating Strategy Comparison Matrix...")
        state.stage4_strategies = self.ceo.formulate_strategies(state)
        self._log_trace(state, "Stage 4", "CEO Agent", "Formulated 2 Viable Strategies", [s.model_dump() for s in state.stage4_strategies])

        # Stage 5: Final CEO Decision
        safe_print("[STAGE 5: DECIDE] CEO Synthesizing Final Strategic Decision Dossier...")
        state.stage5_ceo_decision = self.ceo.make_final_decision(state)
        self._log_trace(state, "Stage 5", "CEO Agent", "Issued Final CEO Decision Dossier", state.stage5_ceo_decision.model_dump())

        safe_print("[SUCCESS] BOARDROOM PROTOCOL COMPLETED SUCCESSFULLY.\n")
        return state

    def _log_trace(self, state: BoardroomState, stage: str, agent: str, action: str, content: Any):
        entry = TraceEntry(
            stage=stage,
            agent=agent,
            timestamp=datetime.datetime.now().isoformat(),
            action=action,
            content=content
        )
        state.execution_trace.append(entry)
