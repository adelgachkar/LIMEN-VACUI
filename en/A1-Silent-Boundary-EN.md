---
title: "A1 — The Boundary Is the Silent Place"
aliases: ["A1 Silence", "Silent Boundary Axiom", "A1 — مرز، محل سکوت است"]
created: 2026-09-21
updated: 2026-09-21
tags: [limen-vacui, axiom, en]
status: "canonical"
license: "CC-BY-4.0"
---

# A1 — The Boundary Is the Silent Place

## Axiom 1 — The boundary is where silence lives

> **Structural Causal Chain (LIMEN):**
> pre-boundary (silence) → constraint overflow (K1) → the registered boundary = silent → posterior being (foam, arrow, rings)

No statement about the "law" of the pre-boundary can be written — the pre-boundary collapses into whatever predicate is asserted about it. The only sayable things are **negative**: the pre-boundary has neither a prior nor a posterior; the prior/posterior distinction is itself born at the boundary, not fed into it. For this reason the axiom names the pre-boundary with a single word — **silence**: not an active void, but the **unspeakability of registration**.

After the overflow (K1), the "boundary" is no longer a transcendent object — it is wherever motion **stopped**. Quantitatively: a site/region whose velocity demand exceeds the overflow cap leaves the fluid register and goes silent (an absorbing state).

## Testable Content — T1 (executed)

`tools/limen_core.py::t1_silence_overflow` (noise quench τ_q=120, cap g_max=0.4):

| Quantity | Value | Meaning |
|---|---|---|
| Registered (silent) boundary fraction | **0.912** | one-shot genesis, not continuous leaking |
| Registration rate after the quench | **0.00** | the boundary is silent after the event |
| Duty during the quench | high → decay | the overflow is an onset event |

The converse proposition was also tested and **rejected**: with sustained noise, a continuous velocity cap builds a self-organizing rough register (steady duty ≈ 0.95) — i.e. "overflow without quench" does **not** make a silent boundary; quenching of the drive is a necessary component of the narrative. [test-specified:passed]

## Related

- [[K1-Constraint-Overflow-EN]] — quantitative form of the overflow
- [[A2-Overflow-From-Perfect-Symmetry-EN]] — why the overflow comes from perfect symmetry
- [[MOC-LIMEN-VACUI-EN]] — the map
