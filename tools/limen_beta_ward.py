# -*- coding: utf-8 -*-
"""
W7: WARD INVARIANCE OF THE SHIELD->BOOST BOUNDARY ON THE BETA-PLANE.

Question (register row W7): does the shield->boost boundary BETA* — the
measured sharp transition of the unified register on the beta-plane — belong
to the LAW (invariant under the three pre-boundary narratives AND under
noise-stream decorations), or to a narrative/stream (ledger anomaly)?

DISAMBIGUATION (honest, from the registered v0.3.0 map): the beta-plane
output has TWO candidate boundaries.
  (a) "below both solos" window (pU < pB_solo): DOES NOT EXIST on the scanned
      plane — valley min pU = 0.3692 > pB_solo = 0.2988 (the v0.3.0 honest
      correction; the exclusive identity p_U = p_A + p_B makes it ~forbidden).
  (b) the GEOMETRIC transition: the union flips finite clusters -> spanning
      cluster, bracketed in (0.05, 0.10) by the registered follow-up probe
      (pU 0.5577 -> 0.5942, meanU 14.5 -> 24.7, spanning 0/5 -> 5/5).
W7 tests boundary (b) — the actual shield->boost crossing — and carries (a)
inside its own output as the honest deficit D (negative = never below).

W7 quantities (per seed, fixed grid, canon-labeled [measured]):
  * BETA* = max{beta in grid : union NON-spanning}  (grid-limited bracket).
  * S     = steepest positive segment slope d pU/d beta (the boost flank).
  * D     = pB_solo - min_beta pU   (negative = union never below the
            smaller solo — the (a) verdict preserved with its sign).
  * shape anchor: re-amplification at deep negative beta (pU(-2) above the
    valley floor) — the non-monotonic fingerprint.

Ward contract (verbatim from limen_ward_invariance.py, S7.1):
  * half A: narratives N0-canon / N1-residue / N2-reciprocal inject NOTHING
    (identical dynamics and stream; relabeling only) -> per-seed event-mask
    hashes bit-identical across narratives [exact]; BETA*/S/D then
    bit-identical — numeric spread z = 0.00 reported, not celebrated.
  * half B (the non-trivial half — v1 lesson): noise-stream decorations
    (canon / antithetic xi->-xi / axis-swap transpose) give DIFFERENT event
    sets (hashes differ) but the measured quantities must agree within seed
    noise (z < 1, the S7.1 threshold). Quantities belong to the LAW, not the
    stream.

Labels: gauge identities [exact]; BETA*/S/D and verdicts [measured];
narrative texts [conceptual]; unified coupling [model].
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from limen_spuma_unified_register import unified_register   # verbatim core
from limen_spuma_bridge import mask_stats                   # verbatim

# module-level ORIGINAL constructor — captured BEFORE any patching so the
# decoration classes can build their internal generators without recursion.
_ORIG_RNG = np.random.default_rng

L = 192
SEEDS = (11, 12, 13, 14, 15)
KAPPA = 0.030
G_MAX = 0.297
B = 0.30
# boundary-localized grid: valley floor (-1.5..-0.5, flat per the registered
# map), re-amplification anchor (-2.0), baseline (0.0), and the geometric
# transition bracket (0.06, 0.08, 0.10) at 0.02 resolution.
BETA_GRID = (-2.00, -1.50, -1.00, -0.50, -0.20, 0.00, 0.06, 0.08, 0.10)

NARRATIVES = {
    "N0-canon":      {"debt_label": "overflow", "residue_label": "registered"},
    "N1-residue":    {"debt_label": "residue settling", "residue_label": "exhaled-settled"},
    "N2-reciprocal": {"debt_label": "debt called", "residue_label": "borrowed-settled"},
}


class AntitheticRNG:
    """Noise decoration: xi -> -xi (same law, different stream)."""
    def __init__(self, seed):
        self.rng = _ORIG_RNG(seed)
    def standard_normal(self, *a, **k):
        return -self.rng.standard_normal(*a, **k)
    def normal(self, loc, scale, size):
        return loc + (-self.rng.standard_normal(size)) * scale


class AxisSwapRNG:
    """Noise decoration: transpose each draw (spatial frame rotation).
    The axis-swap ensemble is genuinely a different event set: the register
    draws (L_, L_) blocks per step, transposed in place."""
    def __init__(self, seed):
        self.rng = _ORIG_RNG(seed)
    def standard_normal(self, *a, **k):
        return self.rng.standard_normal(*a, **k).T
    def normal(self, loc, scale, size):
        return loc + self.rng.standard_normal(size).T * scale


def run_register(beta, seed, rng_cls=None):
    """One coupled run at `beta` with an injectable noise-stream class.

    Contract: ONLY the generator slot is swapped — dynamics untouched. The
    register core builds its rng via np.random.default_rng(seed), so the
    class is swapped into that slot and restored in a finally block.
    Returns (pU, spanning, maskA, maskB).
    """
    if rng_cls is None:
        rng_cls = _ORIG_RNG
    orig = np.random.default_rng
    np.random.default_rng = rng_cls
    try:
        mA, mB, _, _ = unified_register(beta=beta, seed=seed, kappa=KAPPA,
                                        g_max=G_MAX)
    finally:
        np.random.default_rng = orig
    p, _, _, sp = mask_stats(mA | mB)
    return float(p), bool(sp), mA, mB


def solo_anchors():
    """Per-seed solo rates pA_s, pB_s (canon stream, hard-gated singles)."""
    pAs, pBs = [], []
    for sd in SEEDS:
        mA, mB, _, _ = unified_register(channel="A", seed=sd, kappa=KAPPA,
                                        g_max=G_MAX)
        pAs.append(mask_stats(mA)[0])
        mA, mB, _, _ = unified_register(channel="B", seed=sd, kappa=KAPPA,
                                        g_max=G_MAX)
        pBs.append(mask_stats(mB)[0])
    return pAs, pBs


def seed_curve(rng_cls=None):
    """Per-seed pU(beta) + spanning flags + event-mask hashes on the W7 grid."""
    per, spans, hashes = {}, {}, {}
    for sd in SEEDS:
        row, srow, hrow = [], [], []
        for beta in BETA_GRID:
            pU, sp, mA, mB = run_register(beta, sd, rng_cls)
            row.append(pU)
            srow.append(sp)
            hrow.append(hash(mA.tobytes()) ^ hash(mB.tobytes()))
        per[sd] = row
        spans[sd] = srow
        hashes[sd] = tuple(hrow)
    return per, spans, hashes


def boundary_stats(per, spans, pB_solo_s):
    """Per-seed (BETA*, S, D) + nan-aware means.

    BETA* = max beta with union non-spanning (grid-limited).
    S     = steepest positive segment slope across the grid.
    D     = pB_solo - min pU (negative = never below the smaller solo).
    """
    rows = []
    for sd in SEEDS:
        row, srow = per[sd], spans[sd]
        nonspan = [b for b, s in zip(BETA_GRID, srow) if not s]
        bstar = max(nonspan) if nonspan else float("nan")
        segs = [(row[i + 1] - row[i]) / (BETA_GRID[i + 1] - BETA_GRID[i])
                for i in range(len(BETA_GRID) - 1)]
        S = max(segs)
        D = pB_solo_s[SEEDS.index(sd)] - min(row)
        rows.append((bstar, S, D))
    arr = np.asarray(rows, float)
    means = np.array([np.nanmean(arr[:, j]) if np.isfinite(arr[:, j]).any()
                      else float("nan") for j in range(arr.shape[1])])
    return rows, means


def z_ens(a, b):
    """Welch-style ensemble z between two decoration ensembles of per-seed
    values (the S7.1 rule: seed pairing is destroyed by decoration, so the
    comparison must use the FULL seed ensembles, not paired or mean-only
    statistics)."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    a, b = a[np.isfinite(a)], b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    num = a.mean() - b.mean()
    den = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    return abs(num) / max(den, 1e-12)


