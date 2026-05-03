# LangSmith Traces — Evidence

Live traces captured from running the agent's evaluation scenarios through the [LangSmith pipeline](../langsmith_pipeline/). Every retrieval, prompt, LLM call, latency, and token count is captured.

---

## Featured traces (start here)

These four screenshots best demonstrate end-to-end observability and the agent's design discipline.

### 1. Fintech professional → financial management (Scenario HP1)

![HP1 trace — input/output](./01_HP1_input_output.png)

The full LangChain run tree on the left: `RunnableParallel` → `VectorStoreRetriever` (Chroma) + `format_docs` → `ChatPromptTemplate` → `ChatAnthropic` (Claude Haiku 4.5, ~3.7s, ~5.4k tokens, ~$0.0007) → `StrOutputParser`. The agent recommends MSF and asks the slot-filling question, exactly as designed.

### 2. Trace metadata + runtime (HP1)

![HP1 trace — metadata/attributes](./02_HP1_metadata.png)

Custom scenario tagging (`scenario_id: HP1`, `scenario_name: Fintech to financial management`) attached at invocation, plus the LangSmith project binding and full Python runtime context. This is what makes the traces filterable in the dashboard.

### 3. Recovered failure case — MBA GMAT waiver (Scenario FC1)

![FC1 trace — input/output](./03_FC1_input_output.png)

This was the original April 4 failure case (agent retrieved the generic admissions chunk and gave a vague answer). The new agent now recognizes the ambiguity (One-Year MBA vs. Online MBA) and asks the disambiguating question — proof the Layer 4 routing rule fix worked.

### 4. Recovered failure case — vague opener (Scenario FC2)

![FC2 trace — input/output](./07_FC2_input_output.png)

The other April 4 failure case — agent originally jumped to experience-level questions on a vague opener. Now correctly opens with the grad-vs-undergrad orienting question per Layer 3 Step 1. The vague-opener rule in the system prompt is doing what it should.

---

## Full screenshot set

All 8 screenshots cover the 4 evaluation scenarios x 2 views each (Input/Output + Metadata/Attributes):

- **HP1** (fintech -> financial mgmt): `01_HP1_input_output.png`, `02_HP1_metadata.png`
- **FC1** (MBA GMAT waiver): `03_FC1_input_output.png`, `04_FC1_metadata.png`
- **HP2** (supply chain slot-fill): `05_HP2_input_output.png`, `06_HP2_metadata.png`
- **FC2** (vague opener): `07_FC2_input_output.png`, `08_FC2_metadata.png`

---

## Trace JSON exports

Raw trace data exported directly from LangSmith. Each file corresponds to one scenario:

| File | Scenario |
|------|----------|
| `run-019dccbb-5e93-...json` | HP1 — Fintech to financial management |
| `run-019dccbb-6d27-...json` | FC1 — MBA GMAT waiver |
| `run-019dccbb-7395-...json` | HP2 — Supply chain professional |
| `run-019dccbb-7a6c-...json` | FC2 — Vague opener |

Each JSON contains the full request payload, retrieval results, model parameters, and timing data — useful for programmatic auditing without LangSmith account access.

---

## How these were generated

```bash
cd langsmith_pipeline
source venv/bin/activate
python run_scenarios.py
```

Then opened https://smith.langchain.com -> Projects -> `etb-daniels-admissions` -> drilled into each run -> captured Input/Output + Metadata views as PNGs, exported the run JSON via the LangSmith UI.

---

## Why this matters

LangSmith tracing is a project-rubric requirement, but it's also a real production-grade observability tool. Every model call is captured, replayable, and auditable — the same workflow you'd use at a company shipping AI to users. These traces are the canonical evidence that the agent's RAG + LLM pipeline runs as designed.
