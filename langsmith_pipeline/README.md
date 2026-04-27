# LangSmith Pipeline

Parallel observability pipeline for the Daniels Admissions Agent. Runs the same knowledge base and system prompt as the Voiceflow front-end agent, but instrumented end-to-end with LangSmith tracing.

This is what generated the trace screenshots in [`../Tracing_LangSmith/`](../Tracing_LangSmith/).

---

## Why this exists separately from Voiceflow

Voiceflow is the user-facing agent — voice + chat embedded on the public webpage. It's optimized for fast iteration and a polished UX, but does **not** natively integrate with LangSmith.

The project rubric requires LangSmith tracing for observability. So this pipeline replicates the agent's logic in Python (LangChain) using the same KB and system prompt, then runs the evaluation scenarios through it. Every retrieval call, prompt composition, and LLM invocation is traced — giving us the production-grade observability the rubric calls for, without sacrificing the Voiceflow front-end.

---

## Architecture

```
user query
    │
    ▼
[ChromaDB retriever]  ──── pulls top-3 KB chunks via semantic similarity
    │
    ▼
[Prompt template]     ──── system prompt + retrieved chunks + user question
    │
    ▼
[ChatAnthropic]       ──── Claude Haiku 4.5 (temp=0.3, max_tokens=400)
    │
    ▼
response

(every step traced by LangSmith via env vars)
```

---

## Setup

### 1. Install Python 3.11+

Verify:
```bash
python3 --version
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Takes 5-10 min on first install (downloads LangChain, ChromaDB, sentence-transformers, etc).

### 4. Configure API keys

```bash
cp .env.example .env
```

Edit `.env` and replace placeholders with your real keys:

- `ANTHROPIC_API_KEY` — get from https://console.anthropic.com/settings/keys
- `LANGSMITH_API_KEY` — get from https://smith.langchain.com/settings (Personal Access Token)

⚠️ **Never commit `.env`** — it's already in `.gitignore`.

---

## Run

### Build the vector store (one time)

```bash
python ingest.py
```

This:
1. Loads all 77 `.txt` files from `../kb/`
2. Embeds them with sentence-transformers (downloads ~80MB model on first run)
3. Saves a Chroma vector store to `chroma_db/` (gitignored)

### Run the test scenarios

```bash
python run_scenarios.py
```

Runs the 4 evaluation scenarios end-to-end. Each invocation creates a trace in LangSmith with full visibility into:

- Which KB chunks were retrieved (and their similarity scores)
- The full prompt sent to Claude (system prompt + context + question)
- The raw model response
- Latency, token counts, and cost per call

### View traces

Open https://smith.langchain.com → Projects → `etb-daniels-admissions`

---

## Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for API keys (copy to `.env` and fill in) |
| `.gitignore` | Excludes `.env`, `venv/`, `chroma_db/`, `__pycache__/` |
| `ingest.py` | Loads `kb/*.txt` into a local Chroma vector store |
| `agent.py` | LangChain RAG agent (retrieval + LLM + system prompt) |
| `run_scenarios.py` | Runs the 4 April-4 evaluation scenarios |

---

## Test scenarios

The 4 scenarios run by `run_scenarios.py`:

| ID | Scenario | What it tests |
|----|----------|---------------|
| HP1 | Fintech professional → financial management | Career-goal routing to MSF, persona-aware tone, employer grounding |
| FC1 | MBA GMAT waiver question | Program disambiguation, explicit waiver routing rule |
| HP2 | Supply chain professional, uncertain direction | Slot-filling before routing, persona awareness |
| FC2 | "I'm thinking about going back to school" | Vague-opener handling — must ask grad-vs-UG before experience |

Originally documented in `docs/test_report.md`.
