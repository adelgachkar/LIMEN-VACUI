# -*- coding: utf-8 -*-
"""
W4c: THE F3 MIGRATION GATE — what companion data turns S→W into a REGISTERED EVENT.

Register row F3 (LIMEN 08_Protocol/Two-Realm-Register):
    "are the imported constants (dtheta, phi_max, f_c) derivable in-model?
     realm: revere | deriving without aligned data = E1;
     the values stay 'imported and labeled' (the honesty triad)"

Migration rule (verbatim): "S->W: every new tool+data+norm alignment
(new empirical data or a newly adopted axiom) makes a realm-2 flag a migration
candidate — migration must be a REGISTERED EVENT, not a hope."

W4c does NOT migrate anything and does NOT manufacture data. It builds the
GATE that any future companion data must pass — so that when data arrives,
the migration is a machine-readable event with pre-committed thresholds
(no post-hoc fitting, no E1 by construction), demonstrated in-silico on
simulated data with FULL [sim] labels.

=======================================================================
THE F3 LEDGER (three flagged constants, each with its import channel)
=======================================================================
  dtheta  7.356103deg  [exact/closed geometry of the packing]  imported as:
          synthetic-gate / phase-debt root  (Companion-Bridge constants table)
          in-model role MEASURED in two channels:
            magnitude channel W4 : even/odd flatness ~ dtheta/2pi
            direction  channel W4b: mirror-parity split, chiral eigenmodes
  phi_max pi/sqrt(18) = 0.7405 [exact/closed Kepler bound] imported as:
          saturation-density ceiling (SPUMA cavity densification)
  f_c     kappa/pi ~ 30 THz  [derived chain kappa(g)=0.025 g^2 omega_0]
          imported as the K1 freezing edge (h f_c ~ 0.12 eV); the operator
          itself is registered (W5: one operator, two clocks).

WHY F3 HOLDS TODAY: all three enter through closed geometry of a model.
A closed form is "exact/closed [exact model]" — it is NOT nature-aligned:
no natural system has registered this packing as measured. Deriving them
"in-model" is circular (the model assumes its own geometry); deriving them
from the pre-boundary is E1. The ONLY honest exit: aligned companion data
(E1's own escape clause: "or a newly adopted axiom").

=======================================================================
THE GATE (the design contribution of W4c)
=======================================================================
Step 0  Declaration: name the table of the register row to migrate (F3),
        name the instrument, name the discipline thresholds BEFORE data.
Step 1  Companion dataset, machine-readable, with instrument metadata:
        geometric units, temperature ladder, resolution.
Step 2  D_1 — the OPPOSITION test: the pentagonal-deficit signature is a
        ABSENCE of the isotropic C4-invisible mode. Formally, the node
        splits the k=1 doublet by the flux f = dtheta/2pi:
            Delta omega_1^2 / omega_1^2 = 2 f (g_eff/g_ring)
        A tetrahedral node (isotropic, C4-analogue: exact doublets, no
        direction channel) predicts Delta = 0. A pentagonal node predicts
        Delta = 2f x 4.0e-3 = 1.635e-4 [model: W4b one-tube estimate].
        The gate: the MEASURED ratio Delta_meas/Delta_pred must match 1
        within the pre-committed discipline tolerance AND the sign/handed
        structure must show (magnitude-even, chirality-odd).
Step 3  D_2 — the CLOCK test: dtheta must also appear as the flatness
        amplitude of the magnitude channel (W4 language): |eta_meas -
        dtheta/2pi| / (dtheta/2pi) <= tau_flat. Independent of D_1's
        instrument (wall spectroscopy vs mode splitting).
Step 4  D_3 — the OPERATOR test: the same measured nodes must accept the
        registered operator kappa(g) = 0.025 g^2 omega_0: the fit must
        return the registered exponent 2 within tolerance.
Step 5  Verdict: MIGRATE (row F3 -> work with a named next-row tool) only
        if ALL gates pass on the SAME aligned dataset; the migration event
        is then a register edit with the dataset as anchor. Any single
        failure = stay revere (honest), with the failing gate named.
        NO-GO forever (never W): if the data instead shows the isotropic
        node WITHOUT the direction channel AND the operator is absent —
        then the corpus vocabulary is not nature's; S1/S2 absorb it.

In-silico demonstration (labeled [sim] end-to-end):
  * simulate TWO companion nodes from the registered vocabulary:
      node A "pentagonal"  : doublet split 2f g_eff, chiral eigenvectors,
                             flatness amplitude eta = f, operator kappa(g).
      node B "isotropic"   : machine-tie doublets, NO split, NO chiral
                             address, operator present (the control).
  * run the gate on A  -> expect all three D gates PASS  -> MIGRATION event
    demonstrated (on [sim] data — a demonstration of the gate, NOT a
    nature claim).
  * run the gate on B  -> expect D_1/D_2 FAIL, gate stays revere, named.
  * adversarial A': correct doublet split but WRONG flatness sign —
    demonstrates that the gate catches a model that mimics D_1 only.

All thresholds are fixed at the top; the battery never reads its inputs
except through the declared interface.

Labels: [exact] registered constants/identities; [model] the W4b one-tube
magnitude; [sim] every simulated number; [measured] reserved for future
aligned companion data (never used in this run).
"""

