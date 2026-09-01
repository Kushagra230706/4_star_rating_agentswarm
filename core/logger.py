import os
import json
import datetime
from typing import Dict, Any
from core.state import BoardroomState

class AuditLogger:
    """
    Exports boardroom state into auditable JSON and Markdown trace reports.
    Satisfies technical requirements for traceable audit record.
    """
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export_trace_json(self, state: BoardroomState, filename: str = "baseline_trace.json") -> str:
        filepath = os.path.join(self.output_dir, filename)
        data = state.model_dump()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[AUDIT LOG] Exported JSON trace to {filepath}")
        return filepath

    def export_decision_markdown(self, state: BoardroomState, filename: str = "baseline_decision.md", title: str = "Baseline CEO Decision Dossier") -> str:
        filepath = os.path.join(self.output_dir, filename)
        ceo = state.stage5_ceo_decision
        brief = state.brief
        
        md = []
        md.append(f"# {title}")
        md.append(f"*Generated at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        if brief:
            md.append("## 1. Executive Problem Brief")
            md.append(f"**Problem**: {brief.problem_statement}\n")
            md.append("### Supplied Case Facts")
            for fact in brief.supplied_facts:
                md.append(f"- {fact}")
            md.append("\n### Tagged Assumptions")
            for ass in brief.identified_assumptions:
                md.append(f"- `{ass}`")
            md.append("\n---\n")

        md.append("## 2. Department Analysis & Evidence (Stage 1 & 2)")
        for agent_name, dept in state.stage1_department_outputs.items():
            md.append(f"### {agent_name}")
            md.append(f"**Summary**: {dept.summary}")
            md.append("**Key Findings**:")
            for kf in dept.key_findings:
                md.append(f"- {kf}")
            md.append(f"**Financial/Operational Impact**: {dept.financial_or_operational_impact}\n")

        md.append("---\n## 3. Stage 3: Risk Challenge & Debate Trace")
        for ch in state.stage3_challenges:
            md.append(f"### Challenge to `{ch.target_agent}`")
            md.append(f"- **Contested Point**: {ch.contested_point}")
            md.append(f"- **Critique Rationale**: {ch.critique_rationale}")
            md.append(f"- **Recommended Adjustment**: {ch.recommended_adjustment}")
            if ch.rebuttal_response:
                md.append(f"- **Rebuttal/Revision**: {ch.rebuttal_response}")
            md.append("")

        md.append("---\n## 4. Stage 4: Strategy Tradeoff Comparison")
        for strat in state.stage4_strategies:
            md.append(f"### {strat.name}")
            md.append(f"**Description**: {strat.description}")
            md.append(f"**Estimated Risk**: {strat.estimated_risk} | **Projected ROI**: {strat.projected_roi}")
            md.append("**Pros**:")
            for p in strat.pros:
                md.append(f"- {p}")
            md.append("**Cons**:")
            for c in strat.cons:
                md.append(f"- {c}")
            md.append("")

        if ceo:
            md.append("---\n## 5. Stage 5: Final CEO Decision Dossier")
            md.append(f"### 📌 Final Order")
            md.append(f"> **{ceo.decision_statement}**\n")
            
            md.append("### 🏛️ Department Evidence Cited")
            for dept, ev in ceo.department_evidence_cited.items():
                md.append(f"- **{dept}**: {ev}")
                
            md.append("\n### ❌ Rejected Alternative & Rationale")
            for k, v in ceo.rejected_alternative.items():
                md.append(f"- **{k}**: {v}")
                
            md.append("\n### ⚖️ Major Trade-offs & Risks")
            for to in ceo.key_tradeoffs:
                md.append(f"- {to}")

            md.append("\n### 🏷️ Tagged Assumptions")
            for tag in ceo.tagged_assumptions:
                md.append(f"- `{tag}`")

            md.append("\n### 🗺️ Phased Implementation Roadmap")
            for phase, steps in ceo.implementation_roadmap.items():
                md.append(f"#### {phase.replace('_', ' ').title()}")
                for step in steps:
                    md.append(f"- {step}")

            md.append("\n### 📊 Measurable Business KPIs")
            for kpi in ceo.business_kpis:
                md.append(f"- **{kpi.get('metric', 'KPI')}**: Target `{kpi.get('target', 'N/A')}` ({kpi.get('timeframe', 'Timeframe')})")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        print(f"[AUDIT LOG] Exported Markdown report to {filepath}")
        return filepath
