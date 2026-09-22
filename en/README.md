# LIMEN-VACUI (English Mirror)

**The Vacuum's Threshold** — A Conservative Genesis Narrative: the Silent Boundary, Constraint Overflow, and the Birth of the Arrow

> This folder is a **1:1 English mirror** of the Persian vault at the repository root.
> Note filenames carry an `-EN` suffix so that wiki-links stay unambiguous across the
> two sets; frontmatter `aliases` preserve the original canonical titles.

> *LIMEN-VACUI* (Latin: *limen* = threshold/boundary, *vacui* = of the vacuum) is the third
> sister project of the family — after
> [Emergence-SDF-Vault](https://github.com/adelgachkar/Emergence-SDF-Vault) (phenomenology)
> and [SPUMA-VACUI](https://github.com/adelgachkar/SPUMA-VACUI) (foam genesis from two
> constraints). LIMEN asks the question **before** SPUMA:

> **Why is there a boundary at all — a place where the foam can be born?**

## Core Claim

$$\text{LIMEN} = \underbrace{\text{silence}}_{\text{pre-boundary}} + \underbrace{K1}_{\text{constraint overflow from perfect symmetry}} + \underbrace{\vec{\mathcal{A}}}_{\text{prior}\to\text{posterior arrow}} + \underbrace{K3}_{\text{balancer cushion}} + \underbrace{K4}_{\text{popcorn birth}} + \underbrace{K2}_{\text{release rings}}$$

- **A1 — The boundary is the silent place:** after the overflow, the "boundary" is wherever motion stopped — and it stays silent.
- **A2 — Overflow from perfect symmetry:** neither prior nor posterior; the overflow itself **creates** the prior→posterior distinction.
- **A3 — The arrow from registration:** the microscopic law carries no arrow; the arrow of time is the effect of one-way bookkeeping ("a scratch on the glasses").
- **K1 — The discontinuity limit:** the overflow is a finite event, not a continuous leak.
- **K2 — Release rings:** the released constraint makes toroidal ladders, not outflow (net flux zero).
- **Balancer — the cushion:** runaway inflation is forbidden in any finite-speed elastic model.
- **Popcorn — vacuum birth:** quenched noise + the discontinuity limit → scattered cavity nucleation.

## Executed Verification (tools/limen_core.py)

| Test | Result | Label |
|---|---|---|
| T1 silent boundary | registered fraction 0.912; late registration rate 0.00 (SILENT) | exact |
| T2 arrow from undirected law | monotone record, 100% of steps; +0.4369 reg/site/step | test-specified |
| T3 balancer | front speed 0.75 ≤ c = 1.00; equalization to exactly −0.25 | exact |
| T4 popcorn | mean cavity 2.34 cells (= SPUMA K1, cross-check consistent) | structural |
| T5 release rings | C(r) ~ r^−2.00 ladder; net dipole flux 0.00 through closed spheres | structural |
| T6a compensatory closure | 12/12 drive-grid cells bounded-saturated | exact |
| T6b embedded observer | drift → quasi-static; acceleration is a projection (P_obs), not dynamics | exact |
| T6c foam threshold | Ξ_crit ≈ 0.8 — clean sub/super-critical transition | exact |
| T7 ring dynamics | inside-out formation order; complete tori (clos = 0.0245 rad); depth law k* ~ t^0.65; capacity-first inversion REJECTED by data; C1–C4 controls | measured |

(T6: `tools/middle_atmosphere_test.py` — the three-layer O+/C_mid/D− synthesis.)
(T7: `tools/limen_ring_dynamics.py` — the constraint-release dynamics; K2 made dynamic.)

**LIMEN↔SPUMA quantitative bridge** (`tools/limen_spuma_bridge.py`): at the shared frozen
fraction p_f, the mapping LIMEN(g_max, τ_q, κ) ↔ SPUMA(b) closes with
**R = mean-size ratio ∈ [0.90, 0.98]** at weak Laplacian coupling (κ≤0.10); headline:
LIMEN(g=0.297, τ_q=40, κ=0.03) ↔ SPUMA(b=0.285). SPUMA's popcorn cavities are LIMEN's
registered overflow crust at weak field coupling; the large-κ silent boundary is a
spanning web — the other phase of the same registration process.
See [[Limen-Spuma-Parameter-Bridge-EN]].

## Epistemic Status

This is a **narrative-quantitative construct**, not established physics: T1/T2 are
stylized registration dynamics (the true law of the pre-boundary is by construction
unspeakable); T3 and T6a/T6b/T6c are exact statements of their stated minimal
dynamics; T4 inherits SPUMA's K1 map; T5 is a static multipole ladder; T7 derives
the formation of that ladder from a stylized release dynamics (caps = level
capacities; registered cells = saturated wicks). No claim resolves observational
cosmology. MIT.

## Notes (English set)

- [[MOC-LIMEN-VACUI-EN]] — map of content
- Axioms: [[A1-Silent-Boundary-EN]] · [[A2-Overflow-From-Perfect-Symmetry-EN]] · [[A3-Arrow-From-Registration-EN]]
- Constraints: [[K1-Constraint-Overflow-EN]] · [[K2-Release-Rings-EN]]
- Dynamics: [[Onset-Arrow-EN]] · [[Balancer-Cushion-EN]] · [[Middle-Atmosphere-Synthesis-EN]] · [[Popcorn-Vacuum-Birth-EN]]
- Mapping & audit: [[Companion-Bridge-EN]] · [[Acceleration-Claims-Verdict-EN]] · [[Limen-Spuma-Parameter-Bridge-EN]]