import json
import math
import cmath
import numpy as np
from dataclasses import dataclass, field, asdict

# ------------------------------------------------------------------ #
# S0. DECLARED GATE CONSTANTS — pre-committed, never tuned below      #
# ------------------------------------------------------------------ #
DEG = math.pi / 180.0
DTHETA = 2 * math.pi - 5 * math.acos(1.0 / 3.0)             # [exact/closed]
assert abs(DTHETA - 7.356103 * DEG) < 1e-7, "delta-theta registry mismatch"
F_FLUX = DTHETA / (2 * math.pi)                             # 0.0204336 [exact]

GATE = {
    "register_row": "F3",
    "instrument": "aligned companion node spectroscopy (to be named by data)",
    "tol_split_ratio": 0.30,      # D_1: |Delta_meas/Delta_pred - 1| <= 0.30
    "tol_flatness":    0.30,      # D_2: |eta_meas/f - 1|            <= 0.30
    "tol_operator":    0.15,      # D_3: |power_meas - 2| / 2        <= 0.15
    "tol_chirality":   0.50,      # D_1b: one-term chirality dominance
    "pred_split_ratio": 2 * F_FLUX * 4.0e-3,   # [model] W4b one-tube g_eff/g_ring
    "pred_eta": F_FLUX,                        # [model] magnitude-channel amplitude
    "pred_operator_power": 2.0,                # [exact] kappa = 0.025 g^2 omega_0
}
GATE["pred_split_ratio"] = None   # set in main() after constants are fixed


# ------------------------------------------------------------------ #
# S1. THE COMPANION-DATA INTERFACE (what a real dataset must provide) #
# ------------------------------------------------------------------ #
@dataclass
class CompanionNode:
    """Machine-readable companion node record — the D1 contract.
    A REAL dataset fills this with [measured] values; this run [sim]."""
    name: str
    geometry: str                 # declared node geometry of the donor model
    omega1_sq: float              # fundamental (k=1) frequency^2
    doublet_split_abs: float      # |Delta omega^2| across the k=1 mirror pair
    chirality_dominance: float    # 0 = balanced two-term; 1 = one-term chiral
    flatness_eta: float           # five-fold flatness amplitude (magnitude channel)
    operator_fits: list = field(default_factory=list)  # [(g, kappa/omega0), ...]
    instrument: dict = field(default_factory=dict)
    label: str = "[sim]"          # will be "[measured]" only from real data


