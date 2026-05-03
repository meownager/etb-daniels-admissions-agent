# Lessons Learned

Honest notes from building this. Not a victory lap — the things that surprised me, broke, or that I'd handle differently next time.

## What I underestimated

**The eval set should come first, not last.** I built the agent, then tested. Should have been the reverse: define the 4 scenarios, write expected outputs, then build to pass them. Saved me from a lot of "is this actually working?" anxiety toward the end.

**Free-tier credit caps are real.** I burned through Voiceflow's $1 free credit in one afternoon of testing + a single oversized resume upload. Had to spin up a fresh project to keep the demo alive for the prof. If I were doing this again, I'd start with a token budget per session and hard-code limits from day one.

**Voiceflow's Agent layer overrides everything.** Spent 30 minutes debugging why my Daniels playbook kept returning generic "products and services" responses. Turned out the Agent's Global Prompt has its own template text that intercepts every request before it reaches the playbook. The fix was to paste the system prompt directly into the Global Prompt, not the playbook. Not in the docs anywhere obvious.

## What worked

**Classifier-routed retrieval over top-k semantic.** The system prompt has explicit Layer 4 rules ("if the question mentions waiver, retrieve chunk 36, not chunk 24"). This is more brittle than pure semantic search, but it gave me predictable behavior on edge cases — like the FC1 GMAT waiver case that semantic-only retrieval kept botching.

**Two parallel agents, one knowledge base.** Voiceflow on the front end (great UX, fast iteration) and a Python LangChain pipeline on the back end (LangSmith integration). Same system prompt, same KB chunks. Voiceflow can't natively integrate with LangSmith, so this was the only way to satisfy both the rubric and the demo.

**Custom chat UI over the floating widget.** The floating Voiceflow bubble looked off-brand on my page. Building a native chat UI that calls the Voiceflow Dialog Manager API directly took maybe 90 minutes and gave me full control over visuals and the resume upload flow.

## What I'd do differently

**Set up branch protection and admin bypass on day one.** I added it midway, which meant my own pushes started getting rejected at 1am. Not the time you want to be debugging GitHub rules.

**Compress before sending, not after.** The first version of resume upload sent the full extracted PDF text (2000+ chars) to Voiceflow as a chat message. That alone burned a chunk of my free credits. The fix was a regex-based summarizer that pulls only key fields (name, experience, role, skills, education) and sends ~500 chars instead. ~60% token reduction per upload.

**Build the eval set in a structured doc, not in my head.** I had the four scenarios in a Slack note. Should have been a CSV with `id, input, expected_chunk, expected_behavior, pass/fail` columns from the start. Would have made the LangSmith tracing more useful too — could have programmatically scored.
