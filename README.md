# Daniels Admissions Agent

An AI-powered admissions advisor for Purdue's Mitch Daniels School of Business graduate programs. Built as a final project for the ETB course (MGMT 59000-ETB, Spring 2026).

> 🌐 **Live demo:** https://meownager.github.io/etb-daniels-admissions-agent/
> 📊 **LangSmith traces:** see [`Tracing_LangSmith/`](./Tracing_LangSmith/)

---

## What it does

Helps prospective applicants explore graduate program options at Daniels by:

- Asking grounded discovery questions (career goals, experience level, constraints)
- Recommending programs from a 13-program catalog based on persona and intent
- Answering specific admissions questions (GMAT waivers, deadlines, costs) with source-backed responses
- Surfacing real outcomes data (salaries, top employers, employment rates)
- Routing out-of-scope questions (housing, athletics) to the right human contact

---

## Architecture

Two parallel implementations sharing one knowledge base:

```
                       ┌──────────────────────────┐
                       │  77-chunk knowledge base │
                       │  (programs, KPIs,        │
                       │   personas, objections)  │
                       └────────────┬─────────────┘
                                    │
              ┌─────────────────────┴─────────────────────┐
              │                                           │
   ┌──────────▼──────────┐                  ┌─────────────▼────────────┐
   │  Voiceflow agent    │                  │  LangChain pipeline      │
   │  (user-facing)      │                  │  (observability)         │
   │                     │                  │                          │
   │  • Embedded chat    │                  │  • ChromaDB retrieval    │
   │    widget on        │                  │  • Claude Haiku 4.5      │
   │    GitHub Pages     │                  │  • LangSmith tracing     │
   └─────────────────────┘                  └──────────────────────────┘
```

**Why two agents?** Voiceflow gives a fast iteration loop and a polished frontend, but doesn't natively integrate with LangSmith. To get end-to-end observability — required by the project rubric — we built a parallel Python pipeline using the same KB and system prompt. Both agents produce equivalent answers; only the runtime differs. The Python pipeline is what generates the traces stored in [`Tracing_LangSmith/`](./Tracing_LangSmith/).

---

## Tech stack

| Layer | Tool |
|-------|------|
| Voice + chat front end | Voiceflow |
| LLM | Anthropic Claude Haiku 4.5 |
| RAG orchestration | LangChain |
| Vector store | ChromaDB (local, file-based) |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2` (free, local) |
| Observability | LangSmith |
| Webpage hosting | GitHub Pages |

---

## Knowledge base

77 plain-text chunks covering:

- **5 applicant personas** — recent grad → senior professional, plus parent
- **13 graduate programs** — MBA (One-Year + Online), MSF, MSGSCM (residential + online), MSBAIM (residential + online), MSHRM (residential + online), MSM, MSA, MBT, Online MS Economics
- **24 career-goal routes** — fintech → MSF, supply chain → MSGSCM, accounting → MSA, etc.
- **Admissions** — shared requirements, program-specific rules, GMAT waivers, scholarships, English tests
- **12 objection-handling chunks** — cost, timing, GMAT anxiety, online-vs-residential, etc.
- **Out-of-scope and escalation** — housing/athletics handoff to admissions team

See [`kb/`](./kb/) for the chunks and [`system_prompt.txt`](./system_prompt.txt) for the routing logic (7-layer architecture).

---

## Running the LangSmith pipeline locally

See [`langsmith_pipeline/README.md`](./langsmith_pipeline/README.md) for full instructions.

Quick version:
```bash
cd langsmith_pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then edit with your real Anthropic + LangSmith keys
python ingest.py       # build local vector store
python run_scenarios.py  # run 4 test scenarios; traces appear in LangSmith
```

---

## Repository structure

```
etb-daniels-admissions-agent/
├── README.md                       # This file
├── index.html                      # Live webpage (GitHub Pages)
├── system_prompt.txt               # 7-layer agent system prompt
├── kb/                             # 77 knowledge-base chunks
├── langsmith_pipeline/             # Python observability pipeline
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   ├── ingest.py
│   ├── agent.py
│   └── run_scenarios.py
├── Tracing_LangSmith/              # LangSmith trace screenshots + JSON exports
└── docs/                           # Project documentation
    ├── changelog.md
    └── test_report.md
```

---

## Acknowledgments

- Built for **MGMT 59000-ETB (Spring 2026)** at Purdue's Mitch Daniels School of Business
- Course instruction: [Add instructor name]
- Group members: [Add teammates]
- Tools: [Anthropic Claude](https://www.anthropic.com/), [LangSmith](https://smith.langchain.com/), [Voiceflow](https://voiceflow.com/), [LangChain](https://langchain.com/)
- Inspired by [add references here — articles, talks, posts, or builds you drew on]

---

## Disclaimer

This is an independent student research project. It is not affiliated with, endorsed by, or operated by Purdue University, the Mitch Daniels School of Business, or its admissions office. Knowledge base content is sourced from publicly available program information.
