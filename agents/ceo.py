import json
from typing import Dict, List
from config import router
from core.state import BoardroomState, StrategyOption, CEODecision

SYSTEM_PROMPT = """You are the Chief Executive Officer (CEO).
Your role: Review all department evidence, debate challenges, and strategy options, then synthesize the final company decision.

CRITICAL INSTRUCTIONS:
1. Provide a crisp 1-sentence decision statement.
2. Direct citations of department evidence (Business Research, Finance, Marketing).
3. Explicitly state the REJECTED alternative strategy with deep rationale including:
   - `strategy_name`: Name of rejected strategy
   - `core_business_flaw`: Primary strategic/financial failure point
   - `department_pushback`: Specific evidence from Finance/Marketing/Research discrediting this option
   - `downside_risk_scenario`: Detailed catastrophic risk (e.g. insolvency runway horizon)
   - `quantitative_comparison`: Hard metrics comparing chosen strategy vs rejected option
4. List key trade-offs and risks.
5. Include tagged assumptions (`[ASSUMPTION: ...]`).
6. Create a 30-60-90 day phased implementation roadmap.
7. Define at least 3 measurable, time-bound business KPIs (e.g. CAC < $45, payback period < 8 months).

You MUST respond ONLY with a valid JSON object matching this schema:
{
  "decision_statement": "We will execute Strategy A (Phased Niche Rollout) to maximize margin while capping early burn.",
  "department_evidence_cited": {
    "Business Research": "Cited mid-market niche opportunity with high pain point.",
    "Finance": "Adopted 6-month runway preservation rule.",
    "Marketing & Sales": "Approved partner organic channel pivot."
  },
  "rejected_alternative": {
    "strategy_name": "Strategy B (Aggressive Paid Blitzscaling)",
    "core_business_flaw": "Requires unsustainable $25,000 upfront ad spend before CAC unit economics are validated.",
    "department_pushback": "Finance warned ad spend would consume >40% of the $60k total seed runway in 60 days, while Marketing admitted cold outbound ad CAC (> $75) exceeds payback thresholds.",
    "downside_risk_scenario": "Insolvency by Month 4 due to rapid cash exhaustion before recurring revenue reaches break-even velocity.",
    "quantitative_comparison": "Strategy A burns $10,000/mo with 0.6mo payback vs Strategy B burning $25,000/mo with 4.5mo payback."
  },
  "key_tradeoffs": [
    "Slower initial revenue growth in exchange for 40% lower capital risk."
  ],
  "tagged_assumptions": [
    "[ASSUMPTION: Organic referral rate reaches 15% by Month 3]"
  ],
  "implementation_roadmap": {
    "first_30_days": ["Finalize partner agreements", "Launch beta product"],
    "days_31_to_60": ["Scale organic outbound sales", "Review CAC benchmarks"],
    "days_61_to_90": ["Evaluate milestone revenue target before unlocking paid ad spend"]
  },
  "business_kpis": [
    {"metric": "Customer Acquisition Cost (CAC)", "target": "< $45", "timeframe": "By Month 3"},
    {"metric": "Monthly Recurring Revenue (MRR)", "target": "$25,000", "timeframe": "By Month 6"},
    {"metric": "Customer Payback Period", "target": "< 8 Months", "timeframe": "Q2"}
  ]
}
"""

SYSTEM_STRATEGY_PROMPT = """You are the CEO formulating strategic options.
Given the business brief and department findings, generate TWO distinct, viable strategic options tailored SPECIFICALLY to this business case idea.
Do NOT use generic boilerplate names like 'Lean Phased Growth' or 'Paid Ad Blitzscale' unless they directly match the specific case. Name each strategy according to the specific business model, market path, or operational model.

You MUST respond ONLY with a valid JSON object matching this schema:
{
  "strategies": [
    {
      "name": "Strategy A: [Specific Custom Strategy Name Tailored to Case]",
      "description": "2-sentence detailed description of this strategic approach for the specific problem",
      "pros": ["Key Advantage 1", "Key Advantage 2"],
      "cons": ["Key Risk 1", "Key Risk 2"],
      "estimated_risk": "Low-Medium",
      "projected_roi": "Estimated timeline or ROI horizon"
    },
    {
      "name": "Strategy B: [Alternative Specific Custom Strategy Name Tailored to Case]",
      "description": "2-sentence detailed description of the alternative strategic approach",
      "pros": ["Key Advantage 1", "Key Advantage 2"],
      "cons": ["Key Risk 1", "Key Risk 2"],
      "estimated_risk": "High",
      "projected_roi": "Estimated timeline or ROI horizon"
    }
  ]
}
"""

