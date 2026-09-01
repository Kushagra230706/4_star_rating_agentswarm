import json
from typing import Dict, List
from config import router
from core.state import BoardroomState, StrategyOption, CEODecision

SYSTEM_PROMPT = """You are the Chief Executive Officer (CEO).
Your role: Review all department evidence, debate challenges, and strategy options, then synthesize the final company decision.

CRITICAL INSTRUCTIONS:
1. Provide a crisp 1-sentence decision statement.
2. Direct citations of department evidence (Business Research, Finance, Marketing).
3. Explicitly state the REJECTED alternative strategy and give the exact business rationale for rejecting it.
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
    "rejection_reason": "Rejected due to unsustainable early cash burn and unvalidated CAC assumptions."
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

class CEOAgent:
    def formulate_strategies(self, state: BoardroomState) -> List[StrategyOption]:
        """Stage 4: Formulate two viable strategies for comparison."""
        return [
            StrategyOption(
                name="Strategy A: Lean Phased Growth (Organic & Partner First)",
                description="Focus on high-margin mid-market accounts using low-cost organic channels, preserving capital until unit economics are proven.",
                pros=["Preserves cash runway", "Lower downside financial risk", "High customer retention potential"],
                cons=["Slower initial top-line growth speed", "Risk of competitor fast-following"],
                estimated_risk="Low-Medium",
                projected_roi="180% over 18 months"
            ),
            StrategyOption(
                name="Strategy B: Aggressive Market Blitzscale (Paid Ad Driven)",
                description="Heavy upfront paid marketing ad spend to capture maximum initial market share across broad demographics.",
                pros=["Faster market penetration", "High top-line brand visibility"],
                cons=["High capital burn rate", "Vulnerable to CAC inflation and runway exhaustion"],
                estimated_risk="High",
                projected_roi="250% if CAC holds, negative if CAC spikes"
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
