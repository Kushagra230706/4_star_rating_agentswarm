from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class StructuredBrief(BaseModel):
    problem_statement: str = ""
    supplied_facts: List[str] = Field(default_factory=list)
    identified_assumptions: List[str] = Field(default_factory=list)
    hard_constraints: List[str] = Field(default_factory=list)
    success_criteria: List[str] = Field(default_factory=list)

class DepartmentOutput(BaseModel):
    agent_name: str
    summary: str = ""
    key_findings: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    financial_or_operational_impact: str = ""
    explicit_assumptions: List[str] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)

class ChallengeMemo(BaseModel):
    challenger: str = "Risk & Reviewer Agent"
    target_agent: str = ""
    contested_point: str = ""
    critique_rationale: str = ""
    recommended_adjustment: str = ""
    rebuttal_response: Optional[str] = None

class StrategyOption(BaseModel):
    name: str
    description: str
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)
    estimated_risk: str = "Medium"
    projected_roi: str = ""

class ImplementationRoadmap(BaseModel):
    first_30_days: List[str] = Field(default_factory=list)
    days_31_to_60: List[str] = Field(default_factory=list)
    days_61_to_90: List[str] = Field(default_factory=list)

class CEODecision(BaseModel):
    decision_statement: str = ""
    department_evidence_cited: Dict[str, str] = Field(default_factory=dict)
    rejected_alternative: Dict[str, str] = Field(default_factory=dict) # e.g. {"strategy": "Strategy B", "reason": "..."}
    key_tradeoffs: List[str] = Field(default_factory=list)
    tagged_assumptions: List[str] = Field(default_factory=list)
    implementation_roadmap: Dict[str, List[str]] = Field(default_factory=dict)
    business_kpis: List[Dict[str, str]] = Field(default_factory=list)

class TraceEntry(BaseModel):
    stage: str
    agent: str
    timestamp: str
    action: str
    content: Any

class BoardroomState(BaseModel):
    brief: Optional[StructuredBrief] = None
    stage1_department_outputs: Dict[str, DepartmentOutput] = Field(default_factory=dict)
    stage3_challenges: List[ChallengeMemo] = Field(default_factory=list)
    stage4_strategies: List[StrategyOption] = Field(default_factory=list)
    stage5_ceo_decision: Optional[CEODecision] = None
    execution_trace: List[TraceEntry] = Field(default_factory=list)
    debate_cycle_count: int = 0
