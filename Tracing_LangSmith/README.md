# LangSmith Traces — Evidence

Real LangSmith traces captured from running the 4 evaluation scenarios through the [LangSmith pipeline](../langsmith_pipeline/) on **April 26, 2026**.

These screenshots demonstrate end-to-end observability: every retrieval, prompt, LLM call, latency measurement, and token count is captured.

---

## Screenshots

The 8 screenshots in this folder show:

| # | What it shows |
|---|---------------|
| 1 | The LangSmith project dashboard with all 4 scenario runs (green status) |
| 2-7 | Drill-in views of individual traces — retrieval step, full prompt, response, metadata |
| 8 | Latency / token count / cost breakdown |

GitHub renders the PNG files inline — click any image to view full-size.

---

## Trace JSON exports

The 4 `run-*.json` files are raw trace exports straight from LangSmith. Each one corresponds to one scenario:

- `run-019dccbb-5e93-...` — Scenario FC2 (vague opener)
- `run-019dccbb-6d27-...` — Scenario HP2 (supply chain, slot-filling)
- `run-019dccbb-7395-...` — Scenario FC1 (MBA GMAT waiver)
- `run-019dccbb-7a6c-...` — Scenario HP1 (fintech → financial management)

The JSONs contain the full request/response payloads, retrieval results, model parameters, and timing data — useful if anyone wants to audit the trace data programmatically without LangSmith account access.

---

## How these were generated

```bash
cd langsmith_pipeline
source venv/bin/activate
python run_scenarios.py
```

Then I opened https://smith.langchain.com → Projects → `etb-daniels-admissions` → drilled into each run → captured screenshots.

---

## Live LangSmith dashboard

If you have a LangSmith account, the live project lives at:
https://smith.langchain.com (Projects → `etb-daniels-admissions`)

(Project visibility is private to my workspace — JSON exports + screenshots in this folder are the externally-shareable equivalent.)
