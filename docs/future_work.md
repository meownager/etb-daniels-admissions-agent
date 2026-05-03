# Future Work

What's deliberately not in this submission, and what I plan to add post-deadline.

## Resume PDF upload — re-enable + harden

Currently disabled in production to preserve Voiceflow free-tier credits. The feature works (browser-side PDF.js extraction + smart summarizer that compresses to ~500 chars), but each upload costs ~$0.002 in Voiceflow tokens, and I want enough credits left for the prof and recruiters to actually try the chat.

To re-enable: open `index.html`, find the comment `RESUME UPLOAD SECTION - TEMPORARILY DISABLED`, change `style="display:none"` to `style=""`. One commit. Done.

Once re-enabled, the next improvement is a backend OCR fallback for image-only / scanned PDFs (PDF.js can't extract text from those). Probably a 1-hour cloudflare worker or vercel function.

## Eval set expansion to 30+ scenarios

I have 4 scenarios from the original April 4 baseline, plus Aritrika added 12 more (HP3-HP5, GR1-GR2, OBJ1-OBJ3, OOS1, FACT1, FAIL1-FAIL2). Solid coverage but not enough to catch regression on future KB edits. Real eval coverage means at least 30 scenarios across all 5 personas, all 13 programs, and the major objection categories. Structured as a CSV with pass/fail columns so I can run nightly and diff.

## Production-grade observability beyond the LangSmith demo

The current LangSmith pipeline is a parallel Python script — not what serves real users. To productionize, I'd:

1. Move retrieval to a hosted vector store (Pinecone or Chroma Cloud)
2. Wrap the agent in a FastAPI endpoint with rate limiting per IP
3. Add LangSmith tracing on every production request, not just eval scenarios
4. Set up alerts for retrieval misses or unusually long responses

## Better resume parsing

Current regex-based summarizer extracts the obvious fields (name, role, education) but misses anything in unusual formats. Real version would either:

- Run a quick Haiku summarization call before sending to the main agent (one extra LLM call but compresses any resume to a structured JSON)
- Use a small dedicated model (something like spaCy NER) for entity extraction

I have a slight preference for the Haiku approach since it handles arbitrary formats.

## Multi-turn conversation testing

Right now I tested 1-3 turn exchanges. Real applicants chat for 5-10 turns before deciding. I want to set up a multi-turn eval framework where each scenario has 5+ pre-scripted user follow-ups, and we score whether the agent stays consistent and on-task across the full conversation.

## What I'm intentionally not adding

- Multi-language support (out of scope for a US-program advisor)
- User authentication (the rubric doesn't need it)
- A native mobile app (the responsive web works fine)
- Voice cloning / custom voices (Web Speech API is good enough for a demo)

Scope discipline matters. Adding things just to add them is how good projects get bloated.
