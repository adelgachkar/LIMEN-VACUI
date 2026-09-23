# -*- coding: utf-8 -*-
"""
DOSE COLLAPSE + PREDICTIVITY TEST for the beta-plane map (open work item of v0.4.0).

Question: is p_U(beta) a single-valued function of an effective cross-noise
dose  D_eff(beta) = occupancy-weighted mean_k |1+beta*k|  — i.e. is the beta
map PREDICTIVE from (i) one frozen reference occupancy measurement + (ii) a
universal response curve F, without refitting anything per point?

Data:
  * FIT (13 pts):  the canonical beta-plane map rows (recorded in
                    limen_beta_plane_output.txt; seed-means of 5 seeds).
  * HELD-OUT (6):  probe points RECORDED but never fitted (free validation).
  * FORWARD (5):   betas never simulated anywhere -> predict, then simulate.
  * SCOPE (4):     recorded strong-coupling points (kappa=0.30, other phase).

Structural corollary tested: a k=1-dominated occupancy makes p_U(beta) a
function of |1+beta| alone => mirror symmetry p_U(beta) ~ p_U(-2-beta).

Labels: amplitude math + mirror identity [exact/structural]; occupancy,
collapse table, F, LOOCV, held-out and forward errors [measured];
the "amplitude-controlled" claim [model, measured support].
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from limen_spuma_unified_register import unified_register, _nbr_count
from limen_spuma_bridge import mask_stats

L = 192
SEEDS = (11, 12, 13, 14, 15)
KAPPA = 0.03
G_MAX = 0.297
P_A_SOLO, P_B_SOLO = 0.3174, 0.2988          # archived canonical solos [exact]

FIT = [(-2.00, 0.5238), (-1.50, 0.3767), (-1.25, 0.3695), (-1.00, 0.3692),
       (-0.85, 0.3693), (-0.70, 0.3701), (-0.50, 0.3761), (-0.35, 0.3895),
       (-0.20, 0.4222), (0.00, 0.5232), (0.35, 0.7674), (0.70, 0.8971),
       (1.00, 0.9329)]                        # (beta, pU) — recorded map
HELDOUT = [(-2.50, 0.8402), (0.05, 0.5577), (0.10, 0.5942),
           (0.15, 0.6312), (0.20, 0.6683), (0.28, 0.7238)]   # recorded probes
FORWARD_NEW = (-2.75, -1.75, -0.60, -0.10, 0.22)             # never simulated
SCOPE_BETA = (-1.00, -1.50, -2.00, -3.00)                    # kappa=0.30 rows
SCOPE_PU = (0.7551, 0.7779, 0.9361, 0.9867)                  # recorded


def occupancy_at(beta, kappa=KAPPA):
    """Accumulate opposite-neighbor-count histograms over the 5 seeds.
    wB_k: B-exit-eligible sites (~mA) with k A-active neighbors;
    wA_k: A-exit-eligible sites (~mB) with k B-active neighbors."""
    wA = np.zeros(5, dtype=np.int64)
    wB = np.zeros(5, dtype=np.int64)
    for sd in SEEDS:
        mA, mB, _, _ = unified_register(beta=beta, seed=sd, kappa=kappa,
                                        g_max=G_MAX)
        kA = _nbr_count(mA)
        kB = _nbr_count(mB)
        wB += [int(((~mA) & (kA == k)).sum()) for k in range(5)]
        wA += [int(((~mB) & (kB == k)).sum()) for k in range(5)]
    return wA, wB


def dose_eff(beta, wA, wB):
    amps = np.array([abs(1.0 + beta * k) for k in range(5)], dtype=float)
    dA = float(np.dot(wA, amps) / max(int(wA.sum()), 1))
    dB = float(np.dot(wB, amps) / max(int(wB.sum()), 1))
    return (P_A_SOLO * dA + P_B_SOLO * dB) / (P_A_SOLO + P_B_SOLO)


def dose_min(beta):
    """Unweighted structural floor min_k |1+beta*k| (k=0..4) — the naive form."""
    return min(abs(1.0 + beta * k) for k in range(5))


def pava_fit(xs, ys):
    """Isotonic (increasing) fit via pooled adjacent violators; linear
    interpolation between block centers, clamped at the ends."""
    order = np.argsort(xs)
    x = np.asarray(xs, float)[order]
    y = np.asarray(ys, float)[order]
    blocks = []                                   # [sum_x, n_x, sum_y, n_y]
    for xi, yi in zip(x, y):
        blocks.append([xi, 1.0, yi, 1.0])
        while (len(blocks) >= 2 and
               blocks[-2][2] / blocks[-2][3] > blocks[-1][2] / blocks[-1][3] + 1e-15):
            a, b = blocks[-2], blocks[-1]
            blocks[-2] = [a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3]]
            blocks.pop()
    centers = [b[0] / b[1] for b in blocks]
    vals = [b[2] / b[3] for b in blocks]

    def predict(xq):
        if len(centers) == 1:
            return float(vals[0])
        return float(np.interp(xq, centers, vals, left=vals[0], right=vals[-1]))
    return predict, list(zip(np.round(centers, 4), np.round(vals, 4)))


def loocv(pairs, maker):
    errs = []
    for i in range(len(pairs)):
        train = [p for j, p in enumerate(pairs) if j != i]
        f = maker(train)
        errs.append(f(pairs[i][0]) - pairs[i][1])
    return float(np.sqrt(np.mean(np.square(errs)))), errs


def poly_maker(deg):
    def mk(train):
        xs = [p[0] for p in train]
        ys = [p[1] for p in train]
        c = np.polyfit(xs, ys, deg)
        return lambda xq: float(np.polyval(c, xq))
    return mk


def pava_maker(train):
    xs = [p[0] for p in train]
    ys = [p[1] for p in train]
    f, _ = pava_fit(xs, ys)
    return f


def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    return float(np.corrcoef(rx, ry)[0, 1])


def violations(pairs):
    """Adjacent inversions when sorted by x (lower bound on non-monotonicity)."""
    s = sorted(pairs, key=lambda p: p[0])
    return sum(1 for i in range(len(s) - 1) if s[i + 1][1] < s[i][1] - 1e-12)


def main():
    print("== DOSE COLLAPSE & PREDICTIVITY: p_U(beta) as F(effective cross-noise dose) ==")
    print(f"L={L}, seeds {SEEDS}, kappa={KAPPA}, g_max={G_MAX}; "
          f"solo weights {P_A_SOLO}/{P_B_SOLO} (archived)\n")

    # ---------- [1] frozen reference occupancy ----------
    print("[1] reference occupancy (frozen; measured at beta=0, 5 seeds)")
    wA_ref, wB_ref = occupancy_at(0.0)
    totA, totB = int(wA_ref.sum()), int(wB_ref.sum())
    print("    wB_k (B-exit sites ~mA by kA): "
          + " ".join(f"k{k}={wB_ref[k]/totB:.3f}" for k in range(5))
          + f"   n={totB}")
    print("    wA_k (A-exit sites ~mB by kB): "
          + " ".join(f"k{k}={wA_ref[k]/totA:.3f}" for k in range(5))
          + f"   n={totA}")
    print("    D_eff(beta) = (pA*D_A + pB*D_B)/(pA+pB); "
          "D_min(beta) = min_k |1+beta*k| (naive, unweighted)\n")

    # ---------- [2] collapse table ----------
    fit_d = [(b, dose_eff(b, wA_ref, wB_ref), dose_min(b), p)
             for b, p in FIT]
    print("[2] collapse table (13 recorded fit points, frozen-q dose)")
    print(f"{'beta':>6} {'D_eff':>7} {'D_min':>7} {'pU':>7}")
    for b, de, dm, p in fit_d:
        print(f"{b:6.2f} {de:7.4f} {dm:7.4f} {p:7.4f}")
    sp_all = spearman([r[1] for r in fit_d], [r[3] for r in fit_d])
    sp_min = spearman([r[2] for r in fit_d], [r[3] for r in fit_d])
    v_all = violations([(r[1], r[3]) for r in fit_d])
    v_min = violations([(r[2], r[3]) for r in fit_d])
    shield = [r for r in fit_d if r[0] <= 0.0]
    boost = [r for r in fit_d if r[0] > 0.0]
    v_shield = violations([(r[1], r[3]) for r in shield])
    v_boost = violations([(r[1], r[3]) for r in boost])
    print(f"    Spearman(pU, D_eff) = {sp_all:+.3f}   (naive D_min: {sp_min:+.3f})")
    print(f"    monotonicity violations (D_eff): all={v_all}, "
          f"shield-branch={v_shield}/9, boost-branch={v_boost}/4   "
          f"(D_min: all={v_min})")
    print()

    # ---------- [3] isotonic F ----------
    F, blocks = pava_fit([r[1] for r in fit_d], [r[3] for r in fit_d])
    ins = np.sqrt(np.mean([(F(d) - p) ** 2 for _, d, _, p in fit_d]))
    print(f"[3] isotonic F on (D_eff, pU): {len(blocks)} blocks; "
          f"in-sample RMSE = {ins:.4f}")
    if len(blocks) <= 9:
        for c, v in blocks:
            print(f"      D~{c:6.4f} -> F={v:.4f}")
    print()

    # ---------- [4] LOOCV model comparison ----------
    print("[4] LOOCV predictivity (n=13; lower = more predictive)")
    r_dose, _ = loocv([(r[1], r[3]) for r in fit_d], pava_maker)
    r_lin, _ = loocv([(r[0], r[3]) for r in fit_d], poly_maker(1))
    r_qua, _ = loocv([(r[0], r[3]) for r in fit_d], poly_maker(4))
    r_dmin, _ = loocv([(r[2], r[3]) for r in fit_d], pava_maker)
    print(f"    dose-PAVA  F(D_eff)        : RMSE = {r_dose:.4f}")
    print(f"    naive dose-PAVA F(D_min)   : RMSE = {r_dmin:.4f}")
    print(f"    null: linear in beta       : RMSE = {r_lin:.4f}")
    print(f"    null: quartic in beta (5p) : RMSE = {r_qua:.4f}")
    print()

    # ---------- [5] held-out validation vs recorded probes ----------
    print("[5] held-out validation: 6 RECORDED probe points never fitted")
    print(f"{'beta':>6} {'pred':>7} {'recorded':>9} {'err':>7}")
    he = []
    for b, p_rec in HELDOUT:
        pr = F(dose_eff(b, wA_ref, wB_ref))
        he.append(pr - p_rec)
        print(f"{b:6.2f} {pr:7.4f} {p_rec:9.4f} {pr - p_rec:+7.4f}")
    print(f"    held-out RMSE = {np.sqrt(np.mean(np.square(he))):.4f}   "
          f"max|err| = {max(abs(e) for e in he):.4f}")
    print()

    # ---------- [6] forward test on NEW betas ----------
    print("[6] forward test: NEW betas — predict first, then simulate (5 seeds)")
    print(f"{'beta':>6} {'pred_frozen':>12} {'pred_self':>10} {'pU_sim':>7} "
          f"{'err_f':>7} {'err_s':>7}  per-seed")
    fe, se = [], []
    for b in FORWARD_NEW:
        per, wA_s = [], np.zeros(5, dtype=np.int64)
        wB_s = np.zeros(5, dtype=np.int64)
        for sd in SEEDS:
            mA, mB, _, _ = unified_register(beta=b, seed=sd, kappa=KAPPA,
                                            g_max=G_MAX)
            p, _, _, _ = mask_stats(mA | mB)
            per.append(p)
            kA = _nbr_count(mA)
            kB = _nbr_count(mB)
            wB_s += [int(((~mA) & (kA == k)).sum()) for k in range(5)]
            wA_s += [int((~mB & (kB == k)).sum()) for k in range(5)]
        pU_sim = float(np.mean(per))
        pr_f = F(dose_eff(b, wA_ref, wB_ref))
        pr_s = F(dose_eff(b, wA_s, wB_s))
        fe.append(pr_f - pU_sim)
        se.append(pr_s - pU_sim)
        sc = f"[{min(per):.3f},{max(per):.3f}]"
        print(f"{b:6.2f} {pr_f:12.4f} {pr_s:10.4f} {pU_sim:7.4f} "
              f"{pr_f - pU_sim:+7.4f} {pr_s - pU_sim:+7.4f}  {sc}")
    print(f"    forward RMSE: frozen-q = {np.sqrt(np.mean(np.square(fe))):.4f}, "
          f"self-q = {np.sqrt(np.mean(np.square(se))):.4f}")
    print()

    # ---------- [7] scope transfer to kappa=0.30 ----------
    print("[7] scope: strong coupling (kappa=0.30, recorded) — does the form transfer?")
    wA_30, wB_30 = occupancy_at(0.0, kappa=0.30)
    tA, tB = int(wA_30.sum()), int(wB_30.sum())
    print("    occupancy at kappa=0.30, beta=0: "
          + " ".join(f"k{k}={wB_30[k]/tB:.3f}" for k in range(5))
          + "  (wB, normalized)")
    print(f"{'beta':>6} {'pred_transfer':>14} {'recorded':>9}")
    tfe = []
    for b, p_rec in zip(SCOPE_BETA, SCOPE_PU):
        pr = F(dose_eff(b, wA_ref, wB_ref))
        tfe.append(pr - p_rec)
        print(f"{b:6.2f} {pr:14.4f} {p_rec:9.4f}")
    d30 = [dose_eff(b, wA_30, wB_30) for b in SCOPE_BETA]
    sp30 = spearman(d30, list(SCOPE_PU))
    v30 = violations(list(zip(d30, SCOPE_PU)))
    print(f"    naive transfer RMSE = {np.sqrt(np.mean(np.square(tfe))):.4f} "
          f"(expected: FAIL — different phase)")
    print(f"    re-measured occupancy: Spearman(pU, D_eff@0.30) = {sp30:+.3f}, "
          f"violations = {v30}/4  -> dose ORDER "
          f"{'transfers' if sp30 > 0.9 and v30 == 0 else 'does NOT transfer cleanly'}")
    print()

    # ---------- [8] mirror corollary ----------
    print("[8] mirror corollary (k=1-dominated => p_U(beta) ~ p_U(-2-beta)) [structural]")
    rec = dict(FIT + HELDOUT)
    pairs = [(b, -2.0 - b) for b in rec if (-2.0 - b) in rec]
    for b1, b2 in pairs:
        print(f"    |pU({b1:+.2f}) - pU({b2:+.2f})| = "
              f"{abs(rec[b1] - rec[b2]):.4f}")
    print()

    # ---------- verdict (from data only) ----------
    print("VERDICT (data-driven):")
    print(f"  - collapse: Spearman {sp_all:+.3f}, violations all={v_all} "
          f"(shield={v_shield}/9, boost={v_boost}/4)")
    print(f"  - LOOCV ranking: dose-PAVA {r_dose:.4f} vs linear {r_lin:.4f} "
          f"/ quartic {r_qua:.4f} / naive-dose {r_dmin:.4f}")
    print(f"  - held-out (6 recorded probes): RMSE "
          f"{np.sqrt(np.mean(np.square(he))):.4f}")
    print(f"  - forward (5 new sims): frozen {np.sqrt(np.mean(np.square(fe))):.4f} "
          f"/ self-q {np.sqrt(np.mean(np.square(se))):.4f}")
    print(f"  - scope kappa=0.30: transfer RMSE "
          f"{np.sqrt(np.mean(np.square(tfe))):.4f}; dose-order spearman {sp30:+.3f}")
    print("Labels: amplitude math, mirror identity [exact/structural]; "
          "occupancy, F, LOOCV, errors [measured];")
    print("'amplitude-controlled' claim [model with measured support].")


if __name__ == "__main__":
    main()
