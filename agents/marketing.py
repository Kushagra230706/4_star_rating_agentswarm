import json
from config import router
from core.state import StructuredBrief, DepartmentOutput

SYSTEM_PROMPT = """You are the Chief Commercial Officer (Marketing & Sales).
Your role: Define Target Customer Profiles (ICP), Customer Acquisition Channels, Pricing Strategy, and Go-To-Market (GTM) rollout.

CRITICAL INSTRUCTIONS:
- Present aggressive growth strategies while acknowledging acquisition costs.
- Tag unvalidated conversion rates with [ASSUMPTION: ...].

You MUST respond ONLY with a valid JSON object matching this schema:
{
  "agent_name": "Marketing & Sales",
  "summary": "1-2 sentence GTM acquisition strategy summary",
  "key_findings": ["finding 1", "finding 2"],
  "recommendations": ["recommendation 1", "recommendation 2"],
  "financial_or_operational_impact": "Requires $25k initial ad spend; projects 500 accounts in Q1",
  "explicit_assumptions": ["[ASSUMPTION: Paid search conversion rate is 3.5%]"],
  "metrics": {"target_cac": "$45", "target_ltv": "$350", "primary_channel": "Paid Search & LinkedIn B2B"}
}
"""

class MarketingAgent:
    def run(self, brief: StructuredBrief) -> DepartmentOutput:
        user_prompt = f"Analyze the acquisition opportunities in this brief:\n{brief.model_dump_json(indent=2)}"
        res_text = router.call_agent_llm("Marketing & Sales", SYSTEM_PROMPT, user_prompt)
        
        try:
            cleaned = res_text.strip()
            if cleaned.startswith("```json"): cleaned = cleaned[7:]
            if cleaned.startswith("```"): cleaned = cleaned[3:]
            if cleaned.endswith("```"): cleaned = cleaned[:-3]
            data = json.loads(cleaned.strip())
            return DepartmentOutput(**data)
        except Exception as e:
            print(f"[AGENT ERROR] Marketing parsing failed: {e}. Using fallback.")
            return DepartmentOutput(
                agent_name="Marketing & Sales",
                summary="Multi-channel acquisition strategy prioritizing digital paid channels.",
                key_findings=["B2B decision makers respond best to targeted case studies"],
                recommendations=["Launch targeted campaign on Google Search and LinkedIn"],
                financial_or_operational_impact="Initial customer acquisition drive requiring ad spend.",
                explicit_assumptions=["[ASSUMPTION: CAC estimated at $50 per qualified lead]"],
                metrics={"Channel": "Digital Outbound"}
            )
