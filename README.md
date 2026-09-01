# Agentic Swarm — Executive AI Boardroom

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Framework: LangGraph](https://img.shields.io/badge/Framework-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![Primary Model: Groq LLMs](https://img.shields.io/badge/Model-Groq_Compound_--_Qwen-green.svg)](https://groq.com/)
[![Fallback Model: Gemini 3.6 Flash](https://img.shields.io/badge/Fallback-Gemini_3.6_Flash-yellow.svg)](https://aistudio.google.com/)

An autonomous executive management team designed for strategic business analysis, quantitative data modeling, rigorous department debate, strategy tradeoff evaluation, and adaptive decision-making under sudden market surprises. Built strictly according to the **Official Agentic Swarm Rulebook v1.0**.

---

## 1. Team & Submission Information (Rulebook §53 & §54)

* **Team Name**: 4 Star Rating Swarm
* **Team Members**:
  - **Kushagra Saxena**: Team Lead & Orchestration Architect (LangGraph Engine & API Router)
  - **Sharath Jeeth N R**: Agent Engineering Lead (Prompts & Schema Validation)
  - **Debadrita Munshi**: Adaptability & Trace Specialist (Surprise Engine & Audit Logging)
  - **Praggya Pal**: UI Dashboard & Documentation Lead (Streamlit & Pitch Deck)
* **Selected Challenge**: Theme A/B/C Enterprise Strategy & Surprise Adaptation (FinSwarm / SaaS Swarm / ChipSwarm)
* **One-Paragraph Solution Summary**: 
  Our system implements an autonomous 5-stage boardroom protocol (Analyse ➔ Share ➔ Challenge ➔ Compare ➔ Decide) powered by 7 specialized agents. An Input Interpreter extracts hard facts vs. tagged `[ASSUMPTION: ...]` labels. Department agents (Business Research, Finance, Marketing, Data Analyst) perform parallel independent analysis and quantitative modeling. A Risk Reviewer scrutinizes departmental claims and issues formal Stage 3 pushback to force realistic rebuttals. The CEO Agent evaluates dynamic strategy tradeoffs, names rejected alternatives with detailed flaws, and outputs a 30-60-90 day roadmap with $\ge 3$ measurable KPIs. A mid-event Surprise Adaptation Engine diffs changed facts and selectively re-runs affected agents, providing dual audit traces (JSON & Markdown) and a Streamlit dashboard with real-time numeric charts and competitor benchmarks.

---

## 2. Agent Roster & Domain Responsibilities (Rulebook §55)

| # | Agent Name | Domain Responsibility | Input Data | Minimum Visible Output |
|---|---|---|---|---|
| 1 | **Input Interpreter** | Case Deconstruction & Fact vs. Assumption Tagging | Raw Business Case Text | Structured Brief JSON (`supplied_facts`, `identified_assumptions`, `constraints`) |
| 2 | **Business Research** | TAM/SAM/SOM, market dynamics, competitive threat matrix | Structured Brief | Market Findings, Evidence & Growth Analysis |
| 3 | **Finance & Treasury** | CapEx/OpEx breakdown, unit economics, ROI, runway modeling | Structured Brief | Financial Plan, Cost Limits & Fiscal Assumptions |
| 4 | **Marketing & Sales** | Ideal Customer Profile (ICP), GTM channels, CAC/LTV benchmarks | Structured Brief | Go-To-Market Recommendation & Channel Allocations |
| 5 | **Data Analyst** | Quantitative segment allocation math & competitor benchmarking | Structured Brief | Numerical Metrics, Segment Allocation Chart & Competitor Matrix |
| 6 | **Risk & Reviewer** | Scrutinizes departmental claims and triggers Stage 3 debate | Shared Department Outputs | Challenge Memos & Mandatory Rebuttal Responses |
| 7 | **CEO Synthesizer** | Resolves conflict, compares strategies, issues final decision | Boardroom Trace State | Final Order, Detailed Rejected Alternative, Roadmap, $\ge 3$ KPIs |

---

## 3. The 5-Stage Boardroom Protocol Workflow

```
[ Raw Business Case Text ]
            │
            ▼
  1. INPUT INTERPRETER (Fact vs Assumption Extractor)
            │
            ├──► 2. BUSINESS RESEARCH (Market Dynamics)
            ├──► 3. FINANCE & TREASURY (Unit Economics & Runway)
            ├──► 4. MARKETING & SALES (GTM & Customer Acquisition)
            └──► 5. DATA ANALYST       (Quantitative Modeling & Charts)
            │
            ▼ (Stage 1: Analyse & Stage 2: Share)
  6. RISK & REVIEWER (Stage 3: Challenge & Rebuttal Trigger)
            │
            ▼ (Stage 4: Compare Dynamic Strategy A vs Strategy B)
  7. CEO SYNTHESIZER (Stage 5: Final Order, Rejected Rationale, Roadmap, ≥3 KPIs)
```

---

## 4. Setup, Installation & Execution Instructions (Rulebook §56)

### Prerequisites
- Python 3.11 or higher installed on Windows, Mac, or Linux.
- Free API keys from [Groq Console](https://console.groq.com) and [Google AI Studio](https://aistudio.google.com).

### Step 1: Clone Repository & Install Dependencies
```bash
git clone https://github.com/Kushagra230706/4_star_rating_agentswarm.git
cd 4_star_rating_agentswarm

python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 2: Configure Environment Variables
Copy `.env.example` to `.env` and insert your API keys:
```bash
cp .env.example .env
```
Edit `.env`:
```env
GROQ_API_KEY=gsk_your_actual_groq_key
GEMINI_API_KEY=AIzaSy_your_actual_gemini_key
```

### Step 3: Run Full Boardroom Swarm (CLI)
```bash
# Run Baseline Protocol & Mid-Event Surprise Adaptation:
python main.py
```
*Outputs generated*:
- `outputs/baseline_trace.json` & `outputs/baseline_decision.md`
- `outputs/surprise_trace.json` & `outputs/revised_decision.md`

### Step 4: Launch Web Dashboard (Interactive Judging UI)
```bash
streamlit run app_ui.py
```
Open **http://localhost:8501** in your browser to view live agent traces, interactive segment bar charts, competitor benchmark matrices, and side-by-side baseline vs. surprise delta views.

---

## 5. Models, Frameworks, Datasets & External Services (Rulebook §57)

* **Primary Reasoning LLM**: Groq Cloud API (`groq/compound`, `qwen/qwen3.8-27b`, `llama-3.3-70b-versatile`) — ultra-fast inference for multi-turn boardroom agent debates.
* **Secondary Fallback LLM**: Google Gemini API (`gemini-3.6-flash`) via Google AI Studio — automatically triggered if Groq API rate-limits or times out.
* **Orchestration Framework**: LangGraph OSS / Custom State Graph Coordinator (`core/engine.py`).
* **UI Framework**: Streamlit (`app_ui.py`) with native interactive charting (`st.bar_chart`, `st.metric`, `st.table`).
* **Validation & Data Libraries**: Pydantic v2, Python-dotenv, Requests.
* **Datasets Used**: Official hackathon case datasets (`data/sample_case.json` and organizer challenge packs).

---

## 6. Known Limitations & Failure-Handling Behavior (Rulebook §58)

1. **Multi-Provider Automatic Fallback**: If the primary Groq API fails or encounters rate limits, the system automatically routes queries to Google Gemini 3.6 Flash.
2. **Deterministic Heuristic Safety Net**: If both cloud APIs become unreachable due to network isolation, the system executes a deterministic domain heuristic backup state so the CEO Agent can still synthesize a complete, non-crashing decision dossier.
3. **Loop Control & Termination**: Debate cycles in Stage 3 are strictly capped at $\le 3$ iterations to prevent uncontrolled conversation loops and guarantee deterministic system termination.
4. **Console Encoding Resilience**: `sys.stdout` is reconfigured to UTF-8 with non-ASCII safe printers to prevent Windows cp1252 character crashes during live agent streaming.
5. **Limitations**: LLM responses are bounded by the facts provided in the brief. Theoretical calculations depend on supplied numerical parameters.

---

## 7. Declaration of Pre-existing & Reused Components (Rulebook §59)

* **Reused Open-Source Libraries**: LangGraph, Groq Python SDK, Google Generative AI SDK, Streamlit, Pydantic, Requests, Python-dotenv.
* **Pre-existing Boilerplate**: Standard Python project structure and environment templates.
* **Original Work Authored During Event**: All 7 agent prompts (`agents/`), Pydantic state schemas (`core/state.py`), 5-stage boardroom coordinator (`core/engine.py`), surprise adaptation engine (`surprise/adapt.py`), trace exporters (`core/logger.py`), dynamic strategy generators, and Streamlit visual UI dashboard (`app_ui.py`).
* **Secrets Declaration**: **Zero API keys or secrets are committed to Git.** All API keys are loaded dynamically via local `.env` file ignored by Git.
