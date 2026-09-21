# -*- coding: utf-8 -*-
"""
T6 — Middle-Atmosphere Synthesis tests (LIMEN-VACUI).

Source: the two "Middle-Atmosphere Inflation Dynamics" documents (EN v3.1.0 + FA)
claim a canonical three-layer system:

    O+   overdense core / generative void   -> positive drive  A_drive
    Cmid middle atmosphere / buffer layer   -> compensatory    A_comp
    D-   distal boundaries / deficit        -> negative pull   A_bdry

    A_total = A_drive - A_comp + A_bdry      (canonical three-component relation)
    claim 1: A_comp saturation prevents runaway -> bounded expansion
    claim 2: an observer embedded in Cmid sees sustained "atmospheric inflation"
             (both bounding fronts recede; the docs call it accelerating)
    claim 3: if the transfer rate exceeds relaxation capacity (Xi_mid > Xi_crit),
             excess gradient tension is shed as localized nucleation -> foam

Geometry (symmetric, right half x = 0 .. M; mirror at x = 0):
    x <  f_c        O+ core (constraint source, pushes outward)
    f_c < x < f_e   Cmid middle layer (elastic, damped = the compensator)
    x >  f_e        D- deficit (pulls outward)
Both fronts move OUTWARD (the middle layer widens = expansion). An observer
comoving with the shell sees both fronts recede.
"""

import numpy as np

N        = 1024                 # full domain; we simulate the right half
STEPS    = 6000
DX       = 1.0
DT       = 0.20
K        = 1.0                  # elastic modulus -> causal speed c = 1
GAMMA    = 0.05                 # Cmid relaxation (damping) = compensatory capacity
XI_CAP   = 1.5                  # velocity saturation (compensatory closure)
G_CRIT   = 1.5                  # gradient-tension nucleation threshold


def run_dynamics(xi_drive, xi_pull, nuc_cap=0):
    M = N // 2
    u = np.zeros(M)
    v = np.zeros(M)
    f_c = 0.10 * M               # core front (float position)
    f_e = 0.90 * M               # edge front
    gap_hist = np.empty(STEPS)
    nuc_times = []
    dt = DT

    for t in range(STEPS):
        ic, ie = int(f_c), int(f_e)
        ic = min(max(ic, 1), M - 2)
        ie = min(max(ie, ic + 2), M - 2)

        acc = K * (np.roll(u, 1) - 2 * u + np.roll(u, -1)) / DX**2
        acc -= GAMMA * v                    # A_comp: compensatory relaxation
        acc[0] = acc[-1] = 0.0

        # three-component drive, evaluated at the two fronts (outward = +x here)
        v[ic] += xi_drive * dt              # A_drive (O+ push)
        v[ie] += xi_pull * dt               # A_bdry  (D- pull)

        v += acc * dt
        v = np.clip(v, -XI_CAP, XI_CAP)     # A_comp saturation = closure
        u += v * dt

        # foam nucleation: gradient tension beyond capacity sheds locally
        g = np.abs(np.gradient(u, DX))
        hot = g > G_CRIT
        if nuc_cap and hot.any():
            u[hot] *= 0.5                   # tension shed (nucleation pulse)
            nuc_times.append(t)
            if len(nuc_times) >= nuc_cap:
                break

        # fronts advect with the local material velocity (outward on both)
        f_c = max(1.0, f_c + v[ic] * dt)
        f_e = min(float(M - 2), f_e + v[ie] * dt)
        gap_hist[t] = f_e - f_c

    return {"gap": gap_hist, "nuc_times": np.array(nuc_times),
            "f_c": f_c, "f_e": f_e, "v": v, "u": u,
            "hit_edge": f_e >= M - 3}


