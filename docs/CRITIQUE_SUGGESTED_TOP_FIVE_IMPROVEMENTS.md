# Critique — Suggested top five improvements

This document tracks the five prioritized changes from the ChatGPT critique (see `CRITIQUE.md`). We implement them in this order: **1 → 3 → 4 → 2 → 5**.

---

## Summary

| # | Change | Effort | Impact |
|---|--------|--------|--------|
| 1 | Rename "Prompt technique" → "Response style" + user-friendly labels | Low | High (non-technical users) |
| 2 | Hide or simplify temperature (e.g. Expert mode or 3 presets) | Low–medium | Medium (less confusion, fewer bad runs) |
| 3 | Move practice type into system prompt (embed category) | Medium | High (better, more consistent answers) |
| 4 | CoT: internal reasoning only, output final answer | Low (prompt edit) | Medium (cleaner answers, best practice) |
| 5 | Add rate limiting (e.g. per session) | Medium | High for any real/deployed use |

**Order:** Do **1, 3, and 4** first (naming, system-prompt category, CoT wording). Then **2** (temperature), then **5** (rate limiting).

---

## Implementation status

- [x] **1.** Rename "Prompt technique" → "Response style" + user-friendly option labels
- [x] **3.** Move practice type into system prompt (embed category dynamically)
- [x] **4.** CoT: internal reasoning only, output final answer
- [x] **2.** Hide or simplify temperature (Expert mode or presets)
- [x] **5.** Add rate limiting (e.g. per session)

---

## Updated final score (follow-up critique)

After implementing the five improvements above, ChatGPT was asked to run a new critique. Below is the updated assessment.

### 🎯 Updated final score

| Category | Score |
|----------|-------|
| **Usability** | 8.5 / 10 |
| **Security** | 7 / 10 |
| **Prompt engineering** | 8 / 10 |

**⭐ Overall MVP assessment: 8 / 10**
