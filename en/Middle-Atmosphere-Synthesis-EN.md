---
title: "Middle-Atmosphere Synthesis — O+/Cmid/D− Three-Layer Dynamics"
aliases: ["Middle Atmosphere", "Compensatory Closure", "Three-Layer System", "جوّ میانی"]
created: 2026-09-21
updated: 2026-09-21
tags: [limen-vacui, balancer, three-layer, numerics, en]
status: "canonical"
license: "MIT"
---

# Middle-Atmosphere Synthesis — the O+/C_mid/D− Three-Layer System

## Origin and placement

The two "Middle-Atmosphere Inflation Dynamics" documents (EN v3.1.0-Canonical-Synthesis and its Persian rendering) present a three-layer formalism that is **exactly LIMEN's balance cushion in formal dress**:

| Source document (SDF v3.1.0) | LIMEN equivalent | Mapping verdict |
|---|---|---|
| Generative core O+ — positive pressure, density overflow (A_drive) | "the leading front in prior pressure" — the released compression of K1 | ✅ exact |
| Distal boundary D− — negative pressure, pull (A_bdry) | the posterior front — the registered silent boundary of A1 | ✅ exact |
| Middle atmosphere C_mid — constraint buffer, compensation (A_comp) | the balance cushion (04_Balancer) | ✅ exact |
| Three-component relation A = A_drive − A_comp + A_bdry | the two elastic propositions of T3 (cone + equalization) | ✅ structural |
| "prevents divergence and unchecked explosion" | the infinite-inflation prohibition | ✅ now quantitative (T6a) |
| Ξ_mid > Ξ_crit → local discharge → **vacuum foam** | popcorn birth (05_Popcorn) | ✅ now quantitative (T6c) |
| "accelerating atmospheric inflation" for an observer inside C_mid | — | ⚠️ inconsistent with the minimal dynamics (T6b — below) |

This synthesis closes the gap between the LIMEN narrative and the SDF formalism: the narrative said "cushion", the document says "compensatory closure" — **the same thing**, and both now carry numerical support.

## Testable Content — T6 (executed)

`tools/middle_atmosphere_test.py` — a damped elastic membrane with two opposing fronts; A_comp implemented as damping Γ + velocity saturation:

### T6a — Compensatory closure (bounded expansion)

A 4×3 grid of drive rates (ξ_drive, ξ_pull ∈ {0.05..0.40}):

| Quantity | Result |
|---|---|
| Bounded cells | **12/12** — "bounded-saturated" in all |
| Late-time drift rate | ≤ 0.005 sites/time; slightly negative (recoil) at high drives |
| Max \|v\| | always below the cap XI_CAP=1.5 — saturation active |

**Closing statement:** the three-component relation with a saturating A_comp forbids unbounded expansion in every sub-threshold regime. [exact — dynamics]

### T6b — An observer embedded in the middle atmosphere

The two fronts do **not** recede from a shell-comoving observer (width 410→407, drift →0):

- Front drift relaxes toward zero: −0.0061 → −0.0004; the buffer is **quasi-static** at long times [exact]
- **Sharp finding (super-critical probe):** in the foam-active regime (Ξ > Ξ_crit, nucleation on), tension discharge lets the fronts pass through each other (width → negative) — i.e. "accelerating atmospheric inflation" does **not** follow from the minimal dynamics; the document's claim is an observational-projection (P_obs) claim, not an automatic consequence of the three-layer balance. [exact — within this very architecture]
- Consistent reading: the document itself states that isotropy and the spherical shape are "a secondary observational mapping (P_obs), not fundamental geometry" — T6b takes that honesty one level up: the *acceleration* too is a projection, not buffer dynamics.

### T6c — Foam nucleation threshold

A sweep of ξ_drive ∈ {0.1..3.0}:

| ξ_drive | Nucleations | First event |
|---|---|---|
| 0.10–0.40 | 0 | — |
| 0.80 | active | t=223 |
| 3.00 | active | t=184 |

**Ξ_crit ≈ 0.8** (in units of damping Γ=0.05 and the velocity cap 1.5) — a clean transition: below it tension accumulates; above it tension discharges locally = foam. [exact — dynamics] This is precisely the document's Ξ_mid > Ξ_crit statement, now tied to a number, and it gives LIMEN's popcorn birth a second trigger.

## Relation to earlier tests

- **T3** (cushion): the cone c=1 and equalization to −0.25 — T6a is its dynamical generalization
- **T4** (popcorn): in SPUMA, birth came from quenched noise; here the same nucleation is driven by **super-critical transfer rates** — two triggers, one phenomenon
- **T1** (boundary silence): D− in this synthesis is the silent boundary exerting negative pressure

## Epistemic Status

T6a/T6c are exact (dynamics with explicit parameters); T6b confirms the mapping of "observed acceleration" to a projection and registers the minimal-dynamics rejection — this is this note's **point of difference** from the source document. No observational-cosmology claim.

## Related

- [[Balancer-Cushion-EN]] — the narrative form of the same mechanism
- [[Popcorn-Vacuum-Birth-EN]] — the super-critical consequence
- [[Acceleration-Claims-Verdict-EN]] — the verdict on document 3 (the dark claims)
- [[Companion-Bridge-EN]] · [[MOC-LIMEN-VACUI-EN]]
