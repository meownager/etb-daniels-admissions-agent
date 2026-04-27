# Daniels Admissions Agent — RAG + System Prompt Fixes

**Date:** April 24, 2026
**Scope:** v3 of the knowledge base and system prompt, addressing 10 issues identified in the April 10 restructure

---

## What's in this folder

- `SYSTEM_PROMPT.txt` — rewritten system prompt (7 layers), ready to paste into Voiceflow or the LLM config
- `purdue_kb_v3_chunks/` — 77 plain-text chunks ready for RAG ingestion
- `purdue_kb_v3_chunks.zip` — same content, zipped for upload

---

## Fixes in this revision

### 1. Archive folder removed from the RAG tree

The April 10 restructure left seven deprecated chunks (01–04, 29_mshrm_msm combined, 37/38 combined career goal maps) inside an `archive/` subfolder that would have been indexed by most RAG pipelines. Those files are gone from `purdue_kb_v3_chunks/`. Their content either moved into the system prompt (identity, lead capture, opening script, handoff) or was superseded by sharded versions (29 + 29b for MSHRM/MSM, 37a–n and 38a–j for career goals).

### 2. Chunk 33 split by program

The original `33_online_ms_admissions_requirements.txt` combined four programs into one file. When a prospect asked about the Online MSBAIM specifically, retrieval pulled admissions requirements for three programs they didn't care about. Split into:

- 33a — Online MSBAIM
- 33b — Online MSGSCM
- 33c — Online MSHRM
- 33d — Online MS Economics

### 3. Missing career goal coverage added

The April 10 career goal sharding covered 18 goals (37a–i, 38a–i) but missed six common ones. Added:

- 37j — accounting, audit, tax, CPA track (routes to MSA)
- 37k — sales, business development, revenue leadership (routes to One-Year MBA)
- 37l — healthcare management, healthcare consulting, life sciences (routes to One-Year MBA)
- 37m — nonprofit, public sector, government (routes to One-Year MBA)
- 37n — real estate development, commercial real estate, investment (routes to MSF)
- 38j — fintech, quantitative finance, algorithmic trading (routes to MSF for quant, MSBAIM for platform)

Each file follows the same structure as the original 18: primary recommendation, reasoning, secondary recommendation, key framing, and common edge cases.

### 4. Chunk 52 (international sponsorship) deduplicated against chunk 41

The original chunk 52 duplicated the STEM-designated program list, the 36-month OPT window, and the H-1B employer names that were already in chunk 41. If both files retrieved, the LLM got the same facts twice. Chunk 52 now contains only the objection-handling frame — honesty up front, how to pivot to structural factors, tone guardrails — and references chunk 41 for the facts. Retrieve both only when the prospect asks a factual sponsorship question.

### 5. Persona chunks 05–09 rewritten as tactical, not routing

The April 10 persona chunks mixed tone guidance with program routing logic. Program routing was also in Layer 5 of the system prompt, so the LLM got two sources of truth that could drift apart. The persona chunks are now pure conversation tactics — emotional register, what to lead with, what to avoid, slot-filling questions for that persona, what prompts typically surface. Program routing lives only in Layer 5 of the system prompt.

### 6. System prompt — Layer 4 retrieval rules expanded

The April 10 Layer 4 had retrieval rules for career goals, program outcomes, program admissions, GMAT waiver, cost, international, and objections. It was silent on six chunk categories that the LLM had to route to by inference:

- Chunk 10 (UG outcomes — Parent persona)
- Chunk 21 (top employers master list)
- Chunk 22 (MBT vs One-Year MBA comparison)
- Chunk 23 (Purdue differentiators / why Purdue)
- Chunk 34 (scholarship and financial aid)
- Chunk 35 (Pathway Program)

All six now have explicit retrieval rules.

### 7. Chunk 36 vs chunk 47 disambiguated

The prior system prompt did not distinguish between the applicant asking whether they qualify for a GMAT/GRE waiver (factual — chunk 36) and the applicant expressing anxiety about the test itself (emotional — chunk 47). Layer 4 now makes the distinction explicit and describes how to handle the blended case ("I'm worried about the GMAT — do I even need to take it?").

### 8. Chunk 29b (MSM) called out explicitly

Layer 4 now documents that 29 covers MSHRM only and 29b covers MSM, so the LLM doesn't try to retrieve a non-existent combined 29 file or miss the MSM split.

### 9. "One file per question" rule softened for multi-topic queries

The April 10 Layer 4 said "You retrieve one file per question." This broke on compound questions like "What does the MSF cost, and is it STEM-designated?" The new rule: retrieve the single best file for most turns, but permit up to two files when the applicant clearly asks two distinct questions in one turn. Added a retrieval architecture note explaining that this KB is designed for classifier-routed retrieval, not top-k semantic matching.

### 10. Parent persona scope-locked to undergraduate

Layer 5 now explicitly prevents the Parent persona from drifting into graduate program routing. Parent queries route to chunk 10, chunk 39, and chunk 34. Graduate content only enters the conversation if the parent explicitly pivots.

### 11. Additional Layer 7 guardrails

Added hard guardrails for three categories the April 10 version did not cover:

- Never state application deadlines from memory (change per cycle)
- Never state tuition figures outside what is in chunk 39
- Never name specific faculty members or course names from memory

These are common hallucination targets for admissions agents and the guardrails block them at the prompt level rather than relying on the KB to catch every case.

---

## What did not change

- The 55-range objection files (43–51, 53–55) are unchanged. Chunk 52 is the only objection file that needed deduplication against a factual chunk.
- Program outcomes chunks (11–20) are unchanged.
- Admissions chunks (24–32) are unchanged.
- Cost chunks (39–40), international chunks (41–42), and out-of-scope chunk (55) are unchanged.
- The 18 original career goal files (37a–i, 38a–i) are unchanged — only added to.

---

## How to deploy

1. Upload `purdue_kb_v3_chunks.zip` (or the unzipped folder) to Voiceflow's knowledge base, replacing any prior version. Confirm that no `archive/` folder is present in the upload.
2. Paste the contents of `SYSTEM_PROMPT.txt` into the Voiceflow agent configuration or wherever the LLM's system prompt lives.
3. Test the four scenarios from the April 4 submission — in particular, the two prior failure cases:
   - "I'm thinking about school" (vague opener) — should now orient with grad-vs-UG question, not jump to experience-level probing
   - MBA GMAT waiver question — should now retrieve chunk 36 (waiver policy) with optional chunk 47 (objection) if the applicant signals anxiety

---

## Files inventory (77 chunks)

- **05–09** — 5 persona files (tactical framing only)
- **10** — undergraduate program outcomes
- **11–20** — 10 program career outcomes files
- **21** — top employers master list
- **22** — MBT vs One-Year MBA comparison
- **23** — Purdue differentiators
- **24** — shared admissions requirements
- **25–32, 29b** — 9 program-specific admissions files (residential)
- **33a–33d** — 4 online MS admissions files
- **34** — scholarship and financial aid
- **35** — Pathway Program
- **36** — GMAT/GRE waiver guidance
- **37a–37n** — 14 business/operations career goal files
- **38a–38j** — 10 people/data/tech career goal files
- **39** — tuition overview
- **40** — ROI framing
- **41** — STEM designation and OPT
- **42** — English test and foreign credentials
- **43–54** — 12 objection files
- **55** — out-of-scope and escalation
