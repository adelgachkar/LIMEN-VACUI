---
title: "Unified-Register-Integration"
aliases: ["Unified Register", "One Lattice Two Exits"]
created: 2026-09-23
updated: 2026-09-23
tags: [limen-vacui, unified-register, spuma-bridge, percolation, exclusive-exits]
status: "canonical"
license: "MIT"
---

# Unified-Register-Integration (EN)

## The unified register — one lattice, two exclusive exits

> **Structural Causal Chain:**
> Live LIMEN phi field (T1) + canonical SPUMA accumulator rho (K1) → two **exclusive** one-way absorbing exits on one lattice → site competition (first channel wins) → at beta=0 the union geometry is exactly iid → at beta≠0 each rim reshapes the other's fluctuation → **negative coupling (shielding) breaks the bridge's p_f floor**.

The open question posed by the parameter bridge — "build one register instead of mapping two" — is now executed and closed. Tool: `tools/limen_spuma_unified_register.py`, full output: `tools/limen_spuma_unified_output.txt`. Persian canonical note: `07_Companion_Mapping/Unified-Register-Integration.md`.

## 1. Construction — canonical rules, verbatim

One L=192 lattice, two fluid variables, two exclusive absorbing exits:

| Channel | Dynamics (canonical, verbatim) | Exit |
|---|---|---|
| **A — LIMEN registration** | v = κ·Lap(φ) + σ₀e^(−t/τ_q)·(1+β·F_froz)·ξ, σ₀=0.15 | ‖v‖ > g_max, g_max=0.297 |
| **B — SPUMA freeze-out** | ρ += b + (1+β·F_reg)·ξ, b=0.30 (no quench — the K1 rule) | ρ < 0 |

- F_froz/F_reg = count of frozen/registered 4-neighbors; β = cross-channel feedback
- **Exclusive:** each site exits at most once — the first channel to fire wins; φ is live only on still-fluid sites
- β=0 ⇒ two canonical registers coupled only through site competition

## 2. U0 — both archives reproduced [exact]

| Metric | Unified register | Reference archive |
|---|---|---|
| Channel-A solo p_f (κ=0.03, τ_q=40) | **0.3174** | 0.320 (bridge B3) |
| Channel-B solo p_f (b=0.30) | **0.2990** | 0.299 (canonical K1) |
| iid formula at κ→0 (channel A) | 0.0194 | gap = the κ=0.03 coupling (as in the bridge) |

In isolation, each channel reproduces its own archive — the unified register distorts neither canon.

## 3. U1 — exclusive-exit identity and iid geometry at β=0 [exact]

- **Exclusive-exit identity:** p_U = p_A,ctx + p_B,ctx → **0.5236 = 0.5236** (machine precision). The naive Bernoulli-union formula 1−(1−p_A)(1−p_B) is wrong for this semantics — a methodological finding of the test itself.
- **Competition shift:** solo sum 0.6164 → measured union 0.5236 (channel B loses the sites A registered first).
- **iid benchmark:** union mean cluster size 9.04 vs TRUE iid percolation at the same p_U: 9.14 → **R(β=0) = 0.989** — iid dust geometry recovered to 1%; spanning 0/3.

## 4. U2 — dose-response: cross-feedback measured [measured]

P(B-exit | k A-neighbors) and the converse (accumulated over seeds):

| β | P(B\|k=0) | P(B\|k=1) | ratio | P(A\|k=0) | P(A\|k=1) | ratio |
|---|---|---|---|---|---|---|
| **0** | 0.3457 | 0.3431 | **1.00 (flat — independent)** | 0.3651 | 0.3616 | **0.99 (flat)** |
| **+1** | 0.4561 | 0.8226 | **1.8× (amplify)** | 0.4282 | 0.9855 | **2.3× (amplify)** |
| **−1** | 0.4107 | 0.0466 | **0.11 (9× shield)** | 0.4144 | 0.0462 | **0.11 (9× shield)** |

At β=0 the dose histogram is perfectly flat (independence, as it must be); β=+1 gives symmetric 1.8–2.3× amplification ("a frozen neighbor is a geometric tension concentrator"); β=−1 gives symmetric 9× shielding ("the silent boundary absorbs the load").

## 5. U3 — β sweep [measured]

| β | p_U | p_A,ctx | p_B,ctx | union s̄ | R_iid | spanning |
|---|---|---|---|---|---|---|
| −1.0 | 0.3700 | 0.1872 | 0.1828 | 2.02 | 0.63 | 0/3 |
| 0.0 | 0.5236 | 0.2736 | 0.2499 | 9.04 | **0.98** | 0/3 |
| +0.5 | 0.8416 | 0.5446 | 0.2970 | 1006 | 0.72 | 3/3 |
| +1.0 | 0.9333 | 0.6196 | 0.3136 | 8032 | 0.37 | 3/3 |
| +2.0 | 0.9652 | 0.6337 | 0.3315 | 35582 | 1.00* | 3/3 |

