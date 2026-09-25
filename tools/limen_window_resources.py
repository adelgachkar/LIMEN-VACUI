# -*- coding: utf-8 -*-
"""
RESOURCE MAP OF THE HONEST WINDOW [d_det, d_class] (Aligned-Protocol S5).

The S5 honest window is bounded by two edges of DIFFERENT nature:
  * d_det   (lower edge) — a NOISE edge: SNR(d) = R(d)/sigma_eff(d) crosses
            the gate 10. Under the v5 deterministic one-sided law the whole
            detection noise is the FROZEN-ANCHOR estimation error.
  * d_class (upper edge) — an EPISTEMIC edge: the closed form rel(d) = d/(m+d)
            with the FIXED choice eps=0.1. No noise enters it.

Structure [exact within the model — and the tool's own history proves it]:
  v5 dynamics: steps below rho_0 are rejected BEFORE the extra drift is added,
  so the registered mask is the d=0 mask BIT-FOR-BIT (the freeze-out gauge
  identity) and per (seed, frame):
      chi(seed, frame, d) = C(seed) + d,   C frame-INDEPENDENT [gauge clause]
  => dev entries = d + e(seed), e = C - Cbar:  R(d) = <|d + e|> is a
  DETERMINISTIC function of the realized seed errors; sigma_eff = nat_sem =
  std(C)/sqrt(S); the +Delta/-Delta pooling adds NOTHING (frames identical),
  so S_eff = S, not 2S. Detection edge: d_det(S,N) = the d where R(d) =
  gate * nat_sem ~ gate * std(C)/sqrt(S), std(C) ~ 1/sqrt(N*w).
  Tool history (E4 lessons): v1 injected GAUSSIAN extra noise instead of the
  deterministic drift — a different law: conditioning on the edge converts it
  into a Mills-scale jump (R ~ 0.45 at any d) — the battery caught it. v2 let
  the mask move with d (edge re-evaluated after the bias) — also not v5.

Conventions identical to limen_residue_param_map.py (v5 register):
b=0.30, tau_q=40, N=4096, window=60, rho_0=0; gauge clause (relabel + Delta,
edge follows); frozen symmetric anchor (same seeds); R/T0 with eps=0.1;
SNR gate 10. Labels: [exact]/[exact model] for identities and closed forms,
[measured] for Monte-Carlo outcomes, [protocol-mirror, conceptual] for
interpretation. Provenance: LIMEN tools/limen_residue_test.py (v5) +
tools/limen_residue_param_map.py (d_class = 0.0686, d_det ~ 0.0067).
"""
import os
import sys
import numpy as np
from math import erf, exp, sqrt, pi

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# ---- canonical v5 register constants ----
B_DRIFT   = 0.30
TAU_Q     = 40            # (window/tau_q: post-quench walk is drift-dominated;
N_STEPS   = 60            #  tau_q stays part of the frozen register contract)
N_WALKERS = 4096
SEEDS     = 8
RHO_0     = 0.0
FRAME_SHIFTS = (+0.25, -0.25)

EPS       = 0.1
SNR_GATE  = 10.0

# ---- closed-form constants [exact model] (limen_residue_param_map) ----
_PHI_B   = exp(-0.5 * B_DRIFT**2) / sqrt(2.0 * pi)
_PHILO_B = 0.5 * (1.0 + erf(B_DRIFT / sqrt(2.0)))
MILLS    = _PHI_B / _PHILO_B          # m = phi(b)/Phi(b) = 0.61722
D_CLASS  = EPS * MILLS / (1.0 - EPS)  # 0.0686 — pinned by eps, NOT by noise

# ---- per-seed registered content C(seed) at d=0 (native = rectified-with-d=0:
# same mask, same entries). Frame-independent by the gauge clause -> one field
# per seed per budget; everything else is algebra. ----
_C_CACHE = {}


def _c_of(seed, n_w):
    key = (n_w, seed)
    if key in _C_CACHE:
        return _C_CACHE[key]
    rng = np.random.default_rng(seed)
    steps = rng.normal(B_DRIFT, 1.0, size=(n_w, N_STEPS))
    s_reg = np.where(steps < RHO_0, 0.0, steps - RHO_0)
    c = s_reg[s_reg > 0].mean()
    _C_CACHE[key] = c
    return c


def _native(n_w, seeds):
    """Frozen symmetric anchor (same seeds): (mean, sem)."""
    chi = np.array([_c_of(s, n_w) for s in range(seeds)])
    return chi.mean(), chi.std(ddof=1) / sqrt(seeds)