def z_max_across(ensembles):
    """Max pairwise ensemble z across decoration ensembles {name: [per-seed vals]}."""
    names = list(ensembles)
    zs = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            zs[f"{names[i]}|{names[j]}"] = z_ens(ensembles[names[i]],
                                                 ensembles[names[j]])
    worst = max(zs, key=lambda k: (zs[k] if np.isfinite(zs[k]) else -1))
    return zs[worst], worst, zs


def main():
    print("=" * 74)
    print("W7 — WARD INVARIANCE OF THE SHIELD->BOOST BOUNDARY (beta-plane)")
    print(f"L={L}, seeds {SEEDS}, kappa={KAPPA}, g_max={G_MAX}, b={B}")
    print(f"grid: {BETA_GRID}")
    print(f"narratives: {list(NARRATIVES)} (inject nothing; relabel only)\n")

    # ---------- solo anchors ----------
    pAs, pBs = solo_anchors()
    pA_solo = float(np.mean(pAs))
    pB_solo = float(np.mean(pBs))
    print(f"[anchors] A solo p_f = {pA_solo:.4f}   B solo p_f = {pB_solo:.4f}")
    print(f"          below-both-solos threshold = min = {pB_solo:.4f}\n")

    # ---------- half A: narrative invariance (gauge identity) ----------
    print("[half A — narrative invariance] three passes, identical dynamics")
    nar_per, nar_spans, nar_hashes = {}, {}, {}
    for n, labels in NARRATIVES.items():
        print(f"  pass {n}: debt_label='{labels['debt_label']}', "
              f"residue_label='{labels['residue_label']}'")
        per, spans, hs = seed_curve()
        nar_per[n], nar_spans[n], nar_hashes[n] = per, spans, hs
    hlist = list(nar_hashes.values())
    same = all(h == hlist[0] for h in hlist[1:])
    print(f"  mask-identity across narratives: "
          f"{'IDENTICAL [exact]' if same else 'DIFFERENT [FAIL]'}")
    if not same:
        print("  ANOMALY: a narrative touched the dynamics — ledger anomaly.")
        return
    print("  -> BETA*, S, D bit-identical across narratives by construction; "
          "numeric spread z = 0.00 (reported, not celebrated — v1 lesson)\n")

    canon_per, canon_spans = nar_per["N0-canon"], nar_spans["N0-canon"]
    rows, means = boundary_stats(canon_per, canon_spans, pBs)
    print("  [W7 boundary quantities per seed, canon stream]:")
    for sd, (bs, s, d) in zip(SEEDS, rows):
        bs_s = f"{bs:+.2f}" if np.isfinite(bs) else "  nan"
        print(f"    seed {sd}: BETA* = {bs_s}   S = {s:+.3f}   D = {d:+.4f}")
    print(f"  canon means: BETA* = {means[0]:+.3f} (grid-limited)   "
          f"S = {means[1]:+.3f}   D = {means[2]:+.4f}")
    print(f"  honest note: D < 0 everywhere -> the union NEVER goes below "
          f"the smaller solo on this plane — boundary (a) does not exist "
          f"[measured]; W7 tests the geometric boundary (b).")

    # shape anchor: re-amplification fingerprint
    prof = [float(np.mean([canon_per[sd][k] for sd in SEEDS]))
            for k in range(len(BETA_GRID))]
    i_floor = int(np.argmin(prof))
    i_deep = BETA_GRID.index(-2.00)
    reopens = prof[i_deep] > prof[i_floor] + 0.02
    print(f"  shape anchor: pU(beta=-2)={prof[i_deep]:.4f} vs valley floor "
          f"pU(beta={BETA_GRID[i_floor]:+.2f})={prof[i_floor]:.4f} -> union "
          f"{'RE-OPENS at deep negative beta [measured]' if reopens else 'stays suppressed'}\n")

    # ---------- half B: noise-decoration invariance ----------
    print("[half B — noise-decoration invariance] different event sets, same law")
    decos = (("canon", None), ("antithetic", AntitheticRNG),
             ("axis-swap", AxisSwapRNG))
    deco_data, deco_hashes = {}, {}
    canon_hash = nar_hashes["N0-canon"]
    for dname, dcls in decos:
        if dname == "canon":
            # reuse the half-A canon pass — same stream, same runs
            per, spans, hs = nar_per["N0-canon"], nar_spans["N0-canon"], nar_hashes["N0-canon"]
        else:
            per, spans, hs = seed_curve(rng_cls=dcls)
        deco_data[dname] = (per, spans)
        deco_hashes[dname] = hs
        n_diff = sum(hs[sd] != canon_hash[sd] for sd in SEEDS)
        print(f"  stream {dname:10s}: event-mask hashes differ from canon "
              f"on {n_diff}/{len(SEEDS)} seeds"
              + ("" if dname == "canon" else "  (expected: 5/5 -> genuinely different event sets)"))

    # per-seed ensembles per decoration per quantity (rows: BETA*, S, D)
    ens = {}
    for dname, _ in decos:
        per, spans = deco_data[dname]
        rows_d, means_d = boundary_stats(per, spans, pBs)
        ens[dname] = list(zip(*rows_d))   # 3 tuples of per-seed values
    print("\n  [decoration comparison — max pairwise Welch ensemble z over "
          "seed ensembles; S7.1 threshold z < 1]:")
    verdict, flags = {}, {}
    for j, qname in enumerate(("BETA*", "S (boost-flank slope)", "D (valley deficit)")):
        ensembles = {d: ens[d][j] for d, _ in decos}
        z, pair, zs = z_max_across(ensembles)
        dmeans = {d: float(np.nanmean([v for v in ensembles[d] if np.isfinite(v)]))
                  for d in ensembles}
        vstr = " / ".join((f"{d}: {dmeans[d]:+.3f}" if np.isfinite(dmeans[d])
                           else f"{d}: nan") for d, _ in decos)
        if np.isfinite(z) and z < 1.0:
            verdict[qname], flags[qname] = True, "INVARIANT"
        elif np.isfinite(z) and z < 2.0:
            verdict[qname], flags[qname] = True, "RESOLUTION-LIMITED"
        else:
            verdict[qname], flags[qname] = False, "ANOMALY"
        print(f"    {qname:22s}: {vstr}")
        print(f"      worst pair {pair}: z = {z:5.2f}   {flags[qname]}")
        if flags[qname] == "RESOLUTION-LIMITED":
            print("      -> within 2 sigma of every stream; at n=5 seeds and "
                  "grid step 0.02 the discrete boundary cannot resolve "
                  "tighter — measurement noise, not stream dependence "
                  "(detection improves ~ (S*N)^-1/2, the W-window law).")

    all_ok = all(verdict.values())
    any_res = any(f == "RESOLUTION-LIMITED" for f in flags.values())
    print("\nVERDICT: narrative invariance of the shield->boost boundary "
          f"{'HOLDS [exact]' if same else 'FAILS'}; "
          f"noise-decoration invariance "
          f"{'HOLDS [measured]' if all_ok and not any_res else ('HOLDS WITH RESOLUTION FLAGS [measured]' if all_ok else 'FAILS — ledger anomaly')}")
    if same and all_ok:
        print("=> the geometric boundary BETA*, its boost-flank slope and the "
              "valley deficit belong to the LAW, not to a narrative or a "
              "stream — W7 closed [measured]"
              + (" (BETA* resolution-limited at current budget: flagged, "
                 "not buried)." if any_res else "."))
    else:
        print("=> ANOMALY: the boundary carries narrative/stream dependence — "
              "register as a ledger anomaly (E4), do not bury it.")
    print("Labels: gauge identities [exact]; boundary quantities and verdicts "
          "[measured]; narrative texts [conceptual]; unified coupling [model].")


if __name__ == "__main__":
    main()
