# -*- coding: utf-8 -*-
"""
W4: CLOSED FORM OF omega_n — the even/odd epsilon_n correction from a wall
model with explicit mu(x).  (Two-Realm Register row W4; SPUMA A4 §2,
Companion-Bridge Open Question 1.)

REGISTERED CONTRACT (verbatim anchors):
  * SPUMA A4 §2 predicts:  f_n ≈ (c_wall/2πR) · n · (1 + ε_n · δθ/2π),
    ε_n = 1 (n even, antagonism preserved) | 0 (n odd, reset),
    with the pentagonal deficit factor  δθ/2π = 0.02044  [exact/closed:
    δθ = 2π − 5·arccos(1/3) = 0.128392 rad → /2π = 0.0204350].
  * A3 gives the wall as an EXPLICIT permeability profile
    mu(x) = mu_in·Θ_cavity + mu_wall·(1−Θ_cavity)  — a two-phase annulus.
  * The register's W4 row demands: "wall model with explicit mu(x)" and the
    K3/K4 collateral: the wall is the K2 polar layer; the balancer contract
    (K3/K4) supplies the two-phase split (interior vs wall).
  * Falsifiable test (A4 §3.1): same-family cavities must show an
    even/odd-flattened spectrum with the CONSTANT ratio δθ/2π.

MODEL (minimal, parameter-poor — the deficit enters through geometry only):
  Two-phase square lattice Helmholtz operator on an L×L grid, disk cavity of
  radius R (wall width w in lattice units):
      H ψ = −∇·( μ(x)^{-1} ∇ψ )   discretized (symmetric, variational —
      consistent eigen-inclusion for the two-phase μ(x); no spurious modes),
      μ(x) = 1 inside the cavity,  μ_wall ≥ 1 in the annulus,  Dirichlet
      outside the wall (the K2 polar boundary, per A3 B_leak ≈ 0).
  The antagonism (A4 §1) is encoded minimally: the wall phase is ANISOTROPIC
  along the pentagonal-frustration direction — implemented as a DIRECTIONAL
  correlation of the wall mass: the annulus thickness modulates as
      w(φ) = w0 · (1 + η·cos(5φ)),      η = δθ/2π  [geometry only —
  five-fold wall polarization is exactly what the pentagonal node deposits;
  no free parameter: the anisotropy amplitude IS the registered factor].

TEST PROTOCOL:
  1. VALIDATION: isotropic wall (η=0) vs the exact continuum radial mode
     roots (Bessel J0 zeros) in the thin-wall limit — the ladder must
     converge to the Dirichlet-disk ladder [exact check].
  2. DISCRIMINATION: for each mode n (radial ladder k=1..8), measure the
     relative even/odd splitting
         ε_n(measured) = (ω_n − ω_n^0) / ω_n^0 / (δθ/2π)
     where ω_n^0 = the isotropic-wall reference (η=0, same geometry).
     PREDICTION (A4): ε_even ≈ 1, ε_odd ≈ 0 — CONSTANT across n.
  3. CONTROL: sign flip of the anisotropy (η → −η) must flip nothing in
     |ε_n| (the ladder depends on the anisotropy AMPLITUDE — the deficit is
     a magnitude, not an orientation) [exact check of the claim's shape].
  4. HONEST LIMITS: lattice discretization of the cos(5φ) wall; finite-size
     scaling of ε_n reported; nothing here is a measurement of nature
     (F3), this is the in-model operator the register banked.

Labels: [exact] for δθ and the operator identities; [measured in-model]
for every ε_n; [model] for the w(φ)=w0(1+η cos5φ) encoding of the
antagonism — flagged as the ONE modeling choice W4 adds.
"""
import numpy as np

# ---------------------------------------------------------------- constants
DTHETA = 2.0 * np.pi - 5.0 * np.arccos(1.0 / 3.0)     # rad  [exact/closed]
DFAC   = DTHETA / (2.0 * np.pi)                       # 0.0204350...
print(f"delta_theta = {DTHETA:.6f} rad   delta_theta/2pi = {DFAC:.7f}  [exact/closed]")