def measure(d, n_w, seeds, nat):
    """Post-swap v5 statistics at depth d: (R, sigma_eff).

    dev pool: 2*seeds entries (both frames, same-seed frozen anchor mean).
    Under the deterministic law every dev entry is EXACTLY d + e(seed);
    R(d) = <|d+e|> is deterministic given the seeds; sigma = std(e)/sqrt(2S)
    < nat_sem = std(C)/sqrt(S) => sigma_eff = nat_sem (the anchor floor).
    Near zero the |.| folding inflates R (E|e| = sqrt(2/pi)*std(C)); the
    operational d_det is the crossing of the FULL statistic — v5's meaning.
    """
    nat_mean, nat_sem = nat
    e = np.array([_c_of(s, n_w) for s in range(seeds)]) - nat_mean
    dev = np.concatenate([e + d, e + d])       # frames bit-identical [gauge]
    R = abs(dev).mean()
    sigma = dev.std(ddof=1) / sqrt(len(dev))
    sigma_eff = max(sigma, nat_sem, 1e-12)
    return R, sigma_eff


def find_d_det(n_w, seeds, nat, d_guess):
    """Bisection on SNR(d) = SNR_GATE (R(d) deterministic per seed set)."""
    a = max(0.2 * d_guess, 1e-6)
    b = 4.0 * d_guess
    for _ in range(40):
        mid = 0.5 * (a + b)
        R, se = measure(mid, n_w, seeds, nat)
        if R / se > SNR_GATE:
            b = mid
        else:
            a = mid
        if (b - a) <= 1e-4 * b:
            break
    return b


