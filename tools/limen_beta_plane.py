# -*- coding: utf-8 -*-
"""
BETA-PLANE MAP for the unified register (open work item of Release v0.3.0).

Question: where in beta does the union register fall BELOW BOTH solo
registers, and is the shield->boost transition sharp or gradual?

Method:
  * anchors on the SAME lattice/seeds/code path as the battery [exact]:
      A-solo (channel="A") and B-solo (channel="B") rates.
  * beta scan at the headline coupling (kappa=0.03, g_max=0.297, b=0.30):
      pU(beta), context split pA_ctx/pB_ctx, union mean size vs the iid
      benchmark R(beta), spanning count.
  * structural amplitude prediction [exact math -> measured check]:
      the cross-noise amplitude for a site with k active opposite-channel
      neighbors is |1 + beta*k|  =>
        - quiet bands at beta = -1/k  (perfect shield),
        - RE-AMPLIFICATION once 1 + beta*k < 0  (|gain| > 1 again).
      Prediction: pU(beta) is NON-MONOTONIC — a minimum near the dominant-k
      quiet band (k=1..2 -> beta ~ -0.5..-1) and a RISE toward beta <= -2.
  * crossing analysis: where pU < min(pA_solo, pB_solo) = pB_solo,
    sharpness (width in beta, per-seed scatter / bimodality hint).

Battery labels: anchors/identities/benchmark [exact]; rates, curve shape,
dose ratios [measured]; unified coupling [model].
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from limen_spuma_unified_register import unified_register   # verbatim core
from limen_spuma_bridge import mask_stats                   # verbatim

L = 192
SEEDS = (11, 12, 13, 14, 15)
KAPPA = 0.03
G_MAX = 0.297
BETA_GRID = (-2.0, -1.5, -1.25, -1.0, -0.85, -0.7, -0.5, -0.35, -0.2,
             0.0, 0.35, 0.7, 1.0)
IID_REPS = 20


def run_stats(beta, kappa=KAPPA, g_max=G_MAX, seeds=SEEDS):
    """Seed loop -> (pU, pA_ctx, pB_ctx, meanU, spanning, per-seed pU)."""
    pUs, pAs, pBs, mUs, span, per = [], [], [], [], 0, []
    for sd in seeds:
        mA, mB, _, _ = unified_register(beta=beta, seed=sd, kappa=kappa,
                                        g_max=g_max)
        p, mn, _, sp = mask_stats(mA | mB)
        pUs.append(p); mUs.append(mn); span += sp
        pAs.append(mA.mean()); pBs.append(mB.mean()); per.append(p)
    return (float(np.mean(pUs)), float(np.mean(pAs)), float(np.mean(pBs)),
            float(np.mean(mUs)), span, per)


def iid_mean(pf, reps=IID_REPS):
    rng = np.random.default_rng(23)
    return float(np.mean([mask_stats(rng.random((L, L)) < pf)[1]
                          for _ in range(reps)]))


def dose_ratio(beta_ref, beta_cmp, seeds=(11, 12)):
    """P(B-exit | k A-neighbors) ratio between two betas, same seeds."""
    from limen_spuma_unified_register import _nbr_count
    out = {k: [0, 0, 0, 0] for k in range(5)}   # [exits_cmp, n_cmp, exits_ref, n_ref]
    for sd in seeds:
        for beta, io in ((beta_cmp, 0), (beta_ref, 2)):
            mA, mB, _, _ = unified_register(beta=beta, seed=sd)
            kA = _nbr_count(mA)
            for k in range(5):
                sel = ~mA & (kA == k)
                out[k][io] += int((sel & mB).sum())
                out[k][io + 1] += int(sel.sum())
    return out


def main():
    print("== BETA-PLANE MAP: shield <-> boost transition of the unified register ==")
    print(f"L={L}, seeds {SEEDS}, kappa={KAPPA}, g_max={G_MAX}, b=0.30 (canonical)")
    print("cross-noise amplitude for k active neighbors: |1 + beta*k|  "
          "-> quiet bands at beta=-1/k, re-amplification for 1+beta*k<0\n")

    # ---------- anchors (same code path as battery U0) ----------
    pAs_, pBs_, mnAs_, mnBs_ = [], [], [], []
    for sd in SEEDS:
        mA, mB, _, _ = unified_register(channel="A", seed=sd)
        p, mn, _, _ = mask_stats(mA); pAs_.append(p); mnAs_.append(mn)
        mA, mB, _, _ = unified_register(channel="B", seed=sd)
        p, mn, _, _ = mask_stats(mB); pBs_.append(p); mnBs_.append(mn)
    pA_solo = float(np.mean(pAs_)); pB_solo = float(np.mean(pBs_))
    print(f"[anchors] A solo p_f = {pA_solo:.4f} (mean size {np.mean(mnAs_):.2f})")
    print(f"[anchors] B solo p_f = {pB_solo:.4f} (mean size {np.mean(mnBs_):.2f})")
    print(f"          'below both solos' threshold = min = {pB_solo:.4f}\n")

    # ---------- beta scan ----------
    print(f"{'beta':>6} {'pU':>7} {'pA_ctx':>7} {'pB_ctx':>7} {'meanU':>7} "
          f"{'R_iid':>6} {'span':>6}   per-seed pU (scatter)")
    rows = []
    for beta in BETA_GRID:
        pU, pAc, pBc, mU, span, per = run_stats(beta)
        mI = iid_mean(pU)
        R = mU / mI if mI > 0 else float("nan")
        scat = f"[{min(per):.3f},{max(per):.3f}]"
        rows.append(dict(beta=beta, pU=pU, pAc=pAc, pBc=pBc, mU=mU, R=R,
                         span=span, per=per))
        print(f"{beta:6.2f} {pU:7.4f} {pAc:7.4f} {pBc:7.4f} {mU:7.2f} "
              f"{R:6.2f} {span:2d}/{len(SEEDS)}   {scat}")

    # ---------- crossing analysis ----------
    below = [r for r in rows if r["pU"] < pB_solo]
    print(f"\n[crossing] points with pU < pB_solo={pB_solo:.4f}: "
          + (", ".join(f"beta={r['beta']:+.2f} (pU={r['pU']:.4f})"
                       for r in below) or "NONE"))
    if below:
        bmin = min(below, key=lambda r: r["pU"])
        print(f"   minimum: beta={bmin['beta']:+.2f}, pU={bmin['pU']:.4f} "
              f"({pB_solo - bmin['pU']:+.4f} below the smaller solo)")
        # window? does pU recover toward beta=-2?
        deep = [r for r in rows if r["beta"] <= -1.5]
        if deep:
            print(f"   re-amplification check (beta<=-1.5): "
                  + ", ".join(f"beta={r['beta']:+.2f}: pU={r['pU']:.4f}"
                              for r in deep))
            recov = deep[-1]["pU"] > bmin["pU"] + 0.02
            verdict = ("RE-OPENS toward deep negative beta" if recov
                       else "stays suppressed")
            print(f"   => union {verdict} [measured]")
        # crossing width in beta (last above -> first below, scanning up)
        ordered = sorted(rows, key=lambda r: r["beta"])
        edges = []
        for i in range(len(ordered) - 1):
            a, b = ordered[i], ordered[i + 1]
            if (a["pU"] - pB_solo) * (b["pU"] - pB_solo) < 0:
                t = (pB_solo - a["pU"]) / (b["pU"] - a["pU"])
                edges.append(a["beta"] + t * (b["beta"] - a["beta"]))
        print(f"   crossings of pU=pB_solo: "
              + (", ".join(f"{e:+.3f}" for e in edges) or "none"))
        if len(edges) >= 2:
            print(f"   => window width in beta = {edges[-1] - edges[0]:.3f}")
        # sharpness: steepest seed-averaged drop per unit beta
        slopes = [(ordered[i + 1]["pU"] - ordered[i]["pU"])
                  / (ordered[i + 1]["beta"] - ordered[i]["beta"])
                  for i in range(len(ordered) - 1)]
        i0 = int(np.argmax(np.abs(slopes)))
        print(f"   steepest slope: {slopes[i0]:+.3f} per unit beta "
              f"between beta={ordered[i0]['beta']:+.2f} and "
              f"{ordered[i0+1]['beta']:+.2f}")
        # per-seed scatter at the minimum (bimodality hint)
        sp = bmin["per"]
        print(f"   per-seed pU at minimum: "
              + ", ".join(f"{v:.3f}" for v in sp)
              + f"  (spread {max(sp)-min(sp):.3f} -> "
              + ("bimodality HINT" if max(sp) - min(sp) > 0.05
                 else "unimodal within seed noise") + ")")

    # ---------- context split: who dies first ----------
    print("\n[context split] channel rates inside the coupled run:")
    for r in rows:
        tag = ""
        if r["pAc"] < 0.5 * pA_solo:
            tag += " A-suppressed"
        if r["pBc"] < 0.5 * pB_solo:
            tag += " B-suppressed"
        print(f"   beta={r['beta']:+6.2f}: pA_ctx={r['pAc']:.4f} "
              f"(solo {pA_solo:.4f}), pB_ctx={r['pBc']:.4f} "
              f"(solo {pB_solo:.4f}){tag}")

    # ---------- amplitude prediction check: dose ratios ----------
    print("\n[dose check] P(B|k A-nbrs) ratio vs beta=0 baseline "
          "(same seeds; structural prediction: ratio tracks |1+beta*k|):")
    for bc in (-0.7, -2.0):
        dr = dose_ratio(0.0, bc)
        print(f"   beta={bc:+.2f}:")
        for k in range(5):
            amp = abs(1.0 + bc * k)
            if dr[k][1] >= 50 and dr[k][3] >= 50:
                ratio = (dr[k][0] / dr[k][1]) / (dr[k][2] / dr[k][3])
                print(f"     k={k}: ratio={ratio:6.3f}   "
                      f"|1+beta*k|={amp:4.2f}   n_cmp={dr[k][1]}")
            else:
                print(f"     k={k}: (insufficient sites: "
                      f"n_cmp={dr[k][1]}, n_ref={dr[k][3]})   "
                      f"|1+beta*k|={amp:4.2f}")

    print("\nVerdict template (filled from data only):")
    print("  shape: non-monotonic with minimum near the k=1..2 quiet band?")
    print("  below-both-solos: window in beta or persistent phase?")
    print("  transition: sharp (width <= 0.25 in beta) or gradual?")
    print("Labels: anchors, amplitude math, identities [exact]; curve,")
    print("crossings, dose ratios [measured]; unified coupling [model].")


if __name__ == "__main__":
    main()
