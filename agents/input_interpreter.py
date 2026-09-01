import json
from config import router
from core.state import StructuredBrief

SYSTEM_PROMPT = """You are the Input Interpreter Agent in an executive AI Boardroom.
Your role: Analyze the raw business case with extreme precision.

CRITICAL INSTRUCTIONS:
1. Extract explicit, hard facts directly stated in the text.
2. Identify implicit or missing information and explicitly tag it as an [ASSUMPTION].
3. Identify core constraints (budget limits, deadlines, regulations) and success criteria.

You MUST respond ONLY with a valid JSON object with the following schema:
{
  "problem_statement": "Concise 1-2 sentence problem definition",
  "supplied_facts": ["fact 1", "fact 2"],
  "identified_assumptions": ["[ASSUMPTION: description 1]", "[ASSUMPTION: description 2]"],
  "hard_constraints": ["constraint 1", "constraint 2"],
  "success_criteria": ["criterion 1", "criterion 2"]
}
Do not include any conversational intro or markdown code fences other than JSON.
"""

class InputInterpreterAgent:
    def run(self, raw_case_text: str) -> StructuredBrief:
        user_prompt = f"Deconstruct the following raw business case text:\n\n{raw_case_text}"
        res_text = router.call_agent_llm("Input Interpreter", SYSTEM_PROMPT, user_prompt)
        
        try:
            # Clean markdown formatting if present
            cleaned = res_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            data = json.loads(cleaned.strip())
            return StructuredBrief(**data)
        except Exception as e:
            print(f"[AGENT ERROR] Input Interpreter parsing failed: {e}. Using structured fallback.")
            return StructuredBrief(
                problem_statement="Business case analysis under ambiguity.",
                supplied_facts=[line for line in raw_case_text.split("\n") if line.strip()][:5],
                identified_assumptions=["[ASSUMPTION: Operational parameters based on standard industry averages]"],
                hard_constraints=["Strict fiscal budget cap", "Rapid timeline to market"],
                success_criteria=["Positive ROI within 12 months", "Customer satisfaction > 85%"]
            )
