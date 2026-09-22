---
title: "Balancer Cushion — Two-Front Compression and the Forbidden Runaway"
aliases: ["Balancer", "Infinite Inflation Forbidden", "بالشتک بالانس"]
created: 2026-09-21
updated: 2026-09-21
tags: [limen-vacui, balancer, numerics, elastic, en]
status: "canonical"
license: "MIT"
---

# Balancer Cushion — Two-Front Compression and the Forbidden Runaway

## The balance cushion; the infinite-inflation prohibition

> Narrative: "the leading front in prior pressure and the posterior front of middle compression can reach a balance cushion — and forbid infinite inflation"

Elastic formulation: compression released into an elastic sheet of modulus K spreads out; the compressed middle front is a **cushion** — not an engine. Two testable propositions:

1. **Causal cone:** no signal outruns the elastic speed c=√K (CFL-bounded dynamics).
2. **Equalization:** released compression settles to uniform equilibrium; it does not run away.

## Testable Content — T3 (executed)

`tools/limen_core.py::t3_balancer` (leapfrog, K=1, dt=0.4, pinned ends, L=256):

| Quantity | Value | Verdict |
|---|---|---|
| Max front speed | **0.750 ± 0.000** sites/step | does not exceed the elastic cone c = 1.00 [exact] |
| CFL | 0.40 ≤ 1 — stable | |
| Final mean s | **−0.25000** (exact equilibrium) | released compression **settles**; no drift [exact] |

**Closing statement:** "infinite inflation" is a forbidden proposition in any finite-speed elastic model — the balance cushion is just another name for these two statements. [exact — a consequence of the equation structure]

## Mapping to the narrative

- "leading front in prior pressure" = the compression wave released from the compressed region
- "posterior front of middle compression" = the equalization tail
- "forbidding infinite inflation" = the causal cone (proposition 1)

## Related

- [[A3-Arrow-From-Registration-EN]] — the direction of the fronts
- [[Middle-Atmosphere-Synthesis-EN]] — the three-layer formalism and the T6 tests (the dynamical generalization of this note)
- [[Popcorn-Vacuum-Birth-EN]] — what is born inside the cushion
- [[MOC-LIMEN-VACUI-EN]]
