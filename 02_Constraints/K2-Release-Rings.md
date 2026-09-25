---
title: "K2 — Constraint-Release Rings Around the Void"
aliases: ["K2 Rings", "Toroidal Release Ladder", "K2 — حلقه‌های رهایش قید"]
created: 2026-09-21
updated: 2026-09-21
tags: [limen-vacui, constraint, rings, topological, en]
status: "canonical"
license: "MIT"
lang: "en"
---

# K2 — Constraint-Release Rings Around the Void

## Constraint 2 — Peripheral voids join a toroidal ladder; the resulting permeability envelope

> **Structural Causal Chain (LIMEN):**
> central void (released constraint) → neighboring constraints join a toroidal ladder → **the ring ladder** + a permeability envelope

The attached image (void-structured-axial-field.png) reads as follows: the constraint released at the center (the overflow site) is a **free axial defect**; the peripheral constraints, no longer level-matched to perfect symmetry, register as **toroidal strands** (donut-shaped forms around the axis). The quantitative ladder of this registration:

$$\mathcal{C}_\alpha = \oint_{\alpha} \vec{A}\cdot d\vec{\ell} = n\,\Phi_0 \;\longrightarrow\; \text{shell } k \text{ of the ladder: } \mathcal{C}_k \sim \frac{\Phi_0}{r_k^2},\quad r_k = k\,\Delta r$$

## Testable Content — T5 (executed)

`tools/limen_core.py::t5_rings` (n=8 shells, true dipole flux over closed spheres):

| Test | Result | Verdict |
|---|---|---|
| Shell ladder | C(r) ~ r^−2.00 (exactly the target) | the discrete circulation ladder = an analog of C_α = n·Φ₀ [structural] |
| Radial bleed falloff | B_r ~ r^−3.00 | dipolar — no monopole propagates [structural] |
| **Net flux through closed spheres** (R=0.5, 1, 2) | **0.00, 0.00, 0.00** | release **builds rings, not outflow** — the "permeability envelope" [structural] |

Ladder ratios: C_k/C_1 = 1, 0.250, 0.111, … (1, ¼, 1/9) — shells are similar tori with strength 1/k².

## Testable Content — T7 (release dynamics — executed)

`tools/limen_ring_dynamics.py` (v5): the release modeled as a transport dynamics on the (k, ζ) annulus — fixed source at the axial defect (k=1, axial m=0 mode), radial+poloidal diffusive transport, one-way registration on the **level** at the capacity cap cap_k = cap_1/k² (the T5 ladder as the capacity profile), registered cells as saturated Dirichlet anchors (wicks), quench complete at 5τ_q, noise sub-cap for the whole run. K=12 shells × L=256 poloidal sites.

| Test | Result | Verdict |
|---|---|---|
| Formation order (canonical point) | inside-out: t_reg from 0.34 (k=1) to 54.2 (k=11) — rank correlation > 0.85 | the ladder **grows from the defect outward** — a saturation front [measured] |
| Ring closure | max clos_k = 0.0245 rad = the grid resolution | registered strands are **complete tori, not arcs** [measured] |
| D_r sweep {0.05→3.2} | order stays inside-out at every D_r; D_r controls depth (k*: 5→12) and capture (peak 0.049 at D_r=0.8) | the capacity-first inversion hypothesis is **rejected**; one capacity-first signature survives: at D_r=3.2 only the largest-cap shell (k=1) fails to register a majority — deep tiny-cap shells bind on the first tail [measured] |
| Depth law k*(τ_q) | k* = 3, 5, 7, 12 → k* ~ t^0.65 | diffusive-front tracking with a measured excess (0.65 > 0.50) — mild capacity-ladder pre-sensitization [measured] |
| C1 — no drive (α=0) | F_k = 0 on every shell | the ladder is **a child of the overflow**, not self-organized texture [measured] |
| C2 — flat caps | depth collapses: k* = 1 (vs 12) | the ladder's role in depth and timing is isolated [measured] |
| C3 — wounded defect (localized source) | open arc (clos_k ~ 2.6–3.5 rad) vs complete tori | toroidal closure requires **the axial release channel** [measured] |
| C4 — infinite caps | capture = 0 (vs 0.030) | the envelope (registered tori) banks the released budget [measured] |

capture at the canonical point banks 0.030 of the injected budget — the remainder stays in the fluid field; at complete quench, that remainder is exactly what a later K1 overflow (a subsequent release event) would consume.

Three tool generations (v1→v5) are findings in themselves (recorded in the tool header): registration-on-accumulator with absolute noise is contaminated (C1 exposed it), a self-advancing source becomes the registration mechanism itself, and the right reading is: **a cap is a LEVEL capacity, not an instantaneous flux**; a registered cell is neither a wall nor deleted — it is a saturated wick feeding its neighbors.

## Image

![Structured void: axial chain, toroidal vector-potential rings, radial bleed, constraint region](../attachments/void-structured-axial-field.png)

## Related

- [[K1-Constraint-Overflow-EN]] — origin of the central void
- [[Companion-Bridge-EN]] — mapping to SPUMA K2
- [[MOC-LIMEN-VACUI-EN]]
