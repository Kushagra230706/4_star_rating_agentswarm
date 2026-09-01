# Agentic Swarm — Executive AI Boardroom

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Framework: LangGraph](https://img.shields.io/badge/Framework-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![Primary Model: Groq Llama--3.3--70B](https://img.shields.io/badge/Model-Groq_Llama--3.3--70B-green.svg)](https://groq.com/)
[![Fallback Model: Gemini 2.0 Flash](https://img.shields.io/badge/Fallback-Gemini_2.0_Flash-yellow.svg)](https://aistudio.google.com/)

An autonomous, 6-agent executive management team designed for strategic business analysis, rigorous department debate, strategy tradeoff evaluation, and adaptive decision-making under sudden market surprises. Built strictly according to the **Official Agentic Swarm Rulebook v1.0**.

---

## 1. Team & Submission Information

* **Team Name**: Agentic Swarm Team
* **Selected Challenge**: Enterprise Business Case Strategy & Surprise Adaptation
* **Solution Summary**: A 5-stage boardroom protocol (Analyse ➔ Share ➔ Challenge ➔ Compare ➔ Decide) powered by 6 specialized agents. Includes an Input Interpreter for fact/assumption tagging, a Risk Reviewer for explicit department pushback, multi-provider fault tolerance (Groq + Gemini fallback), and a selective re-execution engine for mid-event business surprises.

---

## 2. Agent Roster & Domain Responsibilities

| # | Agent Name | Domain Responsibility | Min Visible Output |
|---|---|---|---|
| 1 | **Input Interpreter** | Deconstructs case into hard facts vs. tagged `[ASSUMPTION]` labels | Structured Brief (JSON) |
| 2 | **Business Research** | TAM/SAM/SOM, market dynamics, competitive threat matrix | Market Findings & Evidence |
| 3 | **Finance Director** | CapEx/OpEx breakdown, unit economics, ROI, runway modeling | Financial Plan & Assumptions |
| 4 | **Marketing & Sales** | Ideal Customer Profile (ICP), GTM channels, CAC/LTV benchmarks | Go-To-Market Recommendation |
| 5 | **Data Analyst** | Quantitative modeling, segment allocation math & competitor benchmarking | Numerical Metrics & Competitor Matrix |
| 6 | **Risk & Reviewer** | Scrutinizes departmental claims and issues formal Stage 3 pushback | Challenge Memo & Debate Rebuttal |
| 7 | **CEO Synthesizer** | Resolves conflict, compares strategies, issues final decision | Final Order, Roadmap, 3+ KPIs |

---

## 3. The 5-Stage Boardroom Protocol Workflow

```
[ Unstructured Business Case ]
              │
              ▼
    1. INPUT INTERPRETER (Fact vs Assumption Extractor)
              │
              ├──► 2. BUSINESS RESEARCH (Market Dynamics)
              ├──► 3. FINANCE DIRECTOR  (Unit Economics & Runway)
              └──► 4. MARKETING & SALES (GTM & Customer Acquisition)
              │
              ▼ (Stage 1: Analyse & Stage 2: Share)
    5. RISK & REVIEWER (Stage 3: Challenge & Dispute Trigger)
              │
              ▼ (Stage 4: Compare Strategy A vs Strategy B)
    6. CEO SYNTHESIZER (Stage 5: Final Decision, Tradeoffs, Roadmap, ≥3 KPIs)
```

---

## 4. Setup & Execution Instructions

### Prerequisites
- Python 3.11 or higher installed.
- Free API keys from [Groq Console](https://console.groq.com) and/or [Google AI Studio](https://aistudio.google.com).

### Step 1: Clone & Install Dependencies
```bash
git clone https://github.com/YourUsername/TeamName_AgenticSwarm.git
cd TeamName_AgenticSwarm
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

### Step 4: Launch Interactive Streamlit UI (Optional Visual Trace)
```bash
streamlit run app_ui.py
```

---

## 5. Technical Architecture & Fault-Tolerant Fallback

* **Primary Reasoning Model**: Groq `llama-3.3-70b-versatile` (ultra-fast inference, high analytical reasoning).
* **Automatic Secondary Fallback**: Google Gemini `gemini-2.0-flash` via AI Studio (triggered automatically if Groq rate-limits or fails).
* **Agent Fault Tolerance**: If a single department agent encounters an unrecoverable error, the system injects a safe domain heuristic fallback state to allow the CEO to synthesize a complete decision without system crash.
* **Debate Loop Control**: Debate cycles are strictly capped at $\le 3$ iterations to guarantee deterministic termination.

---

## 6. Disclosures & Declarations

* **Frameworks Used**: LangGraph (OSS execution graph), Groq SDK, Google Generative AI SDK, Streamlit, Pydantic.
* **Pre-existing / Reused Code**: Standard Python libraries and framework starter boilerplate. All agent instructions, state schemas, conflict triggers, and surprise adaptation logic were authored during the event.
* **Secrets Management**: No API keys or credentials are included in the repository. All keys are loaded dynamically via `.env` ignored by Git.