# ------------------------------------------------------------------ #
# S2. THE GATE ITSELF                                                 #
# ------------------------------------------------------------------ #
def run_gate(node: CompanionNode) -> dict:
    verdict = {
        "node": node.name, "declared_geometry": node.geometry,
        "data_label": node.label, "gates": {}, "violations": [],
    }

    # D_1 — opposition: the split magnitude matches the registered [model] prediction
    ratio = node.doublet_split_abs / GATE["pred_split_ratio"]
    ok1 = abs(ratio - 1.0) <= GATE["tol_split_ratio"]
    verdict["gates"]["D1_opposition_split"] = {
        "measured_ratio": round(ratio, 6), "tolerance": GATE["tol_split_ratio"],
        "pass": bool(ok1),
    }

    # D_1b — direction structure: chiral one-term eigenmodes (W4b signature)
    ok1b = node.chirality_dominance >= GATE["tol_chirality"]
    verdict["gates"]["D1b_direction_chirality"] = {
        "measured_dominance": round(node.chirality_dominance, 6),
        "tolerance": GATE["tol_chirality"], "pass": bool(ok1b),
    }

    # D_2 — clock: the magnitude channel re-measures the SAME constant
    eta_ratio = node.flatness_eta / GATE["pred_eta"]
    ok2 = abs(eta_ratio - 1.0) <= GATE["tol_flatness"]
    verdict["gates"]["D2_clock_flatness"] = {
        "measured_eta_over_f": round(eta_ratio, 6),
        "tolerance": GATE["tol_flatness"], "pass": bool(ok2),
    }

    # D_3 — operator: kappa/omega0 = 0.025 * g^2 (registered, W5)
    fits = node.operator_fits
    if len(fits) >= 2:
        gs = np.array([g for g, _ in fits], float)
        ys = np.array([y for _, y in fits], float)
        power, amp = np.polyfit(np.log(gs), np.log(ys), 1)
        ok3 = abs(power - GATE["pred_operator_power"]) / GATE[
            "pred_operator_power"] <= GATE["tol_operator"]
        verdict["gates"]["D3_operator"] = {
            "fitted_power": round(float(power), 6),
            "fitted_amp": round(float(amp), 8),
            "registered_power": GATE["pred_operator_power"],
            "tolerance": GATE["tol_operator"], "pass": bool(ok3),
        }
    else:
        ok3 = False
        verdict["gates"]["D3_operator"] = {
            "pass": False, "reason": "operator ladder missing (<2 points)"}

    all_pass = ok1 and ok1b and ok2 and ok3
    verdict["verdict"] = "MIGRATE — register row F3 -> work (event: registered)" \
        if all_pass else "STAY REVERE — F3 unchanged (honest)"
    return verdict


# ------------------------------------------------------------------ #
# S3. IN-SILICO NODE BUILDERS — the registered vocabulary, simulated  #
# ------------------------------------------------------------------ #
def build_pentagonal_node(seed: int = 42) -> CompanionNode:
    """[sim] Pentagonal node: the W4b physics at f = dtheta/2pi.
    doublet split |Delta w^2| = 2 f g_eff/g_ring * w0^2  (direction channel)
    flatness eta = f                                        (magnitude channel)
    operator kappa/omega0 = 0.025 g^2                        (registered)
    Simulation adds O(1e-3) instrument noise; label stays [sim]."""
    rng = np.random.default_rng(seed)
    w0 = 1.0
    noise = 1e-3 * rng.standard_normal()
    split = 2 * F_FLUX * 4.0e-3 * w0**2 * (1 + noise)          # [model] x [sim noise]
    return CompanionNode(
        name="nodeA-pentagonal",
        geometry="pentagonal-deficit node (declared donor geometry)",
        omega1_sq=w0**2,
        doublet_split_abs=abs(split),
        chirality_dominance=0.995 * (1 + 1e-4 * rng.standard_normal()),
        flatness_eta=F_FLUX * (1 + 5e-3 * rng.standard_normal()),
        operator_fits=[(g, 0.025 * g**2 * (1 + 2e-3 * rng.standard_normal()))
                       for g in (0.57, 0.70, 0.80)],
        instrument={"units": "geometric (a=1)", "resolution": "1e-4",
                    "seed": seed},
        label="[sim]",
    )