class CEOAgent:
    def formulate_strategies(self, state: BoardroomState) -> List[StrategyOption]:
        """Stage 4: Formulate two dynamic, case-specific strategies for comparison."""
        payload = {
            "brief": state.brief.model_dump() if state.brief else {},
            "department_findings": {k: v.summary for k, v in state.stage1_department_outputs.items()}
        }
        user_prompt = f"Formulate 2 contrasting, custom strategic options for this business brief:\n{json.dumps(payload, indent=2)}"
        res_text = router.call_agent_llm("CEO Synthesizer", SYSTEM_STRATEGY_PROMPT, user_prompt)
        
        try:
            cleaned = res_text.strip()
            if cleaned.startswith("```json"): cleaned = cleaned[7:]
            if cleaned.startswith("```"): cleaned = cleaned[3:]
            if cleaned.endswith("```"): cleaned = cleaned[:-3]
            data = json.loads(cleaned.strip())
            return [StrategyOption(**s) for s in data.get("strategies", [])]
        except Exception as e:
            print(f"[AGENT ERROR] Strategy formulation parsing failed: {e}. Using case fallback.")
            problem = state.brief.problem_statement if state.brief else "Business expansion"
            return [
                StrategyOption(
                    name=f"Strategy A: Focused Capital-Efficient Execution",
                    description=f"Tailored lean rollout focusing on immediate high-intent customer segments for {problem}.",
                    pros=["Preserves capital runway", "Low downside risk"],
                    cons=["Slower initial market capture"],
                    estimated_risk="Low-Medium",
                    projected_roi="180% over 18 months"
                ),
                StrategyOption(
                    name=f"Strategy B: Rapid Market Expansion Model",
                    description=f"Aggressive upfront investment path to capture broader market share rapidly.",
                    pros=["Faster brand footprint"],
                    cons=["High upfront capital burn rate"],
                    estimated_risk="High",
                    projected_roi="250% if unit economics hold"
                )
            ]

    def make_final_decision(self, state: BoardroomState) -> CEODecision:
        """Stage 5: Synthesize complete CEO decision dossier."""
        summary_payload = {
            "brief": state.brief.model_dump() if state.brief else {},
            "department_outputs": {k: v.model_dump() for k, v in state.stage1_department_outputs.items()},
            "challenges": [c.model_dump() for c in state.stage3_challenges],
            "strategies_compared": [s.model_dump() for s in state.stage4_strategies]
        }
        
        user_prompt = f"Synthesize the final CEO decision from this boardroom trace:\n{json.dumps(summary_payload, indent=2)}"
        res_text = router.call_agent_llm("CEO Synthesizer", SYSTEM_PROMPT, user_prompt)
        
        try:
            cleaned = res_text.strip()
            if cleaned.startswith("```json"): cleaned = cleaned[7:]
            if cleaned.startswith("```"): cleaned = cleaned[3:]
            if cleaned.endswith("```"): cleaned = cleaned[:-3]
            data = json.loads(cleaned.strip())
            return CEODecision(**data)
        except Exception as e:
            print(f"[AGENT ERROR] CEO decision parsing failed: {e}. Using fallback decision.")
            return CEODecision(
                decision_statement="Execute Strategy A (Lean Phased Growth) prioritizing capital preservation and organic unit economics.",
                department_evidence_cited={
                    "Finance": "Adopted strict budget ceiling to preserve 6-month runway.",
                    "Marketing & Sales": "Pivoted initial focus to low-cost partner distribution channels.",
                    "Business Research": "Targeting mid-market niche with proven customer pain point."
                },
                rejected_alternative={
                    "strategy_name": "Strategy B (Aggressive Paid Blitzscale)",
                    "rejection_reason": "Rejected due to high risk of CAC inflation and early capital exhaustion."
                },
                key_tradeoffs=["Accepting moderate initial revenue growth to de-risk bankruptcy probability."],
                tagged_assumptions=["[ASSUMPTION: Organic channel conversion rate stays above 2.5%]"],
                implementation_roadmap={
                    "first_30_days": ["Finalize core product offering", "Establish 3 key partner channels"],
                    "days_31_to_60": ["Acquire first 50 pilot accounts", "Validate retention metrics"],
                    "days_61_to_90": ["Review cash flow and consider unlocking paid advertising tier"]
                },
                business_kpis=[
                    {"metric": "CAC", "target": "< $40", "timeframe": "Month 3"},
                    {"metric": "Gross Margin", "target": "> 65%", "timeframe": "Month 6"},
                    {"metric": "Runway Preserved", "target": "> 9 Months", "timeframe": "Ongoing"}
                ]
            )
