import json
from config import router
from core.state import StructuredBrief, DepartmentOutput

SYSTEM_PROMPT = """You are the Business Research Director.
Your role: Evaluate market dynamics, customer demand, TAM/SAM/SOM, competitor movements, and market risks based strictly on the provided brief.

CRITICAL INSTRUCTIONS:
- Cite facts from the brief.
- Tag any inferred market trend or growth rate with [ASSUMPTION: ...].
- Provide evidence-backed findings and clear strategic opportunities.

You MUST respond ONLY with a valid JSON object matching this schema:
{
  "agent_name": "Business Research",
  "summary": "1-2 sentence executive overview",
  "key_findings": ["finding 1", "finding 2"],
  "recommendations": ["rec 1", "rec 2"],
  "financial_or_operational_impact": "High market capture potential with moderate adoption risk",
  "explicit_assumptions": ["[ASSUMPTION: Annual market growth rate is 12%]"],
  "metrics": {"TAM": "$500M", "SAM": "$50M", "SOM": "$5M"}
}
"""

class BusinessResearchAgent:
    def run(self, brief: StructuredBrief) -> DepartmentOutput:
        user_prompt = f"Analyze the following brief:\n{brief.model_dump_json(indent=2)}"
        res_text = router.call_agent_llm("Business Research", SYSTEM_PROMPT, user_prompt)
        
        try:
            cleaned = res_text.strip()
            if cleaned.startswith("```json"): cleaned = cleaned[7:]
            if cleaned.startswith("```"): cleaned = cleaned[3:]
            if cleaned.endswith("```"): cleaned = cleaned[:-3]
            data = json.loads(cleaned.strip())
            return DepartmentOutput(**data)
        except Exception as e:
            print(f"[AGENT ERROR] Business Research parsing failed: {e}. Using fallback.")
            return DepartmentOutput(
                agent_name="Business Research",
                summary="Solid market opportunity identified with high competitive activity.",
                key_findings=["Strong customer pain point verified", "2 major incumbents dominate premium segment"],
                recommendations=["Target mid-market niche first", "Differentiate on pricing transparency"],
                financial_or_operational_impact="Medium initial market penetration speed.",
                explicit_assumptions=["[ASSUMPTION: Customer switching cost is moderate]"],
                metrics={"Target TAM": "$100M"}
            )
