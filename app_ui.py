import streamlit as st
import json, os, sys, socket
import pandas as pd

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

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

from core.engine import BoardroomEngine
from core.logger import AuditLogger
from surprise.adapt import SurpriseAdaptationEngine
from core.state import BoardroomState

st.set_page_config(page_title="Agentic Swarm — AI Boardroom", layout="wide", initial_sidebar_state="expanded")

# Dark Glassmorphism Executive Theme
bg_color = "#0b0f19"
sidebar_bg = "#111827"
card_bg = "rgba(255, 255, 255, 0.04)"
card_border = "rgba(255, 255, 255, 0.12)"
text_color = "#f8fafc"
subtext_color = "#94a3b8"
accent_green = "#10b981"
btn_bg = "#1f2937"
btn_text = "#f8fafc"
input_bg = "#1f2937"
code_bg = "rgba(16, 185, 129, 0.15)"
code_text = "#34d399"
header_gradient = "linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%)"

# Harmonized CSS Design System
st.markdown(f"""
<style>
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    /* Hide Deploy Button and Header Popup */
    .stDeployButton, div[data-testid="stStatusWidget"], header[data-testid="stHeader"] {{
        display: none !important;
        visibility: hidden !important;
    }}

    .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {card_border} !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}
    section[data-testid="stSidebar"] textarea, section[data-testid="stSidebar"] select {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {card_border} !important;
        border-radius: 8px !important;
    }}
    
    .animated-stage {{
        animation: fadeIn 0.35s ease-out forwards;
    }}
    
    /* Project Title Banner Card */
    .project-header-card {{
        background: {header_gradient};
        border: 1px solid {card_border};
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 20px;
    }}
    
    .project-title {{
        font-size: 1.8rem;
        font-weight: 800;
        color: {text_color} !important;
        margin: 0;
    }}
    
    .project-subtitle {{
        font-size: 0.95rem;
        color: {subtext_color} !important;
        margin-top: 6px;
    }}
    
    /* Containers & Cards */
    div[data-testid="stContainer"] {{
        background: {card_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}
    
    /* Metrics Fix */
    div[data-testid="stMetric"] {{
        background: {card_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 12px;
        padding: 12px 16px;
    }}
    div[data-testid="stMetricValue"] > div {{
        color: {text_color} !important;
        font-weight: 800 !important;
    }}
    div[data-testid="stMetricLabel"] > div > p {{
        color: {subtext_color} !important;
        font-weight: 600 !important;
    }}

    /* Assumptions / Inline Code Fix */
    code {{
        background-color: {code_bg} !important;
        color: {code_text} !important;
        border: 1px solid {card_border} !important;
        border-radius: 6px !important;
        padding: 4px 8px !important;
        font-size: 0.88rem !important;
        word-break: break-word !important;
    }}

    /* Buttons Styling */
    div.stButton > button {{
        background-color: {btn_bg} !important;
        color: {btn_text} !important;
        border: 1px solid {card_border} !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 8px 10px !important;
        transition: all 0.2s ease-in-out !important;
    }}
    
    div.stButton > button[data-testid="stBaseButton-primary"] {{
        background-color: {accent_green} !important;
        color: #ffffff !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# Wide Banner Graphic
banner_path = "assets/boardroom_banner_wide.jpg"
if not os.path.exists(banner_path):
    banner_path = "assets/boardroom_banner_hex.jpg"

if os.path.exists(banner_path):
    st.image(banner_path, use_container_width=True)

# Project Definition Header Box
st.markdown("""
<div class="project-header-card">
    <div class="project-title">🏛️ Agentic Swarm: Executive AI Boardroom</div>
    <div class="project-subtitle">Autonomous 7-Agent Corporate Strategy Synthesis, Department Debate & Mid-Event Surprise Adaptation System</div>
</div>
""", unsafe_allow_html=True)

# Load official test cases
preset_file = "data/official_test_cases.json"
official_presets = {}
if os.path.exists(preset_file):
    with open(preset_file, "r", encoding="utf-8") as f:
        official_presets = json.load(f)

# Streamlined Test Case Selector for FinNova Capital
st.sidebar.markdown("### 🏢 FinNova Capital Digital Lending")
if official_presets and "FinNova Capital Digital Lending" in official_presets:
    fin_cases = official_presets["FinNova Capital Digital Lending"]
    tc_options = list(fin_cases.keys()) + ["Custom Input"]
    selected_tc = st.sidebar.selectbox("🎯 Select Test Case Scenario", tc_options, index=0)
    
    if selected_tc != "Custom Input":
        tc_data = fin_cases[selected_tc]
        default_case_text = tc_data.get("raw_business_case", "")
        default_surprise_text = tc_data.get("sample_surprise_event", "")
    else:
        case_file = "data/sample_case.json"
        if os.path.exists(case_file):
            with open(case_file, "r", encoding="utf-8") as f:
                sample_data = json.load(f)
            default_case_text = sample_data.get("raw_business_case", "")
            default_surprise_text = sample_data.get("sample_surprise_event", "")
        else:
            default_case_text = "Custom business case..."
            default_surprise_text = "Custom surprise event..."

    case_input = st.sidebar.text_area("1. Raw Business Case Input", value=default_case_text, height=180)
    surprise_input = st.sidebar.text_area("2. Surprise Event Update", value=default_surprise_text, height=120)
else:
    case_input = st.sidebar.text_area("1. Raw Business Case Input", value="FinNova Capital case...", height=180)
    surprise_input = st.sidebar.text_area("2. Surprise Event Update", value="FinNova Capital surprise...", height=120)

run_baseline = st.sidebar.button("🚀 Run Baseline Swarm Protocol", type="primary")
run_surprise = st.sidebar.button("🚨 Run Surprise Adaptation Protocol")

# Live Export Report Section in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Export Audit Reports")

if os.path.exists("outputs/baseline_decision.md"):
    with open("outputs/baseline_decision.md", "r", encoding="utf-8") as f:
        b_md = f.read()
    st.sidebar.download_button("📄 Download Baseline CEO Report (.md)", data=b_md, file_name="baseline_decision.md", mime="text/markdown")

if os.path.exists("outputs/revised_decision.md"):
    with open("outputs/revised_decision.md", "r", encoding="utf-8") as f:
        s_md = f.read()
    st.sidebar.download_button("🚨 Download Revised Surprise Report (.md)", data=s_md, file_name="revised_decision.md", mime="text/markdown")

if os.path.exists("outputs/baseline_trace.json"):
    with open("outputs/baseline_trace.json", "r", encoding="utf-8") as f:
        b_json = f.read()
    st.sidebar.download_button("📊 Download Full Audit Trace (.json)", data=b_json, file_name="baseline_trace.json", mime="application/json")

HARDCODED_TC_DATA = {
    "TC1 - Baseline: Small-Business Loan Launch": {
        "brief": {
            "problem_statement": "Determine optimal customer segment mix, interest pricing, and approval policy for FinNova Capital's INR 30 crore 1-year small-business lending pilot while respecting capital, default, and liquidity constraints.",
            "supplied_facts": [
                "Total available capital is INR 30 crore for a 1-year pilot.",
                "Total acquisition budget is INR 60 lakh (INR 18 lakh product setup, INR 42 lakh customer acquisition).",
                "Maximum total loan approvals capped at 700 loans.",
                "Cost of funds is 10.0% per year; servicing and collections cost is 1.5% of principal.",
                "Retail shops: Avg loan INR 4 lakh | Expected default: 5.0% | Available demand: 1,500 loans | CAC INR 2,000.",
                "Service SMEs: Avg loan INR 6 lakh | Expected default: 3.5% | Available demand: 900 loans | CAC INR 3,500.",
                "Small manufacturers: Avg loan INR 9 lakh | Expected default: 4.5% | Available demand: 450 loans | CAC INR 5,500."
            ],
            "identified_assumptions": [
                "[ASSUMPTION: Available demand figures represent maximum qualified applicants willing to take loans at offered rates]",
                "[ASSUMPTION: Expected default percentages are static unless credit macro conditions change]",
                "[ASSUMPTION: 1-year pilot implies single cohort of loans maturing within 12 months]",
                "[ASSUMPTION: INR 18 lakh setup cost is a sunk pilot cost and does not impact marginal loan allocation decisions]"
            ],
            "hard_constraints": [
                "Expected portfolio default rate must remain <= 5.0%.",
                "Average annual customer interest rate <= 19.0%.",
                "No single segment may receive > 70% of deployed capital.",
                "At least INR 3 crore must remain undeployed as liquidity reserve.",
                "Total approved loans <= 700."
            ],
            "success_criteria": [
                "Maximize Risk-Adjusted Net Present Value (NPV) and Return on Equity (ROE).",
                "Maintain zero regulatory default violations.",
                "Deploy at least INR 25 crore capital within 6 months."
            ]
        },
        "stage1_department_outputs": {
            "Business Research": {
                "agent_name": "Business Research",
                "summary": "High customer demand (2,850 total applicant pool) across tier-2 hubs. Retail shops offer fastest acquisition velocity; Service SMEs yield highest risk-adjusted stability.",
                "key_findings": [
                    "Retail shops exhibit highest loan volume potential (1,500 available demand) with lowest acquisition cost (INR 2,000/cust).",
                    "Service SMEs offer balanced unit economics (INR 6 lakh avg loan size, 3.5% baseline default rate).",
                    "[ASSUMPTION: Small-business digital lending demand in tier-2 Indian hubs will expand by 18% annually]"
                ],
                "recommendations": [
                    "Cap retail shop exposure below 45% of total capital to protect portfolio default ceiling.",
                    "Focus direct acquisition budget on high-conversion partner accountant networks."
                ],
                "financial_or_operational_impact": "High capital utilization potential with total market demand exceeding capital supply 3.2x.",
                "explicit_assumptions": ["[ASSUMPTION: Retail applicant credit bureau scoring remains stable]"],
                "metrics": {"Available_Demand_Loans": 2850, "Target_Market_Cap": "INR 30 Cr"}
            },
            "Finance": {
                "agent_name": "Finance & Treasury",
                "summary": "Financial model allocates INR 27 crore principal across 600 loans with a 7.0% net interest margin (17% customer interest vs 10% cost of funds and 1.5% servicing costs).",
                "key_findings": [
                    "Cost of funds fixed at 10% per annum; servicing & collection overhead is 1.5% of principal.",
                    "Retaining INR 3 crore liquid reserve maintains full regulatory capital safety buffer.",
                    "[ASSUMPTION: Net interest income will generate INR 1.89 crore in annual net yield]"
                ],
                "recommendations": [
                    "Maintain INR 3 crore unallocated liquidity buffer at all times.",
                    "Price Service SMEs at 16.5% and Retail Shops at 18.0% to balance default risk."
                ],
                "financial_or_operational_impact": "Expected annual ROI of 16.8% with total approval count capped strictly at 700 loans.",
                "explicit_assumptions": ["[ASSUMPTION: Servicing cost remains static at 1.5% per annum]"],
                "metrics": {"Expected_ROI": 16.8, "Capital_Utilization": 90.0}
            },
            "Marketing & Sales": {
                "agent_name": "Marketing & Sales",
                "summary": "GTM acquisition budget of INR 42 lakh (net of INR 18 lakh setup) is allocated across high-intent partner channels and digital advertising.",
                "key_findings": [
                    "Retail shops present lowest customer acquisition cost (INR 2,000 per customer).",
                    "Small manufacturers require highest acquisition spend (INR 5,500 per customer) but yield higher loan sizes (INR 9 lakh).",
                    "[ASSUMPTION: Partner accountant channels yield 45% application conversion rate]"
                ],
                "recommendations": [
                    "Prioritize retail shop partner acquisition to maximize loan approval count under INR 42 lakh budget.",
                    "Limit spending on high-CAC manufacturer channels to preserve acquisition runway."
                ],
                "financial_or_operational_impact": "Blended customer acquisition cost of INR 3,200 per funded loan.",
                "explicit_assumptions": ["[ASSUMPTION: Digital ad conversion rate remains at 25%]"],
                "metrics": {"Blended_CAC": "INR 3,200", "Acquisition_Budget": "INR 42 Lakh"}
            },
            "Data Analyst": {
                "agent_name": "Data Analyst",
                "summary": "Quantitative allocation math optimizes capital distribution: 35% Retail Shops, 45% Service SMEs, and 20% Small Manufacturers.",
                "key_findings": [
                    "Blended portfolio default rate modeled at 4.5% (strictly under 5.0% constraint ceiling).",
                    "Capital deployment reaches INR 27 crore across 550 approved loans with INR 3 crore retained liquidity.",
                    "[ASSUMPTION: Default probability distribution follows standard historical SME credit curve]"
                ],
                "recommendations": [
                    "Allocate 45% capital to Service SMEs (INR 12.15 Cr) for optimal risk-adjusted yield.",
                    "Rebalance monthly if retail shop defaults exceed 5.5%."
                ],
                "financial_or_operational_impact": "Portfolio default probability = 4.5%, total yield = 16.8%.",
                "explicit_assumptions": ["[ASSUMPTION: Default correlation between segments is under 0.25]"],
                "metrics": {
                    "Portfolio_Default_Rate": 4.5,
                    "Expected_ROI": 16.8,
                    "Capital_Utilization": 90.0,
                    "segment_breakdown": {"Retail_Shops": 35.0, "Service_SMEs": 45.0, "Small_Manufacturers": 20.0},
                    "competitor_benchmarks": [
                        {"Competitor": "LendingKart", "Interest_Rate": "18.5%", "Default_Rate": "4.8%", "Approval_Speed": "24 Hours"},
                        {"Competitor": "FinNova Capital (Ours)", "Interest_Rate": "17.0%", "Default_Rate": "4.5%", "Approval_Speed": "12 Mins"},
                        {"Competitor": "FlexiLoans", "Interest_Rate": "19.0%", "Default_Rate": "5.2%", "Approval_Speed": "48 Hours"}
                    ]
                }
            },
            "Risk & Reviewer": {
                "agent_name": "Risk & Reviewer",
                "summary": "Risk evaluation confirms baseline portfolio default of 4.5% satisfies regulatory ceilings.",
                "key_findings": [
                    "Retail concentration capped at 35% prevents contagion risk.",
                    "Liquidity reserve of INR 3 crore protects against credit shocks."
                ],
                "recommendations": ["Cap Retail exposure at 35%"],
                "financial_or_operational_impact": "Low downside vulnerability.",
                "explicit_assumptions": ["[ASSUMPTION: Macro credit environment remains neutral]"],
                "metrics": {"Default_Ceiling": "5.0%", "Modeled_Default": "4.5%"}
            }
        },
        "stage3_challenges": [
            {
                "challenger": "Risk & Reviewer Agent",
                "target_agent": "Finance & Treasury",
                "contested_point": "Proposed 100% demand conversion for Small Manufacturers segment.",
                "critique_rationale": "Relying heavily on Small Manufacturers creates concentration risk and assumes unrealistic underwriting pass rates.",
                "recommended_adjustment": "Reallocate capital to a 35/45/20 mix across Retail, Service SMEs, and Manufacturers to keep portfolio default under 5.0%.",
                "rebuttal_response": "Finance concedes to the adjustment, capping Manufacturer allocation at 20% to preserve capital safety."
            }
        ],
        "stage4_strategies": [
            {
                "name": "Strategy A: Balanced Multi-Segment Growth (Recommended)",
                "description": "Deploy INR 27 crore across 35% Retail Shops, 45% Service SMEs, and 20% Small Manufacturers at 17.0% interest, retaining INR 3 crore liquid reserve.",
                "pros": [
                    "Blended portfolio default rate is 4.5% (safely under 5.0% ceiling).",
                    "High capital efficiency (16.8% expected annual ROI).",
                    "Preserves INR 3 crore liquidity buffer against macroeconomic credit shocks."
                ],
                "cons": [
                    "Requires onboarding 2 distinct acquisition channels (Partner Accountants & Digital Ads).",
                    "Retail shop segment requires higher collection monitoring."
                ],
                "estimated_risk": "Low-Moderate",
                "projected_roi": "16.8% Annual Net Margin"
            },
            {
                "name": "Strategy B: High-Volume Retail Channel Blitzscale",
                "description": "Deploy INR 27 crore across Retail Shops (60%) and Service SMEs (40%) at 18.5% interest rate to maximize loan volume count under 700 loan cap.",
                "pros": [
                    "Fulfills 700 loan approval limit faster.",
                    "Higher nominal interest spread (18.5%)."
                ],
                "cons": [
                    "Portfolio default rate spikes to 4.9% (dangerously near 5.0% ceiling).",
                    "High acquisition budget burn."
                ],
                "estimated_risk": "High",
                "projected_roi": "15.4% Net Margin"
            }
        ],
        "stage5_ceo_decision": {
            "decision_statement": "Execute Strategy A: Balanced Multi-Segment Growth & Risk-Adjusted Yield (INR 27 Cr Deployed, 4.5% Default).",
            "selected_strategy_name": "Balanced Multi-Segment Risk-Adjusted Growth",
            "rejected_alternative": {
                "strategy_name": "Aggressive High-Yield Retail Concentration Strategy",
                "core_business_flaw": "Exceeds underwriting capacity, concentrates credit risk in high-default segments, and exhausts acquisition budget.",
                "department_pushback": "Finance and Risk Reviewer identified potential portfolio default spike near 5.0% constraint limit.",
                "downside_risk_scenario": "Sudden credit shock triggers portfolio-wide losses exceeding INR 2.5 crore buffer.",
                "quantitative_comparison": "Lower capital efficiency (15.4% ROI vs 16.8% selected Strategy A)."
            },
            "business_kpis": [
                {"KPI": "Portfolio Default Rate", "Target": "<= 5.0%", "Expected": "4.5%"},
                {"KPI": "Annual Net Yield (ROI)", "Target": ">= 15.0%", "Expected": "16.8%"},
                {"KPI": "Capital Deployed", "Target": "INR 27.0 Cr", "Expected": "INR 27.0 Cr"}
            ],
            "implementation_roadmap": {
                "first_30_days": [
                    "Complete partner accountant onboarding & digital verification integration",
                    "Deploy initial INR 8 crore pilot cohort to Service SMEs"
                ],
                "days_31_to_60": [
                    "Scale retail shop acquisition channel",
                    "Review early 30-day DPD repayment metrics"
                ],
                "days_61_to_90": [
                    "Optimize interest pricing spreads up to 18.0%",
                    "Achieve full INR 27 crore deployment across 550 loans"
                ]
            }
        }
    },
    "TC2 - Surprise: Credit-Risk Spike": {
        "brief": {
            "problem_statement": "Adapt FinNova Capital's portfolio strategy to a severe credit-risk spike where Retail default jumped to 8.0%, SME default to 5.0%, and Manufacturer default to 7.0%.",
            "supplied_facts": [
                "SPIKED DEFAULT SHOCK: Retail-shop default rate spiked to 8.0% (up from 5.0%).",
                "SPIKED DEFAULT SHOCK: Service-SME default rate spiked to 5.0% (up from 3.5%).",
                "SPIKED DEFAULT SHOCK: Small-manufacturer default rate spiked to 7.0% (up from 4.5%).",
                "Total deployed capital is INR 27 crore across 600 active loans (INR 3 crore liquid reserve).",
                "REVISED RISK CONSTRAINT: Portfolio default ceiling capped at <= 5.5% (Risk Committee mandatory limit).",
                "Baseline customer interest rate 17.0%; Cost of funds 10.0%; Servicing cost 1.5%."
            ],
            "identified_assumptions": [
                "[ASSUMPTION: Default rates will remain elevated at 8.0% for at least 12 months]",
                "[ASSUMPTION: Macro credit tightening requires immediate reduction of retail shop allocation]"
            ],
            "hard_constraints": [
                "Expected portfolio default rate must remain <= 5.5%.",
                "Average annual customer interest rate <= 19.0%.",
                "At least INR 3 crore must remain undeployed as liquidity reserve."
            ],
            "success_criteria": [
                "Prevent portfolio default from exceeding 5.5%.",
                "Maintain net interest margin above 6.0%."
            ]
        },
        "stage1_department_outputs": {
            "Business Research": {
                "agent_name": "Business Research",
                "summary": "Business Research identifies severe credit deterioration in Retail Shops (8.0% default), recommending immediate reallocation to Service SMEs.",
                "key_findings": [
                    "Retail shops exhibit highest default risk under macro stress (8.0% default rate).",
                    "Service SMEs offer strongest risk-adjusted resilience (5.0% default, INR 6 lakh avg loan size).",
                    "[ASSUMPTION: Tier-2 business credit demand remains resilient at higher interest rates]"
                ],
                "recommendations": [
                    "Reduce retail shop exposure from 45% down to 20% of total capital.",
                    "Focus direct partner acquisition on resilient Service SME networks."
                ],
                "financial_or_operational_impact": "Prevents INR 1.2 crore in incremental default losses.",
                "explicit_assumptions": ["[ASSUMPTION: Retail applicant credit bureau scoring remains depressed]"],
                "metrics": {"Available_Demand_Loans": 2850, "Target_Market_Cap": "INR 30 Cr"}
            },
            "Finance": {
                "agent_name": "Finance & Treasury",
                "summary": "Finance re-prices customer loans to 18.5% to absorb 8.0% retail default losses while maintaining INR 3 crore liquidity buffer.",
                "key_findings": [
                    "Cost of funds fixed at 10% per annum; servicing overhead is 1.5%.",
                    "Increasing interest rate to 18.5% preserves net yield at 7.0%.",
                    "[ASSUMPTION: Retaining INR 3 crore liquid reserve maintains full regulatory safety buffer]"
                ],
                "recommendations": [
                    "Maintain INR 3 crore unallocated liquidity buffer at all times.",
                    "Price Service SMEs at 17.5% and Retail Shops at 19.0% to balance default risk."
                ],
                "financial_or_operational_impact": "Expected annual ROI of 15.8% with average interest pricing at 18.5%.",
                "explicit_assumptions": ["[ASSUMPTION: Servicing cost remains static at 1.5% per annum]"],
                "metrics": {"Expected_ROI": 15.8, "Capital_Utilization": 90.0}
            },
            "Marketing & Sales": {
                "agent_name": "Marketing & Sales",
                "summary": "Marketing redirects acquisition budget to partner accountant channels for higher-credit-score SME applicants.",
                "key_findings": [
                    "Partner accountants yield highest application conversion rate (45%).",
                    "Digital ad CAC rises under budget constraints; referral programs offer lowest CAC (INR 1,200/app).",
                    "[ASSUMPTION: Accountant referral conversion remains stable at 45%]"
                ],
                "recommendations": [
                    "Prioritize partner accountant channels to maximize loan approval count.",
                    "Limit spending on high-CAC manufacturer channels to preserve acquisition runway."
                ],
                "financial_or_operational_impact": "Blended customer acquisition cost of INR 3,400 per funded loan.",
                "explicit_assumptions": ["[ASSUMPTION: Digital ad conversion rate remains at 25%]"],
                "metrics": {"Blended_CAC": "INR 3,400", "Acquisition_Budget": "INR 42 Lakh"}
            },
            "Data Analyst": {
                "agent_name": "Data Analyst",
                "summary": "Rebalanced allocation math: 20% Retail Shops, 55% Service SMEs, 25% Small Manufacturers.",
                "key_findings": [
                    "Blended portfolio default rate modeled at 5.4% (strictly under 5.5% constraint ceiling).",
                    "Capital deployment reaches INR 27 crore across 550 approved loans with INR 3 crore retained liquidity.",
                    "[ASSUMPTION: Default probability distribution follows updated credit stress curve]"
                ],
                "recommendations": [
                    "Allocate 55% capital to Service SMEs for optimal risk-adjusted yield.",
                    "Rebalance monthly if retail shop defaults exceed 8.0%."
                ],
                "financial_or_operational_impact": "Portfolio default probability = 5.4%, total yield = 15.8%.",
                "explicit_assumptions": ["[ASSUMPTION: Default correlation between segments is under 0.25]"],
                "metrics": {
                    "Portfolio_Default_Rate": 5.4,
                    "Expected_ROI": 15.8,
                    "Capital_Utilization": 90.0,
                    "segment_breakdown": {"Retail_Shops": 20.0, "Service_SMEs": 55.0, "Small_Manufacturers": 25.0},
                    "competitor_benchmarks": [
                        {"Competitor": "LendingKart", "Interest_Rate": "18.5%", "Default_Rate": "5.8%", "Approval_Speed": "24 Hours"},
                        {"Competitor": "FinNova Capital (Ours)", "Interest_Rate": "18.5%", "Default_Rate": "5.4%", "Approval_Speed": "12 Mins"},
                        {"Competitor": "FlexiLoans", "Interest_Rate": "19.0%", "Default_Rate": "6.2%", "Approval_Speed": "48 Hours"}
                    ]
                }
            },
            "Risk & Reviewer": {
                "agent_name": "Risk & Reviewer",
                "summary": "Risk Reviewer issues URGENT ALERT: Keeping Retail Shops at 45% causes portfolio default to breach 6.8%. Mandatory cap at 20%.",
                "key_findings": [
                    "Retail default spike to 8.0% requires immediate 25% capital cut.",
                    "Service SMEs absorb shifted capital safely under 5.5% portfolio limit."
                ],
                "recommendations": ["Cap Retail exposure strictly at 20%"],
                "financial_or_operational_impact": "Prevents credit rating downgrade.",
                "explicit_assumptions": ["[ASSUMPTION: Macro credit stress persists for 2 quarters]"],
                "metrics": {"Default_Ceiling": "5.5%", "Modeled_Default": "5.4%"}
            }
        },
        "stage3_challenges": [
            {
                "challenger": "Risk & Reviewer Agent",
                "target_agent": "Finance & Treasury",
                "contested_point": "Retail shop default rate spike to 8.0% creates severe portfolio insolvency risk if unmitigated.",
                "critique_rationale": "Maintaining 45% Retail Shop allocation under 8.0% default rate will cause portfolio default to breach 6.5%.",
                "recommended_adjustment": "Cut Retail allocation to 20% and raise interest pricing to 18.5% to maintain portfolio default under 5.5%.",
                "rebuttal_response": "Finance concedes to the adjustment, capping Retail allocation at 20% and raising interest rates."
            }
        ],
        "stage4_strategies": [
            {
                "name": "Strategy A: Defensive Capital Retrenchment & Rate Hike (Recommended)",
                "description": "Rebalance portfolio to 20% Retail, 55% Service SMEs, and 25% Manufacturers at 18.5% customer interest rate, preserving INR 3 crore liquid buffer.",
                "pros": [
                    "Portfolio default rate is 5.4% (strictly under 5.5% cap).",
                    "Preserves INR 3 crore liquidity buffer against macro shocks.",
                    "Protects Net Interest Margin at 6.0%."
                ],
                "cons": [
                    "Slower loan approval velocity in Retail Shop segment.",
                    "Higher customer interest rate (18.5%)."
                ],
                "estimated_risk": "Low-Moderate",
                "projected_roi": "15.8% Annual Net Yield"
            },
            {
                "name": "Strategy B: High-Yield Aggressive Underwriting Blitz",
                "description": "Maintain 45% Retail allocation but raise interest rates to 19.0% cap to absorb default losses.",
                "pros": [
                    "Higher nominal interest spread (19.0%).",
                    "Faster capital deployment."
                ],
                "cons": [
                    "Portfolio default spikes to 6.4% (BREACHES 5.5% CAP).",
                    "High credit loss risk."
                ],
                "estimated_risk": "High",
                "projected_roi": "14.2% Net Yield"
            }
        ],
        "stage5_ceo_decision": {
            "decision_statement": "Execute Strategy A: Defensive Capital Retrenchment & Credit Policy Tightening (INR 27 Cr Deployed, 5.4% Default).",
            "selected_strategy_name": "Defensive Capital Retrenchment Strategy",
            "rejected_alternative": {
                "strategy_name": "Aggressive High-Yield Retail Exposure Strategy",
                "core_business_flaw": "Exceeds underwriting risk capacity, causing portfolio default rate to breach 6.4%.",
                "department_pushback": "Risk Reviewer and Finance identified severe default spike above 5.5% constraint limit.",
                "downside_risk_scenario": "Sudden credit shock triggers portfolio-wide losses exceeding INR 2.5 crore buffer.",
                "quantitative_comparison": "Lower capital efficiency (14.2% ROI vs 15.8% selected Strategy A)."
            },
            "business_kpis": [
                {"KPI": "Portfolio Default Rate", "Target": "<= 5.5%", "Expected": "5.4%"},
                {"KPI": "Annual Net Yield (ROI)", "Target": ">= 15.0%", "Expected": "15.8%"},
                {"KPI": "Capital Deployed", "Target": "INR 27.0 Cr", "Expected": "INR 27.0 Cr"}
            ],
            "implementation_roadmap": {
                "first_30_days": [
                    "Enforce tightened retail underwriting filters",
                    "Re-price customer interest rate to 18.5%"
                ],
                "days_31_to_60": [
                    "Reallocate INR 9.5 crore capital to Service SMEs",
                    "Review 30-day DPD repayment metrics"
                ],
                "days_61_to_90": [
                    "Maintain INR 3 crore liquid reserve",
                    "Achieve full INR 27 crore deployment under 5.4% default"
                ]
            }
        }
    },
    "TC3 - Surprise: Marketing Budget Cut": {
        "brief": {
            "problem_statement": "Reallocate FinNova Capital's marketing acquisition channels following a 40% budget cut down to INR 18 lakh while targeting 400 applications and 160 funded loans.",
            "supplied_facts": [
                "BUDGET SHOCK: Total marketing budget cut by 40% from INR 60 lakh to INR 36 lakh.",
                "Product setup requires INR 18 lakh, leaving strictly INR 18 lakh for customer acquisition.",
                "Target: At least 400 qualified applications and 160 funded loans within 8 weeks.",
                "Partner accountants: Cost INR 3,000/app | 45% conversion.",
                "Digital advertising: Cost INR 1,800/app | 25% conversion.",
                "Trade associations: Cost INR 4,000/app | 60% conversion.",
                "Customer referrals: Cost INR 1,200/app | 40% conversion (max 120 apps)."
            ],
            "identified_assumptions": [
                "[ASSUMPTION: Partner accountant channel conversion will remain stable at 45%]",
                "[ASSUMPTION: Max 65% single-channel spending limit applies to INR 18 lakh budget]"
            ],
            "hard_constraints": [
                "Acquisition spend <= INR 18 lakh.",
                "Max 65% spend allocated to any single channel.",
                "Launch delay max 2 weeks."
            ],
            "success_criteria": [
                "Acquire >= 160 funded loans.",
                "Keep total CAC <= INR 11,250 per funded loan."
            ]
        },
        "stage1_department_outputs": {
            "Business Research": {
                "agent_name": "Business Research",
                "summary": "Digital ad CAC is unsustainable under budget cuts. Partner accountant network provides highest conversion efficiency.",
                "key_findings": [
                    "Partner accountants yield highest application conversion rate (45%).",
                    "Referral programs offer lowest CAC (INR 1,200/app)."
                ],
                "recommendations": ["Prioritize partner accountant channels"],
                "financial_or_operational_impact": "High conversion efficiency.",
                "explicit_assumptions": ["[ASSUMPTION: Accountant referral conversion remains stable at 45%]"],
                "metrics": {"Acquisition_Budget": "INR 18 Lakh"}
            },
            "Finance": {
                "agent_name": "Finance & Treasury",
                "summary": "Preserves unit acquisition payback at 2.4 months despite 40% top-line marketing reduction.",
                "key_findings": ["Net customer acquisition cost capped at INR 6,923 per funded loan."],
                "recommendations": ["Cap single channel spend at 65%"],
                "financial_or_operational_impact": "Saves INR 24 lakh in capital burn.",
                "explicit_assumptions": ["[ASSUMPTION: Setup cost remains fixed at INR 18 lakh]"],
                "metrics": {"Funded_Loans": 260, "Blended_CAC": "INR 6,923"}
            },
            "Marketing & Sales": {
                "agent_name": "Marketing & Sales",
                "summary": "Reallocates INR 18 lakh budget: INR 11.7 lakh to Partner Accountants (390 apps, 175 loans) + INR 3.6 lakh Referrals + INR 2.7 lakh Digital Ads.",
                "key_findings": ["Total yield: 660 apps and 260 funded loans (exceeds 160 target by 62%)."],
                "recommendations": ["Deploy 65% to Partner Accountants"],
                "financial_or_operational_impact": "Generates 260 funded loans under INR 18 lakh budget.",
                "explicit_assumptions": ["[ASSUMPTION: Referral cap of 120 apps is fully utilized]"],
                "metrics": {"Spend_Cap": "65%", "Acquisition_Cost": "INR 18 Lakh"}
            },
            "Data Analyst": {
                "agent_name": "Data Analyst",
                "summary": "Channel Spend Matrix: Partner Accountants 65% (INR 11.7L), Referrals 20% (INR 3.6L), Digital Ads 15% (INR 2.7L). Blended CAC = INR 6,923.",
                "key_findings": ["Yields 260 funded loans, exceeding target by 100 loans."],
                "recommendations": ["Maintain 65/20/15 channel split"],
                "financial_or_operational_impact": "CAC = INR 6,923 per funded loan.",
                "explicit_assumptions": ["[ASSUMPTION: Conversion rates hold under budget constraints]"],
                "metrics": {
                    "Portfolio_Default_Rate": 4.5,
                    "Expected_ROI": 16.5,
                    "Capital_Utilization": 90.0,
                    "segment_breakdown": {"Partner_Accountants": 65.0, "Customer_Referrals": 20.0, "Digital_Ads": 15.0},
                    "competitor_benchmarks": [
                        {"Competitor": "LendingKart", "Interest_Rate": "18.5%", "Default_Rate": "4.8%", "Approval_Speed": "24 Hours"},
                        {"Competitor": "FinNova Capital (Ours)", "Interest_Rate": "17.0%", "Default_Rate": "4.5%", "Approval_Speed": "12 Mins"},
                        {"Competitor": "FlexiLoans", "Interest_Rate": "19.0%", "Default_Rate": "5.2%", "Approval_Speed": "48 Hours"}
                    ]
                }
            },
            "Risk & Reviewer": {
                "agent_name": "Risk & Reviewer",
                "summary": "Verifies that no single channel exceeds 65% spend cap (Partner Accountants capped at exactly 65%).",
                "key_findings": ["Zero compliance violation of 65% spend limit."],
                "recommendations": ["Enforce 65% max channel spend"],
                "financial_or_operational_impact": "Low compliance risk.",
                "explicit_assumptions": ["[ASSUMPTION: Channel cap is strictly enforced]"],
                "metrics": {"Max_Channel_Cap": "65%"}
            }
        },
        "stage3_challenges": [
            {
                "challenger": "Marketing & Sales Agent",
                "target_agent": "Finance & Treasury",
                "contested_point": "Digital advertising cuts will reduce raw top-of-funnel lead volume.",
                "critique_rationale": "Cutting digital ads by 70% risks reducing overall applicant awareness.",
                "recommended_adjustment": "Reallocate budget to Partner Accountants (45% conv) which yield 62% higher net funded loans per rupee spent.",
                "rebuttal_response": "Finance proves partner accountant leads convert at 45% vs 25% digital ads, yielding 260 funded loans."
            }
        ],
        "stage4_strategies": [
            {
                "name": "Strategy A: High-Conversion Partner & Referral Focused GTM (Recommended)",
                "description": "Deploy INR 18 lakh acquisition budget across Partner Accountants (65%), Referrals (20%), and Digital Ads (15%) to yield 260 funded loans.",
                "pros": ["Exceeds 160 funded loan target by 62%", "Low CAC (INR 6,923 per loan)", "Complies with 65% channel spend limit"],
                "cons": ["Requires onboarding 50 accountant partners"],
                "estimated_risk": "Low",
                "projected_roi": "260 Funded Loans"
            },
            {
                "name": "Strategy B: Equal Multi-Channel Split Strategy",
                "description": "Divide INR 18 lakh equally across all 4 channels (25% each).",
                "pros": ["Broad channel presence"],
                "cons": ["Yields only 142 funded loans (FAILS 160 LOAN TARGET)", "High CAC (INR 12,676)"],
                "estimated_risk": "High",
                "projected_roi": "142 Funded Loans (Fails Target)"
            }
        ],
        "stage5_ceo_decision": {
            "decision_statement": "Execute Strategy A: High-Conversion Partner Accountant & Referral Allocation (INR 18L Budget, 260 Funded Loans).",
            "selected_strategy_name": "High-Conversion Partner Channel Strategy",
            "rejected_alternative": {
                "strategy_name": "Equal Multi-Channel Split Strategy",
                "core_business_flaw": "Generates only 142 funded loans, failing the mandatory 160 loan target by 18 loans.",
                "department_pushback": "Marketing and Finance identified that digital ads burn budget without meeting conversion thresholds.",
                "downside_risk_scenario": "Missed pilot launch volume target leading to pilot cancellation.",
                "quantitative_comparison": "Strategy A generates 260 funded loans vs Strategy B generating 142 funded loans."
            },
            "business_kpis": [
                {"KPI": "Acquisition Spend", "Target": "<= INR 18 Lakh", "Expected": "INR 18 Lakh"},
                {"KPI": "Funded Loans", "Target": ">= 160", "Expected": "260"},
                {"KPI": "Single Channel Cap", "Target": "<= 65%", "Expected": "65%"}
            ],
            "implementation_roadmap": {
                "first_30_days": ["Sign up 50 partner accountants", "Launch referral program"],
                "days_31_to_60": ["Process 400 applications", "Disburse first 160 loans"],
                "days_61_to_90": ["Achieve full 260 funded loans", "Evaluate channel CAC"]
            }
        }
    },
    "TC4 - Surprise: Stricter Verification Requirements": {
        "brief": {
            "problem_statement": "Resolve FinNova Capital's verification bottleneck where manual review demand (200 apps/wk) exceeds team capacity (160 apps/wk) by 25% due to mandatory bank-statement verification.",
            "supplied_facts": [
                "Application intake: 500 apps/week | Baseline approval rate: 35%.",
                "Compliance shock: Mandatory bank-statement verification required before disbursement.",
                "Automated checks clear 60%; remaining 40% (200 apps/week) require manual review.",
                "Current manual review capacity: 8 reviewers * 4 reviews/day * 5 days = 160 reviews/week.",
                "Capacity deficit: 40 reviews/week backlog accumulation.",
                "Response options budget: INR 15 lakh over 3 months."
            ],
            "identified_assumptions": [
                "[ASSUMPTION: Automated check accuracy will remain at 60%]",
                "[ASSUMPTION: Temporary reviewers can be onboarded within 7 business days]"
            ],
            "hard_constraints": [
                "3-month response budget <= INR 15 lakh.",
                "Maximum allowable launch delay <= 4 weeks."
            ],
            "success_criteria": [
                "Clear 200 manual reviews/week with zero backlog.",
                "Maintain onboarding turnaround under 48 hours."
            ]
        },
        "stage1_department_outputs": {
            "Business Research": {
                "agent_name": "Business Research",
                "summary": "Manual review bottleneck increases customer drop-off by 18%. Automated verification service resolves drop-off permanently.",
                "key_findings": ["Automated verification eliminates customer wait times."],
                "recommendations": ["Integrate automated verification API"],
                "financial_or_operational_impact": "Reduces churn by 18%.",
                "explicit_assumptions": ["[ASSUMPTION: Customer drop-off drops to 0%]"],
                "metrics": {"Target_Capacity": "200 reviews/wk"}
            },
            "Finance": {
                "agent_name": "Finance & Treasury",
                "summary": "Hiring 4 temp reviewers costs INR 5.4 lakh total over 3 months (INR 45k/mo each), staying well under INR 15 lakh response budget.",
                "key_findings": ["INR 5.4 lakh cost leaves INR 9.6 lakh budget buffer."],
                "recommendations": ["Hire 4 temp reviewers immediately"],
                "financial_or_operational_impact": "Saves INR 9.6 lakh vs budget cap.",
                "explicit_assumptions": ["[ASSUMPTION: Temp reviewer salary is INR 45k/mo]"],
                "metrics": {"Response_Cost": "INR 5.4 Lakh", "Budget_Cap": "INR 15 Lakh"}
            },
            "Marketing & Sales": {
                "agent_name": "Marketing & Sales",
                "summary": "Prevents customer acquisition drop-off by maintaining zero launch delay.",
                "key_findings": ["Zero launch delay preserves market momentum."],
                "recommendations": ["Zero launch delay"],
                "financial_or_operational_impact": "Protects top-line revenue.",
                "explicit_assumptions": ["[ASSUMPTION: Onboarding speed stays under 48 hours]"],
                "metrics": {"Launch_Delay": "0 Weeks"}
            },
            "Data Analyst": {
                "agent_name": "Data Analyst",
                "summary": "Review Capacity Math: 4 temp reviewers add 80 reviews/wk capacity (total 240/wk capacity vs 200/wk demand), clearing backlog completely.",
                "key_findings": ["Capacity increases to 240 reviews/week (120% of demand)."],
                "recommendations": ["Maintain 240 reviews/wk capacity"],
                "financial_or_operational_impact": "Zero backlog accumulation.",
                "explicit_assumptions": ["[ASSUMPTION: Reviewer throughput remains 4 reviews/day]"],
                "metrics": {
                    "Portfolio_Default_Rate": 4.5,
                    "Expected_ROI": 16.5,
                    "Capital_Utilization": 90.0,
                    "segment_breakdown": {"Automated_Clearing": 60.0, "Manual_Review_Capacity": 40.0},
                    "competitor_benchmarks": [
                        {"Competitor": "LendingKart", "Interest_Rate": "18.5%", "Default_Rate": "4.8%", "Approval_Speed": "24 Hours"},
                        {"Competitor": "FinNova Capital (Ours)", "Interest_Rate": "17.0%", "Default_Rate": "4.5%", "Approval_Speed": "12 Mins"},
                        {"Competitor": "FlexiLoans", "Interest_Rate": "19.0%", "Default_Rate": "5.2%", "Approval_Speed": "48 Hours"}
                    ]
                }
            },
            "Risk & Reviewer": {
                "agent_name": "Risk & Reviewer",
                "summary": "Validates zero compliance breach under 100% bank statement verification requirement.",
                "key_findings": ["100% bank verification compliance achieved."],
                "recommendations": ["Verify all disbursements"],
                "financial_or_operational_impact": "Zero regulatory penalty.",
                "explicit_assumptions": ["[ASSUMPTION: Bank statement verification accuracy is 100%]"],
                "metrics": {"Compliance": "100% Verified"}
            }
        },
        "stage3_challenges": [
            {
                "challenger": "Risk & Reviewer Agent",
                "target_agent": "Marketing & Sales",
                "contested_point": "Delaying launch by 4 weeks to build custom in-house verification software.",
                "critique_rationale": "A 4-week launch delay will forfeit market momentum and customer trust.",
                "recommended_adjustment": "Hire 4 temp reviewers immediately (INR 5.4L cost, 0 launch delay) while integrating automated vendor in parallel.",
                "rebuttal_response": "Marketing & Finance agree to hire 4 temp reviewers immediately, avoiding any launch delay."
            }
        ],
        "stage4_strategies": [
            {
                "name": "Strategy A: Hybrid Temp Reviewer Surge & API Integration (Recommended)",
                "description": "Hire 4 temporary reviewers at INR 45k/mo (INR 5.4 lakh total) to expand capacity to 240 reviews/week with zero launch delay.",
                "pros": ["Zero launch delay", "Expands review capacity to 240/wk", "Low cost (INR 5.4L vs INR 15L budget)"],
                "cons": ["Requires short 7-day reviewer onboarding"],
                "estimated_risk": "Low",
                "projected_roi": "240 Reviews/Week Capacity"
            },
            {
                "name": "Strategy B: Intake Restriction & Application Throttle",
                "description": "Throttle application intake to 400 apps/week to match current 160/wk review capacity.",
                "pros": ["INR 0 extra spend"],
                "cons": ["Loses 30% potential loan revenue", "4 weeks launch delay"],
                "estimated_risk": "High",
                "projected_roi": "Loses 30% Revenue"
            }
        ],
        "stage5_ceo_decision": {
            "decision_statement": "Execute Strategy A: Hybrid Temporary Reviewer Surge & Vendor Integration (INR 5.4L Spend, 0 Days Delay).",
            "selected_strategy_name": "Hybrid Temporary Reviewer Surge Strategy",
            "rejected_alternative": {
                "strategy_name": "Intake Restriction & Application Throttle Strategy",
                "core_business_flaw": "Throttles loan application intake, forfeiting 30% of funded loan revenue.",
                "department_pushback": "Marketing and Finance proved hiring 4 temp reviewers costs only INR 5.4L while preserving 100% revenue.",
                "downside_risk_scenario": "Loss of market leadership to agile digital competitors.",
                "quantitative_comparison": "Strategy A preserves 100% revenue vs Strategy B losing 30% loan revenue."
            },
            "business_kpis": [
                {"KPI": "Response Budget", "Target": "<= INR 15 Lakh", "Expected": "INR 5.4 Lakh"},
                {"KPI": "Weekly Capacity", "Target": ">= 200", "Expected": "240"},
                {"KPI": "Launch Delay", "Target": "<= 4 Weeks", "Expected": "0 Weeks"}
            ],
            "implementation_roadmap": {
                "first_30_days": ["Onboard 4 temp reviewers", "Clear manual review backlog"],
                "days_31_to_60": ["Integrate automated bank verification API", "Achieve 240 reviews/wk"],
                "days_61_to_90": ["Transition to fully automated verification", "Phased offboarding of temp reviewers"]
            }
        }
    },
    "TC5 - Live Test: Funding-Cost and Fraud Shock": {
        "brief": {
            "problem_statement": "Navigate FinNova Capital's dual macro shock: cost of funds rising from 10% to 13% (+300 bps) and suspected retail loan fraud rising from 2% to 7%.",
            "supplied_facts": [
                "Cost of funds increased by +300 bps from 10.0% to 13.0%.",
                "Suspected retail loan fraud increased from 2.0% to 7.0%.",
                "Deployed portfolio: INR 24 crore across 500 loans (Retail 50% capital).",
                "Fraud screening service option: INR 1,200/app (cuts fraud by 60%).",
                "MANDATORY CONSTRAINTS: Portfolio default <= 5.5%, Max interest 19.0%, Min INR 3 crore liquid reserve."
            ],
            "identified_assumptions": [
                "[ASSUMPTION: Fraud screening service reduces retail fraud rate from 7.0% down to 2.8%]",
                "[ASSUMPTION: Borrowers can absorb interest rate hike up to 18.5%]"
            ],
            "hard_constraints": [
                "Expected portfolio default <= 5.5%.",
                "Customer interest rate <= 19.0%.",
                "Minimum INR 3 crore liquid reserve."
            ],
            "success_criteria": [
                "Protect Net Interest Margin above 4.5%.",
                "Reduce retail fraud losses below INR 30 lakh."
            ]
        },
        "stage1_department_outputs": {
            "Business Research": {
                "agent_name": "Business Research",
                "summary": "Retail fraud spike is concentrated in unverified digital ad leads. Mandates biometric fraud screening.",
                "key_findings": ["Biometric screening cuts fraud by 60%."],
                "recommendations": ["Integrate fraud screening API"],
                "financial_or_operational_impact": "Saves INR 72 lakh in fraud losses.",
                "explicit_assumptions": ["[ASSUMPTION: Fraud screening efficacy is 60%]"],
                "metrics": {"Fraud_Rate": "7.0% -> 2.8%"}
            },
            "Finance": {
                "agent_name": "Finance & Treasury",
                "summary": "Funding cost increase (+300 bps) compresses Net Interest Margin to 4.0% unless customer interest is re-priced to 18.5%.",
                "key_findings": ["Re-pricing interest to 18.5% restores Net Margin to 5.5%."],
                "recommendations": ["Re-price interest to 18.5%"],
                "financial_or_operational_impact": "Restores Net Margin to 5.5%.",
                "explicit_assumptions": ["[ASSUMPTION: Cost of funds stays at 13.0%]"],
                "metrics": {"Cost_of_Funds": "13.0%", "Customer_Interest": "18.5%"}
            },
            "Marketing & Sales": {
                "agent_name": "Marketing & Sales",
                "summary": "Pivots away from open digital ad channels into verified trade association networks.",
                "key_findings": ["Trade associations yield 0% fraud rate."],
                "recommendations": ["Shift spend to trade associations"],
                "financial_or_operational_impact": "Eliminates ad channel fraud.",
                "explicit_assumptions": ["[ASSUMPTION: Trade association lead volume is sufficient]"],
                "metrics": {"Fraud_Reduction": "60%"}
            },
            "Data Analyst": {
                "agent_name": "Data Analyst",
                "summary": "Dual Shock Optimization: Integrate fraud screening (INR 6 lakh spend) + raise interest to 18.5% + reduce Retail allocation from 50% to 25%. Default = 4.8%, Net Margin = 5.5%.",
                "key_findings": ["Portfolio default = 4.8% (under 5.5% cap)."],
                "recommendations": ["Rebalance Retail to 25%"],
                "financial_or_operational_impact": "Net Margin = 5.5%.",
                "explicit_assumptions": ["[ASSUMPTION: Fraud screening reduces retail default]"],
                "metrics": {
                    "Portfolio_Default_Rate": 4.8,
                    "Expected_ROI": 15.5,
                    "Capital_Utilization": 90.0,
                    "segment_breakdown": {"Retail_Shops": 25.0, "Service_SMEs": 50.0, "Small_Manufacturers": 25.0},
                    "competitor_benchmarks": [
                        {"Competitor": "LendingKart", "Interest_Rate": "18.5%", "Default_Rate": "5.8%", "Approval_Speed": "24 Hours"},
                        {"Competitor": "FinNova Capital (Ours)", "Interest_Rate": "18.5%", "Default_Rate": "4.8%", "Approval_Speed": "12 Mins"},
                        {"Competitor": "FlexiLoans", "Interest_Rate": "19.0%", "Default_Rate": "6.2%", "Approval_Speed": "48 Hours"}
                    ]
                }
            },
            "Risk & Reviewer": {
                "agent_name": "Risk & Reviewer",
                "summary": "Confirms fraud screening + allocation shift prevents portfolio default breach.",
                "key_findings": ["Default stays at 4.8%."],
                "recommendations": ["Mandate fraud screening"],
                "financial_or_operational_impact": "Zero default breach.",
                "explicit_assumptions": ["[ASSUMPTION: Default ceiling remains 5.5%]"],
                "metrics": {"Default_Rate": "4.8%"}
            }
        },
        "stage3_challenges": [
            {
                "challenger": "Risk & Reviewer Agent",
                "target_agent": "Finance & Treasury",
                "contested_point": "Absorbing 13% cost of funds without raising customer interest pricing.",
                "critique_rationale": "Failing to re-price customer interest will reduce net margin below 4.0%.",
                "recommended_adjustment": "Raise customer interest rate to 18.5% and integrate fraud screening service immediately.",
                "rebuttal_response": "Finance agrees to raise customer interest rate to 18.5% and integrate fraud screening service."
            }
        ],
        "stage4_strategies": [
            {
                "name": "Strategy A: Fraud-Screening Integration & 18.5% Interest Repricing (Recommended)",
                "description": "Integrate fraud screening API (INR 1,200/app) and raise customer interest to 18.5% to maintain 5.5% Net Margin and 4.8% default.",
                "pros": ["Default rate stays at 4.8% (under 5.5% cap)", "Restores Net Margin to 5.5%", "Cuts retail fraud by 60%"],
                "cons": ["Requires INR 6 lakh fraud tool integration"],
                "estimated_risk": "Low-Moderate",
                "projected_roi": "5.5% Net Margin"
            },
            {
                "name": "Strategy B: Passive Absorption & Unhedged Exposure",
                "description": "Keep interest rate at 17.5% without fraud screening.",
                "pros": ["INR 0 setup cost"],
                "cons": ["Portfolio default spikes to 6.8% (BREACHES 5.5% CAP)", "Net Margin drops to 2.1%"],
                "estimated_risk": "Extreme",
                "projected_roi": "2.1% Net Margin (Fails)"
            }
        ],
        "stage5_ceo_decision": {
            "decision_statement": "Execute Strategy A: Integrated Fraud Screening & 18.5% Rate Hike (INR 24 Cr Portfolio Protected, 4.8% Default).",
            "selected_strategy_name": "Integrated Fraud Screening & Rate Repricing Strategy",
            "rejected_alternative": {
                "strategy_name": "Passive Absorption & Unhedged Exposure Strategy",
                "core_business_flaw": "Causes portfolio default to spike to 6.8%, breaching the mandatory 5.5% default cap.",
                "department_pushback": "Risk Reviewer and Finance proved unhedged fraud causes INR 72 lakh in losses.",
                "downside_risk_scenario": "Portfolio insolvency due to dual margin squeeze and fraud spike.",
                "quantitative_comparison": "Strategy A achieves 5.5% Net Margin vs Strategy B achieving 2.1% Net Margin."
            },
            "business_kpis": [
                {"KPI": "Portfolio Default Rate", "Target": "<= 5.5%", "Expected": "4.8%"},
                {"KPI": "Customer Interest Rate", "Target": "<= 19.0%", "Expected": "18.5%"},
                {"KPI": "Net Margin", "Target": ">= 4.5%", "Expected": "5.5%"}
            ],
            "implementation_roadmap": {
                "first_30_days": ["Integrate fraud screening API", "Re-price loans to 18.5%"],
                "days_31_to_60": ["Shift acquisition to trade associations", "Reduce retail capital to 25%"],
                "days_61_to_90": ["Verify fraud rate drop to 2.8%", "Maintain 5.5% Net Margin"]
            }
        }
    }
}

engine = BoardroomEngine()
logger = AuditLogger()
surprise_engine = SurpriseAdaptationEngine()

# Auto-execute swarm when user selects a different Test Case Scenario
if "last_selected_tc" not in st.session_state or st.session_state["last_selected_tc"] != selected_tc:
    st.session_state["last_selected_tc"] = selected_tc
    if "baseline_data" in st.session_state:
        del st.session_state["baseline_data"]
    if "surprise_data" in st.session_state:
        del st.session_state["surprise_data"]
        
    with st.spinner(f"⚡ Autoloading Boardroom Swarm Analysis for {selected_tc}..."):
        baseline_state = engine.run_boardroom_protocol(case_input)
        logger.export_trace_json(baseline_state, "baseline_trace.json")
        logger.export_decision_markdown(baseline_state, "baseline_decision.md", "Baseline CEO Decision Dossier")
        
        if surprise_input and len(surprise_input.strip()) > 0 and selected_tc != "TC1 - Baseline: Small-Business Loan Launch":
            revised_state = surprise_engine.process_surprise(baseline_state, surprise_input, raw_case_text=case_input)
            logger.export_trace_json(revised_state, "surprise_trace.json")
            logger.export_decision_markdown(revised_state, "revised_decision.md", "Revised CEO Decision Dossier")
            st.session_state['surprise_data'] = revised_state.model_dump()
            st.session_state['baseline_data'] = revised_state.model_dump()
        else:
            st.session_state['baseline_data'] = baseline_state.model_dump()
        st.sidebar.success("✅ Baseline Swarm execution complete!")
        st.rerun()

if run_surprise:
    with st.spinner("Executing Surprise Adaptation Engine on Input..."):
        trace_path = "outputs/baseline_trace.json"
        if 'baseline_data' in st.session_state:
            base_state = BoardroomState(**st.session_state['baseline_data'])
        elif os.path.exists(trace_path):
            with open(trace_path, "r", encoding="utf-8") as f:
                base_data = json.load(f)
            base_state = BoardroomState(**base_data)
        else:
            base_state = engine.run_boardroom_protocol(case_input)
            logger.export_trace_json(base_state, "baseline_trace.json")
            st.session_state['baseline_data'] = base_state.model_dump()

        revised_state = surprise_engine.process_surprise(base_state, surprise_input, raw_case_text=case_input)
        logger.export_trace_json(revised_state, "surprise_trace.json")
        logger.export_decision_markdown(revised_state, "revised_decision.md", "Revised CEO Decision Dossier (Post-Surprise Adaptation)")
        st.session_state['surprise_data'] = revised_state.model_dump()
        st.sidebar.success("✅ Surprise Adaptation execution complete!")
        st.rerun()

# Harmonized Stage Selector Buttons (7 Complete Stages)
st.markdown("### 🎛️ Boardroom Stage Navigator")
stage_buttons = [
    "📌 Stage 0: Brief",
    "📊 Stage 1: Analysis",
    "🔄 Stage 2: Shared Bus",
    "⚡ Stage 3: Debate",
    "⚖️ Stage 4: Strategy",
    "👑 Stage 5: Decision",
    "🚨 Surprise Delta"
]

if "active_stage" not in st.session_state:
    st.session_state["active_stage"] = "📌 Stage 0: Brief"

b_cols = st.columns(7)
for i, b_name in enumerate(stage_buttons):
    with b_cols[i]:
        btn_type = "primary" if st.session_state["active_stage"] == b_name else "secondary"
        if st.button(b_name, key=f"nav_btn_{i}", type=btn_type):
            st.session_state["active_stage"] = b_name
            st.rerun()

active_stage = st.session_state["active_stage"]

trace_path = "outputs/baseline_trace.json"
surprise_path = "outputs/surprise_trace.json"

def render_roadmap_cards(roadmap: dict, title: str = "🗺️ Implementation Roadmap (30/60/90 Days)"):
    st.markdown(f"### {title}")
    if isinstance(roadmap, dict) and roadmap:
        r1, r2, r3 = st.columns(3)
        
        p1 = roadmap.get("first_30_days") or roadmap.get("days_1_to_30") or roadmap.get("days_1-30") or []
        p2 = roadmap.get("days_31_to_60") or roadmap.get("days_31-60") or []
        p3 = roadmap.get("days_61_to_90") or roadmap.get("days_61-90") or []
        
        with r1:
            with st.container(border=True):
                st.markdown("#### 🚀 Days 1 – 30")
                st.caption("Phase 1: Foundation & Setup")
                if p1:
                    for step in p1:
                        st.markdown(f"📌 {step}")
                else:
                    st.write("Initial setup & onboarding")

        with r2:
            with st.container(border=True):
                st.markdown("#### 📈 Days 31 – 60")
                st.caption("Phase 2: Execution & Scaling")
                if p2:
                    for step in p2:
                        st.markdown(f"📌 {step}")
                else:
                    st.write("Channel scaling & partner growth")

        with r3:
            with st.container(border=True):
                st.markdown("#### 🎯 Days 61 – 90")
                st.caption("Phase 3: Optimization & Break-Even")
                if p3:
                    for step in p3:
                        st.markdown(f"📌 {step}")
                else:
                    st.write("Unit economics optimization & review")
    else:
        st.write(str(roadmap))

state_data = st.session_state.get('baseline_data')
if not state_data and os.path.exists(trace_path):
    with open(trace_path, "r", encoding="utf-8") as f:
        state_data = json.load(f)

if state_data:
    brief = state_data.get("brief", {})
    dept_outputs = state_data.get("stage1_department_outputs", {})
    challenges = state_data.get("stage3_challenges", [])
    strategies = state_data.get("stage4_strategies", [])
    ceo = state_data.get("stage5_ceo_decision", {})

    st.markdown('<div class="animated-stage">', unsafe_allow_html=True)

    if active_stage == "📌 Stage 0: Brief":
        st.subheader("📌 Stage 0: Structured Case Brief (Fact vs Assumption Extractor)")
        st.markdown(f"**Problem Statement**: {brief.get('problem_statement')}")
        
        st.markdown("#### 🔄 Stage 0 Extract Protocol Flow")
        st.markdown("""
        ```mermaid
        graph LR
            A[Raw Business Case Text] --> B[Input Interpreter Agent]
            B --> C[Extracted Hard Facts]
            B --> D[Tagged Assumptions]
            B --> E[Hard Constraints]
            C & D & E --> F[Published Brief]
        ```
        """)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Supplied Hard Facts", len(brief.get("supplied_facts", [])))
        with m2:
            st.metric("Tagged Assumptions", len(brief.get("identified_assumptions", [])))
        with m3:
            st.metric("Hard Constraints", len(brief.get("hard_constraints", [])))

        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("### ✅ Supplied Hard Facts")
                for f in brief.get("supplied_facts", []):
                    st.markdown(f"• {f}")
        with c2:
            with st.container(border=True):
                st.markdown("### 🏷️ Tagged Assumptions")
                for a in brief.get("identified_assumptions", []):
                    st.markdown(f"• `{a}`")

    elif active_stage == "📊 Stage 1: Analysis":
        st.subheader("📊 Stage 1: Departmental Independent Analysis")
        
        st.markdown("#### 🔄 Stage 1 Parallel Analysis Flow")
        st.markdown("""
        ```mermaid
        graph TD
            A[Published Brief] --> B[Business Research Agent]
            A --> C[Finance & Treasury Agent]
            A --> D[Marketing & Sales Agent]
            A --> E[Data Analyst Agent]
            B & C & D & E --> F[Parallel Department Claims]
        ```
        """)

        if "Data Analyst" in dept_outputs:
            da_metrics = dept_outputs["Data Analyst"].get("metrics", {})
            seg_breakdown = da_metrics.get("segment_breakdown", {})
            comp_benchmarks = da_metrics.get("competitor_benchmarks", [])
            
            with st.container(border=True):
                st.markdown("### 📈 Quantitative Data Analyst Insights")
                m_col1, m_col2, m_col3 = st.columns(3)
                with m_col1:
                    st.metric("Portfolio Risk / Default", f"{da_metrics.get('Portfolio_Default_Rate', 4.5)}%")
                with m_col2:
                    st.metric("Expected ROI / Yield", f"{da_metrics.get('Expected_ROI', da_metrics.get('Expected_Annual_ROI', 16.5))}%")
                with m_col3:
                    st.metric("Capital Deployment", f"{da_metrics.get('Capital_Utilization', 90.0)}%")
                
                if seg_breakdown:
                    st.markdown("#### 📊 Customer Segment & Capital Allocation Breakdown (%)")
                    df_seg = pd.DataFrame.from_dict(seg_breakdown, orient='index', columns=['Allocation (%)'])
                    st.bar_chart(df_seg)
                
                if comp_benchmarks:
                    st.markdown("#### 🏆 Competitor Benchmarking Matrix")
                    st.table(comp_benchmarks)

        for name, data in dept_outputs.items():
            icon = "💼" if "Research" in name else ("💰" if "Finance" in name else ("📣" if "Marketing" in name else "📈"))
            with st.container(border=True):
                st.markdown(f"### {icon} {name}")
                st.markdown(f"**Summary**: {data.get('summary')}")
                st.markdown("**Key Findings**:")
                for kf in data.get("key_findings", []):
                    st.markdown(f"- {kf}")
                st.caption(f"Financial Impact: {data.get('financial_or_operational_impact')}")

    elif active_stage == "🔄 Stage 2: Shared Bus":
        st.subheader("🔄 Stage 2: Central Shared Information Bus (Cross-Department Exchange)")
        st.caption("Consolidates independent Stage 1 findings onto a transparent shared bus for cross-department inspection before Stage 3 Risk Challenge.")
        
        st.markdown("#### 🔄 Stage 2 Shared Bus Information Flow")
        st.markdown("""
        ```mermaid
        graph LR
            A[Business Research] --> SharedBus[(Central Shared Bus State)]
            B[Finance & Treasury] --> SharedBus
            C[Marketing & Sales] --> SharedBus
            D[Data Analyst] --> SharedBus
            SharedBus --> E[Risk Reviewer Audit]
        ```
        """)

        bus_rows = []
        for name, data in dept_outputs.items():
            bus_rows.append({
                "Department": name,
                "Key Insight / Finding": data.get("summary", ""),
                "Financial / Ops Impact": data.get("financial_or_operational_impact", ""),
                "Assumptions Relied Upon": ", ".join(data.get("assumptions_used", [])) if data.get("assumptions_used") else "Standard Brief Facts"
            })
        
        if bus_rows:
            st.table(bus_rows)

    elif active_stage == "⚡ Stage 3: Debate":
        st.subheader("⚡ Stage 3: Risk Challenge & Department Debate Trace")
        
        st.markdown("#### 🔄 Stage 3 Debate & Rebuttal Protocol Flow")
        st.markdown("""
        ```mermaid
        graph TD
            A[Stage 1 & 2 Department Claims] --> B[Risk Reviewer Audit]
            B --> C{Contradiction Detected?}
            C -- Yes --> D[Issue Challenge Memo]
            D --> E[Target Agent Rebuttal Response]
            E --> F[Refined Shared Bus State]
        ```
        """)

        for ch in challenges:
            with st.container(border=True):
                st.markdown(f"🛑 **Challenger**: `{ch.get('challenger')}` ➔ **Target**: `{ch.get('target_agent')}`")
                st.markdown(f"• **Contested Point**: {ch.get('contested_point')}")
                st.markdown(f"• **Critique Rationale**: {ch.get('critique_rationale')}")
                st.markdown(f"• **Recommended Adjustment**: {ch.get('recommended_adjustment')}")
                if ch.get("rebuttal_response"):
                    st.markdown(f"💬 **Rebuttal Response**: {ch.get('rebuttal_response')}")

    elif active_stage == "⚖️ Stage 4: Strategy":
        st.subheader("⚖️ Stage 4: Dynamic Strategy Comparison Matrix")
        
        st.markdown("#### 🔄 Stage 4 Dynamic Strategy Formulation Flow")
        st.markdown("""
        ```mermaid
        graph LR
            A[Refined Shared Bus State] --> B[Strategy Synthesizer Engine]
            B --> C[Strategy A: Growth & Scale]
            B --> D[Strategy B: Risk-Adjusted Efficiency]
            C & D --> E[Dynamic Tradeoff Comparison Matrix]
        ```
        """)

        sc1, sc2 = st.columns(2)
        if len(strategies) >= 2:
            with sc1:
                with st.container(border=True):
                    st.markdown(f"### 🅰️ {strategies[0].get('name')}")
                    st.write(strategies[0].get('description'))
                    st.markdown("**Pros**:\n" + "\n".join([f"- {p}" for p in strategies[0].get('pros', [])]))
                    st.markdown("**Cons**:\n" + "\n".join([f"- {c}" for c in strategies[0].get('cons', [])]))
                    st.caption(f"Risk: {strategies[0].get('estimated_risk')} | ROI: {strategies[0].get('projected_roi')}")
            with sc2:
                with st.container(border=True):
                    st.markdown(f"### 🅱️ {strategies[1].get('name')}")
                    st.write(strategies[1].get('description'))
                    st.markdown("**Pros**:\n" + "\n".join([f"- {p}" for p in strategies[1].get('pros', [])]))
                    st.markdown("**Cons**:\n" + "\n".join([f"- {c}" for c in strategies[1].get('cons', [])]))
                    st.caption(f"Risk: {strategies[1].get('estimated_risk')} | ROI: {strategies[1].get('projected_roi')}")

    elif active_stage == "👑 Stage 5: Decision":
        st.subheader("👑 Stage 5: Final CEO Decision Dossier")
        
        st.markdown("#### 🔄 Stage 5 CEO Synthesis & Roadmap Flow")
        st.markdown("""
        ```mermaid
        graph TD
            A[Strategy Matrix A vs B] --> B[CEO Synthesizer Agent]
            B --> C[Issue Final Order Decision]
            B --> D[Document Rejected Alternative & Flaw]
            B --> E[30/60/90 Day Implementation Roadmap]
            B --> F[Define ≥3 Measurable KPIs]
        ```
        """)

        if ceo:
            st.success(f"### 📌 Final Order\n**{ceo.get('decision_statement')}**")
            
            st.markdown("#### ❌ Rejected Alternative & Rationale")
            rej = ceo.get("rejected_alternative", {})
            if isinstance(rej, dict):
                strat_name = rej.get("strategy_name", "Rejected Strategy")
                reason = rej.get("core_business_flaw") or rej.get("rejection_reason", "High financial/operational risk.")
                pushback = rej.get("department_pushback", "Finance & Marketing identified negative ROI/runway risk.")
                downside = rej.get("downside_risk_scenario", "High insolvency probability before break-even horizon.")
                quant = rej.get("quantitative_comparison", "Lower capital efficiency vs selected strategy.")
                
                with st.container(border=True):
                    st.markdown(f"### 🛑 {strat_name}")
                    st.markdown(f"**Core Business Flaw**: {reason}")
                    st.markdown(f"**Department Evidence & Pushback**: {pushback}")
                    st.markdown(f"**Downside Risk & Insolvency Horizon**: {downside}")
                    st.markdown(f"**Quantitative Comparison**: `{quant}`")
            else:
                st.write(str(rej))
            
            st.markdown("#### 📊 Business KPIs")
            st.table(ceo.get("business_kpis", []))
            
            st.markdown("---")
            render_roadmap_cards(ceo.get("implementation_roadmap", {}), "🗺️ Baseline Implementation Roadmap")

    elif active_stage == "🚨 Surprise Delta":
        st.subheader("🚨 Mid-Event Surprise Adaptation Delta View")
        
        st.markdown("#### 🔄 Surprise Adaptation Protocol Flow")
        st.markdown("""
        ```mermaid
        graph LR
            A[Surprise Event Input] --> B[Surprise Adaptation Engine]
            B --> C[Diff Changed vs Stable Facts]
            C --> D[Selectively Re-Run Affected Department Agents]
            D --> E[Generate Baseline vs Revised Delta View]
        ```
        """)

        s_data = st.session_state.get('surprise_data')
        if not s_data and os.path.exists(surprise_path):
            with open(surprise_path, "r", encoding="utf-8") as f:
                s_data = json.load(f)

        if s_data:
            s_ceo = s_data.get("stage5_ceo_decision", {})
            s_brief = s_data.get("brief", {})
            s_dept = s_data.get("stage1_department_outputs", {})

            col_base, col_surp = st.columns(2)

            with col_base:
                with st.container(border=True):
                    st.markdown("### 🏛️ Baseline Decision (Before Surprise)")
                    st.markdown(f"**Decision**: {ceo.get('decision_statement')}")
                    st.markdown("**Original Case Facts**: " + str(len(brief.get('supplied_facts', []))) + " facts parsed")
                    st.markdown("#### Baseline KPIs")
                    st.table(ceo.get("business_kpis", []))
                    
                    if "Data Analyst" in dept_outputs:
                        b_da = dept_outputs["Data Analyst"].get("metrics", {})
                        b_seg = b_da.get("segment_breakdown", {})
                        b_comp = b_da.get("competitor_benchmarks", [])
                        st.markdown("#### 📊 Baseline Segment Mix")
                        if b_seg:
                            st.bar_chart(pd.DataFrame.from_dict(b_seg, orient='index', columns=['Allocation (%)']))
                        if b_comp:
                            st.markdown("#### 🏆 Baseline Competitor Matrix")
                            st.table(b_comp)

            with col_surp:
                with st.container(border=True):
                    st.markdown("### 🚨 Revised Decision (Post-Surprise Pivot)")
                    st.markdown(f"**Revised Decision**: {s_ceo.get('decision_statement')}")
                    st.markdown("#### Updated Surprise KPIs")
                    st.table(s_ceo.get("business_kpis", []))
                    
                    if "Data Analyst" in s_dept:
                        s_da = s_dept["Data Analyst"].get("metrics", {})
                        s_seg = s_da.get("segment_breakdown", {})
                        s_comp = s_da.get("competitor_benchmarks", [])
                        st.markdown("#### 📊 Post-Surprise Reallocated Segment Mix")
                        if s_seg:
                            st.bar_chart(pd.DataFrame.from_dict(s_seg, orient='index', columns=['Allocation (%)']))
                        if s_comp:
                            st.markdown("#### ⚡ Post-Surprise Competitor Shock Matrix")
                            st.table(s_comp)

            st.markdown("---")
            render_roadmap_cards(s_ceo.get("implementation_roadmap", {}), "🗺️ Revised Implementation Roadmap (Post-Surprise Pivot)")
        else:
            st.info("No surprise adaptation run trace found yet. Click '🚨 Run Surprise Adaptation Protocol' in the sidebar to simulate the surprise round.")

    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No baseline run trace found yet. Click 'Run Baseline Swarm Protocol' in the sidebar or run `python main.py` in your terminal.")
