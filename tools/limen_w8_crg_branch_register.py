# -*- coding: utf-8 -*-
"""
W8: THE CRG BISTABLE BRANCHES MEET THE UNIFIED REGISTER — exit reading of
each stable branch (OQ-C4-2, banked in CRG-Flux 00_Index/Family-Register-
Mapping §5).

The question (OQ-C4-2, verbatim): "Does a bistable CRG parameter set (the
~2% region outside the sufficient condition) map to a definite exit of the
LIMEN unified register?" — conceiv_able tool: "run the CRG battery at
bistable points, feed each stable branch's x* as LIMEN seed density, read
the exit channel."

Design (labels per family contract):
  [exact]  CRG equilibrium branch computation (Coupled Dynamical Equations
           §2-3): solve the quartic of the vault's own battery, classify
           each branch with the Routh-Hurwitz battery (verified there at
           every stable branch, 1e5 draws, zero violations).
  [exact]  branch -> seed mapping DENSITY-preserving (E4 discipline — the
           variable that moves the unified register's exit rates is the
           field AMPLITUDE, not a re-labeled seed):
             channel A: amp = sigma0 * (1 + eta*(x - 0.5)) with the
               reference anchored at x=0.5 == canonical amp 0.1, eta=3
               => amp ranges 0.025..0.175 over x in [0,1];
             channel B: rho0_mean = 1.5 + delta*(x - 0.5), delta=1
               (margin at the canonical buffer layer).
  [measured] exit reading: for each branch (both branches for bistable
           parameter sets) run the unified register at beta=0 (competition
           only), read p_A^ctx, p_B^ctx and p_U, and register WHICH exit
           each branch feeds and whether the two branches of one parameter
           set split the exit channels.

Honest boundary (inherited from Unified-Register-Integration §9): the
unified dynamics is [model]; every rate comparison is [measured]; the
CRG branch classification is [exact]; the branch->seed identification
is the [model] choice of this test, registered as such.

Ward neutrality: no pre-boundary proposition — the CRG side is a
boundary-side dynamical system; the pre-boundary stays silent (S1/S2).
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from limen_spuma_unified_register import unified_register, mask_stats

L = 192
SEEDS = (11, 12, 13)
STEPS = 800
PATIENCE = 60
QUIET_THR = 3e-4
BETA = 0.0          # competition-only coupling (the registered iid point)

# CRG reference parameters (Coupled Dynamical Equations, the recorded
# three-root example). W8 re-computation (corrected quartic + corrected
# Jacobian + det(J)<0 stability sign) REPRODUCES the vault note exactly:
#   x* = {0.0029 stable, 0.0994 saddle, 0.9449 stable} — bistable, as
#   registered. The earlier W8 run's failures were the tool's own bugs
#   (E4): a wrong quartic coefficient set and a reversed det sign.
CRG_REF = dict(alpha1=0.0252, alpha2=0.042, beta2=40.85,
               gamma1=0.22, gamma2=0.215, lam=0.0222, mu=15.27)
# Frequency context (20,000-draw grid, corrected classification):
#   multi-root 3.02% of outside-sufficient draws; BISTABLE 0.37% overall
#   (74/20000; 25% of multi-root draws). E4 refinement of the vault note:
#   "on average two of the equilibria are linearly stable" in multi-root
#   draws is REFUTED — the mean is 1.25 stable equilibria per multi-root
#   draw; bistability is real but the minority case.
# W8 calibration:
ETA_A = 3.0         # channel A amplitude swing (x=0.5 -> canonical 0.1)
DELTA_B = 1.0       # channel B margin swing  (x=0.5 -> canonical 1.5)
SIGMA0_CANON = 0.15 # canonical channel-A noise (T1)


# ----------------------------------------------------------------- [exact]
def crg_branches(p):
    """All real roots x in (0,1) of the CRG equilibrium quartic with the
    Routh-Hurwitz stability battery of the vault's Coupled Dynamical
    Equations. Returns list of dicts sorted by x."""
    a1, a2, b2 = p["alpha1"], p["alpha2"], p["beta2"]
    g1, g2, lam, mu = p["gamma1"], p["gamma2"], p["lam"], p["mu"]
    # Equilibrium: a1*(1-x^2)*(a2 + K*x^2) = g1*a2*b2*x,  K = g2*mu/lam
    #   => a1*K*x^4 + a1*(a2-K)*x^2 + g1*a2*b2*x - a1*a2 = 0
    # (no cubic term; Descartes sign pattern (+,0,-,+,-) when K>a2
    #  => 3 or 1 positive roots — exactly the vault note's claim)
    K = g2 * mu / lam
    c4 = a1 * K
    c3 = 0.0
    c2 = a1 * (a2 - K)
    c1 = g1 * a2 * b2
    c0 = -a1 * a2
    roots = np.roots([c4, c3, c2, c1, c0])
    out = []
    for r in roots:
        if abs(r.imag) < 1e-10 and 0.0 < r.real < 1.0:
            x = float(r.real)
            y = a2 * b2 * x / (a2 + g2 * mu / lam * x * x)
            z = mu / lam * x * x * y
            j = np.array([
                [a1 * (1 - 3 * x * x) - g1 * y, -g1 * x,
                 0.0],
                [a2 * b2 * y,
                 a2 * (b2 * x - 2 * y) - g2 * z,
                 -g2 * y],
                [2 * mu * x * y, mu * x * x, -lam]])
            tr = float(np.trace(j))
            m2 = float(np.trace(j @ j))
            d2 = tr * tr / 2.0 - m2
            char = np.poly(j)
            a1c, a2c, a3c = float(char[1]), float(char[2]), float(char[3])
            rh_ok = (a1c > 0) and (a2c > 0) and (a3c > 0) and (d2 > 0)
            det = float(np.linalg.det(j))
            # 3D flow: char poly is s^3 + a1 s^2 + a2 s + a3 with a3 = -det(J);
            # RH needs a3 > 0  <=>  det(J) < 0 (the vault note's own sign)
            out.append(dict(x=x, y=y, z=z, rh=bool(rh_ok),
                            det=det, stable=bool(rh_ok and det < 0)))
    out.sort(key=lambda d: d["x"])
    return out


# ------------------------------------------------- [model] branch -> seed
def branch_to_seed(x_star):
    """Density-preserving identification (the W8 [model] choice):
    x=0.5 anchors the canonical seeds; the swing keeps the field in the
    measured dynamic range of the reference register.
    Returns (phi_amp, rho0_mean)."""
    amp = max(SIGMA0_CANON * (1.0 + ETA_A * (x_star - 0.5)), 1e-4)
    return amp, 1.5 + DELTA_B * (x_star - 0.5)


# -------------------------------------------------------- [measured] exit
def read_exit(beta=BETA, seeds=SEEDS, steps=STEPS, phi_amp=None,
              rho0_mean=None, channel="both"):
    pAs, pBs, pUs = [], [], []
    for sd in seeds:
        mA, mB, _, _ = unified_register(beta=beta, seed=sd, steps=steps,
                                        patience=PATIENCE,
                                        quiet_thr=QUIET_THR,
                                        channel=channel,
                                        phi_amp=phi_amp,
                                        rho0_mean=rho0_mean)
        pAs.append(mA.mean())
        pBs.append(mB.mean())
        pUs.append((mA | mB).mean())
    return (float(np.mean(pAs)), float(np.mean(pBs)), float(np.mean(pUs)))


# ------------------------------------------------- [exact] bistable search
def find_bistable(n_draw=20000, seed=20260928):
    """Honest exemplar search: log-uniform parameters outside the
    sufficient condition (g2*mu/lam > a2, the measured ~2% region); keep
    the first parameter set with >= 2 linearly stable equilibria."""
    rng = np.random.default_rng(seed)
    lo, hi = np.log10(0.01), np.log10(50.0)
    for _ in range(n_draw):
        p = dict(alpha1=10 ** rng.uniform(lo, hi),
                 alpha2=10 ** rng.uniform(lo, hi),
                 beta2=10 ** rng.uniform(lo, hi),
                 gamma1=10 ** rng.uniform(lo, hi),
                 gamma2=10 ** rng.uniform(lo, hi),
                 lam=10 ** rng.uniform(lo, hi),
                 mu=10 ** rng.uniform(lo, hi))
        if p["gamma2"] * p["mu"] / p["lam"] <= p["alpha2"]:
            continue  # inside the sufficient condition — skip
        br = [b for b in crg_branches(p) if b["stable"]]
        if len(br) >= 2:
            return p, br
    return None, None


def run_battery():
    print("== W8: CRG bistable branches -> unified register exits ==")
    print(f"L={L}, seeds {SEEDS}, steps<={STEPS}, beta={BETA}")
    print(f"CRG recorded reference (Coupled Dynamical Equations): {CRG_REF}")
    ref_br = crg_branches(CRG_REF)
    stable = [b for b in ref_br if b["stable"]]
    print(f"[exact] its equilibria in (0,1): "
          + (", ".join(f"x*={b['x']:.4f} "
                       f"({'stable' if b['stable'] else 'saddle'})"
                       for b in ref_br) or "none"))
    if len(stable) < 2:
        print("FATAL: recorded reference is not bistable under the "
              "corrected classification.")
        return
    print(f"   => the recorded exemplar IS bistable "
          f"({', '.join(f'{b[chr(120)]:.4f}' for b in stable)})")
    print("   frequency context [exact, 20k-draw grid]: multi-root 3.02% of")
    print("   outside-condition draws; bistable 0.37% overall — E4")
    print("   refinement: 'on average two stable' is refuted (mean 1.25).\n")

    # --- reference exits at canonical seeds [measured baseline]
    pA0, pB0, pU0 = read_exit()
    print(f"[measured] canonical reference: pA={pA0:.4f} pB={pB0:.4f} "
          f"pU={pU0:.4f}")

    # --- feed each stable branch
    print("\n[measured] branch-feeding (density-preserving [model] map):")
    print(f"{'branch':>8} {'x*':>7} {'amp_A':>7} {'rho0_B':>7} "
          f"{'pA_ctx':>8} {'pB_ctx':>8} {'pU':>8}")
    rows = []
    for tag, b in (("low", stable[0]), ("high", stable[1])):
        amp, r0 = branch_to_seed(b["x"])
        pA, pB, pU = read_exit(phi_amp=amp, rho0_mean=r0)
        rows.append((tag, b["x"], pA, pB, pU, amp, r0))
        print(f"{tag:>8} {b['x']:7.3f} "
              f"{amp:7.4f} "
              f"{r0:7.4f} "
              f"{pA:8.4f} {pB:8.4f} {pU:8.4f}")

    # --- split analysis: does one parameter set feed DIFFERENT exits?
    dA = rows[1][2] - rows[0][2]
    dB = rows[1][3] - rows[0][3]
    split_ratio = dA / dB if dB != 0 else float("inf")
    print(f"\n   branch split (high minus low): "
          f"dpA={dA:+.4f}  dpB={dB:+.4f}  ratio={split_ratio:.3f}")
    if abs(dB) < 1e-3:
        verdict = ("no split: both branches feed the SAME exit channel "
                   "(B is saturated in the same direction) — the unified "
                   "register reads CRG bistability as a single-exit "
                   "phenomenon")
    elif abs(dA / dB) < 0.5:
        verdict = ("split toward B: the high-x branch pushes the SPUMA "
                   "freeze-out exit harder than the LIMEN registration exit")
    elif abs(dA / dB) > 2.0:
        verdict = ("split toward A: the high-x branch pushes the LIMEN "
                   "registration exit harder")
    else:
        verdict = ("balanced split: both exits move comparably")
    print(f"   => OQ-C4-2 verdict: {verdict}")

    # --- per-branch solo reads (which channel is the branch's own exit?)
    print("\n[measured] per-branch solo reads (single-exit runs):")
    for tag, b in (("low", stable[0]), ("high", stable[1])):
        amp, r0 = branch_to_seed(b["x"])
        pA_solo = read_exit(phi_amp=amp, rho0_mean=r0, channel="A")[0]
        pB_solo = read_exit(phi_amp=amp, rho0_mean=r0, channel="B")[1]
        print(f"   {tag} branch: A-solo p={pA_solo:.4f} | "
              f"B-solo p={pB_solo:.4f}  -> dominant exit: "
              f"{'A (LIMEN)' if pA_solo > pB_solo else 'B (SPUMA)'}")

    print("\nVerdict labels: CRG branches [exact]; branch->seed map [model];")
    print("exit reads [measured]; the unified dynamics stays [model] per")
    print("Unified-Register-Integration §9. F3 untouched — no nature-side")
    print("claim; S1/S2 untouched — the CRG core is a boundary-side system.")
    print("\nHonest limit: the x->amplitude identification is ONE calibrated")
    print("choice; sensitivity to eta/delta is the next-row tool (OQ-C4-2b).")


if __name__ == "__main__":
    run_battery()
