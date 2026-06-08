# 🔍 AI Research Agent

> An autonomous multi-agent research system powered by **CrewAI**, **Groq LLM**, and **Tavily Search** that researches any topic and generates a professional, structured research report automatically.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-0.108.0-orange)
![Groq](https://img.shields.io/badge/LLM-Groq%20LLaMA%203.3-green)
![Gradio](https://img.shields.io/badge/UI-Gradio-yellow)
![Pydantic](https://img.shields.io/badge/Validation-Pydantic%20v2-red)

---

## 📌 Project Overview

This project is a **production-grade Agentic AI system** built using CrewAI framework. It uses **3 specialized AI agents** that work sequentially — each agent handles one specific responsibility — to produce a comprehensive research report on any given topic.

The system features:
- Multi-agent pipeline (Researcher → Analyst → Writer)
- Real-time internet search using Tavily API
- Pydantic v2 input/output validation
- Interactive Gradio web UI
- Auto-saved reports with timestamps
- FastAPI-ready backend structure

---

## 🎯 Problem Statement

Manually researching a topic requires:
- Searching multiple sources
- Filtering relevant information
- Extracting key insights
- Writing a structured report

This is time-consuming and inconsistent. This agent system automates the **entire research pipeline** end-to-end in minutes.

---

## 🏗️ System Architecture

```
User Input (Topic)
        │
        ▼
┌───────────────────┐
│   Gradio UI       │  ← Web Interface (browser)
│   gradio_app.py   │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Pydantic         │  ← Input Validation
│  ResearchInput    │  (min_length, max_length, type check)
└────────┬──────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│              CrewAI Crew                    │
│                                             │
│  ┌─────────────┐                            │
│  │  Researcher │ ← Tavily Search Tool       │
│  │   Agent     │   (real internet search)   │
│  └──────┬──────┘                            │
│         │ research notes                    │
│         ▼                                   │
│  ┌─────────────┐                            │
│  │   Analyst   │ ← No tool (LLM reasoning)  │
│  │   Agent     │   (extracts key insights)  │
│  └──────┬──────┘                            │
│         │ structured insights               │
│         ▼                                   │
│  ┌─────────────┐                            │
│  │   Writer    │ ← No tool (LLM writing)    │
│  │   Agent     │   (writes final report)    │
│  └──────┬──────┘                            │
└─────────┼───────────────────────────────────┘
          │
          ▼
┌───────────────────┐
│  Pydantic         │  ← Output Validation
│  ResearchOutput   │  (word count, status, timestamp)
└────────┬──────────┘
         │
         ▼
  outputs/reports/
  report_20260608_143022.md  ← Auto-saved report
```

---

## 🤖 Agents — Roles & Responsibilities

### Agent 1 — Senior Research Analyst
| Property | Detail |
|---|---|
| **Role** | Senior Research Analyst |
| **Goal** | Research deeply on given topic using internet search |
| **Tool** | Tavily Search API (real-time web search) |
| **Max Iterations** | 5 |
| **Output** | Detailed research notes with sources and links |

### Agent 2 — Data Analyst
| Property | Detail |
|---|---|
| **Role** | Expert Data Analyst and Insight Extractor |
| **Goal** | Extract key insights, statistics, and trends from research notes |
| **Tool** | None — pure LLM reasoning |
| **Max Iterations** | 3 |
| **Output** | Structured analysis with key insights, statistics, trends |

### Agent 3 — Professional Report Writer
| Property | Detail |
|---|---|
| **Role** | Professional Technical Report Writer |
| **Goal** | Write a complete, professional markdown report |
| **Tool** | None — pure LLM writing |
| **Max Iterations** | 3 |
| **Output** | Full markdown report saved to outputs/reports/ |

---

## 📋 Tasks Flow

```
Task 1: research_task
→ Assigned to: Researcher Agent
→ Action: Multiple web searches on topic
→ Output: Comprehensive research notes (min 500 words)

        ↓ (notes passed as context)

Task 2: analysis_task
→ Assigned to: Analyst Agent
→ Action: Extract insights from research notes
→ Output: Structured key insights, stats, trends

        ↓ (insights passed as context)

Task 3: write_task
→ Assigned to: Writer Agent
→ Action: Write professional report
→ Output: report_<timestamp>.md saved to outputs/reports/
```

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|---|---|---|
| **Agent Framework** | CrewAI 0.108.0 | Multi-agent orchestration |
| **LLM** | Groq (LLaMA 3.3 70B) | Language model — free & fast |
| **Search Tool** | Tavily API | Real-time internet search |
| **Validation** | Pydantic v2 | Input/output data validation |
| **Web UI** | Gradio | Interactive browser interface |
| **Package Manager** | UV | Fast Python package management |
| **Language** | Python 3.10+ | Core programming language |
| **Config** | YAML | Agents and tasks configuration |
| **Env Management** | python-dotenv | API key management |

---

## 📁 Project Structure

```
research_agent/
│
├── .env                          # API Keys (never commit)
├── .gitignore                    # Git ignore rules
├── pyproject.toml                # Project dependencies (UV)
├── README.md                     # This file
│
├── src/
│   └── research/
│       ├── __init__.py
│       ├── crew.py               # Core crew assembly + run logic
│       ├── main.py               # CLI entry point
│       ├── models.py             # Pydantic models (validation)
│       └── config/
│           ├── agents.yaml       # 3 agents definition
│           └── tasks.yaml        # 3 tasks definition
│
├── ui/
│   └── gradio_app.py             # Gradio web UI
│
└── outputs/
    └── reports/                  # Auto-saved research reports
        └── report_<timestamp>.md
```

---

## ✅ Pydantic Validation

### Input Validation (ResearchInput)
```python
topic: str        # min 3 chars, max 200 chars
depth: str        # must be: quick / detailed / comprehensive
```

**Validation Rules:**
- Topic cannot be empty or whitespace only
- Topic cannot be numbers only
- Depth must be one of allowed values
- Topic is auto-stripped of extra spaces

### Output Validation (ResearchOutput)
```python
topic: str              # Research topic
report: str             # Cannot be empty
status: str             # success / error
timestamp: str          # Auto-generated
word_count: int         # Auto-calculated
error_message: str      # Present only on failure
```

---

## 🖥️ Gradio UI Features

- **Topic Input** — Text box for entering research topic
- **Depth Selector** — Dropdown: quick / detailed / comprehensive
- **Start Research Button** — Triggers the multi-agent pipeline
- **Clear Button** — Resets all fields
- **Status Display** — Shows success or error status
- **Word Count Display** — Shows report word count
- **Report Display** — Renders markdown report in browser
- **Example Topics** — Click-to-try example topics

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10 or higher
- UV package manager installed
- Groq API key (free at console.groq.com)
- Tavily API key (free at tavily.com)

### Step 1 — Clone Repository
```bash
git clone https://github.com/abubakarsaddique22/research_agent.git
cd research_agent
```

### Step 2 — Install Dependencies
```bash
uv sync
```

### Step 3 — Setup Environment Variables
Create `.env` file in project root:
```env
MODEL=groq/llama-3.3-70b-versatile
GROQ_API_KEY=gsk_your_groq_api_key_here
TAVILY_API_KEY=tvly-your_tavily_api_key_here
```

### Step 4 — Create Output Directory
```bash
mkdir outputs
mkdir outputs\reports
```

### Step 5 — Run

**Option A — Web UI (Recommended)**
```bash
cd ui
python gradio_app.py
```
Open browser: `http://localhost:7860`

**Option B — Command Line**
```bash
crewai run
```

---

## 🔑 API Keys — How to Get

### Groq API Key (Free)
1. Go to https://console.groq.com
2. Create free account
3. Navigate to API Keys
4. Click "Create API Key"
5. Copy and paste in `.env`

### Tavily API Key (Free)
1. Go to https://tavily.com
2. Create free account
3. 1000 free searches per month
4. Copy API key and paste in `.env`

---

## 🐛 Problems Faced & Solutions

### Problem 1 — search_tool KeyError
```
KeyError: 'search_tool'
```
**Cause:** tasks.yaml had tools section which CrewAI could not resolve.
**Solution:** Removed tools section from tasks.yaml. Tools are assigned directly to agents in crew.py only.

---

### Problem 2 — OPENAI_API_KEY Required
```
ERROR: OpenAI API call failed: OPENAI_API_KEY is required
```
**Cause:** CrewAI defaults to OpenAI if no LLM is explicitly set.
**Solution:** Explicitly defined Groq LLM in crew.py with `LLM()` class and passed it to each agent.

---

### Problem 3 — cache_breakpoint Unsupported
```
GroqException: property 'cache_breakpoint' is unsupported
```
**Cause:** Latest CrewAI version injects cache_breakpoint into messages which Groq API does not support.
**Solution:** Pinned CrewAI to version 0.108.0 in pyproject.toml and set `cache=False` in Crew, Agents, and LLM.

---

### Problem 4 — Pydantic Report Empty Error
```
ValidationError: Report empty nahi ho sakti
```
**Cause:** When LLM failed, empty string was passed to ResearchOutput validator.
**Solution:** Set default fallback strings ("Research failed", "Validation failed") instead of empty string in error handlers.

---

### Problem 5 — Gradio theme Warning
```
UserWarning: theme parameter moved to launch() method
```
**Cause:** Gradio 6.0 moved theme parameter from Blocks() to launch().
**Solution:** Removed theme from `gr.Blocks()` constructor.

---

### Problem 6 — Browser ERR_ADDRESS_INVALID
```
Failed to load page — ERR_ADDRESS_INVALID
URL: http://0.0.0.0:7860
```
**Cause:** `0.0.0.0` is server binding address, not browser address.
**Solution:** Open `http://localhost:7860` in browser instead.

---

### Problem 7 — Duplicate [tool.crewai] in pyproject.toml
**Cause:** Section was accidentally written twice.
**Solution:** Merged both into single `[tool.crewai]` section with all fields.

---

## 📊 Sample Report Output

```markdown
# Artificial Intelligence Trends in 2026 — Research Report

## Executive Summary
AI in 2026 is defined by agentic systems...

## Introduction
Artificial Intelligence has evolved rapidly...

## Key Findings
- Agentic AI is the fastest growing segment
- Multi-agent systems adopted by 60% of enterprises...

## Current Trends
1. Agentic AI replacing simple chatbots
2. Small Language Models (SLMs) growing...

## Key Players
- OpenAI, Anthropic, Google DeepMind...

## Future Outlook
By 2027, autonomous agents expected to...

## References
- Source 1: https://...
- Source 2: https://...
```

---

## 🚀 Future Improvements

- [ ] FastAPI backend for REST API access
- [ ] Docker containerization
- [ ] AWS EC2 deployment
- [ ] Report history viewer in UI
- [ ] PDF export of reports
- [ ] Multiple language support
- [ ] Email report delivery

---

## 👤 Author

**Abubakar Saddique**
- GitHub: [@abubakarsaddique22](https://github.com/abubakarsaddique22)
- LinkedIn: [abubakrsaddique](https://linkedin.com/in/abubakrsaddique)
- Portfolio: [abubakarsaddique22.github.io](https://abubakarsaddique22.github.io/portfolio_datascience/)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with ❤️ using CrewAI + Groq + Tavily*