def build_isotropic_node(seed: int = 7) -> CompanionNode:
    """[sim] Isotropic control: exact machine-tie doublets (no direction
    channel), no five-fold flatness — the C4-analogue signature."""
    rng = np.random.default_rng(seed)
    w0 = 1.0
    return CompanionNode(
        name="nodeB-isotropic",
        geometry="isotropic node (control; C4 analogue, exact doublets)",
        omega1_sq=w0**2,
        doublet_split_abs=1e-12,                      # machine tie, no channel
        chirality_dominance=0.02,                     # balanced eigenmodes
        flatness_eta=2e-4,                            # ~ 1% of f — noise floor
        operator_fits=[(g, 0.025 * g**2 * (1 + 1e-3 * rng.standard_normal()))
                       for g in (0.57, 0.80)],
        instrument={"units": "geometric (a=1)", "resolution": "1e-4",
                    "seed": seed},
        label="[sim]",
    )


def build_mimic_node(seed: int = 11) -> CompanionNode:
    """[sim] Adversarial mimic: correct D_1 split but WRONG flatness sign —
    a model that carries the direction channel yet contradicts the
    magnitude channel. The gate must catch it at D_2."""
    node = build_pentagonal_node(seed)
    node.name = "nodeA2-mimic-split-only"
    node.flatness_eta = -0.5 * F_FLUX      # right order, WRONG sign
    return node


# ------------------------------------------------------------------ #
# S4. CHIRALITY CHECK — the W4b eigenvector signature, restated       #
# ------------------------------------------------------------------ #
def chiral_dominance_from_mode(s: complex, c: complex) -> tuple:
    """W4b one-term chirality, restated in the (s, c) standing-wave basis:
    a pure traveling wave has (s, c) = (1, ±i)/sqrt2, i.e. s ∓ ic -> 0.
    Returns (dominance in [0,1], handedness string). dominance 1 = fully
    chiral one-term; 0 = standing wave (equal in-phase terms)."""
    plus_mag  = abs(s + 1j * c)     # vanishes for the (1, -i) handedness
    minus_mag = abs(s - 1j * c)     # vanishes for the (1, +i) handedness
    lo, hi = min(plus_mag, minus_mag), max(plus_mag, minus_mag)
    dom = 1.0 - (lo / hi if hi > 0 else 1.0)
    hand = "(+i)-wave" if plus_mag < minus_mag else "(-i)-wave"
    return dom, hand


def demonstrate_chiral_address():
    """[exact] The direction channel's fingerprint, restated on the 2x2
    effective Hamiltonian exactly as the W4b register carries it: the
    raised branch at +f and at -f are BOTH fully chiral one-term modes
    with OPPOSITE handedness (chirality-odd, H(-f) = H(f)*)."""
    f, g = F_FLUX, 4.0e-3
    lam_p = np.array([[0.0, 1j * f * g], [-1j * f * g, 0.0]])
    _, vp = np.linalg.eigh(lam_p)
    s_p, c_p = vp[:, 1]                      # raised branch at +f
    dom_p, hand_p = chiral_dominance_from_mode(s_p, c_p)
    lam_m = np.array([[0.0, -1j * f * g], [1j * f * g, 0.0]])
    _, vm = np.linalg.eigh(lam_m)
    s_m, c_m = vm[:, 1]                      # raised branch at -f
    dom_m, hand_m = chiral_dominance_from_mode(s_m, c_m)
    return {
        "raised_branch_dominance_at_plus_f": round(dom_p, 8),
        "raised_branch_handedness_at_plus_f": hand_p,
        "raised_branch_dominance_at_minus_f": round(dom_m, 8),
        "raised_branch_handedness_at_minus_f": hand_m,
        "chirality_odd_flip": bool(hand_p != hand_m),
        "label": "[exact] (2x2 algebra; simulation only of noise levels)",
    }


