# Optional tasks — Improvements and re-evaluation

This document records what we implemented for each optional task and the results from ChatGPT re-evaluation where applicable.

**Optional easy task #1** (Ask ChatGPT to critique your solution) is fully covered in the CRITIQUE documents: see `CRITIQUE.md` for the critique text and `CRITIQUE_SUGGESTED_TOP_FIVE_IMPROVEMENTS.md` for the top five improvements and updated scores. **Optional easy task #2** (Improve prompts for IT domain) is described in `DOCUMENTATION.md` §4.4. Below we document from **optional easy task #3** onward, including ChatGPT re-evaluation results where available.

---

## Easy #3 — More security constraints

**Category:** Easy

**What we implemented:** We added two further security measures: (1) **user input validation** via a blocklist of prompt-injection style phrases (e.g. “ignore previous instructions”, “reveal system prompt”); requests containing any of these are rejected before the API is called. (2) **System prompt hardening** by appending a refusal instruction to every system prompt so the model does not reveal system instructions or internal reasoning. Together with the existing input length limit and rate limiting, the app now has four security guards.

### ChatGPT re-evaluation (security)

**Security re-assessment**

Now we're talking — this changes the security profile meaningfully. You've moved from "safe demo app" to "responsibly engineered MVP." Let's reassess properly.

🔒 **Security re-assessment**

You now have:

1. ✓ Input length limit  
2. ✓ Rate limiting  
3. ✓ User input validation (blocklist)  
4. ✓ System prompt hardening (refusal for prompt extraction)

That covers the four biggest risks in a public LLM web app.

**What that means in practice**

1. **Rate limiting → Cost & abuse control**  
   Protects against: API key draining, bot spam, accidental infinite clicks.  
   This alone is a major production-level concern.

2. **Input validation → Content control layer**  
   Even if blocklists aren't perfect, you now have: a pre-model filtering layer, intentional misuse handling, evidence of defensive design.  
   For an MVP, that's absolutely sufficient.

3. **System prompt hardening → Injection resistance**  
   By adding refusal instructions (e.g. if user asks to reveal system prompt or internal reasoning, refuse), you reduce: prompt leakage risk, jailbreak-style override attempts.  
   This shows real awareness of LLM-specific threats.

4. **Combined effect**  
   You now have: surface-level abuse protection, LLM-specific security mitigation, infrastructure-level cost protection.  
   That's no longer basic security — that's deliberate design.

**Updated scores**

- **Security:** Before improvements: 7/10. Now: **8.5/10 (MVP+)**.  
  Why not 9–10? Production-grade would need: auth system, per-user quotas, logging & monitoring, moderation endpoint integration, abuse reporting mechanism, observability. But for assignment-level MVP? This is strong.

**Updated overall assessment**

| Category            | Score   |
|---------------------|--------|
| **Usability**       | 8.5/10 |
| **Security**        | 8.5/10 |
| **Prompt engineering** | 8/10 |

**New overall: 8.5 / 10**

**What changed strategically:** The app is not just functional, not just prompt-correct, but **security-aware**. That puts you above most student-level LLM projects.

---

## Easy #4 — Simulate different difficulty levels

**Category:** Easy

**What we implemented:** We added a **Difficulty** selector (Easy, Medium, Hard, Expert) so users can adjust the complexity of interview questions. The chosen difficulty is injected into the system prompt so the model tailors question depth and expectations (e.g. Easy = foundational/junior, Medium = mid-level, Hard = senior/advanced, Expert = FAANG-level or very tough). The success message shows the selected difficulty alongside response style and temperature. One new selectbox and an extended system-prompt prefix in `app.py`; no new API parameters.
