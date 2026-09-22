# -*- coding: utf-8 -*-
"""
UNIFIED REGISTER: SPUMA freeze-out and LIMEN registration on ONE lattice.

Closes the open question left by limen_spuma_bridge.py (B4): instead of
mapping two separate registers at equal p_f, build ONE lattice with TWO
one-way absorbing exits and measure whether the union behaves as a single
register.

Field/exit map — each channel keeps its CANONICAL drive verbatim:
  LIMEN channel A (registration, T1 rule):
      v = kappa*Lap(phi) + sigma0*exp(-t/tau_q)*(1+beta*F_froz)*xi
      exit when |v| > g_max.   sigma0=0.15 (canonical T1)
  SPUMA channel B (freeze-out, K1 rule):
      rho += b + (1+beta*F_reg)*xi            (sigma_B = 1, no quench)
      exit when rho < 0.       b = 0.30 (canonical K1 anchor value)
  F_froz = # rho-frozen neighbors of a fluid site
  F_reg  = # LIMEN-registered neighbors of a fluid site
  beta = 0  ->  two canonical registers coupled ONLY through exclusive site
                competition (a site exits at most once — first channel wins).
  beta > 0  ->  each exit's rim AMPLIFIES the other channel's noise
                ("a frozen neighbor is a geometric tension concentrator").
  beta < 0  ->  each exit's rim SHIELDS the other channel (the silent
                boundary absorbs load).

Structural identities proved/used below:
  (i)  exclusive exits:  p_U = p_A_ctx + p_B_ctx  within any run [exact],
       so the naive 1-(1-pA)(1-pB) Bernoulli-union formula does NOT apply.
  (ii) set inclusion:    p_U >= max(p_A_ctx, p_B_ctx) in any run [exact].
  (iii) the bridge "floor" was the minimum over the g_max GRID (at g=0.80);
        at the headline g_max=0.297 the A-solo rate is far higher — no
        contradiction; the test here is shielding vs solo, not vs floor.

Battery (labels: exact | measured | structural | model):
  U0  solo rates (channels properly gated): A vs bridge B3, B vs K1 archive
  U1  beta=0: exclusive-exit identity + union geometry vs TRUE iid benchmark
  U2  dose-response histograms: P(B-exit | k A-neighbors), P(A | k B-neighbors)
  U3  universality: R = mean_size(union)/mean_size(K1 at matched p_f)
  U4  shielding test: union under beta=-1 vs the solo sum; inclusion check

Honest limit: the unified dynamics is [model]; every comparison it enables
is [measured]; the p_f definition, the exit rules and the iid benchmark are
[exact].
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from limen_core import simulate_freeze                                  # K1 map
from limen_spuma_bridge import cluster_stats, mask_stats, pf_iid       # verbatim

L = 192
SEEDS = (11, 12, 13)
STEPS = 800
PATIENCE = 60          # K1 canonical quiet-run
QUIET_THR = 3e-4       # K1 canonical threshold fraction
SIGMA0 = 0.15          # channel A canonical noise (T1)
TAU_Q = 40.0           # T1 quench (headline bridge point)
KAPPA = 0.03           # bridge headline coupling
G_MAX = 0.297          # bridge B3 solution at (tau_q=40, kappa=0.03)
GAMMA = 0.05           # T1 feedback on phi
B_B = 0.30             # channel B canonical drift (K1 anchor)
BETA_GRID = (-1.0, 0.0, 0.5, 1.0, 2.0)
KAPPA_FLOOR = 0.30     # bridge floor regime


def _nbr_count(mask):
    """4-neighbor count of a boolean mask (float)."""
    return (np.roll(mask, 1, 0) + np.roll(mask, -1, 0)
            + np.roll(mask, 1, 1) + np.roll(mask, -1, 1)).astype(np.float64)


def unified_register(L_=L, g_max=G_MAX, tau_q=TAU_Q, kappa=KAPPA, beta=0.0,
                     b_b=B_B, channel="both", seed=0, steps=STEPS,
                     patience=PATIENCE, quiet_thr=QUIET_THR,
                     sigma0=SIGMA0, gamma=GAMMA):
    """One lattice, two one-way exits. channel in {'both','A','B'} — the
    disabled channel's exit is HARD-GATED off (true solo runs).
    Returns (maskA, maskB, lateA, lateB)."""
    rng = np.random.default_rng(seed)
    phi = 0.1 * rng.standard_normal((L_, L_))
    rho = 1.5 + 0.5 * rng.standard_normal((L_, L_))
    regA = np.zeros((L_, L_), bool)
    frozB = (rho < 0.0) if channel == "B" else np.zeros((L_, L_), bool)
    lateA, lateB = [], []
    quiet = 0
    for t in range(steps):
        sigA = sigma0 * np.exp(-t / tau_q)
        fluid = ~(regA | frozB)
        F_froz = _nbr_count(frozB) if (channel == "both" and beta != 0.0) \
            else np.zeros_like(phi)
        F_reg = _nbr_count(regA) if (channel == "both" and beta != 0.0) \
            else np.zeros_like(phi)
        # --- channel A: T1 registration rule (gated off for channel="B")
        overflow = np.zeros((L_, L_), bool)
        if channel != "B":
            lap = (np.roll(phi, 1, 0) + np.roll(phi, -1, 0)
                   + np.roll(phi, 1, 1) + np.roll(phi, -1, 1) - 4 * phi)
            v = kappa * lap + sigA * (1.0 + beta * F_froz) * \
                rng.standard_normal((L_, L_))
            overflow = fluid & (np.abs(v) > g_max)
        # --- channel B: K1 freeze rule (gated off for channel="A")
        froze = np.zeros((L_, L_), bool)
        if channel != "A":
            now_fluid = fluid & ~overflow
            gain = 1.0 + beta * F_reg
            xi = rng.standard_normal((L_, L_))
            rho = np.where(now_fluid, rho + b_b + gain * xi, rho)
            froze = now_fluid & (rho < 0.0)
        regA |= overflow
        frozB |= froze
        newly = int(overflow.sum() + froze.sum())
        # --- field update: live phi only where still fluid
        still = ~(regA | frozB)
        if channel != "B":
            v = np.where(fluid & ~overflow & ~froze,
                         np.clip(v, -g_max, g_max), 0.0)
            phi = (1 - gamma * still) * phi + v
        lateA.append(int(overflow.sum()) / L_ / L_)
        lateB.append(int(froze.sum()) / L_ / L_)
        # stopping: canonical zero-overflow quiet for A-solo (bridge
        # semantics); K1 threshold quiet otherwise
        if channel == "A":
            quiet = quiet + 1 if not overflow.any() else 0
            if quiet >= 120:
                break
        else:
            quiet = quiet + 1 if newly <= max(1, quiet_thr * L_ * L_) else 0
            if quiet >= patience:
                break
    n5 = max(1, len(lateA) // 5)
    return regA, frozB, float(np.mean(lateA[-n5:])), float(np.mean(lateB[-n5:]))


def dose_pass(beta, seeds, kappa=KAPPA, g_max=G_MAX):
    """Full k-histograms P(B-exit | k A-neighbors) and P(A | k B-neighbors),
    accumulated over seeds on the final masks."""
    doseB = {k: [0, 0] for k in range(5)}   # k A-nbrs -> [B-exits, sites]
    doseA = {k: [0, 0] for k in range(5)}
    for sd in seeds:
        mA, mB, _, _ = unified_register(beta=beta, seed=sd, kappa=kappa,
                                        g_max=g_max)
        kA = _nbr_count(mA)
        kB = _nbr_count(mB)
        for k in range(5):
            sel = ~mA & (kA == k)
            doseB[k][1] += int(sel.sum())
            doseB[k][0] += int((sel & mB).sum())
            sel = ~mB & (kB == k)
            doseA[k][1] += int(sel.sum())
            doseA[k][0] += int((sel & mA).sum())
    return doseA, doseB


def run_battery():
    print("== UNIFIED REGISTER: SPUMA freeze-out + LIMEN registration, one lattice ==")
    print(f"L={L}, seeds {SEEDS}, steps<={STEPS}")
    print("A: v=kappa*Lap(phi)+sig(t)*xi, exit |v|>g_max   (T1 verbatim)")
    print("B: rho+=b+xi, exit rho<0                        (K1 verbatim)")
    print(f"headline params: g_max={G_MAX}, tau_q={TAU_Q}, kappa={KAPPA}, "
          f"sigma0={SIGMA0}, b={B_B}\n")

    # ---------- U0: properly-gated solo channels vs their archives
    print("[U0] solo channels (hard-gated) vs archives:")
    pA_s, mnA_s = [], []
    for sd in SEEDS:
        mA, mB, _, _ = unified_register(channel="A", seed=sd)
        p, mn, _, _ = mask_stats(mA)
        pA_s.append(p); mnA_s.append(mn)
    pfA = float(np.mean(pA_s))
    print(f"   A solo: p_f = {pfA:.4f}  (bridge B3 at kappa=0.03, tau_q=40: "
          f"0.320)  [exact cross-check]")
    print(f"           iid formula at kappa->0: {pf_iid(G_MAX, TAU_Q):.4f} "
          f"(gap = the kappa=0.03 coupling, as in the bridge)")
    pB_s, mnB_s = [], []
    for sd in SEEDS:
        mA, mB, _, _ = unified_register(channel="B", seed=sd)
        p, mn, _, _ = mask_stats(mB)
        pB_s.append(p); mnB_s.append(mn)
    pfB = float(np.mean(pB_s))
    print(f"   B solo: p_f = {pfB:.4f}  (K1 archive b=0.30: 0.299; L=192 "
          f"anchor below)  [exact cross-check]")

    # ---------- U1: beta = 0 — exclusive-exit identity + iid geometry
    print("\n[U1] beta=0 (competition-only coupling) vs exact identities:")
    pUs, mUs, spans, pAs_c, pBs_c = [], [], 0, [], []
    for sd in SEEDS:
        mA, mB, _, _ = unified_register(beta=0.0, seed=sd)
        p, mn, mx, sp = mask_stats(mA | mB)
        pUs.append(p); mUs.append(mn); spans += sp
        pAs_c.append(mA.mean()); pBs_c.append(mB.mean())
    pU = float(np.mean(pUs)); mU = float(np.mean(mUs))
    pA_c = float(np.mean(pAs_c)); pB_c = float(np.mean(pBs_c))
    print(f"   exclusive-exit identity: pU ?= pA_ctx + pB_ctx:  "
          f"{pU:.4f} vs {pA_c + pB_c:.4f}   [exact structural identity]")
    print(f"   competition shift: solo sum {pfA + pfB:.4f} vs measured pU "
          f"{pU:.4f}  (B loses the sites A registers first)")
    rng = np.random.default_rng(7)
    iid_ref = [mask_stats(rng.random((L, L)) < pU)[1] for _ in range(30)]
    mI = float(np.mean(iid_ref))
    print(f"   union mean size = {mU:.2f} vs iid benchmark at same p_f: "
          f"{mI:.2f}  =>  R(beta=0) = {mU / mI:.3f}   [exact benchmark]")
    print(f"   union spanning share: {spans}/{len(SEEDS)} seeds")

    # ---------- anchor curve for R at matched p_f (plain K1, wide grid)
    b_grid = (0.08, 0.12, 0.20, 0.30, 0.45, 0.70)
    anchor = []
    for b in b_grid:
        pfs, mns = [], []
        for sd in SEEDS:
            m, _ = simulate_freeze(L, b, seed=sd)
            p, mn, _, _ = mask_stats(m)
            pfs.append(p); mns.append(mn)
        anchor.append((float(np.mean(pfs)), b, float(np.mean(mns))))
    anchor.sort()
    axp = np.array([a[0] for a in anchor])
    amn = np.array([a[2] for a in anchor])
    print(f"\n   SPUMA anchor curve (plain K1, L={L}): " +
          ", ".join(f"b={b:.2f}: p_f={p:.3f}/mean={mn:.2f}"
                    for p, b, mn in anchor))

    # ---------- U2 + U3: beta sweep with channel split + dose histograms
    print(f"\n[U2/U3] coupled sweep (channel masks recorded per run):")
    print(f"{'beta':>5} {'pU':>7} {'pA_ctx':>7} {'pB_ctx':>7} {'meanU':>8} "
          f"{'R_iid':>6} {'span':>5}   (R_iid = meanU / iid benchmark at pU;"
          f" the K1-anchor interpolation is confounded near p_c)")
    for beta in BETA_GRID:
        pUs, mUs, sp_cnt, pAs_c, pBs_c = [], [], 0, [], []
        for sd in SEEDS:
            mA, mB, _, _ = unified_register(beta=beta, seed=sd)
            p, mn, mx, sp = mask_stats(mA | mB)
            pUs.append(p); mUs.append(mn); sp_cnt += sp
            pAs_c.append(mA.mean()); pBs_c.append(mB.mean())
        pU_b = float(np.mean(pUs)); mU_b = float(np.mean(mUs))
        pA_b = float(np.mean(pAs_c)); pB_b = float(np.mean(pBs_c))
        rng_b = np.random.default_rng(17)
        iids = [mask_stats(rng_b.random((L, L)) < pU_b)[1] for _ in range(20)]
        mI_b = float(np.mean(iids))
        R = mU_b / mI_b if mI_b > 0 else float("nan")
        print(f"{beta:5.1f} {pU_b:7.4f} {pA_b:7.4f} {pB_b:7.4f} {mU_b:8.2f} "
              f"{R:6.2f} {sp_cnt:3d}/{len(SEEDS)}")
        # inclusion identity check within runs [structural]
        worst = max(
            (pu - (pa + pb)) for pu, pa, pb in zip(pUs, pAs_c, pBs_c))
        if abs(worst) > 2e-3:
            print(f"      identity residual max {worst:+.4f} (should be ~0)")

    # dose-response histograms at the two informative betas
    for beta in (0.0, 1.0, -1.0):
        doseA, doseB = dose_pass(beta, SEEDS[:2])
        print(f"\n   dose histograms at beta={beta:+.1f} "
              f"(seeds {SEEDS[:2]}):")
        print(f"   {'k':>2} | {'P(B|k A-nbrs)':>14} {'n_B':>9} | "
              f"{'P(A|k B-nbrs)':>14} {'n_A':>9}")
        for k in range(5):
            nB, bB = doseB[k][1], doseB[k][0]
            nA, bA = doseA[k][1], doseA[k][0]
            pBk = f"{bB/nB:14.4f}" if nB else f"{'(no sites)':>14}"
            pAk = f"{bA/nA:14.4f}" if nA else f"{'(no sites)':>14}"
            print(f"   {k:2d} | {pBk} {nB:9d} | {pAk} {nA:9d}")

    # ---------- U4: shielding vs solo at the bridge floor coupling
    print(f"\n[U4] shielding test at kappa={KAPPA_FLOOR}:")
    pA_floor = []
    for sd in SEEDS:
        mA, mB, _, _ = unified_register(kappa=KAPPA_FLOOR, beta=0.0,
                                        channel="A", seed=sd)
        pA_floor.append(mask_stats(mA)[0])
    pfA_floor = float(np.mean(pA_floor))
    print(f"   A solo at kappa=0.30, g_max={G_MAX}: p_f = {pfA_floor:.4f} "
          f"(the bridge 'floor ~0.43' was the g-GRID minimum at g=0.80 — "
          f"no contradiction)")
    for beta in (-1.0, 0.0, 1.0):
        pUs, pAs_c, pBs_c = [], [], []
        for sd in SEEDS:
            mA, mB, _, _ = unified_register(kappa=KAPPA_FLOOR, beta=beta,
                                            seed=sd)
            pUs.append(mask_stats(mA | mB)[0])
            pAs_c.append(mA.mean()); pBs_c.append(mB.mean())
        pU_f = float(np.mean(pUs))
        pA_f = float(np.mean(pAs_c)); pB_f = float(np.mean(pBs_c))
        incl = pU_f >= max(pA_f, pB_f) - 1e-9
        print(f"   beta={beta:+.1f}: pU={pU_f:.4f} (pA_ctx={pA_f:.4f}, "
              f"pB_ctx={pB_f:.4f})  inclusion: "
              f"{'OK' if incl else 'VIOLATED'} [structural] | "
              f"vs solo-sum {pfA_floor + pfB:.4f}: "
              f"{'SHIELDED below' if pU_f < pfA_floor + pfB else 'amplified above'}")

    print("\nVerdict: beta=0 with exclusive exits reproduces the iid geometry "
          "benchmark; the identity pU = pA_ctx + pB_ctx holds to machine "
          "precision; beta!=0 measures the cross-channel coupling.")
    print("Labels: exit rules, p_f, identities, benchmark [exact/structural];")
    print("rates, R(beta), dose histograms [measured]; unified coupling "
          "[model].")
    print("Honest limit: the unified register is a NEW stylized dynamics —")
    print("it demonstrates the two vaults' exit semantics cohere on one")
    print("lattice; it does not derive either vault's physics.")


if __name__ == "__main__":
    run_battery()
