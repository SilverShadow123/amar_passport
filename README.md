# AmarPassport — Bangladesh E-Passport Readiness Assistant

A multi-agent AI system built with [CrewAI](https://crewai.com) that helps Bangladeshi citizens prepare their e-passport application. Given an applicant's profile, it analyzes eligibility, calculates fees, generates a document checklist, and produces a comprehensive readiness report in both English and Bangla.

## Agents

| Agent | Role |
|---|---|
| **Police Guardian** | Bangladesh Passport Policy Expert — determines passport validity (5 vs 10 years) and required ID (NID vs Birth Registration) based on age |
| **Chancellor of the Exchequer** | Financial Auditor — calculates exact BDT fee including 15% VAT based on page count and delivery speed |
| **Document Architect** | Documentation Officer — generates a customized document checklist based on age, profession, and circumstances |
| **Passport Readiness Officer** | Virtual Consular Officer — synthesizes all outputs into a final Markdown report in English and Bangla |

## How It Works

```
User Profile → [Policy Guardian] → [Fee Auditor] → [Document Architect] → [Readiness Officer] → Report
```

1. You provide applicant details (age, profession, urgency, page count, location, NID status)
2. Agents collaborate sequentially, each with access to a knowledge base of 2026 fee tables and document rules
3. A final `report.md` is generated with eligibility, fees, required documents, and policy flags

## Requirements

- Python >=3.10, <3.14
- [UV](https://docs.astral.sh/uv/) package manager
- An [OpenRouter](https://openrouter.ai) API key (or any LLM supported by CrewAI)
- A [Serper](https://serper.dev) API key for web search

## Setup

```bash
# Install uv if needed
pip install uv

# Clone and enter the project
cd amar_passport

# Install dependencies
uv sync

# Configure environment variables
cp .env.example .env
```

Edit `.env` and add your keys:

```
OPENROUTER_API_KEY=sk-or-v1-...
SERPER_API_KEY=...
```

## Run

```bash
# From the project root
uv run --active python src/amar_passport/main.py
```

Or use the CrewAI CLI:

```bash
crewai run
```

The output will be written to `report.md`.

## Customize

Edit the applicant profile in `src/amar_passport/main.py:run()`:

```python
inputs = {
    'age': '24',
    'profession': 'private sector employee',
    'urgency': 'Express',
    'pages': '64',
    'location': 'Dhaka',
    'has_nid': 'Yes'
}
```

## Project Structure

```
amar_passport/
├── knowledge/
│   ├── passport_db.json      # Fee table & document rules (JSON knowledge source)
│   └── user_preference.txt   # Sample user context
├── src/amar_passport/
│   ├── config/
│   │   ├── agents.yaml       # Agent role/goal/backstory definitions
│   │   └── tasks.yaml        # Task descriptions & agent assignments
│   ├── tools/
│   │   └── custom_tool.py    # Custom tool implementations
│   ├── crew.py               # Crew orchestration class
│   └── main.py               # Entry point with applicant inputs
├── .env                      # API keys
├── pyproject.toml
└── README.md
```

## Tech Stack

- **CrewAI** — Multi-agent orchestration
- **OpenRouter (gpt-4o-mini)** — LLM inference
- **SerperDevTool** — Web search capability
- **sentence-transformers** — Local embeddings for knowledge retrieval (no OpenAI key required)
- **ChromaDB** — Vector storage for knowledge source
