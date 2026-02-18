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

- [ ] **1.** Rename "Prompt technique" → "Response style" + user-friendly option labels
- [ ] **3.** Move practice type into system prompt (embed category dynamically)
- [ ] **4.** CoT: internal reasoning only, output final answer
- [ ] **2.** Hide or simplify temperature (Expert mode or presets)
- [ ] **5.** Add rate limiting (e.g. per session)

---

*Details and notes for each item can be added below as we implement.*