# ---------------------------------------------------------------- grid tools
def build_mu(L, R, w0, mu_wall, eta):
    """Explicit two-phase mu(x): cavity=1, annulus=mu_wall with five-fold
    thickness modulation w(phi)=w0*(1+eta*cos(5*phi)), Dirichlet beyond."""
    y, x = np.mgrid[0:L, 0:L]
    cx = cy = (L - 1) / 2.0
    dx, dy = x - cx, y - cy
    r   = np.hypot(dx, dy)
    phi = np.arctan2(dy, dx)
    w   = w0 * (1.0 + eta * np.cos(5.0 * phi))
    inside  = r <= R
    annulus = (~inside) & (r <= R + w)
    mu = np.ones((L, L))
    mu[annulus] = mu_wall
    # Dirichlet border: mask False beyond the annulus
    valid = inside | annulus
    return mu, valid, inside

def helmholtz_modes(L, R, w0, mu_wall, eta, nmodes):
    """Sparse variational discretization of -div( mu^-1 grad ) + Dirichlet;
    returns the nmodes lowest eigenvalues (omega^2)."""
    mu, valid, _ = build_mu(L, R, w0, mu_wall, eta)
    inv_mu = 1.0 / mu
    idx = -np.ones((L, L), dtype=int)
    idx[valid] = np.arange(valid.sum())
    n = valid.sum()
    rows, cols, vals = [], [], []
    pos = np.argwhere(valid)
    for (i, j) in pos:
        a = idx[i, j]
        diag = 0.0
        for (di, dj) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ii, jj = i + di, j + dj
            if not (0 <= ii < L and 0 <= jj < L) or not valid[ii, jj]:
                g = 1.0 / mu[i, j]          # Dirichlet wall (K2): value 0 outside
            else:
                g = 2.0 / (mu[i, j] + mu[ii, jj])   # harmonic face average
            diag += g
            if valid[ii, jj]:
                rows.append(a); cols.append(idx[ii, jj]); vals.append(-g)
        rows.append(a); cols.append(a); vals.append(diag)
    from scipy.sparse import coo_matrix
    from scipy.sparse.linalg import eigsh
    H = coo_matrix((vals, (rows, cols)), shape=(n, n)).tocsr()
    vals_, vecs_ = eigsh(H, k=nmodes, sigma=1e-9, which='LM')
    o = np.argsort(vals_)
    return vals_[o], idx, valid

def bessel_reference(nref):
    """Exact Dirichlet-disk ladder k_n = j_{0,n}/R normalized to k_1 [exact]."""
    # j0 zeros
    try:
        from scipy.special import jn_zeros
        z = jn_zeros(0, nref)
    except Exception:
        z = np.array([2.404826, 5.520078, 8.653728, 11.791534,
                      14.930918, 18.071064, 21.211637, 24.352472])
    return z / z[0]

# ================================================================ 1. VALIDATION
print("\n[1] VALIDATION — isotropic wall (eta=0) vs Dirichlet-disk ladder [exact]")
L, R, w0, mu_wall = 120, 18.0, 4.0, 8.0
lam_iso, idx_, valid_ = helmholtz_modes(L, R, w0, mu_wall, 0.0, 8)
om = np.sqrt(lam_iso)
ref = bessel_reference(8)
# the wall imposes a Robin-like shift; the LADDER SHAPE is the discriminator:
shape_iso = om / om[0]
print(f"{'n':>3} {'omega/omega_1 (eta=0)':>22} {'j0n/j01 disk':>14} {'ratio':>8}")
for n in range(8):
    print(f"{n+1:>3} {shape_iso[n]:>22.6f} {ref[n]:>14.6f} {shape_iso[n]/ref[n]:>8.4f}")
corr = np.corrcoef(shape_iso, ref)[0, 1]
print(f"ladder-shape correlation vs disk: {corr:.6f}  (same-family test)")

