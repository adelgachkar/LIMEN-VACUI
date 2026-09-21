---
title: "K2 — Constraint-Release Rings Around the Void"
aliases: ["K2 Rings", "Toroidal Release Ladder", "K2 — حلقه‌های رهایش قید"]
created: 2026-09-21
updated: 2026-09-21
tags: [limen-vacui, constraint, rings, topological, en]
status: "canonical"
license: "CC-BY-4.0"
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

## Image

![Structured void: axial chain, toroidal vector-potential rings, radial bleed, constraint region](../attachments/void-structured-axial-field.png)

## Related

- [[K1-Constraint-Overflow-EN]] — origin of the central void
- [[Companion-Bridge-EN]] — mapping to SPUMA K2
- [[MOC-LIMEN-VACUI-EN]]
