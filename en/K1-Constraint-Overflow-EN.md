---
title: "K1 — Constraint Overflow and the Discontinuity Limit"
aliases: ["K1 Overflow", "LIMEN K1", "K1 — سرریز قید و حد انفصال"]
created: 2026-09-21
updated: 2026-09-21
tags: [limen-vacui, constraint, numerics, en]
status: "canonical"
license: "MIT"
---

# K1 — Constraint Overflow and the Discontinuity Limit

## Constraint 1 — Constraint overflow and the vacuum discontinuity limit

> **Structural Causal Chain (LIMEN):**
> perfect symmetry → constraint accumulation → **overflow** → silent boundary (the discontinuity limit) + a potential-bearing posterior

The two constraints inherited from SPUMA-VACUI play the opening roles here: the **vacuum discontinuity limit** (registration at the threshold, no continuous transition) and the **absence of infinite polarization-tension continuity** (a cap, g_max). The narrative adds: these constraints accumulate until they **overflow** — and the overflow is the birth of the boundary.

## Testable Content — T1 (executed)

`tools/limen_core.py::t1_silence_overflow` — a register with a velocity cap + drive quench:

| Quantity | Value |
|---|---|
| Registered fraction (silent boundary) | **0.912** |
| Registration rate after the quench (last 100 steps) | **0.00** — total silence |
| Converse (sustained noise, no quench) | steady duty ≈ 0.95 — does **not** build a silent boundary (rejected) |

**Closing statement:** the overflow is a finite generative event; the "boundary" is where motion stopped — and it stays silent afterwards. [exact — dynamics with an absorbing state]

## Related

- [[A1-Silent-Boundary-EN]] — interpretation
- [[Popcorn-Vacuum-Birth-EN]] — the posterior consequence
- [[Companion-Bridge-EN]] — the SPUMA counterpart
- [[MOC-LIMEN-VACUI-EN]]