def main():
    W = 72
    print("=" * W, flush=True)
    print("HONEST-WINDOW RESOURCE MAP — which edge moves with compute?")
    print("register: v5 (b=%.2f, N=%d, w=%d, seeds=%d); deterministic one-sided"
          % (B_DRIFT, N_WALKERS, N_STEPS, SEEDS))
    print("law: chi = C(seed) + d [exact, gauge identity]; SNR gate %.0f;"
          % SNR_GATE)
    print("d_class = %.4f [exact model, pinned by eps=%.2f]" % (D_CLASS, EPS))
    print("=" * W, flush=True)

    # ---- [1] theory -------------------------------------------------------
    print("\n[1] structure of the two edges [exact model]:", flush=True)
    print("    d_det(S,N) ~ gate * std(C)/sqrt(S), std(C) ~ 1/sqrt(N*w)")
    print("        -> noise edge: MOVES with compute (1/sqrt(S*N*w) law).")
    print("    d_class = eps*m/(1-eps) = %.4f" % D_CLASS)
    print("        -> epistemic edge: PINNED by the choice eps — does NOT move.")
    print("    -> resources push the LOWER edge down: the SILENT zone")
    print("       [0, d_det] shrinks (what compute buys) while the honest")
    print("       window [d_det, d_class] WIDENS from below; its right edge")
    print("       stays pinned. Closing BOTH edges is the epistemic choice")
    print("       eps* = rel(d_det) = d_det/(m+d_det), never a compute purchase.")

    # ---- [2] canonical anchor + k calibration ----------------------------
    print("\n[2] canonical anchor + gain calibration [measured]:", flush=True)
    nat0 = _native(N_WALKERS, SEEDS)
    print("    d=0 health: native anchor = %.5f +- %.2e (s.e.m.)  [v5: 0.91720]"
          % nat0)
    R0, se0 = measure(0.0, N_WALKERS, SEEDS, nat0)
    print("    frame-made side at d=0: R(0) = %.5f (R/T0 = %.4f [v5: 0.0024]),"
          % (R0, R0 / MILLS))
    print("    SNR = %.1f [v5: 2.2]" % (R0 / se0))
    d0 = find_d_det(N_WALKERS, SEEDS, nat0, d_guess=0.0067)
    k0 = SNR_GATE / d0
    print("    d_det(canonical 8x4096) = %.5f  ->  k0 = %.0f per unit d"
          % (d0, k0))
    print("    [v5 map: d_det ~ 0.0067, SNR ~ 1488 per unit d]", flush=True)

    # ---- [3] the (S, N) grid ---------------------------------------------
    print("\n[3] (S, N) grid [measured] — d_det measured, d_class pinned:", flush=True)
    print("    %-6s %-6s | %-9s | %-9s | %s"
          % ("S", "N", "d_det", "d_class*", "window width (class - det)"))
    grid = [(4, 1024), (8, 1024), (16, 1024),
            (8, 4096), (32, 4096),
            (16, 16384), (64, 16384),
            (32, 65536), (64, 65536)]
    rows = []
    for S, N in grid:
        nat = _native(N, S) if (N, S) != (N_WALKERS, SEEDS) else nat0
        d_guess = d0 * sqrt((SEEDS * N_WALKERS) / (S * N))
        d_det = find_d_det(N, S, nat, d_guess)
        k = SNR_GATE / d_det
        d_cls_star = EPS / k
        rows.append((S, N, d_det, d_cls_star))
        print("    %-6d %-6d | %-9.5f | %-9.5f | %.5f"
              % (S, N, d_det, d_cls_star, D_CLASS - d_det), flush=True)

    # ---- [4] power law over the noise edge --------------------------------
    print("\n[4] noise-edge power law [measured]: d_det ~ A * (S*N*w)^(-gamma):")
    X = np.array([S * N * N_STEPS for S, N, _, _ in rows], dtype=float)
    y = np.array([d for _, _, d, _ in rows])
    slope, intercept = np.polyfit(np.log10(X), np.log10(y), 1)
    gamma, amp = -slope, 10.0 ** intercept
    pred = amp * X ** (-gamma)
    print("    gamma = %.3f  (theory: 0.5) ; A = %.4g"
          % (gamma, amp))
    print("    max |log residual| = %.4f dex"
          % np.max(np.abs(np.log10(y) - np.log10(pred))))

    # ---- [5] the closing standard: eps* must TRACK the budget -------------
    print("\n[5] the closing standard per budget [exact model + measured d_det]:")
    print("    eps*_close = d_det/(m+d_det) — the epistemic choice that makes")
    print("    the classification edge MEET the detection edge (eps=0.1 is")
    print("    pinned; its window never closes at any feasible budget):")
    print("    %-6s %-6s | %-10s %-12s" % ("S", "N", "d_det", "eps*_close"))
    for S, N, d_det, _ in rows:
        print("    %-6d %-6d | %-10.5f %-12.5f"
              % (S, N, d_det, d_det / (MILLS + d_det)))
    print("    law: eps*_close ~ (A/m)*(S*N*w)^-1/2 — the affordable standard")
    print("    tightens like a noise floor; price of a FIXED standard:")
    for e_t in (0.01, 1e-3, 1e-4):
        d_c = e_t * MILLS / (1.0 - e_t)
        SNw = (amp * (1.0 - e_t) / (e_t * MILLS)) ** 2
        print("      eps*=%.0e -> d_det=%.4f, S*N*w=%.2e (S*N=%.2e)"
              % (e_t, d_c, SNw, SNw / N_STEPS))

    # ---- verdict -----------------------------------------------------------
    d_big = max(d for _, N, d, _ in rows if N == 65536)
    print("\n" + "=" * W)
    print("VERDICT:")
    print("  1. the two edges MOVE DIFFERENTLY [measured vs exact model]:")
    print("     d_det (noise) ~ A*(S*N*w)^-%.3f — recedes with compute;" % gamma)
    print("     d_class (epistemic) pinned by eps at %.4f — does NOT move." % D_CLASS)
    print("  2. compute buys DETECTION, never classification: the silent zone")
    print("     [0, d_det] shrinks [%.5f -> %.5f]; the honest window" % (d0, d_big))
    print("     [d_det, d_class(0.1)] WIDENS from below: width %.4f -> %.4f."
          % (D_CLASS - d0, D_CLASS - d_big))
    print("  3. closing BOTH edges is an epistemic choice that must TRACK the")
    print("     budget: eps*_close = d_det/(m+d_det): %.4f (canonical) -> %.5f"
          % (d0 / (MILLS + d0), d_big / (MILLS + d_big)))
    print("     at the best cell — the affordable standard tightens like a")
    print("     noise floor, (S*N*w)^-1/2; each decade = x100 compute")
    print("     (eps*=1e-4: S*N*w ~ %.1e)." % ((amp / (1e-4 * MILLS)) ** 2))
    print("labels: gauge identity chi=C+d, d_class form, S_eff=S [exact model];")
    print("grid, gamma, eps* table [measured]; interpretation")
    print("[protocol-mirror, conceptual]. E4 lessons registered: v1 injected")
    print("   Gaussian noise instead of the deterministic drift (a different")
    print("   law: Mills-scale jump, caught by the battery); v2 let the mask")
    print("   move with d (edge re-evaluated) — also not v5.")


if __name__ == "__main__":
    main()