# ------------------------------------------------------------------ #
# S5. THE BATTERY                                                     #
# ------------------------------------------------------------------ #
def main() -> int:
    GATE["pred_split_ratio"] = round(2 * F_FLUX * 4.0e-3, 8)
    print("=" * 74)
    print("W4c — THE F3 MIGRATION GATE (what data turns S->W into an event)")
    print("=" * 74)
    print(f"registered row: {GATE['register_row']}   "
          f"dtheta = {math.degrees(DTHETA):.6f} deg  [exact/closed]")
    print(f"flux f = dtheta/2pi = {F_FLUX:.7f}  [exact]")
    print(f"pred split |dw^2|/w0^2 = 2 f (g_eff/g_ring) = "
          f"{GATE['pred_split_ratio']:.6e}  [model: W4b one-tube]")
    print("pre-committed tolerances: split 0.30 | flatness 0.30 | "
          "operator 0.15 | chirality 0.50")
    print()
    print("-" * 74)
    print("S1 — the companion-data contract (what a REAL dataset must carry)")
    print("-" * 74)
    for line in [
        "  1. node table: geometry declared, k=1 doublet, chiral eigenvectors",
        "  2. magnitude channel: five-fold flatness amplitude of the wall",
        "  3. operator ladder: kappa/omega0 at >= 2 declared g-points",
        "  4. instrument metadata: units, temperature ladder, resolution",
    ]:
        print(line)
    print()
    print("-" * 74)
    print("S2 — direction-channel fingerprint restated [exact 2x2 algebra]")
    print("-" * 74)
    fp = demonstrate_chiral_address()
    for k, v in fp.items():
        print(f"  {k:38s} = {v}")
    print()

    results = {}
    for builder, expect in (
        (build_pentagonal_node, "ALL PASS -> MIGRATE demonstrated"),
        (build_isotropic_node,  "D1/D1b/D2 FAIL -> stays revere, named"),
        (build_mimic_node,      "D2 FAIL -> mimic caught (not buried)"),
    ):
        node = builder()
        print("-" * 74)
        print(f"S3 — gate on {node.name}   ({expect})")
        print("-" * 74)
        verdict = run_gate(node)
        for gname, g in verdict["gates"].items():
            state = "PASS" if g["pass"] else "FAIL"
            detail = {k: v for k, v in g.items() if k != "pass"}
            print(f"  [{state}] {gname:26s} {detail}")
        print(f"  ==> VERDICT: {verdict['verdict']}")
        results[node.name] = verdict
        print()

    print("=" * 74)
    print("S4 — MACHINE-READABLE MIGRATION LEDGER (the W4c deliverable)")
    print("=" * 74)
    ledger = {
        "tool": "limen_w4c_f3_migration",
        "what_this_is": "pre-committed acceptance gate for the F3 row; "
                        "NOT a migration event and NOT data",
        "migration_rule": "S->W requires ALL gates on the SAME aligned "
                          "dataset; verdict is a register edit anchored to "
                          "the dataset",
        "no_go_forever": "isotropic node without direction channel AND "
                         "without operator -> S1/S2 absorb (not W)",
        "gate_constants": {k: v for k, v in GATE.items()},
        "in_sim_results": results,
        "honesty": "every simulated number [sim]; [measured] reserved for "
                   "future aligned data; no nature claim made",
    }
    out = json.dumps(ledger, indent=2, ensure_ascii=False)
    with open(__file__.replace(".py", "_ledger.json"), "w",
              encoding="utf-8") as fh:
        fh.write(out)
    print(out)
    print()
    print("ledger written -> limen_w4c_f3_migration_ledger.json")
    print("STATUS: gate BUILT and DEMONSTRATED in-silico — row F3 stays "
          "revere until real aligned data passes the same gate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
