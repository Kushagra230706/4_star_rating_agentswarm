import json
from config import router
from core.state import StructuredBrief, DepartmentOutput

SYSTEM_PROMPT = """You are the Chief Financial Officer (CFO).
Your role: Evaluate financial viability, unit economics (LTV/CAC), CapEx vs OpEx, profitability, break-even timelines, and budget constraints.

CRITICAL INSTRUCTIONS:
- Be fiscally conservative.
- Challenge unvalidated spending.
- Explicitly tag financial estimates as [ASSUMPTION: ...].

You MUST respond ONLY with a valid JSON object matching this schema:
{
  "agent_name": "Finance",
  "summary": "1-2 sentence financial health summary",
  "key_findings": ["finding 1", "finding 2"],
  "recommendations": ["recommendation 1", "recommendation 2"],
  "financial_or_operational_impact": "CapEx capped at $50k; break-even projected in month 9",
  "explicit_assumptions": ["[ASSUMPTION: Gross margin remains at 65%]"],
  "metrics": {"payback_months": 9, "cap_ex": "$50,000", "op_ex_monthly": "$12,000"}
}
"""

class FinanceAgent:
    def run(self, brief: StructuredBrief) -> DepartmentOutput:
        user_prompt = f"Analyze the financial constraints in this brief:\n{brief.model_dump_json(indent=2)}"
        res_text = router.call_agent_llm("Finance", SYSTEM_PROMPT, user_prompt)
        
        try:
            cleaned = res_text.strip()
            if cleaned.startswith("```json"): cleaned = cleaned[7:]
            if cleaned.startswith("```"): cleaned = cleaned[3:]
            if cleaned.endswith("```"): cleaned = cleaned[:-3]
            data = json.loads(cleaned.strip())
            return DepartmentOutput(**data)
        except Exception as e:
            print(f"[AGENT ERROR] Finance parsing failed: {e}. Using fallback.")
            return DepartmentOutput(
                agent_name="Finance",
                summary="Conservative cash flow management required to prevent runway exhaustion.",
                key_findings=["Upfront CapEx must be minimized", "Operating margin sensitive to CAC spikes"],
                recommendations=["Implement phased budget release based on revenue milestones"],
                financial_or_operational_impact="Strict ceiling on unvalidated paid advertising.",
                explicit_assumptions=["[ASSUMPTION: 6-month minimum runway preservation required]"],
                metrics={"Max Initial Budget": "$30,000"}
            )