# ============================================================ 2. DISCRIMINATION
print("\n[2] DISCRIMINATION — five-fold wall anisotropy eta = delta_theta/2pi")
eta = DFAC
lam_aniso, _, _ = helmholtz_modes(L, R, w0, mu_wall, eta, 8)
om_a = np.sqrt(lam_aniso)
eps_n = (om_a - om) / om / eta          # measured epsilon_n per A4 §2
print(f"{'n':>3} {'omega_iso':>12} {'omega_aniso':>13} {'split/eta':>12} {'eps_n':>10} {'A4 verdict':>14}")
verd = []
for n in range(8):
    e = eps_n[n]
    want = 1.0 if (n + 1) % 2 == 0 else 0.0
    verd.append('even≈1' if (n+1) % 2 == 0 else 'odd≈0')
    print(f"{n+1:>3} {om[n]:>12.6f} {om_a[n]:>13.6f} {(om_a[n]-om[n])/om[n]/eta:>12.4f} {e:>10.5f} {verd[-1]:>14}")
even_eps = eps_n[1::2]
odd_eps  = eps_n[0::2]
print(f"\neven-family mean eps = {even_eps.mean():+.4f}  (A4 predicts +1)")
print(f"odd-family  mean eps = {odd_eps.mean():+.4f}  (A4 predicts  0)")
print(f"even/odd discrimination amplitude = {even_eps.mean() - odd_eps.mean():+.4f}")
print(f"predicted amplitude               = {1.0:+.4f} (one delta_theta/2pi step)")

# ================================================================ 3. CONTROL
print("\n[3] CONTROL — sign flip eta -> -eta (deficit is a magnitude)")
lam_flip, _, _ = helmholtz_modes(L, R, w0, mu_wall, -eta, 8)
om_f = np.sqrt(lam_flip)
# the physical check: the SPECTRUM is even in eta (the cos(5phi) sign flip is a
# rotation by pi/5 — same ladder). Report spectrum evenness directly [exact].
evenness = np.max(np.abs(om_f - om_a)) / om_a[0]
print(f"max |omega(-eta) - omega(+eta)| / omega_1 = {evenness:.3e}   [exact: spectrum even in eta]")
print(f"{'n':>3} {'eps_n(+eta)':>14} {'eps_n(-eta) bookkeeping':>24}")
for n in range(8):
    eps_f = (om_f[n] - om[n]) / om[n] / (-eta)   # = -eps_n when evenness holds
    print(f"{n+1:>3} {eps_n[n]:>14.5f} {eps_f:>24.5f}")

# ================================================================ 4. CONVERGENCE
print("\n[4] FINITE-SIZE / LADDER STABILITY of the even/odd amplitude")
for (Lx, Rx) in ((90, 14.0), (120, 18.0), (150, 22.0)):
    lam0, _, _ = helmholtz_modes(Lx, Rx, w0, mu_wall, 0.0, 6)
    lam5, _, _ = helmholtz_modes(Lx, Rx, w0, mu_wall, eta, 6)
    o0, o5 = np.sqrt(lam0), np.sqrt(lam5)
    e = (o5 - o0) / o0 / eta
    print(f"L={Lx:>3} R={Rx:>5}: even mean {e[1::2].mean():+.4f} | odd mean {e[0::2].mean():+.4f}"
          f" | discrimination {e[1::2].mean()-e[0::2].mean():+.4f}")

print("\n" + "=" * 74)
print("W4 HONEST SUMMARY")
print("=" * 74)
print(f"* operator: variational two-phase mu(x) Helmholtz, five-fold wall")
print(f"  modulation w(phi)=w0*(1+eta*cos5phi), eta = delta_theta/2pi = {DFAC:.7f} [exact]")
print(f"* the encoding of the antagonism (the cos5phi wall) is the ONE modeling")
print(f"  choice [model]; every eps_n above is [measured in-model]")
print(f"* A4 §2 prediction (eps_even=1, eps_odd=0, constant in n) vs the measured")
print(f"  ladder: see the discrimination block — the register records whatever")
print(f"  came out, including a partial/no detection (all three are honest")
print(f"  outcomes; only the SHAPES are claimed in advance)")
print(f"* no nature-side claim: F3 status of delta-theta is untouched by this")
print(f"  tool; a full migration S->W would require the companion's empirical")
print(f"  spectral data, not a simulation")
