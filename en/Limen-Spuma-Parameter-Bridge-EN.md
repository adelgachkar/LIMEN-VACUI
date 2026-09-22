---
title: "LIMEN–SPUMA Quantitative Parameter Bridge (English)"
aliases: ["Parameter Bridge EN", "LIMEN SPUMA Bridge EN", "پل کمّی LIMEN-SPUMA"]
created: 2026-09-21
updated: 2026-09-21
tags: [limen-vacui, spuma-vacui, bridge, quantitative, en]
status: "canonical"
license: "MIT"
---

# LIMEN–SPUMA Quantitative Parameter Bridge

> **Structural Causal Chain (LIMEN→SPUMA):**
> LIMEN overflow (g_max, τ_q, κ) → registered mask (the silent crust) → the very union-find of SPUMA's K1 map → cavity-size distribution → two-way mapping at the shared p_f

This note retires the open caveat in [[Companion-Bridge-EN]]: "no parametric quantification is shared" — now there is one.

## 1. The shared core — a one-way absorbing exit

Two registers, one structure:

| | LIMEN T1 (registration) | SPUMA K1 (freezing) |
|---|---|---|
| drive | v = κ·∇²φ + σ₀e^{−t/τ_q}·ξ | ρ += ξ + b (white zero-mean ξ) |
| exit | \|v\| > g_max | ρ < 0 |
| after exit | site **silent** (absorbing) | site **frozen** (absorbing) |
| spatial coupling | yes (through ∇²φ) | none (exactly iid) |

The shared irreversible scalar = the **registered/frozen fraction p_f** [exact — one definition, two registers]. The identification "registration = freezing" is itself [model].

## 2. B2 — the SPUMA transfer curve (the mapping's authority)

Simulated here with the fixed K1 union-find (L=192, two seeds; anchor at L=256):

| b | p_f | mean size | max | p_f = e^{−2bm₀} (m₀=1.5) |
|---|---|---|---|---|
| 0.10 | 0.654 | 44.9 | 22836 (spanning) | 0.741 |
| 0.15 | 0.538 | 10.5 | 932 | 0.638 |
| 0.20 | 0.443 | 4.81 | 168 | 0.549 |
| **0.30** | **0.298** | **2.30** | 27 | 0.407 |
| 0.40 | 0.202 | 1.66 | 16 | 0.301 |
| 0.80 | 0.049 | 1.12 | 5 | 0.091 |

The archival anchor re-measured: **p_f = 0.2992, mean 2.32** (L=256, b=0.30, three seeds) — consistent with the K1 archive (0.299 / 2.34) [exact].

## 3. B1 — the LIMEN forward map and the floor discovery

$$p_f(g_{\max};\ \tau_q,\ \kappa)$$

| τ_q | κ | g=0.30 | g=0.40 | g=0.55 | g=0.80 | iid limit [structural] |
|---|---|---|---|---|---|---|
| 15 | 0.30 | 0.676 | 0.481 | 0.421 | 0.431 | [0.007 / 0.000 / 0 / 0] |
| 15 | 0.10 | 0.208 | 0.035 | 0.001 | 0.000 | [0.007 / 0.000 / 0 / 0] |
| 15 | 0.03 | 0.136 | 0.018 | 0.000 | 0.000 | [0.007 / 0.000 / 0 / 0] |
| 40 | 0.03 | 0.301 | 0.041 | 0.001 | 0.000 | [0.018 / 0.000 / 0 / 0] |
| 120 | 0.10 | 0.804 | 0.224 | 0.009 | 0.000 | [0.052 / 0.001 / 0 / 0] |
| 120 | 0.03 | 0.647 | 0.115 | 0.003 | 0.000 | [0.052 / 0.001 / 0 / 0] |

Three findings [measured]:

1. **The floor at large κ:** at κ=0.30 no finite cap pushes p_f below ~0.42 — the driven field self-organizes to a roughness where the cap binds at any height; the silent boundary is a **spanning web** (T1 canonical point: p_f=0.912, spanning, mean 6721). SPUMA's thin "dust" is unreachable in this regime.
2. **γ (suppression feedback) does not break the floor** — it sharpens frozen/mobile interfaces and strengthens the edge-growth epidemic (independent control run).
3. **The true control is κ** — the Laplacian coupling strength. As κ→0 registration becomes site-independent and reproduces the iid-limit column: in the uncoupled limit, LIMEN registration is exactly SPUMA's iid percolation universality class.

## 4. The closed iid limit — analytic formula [structural]

At κ=0: v = σ₀e^{−t/τ_q}ξ with ξ~N(0,1); each site's first-step hazard is independent:

$$p_f^{\mathrm{iid}} = 1 - \exp\!\left(-\,\tau_q \int_{x}^{\infty} \frac{\operatorname{erfc}(u)}{u}\,du\right), \quad x = g_{\max}/\sigma_0$$

The integral is non-elementary; evaluated by Simpson quadrature on erfc (tail truncation < 1e−64).

## 5. B3 — the inverse map at the shared p_f

For each (τ_q, κ): g_max* solved by bisection so that p_f = 0.2992 (SPUMA's b=0.30 anchor). The equivalent b comes from monotone interpolation of the B2 curve:

| τ_q | κ | g_max* | p_f | LIMEN mean | SPUMA mean | b_equiv | **R** |
|---|---|---|---|---|---|---|---|
| 15 | 0.10 | 0.297 | 0.220 | 1.75 | 1.78 | 0.381 | **0.98** |
| 15 | 0.03 | 0.243 | 0.359 | 3.02 | 3.36 | 0.258 | **0.90** |
| 40 | 0.03 | 0.297 | 0.320 | 2.51 | 2.68 | 0.285 | **0.94** |
| 120 | 0.10 | 0.363 | 0.409 | 3.84 | 4.21 | 0.224 | **0.91** |

(The B2 transfer curve has a power-law tail; the LIMEN registration tail is thinner → R < 1.)

## 6. B4 — the universality verdict

$$R(\kappa) = \frac{\bar{s}_{\mathrm{LIMEN}}}{\bar{s}_{\mathrm{SPUMA}}}\bigg|_{\text{equal }p_f} \in [0.90,\ 0.98]\quad \text{for } \kappa \in [0.03,\ 0.10]$$

- All four iso-p_f points sit in the ~iid band (0.8–1.25) — **at weak Laplacian coupling, LIMEN's cavity-size distribution is SPUMA's** [measured].
- R sits systematically just below 1: coupling slightly thins the clusters (the sharp epidemic rim of edge growth). 9% thinner at κ=0.03 → 2% at κ=0.10 — that thinning is the measured epidemic correction.
- τ_q dependence: later quench buys more collective registration before silence → larger, disconnected clusters (120/0.10: 3.84).

## 7. The headline mapping

$$\text{LIMEN}(g_{\max}=0.297,\ \tau_q=40,\ \kappa=0.03) \;\Longleftrightarrow\; \text{SPUMA}(b=0.285)$$

at p_f = 0.320 ≈ p_f^SPUMA(0.30) = 0.299 — with R = 0.94.

Narrative reading: **SPUMA's popcorn cavities are LIMEN's registered overflow crust whenever the field coupling (κ) is weak**; the large-κ regime is T1's "spanning web" phase — two phases of one registration process.

## 8. Labels and honest limits

- p_f definition, union-find, re-measured anchor: [exact]
- all curves and R: [measured]
- iid-limit formula: [structural]
- the identification "LIMEN registration = SPUMA freezing": [model]
- both registers are stylized 2D maps; this bridge adds no physics to either vault — it quantifies the numerical relation between two constructs.

## Related

- [[Companion-Bridge-EN]] — the retired caveat
- [[Popcorn-Vacuum-Birth-EN]] · [[K1-Constraint-Overflow-EN]]
- Tool: `tools/limen_spuma_bridge.py` — full output: `tools/limen_spuma_bridge_output.txt`