def classify_run(r):
    """Bounded vs runaway from the gap-RATE history (not the gap itself)."""
    g = r["gap"]
    rate = np.diff(g) / DT
    if r["hit_edge"]:
        return "runaway-to-edge"
    early = rate[:len(rate)//4].mean()
    late  = rate[-len(rate)//4:].mean()
    if late > early + 0.01 and late > 0.05:
        return "accelerating-runaway"
    if abs(late) <= 0.01:
        return "bounded-saturated"
    if late < early:
        return "bounded-decelerating"
    return "bounded-steady"


def t6a_bounded_phase_diagram():
    print("=" * 68)
    print("T6a — bounded expansion: does A_comp prevent runaway?")
    print("=" * 68)
    print(f"{'xi_drive':>9} {'xi_pull':>8} {'outcome':>22} {'late rate':>10}")
    rows = []
    for xd in (0.05, 0.10, 0.20, 0.40):
        for xp in (0.05, 0.10, 0.20):
            r = run_dynamics(xd, xp)
            cls = classify_run(r)
            rate = np.diff(r["gap"]) / DT
            late = rate[-len(rate)//4:].mean()
            rows.append((xd, xp, cls, late))
            print(f"{xd:>9.2f} {xp:>8.2f} {cls:>22} {late:>10.4f}")
    bounded = sum(1 for x in rows if x[2].startswith("bounded"))
    print(f"\nbounded in {bounded}/{len(rows)} cells "
          f"-> compensatory closure {'HOLDS' if bounded == len(rows) else 'FAILS'}")
    return rows


def t6b_embedded_observer():
    print()
    print("=" * 68)
    print("T6b — embedded observer in Cmid: recession & its time profile")
    print("=" * 68)
    r = run_dynamics(0.15, 0.10)
    g = r["gap"]
    rate = np.diff(g) / DT
    n = len(rate)
    segs = [rate[:n//3].mean(), rate[n//3:2*n//3].mean(), rate[2*n//3:].mean()]
    print(f"  middle-layer width : {g[0]:.0f} -> {g[-1]:.0f} sites "
          f"({100.0*(g[-1]-g[0])/g[0]:+.1f}%)  [+= expansion]")
    print(f"  front drift rate   : {segs[0]:+.4f} -> {segs[1]:+.4f} -> {segs[2]:+.4f} sites/time")
    peak_t = int(np.argmax(np.abs(rate)))
    print(f"  peak |rate| at t={peak_t} ({100.0*peak_t/STEPS:.0f}% of run)")
    drift_decay = abs(segs[2]) < abs(segs[0])
    quasi_static = abs(segs[-1]) <= 0.005
    print(f"  |drift| decays toward zero : {drift_decay}")
    print(f"  quasi-static buffer at long times (|rate|<=0.005): {quasi_static}")
    print(f"  -> in minimal membrane dynamics the buffer is BOUNDED and "
          f"{'quasi-static' if quasi_static else 'still drifting'};")
    print(f"     the docs' 'accelerating inflation' is a PROJECTION (P_obs) claim, "
          f"not an automatic consequence of the three-layer balance")
    return {"segs": segs, "quasi_static": quasi_static,
            "drift_decay": drift_decay}


def t6c_foam_threshold():
    print()
    print("=" * 68)
    print("T6c — foam nucleation threshold: Xi_mid > Xi_crit sheds tension")
    print("=" * 68)
    print(f"{'xi_drive':>9} {'nucleations':>12} {'first at t':>11}")
    table = []
    for xd in (0.10, 0.20, 0.40, 0.80, 1.20, 1.60, 2.00, 3.00):
        r = run_dynamics(xd, xd, nuc_cap=300)
        t0 = int(r["nuc_times"][0]) if len(r["nuc_times"]) else -1
        table.append((xd, len(r["nuc_times"]), t0))
        print(f"{xd:>9.2f} {len(r['nuc_times']):>12d} {t0:>11d}")
    crit = next((x for x, n, _ in table if n > 0), None)
    print(f"\nempirical Xi_crit ~ {crit} (drive rate where the middle layer first "
          f"exceeds relaxation capacity: damping {GAMMA} + velocity cap {XI_CAP})")
    return crit


if __name__ == "__main__":
    t6a_bounded_phase_diagram()
    t6b_embedded_observer()
    t6c_foam_threshold()
    print("\nT6 complete.")
