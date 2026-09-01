import json
from typing import Dict, List
from config import router
from core.state import DepartmentOutput, ChallengeMemo

SYSTEM_PROMPT = """You are the Chief Risk Officer & Devil's Advocate in the executive boardroom.
Your role: Scrutinize the outputs from Business Research, Finance, and Marketing & Sales.
You MUST identify at least one material disagreement or flawed assumption between departments (e.g., Marketing's target CAC conflicts with Finance's conservative budget, or Research's market size is overly optimistic).

You MUST respond ONLY with a valid JSON object containing an array of challenges matching this schema:
{
  "challenges": [
    {
      "challenger": "Risk & Reviewer Agent",
      "target_agent": "Marketing & Sales",
      "contested_point": "The proposed $25,000 paid advertising spend assumes a $45 CAC",
      "critique_rationale": "Finance has capped overall spend and benchmark CAC in this segment is historically >$75, risking budget exhaustion.",
      "recommended_adjustment": "Pivot 60% of marketing effort to organic partner distribution to lower cash burn."
    }
  ]
}
"""

class RiskReviewerAgent:
    def run(self, dept_outputs: Dict[str, DepartmentOutput]) -> List[ChallengeMemo]:
        context = {name: out.model_dump() for name, out in dept_outputs.items()}
        user_prompt = f"Evaluate these department outputs for risks and conflicts:\n{json.dumps(context, indent=2)}"
        res_text = router.call_agent_llm("Risk & Reviewer", SYSTEM_PROMPT, user_prompt)
        
        try:
            cleaned = res_text.strip()
            if cleaned.startswith("```json"): cleaned = cleaned[7:]
            if cleaned.startswith("```"): cleaned = cleaned[3:]
            if cleaned.endswith("```"): cleaned = cleaned[:-3]
            data = json.loads(cleaned.strip())
            challenges = [ChallengeMemo(**item) for item in data.get("challenges", [])]
            return challenges if challenges else self._default_challenge()
        except Exception as e:
            print(f"[AGENT ERROR] Risk Reviewer parsing failed: {e}. Using fallback dispute.")
            return self._default_challenge()

    def _default_challenge(self) -> List[ChallengeMemo]:
        return [
            ChallengeMemo(
                challenger="Risk & Reviewer Agent",
                target_agent="Marketing & Sales",
                contested_point="Marketing's aggressive paid acquisition budget projections.",
                critique_rationale="Finance has imposed a conservative cash preservation rule; unvalidated paid ad burn poses high insolvency risk.",
                recommended_adjustment="Cap paid ad spending to 30% of marketing budget and tie further funding to CAC milestone targets."
            )
        ]

    def generate_rebuttal(self, challenge: ChallengeMemo, dept_output: DepartmentOutput) -> str:
        """Simulates the challenged department's rebuttal or concession during Stage 3."""
        prompt = f"""
Agent '{challenge.target_agent}' received this challenge from Risk Reviewer:
Contested Point: {challenge.contested_point}
Critique Rationale: {challenge.critique_rationale}
Recommended Adjustment: {challenge.recommended_adjustment}

Your Original Output: {dept_output.summary}

Provide a crisp 2-sentence response either defending your position with revised assumptions or conceding to the adjustment.
"""
        return router.call_agent_llm(challenge.target_agent, "You are a executive responding to a peer review challenge.", prompt).strip()