*At β=2 the lattice is nearly complete (both worlds' s̄ is set by the giant cluster). R_iid is non-monotone for β>0 — the coupled register's cluster geometry is not exactly iid at any β>0, but its "class" (spanning share) rejoins iid at strong coupling.

## 6. U4 — headline finding: negative shielding breaks the bridge floor [measured]

In the bridge's floor regime (κ=0.30) at g_max=0.297:

| Configuration | p_A | p_B,ctx | p_U |
|---|---|---|---|
| A solo | **0.9149** | — | — |
| Union β=0 | 0.7864 | 0.1510 | 0.9374 |
| Union β=+1 | 0.7635 | 0.2237 | 0.9872 |
| **Union β=−1** | 0.6749 | 0.0802 | **0.7551** |
| Union β=−1.5 | 0.6855 | 0.0923 | 0.7779 |
| Union β=−2 | 0.7856 | 0.1505 | 0.9361 |
| Union β=−3 | 0.7646 | 0.2221 | 0.9867 |

- **The shielded union (0.7551) is BELOW channel A's own solo rate (0.9149)** — adding the second exit under negative coupling *reduces* total registration. This is exactly what "the two registers are complementary" means: the soft silent boundary absorbs the hard channel's tension.
- The derived inclusion p_U ≥ max(p_A, p_B) — set membership — survives in the per-channel masks viewed as independent sets; what breaks is **not** that identity but the "floor" as an empirical lower bound on the total: the bridge's floor assumed channel independence, and that assumption is falsified by negative shielding.
- Bridge clarification: the "~0.43 floor" was the **g_max-grid** minimum (at g=0.80); at the headline g_max=0.297 the solo rate is far higher — no contradiction with the bridge.

## 7. The β-plane map — shield, transition, re-amplification [measured]

Dedicated scan (`tools/limen_beta_plane.py`, output: `tools/limen_beta_plane_output.txt`; 13 β points × 5 seeds + two follow-up probes). Structural driver: the cross-noise amplitude at a site with k active opposite-channel neighbors is **|1+βk|** — perfect-quiet bands at β=−1/k and re-amplification once 1+βk<0. Five findings:

1. **"Falling below BOTH solos" never happens on the mapped plane — and structurally cannot:** the exclusive identity p_U = p_A+p_B forces p_U ≥ max(p_A,p_B). **Honest correction of the question:** shielding must be gauged against the **hard channel's solo (A)** and the solo sum; moreover the solo-sum benchmark is intrinsically weak (exclusive competition alone keeps p_U below it).
2. **At headline coupling (κ=0.03) there is a shield PLATEAU, not a sub-solo crossing** [measured]: minimum p_U = **0.3692** on the plateau β∈[−1.25,−0.85] — above the smaller solo (0.2988). The shield onset is **gradual** (no jump; steepest slope ≈ −0.15 per unit β between β=−0.2 and −0.5; drop from 0.5232 at β=0 onto the plateau).
3. **The curve is mirror-symmetric about β=−1** — the |1+βk| signature with k=1 dominant [measured]: p_U(0)=0.5232 ≈ p_U(−2)=0.5238 and p_U(−0.5)=0.3761 ≈ p_U(−1.5)=0.3767; the k=1 shield switches off exactly at β=−2 (dose ratio P(B|k=1) = 0.999 ≈ 1) and **re-amplification** starts by β=−2.5 (p_U=0.8402, spanning 5/5).
4. **The sub-hard-solo window exists only at strong coupling (κ=0.30)** [measured]: p_U is below the A solo (0.9149) at β=−1 and −1.5 (0.7551 / 0.7779) and above it at β=−2, 0, −3 (0.9361 / 0.9374 / 0.9867) ⇒ **window ≈ β∈(−1.9, −0.2)** (crossings bracketed between −2…−1.5 and −1…0). The deep-negative recovery crosses back above the hard solo through the additive identity: both channels are still suppressed individually (0.7646 < 0.9149; 0.2221 < 0.2988) yet their sum rises.
5. **The dust→tarp geometric transition is continuous and percolation-like** [measured]: between β=0.05 (spanning 0/5, s̄=14.5, R=1.11) and β=0.10 (spanning 5/5, s̄=24.7) — s̄ grows smoothly across the whole β>0 range (9.07 → 14.5 → 24.7 → 42.5 → 71.8 → 161 → 327 → 3011 → 7569) with no first-order jump in p_U (0.5577 → 0.5942). The "sharpness" lives in the geometry (spanning switch), not in the registered rate.

## 8. Labels and honest boundaries

- Exit rules, p_f definition, exclusive identity, iid benchmark: **[exact/structural]**
- Solo rates, dose histograms, R(β), floor break: **[measured]**
- The unified dynamics itself (how the two channels couple): **[model]** — a new stylized register, not derived from either vault; it demonstrates the semantic compatibility of the two exit rules on one lattice, not the physics of either.
- Three tool generations (v1→v3) became findings themselves: a −λρ relaxation instead of the K1 drive froze the whole lattice; a shared noise envelope between channels was wrong (each channel keeps its canonical σ); the correct union identity is exclusive, not Bernoulli. A fourth generation (`limen_beta_plane.py`) caught and fixed one of its own bugs mid-run (numpy mean over a generator).
- β-map-specific labels: the prediction "quiet bands at β=−1/k and re-amplification when 1+βk<0" is structural; the crossing locations and the plateau shape are **[measured]**.

## Related

- [[Limen-Spuma-Parameter-Bridge-EN]] — the quantitative bridge (parent of this test)
- [[K1-Constraint-Overflow-EN]] · [[Companion-Bridge-EN]]
- [[MOC-LIMEN-VACUI-EN]]
