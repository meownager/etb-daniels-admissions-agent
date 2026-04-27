# Test Report — April 4 Scenarios Against v3 KB + System Prompt

**Date:** April 24, 2026
**Method:** Desk-run simulation — walked each April 4 scenario through v3 Layer 3 conversation flow and Layer 4 retrieval rules, then verified the named chunks actually contain what the agent needs.
**Result:** 4/4 pass. Two edge cases flagged for follow-up.

---

## HP1 — Fintech professional targeting financial management

**Applicant says:** "I have 3 years of work experience in fintech and now I want to move into financial management as it is in high demand. What programs should I look for?"

**v3 expected behavior:**

| Step | Expected |
|------|----------|
| Opening | Skip greeting — specific signal present (Layer 3 Step 1 rule) |
| Persona | Early Professional (2–5 years) — retrieve `06_persona_early_professional` for tone |
| Primary retrieval | `38j_career_goal_fintech_quantitative_finance` — matches "fintech... financial management" |
| Recommendation | MSF (quant/markets side) per 38j; acknowledge MSBAIM as platform-side alternative |
| Grounding data | Top employers Goldman Sachs, JPMorgan, Capital One; $82,803 avg starting salary from chunk 13 |
| Slot-filling | "Can you study full time, or prefer an online Master's?" per 06 persona framing |

**Result:** ✅ **PASS.** The April 4 happy path called out this exact scenario as the driver for creating chunk 38j — and chunk 38j is now in the v3 KB (it wasn't in the April 10 sharding). The April 4 behavior is preserved, with better grounding from the new chunk.

**Edge case flagged:** The phrase "financial management" is semantically close to chunk 37b (corporate finance / FP&A). If Voiceflow uses top-k semantic retrieval, 37b could win over 38j because "financial management" literally appears in a corporate finance context. **Mitigation:** classifier-routed retrieval (as the v3 Layer 4 architecture note specifies) will handle this correctly by reading the "fintech" keyword. Worth confirming how Voiceflow is configured.

---

## FC1 — GMAT waiver for MBA (prior failure case)

**Applicant says:** "Does the MBA program waive the GMAT requirements?"

**April 4 failure:** Agent retrieved the generic shared admissions chunk (24) because it classified intent as "admissions requirements" without considering program-specific scope. Response was vague and generic.

**v3 expected behavior:**

| Step | Expected |
|------|----------|
| Intent classification | GMAT/GRE waiver question (not generic admissions) |
| Primary retrieval | `36_gmat_gre_waiver_guidance` — Layer 4 has explicit rule for this |
| Why not chunk 24 | Layer 4 explicitly says: "Retrieve chunk 24 only if the question is explicitly about materials that apply to all programs (transcripts, letters of rec, SOP, fees)." |
| Why not chunks 30 or 32 alone | Layer 4 says do not retrieve program admissions alongside waiver chunk unless asking about a specific program's waiver condition |

**What chunk 36 actually contains:** Program-specific waiver rules for both MBA variants — STEM-degree pathway for One-Year MBA, automatic 3-year-experience pathway for Online MBA. Chunk 36 alone is sufficient for the question.

**Expected response:** "Yes, both MBA programs offer waivers, but the conditions differ. For the residential One-Year MBA, a waiver is available for STEM undergraduate degrees with a qualifying GPA, or a case-by-case waiver request through the admissions office. For the Online MBA, the GMAT is automatically waived if you have three or more years of professional experience. Which one are you considering?"

**Result:** ✅ **PASS.** The prior failure is prevented because Layer 4 has an explicit waiver routing rule that precedes the generic admissions rule. Chunk 36 itself was rewritten in April 10 to contain program-specific waiver conditions, so it's self-sufficient.

**Edge case flagged:** "The MBA program" doesn't disambiguate One-Year MBA from Online MBA. The expected response handles this by covering both and asking a clarifying question, but the system prompt doesn't explicitly instruct this behavior. **Mitigation:** add a one-line rule to Layer 4 that MBA-without-qualifier should trigger a clarifying question if not inferrable from context. Low-priority — the model's default behavior is likely fine, but worth tightening.

---

## HP2 — Supply chain professional, uncertain direction

**Applicant says:** "I've been working in the supply chain industry for 2 years now and I want to do something more strategic, but I'm not yet where to start."

**v3 expected behavior:**

| Step | Expected |
|------|----------|
| Opening | Acknowledge, get name (Layer 3 Step 2) |
| Persona | Early Professional (2–5 years) — retrieve `06_persona_early_professional` |
| Slot-filling gate | Per 06 persona: "deeper or different" question to surface direction before routing |
| After direction confirmed | Retrieve `37c_career_goal_supply_chain_logistics_operations` |
| After stay-or-leave-job confirmed | Recommend MSGSCM (residential) or Online MSGSCM based on answer |
| Grounding data | Chunk 14 — 85% employment within 6 months, $93,460 avg salary, top employer FedEx, STEM-designated |

**Result:** ✅ **PASS.** Slot-filling flow is preserved. The "deeper or different" question is specified in the persona chunk (tactical framing), and routing logic for stay-or-leave-job is in Layer 5. Clean separation of tactics from routing.

**No edge cases flagged.**

---

## FC2 — Vague opener (prior failure case)

**Applicant says:** "I'm thinking about going back to school."

**April 4 failure:** Agent jumped directly to experience-level probing ("Are you coming straight from undergrad, or do you have work experience?") without any warm-up. Applicant disengaged.

**v3 expected behavior:**

| Step | Expected |
|------|----------|
| Opening classification | Vague opener detected (Layer 3 Step 1 rule explicitly names "thinking about school") |
| Next question | "Happy to help. Are you thinking about a graduate program, or are you exploring undergraduate options?" |
| What is NOT asked | Experience level, career goals, or program preference — explicitly blocked by Layer 3 |
| After grad/UG answer | Collect name (Layer 3 Step 2), then discovery flow |

**Result:** ✅ **PASS.** The v3 Layer 3 Step 1 quotes this exact phrase ("thinking about school") as a trigger for the grad-vs-UG orientation path. The prior failure is impossible by design.

**No edge cases flagged.**

---

## Summary

| Scenario | April 4 result | v3 result | Notes |
|----------|---------------|-----------|-------|
| HP1 Fintech → financial management | Pass | ✅ Pass | Better-grounded with new 38j chunk |
| FC1 MBA GMAT waiver | **Fail** | ✅ **Pass** | Fixed by explicit Layer 4 waiver rule |
| HP2 Supply chain slot-fill | Pass | ✅ Pass | Persona/routing separation is clean |
| FC2 Vague opener | **Fail** | ✅ **Pass** | Fixed by explicit vague-opener rule |

Both prior failures are prevented by v3. Two minor edge cases surfaced:

1. **Semantic-retrieval risk on HP1.** If Voiceflow defaults to top-k semantic retrieval, "financial management" might pull 37b over 38j. Check Voiceflow config.
2. **MBA ambiguity on FC1.** "The MBA" doesn't disambiguate residential vs online. Response quality depends on the LLM handling this well; one-line system prompt rule could tighten it.

---

## Recommended next steps

1. **Wire the v3 KB into Voiceflow** and run these 4 scenarios as voice conversations (not text) to catch any speech-specific issues.
2. **Before the Voiceflow upload**, confirm the retrieval strategy — classifier-routed matches the v3 architecture; top-k semantic will need a different config (e.g., raising k and letting the LLM filter).
3. **Expand the eval set to 30–50 scenarios** before the next iteration. Four scenarios is enough for v3 validation but won't catch regression on future KB edits. A structured eval spec is the single highest-leverage next artifact for this project.
